"""IR node for the groupby, pivot and cross_tabulation"""
import ctypes
import operator
import types as pytypes
from collections import defaultdict, namedtuple
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, compiler, ir, ir_utils, types
from numba.core.analysis import compute_use_defs
from numba.core.ir_utils import build_definitions, compile_to_numba_ir, find_callname, find_const, find_topo_order, get_definition, get_ir_of_code, get_name_var_table, guard, is_getitem, mk_unique_var, next_label, remove_dels, replace_arg_nodes, replace_var_names, replace_vars_inner, visit_vars_inner
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, lower_builtin, overload
from numba.parfors.parfor import Parfor, unwrap_parfor_blocks, wrap_parfor_blocks
import bodo
from bodo.hiframes.datetime_date_ext import DatetimeDateArrayType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.libs.array import arr_info_list_to_table, array_to_info, compute_node_partition_by_hash, delete_info_decref_array, delete_table, delete_table_decref_arrays, groupby_and_aggregate, info_from_table, info_to_array, pivot_groupby_and_aggregate
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, pre_alloc_array_item_array
from bodo.libs.binary_arr_ext import BinaryArrayType, pre_alloc_binary_array
from bodo.libs.bool_arr_ext import BooleanArrayType
from bodo.libs.decimal_arr_ext import DecimalArrayType, alloc_decimal_array
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.utils.transform import get_call_expr_arg
from bodo.utils.typing import BodoError, get_literal_value, get_overload_const_func, get_overload_const_str, get_overload_constant_dict, is_overload_constant_dict, is_overload_constant_str, list_cumulative
from bodo.utils.utils import debug_prints, incref, is_assign, is_call_assign, is_expr, is_null_pointer, is_var_assign, sanitize_varname, unliteral_all
gb_agg_cfunc = {}
gb_agg_cfunc_addr = {}


@intrinsic
def add_agg_cfunc_sym(typingctx, func, sym):

    def codegen(context, builder, signature, args):
        sig = func.signature
        if sig == types.none(types.voidptr):
            brdls__iuw = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer()])
            yna__rocm = cgutils.get_or_insert_function(builder.module,
                brdls__iuw, sym._literal_value)
            builder.call(yna__rocm, [context.get_constant_null(sig.args[0])])
        elif sig == types.none(types.int64, types.voidptr, types.voidptr):
            brdls__iuw = lir.FunctionType(lir.VoidType(), [lir.IntType(64),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
            yna__rocm = cgutils.get_or_insert_function(builder.module,
                brdls__iuw, sym._literal_value)
            builder.call(yna__rocm, [context.get_constant(types.int64, 0),
                context.get_constant_null(sig.args[1]), context.
                get_constant_null(sig.args[2])])
        else:
            brdls__iuw = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64).
                as_pointer()])
            yna__rocm = cgutils.get_or_insert_function(builder.module,
                brdls__iuw, sym._literal_value)
            builder.call(yna__rocm, [context.get_constant_null(sig.args[0]),
                context.get_constant_null(sig.args[1]), context.
                get_constant_null(sig.args[2])])
        context.add_linking_libs([gb_agg_cfunc[sym._literal_value]._library])
        return
    return types.none(func, sym), codegen


@numba.jit
def get_agg_udf_addr(name):
    with numba.objmode(addr='int64'):
        addr = gb_agg_cfunc_addr[name]
    return addr


class AggUDFStruct(object):

    def __init__(self, regular_udf_funcs=None, general_udf_funcs=None):
        assert regular_udf_funcs is not None or general_udf_funcs is not None
        self.regular_udfs = False
        self.general_udfs = False
        self.regular_udf_cfuncs = None
        self.general_udf_cfunc = None
        if regular_udf_funcs is not None:
            (self.var_typs, self.init_func, self.update_all_func, self.
                combine_all_func, self.eval_all_func) = regular_udf_funcs
            self.regular_udfs = True
        if general_udf_funcs is not None:
            self.general_udf_funcs = general_udf_funcs
            self.general_udfs = True

    def set_regular_cfuncs(self, update_cb, combine_cb, eval_cb):
        assert self.regular_udfs and self.regular_udf_cfuncs is None
        self.regular_udf_cfuncs = [update_cb, combine_cb, eval_cb]

    def set_general_cfunc(self, general_udf_cb):
        assert self.general_udfs and self.general_udf_cfunc is None
        self.general_udf_cfunc = general_udf_cb


AggFuncStruct = namedtuple('AggFuncStruct', ['func', 'ftype'])
supported_agg_funcs = ['no_op', 'head', 'transform', 'size', 'shift', 'sum',
    'count', 'nunique', 'median', 'cumsum', 'cumprod', 'cummin', 'cummax',
    'mean', 'min', 'max', 'prod', 'first', 'last', 'idxmin', 'idxmax',
    'var', 'std', 'udf', 'gen_udf']
supported_transform_funcs = ['no_op', 'sum', 'count', 'nunique', 'median',
    'mean', 'min', 'max', 'prod', 'first', 'last', 'var', 'std']


