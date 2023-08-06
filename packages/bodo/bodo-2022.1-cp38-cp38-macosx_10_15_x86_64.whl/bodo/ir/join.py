"""IR node for the join and merge"""
from collections import defaultdict
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba import generated_jit
from numba.core import cgutils, ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, next_label, replace_arg_nodes, replace_vars_inner, visit_vars_inner
from numba.extending import intrinsic, overload
import bodo
from bodo.libs.array import arr_info_list_to_table, array_to_info, compute_node_partition_by_hash, delete_table, delete_table_decref_arrays, hash_join_table, info_from_table, info_to_array
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.str_arr_ext import copy_str_arr_slice, cp_str_list_to_array, get_bit_bitmap, get_null_bitmap_ptr, get_str_arr_item_length, get_str_arr_item_ptr, get_utf8_size, getitem_str_offset, num_total_chars, pre_alloc_string_array, set_bit_to, str_copy_ptr, string_array_type, to_list_if_immutable_arr
from bodo.libs.str_ext import string_type
from bodo.libs.timsort import getitem_arr_tup, setitem_arr_tup
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.utils.shuffle import _get_data_tup, _get_keys_tup, alloc_pre_shuffle_metadata, alltoallv_tup, finalize_shuffle_meta, getitem_arr_tup_single, update_shuffle_meta
from bodo.utils.typing import BodoError, dtype_to_array_type, find_common_np_dtype, is_dtype_nullable, is_nullable_type, to_nullable_type
from bodo.utils.utils import alloc_arr_tup, debug_prints, is_null_pointer
join_gen_cond_cfunc = {}
join_gen_cond_cfunc_addr = {}


@intrinsic
def add_join_gen_cond_cfunc_sym(typingctx, func, sym):

    def codegen(context, builder, signature, args):
        fwoiz__laaw = func.signature
        ekfn__botmo = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(64)])
        tazu__wtbdm = cgutils.get_or_insert_function(builder.module,
            ekfn__botmo, sym._literal_value)
        builder.call(tazu__wtbdm, [context.get_constant_null(fwoiz__laaw.
            args[0]), context.get_constant_null(fwoiz__laaw.args[1]),
            context.get_constant_null(fwoiz__laaw.args[2]), context.
            get_constant_null(fwoiz__laaw.args[3]), context.
            get_constant_null(fwoiz__laaw.args[4]), context.
            get_constant_null(fwoiz__laaw.args[5]), context.get_constant(
            types.int64, 0), context.get_constant(types.int64, 0)])
        context.add_linking_libs([join_gen_cond_cfunc[sym._literal_value].
            _library])
        return
    return types.none(func, sym), codegen


@numba.jit
def get_join_cond_addr(name):
    with numba.objmode(addr='int64'):
        addr = join_gen_cond_cfunc_addr[name]
    return addr


class Join(ir.Stmt):

    def __init__(self, df_out, left_df, right_df, left_keys, right_keys,
        out_data_vars, left_vars, right_vars, how, suffix_x, suffix_y, loc,
        is_left, is_right, is_join, left_index, right_index, indicator,
        is_na_equal, gen_cond_expr):
        self.df_out = df_out
        self.left_df = left_df
        self.right_df = right_df
        self.left_keys = left_keys
        self.right_keys = right_keys
        self.out_data_vars = out_data_vars
        self.left_vars = left_vars
        self.right_vars = right_vars
        self.how = how
        self.suffix_x = suffix_x
        self.suffix_y = suffix_y
        self.loc = loc
        self.is_left = is_left
        self.is_right = is_right
        self.is_join = is_join
        self.left_index = left_index
        self.right_index = right_index
        self.indicator = indicator
        self.is_na_equal = is_na_equal
        self.gen_cond_expr = gen_cond_expr
        self.left_cond_cols = set(zyiqo__davn for zyiqo__davn in left_vars.
            keys() if f'(left.{zyiqo__davn})' in gen_cond_expr)
        self.right_cond_cols = set(zyiqo__davn for zyiqo__davn in
            right_vars.keys() if f'(right.{zyiqo__davn})' in gen_cond_expr)
        dctj__mbtuf = set(left_keys) & set(right_keys)
        avezb__bnu = set(left_vars.keys()) & set(right_vars.keys())
        myxv__bbyge = avezb__bnu - dctj__mbtuf
        vect_same_key = []
        n_keys = len(left_keys)
        for swyse__ynq in range(n_keys):
            ichy__niqu = left_keys[swyse__ynq]
            iae__heait = right_keys[swyse__ynq]
            vect_same_key.append(ichy__niqu == iae__heait)
        self.vect_same_key = vect_same_key
        self.column_origins = {(str(zyiqo__davn) + suffix_x if zyiqo__davn in
            myxv__bbyge else zyiqo__davn): ('left', zyiqo__davn) for
            zyiqo__davn in left_vars.keys()}
        self.column_origins.update({(str(zyiqo__davn) + suffix_y if 
            zyiqo__davn in myxv__bbyge else zyiqo__davn): ('right',
            zyiqo__davn) for zyiqo__davn in right_vars.keys()})
        if '$_bodo_index_' in myxv__bbyge:
            myxv__bbyge.remove('$_bodo_index_')
        self.add_suffix = myxv__bbyge

    def __repr__(self):
        unskl__cnu = ''
        for zyiqo__davn, tojef__wlxcp in self.out_data_vars.items():
            unskl__cnu += "'{}':{}, ".format(zyiqo__davn, tojef__wlxcp.name)
        jmhiq__lkzt = '{}{{{}}}'.format(self.df_out, unskl__cnu)
        nvmb__leiki = ''
        for zyiqo__davn, tojef__wlxcp in self.left_vars.items():
            nvmb__leiki += "'{}':{}, ".format(zyiqo__davn, tojef__wlxcp.name)
        lqo__sipn = '{}{{{}}}'.format(self.left_df, nvmb__leiki)
        nvmb__leiki = ''
        for zyiqo__davn, tojef__wlxcp in self.right_vars.items():
            nvmb__leiki += "'{}':{}, ".format(zyiqo__davn, tojef__wlxcp.name)
        yfnkv__qtiz = '{}{{{}}}'.format(self.right_df, nvmb__leiki)
        return 'join [{}={}]: {} , {}, {}'.format(self.left_keys, self.
            right_keys, jmhiq__lkzt, lqo__sipn, yfnkv__qtiz)


def join_array_analysis(join_node, equiv_set, typemap, array_analysis):
    pfu__toc = []
    assert len(join_node.out_data_vars) > 0, 'empty join in array analysis'
    mknxv__aka = []
    wdpcz__lfy = list(join_node.left_vars.values())
    for abugp__kay in wdpcz__lfy:
        zmve__jge = typemap[abugp__kay.name]
        nknjb__uas = equiv_set.get_shape(abugp__kay)
        if nknjb__uas:
            mknxv__aka.append(nknjb__uas[0])
    if len(mknxv__aka) > 1:
        equiv_set.insert_equiv(*mknxv__aka)
    mknxv__aka = []
    wdpcz__lfy = list(join_node.right_vars.values())
    for abugp__kay in wdpcz__lfy:
        zmve__jge = typemap[abugp__kay.name]
        nknjb__uas = equiv_set.get_shape(abugp__kay)
        if nknjb__uas:
            mknxv__aka.append(nknjb__uas[0])
    if len(mknxv__aka) > 1:
        equiv_set.insert_equiv(*mknxv__aka)
    mknxv__aka = []
    for abugp__kay in join_node.out_data_vars.values():
        zmve__jge = typemap[abugp__kay.name]
        beyj__gny = array_analysis._gen_shape_call(equiv_set, abugp__kay,
            zmve__jge.ndim, None, pfu__toc)
        equiv_set.insert_equiv(abugp__kay, beyj__gny)
        mknxv__aka.append(beyj__gny[0])
        equiv_set.define(abugp__kay, set())
    if len(mknxv__aka) > 1:
        equiv_set.insert_equiv(*mknxv__aka)
    return [], pfu__toc


