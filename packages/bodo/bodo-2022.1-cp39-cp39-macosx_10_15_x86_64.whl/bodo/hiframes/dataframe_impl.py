"""
Implementation of DataFrame attributes and methods using overload.
"""
import operator
import re
import warnings
from collections import namedtuple
from typing import Tuple
import llvmlite.llvmpy.core as lc
import numba
import numpy as np
import pandas as pd
from numba.core import cgutils, ir, types
from numba.core.imputils import RefType, impl_ret_borrowed, impl_ret_new_ref, iternext_impl, lower_builtin
from numba.core.ir_utils import mk_unique_var, next_label
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import models, overload, overload_attribute, overload_method, register_model, type_callable
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import _no_input, datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported, handle_inplace_df_type_change
from bodo.hiframes.pd_index_ext import StringIndexType, is_pd_index_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import SeriesType, if_series_to_array_type
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_type
from bodo.hiframes.rolling import is_supported_shift_array_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils.transform import bodo_types_with_params, gen_const_tup, no_side_effect_call_tuples
from bodo.utils.typing import BodoError, BodoWarning, check_unsupported_args, dtype_to_array_type, ensure_constant_arg, ensure_constant_values, get_index_data_arr_types, get_index_names, get_literal_value, get_nullable_and_non_nullable_types, get_overload_const_bool, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_const_tuple, get_overload_constant_dict, get_overload_constant_series, is_common_scalar_dtype, is_literal_type, is_overload_bool, is_overload_bool_list, is_overload_constant_bool, is_overload_constant_dict, is_overload_constant_int, is_overload_constant_list, is_overload_constant_series, is_overload_constant_str, is_overload_constant_tuple, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_overload_zero, parse_dtype, raise_bodo_error, raise_const_error, unliteral_val
from bodo.utils.utils import is_array_typ


@overload_attribute(DataFrameType, 'index', inline='always')
def overload_dataframe_index(df):
    return lambda df: bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)


def generate_col_to_index_func_text(col_names: Tuple):
    if all(isinstance(a, str) for a in col_names) or all(isinstance(a,
        bytes) for a in col_names):
        osq__cgfz = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return (
            f'bodo.hiframes.pd_index_ext.init_binary_str_index({osq__cgfz})\n')
    elif all(isinstance(a, (int, float)) for a in col_names):
        arr = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return f'bodo.hiframes.pd_index_ext.init_numeric_index({arr})\n'
    else:
        return f'bodo.hiframes.pd_index_ext.init_heter_index({col_names})\n'


@overload_attribute(DataFrameType, 'columns', inline='always')
def overload_dataframe_columns(df):
    check_runtime_cols_unsupported(df, 'DataFrame.columns')
    beneg__gjlbt = 'def impl(df):\n'
    siwg__rswe = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(
        df.columns)
    beneg__gjlbt += f'  return {siwg__rswe}'
    grcyb__ihbff = {}
    exec(beneg__gjlbt, {'bodo': bodo}, grcyb__ihbff)
    impl = grcyb__ihbff['impl']
    return impl


@overload_attribute(DataFrameType, 'values')
def overload_dataframe_values(df):
    check_runtime_cols_unsupported(df, 'DataFrame.values')
    if not is_df_values_numpy_supported_dftyp(df):
        raise_bodo_error(
            'DataFrame.values: only supported for dataframes containing numeric values'
            )
    vkscu__dblgm = len(df.columns)
    pkxm__ryxdc = set(i for i in range(vkscu__dblgm) if isinstance(df.data[
        i], IntegerArrayType))
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(i, '.astype(float)' if i in pkxm__ryxdc else '') for i in
        range(vkscu__dblgm))
    beneg__gjlbt = 'def f(df):\n'.format()
    beneg__gjlbt += '    return np.stack(({},), 1)\n'.format(data_args)
    grcyb__ihbff = {}
    exec(beneg__gjlbt, {'bodo': bodo, 'np': np}, grcyb__ihbff)
    fxs__gztb = grcyb__ihbff['f']
    return fxs__gztb


@overload_method(DataFrameType, 'to_numpy', inline='always', no_unliteral=True)
def overload_dataframe_to_numpy(df, dtype=None, copy=False, na_value=_no_input
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.to_numpy()')
    if not is_df_values_numpy_supported_dftyp(df):
        raise_bodo_error(
            'DataFrame.to_numpy(): only supported for dataframes containing numeric values'
            )
    gtm__cjmma = {'dtype': dtype, 'na_value': na_value}
    ywtq__cnv = {'dtype': None, 'na_value': _no_input}
    check_unsupported_args('DataFrame.to_numpy', gtm__cjmma, ywtq__cnv,
        package_name='pandas', module_name='DataFrame')

    def impl(df, dtype=None, copy=False, na_value=_no_input):
        return df.values
    return impl


@overload_attribute(DataFrameType, 'ndim', inline='always')
def overload_dataframe_ndim(df):
    return lambda df: 2


@overload_attribute(DataFrameType, 'size')
def overload_dataframe_size(df):
    if df.has_runtime_cols:

        def impl(df):
            t = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            mbrjy__uejph = bodo.hiframes.table.compute_num_runtime_columns(t)
            return mbrjy__uejph * len(t)
        return impl
    ncols = len(df.columns)
    return lambda df: ncols * len(df)


@overload_attribute(DataFrameType, 'shape')
def overload_dataframe_shape(df):
    if df.has_runtime_cols:

        def impl(df):
            t = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            mbrjy__uejph = bodo.hiframes.table.compute_num_runtime_columns(t)
            return len(t), mbrjy__uejph
        return impl
    ncols = len(df.columns)
    return lambda df: (len(df), types.int64(ncols))


@overload_attribute(DataFrameType, 'dtypes')
def overload_dataframe_dtypes(df):
    check_runtime_cols_unsupported(df, 'DataFrame.dtypes')
    beneg__gjlbt = 'def impl(df):\n'
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype\n'
         for i in range(len(df.columns)))
    dbfji__ymmsw = ',' if len(df.columns) == 1 else ''
    index = f'bodo.hiframes.pd_index_ext.init_heter_index({df.columns})'
    beneg__gjlbt += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}{dbfji__ymmsw}), {index}, None)
"""
    grcyb__ihbff = {}
    exec(beneg__gjlbt, {'bodo': bodo}, grcyb__ihbff)
    impl = grcyb__ihbff['impl']
    return impl


@overload_attribute(DataFrameType, 'empty')
def overload_dataframe_empty(df):
    check_runtime_cols_unsupported(df, 'DataFrame.empty')
    if len(df.columns) == 0:
        return lambda df: True
    return lambda df: len(df) == 0


@overload_method(DataFrameType, 'assign', no_unliteral=True)
def overload_dataframe_assign(df, **kwargs):
    check_runtime_cols_unsupported(df, 'DataFrame.assign()')
    raise_bodo_error('Invalid df.assign() call')


@overload_method(DataFrameType, 'insert', no_unliteral=True)
def overload_dataframe_insert(df, loc, column, value, allow_duplicates=False):
    check_runtime_cols_unsupported(df, 'DataFrame.insert()')
    raise_bodo_error('Invalid df.insert() call')


def _get_dtype_str(dtype):
    if isinstance(dtype, types.Function):
        if dtype.key[0] == str:
            return "'str'"
        elif dtype.key[0] == float:
            return 'float'
        elif dtype.key[0] == int:
            return 'int'
        elif dtype.key[0] == bool:
            return 'bool'
        else:
            raise BodoError(f'invalid dtype: {dtype}')
    if isinstance(dtype, types.DTypeSpec):
        dtype = dtype.dtype
    if isinstance(dtype, types.functions.NumberClass):
        return f"'{dtype.key}'"
    if dtype in (bodo.libs.str_arr_ext.string_dtype, pd.StringDtype()):
        return 'str'
    return f"'{dtype}'"


@overload_method(DataFrameType, 'astype', inline='always', no_unliteral=True)
def overload_dataframe_astype(df, dtype, copy=True, errors='raise',
    _bodo_nan_to_str=True):
    check_runtime_cols_unsupported(df, 'DataFrame.astype()')
    gtm__cjmma = {'copy': copy, 'errors': errors}
    ywtq__cnv = {'copy': True, 'errors': 'raise'}
    check_unsupported_args('df.astype', gtm__cjmma, ywtq__cnv, package_name
        ='pandas', module_name='DataFrame')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "DataFrame.astype(): 'dtype' when passed as string must be a constant value"
            )
    if is_overload_constant_dict(dtype) or is_overload_constant_series(dtype):
        jnid__djr = get_overload_constant_dict(dtype
            ) if is_overload_constant_dict(dtype) else dict(
            get_overload_constant_series(dtype))
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {_get_dtype_str(jnid__djr[nxjg__nry])}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             if nxjg__nry in jnid__djr else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for
            i, nxjg__nry in enumerate(df.columns))
    else:
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dtype, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             for i in range(len(df.columns)))
    header = (
        "def impl(df, dtype, copy=True, errors='raise', _bodo_nan_to_str=True):\n"
        )
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'copy', inline='always', no_unliteral=True)
def overload_dataframe_copy(df, deep=True):
    check_runtime_cols_unsupported(df, 'DataFrame.copy()')
    ovh__yoorr = []
    for i in range(len(df.columns)):
        arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
        if is_overload_true(deep):
            ovh__yoorr.append(arr + '.copy()')
        elif is_overload_false(deep):
            ovh__yoorr.append(arr)
        else:
            ovh__yoorr.append(f'{arr}.copy() if deep else {arr}')
    header = 'def impl(df, deep=True):\n'
    return _gen_init_df(header, df.columns, ', '.join(ovh__yoorr))


@overload_method(DataFrameType, 'rename', inline='always', no_unliteral=True)
def overload_dataframe_rename(df, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False, level=None, errors='ignore',
    _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.rename()')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'rename')
    gtm__cjmma = {'index': index, 'level': level, 'errors': errors}
    ywtq__cnv = {'index': None, 'level': None, 'errors': 'ignore'}
    check_unsupported_args('DataFrame.rename', gtm__cjmma, ywtq__cnv,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_constant_bool(inplace):
        raise BodoError(
            "DataFrame.rename(): 'inplace' keyword only supports boolean constant assignment"
            )
    if not is_overload_none(mapper):
        if not is_overload_none(columns):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'mapper' and 'columns'"
                )
        if not (is_overload_constant_int(axis) and get_overload_const_int(
            axis) == 1):
            raise BodoError(
                "DataFrame.rename(): 'mapper' only supported with axis=1")
        if not is_overload_constant_dict(mapper):
            raise_bodo_error(
                "'mapper' argument to DataFrame.rename() should be a constant dictionary"
                )
        owh__zdnc = get_overload_constant_dict(mapper)
    elif not is_overload_none(columns):
        if not is_overload_none(axis):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'axis' and 'columns'")
        if not is_overload_constant_dict(columns):
            raise_bodo_error(
                "'columns' argument to DataFrame.rename() should be a constant dictionary"
                )
        owh__zdnc = get_overload_constant_dict(columns)
    else:
        raise_bodo_error(
            "DataFrame.rename(): must pass columns either via 'mapper' and 'axis'=1 or 'columns'"
            )
    are__taftw = [owh__zdnc.get(df.columns[i], df.columns[i]) for i in
        range(len(df.columns))]
    ovh__yoorr = []
    for i in range(len(df.columns)):
        arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
        if is_overload_true(copy):
            ovh__yoorr.append(arr + '.copy()')
        elif is_overload_false(copy):
            ovh__yoorr.append(arr)
        else:
            ovh__yoorr.append(f'{arr}.copy() if copy else {arr}')
    header = """def impl(df, mapper=None, index=None, columns=None, axis=None, copy=True, inplace=False, level=None, errors='ignore', _bodo_transformed=False):
"""
    return _gen_init_df(header, are__taftw, ', '.join(ovh__yoorr))


@overload_method(DataFrameType, 'filter', no_unliteral=True)
def overload_dataframe_filter(df, items=None, like=None, regex=None, axis=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.filter()')
    hkoe__limgu = not is_overload_none(items)
    bzo__zeawk = not is_overload_none(like)
    nqcu__crvn = not is_overload_none(regex)
    tizic__vukj = hkoe__limgu ^ bzo__zeawk ^ nqcu__crvn
    ivpya__ubrvx = not (hkoe__limgu or bzo__zeawk or nqcu__crvn)
    if ivpya__ubrvx:
        raise BodoError(
            'DataFrame.filter(): one of keyword arguments `items`, `like`, and `regex` must be supplied'
            )
    if not tizic__vukj:
        raise BodoError(
            'DataFrame.filter(): keyword arguments `items`, `like`, and `regex` are mutually exclusive'
            )
    if is_overload_none(axis):
        axis = 'columns'
    if is_overload_constant_str(axis):
        axis = get_overload_const_str(axis)
        if axis not in {'index', 'columns'}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either "index" or "columns" if string'
                )
        rio__fuoun = 0 if axis == 'index' else 1
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
        if axis not in {0, 1}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either 0 or 1 if integer'
                )
        rio__fuoun = axis
    else:
        raise_bodo_error(
            'DataFrame.filter(): keyword arguments `axis` must be constant string or integer'
            )
    assert rio__fuoun in {0, 1}
    beneg__gjlbt = (
        'def impl(df, items=None, like=None, regex=None, axis=None):\n')
    if rio__fuoun == 0:
        raise BodoError(
            'DataFrame.filter(): filtering based on index is not supported.')
    if rio__fuoun == 1:
        gbwzp__ouvj = []
        otziu__jyfx = []
        efqav__qkspa = []
        if hkoe__limgu:
            if is_overload_constant_list(items):
                dubn__esvqr = get_overload_const_list(items)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'items' must be a list of constant strings."
                    )
        if bzo__zeawk:
            if is_overload_constant_str(like):
                yykwb__rjtem = get_overload_const_str(like)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'like' must be a constant string."
                    )
        if nqcu__crvn:
            if is_overload_constant_str(regex):
                whfj__umcd = get_overload_const_str(regex)
                nic__ujkc = re.compile(whfj__umcd)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'regex' must be a constant string."
                    )
        for i, nxjg__nry in enumerate(df.columns):
            if not is_overload_none(items
                ) and nxjg__nry in dubn__esvqr or not is_overload_none(like
                ) and yykwb__rjtem in str(nxjg__nry) or not is_overload_none(
                regex) and nic__ujkc.search(str(nxjg__nry)):
                otziu__jyfx.append(nxjg__nry)
                efqav__qkspa.append(i)
        for i in efqav__qkspa:
            kmdfv__fvje = f'data_{i}'
            gbwzp__ouvj.append(kmdfv__fvje)
            beneg__gjlbt += f"""  {kmdfv__fvje} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})
"""
        data_args = ', '.join(gbwzp__ouvj)
        return _gen_init_df(beneg__gjlbt, otziu__jyfx, data_args)


@overload_method(DataFrameType, 'isna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'isnull', inline='always', no_unliteral=True)
def overload_dataframe_isna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.isna()')
    data_args = ', '.join(
        f'bodo.libs.array_ops.array_op_isna(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
         for i in range(len(df.columns)))
    header = 'def impl(df):\n'
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'select_dtypes', inline='always',
    no_unliteral=True)
def overload_dataframe_select_dtypes(df, include=None, exclude=None):
    check_runtime_cols_unsupported(df, 'DataFrame.select_dtypes')
    qcwx__old = is_overload_none(include)
    cri__vyqa = is_overload_none(exclude)
    qbbw__iios = 'DataFrame.select_dtypes'
    if qcwx__old and cri__vyqa:
        raise_bodo_error(
            'DataFrame.select_dtypes() At least one of include or exclude must not be none'
            )

    def is_legal_input(elem):
        return is_overload_constant_str(elem) or isinstance(elem, types.
            DTypeSpec) or isinstance(elem, types.Function)
    if not qcwx__old:
        if is_overload_constant_list(include):
            include = get_overload_const_list(include)
            afsq__lifcg = [dtype_to_array_type(parse_dtype(elem, qbbw__iios
                )) for elem in include]
        elif is_legal_input(include):
            afsq__lifcg = [dtype_to_array_type(parse_dtype(include,
                qbbw__iios))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        afsq__lifcg = get_nullable_and_non_nullable_types(afsq__lifcg)
        weio__fovhf = tuple(nxjg__nry for i, nxjg__nry in enumerate(df.
            columns) if df.data[i] in afsq__lifcg)
    else:
        weio__fovhf = df.columns
    if not cri__vyqa:
        if is_overload_constant_list(exclude):
            exclude = get_overload_const_list(exclude)
            voxe__bkbt = [dtype_to_array_type(parse_dtype(elem, qbbw__iios)
                ) for elem in exclude]
        elif is_legal_input(exclude):
            voxe__bkbt = [dtype_to_array_type(parse_dtype(exclude, qbbw__iios))
                ]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        voxe__bkbt = get_nullable_and_non_nullable_types(voxe__bkbt)
        weio__fovhf = tuple(nxjg__nry for nxjg__nry in weio__fovhf if df.
            data[df.columns.index(nxjg__nry)] not in voxe__bkbt)
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(nxjg__nry)})'
         for nxjg__nry in weio__fovhf)
    header = 'def impl(df, include=None, exclude=None):\n'
    return _gen_init_df(header, weio__fovhf, data_args)


@overload_method(DataFrameType, 'notna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'notnull', inline='always', no_unliteral=True)
def overload_dataframe_notna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.notna()')
    data_args = ', '.join(
        f'bodo.libs.array_ops.array_op_isna(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})) == False'
         for i in range(len(df.columns)))
    header = 'def impl(df):\n'
    return _gen_init_df(header, df.columns, data_args)


def overload_dataframe_head(df, n=5):
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[:n]' for
        i in range(len(df.columns)))
    header = 'def impl(df, n=5):\n'
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[:n]'
    return _gen_init_df(header, df.columns, data_args, index)


@lower_builtin('df.head', DataFrameType, types.Integer)
@lower_builtin('df.head', DataFrameType, types.Omitted)
def dataframe_head_lower(context, builder, sig, args):
    impl = overload_dataframe_head(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'tail', inline='always', no_unliteral=True)
def overload_dataframe_tail(df, n=5):
    check_runtime_cols_unsupported(df, 'DataFrame.tail()')
    if not is_overload_int(n):
        raise BodoError("Dataframe.tail(): 'n' must be an Integer")
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[m:]' for
        i in range(len(df.columns)))
    header = 'def impl(df, n=5):\n'
    header += '  m = bodo.hiframes.series_impl.tail_slice(len(df), n)\n'
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[m:]'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'first', inline='always', no_unliteral=True)
def overload_dataframe_first(df, offset):
    check_runtime_cols_unsupported(df, 'DataFrame.first()')
    ldp__ayyob = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in ldp__ayyob:
        raise BodoError(
            "DataFrame.first(): 'offset' must be an string or DateOffset")
    index = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[:valid_entries]'
        )
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[:valid_entries]'
         for i in range(len(df.columns)))
    header = 'def impl(df, offset):\n'
    header += (
        '  df_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
        )
    header += '  if len(df_index):\n'
    header += '    start_date = df_index[0]\n'
    header += """    valid_entries = bodo.libs.array_kernels.get_valid_entries_from_date_offset(df_index, offset, start_date, False)