def get_agg_func(func_ir, func_name, rhs, series_type=None, typemap=None):
    if func_name == 'no_op':
        raise BodoError('Unknown aggregation function used in groupby.')
    if series_type is None:
        series_type = SeriesType(types.float64)
    if func_name in {'var', 'std'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 3
        func.ncols_post_shuffle = 4
        return func
    if func_name in {'first', 'last'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        return func
    if func_name in {'idxmin', 'idxmax'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 2
        func.ncols_post_shuffle = 2
        return func
    if func_name in supported_agg_funcs[:-8]:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        sjih__yyjhr = True
        jgzf__xgc = 1
        daqh__rob = -1
        if isinstance(rhs, ir.Expr):
            for vba__mtas in rhs.kws:
                if func_name in list_cumulative:
                    if vba__mtas[0] == 'skipna':
                        sjih__yyjhr = guard(find_const, func_ir, vba__mtas[1])
                        if not isinstance(sjih__yyjhr, bool):
                            raise BodoError(
                                'For {} argument of skipna should be a boolean'
                                .format(func_name))
                if func_name == 'nunique':
                    if vba__mtas[0] == 'dropna':
                        sjih__yyjhr = guard(find_const, func_ir, vba__mtas[1])
                        if not isinstance(sjih__yyjhr, bool):
                            raise BodoError(
                                'argument of dropna to nunique should be a boolean'
                                )
        if func_name == 'shift' and (len(rhs.args) > 0 or len(rhs.kws) > 0):
            jgzf__xgc = get_call_expr_arg('shift', rhs.args, dict(rhs.kws),
                0, 'periods', jgzf__xgc)
            jgzf__xgc = guard(find_const, func_ir, jgzf__xgc)
        if func_name == 'head':
            daqh__rob = get_call_expr_arg('head', rhs.args, dict(rhs.kws), 
                0, 'n', 5)
            if not isinstance(daqh__rob, int):
                daqh__rob = guard(find_const, func_ir, daqh__rob)
            if daqh__rob < 0:
                raise BodoError(
                    f'groupby.{func_name} does not work with negative values.')
        func.skipdropna = sjih__yyjhr
        func.periods = jgzf__xgc
        func.head_n = daqh__rob
        if func_name == 'transform':
            kws = dict(rhs.kws)
            lzgw__tbox = get_call_expr_arg(func_name, rhs.args, kws, 0,
                'func', '')
            fjblc__mgy = typemap[lzgw__tbox.name]
            xttr__rpc = None
            if isinstance(fjblc__mgy, str):
                xttr__rpc = fjblc__mgy
            elif is_overload_constant_str(fjblc__mgy):
                xttr__rpc = get_overload_const_str(fjblc__mgy)
            elif bodo.utils.typing.is_builtin_function(fjblc__mgy):
                xttr__rpc = bodo.utils.typing.get_builtin_function_name(
                    fjblc__mgy)
            if xttr__rpc not in bodo.ir.aggregate.supported_transform_funcs[:]:
                raise BodoError(f'unsupported transform function {xttr__rpc}')
            func.transform_func = supported_agg_funcs.index(xttr__rpc)
        else:
            func.transform_func = supported_agg_funcs.index('no_op')
        return func
    assert func_name in ['agg', 'aggregate']
    assert typemap is not None
    kws = dict(rhs.kws)
    lzgw__tbox = get_call_expr_arg(func_name, rhs.args, kws, 0, 'func', '')
    if lzgw__tbox == '':
        fjblc__mgy = types.none
    else:
        fjblc__mgy = typemap[lzgw__tbox.name]
    if is_overload_constant_dict(fjblc__mgy):
        bqn__knv = get_overload_constant_dict(fjblc__mgy)
        amycx__ipifb = [get_agg_func_udf(func_ir, f_val, rhs, series_type,
            typemap) for f_val in bqn__knv.values()]
        return amycx__ipifb
    if fjblc__mgy == types.none:
        return [get_agg_func_udf(func_ir, get_literal_value(typemap[f_val.
            name])[1], rhs, series_type, typemap) for f_val in kws.values()]
    if isinstance(fjblc__mgy, types.BaseTuple):
        amycx__ipifb = []
        tth__xrytv = 0
        for t in fjblc__mgy.types:
            if is_overload_constant_str(t):
                func_name = get_overload_const_str(t)
                amycx__ipifb.append(get_agg_func(func_ir, func_name, rhs,
                    series_type, typemap))
            else:
                assert typemap is not None, 'typemap is required for agg UDF handling'
                func = _get_const_agg_func(t, func_ir)
                func.ftype = 'udf'
                func.fname = _get_udf_name(func)
                if func.fname == '<lambda>':
                    func.fname = '<lambda_' + str(tth__xrytv) + '>'
                    tth__xrytv += 1
                amycx__ipifb.append(func)
        return [amycx__ipifb]
    if is_overload_constant_str(fjblc__mgy):
        func_name = get_overload_const_str(fjblc__mgy)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(fjblc__mgy):
        func_name = bodo.utils.typing.get_builtin_function_name(fjblc__mgy)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    assert typemap is not None, 'typemap is required for agg UDF handling'
    func = _get_const_agg_func(typemap[rhs.args[0].name], func_ir)
    func.ftype = 'udf'
    func.fname = _get_udf_name(func)
    return func


def get_agg_func_udf(func_ir, f_val, rhs, series_type, typemap):
    if isinstance(f_val, str):
        return get_agg_func(func_ir, f_val, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(f_val):
        func_name = bodo.utils.typing.get_builtin_function_name(f_val)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if isinstance(f_val, (tuple, list)):
        tth__xrytv = 0
        qls__jghlc = []
        for xml__xeq in f_val:
            func = get_agg_func_udf(func_ir, xml__xeq, rhs, series_type,
                typemap)
            if func.fname == '<lambda>' and len(f_val) > 1:
                func.fname = f'<lambda_{tth__xrytv}>'
                tth__xrytv += 1
            qls__jghlc.append(func)
        return qls__jghlc
    else:
        assert is_expr(f_val, 'make_function') or isinstance(f_val, (numba.
            core.registry.CPUDispatcher, types.Dispatcher))
        assert typemap is not None, 'typemap is required for agg UDF handling'
        func = _get_const_agg_func(f_val, func_ir)
        func.ftype = 'udf'
        func.fname = _get_udf_name(func)
        return func


def _get_udf_name(func):
    code = func.code if hasattr(func, 'code') else func.__code__
    xttr__rpc = code.co_name
    return xttr__rpc


def _get_const_agg_func(func_typ, func_ir):
    agg_func = get_overload_const_func(func_typ, func_ir)
    if is_expr(agg_func, 'make_function'):

        def agg_func_wrapper(A):
            return A
        agg_func_wrapper.__code__ = agg_func.code
        agg_func = agg_func_wrapper
        return agg_func
    return agg_func


@infer_global(type)
class TypeDt64(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if len(args) == 1 and isinstance(args[0], (types.NPDatetime, types.
            NPTimedelta)):
            bnz__okzvk = types.DType(args[0])
            return signature(bnz__okzvk, *args)


@numba.njit(no_cpython_wrapper=True)
def _var_combine(ssqdm_a, mean_a, nobs_a, ssqdm_b, mean_b, nobs_b):
    stbh__vsm = nobs_a + nobs_b
    hidwt__bdzsq = (nobs_a * mean_a + nobs_b * mean_b) / stbh__vsm
    yihvs__norv = mean_b - mean_a
    lhc__djha = (ssqdm_a + ssqdm_b + yihvs__norv * yihvs__norv * nobs_a *
        nobs_b / stbh__vsm)
    return lhc__djha, hidwt__bdzsq, stbh__vsm


def __special_combine(*args):
    return


@infer_global(__special_combine)
class SpecialCombineTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *unliteral_all(args))


@lower_builtin(__special_combine, types.VarArg(types.Any))
def lower_special_combine(context, builder, sig, args):
    return context.get_dummy_value()


class Aggregate(ir.Stmt):

    def __init__(self, df_out, df_in, key_names, gb_info_in, gb_info_out,
        out_key_vars, df_out_vars, df_in_vars, key_arrs, input_has_index,
        same_index, return_key, loc, func_name, dropna=True, pivot_arr=None,
        pivot_values=None, is_crosstab=False):
        self.df_out = df_out
        self.df_in = df_in
        self.key_names = key_names
        self.gb_info_in = gb_info_in
        self.gb_info_out = gb_info_out
        self.out_key_vars = out_key_vars
        self.df_out_vars = df_out_vars
        self.df_in_vars = df_in_vars
        self.key_arrs = key_arrs
        self.input_has_index = input_has_index
        self.same_index = same_index
        self.return_key = return_key
        self.loc = loc
        self.func_name = func_name
        self.dropna = dropna
        self.pivot_arr = pivot_arr
        self.pivot_values = pivot_values
        self.is_crosstab = is_crosstab

    def __repr__(self):
        ise__xvdu = ''
        for dcqr__hnz, v in self.df_out_vars.items():
            ise__xvdu += "'{}':{}, ".format(dcqr__hnz, v.name)
        ofpx__bggr = '{}{{{}}}'.format(self.df_out, ise__xvdu)
        aslt__uxzfz = ''
        for dcqr__hnz, v in self.df_in_vars.items():
            aslt__uxzfz += "'{}':{}, ".format(dcqr__hnz, v.name)
        mqxy__gnk = '{}{{{}}}'.format(self.df_in, aslt__uxzfz)
        sck__aikr = 'pivot {}:{}'.format(self.pivot_arr.name, self.pivot_values
            ) if self.pivot_arr is not None else ''
        key_names = ','.join(self.key_names)
        ngqc__otok = ','.join([v.name for v in self.key_arrs])
        return 'aggregate: {} = {} [key: {}:{}] {}'.format(ofpx__bggr,
            mqxy__gnk, key_names, ngqc__otok, sck__aikr)

    def remove_out_col(self, out_col_name):
        self.df_out_vars.pop(out_col_name)
        ayj__efksk, yfc__wtvj = self.gb_info_out.pop(out_col_name)
        if ayj__efksk is None and not self.is_crosstab:
            return
        gei__syyj = self.gb_info_in[ayj__efksk]
        if self.pivot_arr is not None:
            self.pivot_values.remove(out_col_name)
            for i, (func, ise__xvdu) in enumerate(gei__syyj):
                try:
                    ise__xvdu.remove(out_col_name)
                    if len(ise__xvdu) == 0:
                        gei__syyj.pop(i)
                        break
                except ValueError as gosx__izuz:
                    continue
        else:
            for i, (func, ljcu__eduy) in enumerate(gei__syyj):
                if ljcu__eduy == out_col_name:
                    gei__syyj.pop(i)
                    break
        if len(gei__syyj) == 0:
            self.gb_info_in.pop(ayj__efksk)
            self.df_in_vars.pop(ayj__efksk)


def aggregate_usedefs(aggregate_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({v.name for v in aggregate_node.key_arrs})
    use_set.update({v.name for v in aggregate_node.df_in_vars.values()})
    if aggregate_node.pivot_arr is not None:
        use_set.add(aggregate_node.pivot_arr.name)
    def_set.update({v.name for v in aggregate_node.df_out_vars.values()})
    if aggregate_node.out_key_vars is not None:
        def_set.update({v.name for v in aggregate_node.out_key_vars})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Aggregate] = aggregate_usedefs


def remove_dead_aggregate(aggregate_node, lives_no_aliases, lives,
    arg_aliases, alias_map, func_ir, typemap):
    ayoj__ojvpx = [dpgf__btbry for dpgf__btbry, nzt__ghp in aggregate_node.
        df_out_vars.items() if nzt__ghp.name not in lives]
    for hhs__jvwv in ayoj__ojvpx:
        aggregate_node.remove_out_col(hhs__jvwv)
    out_key_vars = aggregate_node.out_key_vars
    if out_key_vars is not None and all(v.name not in lives for v in
        out_key_vars):
        aggregate_node.out_key_vars = None
    if len(aggregate_node.df_out_vars
        ) == 0 and aggregate_node.out_key_vars is None:
        return None
    return aggregate_node


ir_utils.remove_dead_extensions[Aggregate] = remove_dead_aggregate


def get_copies_aggregate(aggregate_node, typemap):
    kiog__stejb = set(v.name for v in aggregate_node.df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        kiog__stejb.update({v.name for v in aggregate_node.out_key_vars})
    return set(), kiog__stejb


ir_utils.copy_propagate_extensions[Aggregate] = get_copies_aggregate


def apply_copies_aggregate(aggregate_node, var_dict, name_var_table,
    typemap, calltypes, save_copies):
    for i in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[i] = replace_vars_inner(aggregate_node.
            key_arrs[i], var_dict)
    for dpgf__btbry in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[dpgf__btbry] = replace_vars_inner(
            aggregate_node.df_in_vars[dpgf__btbry], var_dict)
    for dpgf__btbry in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[dpgf__btbry] = replace_vars_inner(
            aggregate_node.df_out_vars[dpgf__btbry], var_dict)
    if aggregate_node.out_key_vars is not None:
        for i in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[i] = replace_vars_inner(aggregate_node
                .out_key_vars[i], var_dict)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = replace_vars_inner(aggregate_node.
            pivot_arr, var_dict)


ir_utils.apply_copy_propagate_extensions[Aggregate] = apply_copies_aggregate


def visit_vars_aggregate(aggregate_node, callback, cbdata):
    if debug_prints():
        print('visiting aggregate vars for:', aggregate_node)
        print('cbdata: ', sorted(cbdata.items()))
    for i in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[i] = visit_vars_inner(aggregate_node.
            key_arrs[i], callback, cbdata)
    for dpgf__btbry in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[dpgf__btbry] = visit_vars_inner(
            aggregate_node.df_in_vars[dpgf__btbry], callback, cbdata)
    for dpgf__btbry in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[dpgf__btbry] = visit_vars_inner(
            aggregate_node.df_out_vars[dpgf__btbry], callback, cbdata)
    if aggregate_node.out_key_vars is not None:
        for i in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[i] = visit_vars_inner(aggregate_node
                .out_key_vars[i], callback, cbdata)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = visit_vars_inner(aggregate_node.
            pivot_arr, callback, cbdata)


ir_utils.visit_vars_extensions[Aggregate] = visit_vars_aggregate


def aggregate_array_analysis(aggregate_node, equiv_set, typemap, array_analysis
    ):
    assert len(aggregate_node.df_out_vars
        ) > 0 or aggregate_node.out_key_vars is not None or aggregate_node.is_crosstab, 'empty aggregate in array analysis'
    rauyd__qkf = []
    for xpwsh__bqk in aggregate_node.key_arrs:
        cdhe__knn = equiv_set.get_shape(xpwsh__bqk)
        if cdhe__knn:
            rauyd__qkf.append(cdhe__knn[0])
    if aggregate_node.pivot_arr is not None:
        cdhe__knn = equiv_set.get_shape(aggregate_node.pivot_arr)
        if cdhe__knn:
            rauyd__qkf.append(cdhe__knn[0])
    for nzt__ghp in aggregate_node.df_in_vars.values():
        cdhe__knn = equiv_set.get_shape(nzt__ghp)
        if cdhe__knn:
            rauyd__qkf.append(cdhe__knn[0])
    if len(rauyd__qkf) > 1:
        equiv_set.insert_equiv(*rauyd__qkf)
    hcn__ucxds = []
    rauyd__qkf = []
    xftzb__xhzii = list(aggregate_node.df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        xftzb__xhzii.extend(aggregate_node.out_key_vars)
    for nzt__ghp in xftzb__xhzii:
        myrtd__ciz = typemap[nzt__ghp.name]
        ctwr__zkzau = array_analysis._gen_shape_call(equiv_set, nzt__ghp,
            myrtd__ciz.ndim, None, hcn__ucxds)
        equiv_set.insert_equiv(nzt__ghp, ctwr__zkzau)
        rauyd__qkf.append(ctwr__zkzau[0])
        equiv_set.define(nzt__ghp, set())
    if len(rauyd__qkf) > 1:
        equiv_set.insert_equiv(*rauyd__qkf)
    return [], hcn__ucxds


numba.parfors.array_analysis.array_analysis_extensions[Aggregate
    ] = aggregate_array_analysis


def aggregate_distributed_analysis(aggregate_node, array_dists):
    zhiq__tadt = Distribution.OneD
    for nzt__ghp in aggregate_node.df_in_vars.values():
        zhiq__tadt = Distribution(min(zhiq__tadt.value, array_dists[
            nzt__ghp.name].value))
    for xpwsh__bqk in aggregate_node.key_arrs:
        zhiq__tadt = Distribution(min(zhiq__tadt.value, array_dists[
            xpwsh__bqk.name].value))
    if aggregate_node.pivot_arr is not None:
        zhiq__tadt = Distribution(min(zhiq__tadt.value, array_dists[
            aggregate_node.pivot_arr.name].value))
        array_dists[aggregate_node.pivot_arr.name] = zhiq__tadt
    for nzt__ghp in aggregate_node.df_in_vars.values():
        array_dists[nzt__ghp.name] = zhiq__tadt
    for xpwsh__bqk in aggregate_node.key_arrs:
        array_dists[xpwsh__bqk.name] = zhiq__tadt
    dshkn__qevp = Distribution.OneD_Var
    for nzt__ghp in aggregate_node.df_out_vars.values():
        if nzt__ghp.name in array_dists:
            dshkn__qevp = Distribution(min(dshkn__qevp.value, array_dists[
                nzt__ghp.name].value))
    if aggregate_node.out_key_vars is not None:
        for nzt__ghp in aggregate_node.out_key_vars:
            if nzt__ghp.name in array_dists:
                dshkn__qevp = Distribution(min(dshkn__qevp.value,
                    array_dists[nzt__ghp.name].value))
    dshkn__qevp = Distribution(min(dshkn__qevp.value, zhiq__tadt.value))
    for nzt__ghp in aggregate_node.df_out_vars.values():
        array_dists[nzt__ghp.name] = dshkn__qevp
    if aggregate_node.out_key_vars is not None:
        for jfw__map in aggregate_node.out_key_vars:
            array_dists[jfw__map.name] = dshkn__qevp
    if dshkn__qevp != Distribution.OneD_Var:
        for xpwsh__bqk in aggregate_node.key_arrs:
            array_dists[xpwsh__bqk.name] = dshkn__qevp
        if aggregate_node.pivot_arr is not None:
            array_dists[aggregate_node.pivot_arr.name] = dshkn__qevp
        for nzt__ghp in aggregate_node.df_in_vars.values():
            array_dists[nzt__ghp.name] = dshkn__qevp


distributed_analysis.distributed_analysis_extensions[Aggregate
    ] = aggregate_distributed_analysis


def build_agg_definitions(agg_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for nzt__ghp in agg_node.df_out_vars.values():
        definitions[nzt__ghp.name].append(agg_node)
    if agg_node.out_key_vars is not None:
        for jfw__map in agg_node.out_key_vars:
            definitions[jfw__map.name].append(agg_node)
    return definitions


ir_utils.build_defs_extensions[Aggregate] = build_agg_definitions


def __update_redvars():
    pass


@infer_global(__update_redvars)
class UpdateDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *args)


def __combine_redvars():
    pass


@infer_global(__combine_redvars)
class CombineDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *args)


def __eval_res():
    pass


@infer_global(__eval_res)
class EvalDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(args[0].dtype, *args)


def agg_distributed_run(agg_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    parallel = False
    if array_dists is not None:
        parallel = True
        for v in (list(agg_node.df_in_vars.values()) + list(agg_node.
            df_out_vars.values()) + agg_node.key_arrs):
            if array_dists[v.name
                ] != distributed_pass.Distribution.OneD and array_dists[v.name
                ] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    law__ftphz = tuple(typemap[v.name] for v in agg_node.key_arrs)
    wlbx__ach = [v for vjyp__jbgjx, v in agg_node.df_in_vars.items()]
    elu__gpkyf = [v for vjyp__jbgjx, v in agg_node.df_out_vars.items()]
    in_col_typs = []
    amycx__ipifb = []
    if agg_node.pivot_arr is not None:
        for ayj__efksk, gei__syyj in agg_node.gb_info_in.items():
            for func, yfc__wtvj in gei__syyj:
                if ayj__efksk is not None:
                    in_col_typs.append(typemap[agg_node.df_in_vars[
                        ayj__efksk].name])
                amycx__ipifb.append(func)
    else:
        for ayj__efksk, func in agg_node.gb_info_out.values():
            if ayj__efksk is not None:
                in_col_typs.append(typemap[agg_node.df_in_vars[ayj__efksk].
                    name])
            amycx__ipifb.append(func)
    out_col_typs = tuple(typemap[v.name] for v in elu__gpkyf)
    pivot_typ = types.none if agg_node.pivot_arr is None else typemap[
        agg_node.pivot_arr.name]
    arg_typs = tuple(law__ftphz + tuple(typemap[v.name] for v in wlbx__ach) +
        (pivot_typ,))
    ozlyq__ulq = {'bodo': bodo, 'np': np, 'dt64_dtype': np.dtype(
        'datetime64[ns]'), 'td64_dtype': np.dtype('timedelta64[ns]')}
    for i, in_col_typ in enumerate(in_col_typs):
        if isinstance(in_col_typ, bodo.CategoricalArrayType):
            ozlyq__ulq.update({f'in_cat_dtype_{i}': in_col_typ})
    for i, pfkh__muqtr in enumerate(out_col_typs):
        if isinstance(pfkh__muqtr, bodo.CategoricalArrayType):
            ozlyq__ulq.update({f'out_cat_dtype_{i}': pfkh__muqtr})
    udf_func_struct = get_udf_func_struct(amycx__ipifb, agg_node.
        input_has_index, in_col_typs, out_col_typs, typingctx, targetctx,
        pivot_typ, agg_node.pivot_values, agg_node.is_crosstab)
    viyf__yhrp = gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs,
        parallel, udf_func_struct)
    ozlyq__ulq.update({'pd': pd, 'pre_alloc_string_array':
        pre_alloc_string_array, 'pre_alloc_binary_array':
        pre_alloc_binary_array, 'pre_alloc_array_item_array':
        pre_alloc_array_item_array, 'string_array_type': string_array_type,
        'alloc_decimal_array': alloc_decimal_array, 'array_to_info':
        array_to_info, 'arr_info_list_to_table': arr_info_list_to_table,
        'coerce_to_array': bodo.utils.conversion.coerce_to_array,
        'groupby_and_aggregate': groupby_and_aggregate,
        'pivot_groupby_and_aggregate': pivot_groupby_and_aggregate,
        'compute_node_partition_by_hash': compute_node_partition_by_hash,
        'info_from_table': info_from_table, 'info_to_array': info_to_array,
        'delete_info_decref_array': delete_info_decref_array,
        'delete_table': delete_table, 'add_agg_cfunc_sym':
        add_agg_cfunc_sym, 'get_agg_udf_addr': get_agg_udf_addr,
        'delete_table_decref_arrays': delete_table_decref_arrays})
    if udf_func_struct is not None:
        if udf_func_struct.regular_udfs:
            ozlyq__ulq.update({'__update_redvars': udf_func_struct.
                update_all_func, '__init_func': udf_func_struct.init_func,
                '__combine_redvars': udf_func_struct.combine_all_func,
                '__eval_res': udf_func_struct.eval_all_func,
                'cpp_cb_update': udf_func_struct.regular_udf_cfuncs[0],
                'cpp_cb_combine': udf_func_struct.regular_udf_cfuncs[1],
                'cpp_cb_eval': udf_func_struct.regular_udf_cfuncs[2]})
        if udf_func_struct.general_udfs:
            ozlyq__ulq.update({'cpp_cb_general': udf_func_struct.
                general_udf_cfunc})
    mgcz__mkj = compile_to_numba_ir(viyf__yhrp, ozlyq__ulq, typingctx=
        typingctx, targetctx=targetctx, arg_typs=arg_typs, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    aedq__fys = []
    if agg_node.pivot_arr is None:
        jqftw__cjot = agg_node.key_arrs[0].scope
        loc = agg_node.loc
        dkh__vvyn = ir.Var(jqftw__cjot, mk_unique_var('dummy_none'), loc)
        typemap[dkh__vvyn.name] = types.none
        aedq__fys.append(ir.Assign(ir.Const(None, loc), dkh__vvyn, loc))
        wlbx__ach.append(dkh__vvyn)
    else:
        wlbx__ach.append(agg_node.pivot_arr)
    replace_arg_nodes(mgcz__mkj, agg_node.key_arrs + wlbx__ach)
    pvn__lnpq = mgcz__mkj.body[-3]
    assert is_assign(pvn__lnpq) and isinstance(pvn__lnpq.value, ir.Expr
        ) and pvn__lnpq.value.op == 'build_tuple'
    aedq__fys += mgcz__mkj.body[:-3]
    xftzb__xhzii = list(agg_node.df_out_vars.values())
    if agg_node.out_key_vars is not None:
        xftzb__xhzii += agg_node.out_key_vars
    for i, ykb__kfro in enumerate(xftzb__xhzii):
        wmm__orr = pvn__lnpq.value.items[i]
        aedq__fys.append(ir.Assign(wmm__orr, ykb__kfro, ykb__kfro.loc))
    return aedq__fys


distributed_pass.distributed_run_extensions[Aggregate] = agg_distributed_run


def get_numba_set(dtype):
    pass


@infer_global(get_numba_set)
class GetNumbaSetTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        arr = args[0]
        dtype = types.Tuple([t.dtype for t in arr.types]) if isinstance(arr,
            types.BaseTuple) else arr.dtype
        if isinstance(arr, types.BaseTuple) and len(arr.types) == 1:
            dtype = arr.types[0].dtype
        return signature(types.Set(dtype), *args)


@lower_builtin(get_numba_set, types.Any)
def lower_get_numba_set(context, builder, sig, args):
    return numba.cpython.setobj.set_empty_constructor(context, builder, sig,
        args)


@infer_global(bool)
class BoolNoneTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        llbvm__vru = args[0]
        if llbvm__vru == types.none:
            return signature(types.boolean, *args)


@lower_builtin(bool, types.none)
def lower_column_mean_impl(context, builder, sig, args):
    ybz__lpozt = context.compile_internal(builder, lambda a: False, sig, args)
    return ybz__lpozt


def setitem_array_with_str(arr, i, v):
    return


@overload(setitem_array_with_str)
def setitem_array_with_str_overload(arr, i, val):
    if arr == string_array_type:

        def setitem_str_arr(arr, i, val):
            arr[i] = val
        return setitem_str_arr
    if val == string_type:
        return lambda arr, i, val: None

    def setitem_impl(arr, i, val):
        arr[i] = val
    return setitem_impl


def _gen_dummy_alloc(t, colnum=0, is_input=False):
    if isinstance(t, IntegerArrayType):
        nguri__wnd = IntDtype(t.dtype).name
        assert nguri__wnd.endswith('Dtype()')
        nguri__wnd = nguri__wnd[:-7]
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype='{nguri__wnd}'))"
            )
    elif isinstance(t, BooleanArrayType):
        return (
            'bodo.libs.bool_arr_ext.init_bool_array(np.empty(0, np.bool_), np.empty(0, np.uint8))'
            )
    elif isinstance(t, StringArrayType):
        return 'pre_alloc_string_array(1, 1)'
    elif isinstance(t, BinaryArrayType):
        return 'pre_alloc_binary_array(1, 1)'
    elif t == ArrayItemArrayType(string_array_type):
        return 'pre_alloc_array_item_array(1, (1, 1), string_array_type)'
    elif isinstance(t, DecimalArrayType):
        return 'alloc_decimal_array(1, {}, {})'.format(t.precision, t.scale)
    elif isinstance(t, DatetimeDateArrayType):
        return (
            'bodo.hiframes.datetime_date_ext.init_datetime_date_array(np.empty(1, np.int64), np.empty(1, np.uint8))'
            )
    elif isinstance(t, bodo.CategoricalArrayType):
        if t.dtype.categories is None:
            raise BodoError(
                'Groupby agg operations on Categorical types require constant categories'
                )
        are__bxso = 'in' if is_input else 'out'
        return (
            f'bodo.utils.utils.alloc_type(1, {are__bxso}_cat_dtype_{colnum})')
    else:
        return 'np.empty(1, {})'.format(_get_np_dtype(t.dtype))


def _get_np_dtype(t):
    if t == types.bool_:
        return 'np.bool_'
    if t == types.NPDatetime('ns'):
        return 'dt64_dtype'
    if t == types.NPTimedelta('ns'):
        return 'td64_dtype'
    return 'np.{}'.format(t)


def gen_update_cb(udf_func_struct, allfuncs, n_keys, data_in_typs_,
    out_data_typs, do_combine, func_idx_to_in_col, label_suffix):
    zdbxn__psdj = udf_func_struct.var_typs
    ecld__xhwk = len(zdbxn__psdj)
    hhz__sim = (
        'def bodo_gb_udf_update_local{}(in_table, out_table, row_to_group):\n'
        .format(label_suffix))
    hhz__sim += '    if is_null_pointer(in_table):\n'
    hhz__sim += '        return\n'
    hhz__sim += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in zdbxn__psdj]), 
        ',' if len(zdbxn__psdj) == 1 else '')
    kvbvu__zhurm = n_keys
    qqv__poima = []
    redvar_offsets = []
    aqmv__ffpf = []
    if do_combine:
        for i, xml__xeq in enumerate(allfuncs):
            if xml__xeq.ftype != 'udf':
                kvbvu__zhurm += xml__xeq.ncols_pre_shuffle
            else:
                redvar_offsets += list(range(kvbvu__zhurm, kvbvu__zhurm +
                    xml__xeq.n_redvars))
                kvbvu__zhurm += xml__xeq.n_redvars
                aqmv__ffpf.append(data_in_typs_[func_idx_to_in_col[i]])
                qqv__poima.append(func_idx_to_in_col[i] + n_keys)
    else:
        for i, xml__xeq in enumerate(allfuncs):
            if xml__xeq.ftype != 'udf':
                kvbvu__zhurm += xml__xeq.ncols_post_shuffle
            else:
                redvar_offsets += list(range(kvbvu__zhurm + 1, kvbvu__zhurm +
                    1 + xml__xeq.n_redvars))
                kvbvu__zhurm += xml__xeq.n_redvars + 1
                aqmv__ffpf.append(data_in_typs_[func_idx_to_in_col[i]])
                qqv__poima.append(func_idx_to_in_col[i] + n_keys)
    assert len(redvar_offsets) == ecld__xhwk
    phv__wdx = len(aqmv__ffpf)
    fgtuq__ghrof = []
    for i, t in enumerate(aqmv__ffpf):
        fgtuq__ghrof.append(_gen_dummy_alloc(t, i, True))
    hhz__sim += '    data_in_dummy = ({}{})\n'.format(','.join(fgtuq__ghrof
        ), ',' if len(aqmv__ffpf) == 1 else '')
    hhz__sim += """
    # initialize redvar cols
"""
    hhz__sim += '    init_vals = __init_func()\n'
    for i in range(ecld__xhwk):
        hhz__sim += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(i, redvar_offsets[i], i))
        hhz__sim += '    incref(redvar_arr_{})\n'.format(i)
        hhz__sim += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(i, i)
    hhz__sim += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(i) for i in range(ecld__xhwk)]), ',' if ecld__xhwk == 1 else '')
    hhz__sim += '\n'
    for i in range(phv__wdx):
        hhz__sim += (
            """    data_in_{} = info_to_array(info_from_table(in_table, {}), data_in_dummy[{}])
"""
            .format(i, qqv__poima[i], i))
        hhz__sim += '    incref(data_in_{})\n'.format(i)
    hhz__sim += '    data_in = ({}{})\n'.format(','.join(['data_in_{}'.
        format(i) for i in range(phv__wdx)]), ',' if phv__wdx == 1 else '')
    hhz__sim += '\n'
    hhz__sim += '    for i in range(len(data_in_0)):\n'
    hhz__sim += '        w_ind = row_to_group[i]\n'
    hhz__sim += '        if w_ind != -1:\n'
    hhz__sim += (
        '            __update_redvars(redvars, data_in, w_ind, i, pivot_arr=None)\n'
        )
    yrnlc__cynz = {}
    exec(hhz__sim, {'bodo': bodo, 'np': np, 'pd': pd, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table, 'incref': incref,
        'pre_alloc_string_array': pre_alloc_string_array, '__init_func':
        udf_func_struct.init_func, '__update_redvars': udf_func_struct.
        update_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, yrnlc__cynz)
    return yrnlc__cynz['bodo_gb_udf_update_local{}'.format(label_suffix)]


def gen_combine_cb(udf_func_struct, allfuncs, n_keys, out_data_typs,
    label_suffix):
    zdbxn__psdj = udf_func_struct.var_typs
    ecld__xhwk = len(zdbxn__psdj)
    hhz__sim = (
        'def bodo_gb_udf_combine{}(in_table, out_table, row_to_group):\n'.
        format(label_suffix))
    hhz__sim += '    if is_null_pointer(in_table):\n'
    hhz__sim += '        return\n'
    hhz__sim += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in zdbxn__psdj]), 
        ',' if len(zdbxn__psdj) == 1 else '')
    njze__fkq = n_keys
    wyj__civ = n_keys
    pnjp__qgoy = []
    cvmb__vrjx = []
    for xml__xeq in allfuncs:
        if xml__xeq.ftype != 'udf':
            njze__fkq += xml__xeq.ncols_pre_shuffle
            wyj__civ += xml__xeq.ncols_post_shuffle
        else:
            pnjp__qgoy += list(range(njze__fkq, njze__fkq + xml__xeq.n_redvars)
                )
            cvmb__vrjx += list(range(wyj__civ + 1, wyj__civ + 1 + xml__xeq.
                n_redvars))
            njze__fkq += xml__xeq.n_redvars
            wyj__civ += 1 + xml__xeq.n_redvars
    assert len(pnjp__qgoy) == ecld__xhwk
    hhz__sim += """
    # initialize redvar cols
"""
    hhz__sim += '    init_vals = __init_func()\n'
    for i in range(ecld__xhwk):
        hhz__sim += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(i, cvmb__vrjx[i], i))
        hhz__sim += '    incref(redvar_arr_{})\n'.format(i)
        hhz__sim += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(i, i)
    hhz__sim += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(i) for i in range(ecld__xhwk)]), ',' if ecld__xhwk == 1 else '')
    hhz__sim += '\n'
    for i in range(ecld__xhwk):
        hhz__sim += (
            """    recv_redvar_arr_{} = info_to_array(info_from_table(in_table, {}), data_redvar_dummy[{}])
"""
            .format(i, pnjp__qgoy[i], i))
        hhz__sim += '    incref(recv_redvar_arr_{})\n'.format(i)
    hhz__sim += '    recv_redvars = ({}{})\n'.format(','.join([
        'recv_redvar_arr_{}'.format(i) for i in range(ecld__xhwk)]), ',' if
        ecld__xhwk == 1 else '')
    hhz__sim += '\n'
    if ecld__xhwk:
        hhz__sim += '    for i in range(len(recv_redvar_arr_0)):\n'
        hhz__sim += '        w_ind = row_to_group[i]\n'
        hhz__sim += (
            '        __combine_redvars(redvars, recv_redvars, w_ind, i, pivot_arr=None)\n'
            )
    yrnlc__cynz = {}
    exec(hhz__sim, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__init_func':
        udf_func_struct.init_func, '__combine_redvars': udf_func_struct.
        combine_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, yrnlc__cynz)
    return yrnlc__cynz['bodo_gb_udf_combine{}'.format(label_suffix)]


def gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_data_typs_, label_suffix
    ):
    zdbxn__psdj = udf_func_struct.var_typs
    ecld__xhwk = len(zdbxn__psdj)
    kvbvu__zhurm = n_keys
    redvar_offsets = []
    ucui__xitzh = []
    out_data_typs = []
    for i, xml__xeq in enumerate(allfuncs):
        if xml__xeq.ftype != 'udf':
            kvbvu__zhurm += xml__xeq.ncols_post_shuffle
        else:
            ucui__xitzh.append(kvbvu__zhurm)
            redvar_offsets += list(range(kvbvu__zhurm + 1, kvbvu__zhurm + 1 +
                xml__xeq.n_redvars))
            kvbvu__zhurm += 1 + xml__xeq.n_redvars
            out_data_typs.append(out_data_typs_[i])
    assert len(redvar_offsets) == ecld__xhwk
    phv__wdx = len(out_data_typs)
    hhz__sim = 'def bodo_gb_udf_eval{}(table):\n'.format(label_suffix)
    hhz__sim += '    if is_null_pointer(table):\n'
    hhz__sim += '        return\n'
    hhz__sim += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in zdbxn__psdj]), 
        ',' if len(zdbxn__psdj) == 1 else '')
    hhz__sim += '    out_data_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t.dtype)) for t in
        out_data_typs]), ',' if len(out_data_typs) == 1 else '')
    for i in range(ecld__xhwk):
        hhz__sim += (
            """    redvar_arr_{} = info_to_array(info_from_table(table, {}), data_redvar_dummy[{}])
"""
            .format(i, redvar_offsets[i], i))
        hhz__sim += '    incref(redvar_arr_{})\n'.format(i)
    hhz__sim += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(i) for i in range(ecld__xhwk)]), ',' if ecld__xhwk == 1 else '')
    hhz__sim += '\n'
    for i in range(phv__wdx):
        hhz__sim += (
            """    data_out_{} = info_to_array(info_from_table(table, {}), out_data_dummy[{}])
"""
            .format(i, ucui__xitzh[i], i))
        hhz__sim += '    incref(data_out_{})\n'.format(i)
    hhz__sim += '    data_out = ({}{})\n'.format(','.join(['data_out_{}'.
        format(i) for i in range(phv__wdx)]), ',' if phv__wdx == 1 else '')
    hhz__sim += '\n'
    hhz__sim += '    for i in range(len(data_out_0)):\n'
    hhz__sim += '        __eval_res(redvars, data_out, i)\n'
    yrnlc__cynz = {}
    exec(hhz__sim, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__eval_res':
        udf_func_struct.eval_all_func, 'is_null_pointer': is_null_pointer,
        'dt64_dtype': np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, yrnlc__cynz)
    return yrnlc__cynz['bodo_gb_udf_eval{}'.format(label_suffix)]