numba.parfors.array_analysis.array_analysis_extensions[Join
    ] = join_array_analysis


def join_distributed_analysis(join_node, array_dists):
    berd__agizr = Distribution.OneD
    riow__ukza = Distribution.OneD
    for abugp__kay in join_node.left_vars.values():
        berd__agizr = Distribution(min(berd__agizr.value, array_dists[
            abugp__kay.name].value))
    for abugp__kay in join_node.right_vars.values():
        riow__ukza = Distribution(min(riow__ukza.value, array_dists[
            abugp__kay.name].value))
    pxrrz__aje = Distribution.OneD_Var
    for abugp__kay in join_node.out_data_vars.values():
        if abugp__kay.name in array_dists:
            pxrrz__aje = Distribution(min(pxrrz__aje.value, array_dists[
                abugp__kay.name].value))
    boota__jdx = Distribution(min(pxrrz__aje.value, berd__agizr.value))
    sgx__jnnix = Distribution(min(pxrrz__aje.value, riow__ukza.value))
    pxrrz__aje = Distribution(max(boota__jdx.value, sgx__jnnix.value))
    for abugp__kay in join_node.out_data_vars.values():
        array_dists[abugp__kay.name] = pxrrz__aje
    if pxrrz__aje != Distribution.OneD_Var:
        berd__agizr = pxrrz__aje
        riow__ukza = pxrrz__aje
    for abugp__kay in join_node.left_vars.values():
        array_dists[abugp__kay.name] = berd__agizr
    for abugp__kay in join_node.right_vars.values():
        array_dists[abugp__kay.name] = riow__ukza
    return


distributed_analysis.distributed_analysis_extensions[Join
    ] = join_distributed_analysis


def join_typeinfer(join_node, typeinferer):
    dctj__mbtuf = set(join_node.left_keys) & set(join_node.right_keys)
    avezb__bnu = set(join_node.left_vars.keys()) & set(join_node.right_vars
        .keys())
    myxv__bbyge = avezb__bnu - dctj__mbtuf
    for edudy__zdekf, vxm__ewug in join_node.out_data_vars.items():
        if join_node.indicator and edudy__zdekf == '_merge':
            continue
        if not edudy__zdekf in join_node.column_origins:
            raise BodoError('join(): The variable ' + edudy__zdekf +
                ' is absent from the output')
        beqt__oljf = join_node.column_origins[edudy__zdekf]
        if beqt__oljf[0] == 'left':
            abugp__kay = join_node.left_vars[beqt__oljf[1]]
        else:
            abugp__kay = join_node.right_vars[beqt__oljf[1]]
        typeinferer.constraints.append(typeinfer.Propagate(dst=vxm__ewug.
            name, src=abugp__kay.name, loc=join_node.loc))
    return


typeinfer.typeinfer_extensions[Join] = join_typeinfer


def visit_vars_join(join_node, callback, cbdata):
    if debug_prints():
        print('visiting join vars for:', join_node)
        print('cbdata: ', sorted(cbdata.items()))
    for bxf__ndq in list(join_node.left_vars.keys()):
        join_node.left_vars[bxf__ndq] = visit_vars_inner(join_node.
            left_vars[bxf__ndq], callback, cbdata)
    for bxf__ndq in list(join_node.right_vars.keys()):
        join_node.right_vars[bxf__ndq] = visit_vars_inner(join_node.
            right_vars[bxf__ndq], callback, cbdata)
    for bxf__ndq in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[bxf__ndq] = visit_vars_inner(join_node.
            out_data_vars[bxf__ndq], callback, cbdata)


ir_utils.visit_vars_extensions[Join] = visit_vars_join