"""
    header += '  else:\n'
    header += '    valid_entries = 0\n'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'last', inline='always', no_unliteral=True)
def overload_dataframe_last(df, offset):
    check_runtime_cols_unsupported(df, 'DataFrame.last()')
    ldp__ayyob = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in ldp__ayyob:
        raise BodoError(
            "DataFrame.last(): 'offset' must be an string or DateOffset")
    index = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[len(df)-valid_entries:]'
        )
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[len(df)-valid_entries:]'
         for i in range(len(df.columns)))
    header = 'def impl(df, offset):\n'
    header += (
        '  df_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
        )
    header += '  if len(df_index):\n'
    header += '    final_date = df_index[-1]\n'
    header += """    valid_entries = bodo.libs.array_kernels.get_valid_entries_from_date_offset(df_index, offset, final_date, True)
"""
    header += '  else:\n'
    header += '    valid_entries = 0\n'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'to_string', no_unliteral=True)
def to_string_overload(df, buf=None, columns=None, col_space=None, header=
    True, index=True, na_rep='NaN', formatters=None, float_format=None,
    sparsify=None, index_names=True, justify=None, max_rows=None, min_rows=
    None, max_cols=None, show_dimensions=False, decimal='.', line_width=
    None, max_colwidth=None, encoding=None):
    check_runtime_cols_unsupported(df, 'DataFrame.to_string()')

    def impl(df, buf=None, columns=None, col_space=None, header=True, index
        =True, na_rep='NaN', formatters=None, float_format=None, sparsify=
        None, index_names=True, justify=None, max_rows=None, min_rows=None,
        max_cols=None, show_dimensions=False, decimal='.', line_width=None,
        max_colwidth=None, encoding=None):
        with numba.objmode(res='string'):
            res = df.to_string(buf=buf, columns=columns, col_space=
                col_space, header=header, index=index, na_rep=na_rep,
                formatters=formatters, float_format=float_format, sparsify=
                sparsify, index_names=index_names, justify=justify,
                max_rows=max_rows, min_rows=min_rows, max_cols=max_cols,
                show_dimensions=show_dimensions, decimal=decimal,
                line_width=line_width, max_colwidth=max_colwidth, encoding=
                encoding)
        return res
    return impl


@overload_method(DataFrameType, 'isin', inline='always', no_unliteral=True)
def overload_dataframe_isin(df, values):
    check_runtime_cols_unsupported(df, 'DataFrame.isin()')
    from bodo.utils.typing import is_iterable_type
    beneg__gjlbt = 'def impl(df, values):\n'
    ragzn__myh = {}
    kdqi__dozab = False
    if isinstance(values, DataFrameType):
        kdqi__dozab = True
        for i, nxjg__nry in enumerate(df.columns):
            if nxjg__nry in values.columns:
                rztw__ijtf = 'val{}'.format(i)
                beneg__gjlbt += (
                    """  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(values, {})
"""
                    .format(rztw__ijtf, values.columns.index(nxjg__nry)))
                ragzn__myh[nxjg__nry] = rztw__ijtf
    elif is_iterable_type(values) and not isinstance(values, SeriesType):
        ragzn__myh = {nxjg__nry: 'values' for nxjg__nry in df.columns}
    else:
        raise_bodo_error(f'pd.isin(): not supported for type {values}')
    data = []
    for i in range(len(df.columns)):
        rztw__ijtf = 'data{}'.format(i)
        beneg__gjlbt += (
            '  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})\n'
            .format(rztw__ijtf, i))
        data.append(rztw__ijtf)
    vzrxm__tnpf = ['out{}'.format(i) for i in range(len(df.columns))]
    oxv__malwt = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  m = len({1})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] == {1}[i] if i < m else False
"""
    zox__uibh = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] in {1}
"""
    atai__kmrp = '  {} = np.zeros(len(df), np.bool_)\n'
    for i, (cname, ibr__furwt) in enumerate(zip(df.columns, data)):
        if cname in ragzn__myh:
            ryoxp__tajr = ragzn__myh[cname]
            if kdqi__dozab:
                beneg__gjlbt += oxv__malwt.format(ibr__furwt, ryoxp__tajr,
                    vzrxm__tnpf[i])
            else:
                beneg__gjlbt += zox__uibh.format(ibr__furwt, ryoxp__tajr,
                    vzrxm__tnpf[i])
        else:
            beneg__gjlbt += atai__kmrp.format(vzrxm__tnpf[i])
    return _gen_init_df(beneg__gjlbt, df.columns, ','.join(vzrxm__tnpf))


@overload_method(DataFrameType, 'abs', inline='always', no_unliteral=True)
def overload_dataframe_abs(df):
    check_runtime_cols_unsupported(df, 'DataFrame.abs()')
    for arr_typ in df.data:
        if not (isinstance(arr_typ.dtype, types.Number) or arr_typ.dtype ==
            bodo.timedelta64ns):
            raise_bodo_error(
                f'DataFrame.abs(): Only supported for numeric and Timedelta. Encountered array with dtype {arr_typ.dtype}'
                )
    vkscu__dblgm = len(df.columns)
    data_args = ', '.join(
        'np.abs(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
        .format(i) for i in range(vkscu__dblgm))
    header = 'def impl(df):\n'
    return _gen_init_df(header, df.columns, data_args)


def overload_dataframe_corr(df, method='pearson', min_periods=1):
    tjfhs__suavs = [nxjg__nry for nxjg__nry, cyp__belq in zip(df.columns,
        df.data) if bodo.utils.typing._is_pandas_numeric_dtype(cyp__belq.dtype)
        ]
    assert len(tjfhs__suavs) != 0
    yiff__upx = ''
    if not any(cyp__belq == types.float64 for cyp__belq in df.data):
        yiff__upx = '.astype(np.float64)'
    ruefl__mitsb = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.columns.index(nxjg__nry), '.astype(np.float64)' if 
        isinstance(df.data[df.columns.index(nxjg__nry)], IntegerArrayType) or
        df.data[df.columns.index(nxjg__nry)] == boolean_array else '') for
        nxjg__nry in tjfhs__suavs)
    xzx__yzo = 'np.stack(({},), 1){}'.format(ruefl__mitsb, yiff__upx)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(
        tjfhs__suavs)))
    index = f'{generate_col_to_index_func_text(tjfhs__suavs)}\n'
    header = "def impl(df, method='pearson', min_periods=1):\n"
    header += '  mat = {}\n'.format(xzx__yzo)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 0, min_periods)\n'
    return _gen_init_df(header, tjfhs__suavs, data_args, index)


@lower_builtin('df.corr', DataFrameType, types.VarArg(types.Any))
def dataframe_corr_lower(context, builder, sig, args):
    impl = overload_dataframe_corr(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'cov', inline='always', no_unliteral=True)
def overload_dataframe_cov(df, min_periods=None, ddof=1):
    check_runtime_cols_unsupported(df, 'DataFrame.cov()')
    lbci__ctjt = dict(ddof=ddof)
    runxq__egz = dict(ddof=1)
    check_unsupported_args('DataFrame.cov', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    bdh__rbtne = '1' if is_overload_none(min_periods) else 'min_periods'
    tjfhs__suavs = [nxjg__nry for nxjg__nry, cyp__belq in zip(df.columns,
        df.data) if bodo.utils.typing._is_pandas_numeric_dtype(cyp__belq.dtype)
        ]
    if len(tjfhs__suavs) == 0:
        raise_bodo_error('DataFrame.cov(): requires non-empty dataframe')
    yiff__upx = ''
    if not any(cyp__belq == types.float64 for cyp__belq in df.data):
        yiff__upx = '.astype(np.float64)'
    ruefl__mitsb = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.columns.index(nxjg__nry), '.astype(np.float64)' if 
        isinstance(df.data[df.columns.index(nxjg__nry)], IntegerArrayType) or
        df.data[df.columns.index(nxjg__nry)] == boolean_array else '') for
        nxjg__nry in tjfhs__suavs)
    xzx__yzo = 'np.stack(({},), 1){}'.format(ruefl__mitsb, yiff__upx)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(
        tjfhs__suavs)))
    index = f'pd.Index({tjfhs__suavs})\n'
    header = 'def impl(df, min_periods=None, ddof=1):\n'
    header += '  mat = {}\n'.format(xzx__yzo)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 1, {})\n'.format(
        bdh__rbtne)
    return _gen_init_df(header, tjfhs__suavs, data_args, index)


@overload_method(DataFrameType, 'count', inline='always', no_unliteral=True)
def overload_dataframe_count(df, axis=0, level=None, numeric_only=False):
    check_runtime_cols_unsupported(df, 'DataFrame.count()')
    lbci__ctjt = dict(axis=axis, level=level, numeric_only=numeric_only)
    runxq__egz = dict(axis=0, level=None, numeric_only=False)
    check_unsupported_args('DataFrame.count', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
         for i in range(len(df.columns)))
    beneg__gjlbt = 'def impl(df, axis=0, level=None, numeric_only=False):\n'
    beneg__gjlbt += '  data = np.array([{}])\n'.format(data_args)
    siwg__rswe = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(
        df.columns)
    beneg__gjlbt += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {siwg__rswe})\n'
        )
    grcyb__ihbff = {}
    exec(beneg__gjlbt, {'bodo': bodo, 'np': np}, grcyb__ihbff)
    impl = grcyb__ihbff['impl']
    return impl


@overload_method(DataFrameType, 'nunique', inline='always', no_unliteral=True)
def overload_dataframe_nunique(df, axis=0, dropna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.unique()')
    lbci__ctjt = dict(axis=axis)
    runxq__egz = dict(axis=0)
    if not is_overload_bool(dropna):
        raise BodoError('DataFrame.nunique: dropna must be a boolean value')
    check_unsupported_args('DataFrame.nunique', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_kernels.nunique(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dropna)'
         for i in range(len(df.columns)))
    beneg__gjlbt = 'def impl(df, axis=0, dropna=True):\n'
    beneg__gjlbt += '  data = np.asarray(({},))\n'.format(data_args)
    siwg__rswe = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(
        df.columns)
    beneg__gjlbt += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {siwg__rswe})\n'
        )
    grcyb__ihbff = {}
    exec(beneg__gjlbt, {'bodo': bodo, 'np': np}, grcyb__ihbff)
    impl = grcyb__ihbff['impl']
    return impl


@overload_method(DataFrameType, 'prod', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'product', inline='always', no_unliteral=True)
def overload_dataframe_prod(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.prod()')
    lbci__ctjt = dict(skipna=skipna, level=level, numeric_only=numeric_only,
        min_count=min_count)
    runxq__egz = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.prod', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    return _gen_reduce_impl(df, 'prod', axis=axis)


@overload_method(DataFrameType, 'sum', inline='always', no_unliteral=True)
def overload_dataframe_sum(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.sum()')
    lbci__ctjt = dict(skipna=skipna, level=level, numeric_only=numeric_only,
        min_count=min_count)
    runxq__egz = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.sum', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    return _gen_reduce_impl(df, 'sum', axis=axis)


@overload_method(DataFrameType, 'max', inline='always', no_unliteral=True)
def overload_dataframe_max(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.max()')
    lbci__ctjt = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    runxq__egz = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.max', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    return _gen_reduce_impl(df, 'max', axis=axis)


@overload_method(DataFrameType, 'min', inline='always', no_unliteral=True)
def overload_dataframe_min(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.min()')
    lbci__ctjt = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    runxq__egz = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.min', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    return _gen_reduce_impl(df, 'min', axis=axis)


@overload_method(DataFrameType, 'mean', inline='always', no_unliteral=True)
def overload_dataframe_mean(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.mean()')
    lbci__ctjt = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    runxq__egz = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.mean', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    return _gen_reduce_impl(df, 'mean', axis=axis)


@overload_method(DataFrameType, 'var', inline='always', no_unliteral=True)
def overload_dataframe_var(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.var()')
    lbci__ctjt = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    runxq__egz = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.var', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    return _gen_reduce_impl(df, 'var', axis=axis)


@overload_method(DataFrameType, 'std', inline='always', no_unliteral=True)
def overload_dataframe_std(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.std()')
    lbci__ctjt = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    runxq__egz = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.std', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    return _gen_reduce_impl(df, 'std', axis=axis)


@overload_method(DataFrameType, 'median', inline='always', no_unliteral=True)
def overload_dataframe_median(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.median()')
    lbci__ctjt = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    runxq__egz = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.median', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    return _gen_reduce_impl(df, 'median', axis=axis)


@overload_method(DataFrameType, 'quantile', inline='always', no_unliteral=True)
def overload_dataframe_quantile(df, q=0.5, axis=0, numeric_only=True,
    interpolation='linear'):
    check_runtime_cols_unsupported(df, 'DataFrame.quantile()')
    lbci__ctjt = dict(numeric_only=numeric_only, interpolation=interpolation)
    runxq__egz = dict(numeric_only=True, interpolation='linear')
    check_unsupported_args('DataFrame.quantile', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    return _gen_reduce_impl(df, 'quantile', 'q', axis=axis)


@overload_method(DataFrameType, 'idxmax', inline='always', no_unliteral=True)
def overload_dataframe_idxmax(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmax()')
    lbci__ctjt = dict(axis=axis, skipna=skipna)
    runxq__egz = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmax', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    for fbztr__ofst in df.data:
        if not (bodo.utils.utils.is_np_array_typ(fbztr__ofst) and (
            fbztr__ofst.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(fbztr__ofst.dtype, (types.Number, types.Boolean))) or
            isinstance(fbztr__ofst, (bodo.IntegerArrayType, bodo.
            CategoricalArrayType)) or fbztr__ofst in [bodo.boolean_array,
            bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmax() only supported for numeric column types. Column type: {fbztr__ofst} not supported.'
                )
        if isinstance(fbztr__ofst, bodo.CategoricalArrayType
            ) and not fbztr__ofst.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmax(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmax', axis=axis)


@overload_method(DataFrameType, 'idxmin', inline='always', no_unliteral=True)
def overload_dataframe_idxmin(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmin()')
    lbci__ctjt = dict(axis=axis, skipna=skipna)
    runxq__egz = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmin', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    for fbztr__ofst in df.data:
        if not (bodo.utils.utils.is_np_array_typ(fbztr__ofst) and (
            fbztr__ofst.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(fbztr__ofst.dtype, (types.Number, types.Boolean))) or
            isinstance(fbztr__ofst, (bodo.IntegerArrayType, bodo.
            CategoricalArrayType)) or fbztr__ofst in [bodo.boolean_array,
            bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmin() only supported for numeric column types. Column type: {fbztr__ofst} not supported.'
                )
        if isinstance(fbztr__ofst, bodo.CategoricalArrayType
            ) and not fbztr__ofst.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmin(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmin', axis=axis)


@overload_method(DataFrameType, 'infer_objects', inline='always')
def overload_dataframe_infer_objects(df):
    check_runtime_cols_unsupported(df, 'DataFrame.infer_objects()')
    return lambda df: df.copy()


def _gen_reduce_impl(df, func_name, args=None, axis=None):
    args = '' if is_overload_none(args) else args
    if is_overload_none(axis):
        axis = 0
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
    else:
        raise_bodo_error(
            f'DataFrame.{func_name}: axis must be a constant Integer')
    assert axis in (0, 1), f'invalid axis argument for DataFrame.{func_name}'
    if func_name in ('idxmax', 'idxmin'):
        out_colnames = df.columns
    else:
        tjfhs__suavs = tuple(nxjg__nry for nxjg__nry, cyp__belq in zip(df.
            columns, df.data) if bodo.utils.typing._is_pandas_numeric_dtype
            (cyp__belq.dtype))
        out_colnames = tjfhs__suavs
    assert len(out_colnames) != 0
    try:
        if func_name in ('idxmax', 'idxmin') and axis == 0:
            comm_dtype = None
        else:
            oels__qth = [numba.np.numpy_support.as_dtype(df.data[df.columns
                .index(nxjg__nry)].dtype) for nxjg__nry in out_colnames]
            comm_dtype = numba.np.numpy_support.from_dtype(np.
                find_common_type(oels__qth, []))
    except NotImplementedError as htwzd__qyxv:
        raise BodoError(
            f'Dataframe.{func_name}() with column types: {df.data} could not be merged to a common type.'
            )
    rgtp__hoap = ''
    if func_name in ('sum', 'prod'):
        rgtp__hoap = ', min_count=0'
    ddof = ''
    if func_name in ('var', 'std'):
        ddof = 'ddof=1, '
    beneg__gjlbt = (
        'def impl(df, axis=None, skipna=None, level=None,{} numeric_only=None{}):\n'
        .format(ddof, rgtp__hoap))
    if func_name == 'quantile':
        beneg__gjlbt = (
            "def impl(df, q=0.5, axis=0, numeric_only=True, interpolation='linear'):\n"
            )
    if func_name in ('idxmax', 'idxmin'):
        beneg__gjlbt = 'def impl(df, axis=0, skipna=True):\n'
    if axis == 0:
        beneg__gjlbt += _gen_reduce_impl_axis0(df, func_name, out_colnames,
            comm_dtype, args)
    else:
        beneg__gjlbt += _gen_reduce_impl_axis1(func_name, out_colnames,
            comm_dtype, df)
    grcyb__ihbff = {}
    exec(beneg__gjlbt, {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba},
        grcyb__ihbff)
    impl = grcyb__ihbff['impl']
    return impl


def _gen_reduce_impl_axis0(df, func_name, out_colnames, comm_dtype, args):
    owofw__pqimo = ''
    if func_name in ('min', 'max'):
        owofw__pqimo = ', dtype=np.{}'.format(comm_dtype)
    if comm_dtype == types.float32 and func_name in ('sum', 'prod', 'mean',
        'var', 'std', 'median'):
        owofw__pqimo = ', dtype=np.float32'
    pvc__wxgm = f'bodo.libs.array_ops.array_op_{func_name}'
    tjeb__fpbty = ''
    if func_name in ['sum', 'prod']:
        tjeb__fpbty = 'True, min_count'
    elif func_name in ['idxmax', 'idxmin']:
        tjeb__fpbty = 'index'
    elif func_name == 'quantile':
        tjeb__fpbty = 'q'
    elif func_name in ['std', 'var']:
        tjeb__fpbty = 'True, ddof'
    elif func_name == 'median':
        tjeb__fpbty = 'True'
    data_args = ', '.join(
        f'{pvc__wxgm}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(nxjg__nry)}), {tjeb__fpbty})'
         for nxjg__nry in out_colnames)
    beneg__gjlbt = ''
    if func_name in ('idxmax', 'idxmin'):
        beneg__gjlbt += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        beneg__gjlbt += (
            '  data = bodo.utils.conversion.coerce_to_array(({},))\n'.
            format(data_args))
    else:
        beneg__gjlbt += '  data = np.asarray(({},){})\n'.format(data_args,
            owofw__pqimo)
    beneg__gjlbt += f"""  return bodo.hiframes.pd_series_ext.init_series(data, pd.Index({out_colnames}))