def gen_general_udf_cb(udf_func_struct, allfuncs, n_keys, in_col_typs,
    out_col_typs, func_idx_to_in_col, label_suffix):
    kvbvu__zhurm = n_keys
    httq__zkh = []
    for i, xml__xeq in enumerate(allfuncs):
        if xml__xeq.ftype == 'gen_udf':
            httq__zkh.append(kvbvu__zhurm)
            kvbvu__zhurm += 1
        elif xml__xeq.ftype != 'udf':
            kvbvu__zhurm += xml__xeq.ncols_post_shuffle
        else:
            kvbvu__zhurm += xml__xeq.n_redvars + 1
    hhz__sim = (
        'def bodo_gb_apply_general_udfs{}(num_groups, in_table, out_table):\n'
        .format(label_suffix))
    hhz__sim += '    if num_groups == 0:\n'
    hhz__sim += '        return\n'
    for i, func in enumerate(udf_func_struct.general_udf_funcs):
        hhz__sim += '    # col {}\n'.format(i)
        hhz__sim += (
            '    out_col = info_to_array(info_from_table(out_table, {}), out_col_{}_typ)\n'
            .format(httq__zkh[i], i))
        hhz__sim += '    incref(out_col)\n'
        hhz__sim += '    for j in range(num_groups):\n'
        hhz__sim += (
            """        in_col = info_to_array(info_from_table(in_table, {}*num_groups + j), in_col_{}_typ)
"""
            .format(i, i))
        hhz__sim += '        incref(in_col)\n'
        hhz__sim += (
            '        out_col[j] = func_{}(pd.Series(in_col))  # func returns scalar\n'
            .format(i))
    ozlyq__ulq = {'pd': pd, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref}
    ggqci__vtss = 0
    for i, func in enumerate(allfuncs):
        if func.ftype != 'gen_udf':
            continue
        func = udf_func_struct.general_udf_funcs[ggqci__vtss]
        ozlyq__ulq['func_{}'.format(ggqci__vtss)] = func
        ozlyq__ulq['in_col_{}_typ'.format(ggqci__vtss)] = in_col_typs[
            func_idx_to_in_col[i]]
        ozlyq__ulq['out_col_{}_typ'.format(ggqci__vtss)] = out_col_typs[i]
        ggqci__vtss += 1
    yrnlc__cynz = {}
    exec(hhz__sim, ozlyq__ulq, yrnlc__cynz)
    xml__xeq = yrnlc__cynz['bodo_gb_apply_general_udfs{}'.format(label_suffix)]
    yezdk__afkhv = types.void(types.int64, types.voidptr, types.voidptr)
    return numba.cfunc(yezdk__afkhv, nopython=True)(xml__xeq)


def gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs, parallel,
    udf_func_struct):
    thnjj__hpq = agg_node.pivot_arr is not None
    if agg_node.same_index:
        assert agg_node.input_has_index
    if agg_node.pivot_values is None:
        esng__onjmp = 1
    else:
        esng__onjmp = len(agg_node.pivot_values)
    yns__lzdox = tuple('key_' + sanitize_varname(dcqr__hnz) for dcqr__hnz in
        agg_node.key_names)
    mob__muz = {dcqr__hnz: 'in_{}'.format(sanitize_varname(dcqr__hnz)) for
        dcqr__hnz in agg_node.gb_info_in.keys() if dcqr__hnz is not None}
    xwey__kpomd = {dcqr__hnz: ('out_' + sanitize_varname(dcqr__hnz)) for
        dcqr__hnz in agg_node.gb_info_out.keys()}
    n_keys = len(agg_node.key_names)
    abpu__kzr = ', '.join(yns__lzdox)
    aaiiq__yqwpq = ', '.join(mob__muz.values())
    if aaiiq__yqwpq != '':
        aaiiq__yqwpq = ', ' + aaiiq__yqwpq
    hhz__sim = 'def agg_top({}{}{}, pivot_arr):\n'.format(abpu__kzr,
        aaiiq__yqwpq, ', index_arg' if agg_node.input_has_index else '')
    if thnjj__hpq:
        hcs__oseg = []
        for ayj__efksk, gei__syyj in agg_node.gb_info_in.items():
            if ayj__efksk is not None:
                for func, yfc__wtvj in gei__syyj:
                    hcs__oseg.append(mob__muz[ayj__efksk])
    else:
        hcs__oseg = tuple(mob__muz[ayj__efksk] for ayj__efksk, yfc__wtvj in
            agg_node.gb_info_out.values() if ayj__efksk is not None)
    ipz__uzhhc = yns__lzdox + tuple(hcs__oseg)
    hhz__sim += '    info_list = [{}{}{}]\n'.format(', '.join(
        'array_to_info({})'.format(a) for a in ipz__uzhhc), 
        ', array_to_info(index_arg)' if agg_node.input_has_index else '', 
        ', array_to_info(pivot_arr)' if agg_node.is_crosstab else '')
    hhz__sim += '    table = arr_info_list_to_table(info_list)\n'
    for i, dcqr__hnz in enumerate(agg_node.gb_info_out.keys()):
        lyy__xgc = xwey__kpomd[dcqr__hnz] + '_dummy'
        pfkh__muqtr = out_col_typs[i]
        ayj__efksk, func = agg_node.gb_info_out[dcqr__hnz]
        if isinstance(func, pytypes.SimpleNamespace) and func.fname in ['min',
            'max', 'shift'] and isinstance(pfkh__muqtr, bodo.
            CategoricalArrayType):
            hhz__sim += '    {} = {}\n'.format(lyy__xgc, mob__muz[ayj__efksk])
        else:
            hhz__sim += '    {} = {}\n'.format(lyy__xgc, _gen_dummy_alloc(
                pfkh__muqtr, i, False))
    do_combine = parallel
    allfuncs = []
    lyao__bgxk = []
    func_idx_to_in_col = []
    jpxmk__ufp = []
    sjih__yyjhr = False
    xcy__gli = 1
    daqh__rob = -1
    xjz__tgsel = 0
    jlnl__vvpme = 0
    if not thnjj__hpq:
        amycx__ipifb = [func for yfc__wtvj, func in agg_node.gb_info_out.
            values()]
    else:
        amycx__ipifb = [func for func, yfc__wtvj in gei__syyj for gei__syyj in
            agg_node.gb_info_in.values()]
    for okmqz__duo, func in enumerate(amycx__ipifb):
        lyao__bgxk.append(len(allfuncs))
        if func.ftype in {'median', 'nunique'}:
            do_combine = False
        if func.ftype in list_cumulative:
            xjz__tgsel += 1
        if hasattr(func, 'skipdropna'):
            sjih__yyjhr = func.skipdropna
        if func.ftype == 'shift':
            xcy__gli = func.periods
            do_combine = False
        if func.ftype in {'transform'}:
            jlnl__vvpme = func.transform_func
            do_combine = False
        if func.ftype == 'head':
            daqh__rob = func.head_n
            do_combine = False
        allfuncs.append(func)
        func_idx_to_in_col.append(okmqz__duo)
        if func.ftype == 'udf':
            jpxmk__ufp.append(func.n_redvars)
        elif func.ftype == 'gen_udf':
            jpxmk__ufp.append(0)
            do_combine = False
    lyao__bgxk.append(len(allfuncs))
    if agg_node.is_crosstab:
        assert len(agg_node.gb_info_out
            ) == esng__onjmp, 'invalid number of groupby outputs for pivot'
    else:
        assert len(agg_node.gb_info_out) == len(allfuncs
            ) * esng__onjmp, 'invalid number of groupby outputs'
    if xjz__tgsel > 0:
        if xjz__tgsel != len(allfuncs):
            raise BodoError(
                f'{agg_node.func_name}(): Cannot mix cumulative operations with other aggregation functions'
                , loc=agg_node.loc)
        do_combine = False
    if udf_func_struct is not None:
        eqmse__sll = next_label()
        if udf_func_struct.regular_udfs:
            yezdk__afkhv = types.void(types.voidptr, types.voidptr, types.
                CPointer(types.int64))
            vzxnn__kbacw = numba.cfunc(yezdk__afkhv, nopython=True)(
                gen_update_cb(udf_func_struct, allfuncs, n_keys,
                in_col_typs, out_col_typs, do_combine, func_idx_to_in_col,
                eqmse__sll))
            tqs__movf = numba.cfunc(yezdk__afkhv, nopython=True)(gen_combine_cb
                (udf_func_struct, allfuncs, n_keys, out_col_typs, eqmse__sll))
            onuj__fvaio = numba.cfunc('void(voidptr)', nopython=True)(
                gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_col_typs,
                eqmse__sll))
            udf_func_struct.set_regular_cfuncs(vzxnn__kbacw, tqs__movf,
                onuj__fvaio)
            for vdz__jzh in udf_func_struct.regular_udf_cfuncs:
                gb_agg_cfunc[vdz__jzh.native_name] = vdz__jzh
                gb_agg_cfunc_addr[vdz__jzh.native_name] = vdz__jzh.address
        if udf_func_struct.general_udfs:
            sldw__lhty = gen_general_udf_cb(udf_func_struct, allfuncs,
                n_keys, in_col_typs, out_col_typs, func_idx_to_in_col,
                eqmse__sll)
            udf_func_struct.set_general_cfunc(sldw__lhty)
        pyn__mqj = []
        cak__wjgiy = 0
        i = 0
        for lyy__xgc, xml__xeq in zip(xwey__kpomd.values(), allfuncs):
            if xml__xeq.ftype in ('udf', 'gen_udf'):
                pyn__mqj.append(lyy__xgc + '_dummy')
                for jsy__zzu in range(cak__wjgiy, cak__wjgiy + jpxmk__ufp[i]):
                    pyn__mqj.append('data_redvar_dummy_' + str(jsy__zzu))
                cak__wjgiy += jpxmk__ufp[i]
                i += 1
        if udf_func_struct.regular_udfs:
            zdbxn__psdj = udf_func_struct.var_typs
            for i, t in enumerate(zdbxn__psdj):
                hhz__sim += ('    data_redvar_dummy_{} = np.empty(1, {})\n'
                    .format(i, _get_np_dtype(t)))
        hhz__sim += '    out_info_list_dummy = [{}]\n'.format(', '.join(
            'array_to_info({})'.format(a) for a in pyn__mqj))
        hhz__sim += (
            '    udf_table_dummy = arr_info_list_to_table(out_info_list_dummy)\n'
            )
        if udf_func_struct.regular_udfs:
            hhz__sim += "    add_agg_cfunc_sym(cpp_cb_update, '{}')\n".format(
                vzxnn__kbacw.native_name)
            hhz__sim += "    add_agg_cfunc_sym(cpp_cb_combine, '{}')\n".format(
                tqs__movf.native_name)
            hhz__sim += "    add_agg_cfunc_sym(cpp_cb_eval, '{}')\n".format(
                onuj__fvaio.native_name)
            hhz__sim += ("    cpp_cb_update_addr = get_agg_udf_addr('{}')\n"
                .format(vzxnn__kbacw.native_name))
            hhz__sim += ("    cpp_cb_combine_addr = get_agg_udf_addr('{}')\n"
                .format(tqs__movf.native_name))
            hhz__sim += ("    cpp_cb_eval_addr = get_agg_udf_addr('{}')\n".
                format(onuj__fvaio.native_name))
        else:
            hhz__sim += '    cpp_cb_update_addr = 0\n'
            hhz__sim += '    cpp_cb_combine_addr = 0\n'
            hhz__sim += '    cpp_cb_eval_addr = 0\n'
        if udf_func_struct.general_udfs:
            vdz__jzh = udf_func_struct.general_udf_cfunc
            gb_agg_cfunc[vdz__jzh.native_name] = vdz__jzh
            gb_agg_cfunc_addr[vdz__jzh.native_name] = vdz__jzh.address
            hhz__sim += "    add_agg_cfunc_sym(cpp_cb_general, '{}')\n".format(
                vdz__jzh.native_name)
            hhz__sim += ("    cpp_cb_general_addr = get_agg_udf_addr('{}')\n"
                .format(vdz__jzh.native_name))
        else:
            hhz__sim += '    cpp_cb_general_addr = 0\n'
    else:
        hhz__sim += (
            '    udf_table_dummy = arr_info_list_to_table([array_to_info(np.empty(1))])\n'
            )
        hhz__sim += '    cpp_cb_update_addr = 0\n'
        hhz__sim += '    cpp_cb_combine_addr = 0\n'
        hhz__sim += '    cpp_cb_eval_addr = 0\n'
        hhz__sim += '    cpp_cb_general_addr = 0\n'
    hhz__sim += '    ftypes = np.array([{}, 0], dtype=np.int32)\n'.format(', '
        .join([str(supported_agg_funcs.index(xml__xeq.ftype)) for xml__xeq in
        allfuncs] + ['0']))
    hhz__sim += '    func_offsets = np.array({}, dtype=np.int32)\n'.format(str
        (lyao__bgxk))
    if len(jpxmk__ufp) > 0:
        hhz__sim += '    udf_ncols = np.array({}, dtype=np.int32)\n'.format(str
            (jpxmk__ufp))
    else:
        hhz__sim += '    udf_ncols = np.array([0], np.int32)\n'
    if thnjj__hpq:
        hhz__sim += '    arr_type = coerce_to_array({})\n'.format(agg_node.
            pivot_values)
        hhz__sim += '    arr_info = array_to_info(arr_type)\n'
        hhz__sim += '    dispatch_table = arr_info_list_to_table([arr_info])\n'
        hhz__sim += '    pivot_info = array_to_info(pivot_arr)\n'
        hhz__sim += (
            '    dispatch_info = arr_info_list_to_table([pivot_info])\n')
        hhz__sim += (
            """    out_table = pivot_groupby_and_aggregate(table, {}, dispatch_table, dispatch_info, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel, agg_node.
            is_crosstab, sjih__yyjhr, agg_node.return_key, agg_node.same_index)
            )
        hhz__sim += '    delete_info_decref_array(pivot_info)\n'
        hhz__sim += '    delete_info_decref_array(arr_info)\n'
    else:
        hhz__sim += (
            """    out_table = groupby_and_aggregate(table, {}, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, cpp_cb_general_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel, sjih__yyjhr,
            xcy__gli, jlnl__vvpme, daqh__rob, agg_node.return_key, agg_node
            .same_index, agg_node.dropna))
    snaz__rvz = 0
    if agg_node.return_key:
        for i, rlefg__sfz in enumerate(yns__lzdox):
            hhz__sim += (
                '    {} = info_to_array(info_from_table(out_table, {}), {})\n'
                .format(rlefg__sfz, snaz__rvz, rlefg__sfz))
            snaz__rvz += 1
    for lyy__xgc in xwey__kpomd.values():
        hhz__sim += (
            '    {} = info_to_array(info_from_table(out_table, {}), {})\n'.
            format(lyy__xgc, snaz__rvz, lyy__xgc + '_dummy'))
        snaz__rvz += 1
    if agg_node.same_index:
        hhz__sim += (
            """    out_index_arg = info_to_array(info_from_table(out_table, {}), index_arg)
"""
            .format(snaz__rvz))
        snaz__rvz += 1
    hhz__sim += (
        f"    ev_clean = bodo.utils.tracing.Event('tables_clean_up', {parallel})\n"
        )
    hhz__sim += '    delete_table_decref_arrays(table)\n'
    hhz__sim += '    delete_table_decref_arrays(udf_table_dummy)\n'
    hhz__sim += '    delete_table(out_table)\n'
    hhz__sim += f'    ev_clean.finalize()\n'
    obbw__ilo = tuple(xwey__kpomd.values())
    if agg_node.return_key:
        obbw__ilo += tuple(yns__lzdox)
    hhz__sim += '    return ({},{})\n'.format(', '.join(obbw__ilo), 
        ' out_index_arg,' if agg_node.same_index else '')
    yrnlc__cynz = {}
    exec(hhz__sim, {}, yrnlc__cynz)
    uzmla__ccv = yrnlc__cynz['agg_top']
    return uzmla__ccv


