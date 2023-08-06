"""
Helper functions for transformations.
"""
import itertools
import math
import operator
import types as pytypes
from collections import namedtuple
import numba
import numpy as np
import pandas as pd
from numba.core import ir, ir_utils, types
from numba.core.ir_utils import GuardException, build_definitions, compile_to_numba_ir, compute_cfg_from_blocks, find_callname, find_const, get_definition, guard, is_setitem, mk_unique_var, replace_arg_nodes, require
from numba.core.registry import CPUDispatcher
from numba.core.typing.templates import fold_arguments
import bodo
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.struct_arr_ext import StructArrayType, StructType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoConstUpdatedError, BodoError, can_literalize_type, get_literal_value, get_overload_const_bool, get_overload_const_list, is_literal_type, is_overload_constant_bool
from bodo.utils.utils import is_array_typ, is_assign, is_call, is_expr
ReplaceFunc = namedtuple('ReplaceFunc', ['func', 'arg_types', 'args',
    'glbls', 'inline_bodo_calls', 'run_full_pipeline', 'pre_nodes'])
bodo_types_with_params = {'ArrayItemArrayType', 'CSRMatrixType',
    'CategoricalArrayType', 'CategoricalIndexType', 'DataFrameType',
    'DatetimeIndexType', 'Decimal128Type', 'DecimalArrayType',
    'IntegerArrayType', 'IntervalArrayType', 'IntervalIndexType', 'List',
    'MapArrayType', 'NumericIndexType', 'PDCategoricalDtype',
    'PeriodIndexType', 'RangeIndexType', 'SeriesType', 'StringIndexType',
    'BinaryIndexType', 'StructArrayType', 'TimedeltaIndexType',
    'TupleArrayType'}
container_update_method_names = ('clear', 'pop', 'popitem', 'update', 'add',
    'difference_update', 'discard', 'intersection_update', 'remove',
    'symmetric_difference_update', 'append', 'extend', 'insert', 'reverse',
    'sort')
no_side_effect_call_tuples = {(int,), (list,), (set,), (dict,), (min,), (
    max,), (abs,), (len,), (bool,), (str,), ('ceil', math), ('init_series',
    'pd_series_ext', 'hiframes', bodo), ('get_series_data', 'pd_series_ext',
    'hiframes', bodo), ('get_series_index', 'pd_series_ext', 'hiframes',
    bodo), ('get_series_name', 'pd_series_ext', 'hiframes', bodo), (
    'get_index_data', 'pd_index_ext', 'hiframes', bodo), ('get_index_name',
    'pd_index_ext', 'hiframes', bodo), ('init_binary_str_index',
    'pd_index_ext', 'hiframes', bodo), ('init_numeric_index',
    'pd_index_ext', 'hiframes', bodo), ('init_categorical_index',
    'pd_index_ext', 'hiframes', bodo), ('_dti_val_finalize', 'pd_index_ext',
    'hiframes', bodo), ('init_datetime_index', 'pd_index_ext', 'hiframes',
    bodo), ('init_timedelta_index', 'pd_index_ext', 'hiframes', bodo), (
    'init_range_index', 'pd_index_ext', 'hiframes', bodo), (
    'init_heter_index', 'pd_index_ext', 'hiframes', bodo), (
    'get_int_arr_data', 'int_arr_ext', 'libs', bodo), ('get_int_arr_bitmap',
    'int_arr_ext', 'libs', bodo), ('init_integer_array', 'int_arr_ext',
    'libs', bodo), ('alloc_int_array', 'int_arr_ext', 'libs', bodo), (
    'inplace_eq', 'str_arr_ext', 'libs', bodo), ('get_bool_arr_data',
    'bool_arr_ext', 'libs', bodo), ('get_bool_arr_bitmap', 'bool_arr_ext',
    'libs', bodo), ('init_bool_array', 'bool_arr_ext', 'libs', bodo), (
    'alloc_bool_array', 'bool_arr_ext', 'libs', bodo), (bodo.libs.
    bool_arr_ext.compute_or_body,), (bodo.libs.bool_arr_ext.
    compute_and_body,), ('alloc_datetime_date_array', 'datetime_date_ext',
    'hiframes', bodo), ('alloc_datetime_timedelta_array',
    'datetime_timedelta_ext', 'hiframes', bodo), ('cat_replace',
    'pd_categorical_ext', 'hiframes', bodo), ('init_categorical_array',
    'pd_categorical_ext', 'hiframes', bodo), ('alloc_categorical_array',
    'pd_categorical_ext', 'hiframes', bodo), ('get_categorical_arr_codes',
    'pd_categorical_ext', 'hiframes', bodo), ('_sum_handle_nan',
    'series_kernels', 'hiframes', bodo), ('_box_cat_val', 'series_kernels',
    'hiframes', bodo), ('_mean_handle_nan', 'series_kernels', 'hiframes',
    bodo), ('_var_handle_mincount', 'series_kernels', 'hiframes', bodo), (
    '_handle_nan_count', 'series_kernels', 'hiframes', bodo), (
    '_handle_nan_count_ddof', 'series_kernels', 'hiframes', bodo), (
    'dist_return', 'distributed_api', 'libs', bodo), ('init_dataframe',
    'pd_dataframe_ext', 'hiframes', bodo), ('get_dataframe_data',
    'pd_dataframe_ext', 'hiframes', bodo), ('get_dataframe_table',
    'pd_dataframe_ext', 'hiframes', bodo), ('get_table_data', 'table',
    'hiframes', bodo), ('get_dataframe_index', 'pd_dataframe_ext',
    'hiframes', bodo), ('init_rolling', 'pd_rolling_ext', 'hiframes', bodo),
    ('init_groupby', 'pd_groupby_ext', 'hiframes', bodo), ('calc_nitems',
    'array_kernels', 'libs', bodo), ('concat', 'array_kernels', 'libs',
    bodo), ('unique', 'array_kernels', 'libs', bodo), ('nunique',
    'array_kernels', 'libs', bodo), ('quantile', 'array_kernels', 'libs',
    bodo), ('explode', 'array_kernels', 'libs', bodo), (
    'str_arr_from_sequence', 'str_arr_ext', 'libs', bodo), (
    'parse_datetime_str', 'pd_timestamp_ext', 'hiframes', bodo), (
    'integer_to_dt64', 'pd_timestamp_ext', 'hiframes', bodo), (
    'dt64_to_integer', 'pd_timestamp_ext', 'hiframes', bodo), (
    'timedelta64_to_integer', 'pd_timestamp_ext', 'hiframes', bodo), (
    'integer_to_timedelta64', 'pd_timestamp_ext', 'hiframes', bodo), (
    'npy_datetimestruct_to_datetime', 'pd_timestamp_ext', 'hiframes', bodo),
    ('isna', 'array_kernels', 'libs', bodo), ('copy',), (
    'from_iterable_impl', 'typing', 'utils', bodo), ('chain', itertools), (
    'groupby',), ('rolling',), (pd.CategoricalDtype,), (bodo.hiframes.
    pd_categorical_ext.get_code_for_value,), ('asarray', np), ('int32', np),
    ('int64', np), ('float64', np), ('float32', np), ('bool_', np), ('full',
    np), ('round', np), ('isnan', np), ('isnat', np), ('internal_prange',
    'parfor', numba), ('internal_prange', 'parfor', 'parfors', numba), (
    'empty_inferred', 'ndarray', 'unsafe', numba), ('_slice_span',
    'unicode', numba), ('_normalize_slice', 'unicode', numba), (
    'init_session_builder', 'pyspark_ext', 'libs', bodo), ('init_session',
    'pyspark_ext', 'libs', bodo), ('init_spark_df', 'pyspark_ext', 'libs',
    bodo), ('h5size', 'h5_api', 'io', bodo), ('pre_alloc_struct_array',
    'struct_arr_ext', 'libs', bodo), (bodo.libs.struct_arr_ext.
    pre_alloc_struct_array,), ('pre_alloc_tuple_array', 'tuple_arr_ext',
    'libs', bodo), (bodo.libs.tuple_arr_ext.pre_alloc_tuple_array,), (
    'pre_alloc_array_item_array', 'array_item_arr_ext', 'libs', bodo), (
    bodo.libs.array_item_arr_ext.pre_alloc_array_item_array,), (
    'dist_reduce', 'distributed_api', 'libs', bodo), (bodo.libs.
    distributed_api.dist_reduce,), ('pre_alloc_string_array', 'str_arr_ext',
    'libs', bodo), (bodo.libs.str_arr_ext.pre_alloc_string_array,), (
    'pre_alloc_binary_array', 'binary_arr_ext', 'libs', bodo), (bodo.libs.
    binary_arr_ext.pre_alloc_binary_array,), ('pre_alloc_map_array',
    'map_arr_ext', 'libs', bodo), (bodo.libs.map_arr_ext.
    pre_alloc_map_array,), ('prange', bodo), (bodo.prange,), ('objmode',
    bodo), (bodo.objmode,), ('get_label_dict_from_categories',
    'pd_categorial_ext', 'hiframes', bodo), (
    'get_label_dict_from_categories_no_duplicates', 'pd_categorial_ext',
    'hiframes', bodo), ('build_nullable_tuple', 'nullable_tuple_ext',
    'libs', bodo)}