"""
    return beneg__gjlbt


def _gen_reduce_impl_axis1(func_name, out_colnames, comm_dtype, df_type):
    ydn__vlczt = [df_type.columns.index(nxjg__nry) for nxjg__nry in
        out_colnames]
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    data_args = '\n    '.join(
        'arr_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
        .format(i) for i in ydn__vlczt)
    ssa__tdq = '\n        '.join(f'row[{i}] = arr_{ydn__vlczt[i]}[i]' for i in
        range(len(out_colnames)))
    assert len(data_args) > 0, f'empty dataframe in DataFrame.{func_name}()'
    dra__dzpb = f'len(arr_{ydn__vlczt[0]})'
    lxlmq__dot = {'max': 'np.nanmax', 'min': 'np.nanmin', 'sum':
        'np.nansum', 'prod': 'np.nanprod', 'mean': 'np.nanmean', 'median':
        'np.nanmedian', 'var': 'bodo.utils.utils.nanvar_ddof1', 'std':
        'bodo.utils.utils.nanstd_ddof1'}
    if func_name in lxlmq__dot:
        spij__tyiok = lxlmq__dot[func_name]
        gac__vegia = 'float64' if func_name in ['mean', 'median', 'std', 'var'
            ] else comm_dtype
        beneg__gjlbt = f"""
    {data_args}
    numba.parfors.parfor.init_prange()
    n = {dra__dzpb}
    row = np.empty({len(out_colnames)}, np.{comm_dtype})
    A = np.empty(n, np.{gac__vegia})
    for i in numba.parfors.parfor.internal_prange(n):
        {ssa__tdq}
        A[i] = {spij__tyiok}(row)
    return bodo.hiframes.pd_series_ext.init_series(A, {index})
"""
        return beneg__gjlbt
    else:
        raise BodoError(f'DataFrame.{func_name}(): Not supported for axis=1')


@overload_method(DataFrameType, 'pct_change', inline='always', no_unliteral
    =True)
def overload_dataframe_pct_change(df, periods=1, fill_method='pad', limit=
    None, freq=None):
    check_runtime_cols_unsupported(df, 'DataFrame.pct_change()')
    lbci__ctjt = dict(fill_method=fill_method, limit=limit, freq=freq)
    runxq__egz = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('DataFrame.pct_change', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.hiframes.rolling.pct_change(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), periods, False)'
         for i in range(len(df.columns)))
    header = (
        "def impl(df, periods=1, fill_method='pad', limit=None, freq=None):\n")
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'cumprod', inline='always', no_unliteral=True)
def overload_dataframe_cumprod(df, axis=None, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.cumprod()')
    lbci__ctjt = dict(axis=axis, skipna=skipna)
    runxq__egz = dict(axis=None, skipna=True)
    check_unsupported_args('DataFrame.cumprod', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).cumprod()'
         for i in range(len(df.columns)))
    header = 'def impl(df, axis=None, skipna=True):\n'
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'cumsum', inline='always', no_unliteral=True)
def overload_dataframe_cumsum(df, axis=None, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.cumsum()')
    lbci__ctjt = dict(skipna=skipna)
    runxq__egz = dict(skipna=True)
    check_unsupported_args('DataFrame.cumsum', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).cumsum()'
         for i in range(len(df.columns)))
    header = 'def impl(df, axis=None, skipna=True):\n'
    return _gen_init_df(header, df.columns, data_args)


def _is_describe_type(data):
    return isinstance(data, IntegerArrayType) or isinstance(data, types.Array
        ) and isinstance(data.dtype, types.Number
        ) or data.dtype == bodo.datetime64ns


@overload_method(DataFrameType, 'describe', inline='always', no_unliteral=True)
def overload_dataframe_describe(df, percentiles=None, include=None, exclude
    =None, datetime_is_numeric=True):
    check_runtime_cols_unsupported(df, 'DataFrame.describe()')
    lbci__ctjt = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    runxq__egz = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('DataFrame.describe', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    tjfhs__suavs = [nxjg__nry for nxjg__nry, cyp__belq in zip(df.columns,
        df.data) if _is_describe_type(cyp__belq)]
    if len(tjfhs__suavs) == 0:
        raise BodoError('df.describe() only supports numeric columns')
    ardpb__hnjlb = sum(df.data[df.columns.index(nxjg__nry)].dtype == bodo.
        datetime64ns for nxjg__nry in tjfhs__suavs)

    def _get_describe(col_ind):
        ybse__ciq = df.data[col_ind].dtype == bodo.datetime64ns
        if ardpb__hnjlb and ardpb__hnjlb != len(tjfhs__suavs):
            if ybse__ciq:
                return f'des_{col_ind} + (np.nan,)'
            return (
                f'des_{col_ind}[:2] + des_{col_ind}[3:] + (des_{col_ind}[2],)')
        return f'des_{col_ind}'
    header = """def impl(df, percentiles=None, include=None, exclude=None, datetime_is_numeric=True):
"""
    for nxjg__nry in tjfhs__suavs:
        col_ind = df.columns.index(nxjg__nry)
        header += f"""  des_{col_ind} = bodo.libs.array_ops.array_op_describe(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {col_ind}))
"""
    data_args = ', '.join(_get_describe(df.columns.index(nxjg__nry)) for
        nxjg__nry in tjfhs__suavs)
    nlwdq__zeit = "['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']"
    if ardpb__hnjlb == len(tjfhs__suavs):
        nlwdq__zeit = "['count', 'mean', 'min', '25%', '50%', '75%', 'max']"
    elif ardpb__hnjlb:
        nlwdq__zeit = (
            "['count', 'mean', 'min', '25%', '50%', '75%', 'max', 'std']")
    index = f'bodo.utils.conversion.convert_to_index({nlwdq__zeit})'
    return _gen_init_df(header, tjfhs__suavs, data_args, index)


@overload_method(DataFrameType, 'take', inline='always', no_unliteral=True)
def overload_dataframe_take(df, indices, axis=0, convert=None, is_copy=True):
    check_runtime_cols_unsupported(df, 'DataFrame.take()')
    lbci__ctjt = dict(axis=axis, convert=convert, is_copy=is_copy)
    runxq__egz = dict(axis=0, convert=None, is_copy=True)
    check_unsupported_args('DataFrame.take', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[indices_t]'
        .format(i) for i in range(len(df.columns)))
    header = 'def impl(df, indices, axis=0, convert=None, is_copy=True):\n'
    header += (
        '  indices_t = bodo.utils.conversion.coerce_to_ndarray(indices)\n')
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[indices_t]'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'shift', inline='always', no_unliteral=True)
def overload_dataframe_shift(df, periods=1, freq=None, axis=0, fill_value=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.shift()')
    lbci__ctjt = dict(freq=freq, axis=axis, fill_value=fill_value)
    runxq__egz = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('DataFrame.shift', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    for hckj__iomg in df.data:
        if not is_supported_shift_array_type(hckj__iomg):
            raise BodoError(
                f'Dataframe.shift() column input type {hckj__iomg.dtype} not supported yet.'
                )
    if not is_overload_int(periods):
        raise BodoError(
            "DataFrame.shift(): 'periods' input must be an integer.")
    data_args = ', '.join(
        f'bodo.hiframes.rolling.shift(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), periods, False)'
         for i in range(len(df.columns)))
    header = 'def impl(df, periods=1, freq=None, axis=0, fill_value=None):\n'
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'diff', inline='always', no_unliteral=True)
def overload_dataframe_diff(df, periods=1, axis=0):
    check_runtime_cols_unsupported(df, 'DataFrame.diff()')
    lbci__ctjt = dict(axis=axis)
    runxq__egz = dict(axis=0)
    check_unsupported_args('DataFrame.diff', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    for hckj__iomg in df.data:
        if not (isinstance(hckj__iomg, types.Array) and (isinstance(
            hckj__iomg.dtype, types.Number) or hckj__iomg.dtype == bodo.
            datetime64ns)):
            raise BodoError(
                f'DataFrame.diff() column input type {hckj__iomg.dtype} not supported.'
                )
    if not is_overload_int(periods):
        raise BodoError("DataFrame.diff(): 'periods' input must be an integer."
            )
    header = 'def impl(df, periods=1, axis= 0):\n'
    for i in range(len(df.columns)):
        header += (
            f'  data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})\n'
            )
    data_args = ', '.join(
        f'bodo.hiframes.series_impl.dt64_arr_sub(data_{i}, bodo.hiframes.rolling.shift(data_{i}, periods, False))'
         if df.data[i] == types.Array(bodo.datetime64ns, 1, 'C') else
        f'data_{i} - bodo.hiframes.rolling.shift(data_{i}, periods, False)' for
        i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'set_index', inline='always', no_unliteral=True
    )
def overload_dataframe_set_index(df, keys, drop=True, append=False, inplace
    =False, verify_integrity=False):
    check_runtime_cols_unsupported(df, 'DataFrame.set_index()')
    gtm__cjmma = {'inplace': inplace, 'append': append, 'verify_integrity':
        verify_integrity}
    ywtq__cnv = {'inplace': False, 'append': False, 'verify_integrity': False}
    check_unsupported_args('DataFrame.set_index', gtm__cjmma, ywtq__cnv,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_constant_str(keys):
        raise_bodo_error(
            "DataFrame.set_index(): 'keys' must be a constant string")
    col_name = get_overload_const_str(keys)
    col_ind = df.columns.index(col_name)
    if len(df.columns) == 1:
        raise BodoError(
            'DataFrame.set_index(): Not supported on single column DataFrames.'
            )
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'.format(
        i) for i in range(len(df.columns)) if i != col_ind)
    header = """def impl(df, keys, drop=True, append=False, inplace=False, verify_integrity=False):
"""
    columns = tuple(nxjg__nry for nxjg__nry in df.columns if nxjg__nry !=
        col_name)
    index = (
        'bodo.utils.conversion.index_from_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}), {})'
        .format(col_ind, f"'{col_name}'" if isinstance(col_name, str) else
        col_name))
    return _gen_init_df(header, columns, data_args, index)


@overload_method(DataFrameType, 'query', no_unliteral=True)
def overload_dataframe_query(df, expr, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.query()')
    gtm__cjmma = {'inplace': inplace}
    ywtq__cnv = {'inplace': False}
    check_unsupported_args('query', gtm__cjmma, ywtq__cnv, package_name=
        'pandas', module_name='DataFrame')
    if not isinstance(expr, (types.StringLiteral, types.UnicodeType)):
        raise BodoError('query(): expr argument should be a string')

    def impl(df, expr, inplace=False):
        khwjb__fsoxw = bodo.hiframes.pd_dataframe_ext.query_dummy(df, expr)
        return df[khwjb__fsoxw]
    return impl


@overload_method(DataFrameType, 'duplicated', inline='always', no_unliteral
    =True)
def overload_dataframe_duplicated(df, subset=None, keep='first'):
    check_runtime_cols_unsupported(df, 'DataFrame.duplicated()')
    gtm__cjmma = {'subset': subset, 'keep': keep}
    ywtq__cnv = {'subset': None, 'keep': 'first'}
    check_unsupported_args('DataFrame.duplicated', gtm__cjmma, ywtq__cnv,
        package_name='pandas', module_name='DataFrame')
    vkscu__dblgm = len(df.columns)
    beneg__gjlbt = "def impl(df, subset=None, keep='first'):\n"
    for i in range(vkscu__dblgm):
        beneg__gjlbt += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    beneg__gjlbt += (
        '  duplicated, index_arr = bodo.libs.array_kernels.duplicated(({},), {})\n'
        .format(', '.join('data_{}'.format(i) for i in range(vkscu__dblgm)),
        index))
    beneg__gjlbt += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    beneg__gjlbt += (
        '  return bodo.hiframes.pd_series_ext.init_series(duplicated, index)\n'
        )
    grcyb__ihbff = {}
    exec(beneg__gjlbt, {'bodo': bodo}, grcyb__ihbff)
    impl = grcyb__ihbff['impl']
    return impl


@overload_method(DataFrameType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_dataframe_drop_duplicates(df, subset=None, keep='first',
    inplace=False, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop_duplicates()')
    gtm__cjmma = {'keep': keep, 'inplace': inplace, 'ignore_index':
        ignore_index}
    ywtq__cnv = {'keep': 'first', 'inplace': False, 'ignore_index': False}
    kuqwp__mqb = []
    if is_overload_constant_list(subset):
        kuqwp__mqb = get_overload_const_list(subset)
    elif is_overload_constant_str(subset):
        kuqwp__mqb = [get_overload_const_str(subset)]
    elif is_overload_constant_int(subset):
        kuqwp__mqb = [get_overload_const_int(subset)]
    elif not is_overload_none(subset):
        raise_bodo_error(
            'DataFrame.drop_duplicates(): subset must be a constant column name, constant list of column names or None'
            )
    srxjx__rzye = []
    for col_name in kuqwp__mqb:
        if col_name not in df.columns:
            raise BodoError(
                'DataFrame.drop_duplicates(): All subset columns must be found in the DataFrame.'
                 +
                f'Column {col_name} not found in DataFrame columns {df.columns}'
                )
        srxjx__rzye.append(df.columns.index(col_name))
    check_unsupported_args('DataFrame.drop_duplicates', gtm__cjmma,
        ywtq__cnv, package_name='pandas', module_name='DataFrame')
    psyl__lywy = []
    if srxjx__rzye:
        for ufhh__hwi in srxjx__rzye:
            if isinstance(df.data[ufhh__hwi], bodo.MapArrayType):
                psyl__lywy.append(df.columns[ufhh__hwi])
    else:
        for i, col_name in enumerate(df.columns):
            if isinstance(df.data[i], bodo.MapArrayType):
                psyl__lywy.append(col_name)
    if psyl__lywy:
        raise BodoError(
            f'DataFrame.drop_duplicates(): Columns {psyl__lywy} ' +
            f'have dictionary types which cannot be used to drop duplicates. '
             +
            "Please consider using the 'subset' argument to skip these columns."
            )
    vkscu__dblgm = len(df.columns)
    dovjv__njdrq = ['data_{}'.format(i) for i in srxjx__rzye]
    kzqxr__wnufe = ['data_{}'.format(i) for i in range(vkscu__dblgm) if i
         not in srxjx__rzye]
    if dovjv__njdrq:
        cvfp__tpir = len(dovjv__njdrq)
    else:
        cvfp__tpir = vkscu__dblgm
    mojpc__nsw = ', '.join(dovjv__njdrq + kzqxr__wnufe)
    data_args = ', '.join('data_{}'.format(i) for i in range(vkscu__dblgm))
    beneg__gjlbt = (
        "def impl(df, subset=None, keep='first', inplace=False, ignore_index=False):\n"
        )
    for i in range(vkscu__dblgm):
        beneg__gjlbt += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    beneg__gjlbt += (
        """  ({0},), index_arr = bodo.libs.array_kernels.drop_duplicates(({0},), {1}, {2})
"""
        .format(mojpc__nsw, index, cvfp__tpir))
    beneg__gjlbt += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(beneg__gjlbt, df.columns, data_args, 'index')


def _gen_init_df(header, columns, data_args, index=None, extra_globals=None,
    out_df_type=None):
    if index is None:
        index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    if extra_globals is None:
        extra_globals = {}
    if out_df_type is not None:
        extra_globals['out_df_type'] = out_df_type
        otief__nbgl = 'out_df_type'
    else:
        otief__nbgl = gen_const_tup(columns)
    data_args = '({}{})'.format(data_args, ',' if data_args else '')
    beneg__gjlbt = f"""{header}  return bodo.hiframes.pd_dataframe_ext.init_dataframe({data_args}, {index}, {otief__nbgl})