def compile_to_optimized_ir(func, arg_typs, typingctx, targetctx):
    code = func.code if hasattr(func, 'code') else func.__code__
    closure = func.closure if hasattr(func, 'closure') else func.__closure__
    f_ir = get_ir_of_code(func.__globals__, code)
    replace_closures(f_ir, closure, code)
    for block in f_ir.blocks.values():
        for pmkj__vur in block.body:
            if is_call_assign(pmkj__vur) and find_callname(f_ir, pmkj__vur.
                value) == ('len', 'builtins') and pmkj__vur.value.args[0
                ].name == f_ir.arg_names[0]:
                zwit__quest = get_definition(f_ir, pmkj__vur.value.func)
                zwit__quest.name = 'dummy_agg_count'
                zwit__quest.value = dummy_agg_count
    mcc__mxlrc = get_name_var_table(f_ir.blocks)
    kzxcv__pjup = {}
    for name, yfc__wtvj in mcc__mxlrc.items():
        kzxcv__pjup[name] = mk_unique_var(name)
    replace_var_names(f_ir.blocks, kzxcv__pjup)
    f_ir._definitions = build_definitions(f_ir.blocks)
    assert f_ir.arg_count == 1, 'agg function should have one input'
    ndqnn__aprkw = numba.core.compiler.Flags()
    ndqnn__aprkw.nrt = True
    rmfd__uryf = bodo.transforms.untyped_pass.UntypedPass(f_ir, typingctx,
        arg_typs, {}, {}, ndqnn__aprkw)
    rmfd__uryf.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    typemap, uwl__hlm, calltypes, yfc__wtvj = (numba.core.typed_passes.
        type_inference_stage(typingctx, targetctx, f_ir, arg_typs, None))
    bxaeh__ryi = numba.core.cpu.ParallelOptions(True)
    targetctx = numba.core.cpu.CPUContext(typingctx)
    qtajl__mufx = namedtuple('DummyPipeline', ['typingctx', 'targetctx',
        'args', 'func_ir', 'typemap', 'return_type', 'calltypes',
        'type_annotation', 'locals', 'flags', 'pipeline'])
    zrfln__kavgs = namedtuple('TypeAnnotation', ['typemap', 'calltypes'])
    tjhc__lwafv = zrfln__kavgs(typemap, calltypes)
    pm = qtajl__mufx(typingctx, targetctx, None, f_ir, typemap, uwl__hlm,
        calltypes, tjhc__lwafv, {}, ndqnn__aprkw, None)
    ddr__pfqsy = (numba.core.compiler.DefaultPassBuilder.
        define_untyped_pipeline(pm))
    pm = qtajl__mufx(typingctx, targetctx, None, f_ir, typemap, uwl__hlm,
        calltypes, tjhc__lwafv, {}, ndqnn__aprkw, ddr__pfqsy)
    cosw__rtqr = numba.core.typed_passes.InlineOverloads()
    cosw__rtqr.run_pass(pm)
    ntxlx__geved = bodo.transforms.series_pass.SeriesPass(f_ir, typingctx,
        targetctx, typemap, calltypes, {}, False)
    ntxlx__geved.run()
    for block in f_ir.blocks.values():
        for pmkj__vur in block.body:
            if is_assign(pmkj__vur) and isinstance(pmkj__vur.value, (ir.Arg,
                ir.Var)) and isinstance(typemap[pmkj__vur.target.name],
                SeriesType):
                myrtd__ciz = typemap.pop(pmkj__vur.target.name)
                typemap[pmkj__vur.target.name] = myrtd__ciz.data
            if is_call_assign(pmkj__vur) and find_callname(f_ir, pmkj__vur.
                value) == ('get_series_data', 'bodo.hiframes.pd_series_ext'):
                f_ir._definitions[pmkj__vur.target.name].remove(pmkj__vur.value
                    )
                pmkj__vur.value = pmkj__vur.value.args[0]
                f_ir._definitions[pmkj__vur.target.name].append(pmkj__vur.value
                    )
            if is_call_assign(pmkj__vur) and find_callname(f_ir, pmkj__vur.
                value) == ('isna', 'bodo.libs.array_kernels'):
                f_ir._definitions[pmkj__vur.target.name].remove(pmkj__vur.value
                    )
                pmkj__vur.value = ir.Const(False, pmkj__vur.loc)
                f_ir._definitions[pmkj__vur.target.name].append(pmkj__vur.value
                    )
            if is_call_assign(pmkj__vur) and find_callname(f_ir, pmkj__vur.
                value) == ('setna', 'bodo.libs.array_kernels'):
                f_ir._definitions[pmkj__vur.target.name].remove(pmkj__vur.value
                    )
                pmkj__vur.value = ir.Const(False, pmkj__vur.loc)
                f_ir._definitions[pmkj__vur.target.name].append(pmkj__vur.value
                    )
    bodo.transforms.untyped_pass.remove_dead_branches(f_ir)
    tcnz__yhuy = numba.parfors.parfor.PreParforPass(f_ir, typemap,
        calltypes, typingctx, targetctx, bxaeh__ryi)
    tcnz__yhuy.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    ieck__bsbrn = numba.core.compiler.StateDict()
    ieck__bsbrn.func_ir = f_ir
    ieck__bsbrn.typemap = typemap
    ieck__bsbrn.calltypes = calltypes
    ieck__bsbrn.typingctx = typingctx
    ieck__bsbrn.targetctx = targetctx
    ieck__bsbrn.return_type = uwl__hlm
    numba.core.rewrites.rewrite_registry.apply('after-inference', ieck__bsbrn)
    rql__qhkmk = numba.parfors.parfor.ParforPass(f_ir, typemap, calltypes,
        uwl__hlm, typingctx, targetctx, bxaeh__ryi, ndqnn__aprkw, {})
    rql__qhkmk.run()
    remove_dels(f_ir.blocks)
    numba.parfors.parfor.maximize_fusion(f_ir, f_ir.blocks, typemap, False)
    return f_ir, pm


def replace_closures(f_ir, closure, code):
    if closure:
        closure = f_ir.get_definition(closure)
        if isinstance(closure, tuple):
            lbyq__cdbew = ctypes.pythonapi.PyCell_Get
            lbyq__cdbew.restype = ctypes.py_object
            lbyq__cdbew.argtypes = ctypes.py_object,
            bqn__knv = tuple(lbyq__cdbew(djn__decy) for djn__decy in closure)
        else:
            assert isinstance(closure, ir.Expr) and closure.op == 'build_tuple'
            bqn__knv = closure.items
        assert len(code.co_freevars) == len(bqn__knv)
        numba.core.inline_closurecall._replace_freevars(f_ir.blocks, bqn__knv)


class RegularUDFGenerator(object):

    def __init__(self, in_col_types, out_col_types, pivot_typ, pivot_values,
        is_crosstab, typingctx, targetctx):
        self.in_col_types = in_col_types
        self.out_col_types = out_col_types
        self.pivot_typ = pivot_typ
        self.pivot_values = pivot_values
        self.is_crosstab = is_crosstab
        self.typingctx = typingctx
        self.targetctx = targetctx
        self.all_reduce_vars = []
        self.all_vartypes = []
        self.all_init_nodes = []
        self.all_eval_funcs = []
        self.all_update_funcs = []
        self.all_combine_funcs = []
        self.curr_offset = 0
        self.redvar_offsets = [0]

    def add_udf(self, in_col_typ, func):
        rmmd__isiw = SeriesType(in_col_typ.dtype, in_col_typ, None, string_type
            )
        f_ir, pm = compile_to_optimized_ir(func, (rmmd__isiw,), self.
            typingctx, self.targetctx)
        f_ir._definitions = build_definitions(f_ir.blocks)
        assert len(f_ir.blocks
            ) == 1 and 0 in f_ir.blocks, 'only simple functions with one block supported for aggregation'
        block = f_ir.blocks[0]
        nld__mjxq, arr_var = _rm_arg_agg_block(block, pm.typemap)
        omhcc__itzhg = -1
        for i, pmkj__vur in enumerate(nld__mjxq):
            if isinstance(pmkj__vur, numba.parfors.parfor.Parfor):
                assert omhcc__itzhg == -1, 'only one parfor for aggregation function'
                omhcc__itzhg = i
        parfor = None
        if omhcc__itzhg != -1:
            parfor = nld__mjxq[omhcc__itzhg]
            remove_dels(parfor.loop_body)
            remove_dels({(0): parfor.init_block})
        init_nodes = []
        if parfor:
            init_nodes = nld__mjxq[:omhcc__itzhg] + parfor.init_block.body
        eval_nodes = nld__mjxq[omhcc__itzhg + 1:]
        redvars = []
        var_to_redvar = {}
        if parfor:
            redvars, var_to_redvar = get_parfor_reductions(parfor, parfor.
                params, pm.calltypes)
        func.ncols_pre_shuffle = len(redvars)
        func.ncols_post_shuffle = len(redvars) + 1
        func.n_redvars = len(redvars)
        reduce_vars = [0] * len(redvars)
        for pmkj__vur in init_nodes:
            if is_assign(pmkj__vur) and pmkj__vur.target.name in redvars:
                ind = redvars.index(pmkj__vur.target.name)
                reduce_vars[ind] = pmkj__vur.target
        var_types = [pm.typemap[v] for v in redvars]
        nlscp__ljk = gen_combine_func(f_ir, parfor, redvars, var_to_redvar,
            var_types, arr_var, pm, self.typingctx, self.targetctx)
        init_nodes = _mv_read_only_init_vars(init_nodes, parfor, eval_nodes)
        dngan__dwb = gen_update_func(parfor, redvars, var_to_redvar,
            var_types, arr_var, in_col_typ, pm, self.typingctx, self.targetctx)
        veyu__xdxei = gen_eval_func(f_ir, eval_nodes, reduce_vars,
            var_types, pm, self.typingctx, self.targetctx)
        self.all_reduce_vars += reduce_vars
        self.all_vartypes += var_types
        self.all_init_nodes += init_nodes
        self.all_eval_funcs.append(veyu__xdxei)
        self.all_update_funcs.append(dngan__dwb)
        self.all_combine_funcs.append(nlscp__ljk)
        self.curr_offset += len(redvars)
        self.redvar_offsets.append(self.curr_offset)

    def gen_all_func(self):
        if len(self.all_update_funcs) == 0:
            return None
        self.all_vartypes = self.all_vartypes * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_vartypes
        self.all_reduce_vars = self.all_reduce_vars * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_reduce_vars
        zlzv__bhm = gen_init_func(self.all_init_nodes, self.all_reduce_vars,
            self.all_vartypes, self.typingctx, self.targetctx)
        hoe__cnb = gen_all_update_func(self.all_update_funcs, self.
            all_vartypes, self.in_col_types, self.redvar_offsets, self.
            typingctx, self.targetctx, self.pivot_typ, self.pivot_values,
            self.is_crosstab)
        tpxx__kes = gen_all_combine_func(self.all_combine_funcs, self.
            all_vartypes, self.redvar_offsets, self.typingctx, self.
            targetctx, self.pivot_typ, self.pivot_values)
        rgju__lkx = gen_all_eval_func(self.all_eval_funcs, self.
            all_vartypes, self.redvar_offsets, self.out_col_types, self.
            typingctx, self.targetctx, self.pivot_values)
        return self.all_vartypes, zlzv__bhm, hoe__cnb, tpxx__kes, rgju__lkx


class GeneralUDFGenerator(object):

    def __init__(self):
        self.funcs = []

    def add_udf(self, func):
        self.funcs.append(bodo.jit(distributed=False)(func))
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        func.n_redvars = 0

    def gen_all_func(self):
        if len(self.funcs) > 0:
            return self.funcs
        else:
            return None


def get_udf_func_struct(agg_func, input_has_index, in_col_types,
    out_col_types, typingctx, targetctx, pivot_typ, pivot_values, is_crosstab):
    if is_crosstab and len(in_col_types) == 0:
        in_col_types = [types.Array(types.intp, 1, 'C')]
    eye__icg = []
    for t, xml__xeq in zip(in_col_types, agg_func):
        eye__icg.append((t, xml__xeq))
    tij__nmf = RegularUDFGenerator(in_col_types, out_col_types, pivot_typ,
        pivot_values, is_crosstab, typingctx, targetctx)
    ypshv__rcwr = GeneralUDFGenerator()
    for in_col_typ, func in eye__icg:
        if func.ftype not in ('udf', 'gen_udf'):
            continue
        try:
            tij__nmf.add_udf(in_col_typ, func)
        except:
            ypshv__rcwr.add_udf(func)
            func.ftype = 'gen_udf'
    regular_udf_funcs = tij__nmf.gen_all_func()
    general_udf_funcs = ypshv__rcwr.gen_all_func()
    if regular_udf_funcs is not None or general_udf_funcs is not None:
        return AggUDFStruct(regular_udf_funcs, general_udf_funcs)
    else:
        return None


