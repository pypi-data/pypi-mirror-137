"""IR node for the data sorting"""
from collections import defaultdict
import numba
import numpy as np
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, mk_unique_var, replace_arg_nodes, replace_vars_inner, visit_vars_inner
import bodo
import bodo.libs.timsort
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_table, delete_table_decref_arrays, info_from_table, info_to_array, sort_values_table
from bodo.libs.str_arr_ext import cp_str_list_to_array, to_list_if_immutable_arr
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.utils.utils import debug_prints, gen_getitem
MIN_SAMPLES = 1000000
samplePointsPerPartitionHint = 20
MPI_ROOT = 0


class Sort(ir.Stmt):

    def __init__(self, df_in, df_out, key_arrs, out_key_arrs, df_in_vars,
        df_out_vars, inplace, loc, ascending_list=True, na_position='last'):
        self.df_in = df_in
        self.df_out = df_out
        self.key_arrs = key_arrs
        self.out_key_arrs = out_key_arrs
        self.df_in_vars = df_in_vars
        self.df_out_vars = df_out_vars
        self.inplace = inplace
        if isinstance(na_position, str):
            if na_position == 'last':
                self.na_position_b = (True,) * len(key_arrs)
            else:
                self.na_position_b = (False,) * len(key_arrs)
        else:
            self.na_position_b = tuple([(True if bmpi__mdrhd == 'last' else
                False) for bmpi__mdrhd in na_position])
        if isinstance(ascending_list, bool):
            ascending_list = (ascending_list,) * len(key_arrs)
        self.ascending_list = ascending_list
        self.loc = loc

    def __repr__(self):
        loh__qdby = ''
        for cmr__fydzl, fzdup__eomne in self.df_in_vars.items():
            loh__qdby += "'{}':{}, ".format(cmr__fydzl, fzdup__eomne.name)
        kwwub__nwxcg = '{}{{{}}}'.format(self.df_in, loh__qdby)
        twba__jobod = ''
        for cmr__fydzl, fzdup__eomne in self.df_out_vars.items():
            twba__jobod += "'{}':{}, ".format(cmr__fydzl, fzdup__eomne.name)
        ojz__ykkh = '{}{{{}}}'.format(self.df_out, twba__jobod)
        return 'sort: [key: {}] {} [key: {}] {}'.format(', '.join(
            fzdup__eomne.name for fzdup__eomne in self.key_arrs),
            kwwub__nwxcg, ', '.join(fzdup__eomne.name for fzdup__eomne in
            self.out_key_arrs), ojz__ykkh)


def sort_array_analysis(sort_node, equiv_set, typemap, array_analysis):
    fjgm__rrlrq = []
    bgtgj__tdub = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    for dtxs__yvuta in bgtgj__tdub:
        jeke__lics = equiv_set.get_shape(dtxs__yvuta)
        if jeke__lics is not None:
            fjgm__rrlrq.append(jeke__lics[0])
    if len(fjgm__rrlrq) > 1:
        equiv_set.insert_equiv(*fjgm__rrlrq)
    npozq__fdli = []
    fjgm__rrlrq = []
    fwlq__gpwsf = sort_node.out_key_arrs + list(sort_node.df_out_vars.values())
    for dtxs__yvuta in fwlq__gpwsf:
        kst__syx = typemap[dtxs__yvuta.name]
        fnepp__txkhq = array_analysis._gen_shape_call(equiv_set,
            dtxs__yvuta, kst__syx.ndim, None, npozq__fdli)
        equiv_set.insert_equiv(dtxs__yvuta, fnepp__txkhq)
        fjgm__rrlrq.append(fnepp__txkhq[0])
        equiv_set.define(dtxs__yvuta, set())
    if len(fjgm__rrlrq) > 1:
        equiv_set.insert_equiv(*fjgm__rrlrq)
    return [], npozq__fdli


numba.parfors.array_analysis.array_analysis_extensions[Sort
    ] = sort_array_analysis