"""
    grcyb__ihbff = {}
    hrx__bkif = {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba}
    hrx__bkif.update(extra_globals)
    exec(beneg__gjlbt, hrx__bkif, grcyb__ihbff)
    impl = grcyb__ihbff['impl']
    return impl


def _get_binop_columns(lhs, rhs, is_inplace=False):
    if lhs.columns != rhs.columns:
        eqon__xbi = pd.Index(lhs.columns)
        mkqae__ovcda = pd.Index(rhs.columns)
        yhvd__wjyr, sgk__zbgi, wvjeb__pbjv = eqon__xbi.join(mkqae__ovcda,
            how='left' if is_inplace else 'outer', level=None,
            return_indexers=True)
        return tuple(yhvd__wjyr), sgk__zbgi, wvjeb__pbjv
    return lhs.columns, range(len(lhs.columns)), range(len(lhs.columns))


def create_binary_op_overload(op):

    def overload_dataframe_binary_op(lhs, rhs):
        jod__fkvxf = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        jmtl__fux = operator.eq, operator.ne
        check_runtime_cols_unsupported(lhs, jod__fkvxf)
        check_runtime_cols_unsupported(rhs, jod__fkvxf)
        if isinstance(lhs, DataFrameType):
            if isinstance(rhs, DataFrameType):
                yhvd__wjyr, sgk__zbgi, wvjeb__pbjv = _get_binop_columns(lhs,
                    rhs)
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {qyego__mjphk}) {jod__fkvxf}bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {zzvk__tqm})'
                     if qyego__mjphk != -1 and zzvk__tqm != -1 else
                    f'bodo.libs.array_kernels.gen_na_array(len(lhs), float64_arr_type)'
                     for qyego__mjphk, zzvk__tqm in zip(sgk__zbgi, wvjeb__pbjv)
                    )
                header = 'def impl(lhs, rhs):\n'
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)')
                return _gen_init_df(header, yhvd__wjyr, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            soqz__xuk = []
            mhc__itye = []
            if op in jmtl__fux:
                for i, yrkya__fqjg in enumerate(lhs.data):
                    if is_common_scalar_dtype([yrkya__fqjg.dtype, rhs]):
                        soqz__xuk.append(
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {jod__fkvxf} rhs'
                            )
                    else:
                        zeh__chbci = f'arr{i}'
                        mhc__itye.append(zeh__chbci)
                        soqz__xuk.append(zeh__chbci)
                data_args = ', '.join(soqz__xuk)
            else:
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {jod__fkvxf} rhs'
                     for i in range(len(lhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(mhc__itye) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(lhs)\n'
                header += ''.join(
                    f'  {zeh__chbci} = np.empty(n, dtype=np.bool_)\n' for
                    zeh__chbci in mhc__itye)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(zeh__chbci, 
                    op == operator.ne) for zeh__chbci in mhc__itye)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)'
            return _gen_init_df(header, lhs.columns, data_args, index)
        if isinstance(rhs, DataFrameType):
            soqz__xuk = []
            mhc__itye = []
            if op in jmtl__fux:
                for i, yrkya__fqjg in enumerate(rhs.data):
                    if is_common_scalar_dtype([lhs, yrkya__fqjg.dtype]):
                        soqz__xuk.append(
                            f'lhs {jod__fkvxf} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {i})'
                            )
                    else:
                        zeh__chbci = f'arr{i}'
                        mhc__itye.append(zeh__chbci)
                        soqz__xuk.append(zeh__chbci)
                data_args = ', '.join(soqz__xuk)
            else:
                data_args = ', '.join(
                    'lhs {1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {0})'
                    .format(i, jod__fkvxf) for i in range(len(rhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(mhc__itye) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(rhs)\n'
                header += ''.join('  {0} = np.empty(n, dtype=np.bool_)\n'.
                    format(zeh__chbci) for zeh__chbci in mhc__itye)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(zeh__chbci, 
                    op == operator.ne) for zeh__chbci in mhc__itye)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(rhs)'
            return _gen_init_df(header, rhs.columns, data_args, index)
    return overload_dataframe_binary_op


skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        oyjzb__azciu = create_binary_op_overload(op)
        overload(op)(oyjzb__azciu)


_install_binary_ops()


def create_inplace_binary_op_overload(op):

    def overload_dataframe_inplace_binary_op(left, right):
        jod__fkvxf = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        check_runtime_cols_unsupported(left, jod__fkvxf)
        check_runtime_cols_unsupported(right, jod__fkvxf)
        if isinstance(left, DataFrameType):
            if isinstance(right, DataFrameType):
                yhvd__wjyr, ttq__hqs, wvjeb__pbjv = _get_binop_columns(left,
                    right, True)
                beneg__gjlbt = 'def impl(left, right):\n'
                for i, zzvk__tqm in enumerate(wvjeb__pbjv):
                    if zzvk__tqm == -1:
                        beneg__gjlbt += f"""  df_arr{i} = bodo.libs.array_kernels.gen_na_array(len(left), float64_arr_type)
"""
                        continue
                    beneg__gjlbt += f"""  df_arr{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {i})
"""
                    beneg__gjlbt += f"""  df_arr{i} {jod__fkvxf} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(right, {zzvk__tqm})
"""
                data_args = ', '.join(f'df_arr{i}' for i in range(len(
                    yhvd__wjyr)))
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)')
                return _gen_init_df(beneg__gjlbt, yhvd__wjyr, data_args,
                    index, extra_globals={'float64_arr_type': types.Array(
                    types.float64, 1, 'C')})
            beneg__gjlbt = 'def impl(left, right):\n'
            for i in range(len(left.columns)):
                beneg__gjlbt += (
                    """  df_arr{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {0})
"""
                    .format(i))
                beneg__gjlbt += '  df_arr{0} {1} right\n'.format(i, jod__fkvxf)
            data_args = ', '.join('df_arr{}'.format(i) for i in range(len(
                left.columns)))
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)'
            return _gen_init_df(beneg__gjlbt, left.columns, data_args, index)
    return overload_dataframe_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        oyjzb__azciu = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(oyjzb__azciu)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_dataframe_unary_op(df):
        if isinstance(df, DataFrameType):
            jod__fkvxf = numba.core.utils.OPERATORS_TO_BUILTINS[op]
            check_runtime_cols_unsupported(df, jod__fkvxf)
            data_args = ', '.join(
                '{1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
                .format(i, jod__fkvxf) for i in range(len(df.columns)))
            header = 'def impl(df):\n'
            return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        oyjzb__azciu = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(oyjzb__azciu)


_install_unary_ops()


def overload_isna(obj):
    check_runtime_cols_unsupported(obj, 'pd.isna()')
    if isinstance(obj, (DataFrameType, SeriesType)
        ) or bodo.hiframes.pd_index_ext.is_pd_index_type(obj):
        return lambda obj: obj.isna()
    if is_array_typ(obj):

        def impl(obj):
            numba.parfors.parfor.init_prange()
            n = len(obj)
            iageg__gtqjc = np.empty(n, np.bool_)
            for i in numba.parfors.parfor.internal_prange(n):
                iageg__gtqjc[i] = bodo.libs.array_kernels.isna(obj, i)
            return iageg__gtqjc
        return impl


overload(pd.isna, inline='always')(overload_isna)
overload(pd.isnull, inline='always')(overload_isna)


@overload(pd.isna)
@overload(pd.isnull)
def overload_isna_scalar(obj):
    if isinstance(obj, (DataFrameType, SeriesType)
        ) or bodo.hiframes.pd_index_ext.is_pd_index_type(obj) or is_array_typ(
        obj):
        return
    if isinstance(obj, (types.List, types.UniTuple)):

        def impl(obj):
            n = len(obj)
            iageg__gtqjc = np.empty(n, np.bool_)
            for i in range(n):
                iageg__gtqjc[i] = pd.isna(obj[i])
            return iageg__gtqjc
        return impl
    obj = types.unliteral(obj)
    if obj == bodo.string_type:
        return lambda obj: unliteral_val(False)
    if isinstance(obj, types.Integer):
        return lambda obj: unliteral_val(False)
    if isinstance(obj, types.Float):
        return lambda obj: np.isnan(obj)
    if isinstance(obj, (types.NPDatetime, types.NPTimedelta)):
        return lambda obj: np.isnat(obj)
    if obj == types.none:
        return lambda obj: unliteral_val(True)
    if obj == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        return lambda obj: np.isnat(bodo.hiframes.pd_timestamp_ext.
            integer_to_dt64(obj.value))
    if obj == bodo.hiframes.datetime_timedelta_ext.pd_timedelta_type:
        return lambda obj: np.isnat(bodo.hiframes.pd_timestamp_ext.
            integer_to_timedelta64(obj.value))
    if isinstance(obj, types.Optional):
        return lambda obj: obj is None
    return lambda obj: unliteral_val(False)


@overload(operator.setitem, no_unliteral=True)
def overload_setitem_arr_none(A, idx, val):
    if is_array_typ(A, False) and isinstance(idx, types.Integer
        ) and val == types.none:
        return lambda A, idx, val: bodo.libs.array_kernels.setna(A, idx)


def overload_notna(obj):
    check_runtime_cols_unsupported(obj, 'pd.notna()')
    if isinstance(obj, DataFrameType):
        return lambda obj: obj.notna()
    if isinstance(obj, (SeriesType, types.Array, types.List, types.UniTuple)
        ) or bodo.hiframes.pd_index_ext.is_pd_index_type(obj
        ) or obj == bodo.string_array_type:
        return lambda obj: ~pd.isna(obj)
    return lambda obj: not pd.isna(obj)


overload(pd.notna, inline='always', no_unliteral=True)(overload_notna)
overload(pd.notnull, inline='always', no_unliteral=True)(overload_notna)


def _get_pd_dtype_str(t):
    if t.dtype == types.NPDatetime('ns'):
        return "'datetime64[ns]'"
    return bodo.ir.csv_ext._get_pd_dtype_str(t)


@overload_method(DataFrameType, 'replace', inline='always', no_unliteral=True)
def overload_dataframe_replace(df, to_replace=None, value=None, inplace=
    False, limit=None, regex=False, method='pad'):
    check_runtime_cols_unsupported(df, 'DataFrame.replace()')
    if is_overload_none(to_replace):
        raise BodoError('replace(): to_replace value of None is not supported')
    gtm__cjmma = {'inplace': inplace, 'limit': limit, 'regex': regex,
        'method': method}
    ywtq__cnv = {'inplace': False, 'limit': None, 'regex': False, 'method':
        'pad'}
    check_unsupported_args('replace', gtm__cjmma, ywtq__cnv, package_name=
        'pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'df.iloc[:, {i}].replace(to_replace, value).values' for i in range
        (len(df.columns)))
    header = """def impl(df, to_replace=None, value=None, inplace=False, limit=None, regex=False, method='pad'):
"""
    return _gen_init_df(header, df.columns, data_args)


def _is_col_access(expr_node):
    yssn__gpy = str(expr_node)
    return yssn__gpy.startswith('left.') or yssn__gpy.startswith('right.')


def _insert_NA_cond(expr_node, left_columns, left_data, right_columns,
    right_data):
    rec__zgx = {'left': 0, 'right': 0, 'NOT_NA': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (rec__zgx,))
    vbq__gwxdd = pd.core.computation.parsing.clean_column_name

    def append_null_checks(expr_node, null_set):
        if not null_set:
            return expr_node
        oua__bgatn = ' & '.join([('NOT_NA.`' + x + '`') for x in null_set])
        cvdzp__gjucn = {('NOT_NA', vbq__gwxdd(yrkya__fqjg)): yrkya__fqjg for
            yrkya__fqjg in null_set}
        mlgym__clcko, ttq__hqs, ttq__hqs = _parse_query_expr(oua__bgatn,
            env, [], [], None, join_cleaned_cols=cvdzp__gjucn)
        pyp__hri = pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        try:
            cpd__xmy = pd.core.computation.ops.BinOp('&', mlgym__clcko,
                expr_node)
        finally:
            (pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
                ) = pyp__hri
        return cpd__xmy

    def _insert_NA_cond_body(expr_node, null_set):
        if isinstance(expr_node, pd.core.computation.ops.BinOp):
            if expr_node.op == '|':
                ate__afypn = set()
                alu__ocaj = set()
                tmlxy__fibzp = _insert_NA_cond_body(expr_node.lhs, ate__afypn)
                aib__ixdw = _insert_NA_cond_body(expr_node.rhs, alu__ocaj)
                qqr__ugtj = ate__afypn.intersection(alu__ocaj)
                ate__afypn.difference_update(qqr__ugtj)
                alu__ocaj.difference_update(qqr__ugtj)
                null_set.update(qqr__ugtj)
                expr_node.lhs = append_null_checks(tmlxy__fibzp, ate__afypn)
                expr_node.rhs = append_null_checks(aib__ixdw, alu__ocaj)
                expr_node.operands = expr_node.lhs, expr_node.rhs
            else:
                expr_node.lhs = _insert_NA_cond_body(expr_node.lhs, null_set)
                expr_node.rhs = _insert_NA_cond_body(expr_node.rhs, null_set)
        elif _is_col_access(expr_node):
            mkevt__zcb = expr_node.name
            fscy__zgqxr, col_name = mkevt__zcb.split('.')
            if fscy__zgqxr == 'left':
                vtdxh__mibbf = left_columns
                data = left_data
            else:
                vtdxh__mibbf = right_columns
                data = right_data
            enr__qql = data[vtdxh__mibbf.index(col_name)]
            if bodo.utils.typing.is_nullable(enr__qql):
                null_set.add(expr_node.name)
        return expr_node
    null_set = set()
    vxyd__dlxml = _insert_NA_cond_body(expr_node, null_set)
    return append_null_checks(expr_node, null_set)


def _extract_equal_conds(expr_node):
    if not hasattr(expr_node, 'op'):
        return [], [], expr_node
    if expr_node.op == '==' and _is_col_access(expr_node.lhs
        ) and _is_col_access(expr_node.rhs):
        ezft__wxiaj = str(expr_node.lhs)
        tbl__abam = str(expr_node.rhs)
        if ezft__wxiaj.startswith('left.') and tbl__abam.startswith('left.'
            ) or ezft__wxiaj.startswith('right.') and tbl__abam.startswith(
            'right.'):
            return [], [], expr_node
        left_on = [ezft__wxiaj.split('.')[1]]
        right_on = [tbl__abam.split('.')[1]]
        if ezft__wxiaj.startswith('right.'):
            return right_on, left_on, None
        return left_on, right_on, None
    if expr_node.op == '&':
        nzv__lssju, rkh__upen, htdcx__fwfos = _extract_equal_conds(expr_node
            .lhs)
        hkphr__eolcy, zjxr__yqn, xrdiv__uugp = _extract_equal_conds(expr_node
            .rhs)
        left_on = nzv__lssju + hkphr__eolcy
        right_on = rkh__upen + zjxr__yqn
        if htdcx__fwfos is None:
            return left_on, right_on, xrdiv__uugp
        if xrdiv__uugp is None:
            return left_on, right_on, htdcx__fwfos
        expr_node.lhs = htdcx__fwfos
        expr_node.rhs = xrdiv__uugp
        expr_node.operands = expr_node.lhs, expr_node.rhs
        return left_on, right_on, expr_node
    return [], [], expr_node


def _parse_merge_cond(on_str, left_columns, left_data, right_columns,
    right_data):
    rec__zgx = {'left': 0, 'right': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (rec__zgx,))
    owh__zdnc = dict()
    vbq__gwxdd = pd.core.computation.parsing.clean_column_name
    for name, bbe__nawl in (('left', left_columns), ('right', right_columns)):
        for yrkya__fqjg in bbe__nawl:
            zbgan__jphh = vbq__gwxdd(yrkya__fqjg)
            bbuv__dntb = name, zbgan__jphh
            if bbuv__dntb in owh__zdnc:
                raise BodoException(
                    f"pd.merge(): {name} table contains two columns that are escaped to the same Python identifier '{yrkya__fqjg}' and '{owh__zdnc[zbgan__jphh]}' Please rename one of these columns. To avoid this issue, please use names that are valid Python identifiers."
                    )
            owh__zdnc[bbuv__dntb] = yrkya__fqjg
    ocou__oyrv, ttq__hqs, ttq__hqs = _parse_query_expr(on_str, env, [], [],
        None, join_cleaned_cols=owh__zdnc)
    left_on, right_on, txx__dkmnv = _extract_equal_conds(ocou__oyrv.terms)
    return left_on, right_on, _insert_NA_cond(txx__dkmnv, left_columns,
        left_data, right_columns, right_data)


@overload_method(DataFrameType, 'merge', inline='always', no_unliteral=True)
@overload(pd.merge, inline='always', no_unliteral=True)
def overload_dataframe_merge(left, right, how='inner', on=None, left_on=
    None, right_on=None, left_index=False, right_index=False, sort=False,
    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None,
    _bodo_na_equal=True):
    check_runtime_cols_unsupported(left, 'DataFrame.merge()')
    check_runtime_cols_unsupported(right, 'DataFrame.merge()')
    lbci__ctjt = dict(sort=sort, copy=copy, validate=validate)
    runxq__egz = dict(sort=False, copy=True, validate=None)
    check_unsupported_args('DataFrame.merge', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
        right_index, sort, suffixes, copy, indicator, validate)
    how = get_overload_const_str(how)
    yyn__jdzst = tuple(sorted(set(left.columns) & set(right.columns), key=
        lambda k: str(k)))
    atzfp__low = ''
    if not is_overload_none(on):
        left_on = right_on = on
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            if on_str not in yyn__jdzst and ('left.' in on_str or 'right.' in
                on_str):
                left_on, right_on, qklt__gtbd = _parse_merge_cond(on_str,
                    left.columns, left.data, right.columns, right.data)
                if qklt__gtbd is None:
                    atzfp__low = ''
                else:
                    atzfp__low = str(qklt__gtbd)
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = yyn__jdzst
        right_keys = yyn__jdzst
    else:
        if is_overload_true(left_index):
            left_keys = ['$_bodo_index_']
        else:
            left_keys = get_overload_const_list(left_on)
            validate_keys(left_keys, left)
        if is_overload_true(right_index):
            right_keys = ['$_bodo_index_']
        else:
            right_keys = get_overload_const_list(right_on)
            validate_keys(right_keys, right)
    if (not left_on or not right_on) and not is_overload_none(on):
        raise BodoError(
            f"DataFrame.merge(): Merge condition '{get_overload_const_str(on)}' requires a cross join to implement, but cross join is not supported."
            )
    if not is_overload_bool(indicator):
        raise_bodo_error(
            'DataFrame.merge(): indicator must be a constant boolean')
    indicator_val = get_overload_const_bool(indicator)
    if not is_overload_bool(_bodo_na_equal):
        raise_bodo_error(
            'DataFrame.merge(): bodo extension _bodo_na_equal must be a constant boolean'
            )
    vgoag__zlckd = get_overload_const_bool(_bodo_na_equal)
    validate_keys_length(left_index, right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    if is_overload_constant_tuple(suffixes):
        yzj__tkh = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        yzj__tkh = list(get_overload_const_list(suffixes))
    suffix_x = yzj__tkh[0]
    suffix_y = yzj__tkh[1]
    validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
        right_keys, left.columns, right.columns, indicator_val)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    beneg__gjlbt = (
        "def _impl(left, right, how='inner', on=None, left_on=None,\n")
    beneg__gjlbt += (
        '    right_on=None, left_index=False, right_index=False, sort=False,\n'
        )
    beneg__gjlbt += """    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None, _bodo_na_equal=True):