def _mv_read_only_init_vars(init_nodes, parfor, eval_nodes):
    if not parfor:
        return init_nodes
    kbjac__kzpb = compute_use_defs(parfor.loop_body)
    ykfo__xlie = set()
    for qnuh__jody in kbjac__kzpb.usemap.values():
        ykfo__xlie |= qnuh__jody
    vtkc__xofgx = set()
    for qnuh__jody in kbjac__kzpb.defmap.values():
        vtkc__xofgx |= qnuh__jody
    eot__byoh = ir.Block(ir.Scope(None, parfor.loc), parfor.loc)
    eot__byoh.body = eval_nodes
    ycl__vcmqi = compute_use_defs({(0): eot__byoh})
    fmmaf__amozy = ycl__vcmqi.usemap[0]
    jtve__xvgdt = set()
    nwfn__kwz = []
    yuu__wsv = []
    for pmkj__vur in reversed(init_nodes):
        mhukt__ldv = {v.name for v in pmkj__vur.list_vars()}
        if is_assign(pmkj__vur):
            v = pmkj__vur.target.name
            mhukt__ldv.remove(v)
            if (v in ykfo__xlie and v not in jtve__xvgdt and v not in
                fmmaf__amozy and v not in vtkc__xofgx):
                yuu__wsv.append(pmkj__vur)
                ykfo__xlie |= mhukt__ldv
                vtkc__xofgx.add(v)
                continue
        jtve__xvgdt |= mhukt__ldv
        nwfn__kwz.append(pmkj__vur)
    yuu__wsv.reverse()
    nwfn__kwz.reverse()
    lmsb__smjh = min(parfor.loop_body.keys())
    ktf__gbtxs = parfor.loop_body[lmsb__smjh]
    ktf__gbtxs.body = yuu__wsv + ktf__gbtxs.body
    return nwfn__kwz


def gen_init_func(init_nodes, reduce_vars, var_types, typingctx, targetctx):
    idljb__yuedg = (numba.parfors.parfor.max_checker, numba.parfors.parfor.
        min_checker, numba.parfors.parfor.argmax_checker, numba.parfors.
        parfor.argmin_checker)
    evfp__vucmw = set()
    yzxp__hlavq = []
    for pmkj__vur in init_nodes:
        if is_assign(pmkj__vur) and isinstance(pmkj__vur.value, ir.Global
            ) and isinstance(pmkj__vur.value.value, pytypes.FunctionType
            ) and pmkj__vur.value.value in idljb__yuedg:
            evfp__vucmw.add(pmkj__vur.target.name)
        elif is_call_assign(pmkj__vur
            ) and pmkj__vur.value.func.name in evfp__vucmw:
            pass
        else:
            yzxp__hlavq.append(pmkj__vur)
    init_nodes = yzxp__hlavq
    dsr__kjuah = types.Tuple(var_types)
    yrik__ihuxx = lambda : None
    f_ir = compile_to_numba_ir(yrik__ihuxx, {})
    block = list(f_ir.blocks.values())[0]
    loc = block.loc
    sth__esi = ir.Var(block.scope, mk_unique_var('init_tup'), loc)
    bqjrp__wbgsk = ir.Assign(ir.Expr.build_tuple(reduce_vars, loc),
        sth__esi, loc)
    block.body = block.body[-2:]
    block.body = init_nodes + [bqjrp__wbgsk] + block.body
    block.body[-2].value.value = sth__esi
    jwssc__avar = compiler.compile_ir(typingctx, targetctx, f_ir, (),
        dsr__kjuah, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    kghcx__prp = numba.core.target_extension.dispatcher_registry[cpu_target](
        yrik__ihuxx)
    kghcx__prp.add_overload(jwssc__avar)
    return kghcx__prp


def gen_all_update_func(update_funcs, reduce_var_types, in_col_types,
    redvar_offsets, typingctx, targetctx, pivot_typ, pivot_values, is_crosstab
    ):
    qpvfa__axyjj = len(update_funcs)
    jkok__itomn = len(in_col_types)
    if pivot_values is not None:
        assert jkok__itomn == 1
    hhz__sim = 'def update_all_f(redvar_arrs, data_in, w_ind, i, pivot_arr):\n'
    if pivot_values is not None:
        isyhd__upojm = redvar_offsets[jkok__itomn]
        hhz__sim += '  pv = pivot_arr[i]\n'
        for jsy__zzu, hrpt__nnmmj in enumerate(pivot_values):
            ihanb__dcaec = 'el' if jsy__zzu != 0 else ''
            hhz__sim += "  {}if pv == '{}':\n".format(ihanb__dcaec, hrpt__nnmmj
                )
            mqu__rysx = isyhd__upojm * jsy__zzu
            hbxky__yqd = ', '.join(['redvar_arrs[{}][w_ind]'.format(i) for
                i in range(mqu__rysx + redvar_offsets[0], mqu__rysx +
                redvar_offsets[1])])
            hlf__gzo = 'data_in[0][i]'
            if is_crosstab:
                hlf__gzo = '0'
            hhz__sim += '    {} = update_vars_0({}, {})\n'.format(hbxky__yqd,
                hbxky__yqd, hlf__gzo)
    else:
        for jsy__zzu in range(qpvfa__axyjj):
            hbxky__yqd = ', '.join(['redvar_arrs[{}][w_ind]'.format(i) for
                i in range(redvar_offsets[jsy__zzu], redvar_offsets[
                jsy__zzu + 1])])
            if hbxky__yqd:
                hhz__sim += ('  {} = update_vars_{}({},  data_in[{}][i])\n'
                    .format(hbxky__yqd, jsy__zzu, hbxky__yqd, 0 if 
                    jkok__itomn == 1 else jsy__zzu))
    hhz__sim += '  return\n'
    ozlyq__ulq = {}
    for i, xml__xeq in enumerate(update_funcs):
        ozlyq__ulq['update_vars_{}'.format(i)] = xml__xeq
    yrnlc__cynz = {}
    exec(hhz__sim, ozlyq__ulq, yrnlc__cynz)
    ixco__dmduf = yrnlc__cynz['update_all_f']
    return numba.njit(no_cpython_wrapper=True)(ixco__dmduf)


def gen_all_combine_func(combine_funcs, reduce_var_types, redvar_offsets,
    typingctx, targetctx, pivot_typ, pivot_values):
    rdya__sbo = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types])
    arg_typs = rdya__sbo, rdya__sbo, types.intp, types.intp, pivot_typ
    lcyz__wwbxp = len(redvar_offsets) - 1
    isyhd__upojm = redvar_offsets[lcyz__wwbxp]
    hhz__sim = (
        'def combine_all_f(redvar_arrs, recv_arrs, w_ind, i, pivot_arr):\n')
    if pivot_values is not None:
        assert lcyz__wwbxp == 1
        for gjz__guoyd in range(len(pivot_values)):
            mqu__rysx = isyhd__upojm * gjz__guoyd
            hbxky__yqd = ', '.join(['redvar_arrs[{}][w_ind]'.format(i) for
                i in range(mqu__rysx + redvar_offsets[0], mqu__rysx +
                redvar_offsets[1])])
            jdv__bczh = ', '.join(['recv_arrs[{}][i]'.format(i) for i in
                range(mqu__rysx + redvar_offsets[0], mqu__rysx +
                redvar_offsets[1])])
            hhz__sim += '  {} = combine_vars_0({}, {})\n'.format(hbxky__yqd,
                hbxky__yqd, jdv__bczh)
    else:
        for jsy__zzu in range(lcyz__wwbxp):
            hbxky__yqd = ', '.join(['redvar_arrs[{}][w_ind]'.format(i) for
                i in range(redvar_offsets[jsy__zzu], redvar_offsets[
                jsy__zzu + 1])])
            jdv__bczh = ', '.join(['recv_arrs[{}][i]'.format(i) for i in
                range(redvar_offsets[jsy__zzu], redvar_offsets[jsy__zzu + 1])])
            if jdv__bczh:
                hhz__sim += '  {} = combine_vars_{}({}, {})\n'.format(
                    hbxky__yqd, jsy__zzu, hbxky__yqd, jdv__bczh)
    hhz__sim += '  return\n'
    ozlyq__ulq = {}
    for i, xml__xeq in enumerate(combine_funcs):
        ozlyq__ulq['combine_vars_{}'.format(i)] = xml__xeq
    yrnlc__cynz = {}
    exec(hhz__sim, ozlyq__ulq, yrnlc__cynz)
    trmtk__ogn = yrnlc__cynz['combine_all_f']
    f_ir = compile_to_numba_ir(trmtk__ogn, ozlyq__ulq)
    tpxx__kes = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        types.none, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    kghcx__prp = numba.core.target_extension.dispatcher_registry[cpu_target](
        trmtk__ogn)
    kghcx__prp.add_overload(tpxx__kes)
    return kghcx__prp


def gen_all_eval_func(eval_funcs, reduce_var_types, redvar_offsets,
    out_col_typs, typingctx, targetctx, pivot_values):
    rdya__sbo = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types])
    out_col_typs = types.Tuple(out_col_typs)
    lcyz__wwbxp = len(redvar_offsets) - 1
    isyhd__upojm = redvar_offsets[lcyz__wwbxp]
    hhz__sim = 'def eval_all_f(redvar_arrs, out_arrs, j):\n'
    if pivot_values is not None:
        assert lcyz__wwbxp == 1
        for jsy__zzu in range(len(pivot_values)):
            mqu__rysx = isyhd__upojm * jsy__zzu
            hbxky__yqd = ', '.join(['redvar_arrs[{}][j]'.format(i) for i in
                range(mqu__rysx + redvar_offsets[0], mqu__rysx +
                redvar_offsets[1])])
            hhz__sim += '  out_arrs[{}][j] = eval_vars_0({})\n'.format(jsy__zzu
                , hbxky__yqd)
    else:
        for jsy__zzu in range(lcyz__wwbxp):
            hbxky__yqd = ', '.join(['redvar_arrs[{}][j]'.format(i) for i in
                range(redvar_offsets[jsy__zzu], redvar_offsets[jsy__zzu + 1])])
            hhz__sim += '  out_arrs[{}][j] = eval_vars_{}({})\n'.format(
                jsy__zzu, jsy__zzu, hbxky__yqd)
    hhz__sim += '  return\n'
    ozlyq__ulq = {}
    for i, xml__xeq in enumerate(eval_funcs):
        ozlyq__ulq['eval_vars_{}'.format(i)] = xml__xeq
    yrnlc__cynz = {}
    exec(hhz__sim, ozlyq__ulq, yrnlc__cynz)
    zxza__otam = yrnlc__cynz['eval_all_f']
    return numba.njit(no_cpython_wrapper=True)(zxza__otam)


def gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types, pm, typingctx,
    targetctx):
    pkdij__oxfmu = len(var_types)
    kxow__juhf = [f'in{i}' for i in range(pkdij__oxfmu)]
    dsr__kjuah = types.unliteral(pm.typemap[eval_nodes[-1].value.name])
    tymyl__ahd = dsr__kjuah(0)
    hhz__sim = 'def agg_eval({}):\n return _zero\n'.format(', '.join(
        kxow__juhf))
    yrnlc__cynz = {}
    exec(hhz__sim, {'_zero': tymyl__ahd}, yrnlc__cynz)
    yfz__oqqm = yrnlc__cynz['agg_eval']
    arg_typs = tuple(var_types)
    f_ir = compile_to_numba_ir(yfz__oqqm, {'numba': numba, 'bodo': bodo,
        'np': np, '_zero': tymyl__ahd}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.
        calltypes)
    block = list(f_ir.blocks.values())[0]
    mptrd__kbqr = []
    for i, v in enumerate(reduce_vars):
        mptrd__kbqr.append(ir.Assign(block.body[i].target, v, v.loc))
        for hyk__sdw in v.versioned_names:
            mptrd__kbqr.append(ir.Assign(v, ir.Var(v.scope, hyk__sdw, v.loc
                ), v.loc))
    block.body = block.body[:pkdij__oxfmu] + mptrd__kbqr + eval_nodes
    veyu__xdxei = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        dsr__kjuah, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    kghcx__prp = numba.core.target_extension.dispatcher_registry[cpu_target](
        yfz__oqqm)
    kghcx__prp.add_overload(veyu__xdxei)
    return kghcx__prp