def sort_distributed_analysis(sort_node, array_dists):
    bgtgj__tdub = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    lwt__nlv = sort_node.out_key_arrs + list(sort_node.df_out_vars.values())
    wgxvr__yul = Distribution.OneD
    for dtxs__yvuta in bgtgj__tdub:
        wgxvr__yul = Distribution(min(wgxvr__yul.value, array_dists[
            dtxs__yvuta.name].value))
    fnwrw__ucp = Distribution(min(wgxvr__yul.value, Distribution.OneD_Var.
        value))
    for dtxs__yvuta in lwt__nlv:
        if dtxs__yvuta.name in array_dists:
            fnwrw__ucp = Distribution(min(fnwrw__ucp.value, array_dists[
                dtxs__yvuta.name].value))
    if fnwrw__ucp != Distribution.OneD_Var:
        wgxvr__yul = fnwrw__ucp
    for dtxs__yvuta in bgtgj__tdub:
        array_dists[dtxs__yvuta.name] = wgxvr__yul
    for dtxs__yvuta in lwt__nlv:
        array_dists[dtxs__yvuta.name] = fnwrw__ucp
    return


distributed_analysis.distributed_analysis_extensions[Sort
    ] = sort_distributed_analysis


def sort_typeinfer(sort_node, typeinferer):
    for iiy__pzf, xmlvf__hjfv in zip(sort_node.key_arrs, sort_node.out_key_arrs
        ):
        typeinferer.constraints.append(typeinfer.Propagate(dst=xmlvf__hjfv.
            name, src=iiy__pzf.name, loc=sort_node.loc))
    for ftbdn__zxau, dtxs__yvuta in sort_node.df_in_vars.items():
        nwp__jgbk = sort_node.df_out_vars[ftbdn__zxau]
        typeinferer.constraints.append(typeinfer.Propagate(dst=nwp__jgbk.
            name, src=dtxs__yvuta.name, loc=sort_node.loc))
    return


typeinfer.typeinfer_extensions[Sort] = sort_typeinfer