"""
    beneg__gjlbt += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, '{}', '{}', '{}', False, {}, {}, '{}')
"""
        .format(left_keys, right_keys, how, suffix_x, suffix_y,
        indicator_val, vgoag__zlckd, atzfp__low))
    grcyb__ihbff = {}
    exec(beneg__gjlbt, {'bodo': bodo}, grcyb__ihbff)
    _impl = grcyb__ihbff['_impl']
    return _impl


def common_validate_merge_merge_asof_spec(name_func, left, right, on,
    left_on, right_on, left_index, right_index, suffixes):
    if not isinstance(left, DataFrameType) or not isinstance(right,
        DataFrameType):
        raise BodoError(name_func + '() requires dataframe inputs')
    valid_dataframe_column_types = (ArrayItemArrayType, MapArrayType,
        StructArrayType, CategoricalArrayType, types.Array,
        IntegerArrayType, DecimalArrayType, IntervalArrayType)
    lrn__frpea = {string_array_type, binary_array_type,
        datetime_date_array_type, datetime_timedelta_array_type, boolean_array}
    sxfa__rrl = {get_overload_const_str(syvcd__vliwb) for syvcd__vliwb in (
        left_on, right_on, on) if is_overload_constant_str(syvcd__vliwb)}
    for df in (left, right):
        for i, yrkya__fqjg in enumerate(df.data):
            if not isinstance(yrkya__fqjg, valid_dataframe_column_types
                ) and yrkya__fqjg not in lrn__frpea:
                raise BodoError(
                    f'{name_func}(): use of column with {type(yrkya__fqjg)} in merge unsupported'
                    )
            if df.columns[i] in sxfa__rrl and isinstance(yrkya__fqjg,
                MapArrayType):
                raise BodoError(
                    f'{name_func}(): merge on MapArrayType unsupported')
    ensure_constant_arg(name_func, 'left_index', left_index, bool)
    ensure_constant_arg(name_func, 'right_index', right_index, bool)
    if not is_overload_constant_tuple(suffixes
        ) and not is_overload_constant_list(suffixes):
        raise_const_error(name_func +
            "(): suffixes parameters should be ['_left', '_right']")
    if is_overload_constant_tuple(suffixes):
        yzj__tkh = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        yzj__tkh = list(get_overload_const_list(suffixes))
    if len(yzj__tkh) != 2:
        raise BodoError(name_func +
            '(): The number of suffixes should be exactly 2')
    yyn__jdzst = tuple(set(left.columns) & set(right.columns))
    if not is_overload_none(on):
        crj__qxype = False
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            crj__qxype = on_str not in yyn__jdzst and ('left.' in on_str or
                'right.' in on_str)
        if len(yyn__jdzst) == 0 and not crj__qxype:
            raise_bodo_error(name_func +
                '(): No common columns to perform merge on. Merge options: left_on={lon}, right_on={ron}, left_index={lidx}, right_index={ridx}'
                .format(lon=is_overload_true(left_on), ron=is_overload_true
                (right_on), lidx=is_overload_true(left_index), ridx=
                is_overload_true(right_index)))
        if not is_overload_none(left_on) or not is_overload_none(right_on):
            raise BodoError(name_func +
                '(): Can only pass argument "on" OR "left_on" and "right_on", not a combination of both.'
                )
    if (is_overload_true(left_index) or not is_overload_none(left_on)
        ) and is_overload_none(right_on) and not is_overload_true(right_index):
        raise BodoError(name_func +
            '(): Must pass right_on or right_index=True')
    if (is_overload_true(right_index) or not is_overload_none(right_on)
        ) and is_overload_none(left_on) and not is_overload_true(left_index):
        raise BodoError(name_func + '(): Must pass left_on or left_index=True')


def validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
    right_index, sort, suffixes, copy, indicator, validate):
    common_validate_merge_merge_asof_spec('merge', left, right, on, left_on,
        right_on, left_index, right_index, suffixes)
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))


def validate_merge_asof_spec(left, right, on, left_on, right_on, left_index,
    right_index, by, left_by, right_by, suffixes, tolerance,
    allow_exact_matches, direction):
    common_validate_merge_merge_asof_spec('merge_asof', left, right, on,
        left_on, right_on, left_index, right_index, suffixes)
    if not is_overload_true(allow_exact_matches):
        raise BodoError(
            'merge_asof(): allow_exact_matches parameter only supports default value True'
            )
    if not is_overload_none(tolerance):
        raise BodoError(
            'merge_asof(): tolerance parameter only supports default value None'
            )
    if not is_overload_none(by):
        raise BodoError(
            'merge_asof(): by parameter only supports default value None')
    if not is_overload_none(left_by):
        raise BodoError(
            'merge_asof(): left_by parameter only supports default value None')
    if not is_overload_none(right_by):
        raise BodoError(
            'merge_asof(): right_by parameter only supports default value None'
            )
    if not is_overload_constant_str(direction):
        raise BodoError(
            'merge_asof(): direction parameter should be of type str')
    else:
        direction = get_overload_const_str(direction)
        if direction != 'backward':
            raise BodoError(
                "merge_asof(): direction parameter only supports default value 'backward'"
                )


def validate_merge_asof_keys_length(left_on, right_on, left_index,
    right_index, left_keys, right_keys):
    if not is_overload_true(left_index) and not is_overload_true(right_index):
        if len(right_keys) != len(left_keys):
            raise BodoError('merge(): len(right_on) must equal len(left_on)')
    if not is_overload_none(left_on) and is_overload_true(right_index):
        raise BodoError(
            'merge(): right_index = True and specifying left_on is not suppported yet.'
            )
    if not is_overload_none(right_on) and is_overload_true(left_index):
        raise BodoError(
            'merge(): left_index = True and specifying right_on is not suppported yet.'
            )


def validate_keys_length(left_index, right_index, left_keys, right_keys):
    if not is_overload_true(left_index) and not is_overload_true(right_index):
        if len(right_keys) != len(left_keys):
            raise BodoError('merge(): len(right_on) must equal len(left_on)')
    if is_overload_true(right_index):
        if len(left_keys) != 1:
            raise BodoError(
                'merge(): len(left_on) must equal the number of levels in the index of "right", which is 1'
                )
    if is_overload_true(left_index):
        if len(right_keys) != 1:
            raise BodoError(
                'merge(): len(right_on) must equal the number of levels in the index of "left", which is 1'
                )


def validate_keys_dtypes(left, right, left_index, right_index, left_keys,
    right_keys):
    ysxm__qbgi = numba.core.registry.cpu_target.typing_context
    if is_overload_true(left_index) or is_overload_true(right_index):
        if is_overload_true(left_index) and is_overload_true(right_index):
            tda__uns = left.index
            oef__pzzrv = isinstance(tda__uns, StringIndexType)
            bqit__heix = right.index
            rvl__kfmut = isinstance(bqit__heix, StringIndexType)
        elif is_overload_true(left_index):
            tda__uns = left.index
            oef__pzzrv = isinstance(tda__uns, StringIndexType)
            bqit__heix = right.data[right.columns.index(right_keys[0])]
            rvl__kfmut = bqit__heix.dtype == string_type
        elif is_overload_true(right_index):
            tda__uns = left.data[left.columns.index(left_keys[0])]
            oef__pzzrv = tda__uns.dtype == string_type
            bqit__heix = right.index
            rvl__kfmut = isinstance(bqit__heix, StringIndexType)
        if oef__pzzrv and rvl__kfmut:
            return
        tda__uns = tda__uns.dtype
        bqit__heix = bqit__heix.dtype
        try:
            rcklt__rxbg = ysxm__qbgi.resolve_function_type(operator.eq, (
                tda__uns, bqit__heix), {})
        except:
            raise_bodo_error(
                'merge: You are trying to merge on {lk_dtype} and {rk_dtype} columns. If you wish to proceed you should use pd.concat'
                .format(lk_dtype=tda__uns, rk_dtype=bqit__heix))
    else:
        for kync__shkjk, hlui__lidx in zip(left_keys, right_keys):
            tda__uns = left.data[left.columns.index(kync__shkjk)].dtype
            sufgj__lae = left.data[left.columns.index(kync__shkjk)]
            bqit__heix = right.data[right.columns.index(hlui__lidx)].dtype
            pmyi__aplzi = right.data[right.columns.index(hlui__lidx)]
            if sufgj__lae == pmyi__aplzi:
                continue
            oemrm__wcabi = (
                'merge: You are trying to merge on column {lk} of {lk_dtype} and column {rk} of {rk_dtype}. If you wish to proceed you should use pd.concat'
                .format(lk=kync__shkjk, lk_dtype=tda__uns, rk=hlui__lidx,
                rk_dtype=bqit__heix))
            alg__qruk = tda__uns == string_type
            mbnzq__ebig = bqit__heix == string_type
            if alg__qruk ^ mbnzq__ebig:
                raise_bodo_error(oemrm__wcabi)
            try:
                rcklt__rxbg = ysxm__qbgi.resolve_function_type(operator.eq,
                    (tda__uns, bqit__heix), {})
            except:
                raise_bodo_error(oemrm__wcabi)


def validate_keys(keys, df):
    usvd__jdt = set(keys).difference(set(df.columns))
    if len(usvd__jdt) > 0:
        if is_overload_constant_str(df.index.name_typ
            ) and get_overload_const_str(df.index.name_typ) in usvd__jdt:
            raise_bodo_error(
                f'merge(): use of index {df.index.name_typ} as key for on/left_on/right_on is unsupported'
                )
        raise_bodo_error(
            f"""merge(): invalid key {usvd__jdt} for on/left_on/right_on
merge supports only valid column names {df.columns}"""
            )


@overload_method(DataFrameType, 'join', inline='always', no_unliteral=True)
def overload_dataframe_join(left, other, on=None, how='left', lsuffix='',
    rsuffix='', sort=False):
    check_runtime_cols_unsupported(left, 'DataFrame.join()')
    check_runtime_cols_unsupported(other, 'DataFrame.join()')
    lbci__ctjt = dict(lsuffix=lsuffix, rsuffix=rsuffix)
    runxq__egz = dict(lsuffix='', rsuffix='')
    check_unsupported_args('DataFrame.join', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort)
    how = get_overload_const_str(how)
    if not is_overload_none(on):
        left_keys = get_overload_const_list(on)
    else:
        left_keys = ['$_bodo_index_']
    right_keys = ['$_bodo_index_']
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    beneg__gjlbt = "def _impl(left, other, on=None, how='left',\n"
    beneg__gjlbt += "    lsuffix='', rsuffix='', sort=False):\n"
    beneg__gjlbt += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, other, {}, {}, '{}', '{}', '{}', True, False, True, '')
"""
        .format(left_keys, right_keys, how, lsuffix, rsuffix))
    grcyb__ihbff = {}
    exec(beneg__gjlbt, {'bodo': bodo}, grcyb__ihbff)
    _impl = grcyb__ihbff['_impl']
    return _impl


def validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort):
    if not isinstance(other, DataFrameType):
        raise BodoError('join() requires dataframe inputs')
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))
    if not is_overload_none(on) and len(get_overload_const_list(on)) != 1:
        raise BodoError('join(): len(on) must equals to 1 when specified.')
    if not is_overload_none(on):
        xxp__mam = get_overload_const_list(on)
        validate_keys(xxp__mam, left)
    if not is_overload_false(sort):
        raise BodoError(
            'join(): sort parameter only supports default value False')
    yyn__jdzst = tuple(set(left.columns) & set(other.columns))
    if len(yyn__jdzst) > 0:
        raise_bodo_error(
            'join(): not supporting joining on overlapping columns:{cols} Use DataFrame.merge() instead.'
            .format(cols=yyn__jdzst))


def validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
    right_keys, left_columns, right_columns, indicator_val):
    hca__sjnhg = set(left_keys) & set(right_keys)
    fftgo__elh = set(left_columns) & set(right_columns)
    ukrf__naljw = fftgo__elh - hca__sjnhg
    gsa__kafq = set(left_columns) - fftgo__elh
    xurud__iwth = set(right_columns) - fftgo__elh
    hfbkm__vinj = {}

    def insertOutColumn(col_name):
        if col_name in hfbkm__vinj:
            raise_bodo_error(
                'join(): two columns happen to have the same name : {}'.
                format(col_name))
        hfbkm__vinj[col_name] = 0
    for hjtk__wvax in hca__sjnhg:
        insertOutColumn(hjtk__wvax)
    for hjtk__wvax in ukrf__naljw:
        mhl__ftiup = str(hjtk__wvax) + suffix_x
        wbtky__xho = str(hjtk__wvax) + suffix_y
        insertOutColumn(mhl__ftiup)
        insertOutColumn(wbtky__xho)
    for hjtk__wvax in gsa__kafq:
        insertOutColumn(hjtk__wvax)
    for hjtk__wvax in xurud__iwth:
        insertOutColumn(hjtk__wvax)
    if indicator_val:
        insertOutColumn('_merge')


@overload(pd.merge_asof, inline='always', no_unliteral=True)
def overload_dataframe_merge_asof(left, right, on=None, left_on=None,
    right_on=None, left_index=False, right_index=False, by=None, left_by=
    None, right_by=None, suffixes=('_x', '_y'), tolerance=None,
    allow_exact_matches=True, direction='backward'):
    validate_merge_asof_spec(left, right, on, left_on, right_on, left_index,
        right_index, by, left_by, right_by, suffixes, tolerance,
        allow_exact_matches, direction)
    if not isinstance(left, DataFrameType) or not isinstance(right,
        DataFrameType):
        raise BodoError('merge_asof() requires dataframe inputs')
    yyn__jdzst = tuple(sorted(set(left.columns) & set(right.columns), key=
        lambda k: str(k)))
    if not is_overload_none(on):
        left_on = right_on = on
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = yyn__jdzst
        right_keys = yyn__jdzst
    else:
        if is_overload_true(left_index):
            left_keys = ['$_bodo_index_']
        else:
            left_keys = get_overload_const_list(left_on)
            validate_keys(left_keys, left)
        if is_overload_true(right_index):
            right_keys = ['$_bodo_index_']
        else:
            right_keys = get_overload_const_list(right_on)
            validate_keys(right_keys, right)
    validate_merge_asof_keys_length(left_on, right_on, left_index,
        right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    if isinstance(suffixes, tuple):
        yzj__tkh = suffixes
    if is_overload_constant_list(suffixes):
        yzj__tkh = list(get_overload_const_list(suffixes))
    if isinstance(suffixes, types.Omitted):
        yzj__tkh = suffixes.value
    suffix_x = yzj__tkh[0]
    suffix_y = yzj__tkh[1]
    beneg__gjlbt = (
        'def _impl(left, right, on=None, left_on=None, right_on=None,\n')
    beneg__gjlbt += (
        '    left_index=False, right_index=False, by=None, left_by=None,\n')
    beneg__gjlbt += (
        "    right_by=None, suffixes=('_x', '_y'), tolerance=None,\n")
    beneg__gjlbt += "    allow_exact_matches=True, direction='backward'):\n"
    beneg__gjlbt += '  suffix_x = suffixes[0]\n'
    beneg__gjlbt += '  suffix_y = suffixes[1]\n'
    beneg__gjlbt += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, 'asof', '{}', '{}', False, False, True, '')
"""
        .format(left_keys, right_keys, suffix_x, suffix_y))
    grcyb__ihbff = {}
    exec(beneg__gjlbt, {'bodo': bodo}, grcyb__ihbff)
    _impl = grcyb__ihbff['_impl']
    return _impl