def remove_hiframes(rhs, lives, call_list):
    hey__rgbz = tuple(call_list)
    if hey__rgbz in no_side_effect_call_tuples:
        return True
    if len(call_list) == 4 and call_list[1:] == ['conversion', 'utils', bodo]:
        return True
    if isinstance(call_list[-1], pytypes.ModuleType) and call_list[-1
        ].__name__ == 'bodosql':
        return True
    if len(call_list) == 2 and call_list[0] == 'copy':
        return True
    if call_list == ['h5read', 'h5_api', 'io', bodo] and rhs.args[5
        ].name not in lives:
        return True
    if call_list == ['move_str_binary_arr_payload', 'str_arr_ext', 'libs', bodo
        ] and rhs.args[0].name not in lives:
        return True
    if call_list == ['setna', 'array_kernels', 'libs', bodo] and rhs.args[0
        ].name not in lives:
        return True
    if call_list == ['set_table_data', 'table', 'hiframes', bodo] and rhs.args[
        0].name not in lives:
        return True
    if len(hey__rgbz) == 1 and tuple in getattr(hey__rgbz[0], '__mro__', ()):
        return True
    return False


numba.core.ir_utils.remove_call_handlers.append(remove_hiframes)


def compile_func_single_block(func, args, ret_var, typing_info=None,
    extra_globals=None, infer_types=True, run_untyped_pass=False, flags=
    None, replace_globals=True):
    mjyy__fzfg = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd, 'math':
        math}
    if extra_globals is not None:
        mjyy__fzfg.update(extra_globals)
    if not replace_globals:
        mjyy__fzfg = func.__globals__
    loc = ir.Loc('', 0)
    if ret_var:
        loc = ret_var.loc
    if typing_info and infer_types:
        loc = typing_info.curr_loc
        f_ir = compile_to_numba_ir(func, mjyy__fzfg, typingctx=typing_info.
            typingctx, targetctx=typing_info.targetctx, arg_typs=tuple(
            typing_info.typemap[gri__pmc.name] for gri__pmc in args),
            typemap=typing_info.typemap, calltypes=typing_info.calltypes)
    else:
        f_ir = compile_to_numba_ir(func, mjyy__fzfg)
    assert len(f_ir.blocks
        ) == 1, 'only single block functions supported in compile_func_single_block()'
    if run_untyped_pass:
        tqu__wogun = tuple(typing_info.typemap[gri__pmc.name] for gri__pmc in
            args)
        bmv__rhu = bodo.transforms.untyped_pass.UntypedPass(f_ir,
            typing_info.typingctx, tqu__wogun, {}, {}, flags)
        bmv__rhu.run()
    zol__urfl = f_ir.blocks.popitem()[1]
    replace_arg_nodes(zol__urfl, args)
    nxo__fcj = zol__urfl.body[:-2]
    update_locs(nxo__fcj[len(args):], loc)
    for stmt in nxo__fcj[:len(args)]:
        stmt.target.loc = loc
    if ret_var is not None:
        igpa__cmnss = zol__urfl.body[-2]
        assert is_assign(igpa__cmnss) and is_expr(igpa__cmnss.value, 'cast')
        bsq__khktg = igpa__cmnss.value.value
        nxo__fcj.append(ir.Assign(bsq__khktg, ret_var, loc))
    return nxo__fcj


def update_locs(node_list, loc):
    for stmt in node_list:
        stmt.loc = loc
        for kkzo__qfcg in stmt.list_vars():
            kkzo__qfcg.loc = loc
        if is_assign(stmt):
            stmt.value.loc = loc


def get_stmt_defs(stmt):
    if is_assign(stmt):
        return set([stmt.target.name])
    if type(stmt) in numba.core.analysis.ir_extension_usedefs:
        sacj__ilma = numba.core.analysis.ir_extension_usedefs[type(stmt)]
        lbbkm__slj, wgjo__qugjz = sacj__ilma(stmt)
        return wgjo__qugjz
    return set()


def get_const_value(var, func_ir, err_msg, typemap=None, arg_types=None,
    file_info=None):
    if hasattr(var, 'loc'):
        loc = var.loc
    else:
        loc = None
    try:
        kgkj__grveg = get_const_value_inner(func_ir, var, arg_types,
            typemap, file_info=file_info)
        if isinstance(kgkj__grveg, ir.UndefinedType):
            bwj__hpw = func_ir.get_definition(var.name).name
            raise BodoError(f"name '{bwj__hpw}' is not defined", loc=loc)
    except GuardException as mtfn__pjfzn:
        raise BodoError(err_msg, loc=loc)
    return kgkj__grveg