def build_sort_definitions(sort_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    if not sort_node.inplace:
        for dtxs__yvuta in (sort_node.out_key_arrs + list(sort_node.
            df_out_vars.values())):
            definitions[dtxs__yvuta.name].append(sort_node)
    return definitions


ir_utils.build_defs_extensions[Sort] = build_sort_definitions


def visit_vars_sort(sort_node, callback, cbdata):
    if debug_prints():
        print('visiting sort vars for:', sort_node)
        print('cbdata: ', sorted(cbdata.items()))
    for qbtf__isu in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[qbtf__isu] = visit_vars_inner(sort_node.key_arrs
            [qbtf__isu], callback, cbdata)
        sort_node.out_key_arrs[qbtf__isu] = visit_vars_inner(sort_node.
            out_key_arrs[qbtf__isu], callback, cbdata)
    for ftbdn__zxau in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[ftbdn__zxau] = visit_vars_inner(sort_node.
            df_in_vars[ftbdn__zxau], callback, cbdata)
    for ftbdn__zxau in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[ftbdn__zxau] = visit_vars_inner(sort_node.
            df_out_vars[ftbdn__zxau], callback, cbdata)


ir_utils.visit_vars_extensions[Sort] = visit_vars_sort


def remove_dead_sort(sort_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    pkjq__bubx = []
    for ftbdn__zxau, dtxs__yvuta in sort_node.df_out_vars.items():
        if dtxs__yvuta.name not in lives:
            pkjq__bubx.append(ftbdn__zxau)
    for cyez__wvxd in pkjq__bubx:
        sort_node.df_in_vars.pop(cyez__wvxd)
        sort_node.df_out_vars.pop(cyez__wvxd)
    if len(sort_node.df_out_vars) == 0 and all(fzdup__eomne.name not in
        lives for fzdup__eomne in sort_node.out_key_arrs):
        return None
    return sort_node


ir_utils.remove_dead_extensions[Sort] = remove_dead_sort


def sort_usedefs(sort_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({fzdup__eomne.name for fzdup__eomne in sort_node.key_arrs})
    use_set.update({fzdup__eomne.name for fzdup__eomne in sort_node.
        df_in_vars.values()})
    if not sort_node.inplace:
        def_set.update({fzdup__eomne.name for fzdup__eomne in sort_node.
            out_key_arrs})
        def_set.update({fzdup__eomne.name for fzdup__eomne in sort_node.
            df_out_vars.values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Sort] = sort_usedefs


def get_copies_sort(sort_node, typemap):
    gqxwx__ygje = set()
    if not sort_node.inplace:
        gqxwx__ygje = set(fzdup__eomne.name for fzdup__eomne in sort_node.
            df_out_vars.values())
        gqxwx__ygje.update({fzdup__eomne.name for fzdup__eomne in sort_node
            .out_key_arrs})
    return set(), gqxwx__ygje


ir_utils.copy_propagate_extensions[Sort] = get_copies_sort


def apply_copies_sort(sort_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for qbtf__isu in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[qbtf__isu] = replace_vars_inner(sort_node.
            key_arrs[qbtf__isu], var_dict)
        sort_node.out_key_arrs[qbtf__isu] = replace_vars_inner(sort_node.
            out_key_arrs[qbtf__isu], var_dict)
    for ftbdn__zxau in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[ftbdn__zxau] = replace_vars_inner(sort_node.
            df_in_vars[ftbdn__zxau], var_dict)
    for ftbdn__zxau in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[ftbdn__zxau] = replace_vars_inner(sort_node.
            df_out_vars[ftbdn__zxau], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Sort] = apply_copies_sort


def sort_distributed_run(sort_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    zian__btx = False
    nkl__papv = list(sort_node.df_in_vars.values())
    fwlq__gpwsf = list(sort_node.df_out_vars.values())
    if array_dists is not None:
        zian__btx = True
        for fzdup__eomne in (sort_node.key_arrs + sort_node.out_key_arrs +
            nkl__papv + fwlq__gpwsf):
            if array_dists[fzdup__eomne.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                fzdup__eomne.name] != distributed_pass.Distribution.OneD_Var:
                zian__btx = False
    loc = sort_node.loc
    dbjy__hdxyo = sort_node.key_arrs[0].scope
    nodes = []
    key_arrs = sort_node.key_arrs
    if not sort_node.inplace:
        ahbg__jxcc = []
        for fzdup__eomne in key_arrs:
            ejktf__xxx = _copy_array_nodes(fzdup__eomne, nodes, typingctx,
                targetctx, typemap, calltypes)
            ahbg__jxcc.append(ejktf__xxx)
        key_arrs = ahbg__jxcc
        ypiu__lmgo = []
        for fzdup__eomne in nkl__papv:
            dvra__vbu = _copy_array_nodes(fzdup__eomne, nodes, typingctx,
                targetctx, typemap, calltypes)
            ypiu__lmgo.append(dvra__vbu)
        nkl__papv = ypiu__lmgo
    key_name_args = [('key' + str(qbtf__isu)) for qbtf__isu in range(len(
        key_arrs))]
    rwe__zam = ', '.join(key_name_args)
    col_name_args = [('c' + str(qbtf__isu)) for qbtf__isu in range(len(
        nkl__papv))]
    vvfw__zarzg = ', '.join(col_name_args)
    rkndv__ifnfa = 'def f({}, {}):\n'.format(rwe__zam, vvfw__zarzg)
    rkndv__ifnfa += get_sort_cpp_section(key_name_args, col_name_args,
        sort_node.ascending_list, sort_node.na_position_b, zian__btx)
    rkndv__ifnfa += '  return key_arrs, data\n'
    gvoih__dkmru = {}
    exec(rkndv__ifnfa, {}, gvoih__dkmru)
    lst__aby = gvoih__dkmru['f']
    fmql__yal = types.Tuple([typemap[fzdup__eomne.name] for fzdup__eomne in
        key_arrs])
    mcdf__qbisa = types.Tuple([typemap[fzdup__eomne.name] for fzdup__eomne in
        nkl__papv])
    hqk__vcyd = compile_to_numba_ir(lst__aby, {'bodo': bodo, 'np': np,
        'to_list_if_immutable_arr': to_list_if_immutable_arr,
        'cp_str_list_to_array': cp_str_list_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'sort_values_table':
        sort_values_table, 'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=tuple(list(fmql__yal.types) + list(mcdf__qbisa.
        types)), typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(hqk__vcyd, key_arrs + nkl__papv)
    nodes += hqk__vcyd.body[:-2]
    aen__jwua = nodes[-1].target
    wdcqc__qzxsn = ir.Var(dbjy__hdxyo, mk_unique_var('key_data'), loc)
    typemap[wdcqc__qzxsn.name] = fmql__yal
    gen_getitem(wdcqc__qzxsn, aen__jwua, 0, calltypes, nodes)
    biq__pkzl = ir.Var(dbjy__hdxyo, mk_unique_var('sort_data'), loc)
    typemap[biq__pkzl.name] = mcdf__qbisa
    gen_getitem(biq__pkzl, aen__jwua, 1, calltypes, nodes)
    for qbtf__isu, var in enumerate(sort_node.out_key_arrs):
        gen_getitem(var, wdcqc__qzxsn, qbtf__isu, calltypes, nodes)
    for qbtf__isu, var in enumerate(fwlq__gpwsf):
        gen_getitem(var, biq__pkzl, qbtf__isu, calltypes, nodes)
    return nodes


distributed_pass.distributed_run_extensions[Sort] = sort_distributed_run


def _copy_array_nodes(var, nodes, typingctx, targetctx, typemap, calltypes):

    def _impl(arr):
        return arr.copy()
    hqk__vcyd = compile_to_numba_ir(_impl, {}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(typemap[var.name],), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(hqk__vcyd, [var])
    nodes += hqk__vcyd.body[:-2]
    return nodes[-1].target


def get_sort_cpp_section(key_name_args, col_name_args, ascending_list,
    na_position_b, parallel_b):
    ixf__yxsrt = len(key_name_args)
    fbkpe__mikfm = ['array_to_info({})'.format(qnb__jan) for qnb__jan in
        key_name_args] + ['array_to_info({})'.format(qnb__jan) for qnb__jan in
        col_name_args]
    rkndv__ifnfa = '  info_list_total = [{}]\n'.format(','.join(fbkpe__mikfm))
    rkndv__ifnfa += '  table_total = arr_info_list_to_table(info_list_total)\n'
    rkndv__ifnfa += '  vect_ascending = np.array([{}])\n'.format(','.join(
        '1' if nddth__shnso else '0' for nddth__shnso in ascending_list))
    rkndv__ifnfa += '  na_position = np.array([{}])\n'.format(','.join('1' if
        nddth__shnso else '0' for nddth__shnso in na_position_b))
    rkndv__ifnfa += (
        """  out_table = sort_values_table(table_total, {}, vect_ascending.ctypes, na_position.ctypes, {})
"""
        .format(ixf__yxsrt, parallel_b))
    egthw__twd = 0
    czu__cnbr = []
    for qnb__jan in key_name_args:
        czu__cnbr.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(egthw__twd, qnb__jan))
        egthw__twd += 1
    rkndv__ifnfa += '  key_arrs = ({},)\n'.format(','.join(czu__cnbr))
    qku__yxb = []
    for qnb__jan in col_name_args:
        qku__yxb.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(egthw__twd, qnb__jan))
        egthw__twd += 1
    if len(qku__yxb) > 0:
        rkndv__ifnfa += '  data = ({},)\n'.format(','.join(qku__yxb))
    else:
        rkndv__ifnfa += '  data = ()\n'
    rkndv__ifnfa += '  delete_table(out_table)\n'
    rkndv__ifnfa += '  delete_table(table_total)\n'
    return rkndv__ifnfa