@overload_method(DataFrameType, 'groupby', inline='always', no_unliteral=True)
def overload_dataframe_groupby(df, by=None, axis=0, level=None, as_index=
    True, sort=False, group_keys=True, squeeze=False, observed=True, dropna
    =True):
    check_runtime_cols_unsupported(df, 'DataFrame.groupby()')
    validate_groupby_spec(df, by, axis, level, as_index, sort, group_keys,
        squeeze, observed, dropna)

    def _impl(df, by=None, axis=0, level=None, as_index=True, sort=False,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        return bodo.hiframes.pd_groupby_ext.init_groupby(df, by, as_index,
            dropna)
    return _impl


def validate_groupby_spec(df, by, axis, level, as_index, sort, group_keys,
    squeeze, observed, dropna):
    if is_overload_none(by):
        raise BodoError("groupby(): 'by' must be supplied.")
    if not is_overload_zero(axis):
        raise BodoError(
            "groupby(): 'axis' parameter only supports integer value 0.")
    if not is_overload_none(level):
        raise BodoError(
            "groupby(): 'level' is not supported since MultiIndex is not supported."
            )
    if not is_literal_type(by) and not is_overload_constant_list(by):
        raise_const_error(
            f"groupby(): 'by' parameter only supports a constant column label or column labels, not {by}."
            )
    if len(set(get_overload_const_list(by)).difference(set(df.columns))) > 0:
        raise_const_error(
            "groupby(): invalid key {} for 'by' (not available in columns {})."
            .format(get_overload_const_list(by), df.columns))
    if not is_overload_constant_bool(as_index):
        raise_const_error(
            "groupby(): 'as_index' parameter must be a constant bool, not {}."
            .format(as_index))
    if not is_overload_constant_bool(dropna):
        raise_const_error(
            "groupby(): 'dropna' parameter must be a constant bool, not {}."
            .format(dropna))
    lbci__ctjt = dict(sort=sort, group_keys=group_keys, squeeze=squeeze,
        observed=observed)
    tvbg__uowyv = dict(sort=False, group_keys=True, squeeze=False, observed
        =True)
    check_unsupported_args('Dataframe.groupby', lbci__ctjt, tvbg__uowyv,
        package_name='pandas', module_name='GroupBy')


def pivot_error_checking(df, index, columns, values, func_name):
    if is_overload_none(index) or not is_literal_type(index):
        raise BodoError(
            f"{func_name}(): 'index' argument is required and must be a constant column label"
            )
    if is_overload_none(columns) or not is_literal_type(columns):
        raise BodoError(
            f"{func_name}(): 'columns' argument is required and must be a constant column label"
            )
    if not is_overload_none(values) and not is_literal_type(values):
        raise BodoError(
            f"{func_name}(): if 'values' argument is provided it must be a constant column label"
            )
    nyu__dfqoe = get_literal_value(index)
    if isinstance(nyu__dfqoe, (list, tuple)):
        if len(nyu__dfqoe) > 1:
            raise BodoError(
                f"{func_name}(): 'index' argument must be a constant column label not a {nyu__dfqoe}"
                )
        nyu__dfqoe = nyu__dfqoe[0]
    jhdv__iaxi = get_literal_value(columns)
    if isinstance(jhdv__iaxi, (list, tuple)):
        if len(jhdv__iaxi) > 1:
            raise BodoError(
                f"{func_name}(): 'columns' argument must be a constant column label not a {jhdv__iaxi}"
                )
        jhdv__iaxi = jhdv__iaxi[0]
    if nyu__dfqoe not in df.columns:
        raise BodoError(
            f"{func_name}(): 'index' column {nyu__dfqoe} not found in DataFrame {df}."
            )
    if jhdv__iaxi not in df.columns:
        raise BodoError(
            f"{func_name}(): 'columns' column {jhdv__iaxi} not found in DataFrame {df}."
            )
    vihvv__dpm = {nxjg__nry: i for i, nxjg__nry in enumerate(df.columns)}
    xarhy__jsx = vihvv__dpm[nyu__dfqoe]
    nix__skeuw = vihvv__dpm[jhdv__iaxi]
    if is_overload_none(values):
        iyv__sel = []
        fsbke__ggld = []
        for i, nxjg__nry in enumerate(df.columns):
            if i not in (xarhy__jsx, nix__skeuw):
                iyv__sel.append(i)
                fsbke__ggld.append(nxjg__nry)
    else:
        fsbke__ggld = get_literal_value(values)
        if not isinstance(fsbke__ggld, (list, tuple)):
            fsbke__ggld = [fsbke__ggld]
        iyv__sel = []
        for val in fsbke__ggld:
            if val not in vihvv__dpm:
                raise BodoError(
                    f"{func_name}(): 'values' column {val} not found in DataFrame {df}."
                    )
            iyv__sel.append(vihvv__dpm[val])
    if all(isinstance(nxjg__nry, int) for nxjg__nry in fsbke__ggld):
        fsbke__ggld = np.array(fsbke__ggld, 'int64')
    elif all(isinstance(nxjg__nry, str) for nxjg__nry in fsbke__ggld):
        fsbke__ggld = pd.array(fsbke__ggld, 'string')
    else:
        raise BodoError(
            f"{func_name}(): column names selected for 'values' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    farxx__bio = set(iyv__sel) | {xarhy__jsx, nix__skeuw}
    if len(farxx__bio) != len(iyv__sel) + 2:
        raise BodoError(
            f"{func_name}(): 'index', 'columns', and 'values' must all refer to different columns"
            )
    jxair__spvd = df.data[xarhy__jsx]
    if isinstance(jxair__spvd, (bodo.ArrayItemArrayType, bodo.MapArrayType,
        bodo.StructArrayType, bodo.TupleArrayType, bodo.IntervalArrayType)):
        raise BodoError(
            f"{func_name}(): 'index' DataFrame column must have scalar rows")
    if isinstance(jxair__spvd, bodo.CategoricalArrayType):
        raise BodoError(
            f"{func_name}(): 'index' DataFrame column does not support categorical data"
            )
    wvn__mfjxj = df.data[nix__skeuw]
    if isinstance(wvn__mfjxj, (bodo.ArrayItemArrayType, bodo.MapArrayType,
        bodo.StructArrayType, bodo.TupleArrayType, bodo.IntervalArrayType)):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column must have scalar rows")
    if isinstance(wvn__mfjxj, bodo.CategoricalArrayType):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column does not support categorical data"
            )
    for bkeap__ttj in iyv__sel:
        ewi__ofpf = df.data[bkeap__ttj]
        if isinstance(ewi__ofpf, (bodo.ArrayItemArrayType, bodo.
            MapArrayType, bodo.StructArrayType, bodo.TupleArrayType)
            ) or ewi__ofpf == bodo.binary_array_type:
            raise BodoError(
                f"{func_name}(): 'values' DataFrame column must have scalar rows"
                )
    return (nyu__dfqoe, jhdv__iaxi, fsbke__ggld, xarhy__jsx, nix__skeuw,
        iyv__sel)


@overload_method(DataFrameType, 'pivot', inline='always', no_unliteral=True)
def overload_dataframe_pivot(df, index=None, columns=None, values=None):
    check_runtime_cols_unsupported(df, 'DataFrame.pivot()')
    (nyu__dfqoe, jhdv__iaxi, fsbke__ggld, xarhy__jsx, nix__skeuw, ntnc__vsxub
        ) = (pivot_error_checking(df, index, columns, values,
        'DataFrame.pivot'))
    if len(fsbke__ggld) == 1:
        tkpe__xilme = None
    else:
        tkpe__xilme = fsbke__ggld
    beneg__gjlbt = 'def impl(df, index=None, columns=None, values=None):\n'
    beneg__gjlbt += f'    pivot_values = df.iloc[:, {nix__skeuw}].unique()\n'
    beneg__gjlbt += '    return bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
    beneg__gjlbt += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {xarhy__jsx}),),
"""
    beneg__gjlbt += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {nix__skeuw}),),
"""
    beneg__gjlbt += '        (\n'
    for bkeap__ttj in ntnc__vsxub:
        beneg__gjlbt += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {bkeap__ttj}),
"""
    beneg__gjlbt += '        ),\n'
    beneg__gjlbt += '        pivot_values,\n'
    beneg__gjlbt += '        index_lit,\n'
    beneg__gjlbt += '        columns_lit,\n'
    beneg__gjlbt += '        values_name_const,\n'
    beneg__gjlbt += '    )\n'
    grcyb__ihbff = {}
    exec(beneg__gjlbt, {'bodo': bodo, 'index_lit': nyu__dfqoe,
        'columns_lit': jhdv__iaxi, 'values_name_const': tkpe__xilme},
        grcyb__ihbff)
    impl = grcyb__ihbff['impl']
    return impl


@overload_method(DataFrameType, 'pivot_table', inline='always',
    no_unliteral=True)
def overload_dataframe_pivot_table(df, values=None, index=None, columns=
    None, aggfunc='mean', fill_value=None, margins=False, dropna=True,
    margins_name='All', observed=False, sort=True, _pivot_values=None):
    check_runtime_cols_unsupported(df, 'DataFrame.pivot_table()')
    lbci__ctjt = dict(fill_value=fill_value, margins=margins, dropna=dropna,
        margins_name=margins_name, observed=observed, sort=sort)
    runxq__egz = dict(fill_value=None, margins=False, dropna=True,
        margins_name='All', observed=False, sort=True)
    check_unsupported_args('DataFrame.pivot_table', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    if _pivot_values is None:
        (nyu__dfqoe, jhdv__iaxi, fsbke__ggld, xarhy__jsx, nix__skeuw,
            ntnc__vsxub) = (pivot_error_checking(df, index, columns, values,
            'DataFrame.pivot_table'))
        if len(fsbke__ggld) == 1:
            tkpe__xilme = None
        else:
            tkpe__xilme = fsbke__ggld
        beneg__gjlbt = 'def impl(\n'
        beneg__gjlbt += '    df,\n'
        beneg__gjlbt += '    values=None,\n'
        beneg__gjlbt += '    index=None,\n'
        beneg__gjlbt += '    columns=None,\n'
        beneg__gjlbt += '    aggfunc="mean",\n'
        beneg__gjlbt += '    fill_value=None,\n'
        beneg__gjlbt += '    margins=False,\n'
        beneg__gjlbt += '    dropna=True,\n'
        beneg__gjlbt += '    margins_name="All",\n'
        beneg__gjlbt += '    observed=False,\n'
        beneg__gjlbt += '    sort=True,\n'
        beneg__gjlbt += '    _pivot_values=None,\n'
        beneg__gjlbt += '):\n'
        qlp__tit = [xarhy__jsx, nix__skeuw] + ntnc__vsxub
        beneg__gjlbt += f'    df = df.iloc[:, {qlp__tit}]\n'
        beneg__gjlbt += """    df = df.groupby([index_lit, columns_lit], as_index=False).agg(aggfunc)
"""
        beneg__gjlbt += '    pivot_values = df.iloc[:, 1].unique()\n'
        beneg__gjlbt += (
            '    return bodo.hiframes.pd_dataframe_ext.pivot_impl(\n')
        beneg__gjlbt += (
            f'        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, 0),),\n'
            )
        beneg__gjlbt += (
            f'        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, 1),),\n'
            )
        beneg__gjlbt += '        (\n'
        for i in range(2, len(ntnc__vsxub) + 2):
            beneg__gjlbt += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}),
"""
        beneg__gjlbt += '        ),\n'
        beneg__gjlbt += '        pivot_values,\n'
        beneg__gjlbt += '        index_lit,\n'
        beneg__gjlbt += '        columns_lit,\n'
        beneg__gjlbt += '        values_name_const,\n'
        beneg__gjlbt += '        check_duplicates=False,\n'
        beneg__gjlbt += '    )\n'
        grcyb__ihbff = {}
        exec(beneg__gjlbt, {'bodo': bodo, 'index_lit': nyu__dfqoe,
            'columns_lit': jhdv__iaxi, 'values_name_const': tkpe__xilme},
            grcyb__ihbff)
        impl = grcyb__ihbff['impl']
        return impl
    if aggfunc == 'mean':

        def _impl(df, values=None, index=None, columns=None, aggfunc='mean',
            fill_value=None, margins=False, dropna=True, margins_name='All',
            observed=False, sort=True, _pivot_values=None):
            return bodo.hiframes.pd_groupby_ext.pivot_table_dummy(df,
                values, index, columns, 'mean', _pivot_values)
        return _impl

    def _impl(df, values=None, index=None, columns=None, aggfunc='mean',
        fill_value=None, margins=False, dropna=True, margins_name='All',
        observed=False, sort=True, _pivot_values=None):
        return bodo.hiframes.pd_groupby_ext.pivot_table_dummy(df, values,
            index, columns, aggfunc, _pivot_values)
    return _impl