def gen_combine_func(f_ir, parfor, redvars, var_to_redvar, var_types,
    arr_var, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda : ())
    pkdij__oxfmu = len(redvars)
    qgw__xctp = [f'v{i}' for i in range(pkdij__oxfmu)]
    kxow__juhf = [f'in{i}' for i in range(pkdij__oxfmu)]
    hhz__sim = 'def agg_combine({}):\n'.format(', '.join(qgw__xctp +
        kxow__juhf))
    xyk__oai = wrap_parfor_blocks(parfor)
    epyrn__glg = find_topo_order(xyk__oai)
    epyrn__glg = epyrn__glg[1:]
    unwrap_parfor_blocks(parfor)
    mxcp__ijqj = {}
    pck__soxh = []
    for qszyg__vjz in epyrn__glg:
        qvybp__tyi = parfor.loop_body[qszyg__vjz]
        for pmkj__vur in qvybp__tyi.body:
            if is_call_assign(pmkj__vur) and guard(find_callname, f_ir,
                pmkj__vur.value) == ('__special_combine', 'bodo.ir.aggregate'):
                args = pmkj__vur.value.args
                pxol__lasti = []
                wdy__rlpc = []
                for v in args[:-1]:
                    ind = redvars.index(v.name)
                    pck__soxh.append(ind)
                    pxol__lasti.append('v{}'.format(ind))
                    wdy__rlpc.append('in{}'.format(ind))
                naqee__paub = '__special_combine__{}'.format(len(mxcp__ijqj))
                hhz__sim += '    ({},) = {}({})\n'.format(', '.join(
                    pxol__lasti), naqee__paub, ', '.join(pxol__lasti +
                    wdy__rlpc))
                bnau__tjhvq = ir.Expr.call(args[-1], [], (), qvybp__tyi.loc)
                kze__afqhs = guard(find_callname, f_ir, bnau__tjhvq)
                assert kze__afqhs == ('_var_combine', 'bodo.ir.aggregate')
                kze__afqhs = bodo.ir.aggregate._var_combine
                mxcp__ijqj[naqee__paub] = kze__afqhs
            if is_assign(pmkj__vur) and pmkj__vur.target.name in redvars:
                rgvmj__idsd = pmkj__vur.target.name
                ind = redvars.index(rgvmj__idsd)
                if ind in pck__soxh:
                    continue
                if len(f_ir._definitions[rgvmj__idsd]) == 2:
                    var_def = f_ir._definitions[rgvmj__idsd][0]
                    hhz__sim += _match_reduce_def(var_def, f_ir, ind)
                    var_def = f_ir._definitions[rgvmj__idsd][1]
                    hhz__sim += _match_reduce_def(var_def, f_ir, ind)
    hhz__sim += '    return {}'.format(', '.join(['v{}'.format(i) for i in
        range(pkdij__oxfmu)]))
    yrnlc__cynz = {}
    exec(hhz__sim, {}, yrnlc__cynz)
    hxe__mps = yrnlc__cynz['agg_combine']
    arg_typs = tuple(2 * var_types)
    ozlyq__ulq = {'numba': numba, 'bodo': bodo, 'np': np}
    ozlyq__ulq.update(mxcp__ijqj)
    f_ir = compile_to_numba_ir(hxe__mps, ozlyq__ulq, typingctx=typingctx,
        targetctx=targetctx, arg_typs=arg_typs, typemap=pm.typemap,
        calltypes=pm.calltypes)
    block = list(f_ir.blocks.values())[0]
    dsr__kjuah = pm.typemap[block.body[-1].value.name]
    nlscp__ljk = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        dsr__kjuah, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    kghcx__prp = numba.core.target_extension.dispatcher_registry[cpu_target](
        hxe__mps)
    kghcx__prp.add_overload(nlscp__ljk)
    return kghcx__prp


def _match_reduce_def(var_def, f_ir, ind):
    hhz__sim = ''
    while isinstance(var_def, ir.Var):
        var_def = guard(get_definition, f_ir, var_def)
    if isinstance(var_def, ir.Expr
        ) and var_def.op == 'inplace_binop' and var_def.fn in ('+=',
        operator.iadd):
        hhz__sim = '    v{} += in{}\n'.format(ind, ind)
    if isinstance(var_def, ir.Expr) and var_def.op == 'call':
        aahr__ajat = guard(find_callname, f_ir, var_def)
        if aahr__ajat == ('min', 'builtins'):
            hhz__sim = '    v{} = min(v{}, in{})\n'.format(ind, ind, ind)
        if aahr__ajat == ('max', 'builtins'):
            hhz__sim = '    v{} = max(v{}, in{})\n'.format(ind, ind, ind)
    return hhz__sim


def gen_update_func(parfor, redvars, var_to_redvar, var_types, arr_var,
    in_col_typ, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda A: ())
    pkdij__oxfmu = len(redvars)
    bzl__ypuia = 1
    jjc__ppp = []
    for i in range(bzl__ypuia):
        oxx__dzeg = ir.Var(arr_var.scope, f'$input{i}', arr_var.loc)
        jjc__ppp.append(oxx__dzeg)
    nyb__qba = parfor.loop_nests[0].index_variable
    snq__mfjox = [0] * pkdij__oxfmu
    for qvybp__tyi in parfor.loop_body.values():
        lgmtt__pga = []
        for pmkj__vur in qvybp__tyi.body:
            if is_var_assign(pmkj__vur
                ) and pmkj__vur.value.name == nyb__qba.name:
                continue
            if is_getitem(pmkj__vur
                ) and pmkj__vur.value.value.name == arr_var.name:
                pmkj__vur.value = jjc__ppp[0]
            if is_call_assign(pmkj__vur) and guard(find_callname, pm.
                func_ir, pmkj__vur.value) == ('isna', 'bodo.libs.array_kernels'
                ) and pmkj__vur.value.args[0].name == arr_var.name:
                pmkj__vur.value = ir.Const(False, pmkj__vur.target.loc)
            if is_assign(pmkj__vur) and pmkj__vur.target.name in redvars:
                ind = redvars.index(pmkj__vur.target.name)
                snq__mfjox[ind] = pmkj__vur.target
            lgmtt__pga.append(pmkj__vur)
        qvybp__tyi.body = lgmtt__pga
    qgw__xctp = ['v{}'.format(i) for i in range(pkdij__oxfmu)]
    kxow__juhf = ['in{}'.format(i) for i in range(bzl__ypuia)]
    hhz__sim = 'def agg_update({}):\n'.format(', '.join(qgw__xctp + kxow__juhf)
        )
    hhz__sim += '    __update_redvars()\n'
    hhz__sim += '    return {}'.format(', '.join(['v{}'.format(i) for i in
        range(pkdij__oxfmu)]))
    yrnlc__cynz = {}
    exec(hhz__sim, {}, yrnlc__cynz)
    emuob__kmvc = yrnlc__cynz['agg_update']
    arg_typs = tuple(var_types + [in_col_typ.dtype] * bzl__ypuia)
    f_ir = compile_to_numba_ir(emuob__kmvc, {'__update_redvars':
        __update_redvars}, typingctx=typingctx, targetctx=targetctx,
        arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.calltypes)
    f_ir._definitions = build_definitions(f_ir.blocks)
    tkh__wwun = f_ir.blocks.popitem()[1].body
    dsr__kjuah = pm.typemap[tkh__wwun[-1].value.name]
    xyk__oai = wrap_parfor_blocks(parfor)
    epyrn__glg = find_topo_order(xyk__oai)
    epyrn__glg = epyrn__glg[1:]
    unwrap_parfor_blocks(parfor)
    f_ir.blocks = parfor.loop_body
    ktf__gbtxs = f_ir.blocks[epyrn__glg[0]]
    vsd__gldp = f_ir.blocks[epyrn__glg[-1]]
    izcbk__mpi = tkh__wwun[:pkdij__oxfmu + bzl__ypuia]
    if pkdij__oxfmu > 1:
        xng__fup = tkh__wwun[-3:]
        assert is_assign(xng__fup[0]) and isinstance(xng__fup[0].value, ir.Expr
            ) and xng__fup[0].value.op == 'build_tuple'
    else:
        xng__fup = tkh__wwun[-2:]
    for i in range(pkdij__oxfmu):
        kpy__rlg = tkh__wwun[i].target
        igw__apth = ir.Assign(kpy__rlg, snq__mfjox[i], kpy__rlg.loc)
        izcbk__mpi.append(igw__apth)
    for i in range(pkdij__oxfmu, pkdij__oxfmu + bzl__ypuia):
        kpy__rlg = tkh__wwun[i].target
        igw__apth = ir.Assign(kpy__rlg, jjc__ppp[i - pkdij__oxfmu],
            kpy__rlg.loc)
        izcbk__mpi.append(igw__apth)
    ktf__gbtxs.body = izcbk__mpi + ktf__gbtxs.body
    jubfr__hau = []
    for i in range(pkdij__oxfmu):
        kpy__rlg = tkh__wwun[i].target
        igw__apth = ir.Assign(snq__mfjox[i], kpy__rlg, kpy__rlg.loc)
        jubfr__hau.append(igw__apth)
    vsd__gldp.body += jubfr__hau + xng__fup
    lglbm__vyn = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        dsr__kjuah, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    kghcx__prp = numba.core.target_extension.dispatcher_registry[cpu_target](
        emuob__kmvc)
    kghcx__prp.add_overload(lglbm__vyn)
    return kghcx__prp


def _rm_arg_agg_block(block, typemap):
    nld__mjxq = []
    arr_var = None
    for i, pmkj__vur in enumerate(block.body):
        if is_assign(pmkj__vur) and isinstance(pmkj__vur.value, ir.Arg):
            arr_var = pmkj__vur.target
            oocha__ktz = typemap[arr_var.name]
            if not isinstance(oocha__ktz, types.ArrayCompatible):
                nld__mjxq += block.body[i + 1:]
                break
            qow__mus = block.body[i + 1]
            assert is_assign(qow__mus) and isinstance(qow__mus.value, ir.Expr
                ) and qow__mus.value.op == 'getattr' and qow__mus.value.attr == 'shape' and qow__mus.value.value.name == arr_var.name
            sdb__gptqg = qow__mus.target
            lmj__ars = block.body[i + 2]
            assert is_assign(lmj__ars) and isinstance(lmj__ars.value, ir.Expr
                ) and lmj__ars.value.op == 'static_getitem' and lmj__ars.value.value.name == sdb__gptqg.name
            nld__mjxq += block.body[i + 3:]
            break
        nld__mjxq.append(pmkj__vur)
    return nld__mjxq, arr_var


def get_parfor_reductions(parfor, parfor_params, calltypes, reduce_varnames
    =None, param_uses=None, var_to_param=None):
    if reduce_varnames is None:
        reduce_varnames = []
    if param_uses is None:
        param_uses = defaultdict(list)
    if var_to_param is None:
        var_to_param = {}
    xyk__oai = wrap_parfor_blocks(parfor)
    epyrn__glg = find_topo_order(xyk__oai)
    epyrn__glg = epyrn__glg[1:]
    unwrap_parfor_blocks(parfor)
    for qszyg__vjz in reversed(epyrn__glg):
        for pmkj__vur in reversed(parfor.loop_body[qszyg__vjz].body):
            if isinstance(pmkj__vur, ir.Assign) and (pmkj__vur.target.name in
                parfor_params or pmkj__vur.target.name in var_to_param):
                udt__nvgwu = pmkj__vur.target.name
                rhs = pmkj__vur.value
                aiu__oxrg = (udt__nvgwu if udt__nvgwu in parfor_params else
                    var_to_param[udt__nvgwu])
                dfec__raxj = []
                if isinstance(rhs, ir.Var):
                    dfec__raxj = [rhs.name]
                elif isinstance(rhs, ir.Expr):
                    dfec__raxj = [v.name for v in pmkj__vur.value.list_vars()]
                param_uses[aiu__oxrg].extend(dfec__raxj)
                for v in dfec__raxj:
                    var_to_param[v] = aiu__oxrg
            if isinstance(pmkj__vur, Parfor):
                get_parfor_reductions(pmkj__vur, parfor_params, calltypes,
                    reduce_varnames, param_uses, var_to_param)
    for xeuqp__pfgh, dfec__raxj in param_uses.items():
        if xeuqp__pfgh in dfec__raxj and xeuqp__pfgh not in reduce_varnames:
            reduce_varnames.append(xeuqp__pfgh)
    return reduce_varnames, var_to_param


@numba.extending.register_jitable
def dummy_agg_count(A):
    return len(A)