def remove_dead_join(join_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    kie__hfsc = []
    mlcee__pmq = True
    for bxf__ndq, abugp__kay in join_node.out_data_vars.items():
        if abugp__kay.name in lives:
            mlcee__pmq = False
            continue
        if bxf__ndq == '$_bodo_index_':
            continue
        if join_node.indicator and bxf__ndq == '_merge':
            kie__hfsc.append('_merge')
            join_node.indicator = False
            continue
        exa__zykkn, pef__pcu = join_node.column_origins[bxf__ndq]
        if (exa__zykkn == 'left' and pef__pcu not in join_node.left_keys and
            pef__pcu not in join_node.left_cond_cols):
            join_node.left_vars.pop(pef__pcu)
            kie__hfsc.append(bxf__ndq)
        if (exa__zykkn == 'right' and pef__pcu not in join_node.right_keys and
            pef__pcu not in join_node.right_cond_cols):
            join_node.right_vars.pop(pef__pcu)
            kie__hfsc.append(bxf__ndq)
    for cname in kie__hfsc:
        join_node.out_data_vars.pop(cname)
    if mlcee__pmq:
        return None
    return join_node


ir_utils.remove_dead_extensions[Join] = remove_dead_join


def join_usedefs(join_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({tojef__wlxcp.name for tojef__wlxcp in join_node.
        left_vars.values()})
    use_set.update({tojef__wlxcp.name for tojef__wlxcp in join_node.
        right_vars.values()})
    def_set.update({tojef__wlxcp.name for tojef__wlxcp in join_node.
        out_data_vars.values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Join] = join_usedefs


def get_copies_join(join_node, typemap):
    gho__nsybj = set(tojef__wlxcp.name for tojef__wlxcp in join_node.
        out_data_vars.values())
    return set(), gho__nsybj


ir_utils.copy_propagate_extensions[Join] = get_copies_join


def apply_copies_join(join_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for bxf__ndq in list(join_node.left_vars.keys()):
        join_node.left_vars[bxf__ndq] = replace_vars_inner(join_node.
            left_vars[bxf__ndq], var_dict)
    for bxf__ndq in list(join_node.right_vars.keys()):
        join_node.right_vars[bxf__ndq] = replace_vars_inner(join_node.
            right_vars[bxf__ndq], var_dict)
    for bxf__ndq in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[bxf__ndq] = replace_vars_inner(join_node.
            out_data_vars[bxf__ndq], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Join] = apply_copies_join


def build_join_definitions(join_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for abugp__kay in join_node.out_data_vars.values():
        definitions[abugp__kay.name].append(join_node)
    return definitions


ir_utils.build_defs_extensions[Join] = build_join_definitions


def join_distributed_run(join_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    left_parallel, right_parallel = False, False
    if array_dists is not None:
        left_parallel, right_parallel = _get_table_parallel_flags(join_node,
            array_dists)
    n_keys = len(join_node.left_keys)
    gdm__znr = tuple(join_node.left_vars[zyiqo__davn] for zyiqo__davn in
        join_node.left_keys)
    rdwsc__noetr = tuple(join_node.right_vars[zyiqo__davn] for zyiqo__davn in
        join_node.right_keys)
    dof__jaq = tuple(join_node.left_vars.keys())
    pio__wmeq = tuple(join_node.right_vars.keys())
    rpp__gqrl = ()
    prm__cwecw = ()
    optional_column = False
    if (join_node.left_index and not join_node.right_index and not
        join_node.is_join):
        ywh__yag = join_node.right_keys[0]
        if ywh__yag in dof__jaq:
            prm__cwecw = ywh__yag,
            rpp__gqrl = join_node.right_vars[ywh__yag],
            optional_column = True
    if (join_node.right_index and not join_node.left_index and not
        join_node.is_join):
        ywh__yag = join_node.left_keys[0]
        if ywh__yag in pio__wmeq:
            prm__cwecw = ywh__yag,
            rpp__gqrl = join_node.left_vars[ywh__yag],
            optional_column = True
    lnn__qjyx = tuple(join_node.out_data_vars[cname] for cname in prm__cwecw)
    erzp__igz = tuple(tojef__wlxcp for puqs__zxib, tojef__wlxcp in sorted(
        join_node.left_vars.items(), key=lambda a: str(a[0])) if puqs__zxib
         not in join_node.left_keys)
    aptk__orh = tuple(tojef__wlxcp for puqs__zxib, tojef__wlxcp in sorted(
        join_node.right_vars.items(), key=lambda a: str(a[0])) if 
        puqs__zxib not in join_node.right_keys)
    mxwh__ycdpv = rpp__gqrl + gdm__znr + rdwsc__noetr + erzp__igz + aptk__orh
    oyh__tzrjj = tuple(typemap[tojef__wlxcp.name] for tojef__wlxcp in
        mxwh__ycdpv)
    ubkr__lrin = tuple('opti_c' + str(i) for i in range(len(rpp__gqrl)))
    left_other_names = tuple('t1_c' + str(i) for i in range(len(erzp__igz)))
    right_other_names = tuple('t2_c' + str(i) for i in range(len(aptk__orh)))
    left_other_types = tuple([typemap[zyiqo__davn.name] for zyiqo__davn in
        erzp__igz])
    right_other_types = tuple([typemap[zyiqo__davn.name] for zyiqo__davn in
        aptk__orh])
    left_key_names = tuple('t1_key' + str(i) for i in range(n_keys))
    right_key_names = tuple('t2_key' + str(i) for i in range(n_keys))
    glbs = {}
    loc = join_node.loc
    func_text = 'def f({}{}, {},{}{}{}):\n'.format('{},'.format(ubkr__lrin[
        0]) if len(ubkr__lrin) == 1 else '', ','.join(left_key_names), ','.
        join(right_key_names), ','.join(left_other_names), ',' if len(
        left_other_names) != 0 else '', ','.join(right_other_names))
    left_key_types = tuple(typemap[tojef__wlxcp.name] for tojef__wlxcp in
        gdm__znr)
    right_key_types = tuple(typemap[tojef__wlxcp.name] for tojef__wlxcp in
        rdwsc__noetr)
    for i in range(n_keys):
        glbs[f'key_type_{i}'] = _match_join_key_types(left_key_types[i],
            right_key_types[i], loc)
    func_text += '    t1_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({left_key_names[i]}, key_type_{i})' for i in
        range(n_keys)))
    func_text += '    t2_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({right_key_names[i]}, key_type_{i})' for
        i in range(n_keys)))
    func_text += '    data_left = ({}{})\n'.format(','.join(
        left_other_names), ',' if len(left_other_names) != 0 else '')
    func_text += '    data_right = ({}{})\n'.format(','.join(
        right_other_names), ',' if len(right_other_names) != 0 else '')
    oosmu__ffhw = []
    for cname in join_node.left_keys:
        if cname in join_node.add_suffix:
            lmmg__luysd = str(cname) + join_node.suffix_x
        else:
            lmmg__luysd = cname
        assert lmmg__luysd in join_node.out_data_vars
        oosmu__ffhw.append(join_node.out_data_vars[lmmg__luysd])
    for i, cname in enumerate(join_node.right_keys):
        if not join_node.vect_same_key[i] and not join_node.is_join:
            if cname in join_node.add_suffix:
                lmmg__luysd = str(cname) + join_node.suffix_y
            else:
                lmmg__luysd = cname
            assert lmmg__luysd in join_node.out_data_vars
            oosmu__ffhw.append(join_node.out_data_vars[lmmg__luysd])

    def _get_out_col_var(cname, is_left):
        if cname in join_node.add_suffix:
            if is_left:
                lmmg__luysd = str(cname) + join_node.suffix_x
            else:
                lmmg__luysd = str(cname) + join_node.suffix_y
        else:
            lmmg__luysd = cname
        return join_node.out_data_vars[lmmg__luysd]
    hhrgw__hmy = lnn__qjyx + tuple(oosmu__ffhw)
    hhrgw__hmy += tuple(_get_out_col_var(puqs__zxib, True) for puqs__zxib,
        tojef__wlxcp in sorted(join_node.left_vars.items(), key=lambda a:
        str(a[0])) if puqs__zxib not in join_node.left_keys)
    hhrgw__hmy += tuple(_get_out_col_var(puqs__zxib, False) for puqs__zxib,
        tojef__wlxcp in sorted(join_node.right_vars.items(), key=lambda a:
        str(a[0])) if puqs__zxib not in join_node.right_keys)
    if join_node.indicator:
        hhrgw__hmy += _get_out_col_var('_merge', False),
    nvzy__moid = [('t3_c' + str(i)) for i in range(len(hhrgw__hmy))]
    general_cond_cfunc, left_col_nums, right_col_nums = (
        _gen_general_cond_cfunc(join_node, typemap))
    if join_node.how == 'asof':
        if left_parallel or right_parallel:
            assert left_parallel and right_parallel
            func_text += """    t2_keys, data_right = parallel_asof_comm(t1_keys, t2_keys, data_right)
"""
        func_text += """    out_t1_keys, out_t2_keys, out_data_left, out_data_right = bodo.ir.join.local_merge_asof(t1_keys, t2_keys, data_left, data_right)
"""
    else:
        func_text += _gen_local_hash_join(optional_column, left_key_names,
            right_key_names, left_key_types, right_key_types,
            left_other_names, right_other_names, left_other_types,
            right_other_types, join_node.vect_same_key, join_node.is_left,
            join_node.is_right, join_node.is_join, left_parallel,
            right_parallel, glbs, [typemap[tojef__wlxcp.name] for
            tojef__wlxcp in hhrgw__hmy], join_node.loc, join_node.indicator,
            join_node.is_na_equal, general_cond_cfunc, left_col_nums,
            right_col_nums)
    if join_node.how == 'asof':
        for i in range(len(left_other_names)):
            func_text += '    left_{} = out_data_left[{}]\n'.format(i, i)
        for i in range(len(right_other_names)):
            func_text += '    right_{} = out_data_right[{}]\n'.format(i, i)
        for i in range(n_keys):
            func_text += f'    t1_keys_{i} = out_t1_keys[{i}]\n'
        for i in range(n_keys):
            func_text += f'    t2_keys_{i} = out_t2_keys[{i}]\n'
    idx = 0
    if optional_column:
        func_text += f'    {nvzy__moid[idx]} = opti_0\n'
        idx += 1
    for i in range(n_keys):
        func_text += f'    {nvzy__moid[idx]} = t1_keys_{i}\n'
        idx += 1
    for i in range(n_keys):
        if not join_node.vect_same_key[i] and not join_node.is_join:
            func_text += f'    {nvzy__moid[idx]} = t2_keys_{i}\n'
            idx += 1
    for i in range(len(left_other_names)):
        func_text += f'    {nvzy__moid[idx]} = left_{i}\n'
        idx += 1
    for i in range(len(right_other_names)):
        func_text += f'    {nvzy__moid[idx]} = right_{i}\n'
        idx += 1
    if join_node.indicator:
        func_text += f'    {nvzy__moid[idx]} = indicator_col\n'
        idx += 1
    knll__jmbji = {}
    exec(func_text, {}, knll__jmbji)
    dmv__sdf = knll__jmbji['f']
    glbs.update({'bodo': bodo, 'np': np, 'pd': pd,
        'to_list_if_immutable_arr': to_list_if_immutable_arr,
        'cp_str_list_to_array': cp_str_list_to_array, 'parallel_asof_comm':
        parallel_asof_comm, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'hash_join_table':
        hash_join_table, 'info_from_table': info_from_table,
        'info_to_array': info_to_array, 'delete_table': delete_table,
        'delete_table_decref_arrays': delete_table_decref_arrays,
        'add_join_gen_cond_cfunc_sym': add_join_gen_cond_cfunc_sym,
        'get_join_cond_addr': get_join_cond_addr})
    if general_cond_cfunc:
        glbs.update({'general_cond_cfunc': general_cond_cfunc})
    zln__qlb = compile_to_numba_ir(dmv__sdf, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=oyh__tzrjj, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(zln__qlb, mxwh__ycdpv)
    kkw__ttk = zln__qlb.body[:-3]
    for i in range(len(hhrgw__hmy)):
        kkw__ttk[-len(hhrgw__hmy) + i].target = hhrgw__hmy[i]
    return kkw__ttk


distributed_pass.distributed_run_extensions[Join] = join_distributed_run


def _gen_general_cond_cfunc(join_node, typemap):
    expr = join_node.gen_cond_expr
    if not expr:
        return None, [], []
    qtos__njphr = next_label()
    vrd__fyzf = _get_col_to_ind(join_node.left_keys, join_node.left_vars)
    zfq__mtw = _get_col_to_ind(join_node.right_keys, join_node.right_vars)
    table_getitem_funcs = {'bodo': bodo, 'numba': numba, 'is_null_pointer':
        is_null_pointer}
    na_check_name = 'NOT_NA'
    func_text = f"""def bodo_join_gen_cond{qtos__njphr}(left_table, right_table, left_data1, right_data1, left_null_bitmap, right_null_bitmap, left_ind, right_ind):
"""
    func_text += '  if is_null_pointer(left_table):\n'
    func_text += '    return False\n'
    expr, func_text, left_col_nums = _replace_column_accesses(expr,
        vrd__fyzf, typemap, join_node.left_vars, table_getitem_funcs,
        func_text, 'left', len(join_node.left_keys), na_check_name)
    expr, func_text, right_col_nums = _replace_column_accesses(expr,
        zfq__mtw, typemap, join_node.right_vars, table_getitem_funcs,
        func_text, 'right', len(join_node.right_keys), na_check_name)
    func_text += f'  return {expr}'
    knll__jmbji = {}
    exec(func_text, table_getitem_funcs, knll__jmbji)
    svzqe__ujdb = knll__jmbji[f'bodo_join_gen_cond{qtos__njphr}']
    csjz__tqffg = types.bool_(types.voidptr, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.int64, types.int64)
    fzk__lde = numba.cfunc(csjz__tqffg, nopython=True)(svzqe__ujdb)
    join_gen_cond_cfunc[fzk__lde.native_name] = fzk__lde
    join_gen_cond_cfunc_addr[fzk__lde.native_name] = fzk__lde.address
    return fzk__lde, left_col_nums, right_col_nums


def _replace_column_accesses(expr, col_to_ind, typemap, col_vars,
    table_getitem_funcs, func_text, table_name, n_keys, na_check_name):
    jgq__dnes = []
    for zyiqo__davn, kfvkp__cuxc in col_to_ind.items():
        cname = f'({table_name}.{zyiqo__davn})'
        if cname not in expr:
            continue
        kqa__kud = f'getitem_{table_name}_val_{kfvkp__cuxc}'
        jrn__plo = f'_bodo_{table_name}_val_{kfvkp__cuxc}'
        qsgn__tpgk = typemap[col_vars[zyiqo__davn].name].dtype
        if qsgn__tpgk == types.unicode_type:
            func_text += f"""  {jrn__plo}, {jrn__plo}_size = {kqa__kud}({table_name}_table, {table_name}_ind)
"""
            func_text += f"""  {jrn__plo} = bodo.libs.str_arr_ext.decode_utf8({jrn__plo}, {jrn__plo}_size)
"""
        else:
            func_text += (
                f'  {jrn__plo} = {kqa__kud}({table_name}_data1, {table_name}_ind)\n'
                )
        table_getitem_funcs[kqa__kud
            ] = bodo.libs.array._gen_row_access_intrinsic(qsgn__tpgk,
            kfvkp__cuxc)
        expr = expr.replace(cname, jrn__plo)
        naddg__xwqwt = f'({na_check_name}.{table_name}.{zyiqo__davn})'
        if naddg__xwqwt in expr:
            rqr__iwg = typemap[col_vars[zyiqo__davn].name]
            ntcxb__qza = f'nacheck_{table_name}_val_{kfvkp__cuxc}'
            tvrpe__bise = f'_bodo_isna_{table_name}_val_{kfvkp__cuxc}'
            if isinstance(rqr__iwg, bodo.libs.int_arr_ext.IntegerArrayType
                ) or rqr__iwg in [bodo.libs.bool_arr_ext.boolean_array,
                bodo.libs.str_arr_ext.string_array_type]:
                func_text += f"""  {tvrpe__bise} = {ntcxb__qza}({table_name}_null_bitmap, {table_name}_ind)
"""
            else:
                func_text += f"""  {tvrpe__bise} = {ntcxb__qza}({table_name}_data1, {table_name}_ind)
"""
            table_getitem_funcs[ntcxb__qza
                ] = bodo.libs.array._gen_row_na_check_intrinsic(rqr__iwg,
                kfvkp__cuxc)
            expr = expr.replace(naddg__xwqwt, tvrpe__bise)
        if kfvkp__cuxc >= n_keys:
            jgq__dnes.append(kfvkp__cuxc)
    return expr, func_text, jgq__dnes


def _get_col_to_ind(key_names, col_vars):
    n_keys = len(key_names)
    col_to_ind = {zyiqo__davn: i for i, zyiqo__davn in enumerate(key_names)}
    i = n_keys
    for zyiqo__davn in sorted(col_vars, key=lambda a: str(a)):
        if zyiqo__davn in key_names:
            continue
        col_to_ind[zyiqo__davn] = i
        i += 1
    return col_to_ind


def _match_join_key_types(t1, t2, loc):
    if t1 == t2:
        return t1
    try:
        arr = dtype_to_array_type(find_common_np_dtype([t1, t2]))
        return to_nullable_type(arr) if is_nullable_type(t1
            ) or is_nullable_type(t2) else arr
    except:
        raise BodoError(f'Join key types {t1} and {t2} do not match', loc=loc)


def _get_table_parallel_flags(join_node, array_dists):
    vrhe__awryc = (distributed_pass.Distribution.OneD, distributed_pass.
        Distribution.OneD_Var)
    left_parallel = all(array_dists[tojef__wlxcp.name] in vrhe__awryc for
        tojef__wlxcp in join_node.left_vars.values())
    right_parallel = all(array_dists[tojef__wlxcp.name] in vrhe__awryc for
        tojef__wlxcp in join_node.right_vars.values())
    if not left_parallel:
        assert not any(array_dists[tojef__wlxcp.name] in vrhe__awryc for
            tojef__wlxcp in join_node.left_vars.values())
    if not right_parallel:
        assert not any(array_dists[tojef__wlxcp.name] in vrhe__awryc for
            tojef__wlxcp in join_node.right_vars.values())
    if left_parallel or right_parallel:
        assert all(array_dists[tojef__wlxcp.name] in vrhe__awryc for
            tojef__wlxcp in join_node.out_data_vars.values())
    return left_parallel, right_parallel


def _gen_local_hash_join(optional_column, left_key_names, right_key_names,
    left_key_types, right_key_types, left_other_names, right_other_names,
    left_other_types, right_other_types, vect_same_key, is_left, is_right,
    is_join, left_parallel, right_parallel, glbs, out_types, loc, indicator,
    is_na_equal, general_cond_cfunc, left_col_nums, right_col_nums):

    def needs_typechange(in_type, need_nullable, is_same_key):
        return isinstance(in_type, types.Array) and not is_dtype_nullable(
            in_type.dtype) and need_nullable and not is_same_key
    ewr__uvgzq = []
    for i in range(len(left_key_names)):
        kpwh__ekcl = _match_join_key_types(left_key_types[i],
            right_key_types[i], loc)
        ewr__uvgzq.append(needs_typechange(kpwh__ekcl, is_right,
            vect_same_key[i]))
    for i in range(len(left_other_names)):
        ewr__uvgzq.append(needs_typechange(left_other_types[i], is_right, 
            False))
    for i in range(len(right_key_names)):
        if not vect_same_key[i] and not is_join:
            kpwh__ekcl = _match_join_key_types(left_key_types[i],
                right_key_types[i], loc)
            ewr__uvgzq.append(needs_typechange(kpwh__ekcl, is_left, False))
    for i in range(len(right_other_names)):
        ewr__uvgzq.append(needs_typechange(right_other_types[i], is_left, 
            False))

    def get_out_type(idx, in_type, in_name, need_nullable, is_same_key):
        if isinstance(in_type, types.Array) and not is_dtype_nullable(in_type
            .dtype) and need_nullable and not is_same_key:
            if isinstance(in_type.dtype, types.Integer):
                sznkm__epc = IntDtype(in_type.dtype).name
                assert sznkm__epc.endswith('Dtype()')
                sznkm__epc = sznkm__epc[:-7]
                uqyz__uige = f"""    typ_{idx} = bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype="{sznkm__epc}"))
"""
                nrscb__klmv = f'typ_{idx}'
            else:
                assert in_type.dtype == types.bool_, 'unexpected non-nullable type in join'
                uqyz__uige = (
                    f'    typ_{idx} = bodo.libs.bool_arr_ext.alloc_bool_array(1)\n'
                    )
                nrscb__klmv = f'typ_{idx}'
        else:
            uqyz__uige = ''
            nrscb__klmv = in_name
        return uqyz__uige, nrscb__klmv
    n_keys = len(left_key_names)
    func_text = '    # beginning of _gen_local_hash_join\n'
    hro__ida = []
    for i in range(n_keys):
        hro__ida.append('t1_keys[{}]'.format(i))
    for i in range(len(left_other_names)):
        hro__ida.append('data_left[{}]'.format(i))
    func_text += '    info_list_total_l = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in hro__ida))
    func_text += '    table_left = arr_info_list_to_table(info_list_total_l)\n'
    mdh__gonp = []
    for i in range(n_keys):
        mdh__gonp.append('t2_keys[{}]'.format(i))
    for i in range(len(right_other_names)):
        mdh__gonp.append('data_right[{}]'.format(i))
    func_text += '    info_list_total_r = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in mdh__gonp))
    func_text += (
        '    table_right = arr_info_list_to_table(info_list_total_r)\n')
    func_text += '    vect_same_key = np.array([{}])\n'.format(','.join('1' if
        agprr__ejvs else '0' for agprr__ejvs in vect_same_key))
    func_text += '    vect_need_typechange = np.array([{}])\n'.format(','.
        join('1' if agprr__ejvs else '0' for agprr__ejvs in ewr__uvgzq))
    func_text += f"""    left_table_cond_columns = np.array({left_col_nums if len(left_col_nums) > 0 else [-1]}, dtype=np.int64)
"""
    func_text += f"""    right_table_cond_columns = np.array({right_col_nums if len(right_col_nums) > 0 else [-1]}, dtype=np.int64)
"""
    if general_cond_cfunc:
        func_text += f"""    cfunc_cond = add_join_gen_cond_cfunc_sym(general_cond_cfunc, '{general_cond_cfunc.native_name}')
"""
        func_text += (
            f"    cfunc_cond = get_join_cond_addr('{general_cond_cfunc.native_name}')\n"
            )
    else:
        func_text += '    cfunc_cond = 0\n'
    func_text += (
        """    out_table = hash_join_table(table_left, table_right, {}, {}, {}, {}, {}, vect_same_key.ctypes, vect_need_typechange.ctypes, {}, {}, {}, {}, {}, {}, cfunc_cond, left_table_cond_columns.ctypes, {}, right_table_cond_columns.ctypes, {})
"""
        .format(left_parallel, right_parallel, n_keys, len(left_other_names
        ), len(right_other_names), is_left, is_right, is_join,
        optional_column, indicator, is_na_equal, len(left_col_nums), len(
        right_col_nums)))
    func_text += '    delete_table(table_left)\n'
    func_text += '    delete_table(table_right)\n'
    idx = 0
    if optional_column:
        func_text += (
            f'    opti_0 = info_to_array(info_from_table(out_table, {idx}), opti_c0)\n'
            )
        idx += 1
    for i, jnq__sfvy in enumerate(left_key_names):
        kpwh__ekcl = _match_join_key_types(left_key_types[i],
            right_key_types[i], loc)
        swb__lmiun = get_out_type(idx, kpwh__ekcl, f't1_keys[{i}]',
            is_right, vect_same_key[i])
        func_text += swb__lmiun[0]
        glbs[f'out_type_{idx}'] = out_types[idx]
        if kpwh__ekcl != left_key_types[i]:
            func_text += f"""    t1_keys_{i} = bodo.utils.utils.astype(info_to_array(info_from_table(out_table, {idx}), {swb__lmiun[1]}), out_type_{idx})
"""
        else:
            func_text += f"""    t1_keys_{i} = info_to_array(info_from_table(out_table, {idx}), {swb__lmiun[1]})
"""
        idx += 1
    for i, jnq__sfvy in enumerate(left_other_names):
        swb__lmiun = get_out_type(idx, left_other_types[i], jnq__sfvy,
            is_right, False)
        func_text += swb__lmiun[0]
        func_text += (
            '    left_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(i, idx, swb__lmiun[1]))
        idx += 1
    for i, jnq__sfvy in enumerate(right_key_names):
        if not vect_same_key[i] and not is_join:
            kpwh__ekcl = _match_join_key_types(left_key_types[i],
                right_key_types[i], loc)
            swb__lmiun = get_out_type(idx, kpwh__ekcl, f't2_keys[{i}]',
                is_left, False)
            func_text += swb__lmiun[0]
            glbs[f'out_type_{idx}'] = out_types[idx - len(left_other_names)]
            if kpwh__ekcl != right_key_types[i]:
                func_text += f"""    t2_keys_{i} = bodo.utils.utils.astype(info_to_array(info_from_table(out_table, {idx}), {swb__lmiun[1]}), out_type_{idx})
"""
            else:
                func_text += f"""    t2_keys_{i} = info_to_array(info_from_table(out_table, {idx}), {swb__lmiun[1]})
"""
            idx += 1
    for i, jnq__sfvy in enumerate(right_other_names):
        swb__lmiun = get_out_type(idx, right_other_types[i], jnq__sfvy,
            is_left, False)
        func_text += swb__lmiun[0]
        func_text += (
            '    right_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(i, idx, swb__lmiun[1]))
        idx += 1
    if indicator:
        func_text += f"""    typ_{idx} = pd.Categorical(values=['both'], categories=('left_only', 'right_only', 'both'))
"""
        func_text += f"""    indicator_col = info_to_array(info_from_table(out_table, {idx}), typ_{idx})
"""
        idx += 1
    func_text += '    delete_table(out_table)\n'
    return func_text


def parallel_join_impl(key_arrs, data):
    fit__dkx = bodo.libs.distributed_api.get_size()
    zde__hkn = alloc_pre_shuffle_metadata(key_arrs, data, fit__dkx, False)
    puqs__zxib = len(key_arrs[0])
    xyofo__itm = np.empty(puqs__zxib, np.int32)
    krrd__uxh = arr_info_list_to_table([array_to_info(key_arrs[0])])
    ytf__nmicy = 1
    vftk__lkxp = compute_node_partition_by_hash(krrd__uxh, ytf__nmicy, fit__dkx
        )
    huglq__vuin = np.empty(1, np.int32)
    jqj__zamyd = info_to_array(info_from_table(vftk__lkxp, 0), huglq__vuin)
    delete_table(vftk__lkxp)
    delete_table(krrd__uxh)
    for i in range(puqs__zxib):
        val = getitem_arr_tup_single(key_arrs, i)
        node_id = jqj__zamyd[i]
        xyofo__itm[i] = node_id
        update_shuffle_meta(zde__hkn, node_id, i, key_arrs, data, False)
    shuffle_meta = finalize_shuffle_meta(key_arrs, data, zde__hkn, fit__dkx,
        False)
    for i in range(puqs__zxib):
        node_id = xyofo__itm[i]
        write_send_buff(shuffle_meta, node_id, i, key_arrs, data)
        shuffle_meta.tmp_offset[node_id] += 1
    msgqc__fprt = alltoallv_tup(key_arrs + data, shuffle_meta, key_arrs)
    oosmu__ffhw = _get_keys_tup(msgqc__fprt, key_arrs)
    lzhlg__oac = _get_data_tup(msgqc__fprt, key_arrs)
    return oosmu__ffhw, lzhlg__oac


@generated_jit(nopython=True, cache=True)
def parallel_shuffle(key_arrs, data):
    return parallel_join_impl


@numba.njit
def parallel_asof_comm(left_key_arrs, right_key_arrs, right_data):
    fit__dkx = bodo.libs.distributed_api.get_size()
    qsj__escy = np.empty(fit__dkx, left_key_arrs[0].dtype)
    rxqf__tsxsz = np.empty(fit__dkx, left_key_arrs[0].dtype)
    bodo.libs.distributed_api.allgather(qsj__escy, left_key_arrs[0][0])
    bodo.libs.distributed_api.allgather(rxqf__tsxsz, left_key_arrs[0][-1])
    wji__jjo = np.zeros(fit__dkx, np.int32)
    uxo__kvu = np.zeros(fit__dkx, np.int32)
    acdd__kdn = np.zeros(fit__dkx, np.int32)
    cda__ogk = right_key_arrs[0][0]
    knis__gbizw = right_key_arrs[0][-1]
    ujexr__hwwr = -1
    i = 0
    while i < fit__dkx - 1 and rxqf__tsxsz[i] < cda__ogk:
        i += 1
    while i < fit__dkx and qsj__escy[i] <= knis__gbizw:
        ujexr__hwwr, eyss__rvk = _count_overlap(right_key_arrs[0],
            qsj__escy[i], rxqf__tsxsz[i])
        if ujexr__hwwr != 0:
            ujexr__hwwr -= 1
            eyss__rvk += 1
        wji__jjo[i] = eyss__rvk
        uxo__kvu[i] = ujexr__hwwr
        i += 1
    while i < fit__dkx:
        wji__jjo[i] = 1
        uxo__kvu[i] = len(right_key_arrs[0]) - 1
        i += 1
    bodo.libs.distributed_api.alltoall(wji__jjo, acdd__kdn, 1)
    hefb__ilukb = acdd__kdn.sum()
    fvydl__uryn = np.empty(hefb__ilukb, right_key_arrs[0].dtype)
    szkya__onpu = alloc_arr_tup(hefb__ilukb, right_data)
    yhluj__fuul = bodo.ir.join.calc_disp(acdd__kdn)
    bodo.libs.distributed_api.alltoallv(right_key_arrs[0], fvydl__uryn,
        wji__jjo, acdd__kdn, uxo__kvu, yhluj__fuul)
    bodo.libs.distributed_api.alltoallv_tup(right_data, szkya__onpu,
        wji__jjo, acdd__kdn, uxo__kvu, yhluj__fuul)
    return (fvydl__uryn,), szkya__onpu


@numba.njit
def _count_overlap(r_key_arr, start, end):
    eyss__rvk = 0
    ujexr__hwwr = 0
    tpjyq__qzopo = 0
    while tpjyq__qzopo < len(r_key_arr) and r_key_arr[tpjyq__qzopo] < start:
        ujexr__hwwr += 1
        tpjyq__qzopo += 1
    while tpjyq__qzopo < len(r_key_arr) and start <= r_key_arr[tpjyq__qzopo
        ] <= end:
        tpjyq__qzopo += 1
        eyss__rvk += 1
    return ujexr__hwwr, eyss__rvk


def write_send_buff(shuffle_meta, node_id, i, key_arrs, data):
    return i


@overload(write_send_buff, no_unliteral=True)
def write_data_buff_overload(meta, node_id, i, key_arrs, data):
    func_text = 'def f(meta, node_id, i, key_arrs, data):\n'
    func_text += (
        '  w_ind = meta.send_disp[node_id] + meta.tmp_offset[node_id]\n')
    n_keys = len(key_arrs.types)
    for i, zmve__jge in enumerate(key_arrs.types + data.types):
        arr = 'key_arrs[{}]'.format(i) if i < n_keys else 'data[{}]'.format(
            i - n_keys)
        if not zmve__jge in (string_type, string_array_type,
            binary_array_type, bytes_type):
            func_text += '  meta.send_buff_tup[{}][w_ind] = {}[i]\n'.format(i,
                arr)
        else:
            func_text += ('  n_chars_{} = get_str_arr_item_length({}, i)\n'
                .format(i, arr))
            func_text += ('  meta.send_arr_lens_tup[{}][w_ind] = n_chars_{}\n'
                .format(i, i))
            if i >= n_keys:
                func_text += (
                    """  out_bitmap = meta.send_arr_nulls_tup[{}][meta.send_disp_nulls[node_id]:].ctypes
"""
                    .format(i))
                func_text += (
                    '  bit_val = get_bit_bitmap(get_null_bitmap_ptr(data[{}]), i)\n'
                    .format(i - n_keys))
                func_text += (
                    '  set_bit_to(out_bitmap, meta.tmp_offset[node_id], bit_val)\n'
                    )
            func_text += (
                """  indc_{} = meta.send_disp_char_tup[{}][node_id] + meta.tmp_offset_char_tup[{}][node_id]
"""
                .format(i, i, i))
            func_text += ('  item_ptr_{} = get_str_arr_item_ptr({}, i)\n'.
                format(i, arr))
            func_text += (
                """  str_copy_ptr(meta.send_arr_chars_tup[{}], indc_{}, item_ptr_{}, n_chars_{})
"""
                .format(i, i, i, i))
            func_text += (
                '  meta.tmp_offset_char_tup[{}][node_id] += n_chars_{}\n'.
                format(i, i))
    func_text += '  return w_ind\n'
    knll__jmbji = {}
    exec(func_text, {'str_copy_ptr': str_copy_ptr, 'get_null_bitmap_ptr':
        get_null_bitmap_ptr, 'get_bit_bitmap': get_bit_bitmap, 'set_bit_to':
        set_bit_to, 'get_str_arr_item_length': get_str_arr_item_length,
        'get_str_arr_item_ptr': get_str_arr_item_ptr}, knll__jmbji)
    uohgo__rgo = knll__jmbji['f']
    return uohgo__rgo


import llvmlite.binding as ll
from bodo.libs import hdist
ll.add_symbol('c_alltoallv', hdist.c_alltoallv)


@numba.njit
def calc_disp(arr):
    cui__ytam = np.empty_like(arr)
    cui__ytam[0] = 0
    for i in range(1, len(arr)):
        cui__ytam[i] = cui__ytam[i - 1] + arr[i - 1]
    return cui__ytam


def ensure_capacity(arr, new_size):
    gip__gij = arr
    peik__pgoyo = len(arr)
    if peik__pgoyo < new_size:
        rtt__gwp = 2 * peik__pgoyo
        gip__gij = bodo.utils.utils.alloc_type(rtt__gwp, arr)
        gip__gij[:peik__pgoyo] = arr
    return gip__gij


@overload(ensure_capacity, no_unliteral=True)
def ensure_capacity_overload(arr, new_size):
    if isinstance(arr, types.Array) or arr == boolean_array:
        return ensure_capacity
    assert isinstance(arr, types.BaseTuple)
    eyss__rvk = arr.count
    func_text = 'def f(arr, new_size):\n'
    func_text += '  return ({}{})\n'.format(','.join([
        'ensure_capacity(arr[{}], new_size)'.format(i) for i in range(
        eyss__rvk)]), ',' if eyss__rvk == 1 else '')
    knll__jmbji = {}
    exec(func_text, {'ensure_capacity': ensure_capacity}, knll__jmbji)
    dgpyi__mgct = knll__jmbji['f']
    return dgpyi__mgct


@numba.njit
def ensure_capacity_str(arr, new_size, n_chars):
    gip__gij = arr
    peik__pgoyo = len(arr)
    jmloz__jlr = num_total_chars(arr)
    zofue__xiqo = getitem_str_offset(arr, new_size - 1) + n_chars
    if peik__pgoyo < new_size or zofue__xiqo > jmloz__jlr:
        rtt__gwp = int(2 * peik__pgoyo if peik__pgoyo < new_size else
            peik__pgoyo)
        vbp__zwarv = int(2 * jmloz__jlr + n_chars if zofue__xiqo >
            jmloz__jlr else jmloz__jlr)
        gip__gij = pre_alloc_string_array(rtt__gwp, vbp__zwarv)
        copy_str_arr_slice(gip__gij, arr, new_size - 1)
    return gip__gij


def trim_arr_tup(data, new_size):
    return data


@overload(trim_arr_tup, no_unliteral=True)
def trim_arr_tup_overload(data, new_size):
    assert isinstance(data, types.BaseTuple)
    eyss__rvk = data.count
    func_text = 'def f(data, new_size):\n'
    func_text += '  return ({}{})\n'.format(','.join([
        'trim_arr(data[{}], new_size)'.format(i) for i in range(eyss__rvk)]
        ), ',' if eyss__rvk == 1 else '')
    knll__jmbji = {}
    exec(func_text, {'trim_arr': trim_arr}, knll__jmbji)
    dgpyi__mgct = knll__jmbji['f']
    return dgpyi__mgct


def copy_elem_buff(arr, ind, val):
    gip__gij = ensure_capacity(arr, ind + 1)
    gip__gij[ind] = val
    return gip__gij


@overload(copy_elem_buff, no_unliteral=True)
def copy_elem_buff_overload(arr, ind, val):
    if isinstance(arr, types.Array) or arr == boolean_array:
        return copy_elem_buff
    assert arr == string_array_type

    def copy_elem_buff_str(arr, ind, val):
        gip__gij = ensure_capacity_str(arr, ind + 1, get_utf8_size(val))
        gip__gij[ind] = val
        return gip__gij
    return copy_elem_buff_str


def copy_elem_buff_tup(arr, ind, val):
    return arr


@overload(copy_elem_buff_tup, no_unliteral=True)
def copy_elem_buff_tup_overload(data, ind, val):
    assert isinstance(data, types.BaseTuple)
    eyss__rvk = data.count
    func_text = 'def f(data, ind, val):\n'
    for i in range(eyss__rvk):
        func_text += ('  arr_{} = copy_elem_buff(data[{}], ind, val[{}])\n'
            .format(i, i, i))
    func_text += '  return ({}{})\n'.format(','.join(['arr_{}'.format(i) for
        i in range(eyss__rvk)]), ',' if eyss__rvk == 1 else '')
    knll__jmbji = {}
    exec(func_text, {'copy_elem_buff': copy_elem_buff}, knll__jmbji)
    frb__axg = knll__jmbji['f']
    return frb__axg


def trim_arr(arr, size):
    return arr[:size]


@overload(trim_arr, no_unliteral=True)
def trim_arr_overload(arr, size):
    if isinstance(arr, types.Array) or arr == boolean_array:
        return trim_arr
    assert arr == string_array_type

    def trim_arr_str(arr, size):
        gip__gij = pre_alloc_string_array(size, np.int64(getitem_str_offset
            (arr, size)))
        copy_str_arr_slice(gip__gij, arr, size)
        return gip__gij
    return trim_arr_str


def setnan_elem_buff(arr, ind):
    gip__gij = ensure_capacity(arr, ind + 1)
    bodo.libs.array_kernels.setna(gip__gij, ind)
    return gip__gij


@overload(setnan_elem_buff, no_unliteral=True)
def setnan_elem_buff_overload(arr, ind):
    if isinstance(arr, types.Array) or arr == boolean_array:
        return setnan_elem_buff
    assert arr == string_array_type

    def setnan_elem_buff_str(arr, ind):
        gip__gij = ensure_capacity_str(arr, ind + 1, 0)
        gip__gij[ind] = ''
        bodo.libs.array_kernels.setna(gip__gij, ind)
        return gip__gij
    return setnan_elem_buff_str


def setnan_elem_buff_tup(arr, ind):
    return arr


@overload(setnan_elem_buff_tup, no_unliteral=True)
def setnan_elem_buff_tup_overload(data, ind):
    assert isinstance(data, types.BaseTuple)
    eyss__rvk = data.count
    func_text = 'def f(data, ind):\n'
    for i in range(eyss__rvk):
        func_text += '  arr_{} = setnan_elem_buff(data[{}], ind)\n'.format(i, i
            )
    func_text += '  return ({}{})\n'.format(','.join(['arr_{}'.format(i) for
        i in range(eyss__rvk)]), ',' if eyss__rvk == 1 else '')
    knll__jmbji = {}
    exec(func_text, {'setnan_elem_buff': setnan_elem_buff}, knll__jmbji)
    frb__axg = knll__jmbji['f']
    return frb__axg


@generated_jit(nopython=True, cache=True)
def _check_ind_if_hashed(right_keys, r_ind, l_key):
    if right_keys == types.Tuple((types.intp[::1],)):
        return lambda right_keys, r_ind, l_key: r_ind

    def _impl(right_keys, r_ind, l_key):
        gjef__nmem = getitem_arr_tup(right_keys, r_ind)
        if gjef__nmem != l_key:
            return -1
        return r_ind
    return _impl


@numba.njit
def local_merge_asof(left_keys, right_keys, data_left, data_right):
    mmfzj__edbvp = len(left_keys[0])
    udq__ulh = len(right_keys[0])
    mgw__akb = alloc_arr_tup(mmfzj__edbvp, left_keys)
    vqyno__nyyya = alloc_arr_tup(mmfzj__edbvp, right_keys)
    aqwa__ngejo = alloc_arr_tup(mmfzj__edbvp, data_left)
    foout__zvmf = alloc_arr_tup(mmfzj__edbvp, data_right)
    vyj__oixvs = 0
    mdmhq__imr = 0
    for vyj__oixvs in range(mmfzj__edbvp):
        if mdmhq__imr < 0:
            mdmhq__imr = 0
        while mdmhq__imr < udq__ulh and getitem_arr_tup(right_keys, mdmhq__imr
            ) <= getitem_arr_tup(left_keys, vyj__oixvs):
            mdmhq__imr += 1
        mdmhq__imr -= 1
        setitem_arr_tup(mgw__akb, vyj__oixvs, getitem_arr_tup(left_keys,
            vyj__oixvs))
        setitem_arr_tup(aqwa__ngejo, vyj__oixvs, getitem_arr_tup(data_left,
            vyj__oixvs))
        if mdmhq__imr >= 0:
            setitem_arr_tup(vqyno__nyyya, vyj__oixvs, getitem_arr_tup(
                right_keys, mdmhq__imr))
            setitem_arr_tup(foout__zvmf, vyj__oixvs, getitem_arr_tup(
                data_right, mdmhq__imr))
        else:
            bodo.libs.array_kernels.setna_tup(vqyno__nyyya, vyj__oixvs)
            bodo.libs.array_kernels.setna_tup(foout__zvmf, vyj__oixvs)
    return mgw__akb, vqyno__nyyya, aqwa__ngejo, foout__zvmf


def copy_arr_tup(arrs):
    return tuple(a.copy() for a in arrs)


@overload(copy_arr_tup, no_unliteral=True)
def copy_arr_tup_overload(arrs):
    eyss__rvk = arrs.count
    func_text = 'def f(arrs):\n'
    func_text += '  return ({},)\n'.format(','.join('arrs[{}].copy()'.
        format(i) for i in range(eyss__rvk)))
    knll__jmbji = {}
    exec(func_text, {}, knll__jmbji)
    impl = knll__jmbji['f']
    return impl


def get_nan_bits(arr, ind):
    return 0


@overload(get_nan_bits, no_unliteral=True)
def overload_get_nan_bits(arr, ind):
    if arr == string_array_type:

        def impl_str(arr, ind):
            nzkcx__ehx = get_null_bitmap_ptr(arr)
            return get_bit_bitmap(nzkcx__ehx, ind)
        return impl_str
    if isinstance(arr, IntegerArrayType) or arr == boolean_array:

        def impl(arr, ind):
            return bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr.
                _null_bitmap, ind)
        return impl
    return lambda arr, ind: False


def get_nan_bits_tup(arr_tup, ind):
    return tuple(get_nan_bits(arr, ind) for arr in arr_tup)


@overload(get_nan_bits_tup, no_unliteral=True)
def overload_get_nan_bits_tup(arr_tup, ind):
    eyss__rvk = arr_tup.count
    func_text = 'def f(arr_tup, ind):\n'
    func_text += '  return ({}{})\n'.format(','.join([
        'get_nan_bits(arr_tup[{}], ind)'.format(i) for i in range(eyss__rvk
        )]), ',' if eyss__rvk == 1 else '')
    knll__jmbji = {}
    exec(func_text, {'get_nan_bits': get_nan_bits}, knll__jmbji)
    impl = knll__jmbji['f']
    return impl


def set_nan_bits(arr, ind, na_val):
    return 0


@overload(set_nan_bits, no_unliteral=True)
def overload_set_nan_bits(arr, ind, na_val):
    if arr == string_array_type:

        def impl_str(arr, ind, na_val):
            nzkcx__ehx = get_null_bitmap_ptr(arr)
            set_bit_to(nzkcx__ehx, ind, na_val)
        return impl_str
    if isinstance(arr, IntegerArrayType) or arr == boolean_array:

        def impl(arr, ind, na_val):
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, na_val)
        return impl
    return lambda arr, ind, na_val: None


def set_nan_bits_tup(arr_tup, ind, na_val):
    return tuple(set_nan_bits(arr, ind, na_val) for arr in arr_tup)


@overload(set_nan_bits_tup, no_unliteral=True)
def overload_set_nan_bits_tup(arr_tup, ind, na_val):
    eyss__rvk = arr_tup.count
    func_text = 'def f(arr_tup, ind, na_val):\n'
    for i in range(eyss__rvk):
        func_text += '  set_nan_bits(arr_tup[{}], ind, na_val[{}])\n'.format(i,
            i)
    func_text += '  return\n'
    knll__jmbji = {}
    exec(func_text, {'set_nan_bits': set_nan_bits}, knll__jmbji)
    impl = knll__jmbji['f']
    return impl