def get_const_value_inner(func_ir, var, arg_types=None, typemap=None,
    updated_containers=None, file_info=None, pyobject_to_literal=False,
    literalize_args=True):
    require(isinstance(var, ir.Var))
    reu__ideae = get_definition(func_ir, var)
    woxg__krdk = None
    if typemap is not None:
        woxg__krdk = typemap.get(var.name, None)
    if isinstance(reu__ideae, ir.Arg) and arg_types is not None:
        woxg__krdk = arg_types[reu__ideae.index]
    if updated_containers and var.name in updated_containers:
        raise BodoConstUpdatedError(
            f"variable '{var.name}' is updated inplace using '{updated_containers[var.name]}'"
            )
    if is_literal_type(woxg__krdk):
        return get_literal_value(woxg__krdk)
    if isinstance(reu__ideae, (ir.Const, ir.Global, ir.FreeVar)):
        kgkj__grveg = reu__ideae.value
        return kgkj__grveg
    if literalize_args and isinstance(reu__ideae, ir.Arg
        ) and can_literalize_type(woxg__krdk, pyobject_to_literal):
        raise numba.core.errors.ForceLiteralArg({reu__ideae.index}, loc=var
            .loc, file_infos={reu__ideae.index: file_info} if file_info is not
            None else None)
    if is_expr(reu__ideae, 'binop'):
        if file_info and reu__ideae.fn == operator.add:
            try:
                zjy__mtuf = get_const_value_inner(func_ir, reu__ideae.lhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(zjy__mtuf, True)
                czv__iajp = get_const_value_inner(func_ir, reu__ideae.rhs,
                    arg_types, typemap, updated_containers, file_info)
                return reu__ideae.fn(zjy__mtuf, czv__iajp)
            except (GuardException, BodoConstUpdatedError) as mtfn__pjfzn:
                pass
            try:
                czv__iajp = get_const_value_inner(func_ir, reu__ideae.rhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(czv__iajp, False)
                zjy__mtuf = get_const_value_inner(func_ir, reu__ideae.lhs,
                    arg_types, typemap, updated_containers, file_info)
                return reu__ideae.fn(zjy__mtuf, czv__iajp)
            except (GuardException, BodoConstUpdatedError) as mtfn__pjfzn:
                pass
        zjy__mtuf = get_const_value_inner(func_ir, reu__ideae.lhs,
            arg_types, typemap, updated_containers)
        czv__iajp = get_const_value_inner(func_ir, reu__ideae.rhs,
            arg_types, typemap, updated_containers)
        return reu__ideae.fn(zjy__mtuf, czv__iajp)
    if is_expr(reu__ideae, 'unary'):
        kgkj__grveg = get_const_value_inner(func_ir, reu__ideae.value,
            arg_types, typemap, updated_containers)
        return reu__ideae.fn(kgkj__grveg)
    if is_expr(reu__ideae, 'getattr') and typemap:
        rqs__cni = typemap.get(reu__ideae.value.name, None)
        if isinstance(rqs__cni, bodo.hiframes.pd_dataframe_ext.DataFrameType
            ) and reu__ideae.attr == 'columns':
            return pd.Index(rqs__cni.columns)
        if isinstance(rqs__cni, types.SliceType):
            ufb__hanw = get_definition(func_ir, reu__ideae.value)
            require(is_call(ufb__hanw))
            yzo__juz = find_callname(func_ir, ufb__hanw)
            gnzlg__sai = False
            if yzo__juz == ('_normalize_slice', 'numba.cpython.unicode'):
                require(reu__ideae.attr in ('start', 'step'))
                ufb__hanw = get_definition(func_ir, ufb__hanw.args[0])
                gnzlg__sai = True
            require(find_callname(func_ir, ufb__hanw) == ('slice', 'builtins'))
            if len(ufb__hanw.args) == 1:
                if reu__ideae.attr == 'start':
                    return 0
                if reu__ideae.attr == 'step':
                    return 1
                require(reu__ideae.attr == 'stop')
                return get_const_value_inner(func_ir, ufb__hanw.args[0],
                    arg_types, typemap, updated_containers)
            if reu__ideae.attr == 'start':
                kgkj__grveg = get_const_value_inner(func_ir, ufb__hanw.args
                    [0], arg_types, typemap, updated_containers)
                if kgkj__grveg is None:
                    kgkj__grveg = 0
                if gnzlg__sai:
                    require(kgkj__grveg == 0)
                return kgkj__grveg
            if reu__ideae.attr == 'stop':
                assert not gnzlg__sai
                return get_const_value_inner(func_ir, ufb__hanw.args[1],
                    arg_types, typemap, updated_containers)
            require(reu__ideae.attr == 'step')
            if len(ufb__hanw.args) == 2:
                return 1
            else:
                kgkj__grveg = get_const_value_inner(func_ir, ufb__hanw.args
                    [2], arg_types, typemap, updated_containers)
                if kgkj__grveg is None:
                    kgkj__grveg = 1
                if gnzlg__sai:
                    require(kgkj__grveg == 1)
                return kgkj__grveg
    if is_expr(reu__ideae, 'getattr'):
        return getattr(get_const_value_inner(func_ir, reu__ideae.value,
            arg_types, typemap, updated_containers), reu__ideae.attr)
    if is_expr(reu__ideae, 'getitem'):
        value = get_const_value_inner(func_ir, reu__ideae.value, arg_types,
            typemap, updated_containers)
        index = get_const_value_inner(func_ir, reu__ideae.index, arg_types,
            typemap, updated_containers)
        return value[index]
    vgw__ngf = guard(find_callname, func_ir, reu__ideae, typemap)
    if vgw__ngf is not None and len(vgw__ngf) == 2 and vgw__ngf[0
        ] == 'keys' and isinstance(vgw__ngf[1], ir.Var):
        pulwx__uknjb = reu__ideae.func
        reu__ideae = get_definition(func_ir, vgw__ngf[1])
        hyxtb__ennpm = vgw__ngf[1].name
        if updated_containers and hyxtb__ennpm in updated_containers:
            raise BodoConstUpdatedError(
                "variable '{}' is updated inplace using '{}'".format(
                hyxtb__ennpm, updated_containers[hyxtb__ennpm]))
        require(is_expr(reu__ideae, 'build_map'))
        vals = [kkzo__qfcg[0] for kkzo__qfcg in reu__ideae.items]
        agbtg__evmv = guard(get_definition, func_ir, pulwx__uknjb)
        assert isinstance(agbtg__evmv, ir.Expr) and agbtg__evmv.attr == 'keys'
        agbtg__evmv.attr = 'copy'
        return [get_const_value_inner(func_ir, kkzo__qfcg, arg_types,
            typemap, updated_containers) for kkzo__qfcg in vals]
    if is_expr(reu__ideae, 'build_map'):
        return {get_const_value_inner(func_ir, kkzo__qfcg[0], arg_types,
            typemap, updated_containers): get_const_value_inner(func_ir,
            kkzo__qfcg[1], arg_types, typemap, updated_containers) for
            kkzo__qfcg in reu__ideae.items}
    if is_expr(reu__ideae, 'build_tuple'):
        return tuple(get_const_value_inner(func_ir, kkzo__qfcg, arg_types,
            typemap, updated_containers) for kkzo__qfcg in reu__ideae.items)
    if is_expr(reu__ideae, 'build_list'):
        return [get_const_value_inner(func_ir, kkzo__qfcg, arg_types,
            typemap, updated_containers) for kkzo__qfcg in reu__ideae.items]
    if is_expr(reu__ideae, 'build_set'):
        return {get_const_value_inner(func_ir, kkzo__qfcg, arg_types,
            typemap, updated_containers) for kkzo__qfcg in reu__ideae.items}
    if vgw__ngf == ('list', 'builtins'):
        values = get_const_value_inner(func_ir, reu__ideae.args[0],
            arg_types, typemap, updated_containers)
        if isinstance(values, set):
            values = sorted(values)
        return list(values)
    if vgw__ngf == ('set', 'builtins'):
        return set(get_const_value_inner(func_ir, reu__ideae.args[0],
            arg_types, typemap, updated_containers))
    if vgw__ngf == ('range', 'builtins') and len(reu__ideae.args) == 1:
        return range(get_const_value_inner(func_ir, reu__ideae.args[0],
            arg_types, typemap, updated_containers))
    if vgw__ngf == ('slice', 'builtins'):
        return slice(*tuple(get_const_value_inner(func_ir, kkzo__qfcg,
            arg_types, typemap, updated_containers) for kkzo__qfcg in
            reu__ideae.args))
    if vgw__ngf == ('str', 'builtins'):
        return str(get_const_value_inner(func_ir, reu__ideae.args[0],
            arg_types, typemap, updated_containers))
    if vgw__ngf == ('bool', 'builtins'):
        return bool(get_const_value_inner(func_ir, reu__ideae.args[0],
            arg_types, typemap, updated_containers))
    if vgw__ngf == ('format', 'builtins'):
        gri__pmc = get_const_value_inner(func_ir, reu__ideae.args[0],
            arg_types, typemap, updated_containers)
        rxpee__jpv = get_const_value_inner(func_ir, reu__ideae.args[1],
            arg_types, typemap, updated_containers) if len(reu__ideae.args
            ) > 1 else ''
        return format(gri__pmc, rxpee__jpv)
    if vgw__ngf in (('init_binary_str_index', 'bodo.hiframes.pd_index_ext'),
        ('init_numeric_index', 'bodo.hiframes.pd_index_ext'), (
        'init_categorical_index', 'bodo.hiframes.pd_index_ext'), (
        'init_datetime_index', 'bodo.hiframes.pd_index_ext'), (
        'init_timedelta_index', 'bodo.hiframes.pd_index_ext'), (
        'init_heter_index', 'bodo.hiframes.pd_index_ext')):
        return pd.Index(get_const_value_inner(func_ir, reu__ideae.args[0],
            arg_types, typemap, updated_containers))
    if vgw__ngf == ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'):
        return np.array(get_const_value_inner(func_ir, reu__ideae.args[0],
            arg_types, typemap, updated_containers))
    if vgw__ngf == ('init_range_index', 'bodo.hiframes.pd_index_ext'):
        return pd.RangeIndex(get_const_value_inner(func_ir, reu__ideae.args
            [0], arg_types, typemap, updated_containers),
            get_const_value_inner(func_ir, reu__ideae.args[1], arg_types,
            typemap, updated_containers), get_const_value_inner(func_ir,
            reu__ideae.args[2], arg_types, typemap, updated_containers))
    if vgw__ngf == ('len', 'builtins') and typemap and isinstance(typemap.
        get(reu__ideae.args[0].name, None), types.BaseTuple):
        return len(typemap[reu__ideae.args[0].name])
    if vgw__ngf == ('len', 'builtins'):
        thknt__rsz = guard(get_definition, func_ir, reu__ideae.args[0])
        if isinstance(thknt__rsz, ir.Expr) and thknt__rsz.op in ('build_tuple',
            'build_list', 'build_set', 'build_map'):
            return len(thknt__rsz.items)
        return len(get_const_value_inner(func_ir, reu__ideae.args[0],
            arg_types, typemap, updated_containers))
    if vgw__ngf == ('CategoricalDtype', 'pandas'):
        kws = dict(reu__ideae.kws)
        wjyrp__gwp = get_call_expr_arg('CategoricalDtype', reu__ideae.args,
            kws, 0, 'categories', '')
        gvtk__bgb = get_call_expr_arg('CategoricalDtype', reu__ideae.args,
            kws, 1, 'ordered', False)
        if gvtk__bgb is not False:
            gvtk__bgb = get_const_value_inner(func_ir, gvtk__bgb, arg_types,
                typemap, updated_containers)
        if wjyrp__gwp == '':
            wjyrp__gwp = None
        else:
            wjyrp__gwp = get_const_value_inner(func_ir, wjyrp__gwp,
                arg_types, typemap, updated_containers)
        return pd.CategoricalDtype(wjyrp__gwp, gvtk__bgb)
    if vgw__ngf == ('dtype', 'numpy'):
        return np.dtype(get_const_value_inner(func_ir, reu__ideae.args[0],
            arg_types, typemap, updated_containers))
    if vgw__ngf is not None and len(vgw__ngf) == 2 and vgw__ngf[1
        ] == 'pandas' and vgw__ngf[0] in ('Int8Dtype', 'Int16Dtype',
        'Int32Dtype', 'Int64Dtype', 'UInt8Dtype', 'UInt16Dtype',
        'UInt32Dtype', 'UInt64Dtype'):
        return getattr(pd, vgw__ngf[0])()
    if vgw__ngf is not None and len(vgw__ngf) == 2 and isinstance(vgw__ngf[
        1], ir.Var):
        kgkj__grveg = get_const_value_inner(func_ir, vgw__ngf[1], arg_types,
            typemap, updated_containers)
        args = [get_const_value_inner(func_ir, kkzo__qfcg, arg_types,
            typemap, updated_containers) for kkzo__qfcg in reu__ideae.args]
        kws = {uygmy__zaviw[0]: get_const_value_inner(func_ir, uygmy__zaviw
            [1], arg_types, typemap, updated_containers) for uygmy__zaviw in
            reu__ideae.kws}
        return getattr(kgkj__grveg, vgw__ngf[0])(*args, **kws)
    if vgw__ngf is not None and len(vgw__ngf) == 2 and vgw__ngf[1
        ] == 'bodo' and vgw__ngf[0] in bodo_types_with_params:
        args = tuple(get_const_value_inner(func_ir, kkzo__qfcg, arg_types,
            typemap, updated_containers) for kkzo__qfcg in reu__ideae.args)
        kwargs = {bwj__hpw: get_const_value_inner(func_ir, kkzo__qfcg,
            arg_types, typemap, updated_containers) for bwj__hpw,
            kkzo__qfcg in dict(reu__ideae.kws).items()}
        return getattr(bodo, vgw__ngf[0])(*args, **kwargs)
    if is_call(reu__ideae) and typemap and isinstance(typemap.get(
        reu__ideae.func.name, None), types.Dispatcher):
        py_func = typemap[reu__ideae.func.name].dispatcher.py_func
        require(reu__ideae.vararg is None)
        args = tuple(get_const_value_inner(func_ir, kkzo__qfcg, arg_types,
            typemap, updated_containers) for kkzo__qfcg in reu__ideae.args)
        kwargs = {bwj__hpw: get_const_value_inner(func_ir, kkzo__qfcg,
            arg_types, typemap, updated_containers) for bwj__hpw,
            kkzo__qfcg in dict(reu__ideae.kws).items()}
        arg_types = tuple(bodo.typeof(kkzo__qfcg) for kkzo__qfcg in args)
        kw_types = {nseql__cbn: bodo.typeof(kkzo__qfcg) for nseql__cbn,
            kkzo__qfcg in kwargs.items()}
        require(_func_is_pure(py_func, arg_types, kw_types))
        return py_func(*args, **kwargs)
    raise GuardException('Constant value not found')


def _func_is_pure(py_func, arg_types, kw_types):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.ir.csv_ext import CsvReader
    from bodo.ir.json_ext import JsonReader
    from bodo.ir.parquet_ext import ParquetReader
    from bodo.ir.sql_ext import SqlReader
    f_ir, typemap, vqpka__xesod, vqpka__xesod = (bodo.compiler.
        get_func_type_info(py_func, arg_types, kw_types))
    for block in f_ir.blocks.values():
        for stmt in block.body:
            if isinstance(stmt, ir.Print):
                return False
            if isinstance(stmt, (CsvReader, JsonReader, ParquetReader,
                SqlReader)):
                return False
            if is_setitem(stmt) and isinstance(guard(get_definition, f_ir,
                stmt.target), ir.Arg):
                return False
            if is_assign(stmt):
                rhs = stmt.value
                if isinstance(rhs, ir.Yield):
                    return False
                if is_call(rhs):
                    dmli__bgwz = guard(get_definition, f_ir, rhs.func)
                    if isinstance(dmli__bgwz, ir.Const) and isinstance(
                        dmli__bgwz.value, numba.core.dispatcher.
                        ObjModeLiftedWith):
                        return False
                    chegd__llzb = guard(find_callname, f_ir, rhs)
                    if chegd__llzb is None:
                        return False
                    func_name, wovh__elcqj = chegd__llzb
                    if wovh__elcqj == 'pandas' and func_name.startswith('read_'
                        ):
                        return False
                    if chegd__llzb in (('fromfile', 'numpy'), ('file_read',
                        'bodo.io.np_io')):
                        return False
                    if chegd__llzb == ('File', 'h5py'):
                        return False
                    if isinstance(wovh__elcqj, ir.Var):
                        woxg__krdk = typemap[wovh__elcqj.name]
                        if isinstance(woxg__krdk, (DataFrameType, SeriesType)
                            ) and func_name in ('to_csv', 'to_excel',
                            'to_json', 'to_sql', 'to_pickle', 'to_parquet',
                            'info'):
                            return False
                        if isinstance(woxg__krdk, types.Array
                            ) and func_name == 'tofile':
                            return False
                        if isinstance(woxg__krdk, bodo.LoggingLoggerType):
                            return False
                        if str(woxg__krdk).startswith('Mpl'):
                            return False
                        if (func_name in container_update_method_names and
                            isinstance(guard(get_definition, f_ir,
                            wovh__elcqj), ir.Arg)):
                            return False
                    if wovh__elcqj in ('numpy.random', 'time', 'logging',
                        'matplotlib.pyplot'):
                        return False
    return True


def fold_argument_types(pysig, args, kws):

    def normal_handler(index, param, value):
        return value

    def default_handler(index, param, default):
        return types.Omitted(default)

    def stararg_handler(index, param, values):
        return types.StarArgTuple(values)
    args = fold_arguments(pysig, args, kws, normal_handler, default_handler,
        stararg_handler)
    return args


def get_const_func_output_type(func, arg_types, kw_types, typing_context,
    target_context, is_udf=True):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
    py_func = None
    if isinstance(func, types.MakeFunctionLiteral):
        tmxrt__tlr = func.literal_value.code
        cqqw__ghq = {'np': np, 'pd': pd, 'numba': numba, 'bodo': bodo}
        if hasattr(func.literal_value, 'globals'):
            cqqw__ghq = func.literal_value.globals
        f_ir = numba.core.ir_utils.get_ir_of_code(cqqw__ghq, tmxrt__tlr)
        fix_struct_return(f_ir)
        typemap, fuag__ghcnf, tyjbx__bkgfj, vqpka__xesod = (numba.core.
            typed_passes.type_inference_stage(typing_context,
            target_context, f_ir, arg_types, None))
    elif isinstance(func, bodo.utils.typing.FunctionLiteral):
        py_func = func.literal_value
        f_ir, typemap, tyjbx__bkgfj, fuag__ghcnf = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    elif isinstance(func, CPUDispatcher):
        py_func = func.py_func
        f_ir, typemap, tyjbx__bkgfj, fuag__ghcnf = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    else:
        if not isinstance(func, types.Dispatcher):
            if isinstance(func, types.Function):
                raise BodoError(
                    f'Bodo does not support built-in functions yet, {func}')
            else:
                raise BodoError(f'Function type expected, not {func}')
        py_func = func.dispatcher.py_func
        f_ir, typemap, tyjbx__bkgfj, fuag__ghcnf = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    if is_udf and isinstance(fuag__ghcnf, types.DictType):
        fpq__bezpa = guard(get_struct_keynames, f_ir, typemap)
        if fpq__bezpa is not None:
            fuag__ghcnf = StructType((fuag__ghcnf.value_type,) * len(
                fpq__bezpa), fpq__bezpa)
    if is_udf and isinstance(fuag__ghcnf, (SeriesType, HeterogeneousSeriesType)
        ):
        gfp__zhe = numba.core.registry.cpu_target.typing_context
        dtllx__lfyb = numba.core.registry.cpu_target.target_context
        kfxi__ulxem = bodo.transforms.series_pass.SeriesPass(f_ir, gfp__zhe,
            dtllx__lfyb, typemap, tyjbx__bkgfj, {})
        kfxi__ulxem.run()
        kfxi__ulxem.run()
        kfxi__ulxem.run()
        hzbk__trnto = compute_cfg_from_blocks(f_ir.blocks)
        ojl__aeir = [guard(_get_const_series_info, f_ir.blocks[izeh__sjz],
            f_ir, typemap) for izeh__sjz in hzbk__trnto.exit_points() if
            isinstance(f_ir.blocks[izeh__sjz].body[-1], ir.Return)]
        if None in ojl__aeir or len(pd.Series(ojl__aeir).unique()) != 1:
            fuag__ghcnf.const_info = None
        else:
            fuag__ghcnf.const_info = ojl__aeir[0]
    return fuag__ghcnf


def _get_const_series_info(block, f_ir, typemap):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType
    assert isinstance(block.body[-1], ir.Return)
    lkjs__pbksq = block.body[-1].value
    jsyd__dsc = get_definition(f_ir, lkjs__pbksq)
    require(is_expr(jsyd__dsc, 'cast'))
    jsyd__dsc = get_definition(f_ir, jsyd__dsc.value)
    require(is_call(jsyd__dsc) and find_callname(f_ir, jsyd__dsc) == (
        'init_series', 'bodo.hiframes.pd_series_ext'))
    puy__lgimq = jsyd__dsc.args[1]
    vnodt__vyr = tuple(get_const_value_inner(f_ir, puy__lgimq, typemap=typemap)
        )
    if isinstance(typemap[lkjs__pbksq.name], HeterogeneousSeriesType):
        return len(typemap[lkjs__pbksq.name].data), vnodt__vyr
    zrwo__hbdv = jsyd__dsc.args[0]
    udu__crdrx = get_definition(f_ir, zrwo__hbdv)
    func_name, geu__uvcd = find_callname(f_ir, udu__crdrx)
    if is_call(udu__crdrx) and bodo.utils.utils.is_alloc_callname(func_name,
        geu__uvcd):
        hnb__vicq = udu__crdrx.args[0]
        iwd__xeh = get_const_value_inner(f_ir, hnb__vicq, typemap=typemap)
        return iwd__xeh, vnodt__vyr
    if is_call(udu__crdrx) and find_callname(f_ir, udu__crdrx) in [(
        'asarray', 'numpy'), ('str_arr_from_sequence', 'bodo.libs.str_arr_ext')
        ]:
        zrwo__hbdv = udu__crdrx.args[0]
        udu__crdrx = get_definition(f_ir, zrwo__hbdv)
    require(is_expr(udu__crdrx, 'build_tuple') or is_expr(udu__crdrx,
        'build_list'))
    return len(udu__crdrx.items), vnodt__vyr


def extract_keyvals_from_struct_map(f_ir, build_map, loc, scope, typemap=None):
    hab__jkso = []
    wjgr__qwmph = []
    values = []
    for nseql__cbn, kkzo__qfcg in build_map.items:
        djml__avqf = find_const(f_ir, nseql__cbn)
        require(isinstance(djml__avqf, str))
        wjgr__qwmph.append(djml__avqf)
        hab__jkso.append(nseql__cbn)
        values.append(kkzo__qfcg)
    huz__jgz = ir.Var(scope, mk_unique_var('val_tup'), loc)
    mel__zadan = ir.Assign(ir.Expr.build_tuple(values, loc), huz__jgz, loc)
    f_ir._definitions[huz__jgz.name] = [mel__zadan.value]
    qcq__feh = ir.Var(scope, mk_unique_var('key_tup'), loc)
    bjltm__fcfw = ir.Assign(ir.Expr.build_tuple(hab__jkso, loc), qcq__feh, loc)
    f_ir._definitions[qcq__feh.name] = [bjltm__fcfw.value]
    if typemap is not None:
        typemap[huz__jgz.name] = types.Tuple([typemap[kkzo__qfcg.name] for
            kkzo__qfcg in values])
        typemap[qcq__feh.name] = types.Tuple([typemap[kkzo__qfcg.name] for
            kkzo__qfcg in hab__jkso])
    return wjgr__qwmph, huz__jgz, mel__zadan, qcq__feh, bjltm__fcfw


def _replace_const_map_return(f_ir, block, label):
    require(isinstance(block.body[-1], ir.Return))
    fmrcy__tbpv = block.body[-1].value
    lpyt__lgui = guard(get_definition, f_ir, fmrcy__tbpv)
    require(is_expr(lpyt__lgui, 'cast'))
    jsyd__dsc = guard(get_definition, f_ir, lpyt__lgui.value)
    require(is_expr(jsyd__dsc, 'build_map'))
    require(len(jsyd__dsc.items) > 0)
    loc = block.loc
    scope = block.scope
    wjgr__qwmph, huz__jgz, mel__zadan, qcq__feh, bjltm__fcfw = (
        extract_keyvals_from_struct_map(f_ir, jsyd__dsc, loc, scope))
    agm__nlo = ir.Var(scope, mk_unique_var('conv_call'), loc)
    dzy__xly = ir.Assign(ir.Global('struct_if_heter_dict', bodo.utils.
        conversion.struct_if_heter_dict, loc), agm__nlo, loc)
    f_ir._definitions[agm__nlo.name] = [dzy__xly.value]
    wwv__kytyg = ir.Var(scope, mk_unique_var('struct_val'), loc)
    suyl__ubs = ir.Assign(ir.Expr.call(agm__nlo, [huz__jgz, qcq__feh], {},
        loc), wwv__kytyg, loc)
    f_ir._definitions[wwv__kytyg.name] = [suyl__ubs.value]
    lpyt__lgui.value = wwv__kytyg
    jsyd__dsc.items = [(nseql__cbn, nseql__cbn) for nseql__cbn,
        vqpka__xesod in jsyd__dsc.items]
    block.body = block.body[:-2] + [mel__zadan, bjltm__fcfw, dzy__xly,
        suyl__ubs] + block.body[-2:]
    return tuple(wjgr__qwmph)


def get_struct_keynames(f_ir, typemap):
    hzbk__trnto = compute_cfg_from_blocks(f_ir.blocks)
    cgn__erjjw = list(hzbk__trnto.exit_points())[0]
    block = f_ir.blocks[cgn__erjjw]
    require(isinstance(block.body[-1], ir.Return))
    fmrcy__tbpv = block.body[-1].value
    lpyt__lgui = guard(get_definition, f_ir, fmrcy__tbpv)
    require(is_expr(lpyt__lgui, 'cast'))
    jsyd__dsc = guard(get_definition, f_ir, lpyt__lgui.value)
    require(is_call(jsyd__dsc) and find_callname(f_ir, jsyd__dsc) == (
        'struct_if_heter_dict', 'bodo.utils.conversion'))
    return get_overload_const_list(typemap[jsyd__dsc.args[1].name])


def fix_struct_return(f_ir):
    tdbzv__zgwg = None
    hzbk__trnto = compute_cfg_from_blocks(f_ir.blocks)
    for cgn__erjjw in hzbk__trnto.exit_points():
        tdbzv__zgwg = guard(_replace_const_map_return, f_ir, f_ir.blocks[
            cgn__erjjw], cgn__erjjw)
    return tdbzv__zgwg


def update_node_list_definitions(node_list, func_ir):
    loc = ir.Loc('', 0)
    dxnh__tnlff = ir.Block(ir.Scope(None, loc), loc)
    dxnh__tnlff.body = node_list
    build_definitions({(0): dxnh__tnlff}, func_ir._definitions)
    return


NESTED_TUP_SENTINEL = '$BODO_NESTED_TUP'


def gen_const_val_str(c):
    if isinstance(c, tuple):
        return "'{}{}', ".format(NESTED_TUP_SENTINEL, len(c)) + ', '.join(
            gen_const_val_str(kkzo__qfcg) for kkzo__qfcg in c)
    if isinstance(c, str):
        return "'{}'".format(c)
    if isinstance(c, (pd.Timestamp, pd.Timedelta, float)):
        return "'{}'".format(c)
    return str(c)


def gen_const_tup(vals):
    heyv__dlzad = ', '.join(gen_const_val_str(c) for c in vals)
    return '({}{})'.format(heyv__dlzad, ',' if len(vals) == 1 else '')


def get_const_tup_vals(c_typ):
    vals = get_overload_const_list(c_typ)
    return _get_original_nested_tups(vals)


def _get_original_nested_tups(vals):
    for yopnr__rbij in range(len(vals) - 1, -1, -1):
        kkzo__qfcg = vals[yopnr__rbij]
        if isinstance(kkzo__qfcg, str) and kkzo__qfcg.startswith(
            NESTED_TUP_SENTINEL):
            nmmse__rjdwb = int(kkzo__qfcg[len(NESTED_TUP_SENTINEL):])
            return _get_original_nested_tups(tuple(vals[:yopnr__rbij]) + (
                tuple(vals[yopnr__rbij + 1:yopnr__rbij + nmmse__rjdwb + 1])
                ,) + tuple(vals[yopnr__rbij + nmmse__rjdwb + 1:]))
    return tuple(vals)


def get_call_expr_arg(f_name, args, kws, arg_no, arg_name, default=None,
    err_msg=None, use_default=False):
    gri__pmc = None
    if len(args) > arg_no and arg_no >= 0:
        gri__pmc = args[arg_no]
        if arg_name in kws:
            err_msg = (
                f"{f_name}() got multiple values for argument '{arg_name}'")
            raise BodoError(err_msg)
    elif arg_name in kws:
        gri__pmc = kws[arg_name]
    if gri__pmc is None:
        if use_default or default is not None:
            return default
        if err_msg is None:
            err_msg = "{} requires '{}' argument".format(f_name, arg_name)
        raise BodoError(err_msg)
    return gri__pmc


def set_call_expr_arg(var, args, kws, arg_no, arg_name):
    if len(args) > arg_no:
        args[arg_no] = var
    elif arg_name in kws:
        kws[arg_name] = var
    else:
        raise BodoError('cannot set call argument since does not exist')


def avoid_udf_inline(py_func, arg_types, kw_types):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    f_ir = numba.core.compiler.run_frontend(py_func, inline_closures=True)
    if '_bodo_inline' in kw_types and is_overload_constant_bool(kw_types[
        '_bodo_inline']):
        return not get_overload_const_bool(kw_types['_bodo_inline'])
    if any(isinstance(t, DataFrameType) for t in arg_types + tuple(kw_types
        .values())):
        return True
    for block in f_ir.blocks.values():
        if isinstance(block.body[-1], (ir.Raise, ir.StaticRaise)):
            return True
        for stmt in block.body:
            if isinstance(stmt, ir.EnterWith):
                return True
    return False


def replace_func(pass_info, func, args, const=False, pre_nodes=None,
    extra_globals=None, pysig=None, kws=None, inline_bodo_calls=False,
    run_full_pipeline=False):
    mjyy__fzfg = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd}
    if extra_globals is not None:
        mjyy__fzfg.update(extra_globals)
    func.__globals__.update(mjyy__fzfg)
    if pysig is not None:
        pre_nodes = [] if pre_nodes is None else pre_nodes
        scope = next(iter(pass_info.func_ir.blocks.values())).scope
        loc = scope.loc

        def normal_handler(index, param, default):
            return default

        def default_handler(index, param, default):
            bhef__msaw = ir.Var(scope, mk_unique_var('defaults'), loc)
            try:
                pass_info.typemap[bhef__msaw.name] = types.literal(default)
            except:
                pass_info.typemap[bhef__msaw.name] = numba.typeof(default)
            rgkvw__txkgu = ir.Assign(ir.Const(default, loc), bhef__msaw, loc)
            pre_nodes.append(rgkvw__txkgu)
            return bhef__msaw
        args = numba.core.typing.fold_arguments(pysig, args, kws,
            normal_handler, default_handler, normal_handler)
    tqu__wogun = tuple(pass_info.typemap[kkzo__qfcg.name] for kkzo__qfcg in
        args)
    if const:
        tgf__ngs = []
        for yopnr__rbij, gri__pmc in enumerate(args):
            kgkj__grveg = guard(find_const, pass_info.func_ir, gri__pmc)
            if kgkj__grveg:
                tgf__ngs.append(types.literal(kgkj__grveg))
            else:
                tgf__ngs.append(tqu__wogun[yopnr__rbij])
        tqu__wogun = tuple(tgf__ngs)
    return ReplaceFunc(func, tqu__wogun, args, mjyy__fzfg,
        inline_bodo_calls, run_full_pipeline, pre_nodes)


def is_var_size_item_array_type(t):
    assert is_array_typ(t, False)
    return t == string_array_type or isinstance(t, ArrayItemArrayType
        ) or isinstance(t, StructArrayType) and any(
        is_var_size_item_array_type(pmzyd__lbuxj) for pmzyd__lbuxj in t.data)


def gen_init_varsize_alloc_sizes(t):
    if t == string_array_type:
        pytph__zzvi = 'num_chars_{}'.format(ir_utils.next_label())
        return f'  {pytph__zzvi} = 0\n', (pytph__zzvi,)
    if isinstance(t, ArrayItemArrayType):
        wydy__zdkx, cyrb__qcp = gen_init_varsize_alloc_sizes(t.dtype)
        pytph__zzvi = 'num_items_{}'.format(ir_utils.next_label())
        return f'  {pytph__zzvi} = 0\n' + wydy__zdkx, (pytph__zzvi,
            ) + cyrb__qcp
    return '', ()


def gen_varsize_item_sizes(t, item, var_names):
    if t == string_array_type:
        return '    {} += bodo.libs.str_arr_ext.get_utf8_size({})\n'.format(
            var_names[0], item)
    if isinstance(t, ArrayItemArrayType):
        return '    {} += len({})\n'.format(var_names[0], item
            ) + gen_varsize_array_counts(t.dtype, item, var_names[1:])
    return ''


def gen_varsize_array_counts(t, item, var_names):
    if t == string_array_type:
        return ('    {} += bodo.libs.str_arr_ext.get_num_total_chars({})\n'
            .format(var_names[0], item))
    return ''


def get_type_alloc_counts(t):
    if isinstance(t, (StructArrayType, TupleArrayType)):
        return 1 + sum(get_type_alloc_counts(pmzyd__lbuxj.dtype) for
            pmzyd__lbuxj in t.data)
    if isinstance(t, ArrayItemArrayType) or t == string_array_type:
        return 1 + get_type_alloc_counts(t.dtype)
    if isinstance(t, MapArrayType):
        return get_type_alloc_counts(t.key_arr_type) + get_type_alloc_counts(t
            .value_arr_type)
    if bodo.utils.utils.is_array_typ(t, False) or t == bodo.string_type:
        return 1
    if isinstance(t, StructType):
        return sum(get_type_alloc_counts(pmzyd__lbuxj) for pmzyd__lbuxj in
            t.data)
    if isinstance(t, types.BaseTuple):
        return sum(get_type_alloc_counts(pmzyd__lbuxj) for pmzyd__lbuxj in
            t.types)
    return 0


def find_udf_str_name(obj_dtype, func_name, typing_context, caller_name):
    afc__tcvvu = typing_context.resolve_getattr(obj_dtype, func_name)
    if afc__tcvvu is None:
        arp__rkhtv = types.misc.Module(np)
        try:
            afc__tcvvu = typing_context.resolve_getattr(arp__rkhtv, func_name)
        except AttributeError as mtfn__pjfzn:
            afc__tcvvu = None
        if afc__tcvvu is None:
            raise BodoError(
                f"{caller_name}(): No Pandas method or Numpy function found with the name '{func_name}'."
                )
    return afc__tcvvu


def get_udf_str_return_type(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    afc__tcvvu = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(afc__tcvvu, types.BoundFunction):
        if axis is not None:
            lxntn__tyqwu = afc__tcvvu.get_call_type(typing_context, (), {
                'axis': axis})
        else:
            lxntn__tyqwu = afc__tcvvu.get_call_type(typing_context, (), {})
        return lxntn__tyqwu.return_type
    else:
        if bodo.utils.typing.is_numpy_ufunc(afc__tcvvu):
            lxntn__tyqwu = afc__tcvvu.get_call_type(typing_context, (
                obj_dtype,), {})
            return lxntn__tyqwu.return_type
        raise BodoError(
            f"{caller_name}(): Only Pandas methods and np.ufunc are supported as string literals. '{func_name}' not supported."
            )


def get_pandas_method_str_impl(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    afc__tcvvu = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(afc__tcvvu, types.BoundFunction):
        dtd__nwpcx = afc__tcvvu.template
        if axis is not None:
            return dtd__nwpcx._overload_func(obj_dtype, axis=axis)
        else:
            return dtd__nwpcx._overload_func(obj_dtype)
    return None


def dict_to_const_keys_var_values_lists(dict_var, func_ir, arg_types,
    typemap, updated_containers, require_const_map, label):
    require(isinstance(dict_var, ir.Var))
    pxff__pcx = get_definition(func_ir, dict_var)
    require(isinstance(pxff__pcx, ir.Expr))
    require(pxff__pcx.op == 'build_map')
    zlw__yite = pxff__pcx.items
    hab__jkso = []
    values = []
    cbb__uxwd = False
    for yopnr__rbij in range(len(zlw__yite)):
        vxnw__chc, value = zlw__yite[yopnr__rbij]
        try:
            bvnt__xjuww = get_const_value_inner(func_ir, vxnw__chc,
                arg_types, typemap, updated_containers)
            hab__jkso.append(bvnt__xjuww)
            values.append(value)
        except GuardException as mtfn__pjfzn:
            require_const_map[vxnw__chc] = label
            cbb__uxwd = True
    if cbb__uxwd:
        raise GuardException
    return hab__jkso, values


def _get_const_keys_from_dict(args, func_ir, build_map, err_msg, loc):
    try:
        hab__jkso = tuple(get_const_value_inner(func_ir, t[0], args) for t in
            build_map.items)
    except GuardException as mtfn__pjfzn:
        raise BodoError(err_msg, loc)
    if not all(isinstance(c, (str, int)) for c in hab__jkso):
        raise BodoError(err_msg, loc)
    return hab__jkso


def _convert_const_key_dict(args, func_ir, build_map, err_msg, scope, loc,
    output_sentinel_tuple=False):
    hab__jkso = _get_const_keys_from_dict(args, func_ir, build_map, err_msg,
        loc)
    onu__wshp = []
    gfrs__azywa = [bodo.transforms.typing_pass._create_const_var(nseql__cbn,
        'dict_key', scope, loc, onu__wshp) for nseql__cbn in hab__jkso]
    rojj__kdk = [t[1] for t in build_map.items]
    if output_sentinel_tuple:
        jssb__sogc = ir.Var(scope, mk_unique_var('sentinel'), loc)
        lsdw__cybg = ir.Var(scope, mk_unique_var('dict_tup'), loc)
        onu__wshp.append(ir.Assign(ir.Const('__bodo_tup', loc), jssb__sogc,
            loc))
        iuje__wfo = [jssb__sogc] + gfrs__azywa + rojj__kdk
        onu__wshp.append(ir.Assign(ir.Expr.build_tuple(iuje__wfo, loc),
            lsdw__cybg, loc))
        return (lsdw__cybg,), onu__wshp
    else:
        qudsp__tsx = ir.Var(scope, mk_unique_var('values_tup'), loc)
        jbn__ejy = ir.Var(scope, mk_unique_var('idx_tup'), loc)
        onu__wshp.append(ir.Assign(ir.Expr.build_tuple(rojj__kdk, loc),
            qudsp__tsx, loc))
        onu__wshp.append(ir.Assign(ir.Expr.build_tuple(gfrs__azywa, loc),
            jbn__ejy, loc))
        return (qudsp__tsx, jbn__ejy), onu__wshp