@overload(pd.crosstab, inline='always', no_unliteral=True)
def crosstab_overload(index, columns, values=None, rownames=None, colnames=
    None, aggfunc=None, margins=False, margins_name='All', dropna=True,
    normalize=False, _pivot_values=None):
    lbci__ctjt = dict(values=values, rownames=rownames, colnames=colnames,
        aggfunc=aggfunc, margins=margins, margins_name=margins_name, dropna
        =dropna, normalize=normalize)
    runxq__egz = dict(values=None, rownames=None, colnames=None, aggfunc=
        None, margins=False, margins_name='All', dropna=True, normalize=False)
    check_unsupported_args('pandas.crosstab', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(index, SeriesType):
        raise BodoError(
            f"pandas.crosstab(): 'index' argument only supported for Series types, found {index}"
            )
    if not isinstance(columns, SeriesType):
        raise BodoError(
            f"pandas.crosstab(): 'columns' argument only supported for Series types, found {columns}"
            )

    def _impl(index, columns, values=None, rownames=None, colnames=None,
        aggfunc=None, margins=False, margins_name='All', dropna=True,
        normalize=False, _pivot_values=None):
        return bodo.hiframes.pd_groupby_ext.crosstab_dummy(index, columns,
            _pivot_values)
    return _impl


@overload_method(DataFrameType, 'sort_values', inline='always',
    no_unliteral=True)
def overload_dataframe_sort_values(df, by, axis=0, ascending=True, inplace=
    False, kind='quicksort', na_position='last', ignore_index=False, key=
    None, _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.sort_values()')
    lbci__ctjt = dict(ignore_index=ignore_index, key=key)
    runxq__egz = dict(ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_values', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'sort_values')
    validate_sort_values_spec(df, by, axis, ascending, inplace, kind,
        na_position)

    def _impl(df, by, axis=0, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', ignore_index=False, key=None,
        _bodo_transformed=False):
        return bodo.hiframes.pd_dataframe_ext.sort_values_dummy(df, by,
            ascending, inplace, na_position)
    return _impl


def validate_sort_values_spec(df, by, axis, ascending, inplace, kind,
    na_position):
    if is_overload_none(by) or not is_literal_type(by
        ) and not is_overload_constant_list(by):
        raise_const_error(
            "sort_values(): 'by' parameter only supports a constant column label or column labels. by={}"
            .format(by))
    oiqcv__eugz = set(df.columns)
    if is_overload_constant_str(df.index.name_typ):
        oiqcv__eugz.add(get_overload_const_str(df.index.name_typ))
    if is_overload_constant_tuple(by):
        jmz__gjvna = [get_overload_const_tuple(by)]
    else:
        jmz__gjvna = get_overload_const_list(by)
    jmz__gjvna = set((k, '') if (k, '') in oiqcv__eugz else k for k in
        jmz__gjvna)
    if len(jmz__gjvna.difference(oiqcv__eugz)) > 0:
        sro__dbza = list(set(get_overload_const_list(by)).difference(
            oiqcv__eugz))
        raise_bodo_error(f'sort_values(): invalid keys {sro__dbza} for by.')
    if not is_overload_zero(axis):
        raise_bodo_error(
            "sort_values(): 'axis' parameter only supports integer value 0.")
    if not is_overload_bool(ascending) and not is_overload_bool_list(ascending
        ):
        raise_bodo_error(
            "sort_values(): 'ascending' parameter must be of type bool or list of bool, not {}."
            .format(ascending))
    if not is_overload_bool(inplace):
        raise_bodo_error(
            "sort_values(): 'inplace' parameter must be of type bool, not {}."
            .format(inplace))
    if kind != 'quicksort' and not isinstance(kind, types.Omitted):
        warnings.warn(BodoWarning(
            'sort_values(): specifying sorting algorithm is not supported in Bodo. Bodo uses stable sort.'
            ))
    if is_overload_constant_str(na_position):
        na_position = get_overload_const_str(na_position)
        if na_position not in ('first', 'last'):
            raise BodoError(
                "sort_values(): na_position should either be 'first' or 'last'"
                )
    elif is_overload_constant_list(na_position):
        zdf__xxqvi = get_overload_const_list(na_position)
        for na_position in zdf__xxqvi:
            if na_position not in ('first', 'last'):
                raise BodoError(
                    "sort_values(): Every value in na_position should either be 'first' or 'last'"
                    )
    else:
        raise_const_error(
            f'sort_values(): na_position parameter must be a literal constant of type str or a constant list of str with 1 entry per key column, not {na_position}'
            )
    na_position = get_overload_const_str(na_position)
    if na_position not in ['first', 'last']:
        raise BodoError(
            "sort_values(): na_position should either be 'first' or 'last'")


@overload_method(DataFrameType, 'sort_index', inline='always', no_unliteral
    =True)
def overload_dataframe_sort_index(df, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    check_runtime_cols_unsupported(df, 'DataFrame.sort_index()')
    lbci__ctjt = dict(axis=axis, level=level, kind=kind, sort_remaining=
        sort_remaining, ignore_index=ignore_index, key=key)
    runxq__egz = dict(axis=0, level=None, kind='quicksort', sort_remaining=
        True, ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_index', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_bool(ascending):
        raise BodoError(
            "DataFrame.sort_index(): 'ascending' parameter must be of type bool"
            )
    if not is_overload_bool(inplace):
        raise BodoError(
            "DataFrame.sort_index(): 'inplace' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "DataFrame.sort_index(): 'na_position' should either be 'first' or 'last'"
            )

    def _impl(df, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        return bodo.hiframes.pd_dataframe_ext.sort_values_dummy(df,
            '$_bodo_index_', ascending, inplace, na_position)
    return _impl


@overload_method(DataFrameType, 'fillna', inline='always', no_unliteral=True)
def overload_dataframe_fillna(df, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    check_runtime_cols_unsupported(df, 'DataFrame.fillna()')
    lbci__ctjt = dict(limit=limit, downcast=downcast)
    runxq__egz = dict(limit=None, downcast=None)
    check_unsupported_args('DataFrame.fillna', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError("DataFrame.fillna(): 'axis' argument not supported.")
    fjmjv__gsr = not is_overload_none(value)
    mkui__jvrs = not is_overload_none(method)
    if fjmjv__gsr and mkui__jvrs:
        raise BodoError(
            "DataFrame.fillna(): Cannot specify both 'value' and 'method'.")
    if not fjmjv__gsr and not mkui__jvrs:
        raise BodoError(
            "DataFrame.fillna(): Must specify one of 'value' and 'method'.")
    if fjmjv__gsr:
        kymm__tjbg = 'value=value'
    else:
        kymm__tjbg = 'method=method'
    data_args = [(
        f"df['{nxjg__nry}'].fillna({kymm__tjbg}, inplace=inplace)" if
        isinstance(nxjg__nry, str) else
        f'df[{nxjg__nry}].fillna({kymm__tjbg}, inplace=inplace)') for
        nxjg__nry in df.columns]
    beneg__gjlbt = """def impl(df, value=None, method=None, axis=None, inplace=False, limit=None, downcast=None):
"""
    if is_overload_true(inplace):
        beneg__gjlbt += '  ' + '  \n'.join(data_args) + '\n'
        grcyb__ihbff = {}
        exec(beneg__gjlbt, {}, grcyb__ihbff)
        impl = grcyb__ihbff['impl']
        return impl
    else:
        return _gen_init_df(beneg__gjlbt, df.columns, ', '.join(cyp__belq +
            '.values' for cyp__belq in data_args))


@overload_method(DataFrameType, 'reset_index', inline='always',
    no_unliteral=True)
def overload_dataframe_reset_index(df, level=None, drop=False, inplace=
    False, col_level=0, col_fill='', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.reset_index()')
    lbci__ctjt = dict(col_level=col_level, col_fill=col_fill)
    runxq__egz = dict(col_level=0, col_fill='')
    check_unsupported_args('DataFrame.reset_index', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'reset_index')
    if not _is_all_levels(df, level):
        raise_bodo_error(
            'DataFrame.reset_index(): only dropping all index levels supported'
            )
    if not is_overload_constant_bool(drop):
        raise BodoError(
            "DataFrame.reset_index(): 'drop' parameter should be a constant boolean value"
            )
    if not is_overload_constant_bool(inplace):
        raise BodoError(
            "DataFrame.reset_index(): 'inplace' parameter should be a constant boolean value"
            )
    beneg__gjlbt = """def impl(df, level=None, drop=False, inplace=False, col_level=0, col_fill='', _bodo_transformed=False,):
"""
    beneg__gjlbt += (
        '  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(df), 1, None)\n'
        )
    drop = is_overload_true(drop)
    inplace = is_overload_true(inplace)
    columns = df.columns
    data_args = [
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}\n'.
        format(i, '' if inplace else '.copy()') for i in range(len(df.columns))
        ]
    if not drop:
        nfy__uesmm = 'index' if 'index' not in columns else 'level_0'
        index_names = get_index_names(df.index, 'DataFrame.reset_index()',
            nfy__uesmm)
        columns = index_names + columns
        if isinstance(df.index, MultiIndexType):
            beneg__gjlbt += (
                '  m_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
                )
            kamz__gnqb = ['m_index._data[{}]'.format(i) for i in range(df.
                index.nlevels)]
            data_args = kamz__gnqb + data_args
        else:
            odu__gtwrt = (
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
                )
            data_args = [odu__gtwrt] + data_args
    return _gen_init_df(beneg__gjlbt, columns, ', '.join(data_args), 'index')


def _is_all_levels(df, level):
    clytn__lgmfc = len(get_index_data_arr_types(df.index))
    return is_overload_none(level) or is_overload_constant_int(level
        ) and get_overload_const_int(level
        ) == 0 and clytn__lgmfc == 1 or is_overload_constant_list(level
        ) and list(get_overload_const_list(level)) == list(range(clytn__lgmfc))


@overload_method(DataFrameType, 'dropna', inline='always', no_unliteral=True)
def overload_dataframe_dropna(df, axis=0, how='any', thresh=None, subset=
    None, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.dropna()')
    if not is_overload_constant_bool(inplace) or is_overload_true(inplace):
        raise BodoError('DataFrame.dropna(): inplace=True is not supported')
    if not is_overload_zero(axis):
        raise_bodo_error(f'df.dropna(): only axis=0 supported')
    ensure_constant_values('dropna', 'how', how, ('any', 'all'))
    if is_overload_none(subset):
        mukg__kuw = list(range(len(df.columns)))
    elif not is_overload_constant_list(subset):
        raise_bodo_error(
            f'df.dropna(): subset argument should a constant list, not {subset}'
            )
    else:
        twuk__ggkok = get_overload_const_list(subset)
        mukg__kuw = []
        for hlxan__uezf in twuk__ggkok:
            if hlxan__uezf not in df.columns:
                raise_bodo_error(
                    f"df.dropna(): column '{hlxan__uezf}' not in data frame columns {df}"
                    )
            mukg__kuw.append(df.columns.index(hlxan__uezf))
    vkscu__dblgm = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(vkscu__dblgm))
    beneg__gjlbt = (
        "def impl(df, axis=0, how='any', thresh=None, subset=None, inplace=False):\n"
        )
    for i in range(vkscu__dblgm):
        beneg__gjlbt += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    beneg__gjlbt += (
        """  ({0}, index_arr) = bodo.libs.array_kernels.dropna(({0}, {1}), how, thresh, ({2},))
"""
        .format(data_args, index, ', '.join(str(a) for a in mukg__kuw)))
    beneg__gjlbt += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(beneg__gjlbt, df.columns, data_args, 'index')


@overload_method(DataFrameType, 'drop', inline='always', no_unliteral=True)
def overload_dataframe_drop(df, labels=None, axis=0, index=None, columns=
    None, level=None, inplace=False, errors='raise', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop()')
    lbci__ctjt = dict(index=index, level=level, errors=errors)
    runxq__egz = dict(index=None, level=None, errors='raise')
    check_unsupported_args('DataFrame.drop', lbci__ctjt, runxq__egz,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'drop')
    if not is_overload_constant_bool(inplace):
        raise_bodo_error(
            "DataFrame.drop(): 'inplace' parameter should be a constant bool")
    if not is_overload_none(labels):
        if not is_overload_none(columns):
            raise BodoError(
                "Dataframe.drop(): Cannot specify both 'labels' and 'columns'")
        if not is_overload_constant_int(axis) or get_overload_const_int(axis
            ) != 1:
            raise_bodo_error('DataFrame.drop(): only axis=1 supported')
        if is_overload_constant_str(labels):
            hakig__rxhc = get_overload_const_str(labels),
        elif is_overload_constant_list(labels):
            hakig__rxhc = get_overload_const_list(labels)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    else:
        if is_overload_none(columns):
            raise BodoError(
                "DataFrame.drop(): Need to specify at least one of 'labels' or 'columns'"
                )
        if is_overload_constant_str(columns):
            hakig__rxhc = get_overload_const_str(columns),
        elif is_overload_constant_list(columns):
            hakig__rxhc = get_overload_const_list(columns)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    for nxjg__nry in hakig__rxhc:
        if nxjg__nry not in df.columns:
            raise_bodo_error(
                'DataFrame.drop(): column {} not in DataFrame columns {}'.
                format(nxjg__nry, df.columns))
    if len(set(hakig__rxhc)) == len(df.columns):
        raise BodoError('DataFrame.drop(): Dropping all columns not supported.'
            )
    inplace = is_overload_true(inplace)
    are__taftw = tuple(nxjg__nry for nxjg__nry in df.columns if nxjg__nry
         not in hakig__rxhc)
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.columns.index(nxjg__nry), '.copy()' if not inplace else
        '') for nxjg__nry in are__taftw)
    beneg__gjlbt = (
        'def impl(df, labels=None, axis=0, index=None, columns=None,\n')
    beneg__gjlbt += (
        "     level=None, inplace=False, errors='raise', _bodo_transformed=False):\n"
        )
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    return _gen_init_df(beneg__gjlbt, are__taftw, data_args, index)


@overload_method(DataFrameType, 'append', inline='always', no_unliteral=True)
def overload_dataframe_append(df, other, ignore_index=False,
    verify_integrity=False, sort=None):
    check_runtime_cols_unsupported(df, 'DataFrame.append()')
    check_runtime_cols_unsupported(other, 'DataFrame.append()')
    if isinstance(other, DataFrameType):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat((df, other), ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    if isinstance(other, types.BaseTuple):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat((df,) + other, ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    if isinstance(other, types.List) and isinstance(other.dtype, DataFrameType
        ):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat([df] + other, ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    raise BodoError(
        'invalid df.append() input. Only dataframe and list/tuple of dataframes supported'
        )


@overload_method(DataFrameType, 'sample', inline='always', no_unliteral=True)
def overload_dataframe_sample(df, n=None, frac=None, replace=False, weights
    =None, random_state=None, axis=None, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.sample()')
    lbci__ctjt = dict(random_state=random_state, weights=weights, axis=axis,
        ignore_index=ignore_index)
    ffn__fkzuj = dict(random_state=None, weights=None, axis=None,
        ignore_index=False)
    check_unsupported_args('DataFrame.sample', lbci__ctjt, ffn__fkzuj,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_none(n) and not is_overload_none(frac):
        raise BodoError(
            'DataFrame.sample(): only one of n and frac option can be selected'
            )
    vkscu__dblgm = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(vkscu__dblgm))
    beneg__gjlbt = """def impl(df, n=None, frac=None, replace=False, weights=None, random_state=None, axis=None, ignore_index=False):
"""
    for i in range(vkscu__dblgm):
        beneg__gjlbt += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    beneg__gjlbt += '  if frac is None:\n'
    beneg__gjlbt += '    frac_d = -1.0\n'
    beneg__gjlbt += '  else:\n'
    beneg__gjlbt += '    frac_d = frac\n'
    beneg__gjlbt += '  if n is None:\n'
    beneg__gjlbt += '    n_i = 0\n'
    beneg__gjlbt += '  else:\n'
    beneg__gjlbt += '    n_i = n\n'
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    beneg__gjlbt += (
        """  ({0},), index_arr = bodo.libs.array_kernels.sample_table_operation(({0},), {1}, n_i, frac_d, replace)
"""
        .format(data_args, index))
    beneg__gjlbt += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return bodo.hiframes.dataframe_impl._gen_init_df(beneg__gjlbt, df.
        columns, data_args, 'index')


@numba.njit
def _sizeof_fmt(num, size_qualifier=''):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f'{num:3.1f}{size_qualifier} {x}'
        num /= 1024.0
    return f'{num:3.1f}{size_qualifier} PB'


@overload_method(DataFrameType, 'info', no_unliteral=True)
def overload_dataframe_info(df, verbose=None, buf=None, max_cols=None,
    memory_usage=None, show_counts=None, null_counts=None):
    check_runtime_cols_unsupported(df, 'DataFrame.info()')
    gtm__cjmma = {'verbose': verbose, 'buf': buf, 'max_cols': max_cols,
        'memory_usage': memory_usage, 'show_counts': show_counts,
        'null_counts': null_counts}
    ywtq__cnv = {'verbose': None, 'buf': None, 'max_cols': None,
        'memory_usage': None, 'show_counts': None, 'null_counts': None}
    check_unsupported_args('DataFrame.info', gtm__cjmma, ywtq__cnv,
        package_name='pandas', module_name='DataFrame')
    xcdl__akfed = f"<class '{str(type(df)).split('.')[-1]}"
    if len(df.columns) == 0:

        def _info_impl(df, verbose=None, buf=None, max_cols=None,
            memory_usage=None, show_counts=None, null_counts=None):
            eegvl__ujdb = xcdl__akfed + '\n'
            eegvl__ujdb += 'Index: 0 entries\n'
            eegvl__ujdb += 'Empty DataFrame'
            print(eegvl__ujdb)
        return _info_impl
    else:
        beneg__gjlbt = """def _info_impl(df, verbose=None, buf=None, max_cols=None, memory_usage=None, show_counts=None, null_counts=None): #pragma: no cover
"""
        beneg__gjlbt += '    ncols = df.shape[1]\n'
        beneg__gjlbt += f'    lines = "{xcdl__akfed}\\n"\n'
        beneg__gjlbt += f'    lines += "{df.index}: "\n'
        beneg__gjlbt += (
            '    index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        if isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType):
            beneg__gjlbt += """    lines += f"{len(index)} entries, {index.start} to {index.stop-1}\\n\"
"""
        elif isinstance(df.index, bodo.hiframes.pd_index_ext.StringIndexType):
            beneg__gjlbt += """    lines += f"{len(index)} entries, {index[0]} to {index[len(index)-1]}\\n\"
"""
        else:
            beneg__gjlbt += (
                '    lines += f"{len(index)} entries, {index[0]} to {index[-1]}\\n"\n'
                )
        beneg__gjlbt += (
            '    lines += f"Data columns (total {ncols} columns):\\n"\n')
        beneg__gjlbt += (
            f'    space = {max(len(str(k)) for k in df.columns) + 1}\n')
        beneg__gjlbt += '    column_width = max(space, 7)\n'
        beneg__gjlbt += '    column= "Column"\n'
        beneg__gjlbt += '    underl= "------"\n'
        beneg__gjlbt += (
            '    lines += f"#   {column:<{column_width}} Non-Null Count  Dtype\\n"\n'
            )
        beneg__gjlbt += (
            '    lines += f"--- {underl:<{column_width}} --------------  -----\\n"\n'
            )
        beneg__gjlbt += '    mem_size = 0\n'
        beneg__gjlbt += (
            '    col_name = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        beneg__gjlbt += """    non_null_count = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)
"""
        beneg__gjlbt += (
            '    col_dtype = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        zhh__gvgo = dict()
        for i in range(len(df.columns)):
            beneg__gjlbt += f"""    non_null_count[{i}] = str(bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})))
"""
            rmmeg__qrx = f'{df.data[i].dtype}'
            if isinstance(df.data[i], bodo.CategoricalArrayType):
                rmmeg__qrx = 'category'
            elif isinstance(df.data[i], bodo.IntegerArrayType):
                vko__vic = bodo.libs.int_arr_ext.IntDtype(df.data[i].dtype
                    ).name
                rmmeg__qrx = f'{vko__vic[:-7]}'
            beneg__gjlbt += f'    col_dtype[{i}] = "{rmmeg__qrx}"\n'
            if rmmeg__qrx in zhh__gvgo:
                zhh__gvgo[rmmeg__qrx] += 1
            else:
                zhh__gvgo[rmmeg__qrx] = 1
            beneg__gjlbt += f'    col_name[{i}] = "{df.columns[i]}"\n'
            beneg__gjlbt += f"""    mem_size += bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).nbytes
"""
        beneg__gjlbt += """    column_info = [f'{i:^3} {name:<{column_width}} {count} non-null      {dtype}' for i, (name, count, dtype) in enumerate(zip(col_name, non_null_count, col_dtype))]
"""
        beneg__gjlbt += '    for i in column_info:\n'
        beneg__gjlbt += "        lines += f'{i}\\n'\n"
        snff__ohtjr = ', '.join(f'{k}({zhh__gvgo[k]})' for k in sorted(
            zhh__gvgo))
        beneg__gjlbt += f"    lines += 'dtypes: {snff__ohtjr}\\n'\n"
        beneg__gjlbt += '    mem_size += df.index.nbytes\n'
        beneg__gjlbt += '    total_size = _sizeof_fmt(mem_size)\n'
        beneg__gjlbt += "    lines += f'memory usage: {total_size}'\n"
        beneg__gjlbt += '    print(lines)\n'
        grcyb__ihbff = {}
        exec(beneg__gjlbt, {'_sizeof_fmt': _sizeof_fmt, 'pd': pd, 'bodo':
            bodo, 'np': np}, grcyb__ihbff)
        _info_impl = grcyb__ihbff['_info_impl']
        return _info_impl


@overload_method(DataFrameType, 'memory_usage', inline='always',
    no_unliteral=True)
def overload_dataframe_memory_usage(df, index=True, deep=False):
    check_runtime_cols_unsupported(df, 'DataFrame.memory_usage()')
    beneg__gjlbt = 'def impl(df, index=True, deep=False):\n'
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).nbytes'
         for i in range(len(df.columns)))
    if is_overload_true(index):
        zjiwd__ywusz = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df).nbytes\n,')
        ecc__fnsvy = ','.join(f"'{nxjg__nry}'" for nxjg__nry in df.columns)
        arr = f"bodo.utils.conversion.coerce_to_array(('Index',{ecc__fnsvy}))"
        index = f'bodo.hiframes.pd_index_ext.init_binary_str_index({arr})'
        beneg__gjlbt += f"""  return bodo.hiframes.pd_series_ext.init_series(({zjiwd__ywusz}{data}), {index}, None)
"""
    else:
        dbfji__ymmsw = ',' if len(df.columns) == 1 else ''
        otief__nbgl = gen_const_tup(df.columns)
        beneg__gjlbt += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}{dbfji__ymmsw}), pd.Index({otief__nbgl}), None)
"""
    grcyb__ihbff = {}
    exec(beneg__gjlbt, {'bodo': bodo, 'pd': pd}, grcyb__ihbff)
    impl = grcyb__ihbff['impl']
    return impl


@overload(pd.read_excel, no_unliteral=True)
def overload_read_excel(io, sheet_name=0, header=0, names=None, index_col=
    None, usecols=None, squeeze=False, dtype=None, engine=None, converters=
    None, true_values=None, false_values=None, skiprows=None, nrows=None,
    na_values=None, keep_default_na=True, na_filter=True, verbose=False,
    parse_dates=False, date_parser=None, thousands=None, comment=None,
    skipfooter=0, convert_float=True, mangle_dupe_cols=True, _bodo_df_type=None
    ):
    df_type = _bodo_df_type.instance_type
    wqu__gdp = 'read_excel_df{}'.format(next_label())
    setattr(types, wqu__gdp, df_type)
    izyp__lkkxq = False
    if is_overload_constant_list(parse_dates):
        izyp__lkkxq = get_overload_const_list(parse_dates)
    ixs__drce = ', '.join(["'{}':{}".format(cname, _get_pd_dtype_str(t)) for
        cname, t in zip(df_type.columns, df_type.data)])
    beneg__gjlbt = (
        """
def impl(
    io,
    sheet_name=0,
    header=0,
    names=None,
    index_col=None,
    usecols=None,
    squeeze=False,
    dtype=None,
    engine=None,
    converters=None,
    true_values=None,
    false_values=None,
    skiprows=None,
    nrows=None,
    na_values=None,
    keep_default_na=True,
    na_filter=True,
    verbose=False,
    parse_dates=False,
    date_parser=None,
    thousands=None,
    comment=None,
    skipfooter=0,
    convert_float=True,
    mangle_dupe_cols=True,
    _bodo_df_type=None,
):
    with numba.objmode(df="{}"):
        df = pd.read_excel(
            io,
            sheet_name,
            header,
            {},
            index_col,
            usecols,
            squeeze,
            {{{}}},
            engine,
            converters,
            true_values,
            false_values,
            skiprows,
            nrows,
            na_values,
            keep_default_na,
            na_filter,
            verbose,
            {},
            date_parser,
            thousands,
            comment,
            skipfooter,
            convert_float,
            mangle_dupe_cols,
        )
    return df
    """
        .format(wqu__gdp, list(df_type.columns), ixs__drce, izyp__lkkxq))
    grcyb__ihbff = {}
    exec(beneg__gjlbt, globals(), grcyb__ihbff)
    impl = grcyb__ihbff['impl']
    return impl


def overload_dataframe_plot(df, x=None, y=None, kind='line', figsize=None,
    xlabel=None, ylabel=None, title=None, legend=True, fontsize=None,
    xticks=None, yticks=None, ax=None):
    if bodo.compiler._matplotlib_installed:
        import matplotlib.pyplot as plt
    else:
        raise BodoError('df.plot needs matplotllib which is not installed.')
    beneg__gjlbt = (
        "def impl(df, x=None, y=None, kind='line', figsize=None, xlabel=None, \n"
        )
    beneg__gjlbt += (
        '    ylabel=None, title=None, legend=True, fontsize=None, \n')
    beneg__gjlbt += '    xticks=None, yticks=None, ax=None):\n'
    if is_overload_none(ax):
        beneg__gjlbt += '   fig, ax = plt.subplots()\n'
    else:
        beneg__gjlbt += '   fig = ax.get_figure()\n'
    if not is_overload_none(figsize):
        beneg__gjlbt += '   fig.set_figwidth(figsize[0])\n'
        beneg__gjlbt += '   fig.set_figheight(figsize[1])\n'
    if is_overload_none(xlabel):
        beneg__gjlbt += '   xlabel = x\n'
    beneg__gjlbt += '   ax.set_xlabel(xlabel)\n'
    if is_overload_none(ylabel):
        beneg__gjlbt += '   ylabel = y\n'
    else:
        beneg__gjlbt += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(title):
        beneg__gjlbt += '   ax.set_title(title)\n'
    if not is_overload_none(fontsize):
        beneg__gjlbt += '   ax.tick_params(labelsize=fontsize)\n'
    kind = get_overload_const_str(kind)
    if kind == 'line':
        if is_overload_none(x) and is_overload_none(y):
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    beneg__gjlbt += (
                        f'   ax.plot(df.iloc[:, {i}], label=df.columns[{i}])\n'
                        )
        elif is_overload_none(x):
            beneg__gjlbt += '   ax.plot(df[y], label=y)\n'
        elif is_overload_none(y):
            hmkfk__myoo = get_overload_const_str(x)
            ngy__dxgr = df.columns.index(hmkfk__myoo)
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    if ngy__dxgr != i:
                        beneg__gjlbt += f"""   ax.plot(df[x], df.iloc[:, {i}], label=df.columns[{i}])
"""
        else:
            beneg__gjlbt += '   ax.plot(df[x], df[y], label=y)\n'
    elif kind == 'scatter':
        legend = False
        beneg__gjlbt += '   ax.scatter(df[x], df[y], s=20)\n'
        beneg__gjlbt += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(xticks):
        beneg__gjlbt += '   ax.set_xticks(xticks)\n'
    if not is_overload_none(yticks):
        beneg__gjlbt += '   ax.set_yticks(yticks)\n'
    if is_overload_true(legend):
        beneg__gjlbt += '   ax.legend()\n'
    beneg__gjlbt += '   return ax\n'
    grcyb__ihbff = {}
    exec(beneg__gjlbt, {'bodo': bodo, 'plt': plt}, grcyb__ihbff)
    impl = grcyb__ihbff['impl']
    return impl


@lower_builtin('df.plot', DataFrameType, types.VarArg(types.Any))
def dataframe_plot_low(context, builder, sig, args):
    impl = overload_dataframe_plot(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def is_df_values_numpy_supported_dftyp(df_typ):
    for zza__yrllh in df_typ.data:
        if not (isinstance(zza__yrllh, IntegerArrayType) or isinstance(
            zza__yrllh.dtype, types.Number) or zza__yrllh.dtype in (bodo.
            datetime64ns, bodo.timedelta64ns)):
            return False
    return True


def typeref_to_type(v):
    if isinstance(v, types.BaseTuple):
        return types.BaseTuple.from_types(tuple(typeref_to_type(a) for a in v))
    return v.instance_type if isinstance(v, (types.TypeRef, types.NumberClass)
        ) else v


def _install_typer_for_type(type_name, typ):

    @type_callable(typ)
    def type_call_type(context):

        def typer(*args, **kws):
            args = tuple(typeref_to_type(v) for v in args)
            kws = {name: typeref_to_type(v) for name, v in kws.items()}
            return types.TypeRef(typ(*args, **kws))
        return typer
    no_side_effect_call_tuples.add((type_name, bodo))
    no_side_effect_call_tuples.add((typ,))


def _install_type_call_typers():
    for type_name in bodo_types_with_params:
        typ = getattr(bodo, type_name)
        _install_typer_for_type(type_name, typ)


_install_type_call_typers()


def set_df_col(df, cname, arr, inplace):
    df[cname] = arr


@infer_global(set_df_col)
class SetDfColInfer(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        assert not kws
        assert len(args) == 4
        assert isinstance(args[1], types.Literal)
        tbs__kjr = args[0]
        nmipy__ekacu = args[1].literal_value
        val = args[2]
        assert val != types.unknown
        ctzou__rzk = tbs__kjr
        check_runtime_cols_unsupported(tbs__kjr, 'set_df_col()')
        if isinstance(tbs__kjr, DataFrameType):
            index = tbs__kjr.index
            if len(tbs__kjr.columns) == 0:
                index = bodo.hiframes.pd_index_ext.RangeIndexType(types.none)
            if isinstance(val, SeriesType):
                if len(tbs__kjr.columns) == 0:
                    index = val.index
                val = val.data
            if is_pd_index_type(val):
                val = bodo.utils.typing.get_index_data_arr_types(val)[0]
            if isinstance(val, types.List):
                val = dtype_to_array_type(val.dtype)
            if not is_array_typ(val):
                val = dtype_to_array_type(val)
            if nmipy__ekacu in tbs__kjr.columns:
                are__taftw = tbs__kjr.columns
                esp__lxz = tbs__kjr.columns.index(nmipy__ekacu)
                xakpg__mgf = list(tbs__kjr.data)
                xakpg__mgf[esp__lxz] = val
                xakpg__mgf = tuple(xakpg__mgf)
            else:
                are__taftw = tbs__kjr.columns + (nmipy__ekacu,)
                xakpg__mgf = tbs__kjr.data + (val,)
            ctzou__rzk = DataFrameType(xakpg__mgf, index, are__taftw,
                tbs__kjr.dist, tbs__kjr.is_table_format)
        return ctzou__rzk(*args)


SetDfColInfer.prefer_literal = True


def _parse_query_expr(expr, env, columns, cleaned_columns, index_name=None,
    join_cleaned_cols=()):
    khfa__bxb = {}

    def _rewrite_membership_op(self, node, left, right):
        xfv__xwey = node.op
        op = self.visit(xfv__xwey)
        return op, xfv__xwey, left, right

    def _maybe_evaluate_binop(self, op, op_class, lhs, rhs, eval_in_python=
        ('in', 'not in'), maybe_eval_in_python=('==', '!=', '<', '>', '<=',
        '>=')):
        res = op(lhs, rhs)
        return res
    mldbh__rnpt = []


    class NewFuncNode(pd.core.computation.ops.FuncNode):

        def __init__(self, name):
            if (name not in pd.core.computation.ops.MATHOPS or pd.core.
                computation.check._NUMEXPR_INSTALLED and pd.core.
                computation.check_NUMEXPR_VERSION < pd.core.computation.ops
                .LooseVersion('2.6.9') and name in ('floor', 'ceil')):
                if name not in mldbh__rnpt:
                    raise BodoError('"{0}" is not a supported function'.
                        format(name))
            self.name = name
            if name in mldbh__rnpt:
                self.func = name
            else:
                self.func = getattr(np, name)

        def __call__(self, *args):
            return pd.core.computation.ops.MathCall(self, args)

        def __repr__(self):
            return pd.io.formats.printing.pprint_thing(self.name)

    def visit_Attribute(self, node, **kwargs):
        akrit__axs = node.attr
        value = node.value
        xkbuj__pvcrf = pd.core.computation.ops.LOCAL_TAG
        if akrit__axs in ('str', 'dt'):
            try:
                iavmc__mcv = str(self.visit(value))
            except pd.core.computation.ops.UndefinedVariableError as spjk__tcs:
                col_name = spjk__tcs.args[0].split("'")[1]
                raise BodoError(
                    'df.query(): column {} is not found in dataframe columns {}'
                    .format(col_name, columns))
        else:
            iavmc__mcv = str(self.visit(value))
        bbuv__dntb = iavmc__mcv, akrit__axs
        if bbuv__dntb in join_cleaned_cols:
            akrit__axs = join_cleaned_cols[bbuv__dntb]
        name = iavmc__mcv + '.' + akrit__axs
        if name.startswith(xkbuj__pvcrf):
            name = name[len(xkbuj__pvcrf):]
        if akrit__axs in ('str', 'dt'):
            vxd__ewtdk = columns[cleaned_columns.index(iavmc__mcv)]
            khfa__bxb[vxd__ewtdk] = iavmc__mcv
            self.env.scope[name] = 0
            return self.term_type(xkbuj__pvcrf + name, self.env)
        mldbh__rnpt.append(name)
        return NewFuncNode(name)

    def __str__(self):
        if isinstance(self.value, list):
            return '{}'.format(self.value)
        if isinstance(self.value, str):
            return "'{}'".format(self.value)
        return pd.io.formats.printing.pprint_thing(self.name)

    def math__str__(self):
        if self.op in mldbh__rnpt:
            return pd.io.formats.printing.pprint_thing('{0}({1})'.format(
                self.op, ','.join(map(str, self.operands))))
        mrm__whoo = map(lambda a:
            'bodo.hiframes.pd_series_ext.get_series_data({})'.format(str(a)
            ), self.operands)
        op = 'np.{}'.format(self.op)
        nmipy__ekacu = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len({}), 1, None)'
            .format(str(self.operands[0])))
        return pd.io.formats.printing.pprint_thing(
            'bodo.hiframes.pd_series_ext.init_series({0}({1}), {2})'.format
            (op, ','.join(mrm__whoo), nmipy__ekacu))

    def op__str__(self):
        jzhfy__xxgjy = ('({0})'.format(pd.io.formats.printing.pprint_thing(
            hcyyt__umsry)) for hcyyt__umsry in self.operands)
        if self.op == 'in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_isin_dummy({})'.format(
                ', '.join(jzhfy__xxgjy)))
        if self.op == 'not in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_notin_dummy({})'.format
                (', '.join(jzhfy__xxgjy)))
        return pd.io.formats.printing.pprint_thing(' {0} '.format(self.op).
            join(jzhfy__xxgjy))
    vwa__cog = pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op
    xxygd__zbrm = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_evaluate_binop)
    myv__pyqh = pd.core.computation.expr.BaseExprVisitor.visit_Attribute
    mpl__djgo = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_downcast_constants)
    nax__osbdy = pd.core.computation.ops.Term.__str__
    lpsk__fpfqp = pd.core.computation.ops.MathCall.__str__
    askv__fnx = pd.core.computation.ops.Op.__str__
    pyp__hri = pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
    try:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            _rewrite_membership_op)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            _maybe_evaluate_binop)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = (
            visit_Attribute)
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = lambda self, left, right: (left, right)
        pd.core.computation.ops.Term.__str__ = __str__
        pd.core.computation.ops.MathCall.__str__ = math__str__
        pd.core.computation.ops.Op.__str__ = op__str__
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        ocou__oyrv = pd.core.computation.expr.Expr(expr, env=env)
        offm__roy = str(ocou__oyrv)
    except pd.core.computation.ops.UndefinedVariableError as spjk__tcs:
        if not is_overload_none(index_name) and get_overload_const_str(
            index_name) == spjk__tcs.args[0].split("'")[1]:
            raise BodoError(
                "df.query(): Refering to named index ('{}') by name is not supported"
                .format(get_overload_const_str(index_name)))
        else:
            raise BodoError(f'df.query(): undefined variable, {spjk__tcs}')
    finally:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            vwa__cog)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            xxygd__zbrm)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = myv__pyqh
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = mpl__djgo
        pd.core.computation.ops.Term.__str__ = nax__osbdy
        pd.core.computation.ops.MathCall.__str__ = lpsk__fpfqp
        pd.core.computation.ops.Op.__str__ = askv__fnx
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = pyp__hri
    xsd__blv = pd.core.computation.parsing.clean_column_name
    khfa__bxb.update({nxjg__nry: xsd__blv(nxjg__nry) for nxjg__nry in
        columns if xsd__blv(nxjg__nry) in ocou__oyrv.names})
    return ocou__oyrv, offm__roy, khfa__bxb


class DataFrameTupleIterator(types.SimpleIteratorType):

    def __init__(self, col_names, arr_typs):
        self.array_types = arr_typs
        self.col_names = col_names
        yhsy__vnj = ['{}={}'.format(col_names[i], arr_typs[i]) for i in
            range(len(col_names))]
        name = 'itertuples({})'.format(','.join(yhsy__vnj))
        xrqln__qre = namedtuple('Pandas', col_names)
        mserd__lrbs = types.NamedTuple([_get_series_dtype(a) for a in
            arr_typs], xrqln__qre)
        super(DataFrameTupleIterator, self).__init__(name, mserd__lrbs)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


def _get_series_dtype(arr_typ):
    if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
        return pd_timestamp_type
    return arr_typ.dtype


def get_itertuples():
    pass


@infer_global(get_itertuples)
class TypeIterTuples(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) % 2 == 0, 'name and column pairs expected'
        col_names = [a.literal_value for a in args[:len(args) // 2]]
        ixydy__yklx = [if_series_to_array_type(a) for a in args[len(args) //
            2:]]
        assert 'Index' not in col_names[0]
        col_names = ['Index'] + col_names
        ixydy__yklx = [types.Array(types.int64, 1, 'C')] + ixydy__yklx
        bag__thvx = DataFrameTupleIterator(col_names, ixydy__yklx)
        return bag__thvx(*args)


TypeIterTuples.prefer_literal = True


@register_model(DataFrameTupleIterator)
class DataFrameTupleIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        qyoo__ljqjx = [('index', types.EphemeralPointer(types.uintp))] + [(
            'array{}'.format(i), arr) for i, arr in enumerate(fe_type.
            array_types[1:])]
        super(DataFrameTupleIteratorModel, self).__init__(dmm, fe_type,
            qyoo__ljqjx)

    def from_return(self, builder, value):
        return value


@lower_builtin(get_itertuples, types.VarArg(types.Any))
def get_itertuples_impl(context, builder, sig, args):
    pvxk__xwpfv = args[len(args) // 2:]
    xzi__mjah = sig.args[len(sig.args) // 2:]
    wgxbe__kqc = context.make_helper(builder, sig.return_type)
    koq__rudke = context.get_constant(types.intp, 0)
    pnd__cdvz = cgutils.alloca_once_value(builder, koq__rudke)
    wgxbe__kqc.index = pnd__cdvz
    for i, arr in enumerate(pvxk__xwpfv):
        setattr(wgxbe__kqc, 'array{}'.format(i), arr)
    for arr, arr_typ in zip(pvxk__xwpfv, xzi__mjah):
        context.nrt.incref(builder, arr_typ, arr)
    res = wgxbe__kqc._getvalue()
    return impl_ret_new_ref(context, builder, sig.return_type, res)


@lower_builtin('getiter', DataFrameTupleIterator)
def getiter_itertuples(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', DataFrameTupleIterator)
@iternext_impl(RefType.UNTRACKED)
def iternext_itertuples(context, builder, sig, args, result):
    vrltu__bsi, = sig.args
    gfo__qmz, = args
    wgxbe__kqc = context.make_helper(builder, vrltu__bsi, value=gfo__qmz)
    nuop__bptk = signature(types.intp, vrltu__bsi.array_types[1])
    rbt__hjgxu = context.compile_internal(builder, lambda a: len(a),
        nuop__bptk, [wgxbe__kqc.array0])
    index = builder.load(wgxbe__kqc.index)
    keb__irr = builder.icmp(lc.ICMP_SLT, index, rbt__hjgxu)
    result.set_valid(keb__irr)
    with builder.if_then(keb__irr):
        values = [index]
        for i, arr_typ in enumerate(vrltu__bsi.array_types[1:]):
            fwetp__vkvig = getattr(wgxbe__kqc, 'array{}'.format(i))
            if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
                jobt__ewwnv = signature(pd_timestamp_type, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: bodo.
                    hiframes.pd_timestamp_ext.
                    convert_datetime64_to_timestamp(np.int64(a[i])),
                    jobt__ewwnv, [fwetp__vkvig, index])
            else:
                jobt__ewwnv = signature(arr_typ.dtype, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: a[i],
                    jobt__ewwnv, [fwetp__vkvig, index])
            values.append(val)
        value = context.make_tuple(builder, vrltu__bsi.yield_type, values)
        result.yield_(value)
        bthnv__jqhxu = cgutils.increment_index(builder, index)
        builder.store(bthnv__jqhxu, wgxbe__kqc.index)


def _analyze_op_pair_first(self, scope, equiv_set, expr, lhs):
    typ = self.typemap[expr.value.name].first_type
    if not isinstance(typ, types.NamedTuple):
        return None
    lhs = ir.Var(scope, mk_unique_var('tuple_var'), expr.loc)
    self.typemap[lhs.name] = typ
    rhs = ir.Expr.pair_first(expr.value, expr.loc)
    ldxn__our = ir.Assign(rhs, lhs, expr.loc)
    unqdt__sbbd = lhs
    wmwnp__zlth = []
    pjlx__jmt = []
    kuqz__vuo = typ.count
    for i in range(kuqz__vuo):
        xyd__xliyo = ir.Var(unqdt__sbbd.scope, mk_unique_var('{}_size{}'.
            format(unqdt__sbbd.name, i)), unqdt__sbbd.loc)
        tjrff__hiurq = ir.Expr.static_getitem(lhs, i, None, unqdt__sbbd.loc)
        self.calltypes[tjrff__hiurq] = None
        wmwnp__zlth.append(ir.Assign(tjrff__hiurq, xyd__xliyo, unqdt__sbbd.loc)
            )
        self._define(equiv_set, xyd__xliyo, types.intp, tjrff__hiurq)
        pjlx__jmt.append(xyd__xliyo)
    wtk__dqhr = tuple(pjlx__jmt)
    return numba.parfors.array_analysis.ArrayAnalysis.AnalyzeResult(shape=
        wtk__dqhr, pre=[ldxn__our] + wmwnp__zlth)


numba.parfors.array_analysis.ArrayAnalysis._analyze_op_pair_first = (
    _analyze_op_pair_first)
