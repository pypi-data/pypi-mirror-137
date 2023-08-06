"""
Implementation of Series attributes and methods using overload.
"""
import operator
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_builtin, overload, overload_attribute, overload_method, register_jitable
import bodo
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.hiframes.datetime_timedelta_ext import PDTimeDeltaType, datetime_timedelta_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.pd_offsets_ext import is_offsets_type
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType, if_series_to_array_type, is_series_type
from bodo.hiframes.pd_timestamp_ext import PandasTimestampType, pd_timestamp_type
from bodo.hiframes.rolling import is_supported_shift_array_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import BinaryArrayType, binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, string_array_type
from bodo.libs.str_ext import string_type
from bodo.utils.transform import gen_const_tup, is_var_size_item_array_type
from bodo.utils.typing import BodoError, can_replace, check_unsupported_args, dtype_to_array_type, element_type, get_common_scalar_dtype, get_literal_value, get_overload_const_bytes, get_overload_const_int, get_overload_const_str, is_common_scalar_dtype, is_iterable_type, is_literal_type, is_nullable_type, is_overload_bool, is_overload_constant_bool, is_overload_constant_bytes, is_overload_constant_int, is_overload_constant_nan, is_overload_constant_str, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_overload_zero, is_scalar_type, raise_bodo_error, to_nullable_type


@overload_attribute(HeterogeneousSeriesType, 'index', inline='always')
@overload_attribute(SeriesType, 'index', inline='always')
def overload_series_index(s):
    return lambda s: bodo.hiframes.pd_series_ext.get_series_index(s)


@overload_attribute(HeterogeneousSeriesType, 'values', inline='always')
@overload_attribute(SeriesType, 'values', inline='always')
def overload_series_values(s):
    return lambda s: bodo.hiframes.pd_series_ext.get_series_data(s)


@overload_attribute(SeriesType, 'dtype', inline='always')
def overload_series_dtype(s):
    if s.dtype == bodo.string_type:
        raise BodoError('Series.dtype not supported for string Series yet')
    return lambda s: bodo.hiframes.pd_series_ext.get_series_data(s).dtype


@overload_attribute(HeterogeneousSeriesType, 'shape')
@overload_attribute(SeriesType, 'shape')
def overload_series_shape(s):
    return lambda s: (len(bodo.hiframes.pd_series_ext.get_series_data(s)),)


@overload_attribute(HeterogeneousSeriesType, 'ndim', inline='always')
@overload_attribute(SeriesType, 'ndim', inline='always')
def overload_series_ndim(s):
    return lambda s: 1


@overload_attribute(HeterogeneousSeriesType, 'size')
@overload_attribute(SeriesType, 'size')
def overload_series_size(s):
    return lambda s: len(bodo.hiframes.pd_series_ext.get_series_data(s))


@overload_attribute(HeterogeneousSeriesType, 'T', inline='always')
@overload_attribute(SeriesType, 'T', inline='always')
def overload_series_T(s):
    return lambda s: s


@overload_attribute(SeriesType, 'hasnans', inline='always')
def overload_series_hasnans(s):
    return lambda s: s.isna().sum() != 0


@overload_attribute(HeterogeneousSeriesType, 'empty')
@overload_attribute(SeriesType, 'empty')
def overload_series_empty(s):
    return lambda s: len(bodo.hiframes.pd_series_ext.get_series_data(s)) == 0


@overload_attribute(SeriesType, 'dtypes', inline='always')
def overload_series_dtypes(s):
    return lambda s: s.dtype


@overload_attribute(HeterogeneousSeriesType, 'name', inline='always')
@overload_attribute(SeriesType, 'name', inline='always')
def overload_series_name(s):
    return lambda s: bodo.hiframes.pd_series_ext.get_series_name(s)


@overload(len, no_unliteral=True)
def overload_series_len(S):
    if isinstance(S, (SeriesType, HeterogeneousSeriesType)):
        return lambda S: len(bodo.hiframes.pd_series_ext.get_series_data(S))


@overload_method(SeriesType, 'copy', inline='always', no_unliteral=True)
def overload_series_copy(S, deep=True):
    if is_overload_true(deep):

        def impl1(S, deep=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr.copy(),
                index, name)
        return impl1
    if is_overload_false(deep):

        def impl2(S, deep=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
        return impl2

    def impl(S, deep=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        if deep:
            arr = arr.copy()
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
    return impl


@overload_method(SeriesType, 'to_list', no_unliteral=True)
@overload_method(SeriesType, 'tolist', no_unliteral=True)
def overload_series_to_list(S):
    if isinstance(S.dtype, types.Float):

        def impl_float(S):
            ykkpr__edm = list()
            for wccx__zmgv in range(len(S)):
                ykkpr__edm.append(S.iat[wccx__zmgv])
            return ykkpr__edm
        return impl_float

    def impl(S):
        ykkpr__edm = list()
        for wccx__zmgv in range(len(S)):
            if bodo.libs.array_kernels.isna(S.values, wccx__zmgv):
                raise ValueError(
                    'Series.to_list(): Not supported for NA values with non-float dtypes'
                    )
            ykkpr__edm.append(S.iat[wccx__zmgv])
        return ykkpr__edm
    return impl


@overload_method(SeriesType, 'to_numpy', inline='always', no_unliteral=True)
def overload_series_to_numpy(S, dtype=None, copy=False, na_value=None):
    zrc__izp = dict(dtype=dtype, copy=copy, na_value=na_value)
    mio__xes = dict(dtype=None, copy=False, na_value=None)
    check_unsupported_args('Series.to_numpy', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')

    def impl(S, dtype=None, copy=False, na_value=None):
        return S.values
    return impl


@overload_method(SeriesType, 'reset_index', inline='always', no_unliteral=True)
def overload_series_reset_index(S, level=None, drop=False, name=None,
    inplace=False):
    zrc__izp = dict(name=name, inplace=inplace)
    mio__xes = dict(name=None, inplace=False)
    check_unsupported_args('Series.reset_index', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')
    if not bodo.hiframes.dataframe_impl._is_all_levels(S, level):
        raise_bodo_error(
            'Series.reset_index(): only dropping all index levels supported')
    if not is_overload_constant_bool(drop):
        raise_bodo_error(
            "Series.reset_index(): 'drop' parameter should be a constant boolean value"
            )
    if is_overload_true(drop):

        def impl_drop(S, level=None, drop=False, name=None, inplace=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_index_ext.init_range_index(0, len(arr),
                1, None)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
        return impl_drop

    def get_name_literal(name_typ, is_index=False, series_name=None):
        if is_overload_none(name_typ):
            if is_index:
                return 'index' if series_name != 'index' else 'level_0'
            return 0
        if is_literal_type(name_typ):
            return get_literal_value(name_typ)
        else:
            raise BodoError(
                'Series.reset_index() not supported for non-literal series names'
                )
    series_name = get_name_literal(S.name_typ)
    wban__cykhm = get_name_literal(S.index.name_typ, True, series_name)
    cnvh__frj = [wban__cykhm, series_name]
    jfhn__nfueo = (
        'def _impl(S, level=None, drop=False, name=None, inplace=False):\n')
    jfhn__nfueo += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    jfhn__nfueo += """    index = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S))
"""
    jfhn__nfueo += """    df_index = bodo.hiframes.pd_index_ext.init_range_index(0, len(S), 1, None)
"""
    jfhn__nfueo += '    col_var = {}\n'.format(gen_const_tup(cnvh__frj))
    jfhn__nfueo += """    return bodo.hiframes.pd_dataframe_ext.init_dataframe((index, arr), df_index, col_var)
"""
    hqlb__oxys = {}
    exec(jfhn__nfueo, {'bodo': bodo}, hqlb__oxys)
    ypfup__wies = hqlb__oxys['_impl']
    return ypfup__wies


@overload_method(SeriesType, 'isna', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'isnull', inline='always', no_unliteral=True)
def overload_series_isna(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        pnuib__vcui = bodo.libs.array_ops.array_op_isna(arr)
        return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui, index, name
            )
    return impl


@overload_method(SeriesType, 'round', inline='always', no_unliteral=True)
def overload_series_round(S, decimals=0):

    def impl(S, decimals=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(arr)
        pnuib__vcui = bodo.utils.utils.alloc_type(n, arr, (-1,))
        for wccx__zmgv in numba.parfors.parfor.internal_prange(n):
            if pd.isna(arr[wccx__zmgv]):
                bodo.libs.array_kernels.setna(pnuib__vcui, wccx__zmgv)
            else:
                pnuib__vcui[wccx__zmgv] = np.round(arr[wccx__zmgv], decimals)
        return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui, index, name
            )
    return impl


@overload_method(SeriesType, 'sum', inline='always', no_unliteral=True)
def overload_series_sum(S, axis=None, skipna=True, level=None, numeric_only
    =None, min_count=0):
    zrc__izp = dict(level=level, numeric_only=numeric_only)
    mio__xes = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sum', zrc__izp, mio__xes, package_name=
        'pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.sum(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.sum(): skipna argument must be a boolean')
    if not is_overload_int(min_count):
        raise BodoError('Series.sum(): min_count argument must be an integer')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None,
        min_count=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_sum(arr, skipna, min_count)
    return impl


@overload_method(SeriesType, 'prod', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'product', inline='always', no_unliteral=True)
def overload_series_prod(S, axis=None, skipna=True, level=None,
    numeric_only=None, min_count=0):
    zrc__izp = dict(level=level, numeric_only=numeric_only)
    mio__xes = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.product', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.product(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.product(): skipna argument must be a boolean')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None,
        min_count=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_prod(arr, skipna, min_count)
    return impl


@overload_method(SeriesType, 'any', inline='always', no_unliteral=True)
def overload_series_any(S, axis=0, bool_only=None, skipna=True, level=None):
    zrc__izp = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=level)
    mio__xes = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.any', zrc__izp, mio__xes, package_name=
        'pandas', module_name='Series')

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        wbm__ujx = 0
        for wccx__zmgv in numba.parfors.parfor.internal_prange(len(A)):
            dvauy__gss = 0
            if not bodo.libs.array_kernels.isna(A, wccx__zmgv):
                dvauy__gss = int(A[wccx__zmgv])
            wbm__ujx += dvauy__gss
        return wbm__ujx != 0
    return impl


@overload_method(SeriesType, 'equals', inline='always', no_unliteral=True)
def overload_series_equals(S, other):
    if not isinstance(other, SeriesType):
        raise BodoError("Series.equals() 'other' must be a Series")
    if isinstance(S.data, bodo.ArrayItemArrayType):
        raise BodoError(
            'Series.equals() not supported for Series where each element is an array or list'
            )
    if S.data != other.data:
        return lambda S, other: False

    def impl(S, other):
        hzx__mnl = bodo.hiframes.pd_series_ext.get_series_data(S)
        xesst__vhe = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        wbm__ujx = 0
        for wccx__zmgv in numba.parfors.parfor.internal_prange(len(hzx__mnl)):
            dvauy__gss = 0
            dvvi__hap = bodo.libs.array_kernels.isna(hzx__mnl, wccx__zmgv)
            uhnw__maf = bodo.libs.array_kernels.isna(xesst__vhe, wccx__zmgv)
            if dvvi__hap and not uhnw__maf or not dvvi__hap and uhnw__maf:
                dvauy__gss = 1
            elif not dvvi__hap:
                if hzx__mnl[wccx__zmgv] != xesst__vhe[wccx__zmgv]:
                    dvauy__gss = 1
            wbm__ujx += dvauy__gss
        return wbm__ujx == 0
    return impl


@overload_method(SeriesType, 'all', inline='always', no_unliteral=True)
def overload_series_all(S, axis=0, bool_only=None, skipna=True, level=None):
    zrc__izp = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=level)
    mio__xes = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.all', zrc__izp, mio__xes, package_name=
        'pandas', module_name='Series')

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        wbm__ujx = 0
        for wccx__zmgv in numba.parfors.parfor.internal_prange(len(A)):
            dvauy__gss = 0
            if not bodo.libs.array_kernels.isna(A, wccx__zmgv):
                dvauy__gss = int(not A[wccx__zmgv])
            wbm__ujx += dvauy__gss
        return wbm__ujx == 0
    return impl


@overload_method(SeriesType, 'mad', inline='always', no_unliteral=True)
def overload_series_mad(S, axis=None, skipna=True, level=None):
    zrc__izp = dict(level=level)
    mio__xes = dict(level=None)
    check_unsupported_args('Series.mad', zrc__izp, mio__xes, package_name=
        'pandas', module_name='Series')
    if not is_overload_bool(skipna):
        raise BodoError("Series.mad(): 'skipna' argument must be a boolean")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mad(): axis argument not supported')
    psgv__vunnt = types.float64
    gdtz__fgppd = types.float64
    if S.dtype == types.float32:
        psgv__vunnt = types.float32
        gdtz__fgppd = types.float32
    tepb__ypgl = psgv__vunnt(0)
    qonip__ewu = gdtz__fgppd(0)
    oqqll__ksby = gdtz__fgppd(1)

    def impl(S, axis=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        ovt__vtabp = tepb__ypgl
        wbm__ujx = qonip__ewu
        for wccx__zmgv in numba.parfors.parfor.internal_prange(len(A)):
            dvauy__gss = tepb__ypgl
            ifv__hag = qonip__ewu
            if not bodo.libs.array_kernels.isna(A, wccx__zmgv) or not skipna:
                dvauy__gss = A[wccx__zmgv]
                ifv__hag = oqqll__ksby
            ovt__vtabp += dvauy__gss
            wbm__ujx += ifv__hag
        lvvuq__tewdb = bodo.hiframes.series_kernels._mean_handle_nan(ovt__vtabp
            , wbm__ujx)
        tegc__tsl = tepb__ypgl
        for wccx__zmgv in numba.parfors.parfor.internal_prange(len(A)):
            dvauy__gss = tepb__ypgl
            if not bodo.libs.array_kernels.isna(A, wccx__zmgv) or not skipna:
                dvauy__gss = abs(A[wccx__zmgv] - lvvuq__tewdb)
            tegc__tsl += dvauy__gss
        crp__lzjy = bodo.hiframes.series_kernels._mean_handle_nan(tegc__tsl,
            wbm__ujx)
        return crp__lzjy
    return impl


@overload_method(SeriesType, 'mean', inline='always', no_unliteral=True)
def overload_series_mean(S, axis=None, skipna=None, level=None,
    numeric_only=None):
    if not isinstance(S.dtype, types.Number) and S.dtype not in [bodo.
        datetime64ns, types.bool_]:
        raise BodoError(f"Series.mean(): Series with type '{S}' not supported")
    zrc__izp = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    mio__xes = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.mean', zrc__izp, mio__xes, package_name=
        'pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mean(): axis argument not supported')

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_mean(arr)
    return impl


@overload_method(SeriesType, 'sem', inline='always', no_unliteral=True)
def overload_series_sem(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    zrc__izp = dict(level=level, numeric_only=numeric_only)
    mio__xes = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sem', zrc__izp, mio__xes, package_name=
        'pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.sem(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.sem(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.sem(): ddof argument must be an integer')

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        etelr__lwwi = 0
        ezt__mmn = 0
        wbm__ujx = 0
        for wccx__zmgv in numba.parfors.parfor.internal_prange(len(A)):
            dvauy__gss = 0
            ifv__hag = 0
            if not bodo.libs.array_kernels.isna(A, wccx__zmgv) or not skipna:
                dvauy__gss = A[wccx__zmgv]
                ifv__hag = 1
            etelr__lwwi += dvauy__gss
            ezt__mmn += dvauy__gss * dvauy__gss
            wbm__ujx += ifv__hag
        s = ezt__mmn - etelr__lwwi * etelr__lwwi / wbm__ujx
        vvaoo__wer = bodo.hiframes.series_kernels._handle_nan_count_ddof(s,
            wbm__ujx, ddof)
        npqgl__ylm = (vvaoo__wer / wbm__ujx) ** 0.5
        return npqgl__ylm
    return impl


@overload_method(SeriesType, 'kurt', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'kurtosis', inline='always', no_unliteral=True)
def overload_series_kurt(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    zrc__izp = dict(level=level, numeric_only=numeric_only)
    mio__xes = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.kurtosis', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.kurtosis(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError(
            "Series.kurtosis(): 'skipna' argument must be a boolean")

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        etelr__lwwi = 0.0
        ezt__mmn = 0.0
        wpdo__iqmw = 0.0
        ylkw__gqxnk = 0.0
        wbm__ujx = 0
        for wccx__zmgv in numba.parfors.parfor.internal_prange(len(A)):
            dvauy__gss = 0.0
            ifv__hag = 0
            if not bodo.libs.array_kernels.isna(A, wccx__zmgv) or not skipna:
                dvauy__gss = np.float64(A[wccx__zmgv])
                ifv__hag = 1
            etelr__lwwi += dvauy__gss
            ezt__mmn += dvauy__gss ** 2
            wpdo__iqmw += dvauy__gss ** 3
            ylkw__gqxnk += dvauy__gss ** 4
            wbm__ujx += ifv__hag
        vvaoo__wer = bodo.hiframes.series_kernels.compute_kurt(etelr__lwwi,
            ezt__mmn, wpdo__iqmw, ylkw__gqxnk, wbm__ujx)
        return vvaoo__wer
    return impl


@overload_method(SeriesType, 'skew', inline='always', no_unliteral=True)
def overload_series_skew(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    zrc__izp = dict(level=level, numeric_only=numeric_only)
    mio__xes = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.skew', zrc__izp, mio__xes, package_name=
        'pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.skew(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.skew(): skipna argument must be a boolean')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        etelr__lwwi = 0.0
        ezt__mmn = 0.0
        wpdo__iqmw = 0.0
        wbm__ujx = 0
        for wccx__zmgv in numba.parfors.parfor.internal_prange(len(A)):
            dvauy__gss = 0.0
            ifv__hag = 0
            if not bodo.libs.array_kernels.isna(A, wccx__zmgv) or not skipna:
                dvauy__gss = np.float64(A[wccx__zmgv])
                ifv__hag = 1
            etelr__lwwi += dvauy__gss
            ezt__mmn += dvauy__gss ** 2
            wpdo__iqmw += dvauy__gss ** 3
            wbm__ujx += ifv__hag
        vvaoo__wer = bodo.hiframes.series_kernels.compute_skew(etelr__lwwi,
            ezt__mmn, wpdo__iqmw, wbm__ujx)
        return vvaoo__wer
    return impl


@overload_method(SeriesType, 'var', inline='always', no_unliteral=True)
def overload_series_var(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    zrc__izp = dict(level=level, numeric_only=numeric_only)
    mio__xes = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.var', zrc__izp, mio__xes, package_name=
        'pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.var(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.var(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.var(): ddof argument must be an integer')

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_var(arr, skipna, ddof)
    return impl


@overload_method(SeriesType, 'std', inline='always', no_unliteral=True)
def overload_series_std(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    zrc__izp = dict(level=level, numeric_only=numeric_only)
    mio__xes = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.std', zrc__izp, mio__xes, package_name=
        'pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.std(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.std(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.std(): ddof argument must be an integer')

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_std(arr, skipna, ddof)
    return impl


@overload_method(SeriesType, 'dot', inline='always', no_unliteral=True)
def overload_series_dot(S, other):

    def impl(S, other):
        hzx__mnl = bodo.hiframes.pd_series_ext.get_series_data(S)
        xesst__vhe = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        ovhdc__yxtt = 0
        for wccx__zmgv in numba.parfors.parfor.internal_prange(len(hzx__mnl)):
            dlye__cyqtd = hzx__mnl[wccx__zmgv]
            qvc__onra = xesst__vhe[wccx__zmgv]
            ovhdc__yxtt += dlye__cyqtd * qvc__onra
        return ovhdc__yxtt
    return impl


@overload_method(SeriesType, 'cumsum', inline='always', no_unliteral=True)
def overload_series_cumsum(S, axis=None, skipna=True):
    zrc__izp = dict(skipna=skipna)
    mio__xes = dict(skipna=True)
    check_unsupported_args('Series.cumsum', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cumsum(): axis argument not supported')

    def impl(S, axis=None, skipna=True):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(A.cumsum(), index, name)
    return impl


@overload_method(SeriesType, 'cumprod', inline='always', no_unliteral=True)
def overload_series_cumprod(S, axis=None, skipna=True):
    zrc__izp = dict(skipna=skipna)
    mio__xes = dict(skipna=True)
    check_unsupported_args('Series.cumprod', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cumprod(): axis argument not supported')

    def impl(S, axis=None, skipna=True):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(A.cumprod(), index, name
            )
    return impl


@overload_method(SeriesType, 'cummin', inline='always', no_unliteral=True)
def overload_series_cummin(S, axis=None, skipna=True):
    zrc__izp = dict(skipna=skipna)
    mio__xes = dict(skipna=True)
    check_unsupported_args('Series.cummin', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cummin(): axis argument not supported')

    def impl(S, axis=None, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.cummin(arr), index, name)
    return impl


@overload_method(SeriesType, 'cummax', inline='always', no_unliteral=True)
def overload_series_cummax(S, axis=None, skipna=True):
    zrc__izp = dict(skipna=skipna)
    mio__xes = dict(skipna=True)
    check_unsupported_args('Series.cummax', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cummax(): axis argument not supported')

    def impl(S, axis=None, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.cummax(arr), index, name)
    return impl


@overload_method(SeriesType, 'rename', inline='always', no_unliteral=True)
def overload_series_rename(S, index=None, axis=None, copy=True, inplace=
    False, level=None, errors='ignore'):
    if not (index == bodo.string_type or isinstance(index, types.StringLiteral)
        ):
        raise BodoError("Series.rename() 'index' can only be a string")
    zrc__izp = dict(copy=copy, inplace=inplace, level=level, errors=errors)
    mio__xes = dict(copy=True, inplace=False, level=None, errors='ignore')
    check_unsupported_args('Series.rename', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')

    def impl(S, index=None, axis=None, copy=True, inplace=False, level=None,
        errors='ignore'):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        ujon__aeu = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_series_ext.init_series(A, ujon__aeu, index)
    return impl


@overload_method(SeriesType, 'abs', inline='always', no_unliteral=True)
def overload_series_abs(S):

    def impl(S):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(np.abs(A), index, name)
    return impl


@overload_method(SeriesType, 'count', no_unliteral=True)
def overload_series_count(S, level=None):
    zrc__izp = dict(level=level)
    mio__xes = dict(level=None)
    check_unsupported_args('Series.count', zrc__izp, mio__xes, package_name
        ='pandas', module_name='Series')

    def impl(S, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_count(A)
    return impl


@overload_method(SeriesType, 'corr', inline='always', no_unliteral=True)
def overload_series_corr(S, other, method='pearson', min_periods=None):
    zrc__izp = dict(method=method, min_periods=min_periods)
    mio__xes = dict(method='pearson', min_periods=None)
    check_unsupported_args('Series.corr', zrc__izp, mio__xes, package_name=
        'pandas', module_name='Series')

    def impl(S, other, method='pearson', min_periods=None):
        n = S.count()
        xatc__uhqux = S.sum()
        wvihr__byxk = other.sum()
        a = n * (S * other).sum() - xatc__uhqux * wvihr__byxk
        jdohp__tuc = n * (S ** 2).sum() - xatc__uhqux ** 2
        zjq__ieof = n * (other ** 2).sum() - wvihr__byxk ** 2
        return a / np.sqrt(jdohp__tuc * zjq__ieof)
    return impl


@overload_method(SeriesType, 'cov', inline='always', no_unliteral=True)
def overload_series_cov(S, other, min_periods=None, ddof=1):
    zrc__izp = dict(min_periods=min_periods)
    mio__xes = dict(min_periods=None)
    check_unsupported_args('Series.cov', zrc__izp, mio__xes, package_name=
        'pandas', module_name='Series')

    def impl(S, other, min_periods=None, ddof=1):
        xatc__uhqux = S.mean()
        wvihr__byxk = other.mean()
        qtk__wum = ((S - xatc__uhqux) * (other - wvihr__byxk)).sum()
        N = np.float64(S.count() - ddof)
        nonzero_len = S.count() * other.count()
        return _series_cov_helper(qtk__wum, N, nonzero_len)
    return impl


def _series_cov_helper(sum_val, N, nonzero_len):
    return


@overload(_series_cov_helper, no_unliteral=True)
def _overload_series_cov_helper(sum_val, N, nonzero_len):

    def impl(sum_val, N, nonzero_len):
        if not nonzero_len:
            return np.nan
        if N <= 0.0:
            eqovq__ktcu = np.sign(sum_val)
            return np.inf * eqovq__ktcu
        return sum_val / N
    return impl


@overload_method(SeriesType, 'min', inline='always', no_unliteral=True)
def overload_series_min(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    zrc__izp = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    mio__xes = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.min', zrc__izp, mio__xes, package_name=
        'pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.min(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.min(): only ordered categoricals are possible')

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_min(arr)
    return impl


@overload(max, no_unliteral=True)
def overload_series_builtins_max(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.max()
        return impl


@overload(min, no_unliteral=True)
def overload_series_builtins_min(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.min()
        return impl


@overload(sum, no_unliteral=True)
def overload_series_builtins_sum(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.sum()
        return impl


@overload(np.prod, inline='always', no_unliteral=True)
def overload_series_np_prod(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.prod()
        return impl


@overload_method(SeriesType, 'max', inline='always', no_unliteral=True)
def overload_series_max(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    zrc__izp = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    mio__xes = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.max', zrc__izp, mio__xes, package_name=
        'pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.max(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.max(): only ordered categoricals are possible')

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_max(arr)
    return impl


@overload_method(SeriesType, 'idxmin', inline='always', no_unliteral=True)
def overload_series_idxmin(S, axis=0, skipna=True):
    zrc__izp = dict(axis=axis, skipna=skipna)
    mio__xes = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmin', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')
    if not (S.dtype == types.none or bodo.utils.utils.is_np_array_typ(S.
        data) and (S.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
        isinstance(S.dtype, (types.Number, types.Boolean))) or isinstance(S
        .data, (bodo.IntegerArrayType, bodo.CategoricalArrayType)) or S.
        data in [bodo.boolean_array, bodo.datetime_date_array_type]):
        raise BodoError(
            f'Series.idxmin() only supported for numeric array types. Array type: {S.data} not supported.'
            )
    if isinstance(S.data, bodo.CategoricalArrayType) and not S.dtype.ordered:
        raise BodoError(
            'Series.idxmin(): only ordered categoricals are possible')

    def impl(S, axis=0, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.libs.array_ops.array_op_idxmin(arr, index)
    return impl


@overload_method(SeriesType, 'idxmax', inline='always', no_unliteral=True)
def overload_series_idxmax(S, axis=0, skipna=True):
    zrc__izp = dict(axis=axis, skipna=skipna)
    mio__xes = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmax', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')
    if not (S.dtype == types.none or bodo.utils.utils.is_np_array_typ(S.
        data) and (S.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
        isinstance(S.dtype, (types.Number, types.Boolean))) or isinstance(S
        .data, (bodo.IntegerArrayType, bodo.CategoricalArrayType)) or S.
        data in [bodo.boolean_array, bodo.datetime_date_array_type]):
        raise BodoError(
            f'Series.idxmax() only supported for numeric array types. Array type: {S.data} not supported.'
            )
    if isinstance(S.data, bodo.CategoricalArrayType) and not S.dtype.ordered:
        raise BodoError(
            'Series.idxmax(): only ordered categoricals are possible')

    def impl(S, axis=0, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.libs.array_ops.array_op_idxmax(arr, index)
    return impl


@overload_method(SeriesType, 'infer_objects', inline='always')
def overload_series_infer_objects(S):
    return lambda S: S.copy()


@overload_attribute(SeriesType, 'is_monotonic', inline='always')
@overload_attribute(SeriesType, 'is_monotonic_increasing', inline='always')
def overload_series_is_monotonic_increasing(S):
    return lambda S: bodo.libs.array_kernels.series_monotonicity(bodo.
        hiframes.pd_series_ext.get_series_data(S), 1)


@overload_attribute(SeriesType, 'is_monotonic_decreasing', inline='always')
def overload_series_is_monotonic_decreasing(S):
    return lambda S: bodo.libs.array_kernels.series_monotonicity(bodo.
        hiframes.pd_series_ext.get_series_data(S), 2)


@overload_attribute(SeriesType, 'nbytes', inline='always')
def overload_series_nbytes(S):
    return lambda S: bodo.hiframes.pd_series_ext.get_series_data(S).nbytes


@overload_method(SeriesType, 'autocorr', inline='always', no_unliteral=True)
def overload_series_autocorr(S, lag=1):
    return lambda S, lag=1: bodo.libs.array_kernels.autocorr(bodo.hiframes.
        pd_series_ext.get_series_data(S), lag)


@overload_method(SeriesType, 'median', inline='always', no_unliteral=True)
def overload_series_median(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    zrc__izp = dict(level=level, numeric_only=numeric_only)
    mio__xes = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.median', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.median(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.median(): skipna argument must be a boolean')
    return (lambda S, axis=None, skipna=True, level=None, numeric_only=None:
        bodo.libs.array_ops.array_op_median(bodo.hiframes.pd_series_ext.
        get_series_data(S), skipna))


def overload_series_head(S, n=5):

    def impl(S, n=5):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        wwxmq__dhwet = arr[:n]
        bsme__bywut = index[:n]
        return bodo.hiframes.pd_series_ext.init_series(wwxmq__dhwet,
            bsme__bywut, name)
    return impl


@lower_builtin('series.head', SeriesType, types.Integer)
@lower_builtin('series.head', SeriesType, types.Omitted)
def series_head_lower(context, builder, sig, args):
    impl = overload_series_head(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@numba.extending.register_jitable
def tail_slice(k, n):
    if n == 0:
        return k
    return -n


@overload_method(SeriesType, 'tail', inline='always', no_unliteral=True)
def overload_series_tail(S, n=5):
    if not is_overload_int(n):
        raise BodoError("Series.tail(): 'n' must be an Integer")

    def impl(S, n=5):
        phh__yvxs = tail_slice(len(S), n)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        wwxmq__dhwet = arr[phh__yvxs:]
        bsme__bywut = index[phh__yvxs:]
        return bodo.hiframes.pd_series_ext.init_series(wwxmq__dhwet,
            bsme__bywut, name)
    return impl


@overload_method(SeriesType, 'first', inline='always', no_unliteral=True)
def overload_series_first(S, offset):
    xzzy__vqn = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in xzzy__vqn:
        raise BodoError(
            "Series.first(): 'offset' must be a string or a DateOffset")

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            zwx__yzo = index[0]
            mcme__xfwhk = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset, zwx__yzo,
                False))
        else:
            mcme__xfwhk = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        wwxmq__dhwet = arr[:mcme__xfwhk]
        bsme__bywut = index[:mcme__xfwhk]
        return bodo.hiframes.pd_series_ext.init_series(wwxmq__dhwet,
            bsme__bywut, name)
    return impl


@overload_method(SeriesType, 'last', inline='always', no_unliteral=True)
def overload_series_last(S, offset):
    xzzy__vqn = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in xzzy__vqn:
        raise BodoError(
            "Series.last(): 'offset' must be a string or a DateOffset")

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            rwkpd__ydtrg = index[-1]
            mcme__xfwhk = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                rwkpd__ydtrg, True))
        else:
            mcme__xfwhk = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        wwxmq__dhwet = arr[len(arr) - mcme__xfwhk:]
        bsme__bywut = index[len(arr) - mcme__xfwhk:]
        return bodo.hiframes.pd_series_ext.init_series(wwxmq__dhwet,
            bsme__bywut, name)
    return impl


@overload_method(SeriesType, 'nlargest', inline='always', no_unliteral=True)
def overload_series_nlargest(S, n=5, keep='first'):
    zrc__izp = dict(keep=keep)
    mio__xes = dict(keep='first')
    check_unsupported_args('Series.nlargest', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nlargest(): n argument must be an integer')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        rfkp__tlsav = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        pnuib__vcui, dvvg__hryh = bodo.libs.array_kernels.nlargest(arr,
            rfkp__tlsav, n, True, bodo.hiframes.series_kernels.gt_f)
        sbyn__ejk = bodo.utils.conversion.convert_to_index(dvvg__hryh)
        return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
            sbyn__ejk, name)
    return impl


@overload_method(SeriesType, 'nsmallest', inline='always', no_unliteral=True)
def overload_series_nsmallest(S, n=5, keep='first'):
    zrc__izp = dict(keep=keep)
    mio__xes = dict(keep='first')
    check_unsupported_args('Series.nsmallest', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nsmallest(): n argument must be an integer')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        rfkp__tlsav = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        pnuib__vcui, dvvg__hryh = bodo.libs.array_kernels.nlargest(arr,
            rfkp__tlsav, n, False, bodo.hiframes.series_kernels.lt_f)
        sbyn__ejk = bodo.utils.conversion.convert_to_index(dvvg__hryh)
        return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
            sbyn__ejk, name)
    return impl


@overload_method(SeriesType, 'notnull', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'notna', inline='always', no_unliteral=True)
def overload_series_notna(S):
    return lambda S: S.isna() == False


@overload_method(SeriesType, 'astype', inline='always', no_unliteral=True)
def overload_series_astype(S, dtype, copy=True, errors='raise',
    _bodo_nan_to_str=True):
    zrc__izp = dict(errors=errors)
    mio__xes = dict(errors='raise')
    check_unsupported_args('Series.astype', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "Series.astype(): 'dtype' when passed as string must be a constant value"
            )

    def impl(S, dtype, copy=True, errors='raise', _bodo_nan_to_str=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        pnuib__vcui = bodo.utils.conversion.fix_arr_dtype(arr, dtype, copy,
            nan_to_str=_bodo_nan_to_str, from_series=True)
        return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui, index, name
            )
    return impl


@overload_method(SeriesType, 'take', inline='always', no_unliteral=True)
def overload_series_take(S, indices, axis=0, is_copy=True):
    zrc__izp = dict(axis=axis, is_copy=is_copy)
    mio__xes = dict(axis=0, is_copy=True)
    check_unsupported_args('Series.take', zrc__izp, mio__xes, package_name=
        'pandas', module_name='Series')
    if not (is_iterable_type(indices) and isinstance(indices.dtype, types.
        Integer)):
        raise BodoError(
            f"Series.take() 'indices' must be an array-like and contain integers. Found type {indices}."
            )

    def impl(S, indices, axis=0, is_copy=True):
        zyryn__wlaoh = bodo.utils.conversion.coerce_to_ndarray(indices)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr[zyryn__wlaoh],
            index[zyryn__wlaoh], name)
    return impl


@overload_method(SeriesType, 'argsort', inline='always', no_unliteral=True)
def overload_series_argsort(S, axis=0, kind='quicksort', order=None):
    zrc__izp = dict(axis=axis, kind=kind, order=order)
    mio__xes = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Series.argsort', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')

    def impl(S, axis=0, kind='quicksort', order=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        n = len(arr)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        hegp__xtpi = S.notna().values
        if not hegp__xtpi.all():
            pnuib__vcui = np.full(n, -1, np.int64)
            pnuib__vcui[hegp__xtpi] = argsort(arr[hegp__xtpi])
        else:
            pnuib__vcui = argsort(arr)
        return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui, index, name
            )
    return impl


@overload_method(SeriesType, 'sort_index', inline='always', no_unliteral=True)
def overload_series_sort_index(S, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    zrc__izp = dict(axis=axis, level=level, inplace=inplace, kind=kind,
        sort_remaining=sort_remaining, ignore_index=ignore_index, key=key)
    mio__xes = dict(axis=0, level=None, inplace=False, kind='quicksort',
        sort_remaining=True, ignore_index=False, key=None)
    check_unsupported_args('Series.sort_index', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_index(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_index(): 'na_position' should either be 'first' or 'last'"
            )

    def impl(S, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        bxm__jbhqb = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col3_',))
        wndx__zuo = bxm__jbhqb.sort_index(ascending=ascending, inplace=
            inplace, na_position=na_position)
        pnuib__vcui = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            wndx__zuo, 0)
        sbyn__ejk = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            wndx__zuo)
        return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
            sbyn__ejk, name)
    return impl


@overload_method(SeriesType, 'sort_values', inline='always', no_unliteral=True)
def overload_series_sort_values(S, axis=0, ascending=True, inplace=False,
    kind='quicksort', na_position='last', ignore_index=False, key=None):
    zrc__izp = dict(axis=axis, inplace=inplace, kind=kind, ignore_index=
        ignore_index, key=key)
    mio__xes = dict(axis=0, inplace=False, kind='quicksort', ignore_index=
        False, key=None)
    check_unsupported_args('Series.sort_values', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_values(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_values(): 'na_position' should either be 'first' or 'last'"
            )

    def impl(S, axis=0, ascending=True, inplace=False, kind='quicksort',
        na_position='last', ignore_index=False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        bxm__jbhqb = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col_',))
        wndx__zuo = bxm__jbhqb.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=inplace, na_position=na_position)
        pnuib__vcui = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            wndx__zuo, 0)
        sbyn__ejk = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            wndx__zuo)
        return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
            sbyn__ejk, name)
    return impl


def get_bin_inds(bins, arr):
    return arr


@overload(get_bin_inds, inline='always', no_unliteral=True)
def overload_get_bin_inds(bins, arr, is_nullable=True, include_lowest=True):
    assert is_overload_constant_bool(is_nullable)
    yhopo__fyyc = is_overload_true(is_nullable)
    jfhn__nfueo = (
        'def impl(bins, arr, is_nullable=True, include_lowest=True):\n')
    jfhn__nfueo += '  numba.parfors.parfor.init_prange()\n'
    jfhn__nfueo += '  n = len(arr)\n'
    if yhopo__fyyc:
        jfhn__nfueo += (
            '  out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
    else:
        jfhn__nfueo += '  out_arr = np.empty(n, np.int64)\n'
    jfhn__nfueo += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    jfhn__nfueo += '    if bodo.libs.array_kernels.isna(arr, i):\n'
    if yhopo__fyyc:
        jfhn__nfueo += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        jfhn__nfueo += '      out_arr[i] = -1\n'
    jfhn__nfueo += '      continue\n'
    jfhn__nfueo += '    val = arr[i]\n'
    jfhn__nfueo += '    if include_lowest and val == bins[0]:\n'
    jfhn__nfueo += '      ind = 1\n'
    jfhn__nfueo += '    else:\n'
    jfhn__nfueo += '      ind = np.searchsorted(bins, val)\n'
    jfhn__nfueo += '    if ind == 0 or ind == len(bins):\n'
    if yhopo__fyyc:
        jfhn__nfueo += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        jfhn__nfueo += '      out_arr[i] = -1\n'
    jfhn__nfueo += '    else:\n'
    jfhn__nfueo += '      out_arr[i] = ind - 1\n'
    jfhn__nfueo += '  return out_arr\n'
    hqlb__oxys = {}
    exec(jfhn__nfueo, {'bodo': bodo, 'np': np, 'numba': numba}, hqlb__oxys)
    impl = hqlb__oxys['impl']
    return impl


@register_jitable
def _round_frac(x, precision: int):
    if not np.isfinite(x) or x == 0:
        return x
    else:
        jgvf__nntc, uid__ybax = np.divmod(x, 1)
        if jgvf__nntc == 0:
            iyvkj__aye = -int(np.floor(np.log10(abs(uid__ybax)))
                ) - 1 + precision
        else:
            iyvkj__aye = precision
        return np.around(x, iyvkj__aye)


@register_jitable
def _infer_precision(base_precision: int, bins) ->int:
    for precision in range(base_precision, 20):
        ebcr__mhu = np.array([_round_frac(b, precision) for b in bins])
        if len(np.unique(ebcr__mhu)) == len(bins):
            return precision
    return base_precision


def get_bin_labels(bins):
    pass


@overload(get_bin_labels, no_unliteral=True)
def overload_get_bin_labels(bins, right=True, include_lowest=True):
    dtype = np.float64 if isinstance(bins.dtype, types.Integer) else bins.dtype
    if dtype == bodo.datetime64ns:
        qdbl__tcwg = bodo.timedelta64ns(1)

        def impl_dt64(bins, right=True, include_lowest=True):
            knrjq__kos = bins.copy()
            if right and include_lowest:
                knrjq__kos[0] = knrjq__kos[0] - qdbl__tcwg
            hcjo__eaveh = bodo.libs.interval_arr_ext.init_interval_array(
                knrjq__kos[:-1], knrjq__kos[1:])
            return bodo.hiframes.pd_index_ext.init_interval_index(hcjo__eaveh,
                None)
        return impl_dt64

    def impl(bins, right=True, include_lowest=True):
        base_precision = 3
        precision = _infer_precision(base_precision, bins)
        knrjq__kos = np.array([_round_frac(b, precision) for b in bins],
            dtype=dtype)
        if right and include_lowest:
            knrjq__kos[0] = knrjq__kos[0] - 10.0 ** -precision
        hcjo__eaveh = bodo.libs.interval_arr_ext.init_interval_array(knrjq__kos
            [:-1], knrjq__kos[1:])
        return bodo.hiframes.pd_index_ext.init_interval_index(hcjo__eaveh, None
            )
    return impl


def get_output_bin_counts(count_series, nbins):
    pass


@overload(get_output_bin_counts, no_unliteral=True)
def overload_get_output_bin_counts(count_series, nbins):

    def impl(count_series, nbins):
        uwezq__rla = bodo.hiframes.pd_series_ext.get_series_data(count_series)
        ypaq__jbbli = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(count_series))
        pnuib__vcui = np.zeros(nbins, np.int64)
        for wccx__zmgv in range(len(uwezq__rla)):
            pnuib__vcui[ypaq__jbbli[wccx__zmgv]] = uwezq__rla[wccx__zmgv]
        return pnuib__vcui
    return impl


def compute_bins(nbins, min_val, max_val):
    pass


@overload(compute_bins, no_unliteral=True)
def overload_compute_bins(nbins, min_val, max_val, right=True):

    def impl(nbins, min_val, max_val, right=True):
        if nbins < 1:
            raise ValueError('`bins` should be a positive integer.')
        min_val = min_val + 0.0
        max_val = max_val + 0.0
        if np.isinf(min_val) or np.isinf(max_val):
            raise ValueError(
                'cannot specify integer `bins` when input data contains infinity'
                )
        elif min_val == max_val:
            min_val -= 0.001 * abs(min_val) if min_val != 0 else 0.001
            max_val += 0.001 * abs(max_val) if max_val != 0 else 0.001
            bins = np.linspace(min_val, max_val, nbins + 1, endpoint=True)
        else:
            bins = np.linspace(min_val, max_val, nbins + 1, endpoint=True)
            sqymu__vubwv = (max_val - min_val) * 0.001
            if right:
                bins[0] -= sqymu__vubwv
            else:
                bins[-1] += sqymu__vubwv
        return bins
    return impl


@overload_method(SeriesType, 'value_counts', inline='always', no_unliteral=True
    )
def overload_series_value_counts(S, normalize=False, sort=True, ascending=
    False, bins=None, dropna=True, _index_name=None):
    zrc__izp = dict(dropna=dropna)
    mio__xes = dict(dropna=True)
    check_unsupported_args('Series.value_counts', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')
    if not is_overload_constant_bool(normalize):
        raise_bodo_error(
            'Series.value_counts(): normalize argument must be a constant boolean'
            )
    if not is_overload_constant_bool(sort):
        raise_bodo_error(
            'Series.value_counts(): sort argument must be a constant boolean')
    if not is_overload_bool(ascending):
        raise_bodo_error(
            'Series.value_counts(): ascending argument must be a constant boolean'
            )
    rfs__qbhq = not is_overload_none(bins)
    jfhn__nfueo = 'def impl(\n'
    jfhn__nfueo += '    S,\n'
    jfhn__nfueo += '    normalize=False,\n'
    jfhn__nfueo += '    sort=True,\n'
    jfhn__nfueo += '    ascending=False,\n'
    jfhn__nfueo += '    bins=None,\n'
    jfhn__nfueo += '    dropna=True,\n'
    jfhn__nfueo += (
        '    _index_name=None,  # bodo argument. See groupby.value_counts\n')
    jfhn__nfueo += '):\n'
    jfhn__nfueo += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    jfhn__nfueo += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    jfhn__nfueo += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    if rfs__qbhq:
        jfhn__nfueo += '    right = True\n'
        jfhn__nfueo += _gen_bins_handling(bins, S.dtype)
        jfhn__nfueo += '    arr = get_bin_inds(bins, arr)\n'
    jfhn__nfueo += (
        '    in_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
    jfhn__nfueo += "        (arr,), index, ('$_bodo_col2_',)\n"
    jfhn__nfueo += '    )\n'
    jfhn__nfueo += "    count_series = in_df.groupby('$_bodo_col2_').size()\n"
    if rfs__qbhq:
        jfhn__nfueo += """    count_series = bodo.gatherv(count_series, allgather=True, warn_if_rep=False)
"""
        jfhn__nfueo += (
            '    count_arr = get_output_bin_counts(count_series, len(bins) - 1)\n'
            )
        jfhn__nfueo += '    index = get_bin_labels(bins)\n'
    else:
        jfhn__nfueo += """    count_arr = bodo.hiframes.pd_series_ext.get_series_data(count_series)
"""
        jfhn__nfueo += '    ind_arr = bodo.utils.conversion.coerce_to_array(\n'
        jfhn__nfueo += (
            '        bodo.hiframes.pd_series_ext.get_series_index(count_series)\n'
            )
        jfhn__nfueo += '    )\n'
        jfhn__nfueo += """    index = bodo.utils.conversion.index_from_array(ind_arr, name=_index_name)
"""
    jfhn__nfueo += (
        '    res = bodo.hiframes.pd_series_ext.init_series(count_arr, index, name)\n'
        )
    if is_overload_true(sort):
        jfhn__nfueo += '    res = res.sort_values(ascending=ascending)\n'
    if is_overload_true(normalize):
        qqtf__iosa = 'len(S)' if rfs__qbhq else 'count_arr.sum()'
        jfhn__nfueo += f'    res = res / float({qqtf__iosa})\n'
    jfhn__nfueo += '    return res\n'
    hqlb__oxys = {}
    exec(jfhn__nfueo, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, hqlb__oxys)
    impl = hqlb__oxys['impl']
    return impl


def _gen_bins_handling(bins, dtype):
    jfhn__nfueo = ''
    if isinstance(bins, types.Integer):
        jfhn__nfueo += '    min_val = bodo.libs.array_ops.array_op_min(arr)\n'
        jfhn__nfueo += '    max_val = bodo.libs.array_ops.array_op_max(arr)\n'
        if dtype == bodo.datetime64ns:
            jfhn__nfueo += '    min_val = min_val.value\n'
            jfhn__nfueo += '    max_val = max_val.value\n'
        jfhn__nfueo += (
            '    bins = compute_bins(bins, min_val, max_val, right)\n')
        if dtype == bodo.datetime64ns:
            jfhn__nfueo += (
                "    bins = bins.astype(np.int64).view(np.dtype('datetime64[ns]'))\n"
                )
    else:
        jfhn__nfueo += (
            '    bins = bodo.utils.conversion.coerce_to_ndarray(bins)\n')
    return jfhn__nfueo


@overload(pd.cut, inline='always', no_unliteral=True)
def overload_cut(x, bins, right=True, labels=None, retbins=False, precision
    =3, include_lowest=False, duplicates='raise', ordered=True):
    zrc__izp = dict(right=right, labels=labels, retbins=retbins, precision=
        precision, duplicates=duplicates, ordered=ordered)
    mio__xes = dict(right=True, labels=None, retbins=False, precision=3,
        duplicates='raise', ordered=True)
    check_unsupported_args('pandas.cut', zrc__izp, mio__xes, package_name=
        'pandas', module_name='General')
    jfhn__nfueo = 'def impl(\n'
    jfhn__nfueo += '    x,\n'
    jfhn__nfueo += '    bins,\n'
    jfhn__nfueo += '    right=True,\n'
    jfhn__nfueo += '    labels=None,\n'
    jfhn__nfueo += '    retbins=False,\n'
    jfhn__nfueo += '    precision=3,\n'
    jfhn__nfueo += '    include_lowest=False,\n'
    jfhn__nfueo += "    duplicates='raise',\n"
    jfhn__nfueo += '    ordered=True\n'
    jfhn__nfueo += '):\n'
    if isinstance(x, SeriesType):
        jfhn__nfueo += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(x)\n')
        jfhn__nfueo += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(x)\n')
        jfhn__nfueo += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(x)\n')
    else:
        jfhn__nfueo += '    arr = bodo.utils.conversion.coerce_to_array(x)\n'
    jfhn__nfueo += _gen_bins_handling(bins, x.dtype)
    jfhn__nfueo += '    arr = get_bin_inds(bins, arr, False, include_lowest)\n'
    jfhn__nfueo += (
        '    label_index = get_bin_labels(bins, right, include_lowest)\n')
    jfhn__nfueo += """    cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(label_index, ordered, None, None)
"""
    jfhn__nfueo += """    out_arr = bodo.hiframes.pd_categorical_ext.init_categorical_array(arr, cat_dtype)
"""
    if isinstance(x, SeriesType):
        jfhn__nfueo += (
            '    res = bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        jfhn__nfueo += '    return res\n'
    else:
        jfhn__nfueo += '    return out_arr\n'
    hqlb__oxys = {}
    exec(jfhn__nfueo, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, hqlb__oxys)
    impl = hqlb__oxys['impl']
    return impl


def _get_q_list(q):
    return q


@overload(_get_q_list, no_unliteral=True)
def get_q_list_overload(q):
    if is_overload_int(q):
        return lambda q: np.linspace(0, 1, q + 1)
    return lambda q: q


@overload(pd.qcut, inline='always', no_unliteral=True)
def overload_qcut(x, q, labels=None, retbins=False, precision=3, duplicates
    ='raise'):
    zrc__izp = dict(labels=labels, retbins=retbins, precision=precision,
        duplicates=duplicates)
    mio__xes = dict(labels=None, retbins=False, precision=3, duplicates='raise'
        )
    check_unsupported_args('pandas.qcut', zrc__izp, mio__xes, package_name=
        'pandas', module_name='General')
    if not (is_overload_int(q) or is_iterable_type(q)):
        raise BodoError(
            "pd.qcut(): 'q' should be an integer or a list of quantiles")

    def impl(x, q, labels=None, retbins=False, precision=3, duplicates='raise'
        ):
        kxcpa__nps = _get_q_list(q)
        arr = bodo.utils.conversion.coerce_to_array(x)
        bins = bodo.libs.array_ops.array_op_quantile(arr, kxcpa__nps)
        return pd.cut(x, bins, include_lowest=True)
    return impl


@overload_method(SeriesType, 'groupby', inline='always', no_unliteral=True)
def overload_series_groupby(S, by=None, axis=0, level=None, as_index=True,
    sort=True, group_keys=True, squeeze=False, observed=True, dropna=True):
    zrc__izp = dict(axis=axis, sort=sort, group_keys=group_keys, squeeze=
        squeeze, observed=observed, dropna=dropna)
    mio__xes = dict(axis=0, sort=True, group_keys=True, squeeze=False,
        observed=True, dropna=True)
    check_unsupported_args('Series.groupby', zrc__izp, mio__xes,
        package_name='pandas', module_name='GroupBy')
    if not is_overload_true(as_index):
        raise BodoError('as_index=False only valid with DataFrame')
    if is_overload_none(by) and is_overload_none(level):
        raise BodoError("You have to supply one of 'by' and 'level'")
    if not is_overload_none(by) and not is_overload_none(level):
        raise BodoError(
            "Series.groupby(): 'level' argument should be None if 'by' is not None"
            )
    if not is_overload_none(level):
        if not (is_overload_constant_int(level) and get_overload_const_int(
            level) == 0) or isinstance(S.index, bodo.hiframes.
            pd_multi_index_ext.MultiIndexType):
            raise BodoError(
                "Series.groupby(): MultiIndex case or 'level' other than 0 not supported yet"
                )

        def impl_index(S, by=None, axis=0, level=None, as_index=True, sort=
            True, group_keys=True, squeeze=False, observed=True, dropna=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            gcak__iwgt = bodo.utils.conversion.coerce_to_array(index)
            bxm__jbhqb = bodo.hiframes.pd_dataframe_ext.init_dataframe((
                gcak__iwgt, arr), index, (' ', ''))
            return bxm__jbhqb.groupby(' ')['']
        return impl_index
    mbd__zhqq = by
    if isinstance(by, SeriesType):
        mbd__zhqq = by.data
    if isinstance(mbd__zhqq, DecimalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with decimal type is not supported yet.'
            )
    if isinstance(by, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with categorical type is not supported yet.'
            )

    def impl(S, by=None, axis=0, level=None, as_index=True, sort=True,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        gcak__iwgt = bodo.utils.conversion.coerce_to_array(by)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        bxm__jbhqb = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            gcak__iwgt, arr), index, (' ', ''))
        return bxm__jbhqb.groupby(' ')['']
    return impl


@overload_method(SeriesType, 'append', inline='always', no_unliteral=True)
def overload_series_append(S, to_append, ignore_index=False,
    verify_integrity=False):
    zrc__izp = dict(verify_integrity=verify_integrity)
    mio__xes = dict(verify_integrity=False)
    check_unsupported_args('Series.append', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')
    if isinstance(to_append, SeriesType):
        return (lambda S, to_append, ignore_index=False, verify_integrity=
            False: pd.concat((S, to_append), ignore_index=ignore_index,
            verify_integrity=verify_integrity))
    if isinstance(to_append, types.BaseTuple):
        return (lambda S, to_append, ignore_index=False, verify_integrity=
            False: pd.concat((S,) + to_append, ignore_index=ignore_index,
            verify_integrity=verify_integrity))
    return (lambda S, to_append, ignore_index=False, verify_integrity=False:
        pd.concat([S] + to_append, ignore_index=ignore_index,
        verify_integrity=verify_integrity))


@overload_method(SeriesType, 'isin', inline='always', no_unliteral=True)
def overload_series_isin(S, values):
    if bodo.utils.utils.is_array_typ(values):

        def impl_arr(S, values):
            zwc__xskm = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(A)
            pnuib__vcui = np.empty(n, np.bool_)
            bodo.libs.array.array_isin(pnuib__vcui, A, zwc__xskm, False)
            return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                index, name)
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(S, values):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        pnuib__vcui = bodo.libs.array_ops.array_op_isin(A, values)
        return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui, index, name
            )
    return impl


@overload_method(SeriesType, 'quantile', inline='always', no_unliteral=True)
def overload_series_quantile(S, q=0.5, interpolation='linear'):
    zrc__izp = dict(interpolation=interpolation)
    mio__xes = dict(interpolation='linear')
    check_unsupported_args('Series.quantile', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')
    if is_iterable_type(q) and isinstance(q.dtype, types.Number):

        def impl_list(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            pnuib__vcui = bodo.libs.array_ops.array_op_quantile(arr, q)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            index = bodo.hiframes.pd_index_ext.init_numeric_index(bodo.
                utils.conversion.coerce_to_array(q), None)
            return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                index, name)
        return impl_list
    elif isinstance(q, (float, types.Number)) or is_overload_constant_int(q):

        def impl(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            return bodo.libs.array_ops.array_op_quantile(arr, q)
        return impl
    else:
        raise BodoError(
            f'Series.quantile() q type must be float or iterable of floats only.'
            )


@overload_method(SeriesType, 'nunique', inline='always', no_unliteral=True)
def overload_series_nunique(S, dropna=True):
    if not is_overload_bool(dropna):
        raise BodoError('Series.nunique: dropna must be a boolean value')

    def impl(S, dropna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_kernels.nunique(arr, dropna)
    return impl


@overload_method(SeriesType, 'unique', inline='always', no_unliteral=True)
def overload_series_unique(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        vup__lgz = bodo.libs.array_kernels.unique(arr)
        return bodo.allgatherv(vup__lgz, False)
    return impl


@overload_method(SeriesType, 'describe', inline='always', no_unliteral=True)
def overload_series_describe(S, percentiles=None, include=None, exclude=
    None, datetime_is_numeric=True):
    zrc__izp = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    mio__xes = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('Series.describe', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')
    if not (isinstance(S.data, types.Array) and (isinstance(S.data.dtype,
        types.Number) or S.data.dtype == bodo.datetime64ns)
        ) and not isinstance(S.data, IntegerArrayType):
        raise BodoError(f'describe() column input type {S.data} not supported.'
            )
    if S.data.dtype == bodo.datetime64ns:

        def impl_dt(S, percentiles=None, include=None, exclude=None,
            datetime_is_numeric=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
                array_ops.array_op_describe(arr), bodo.utils.conversion.
                convert_to_index(['count', 'mean', 'min', '25%', '50%',
                '75%', 'max']), name)
        return impl_dt

    def impl(S, percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.array_ops.
            array_op_describe(arr), bodo.utils.conversion.convert_to_index(
            ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']), name)
    return impl


@overload_method(SeriesType, 'memory_usage', inline='always', no_unliteral=True
    )
def overload_series_memory_usage(S, index=True, deep=False):
    if is_overload_true(index):

        def impl(S, index=True, deep=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            return arr.nbytes + index.nbytes
        return impl
    else:

        def impl(S, index=True, deep=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            return arr.nbytes
        return impl


def binary_str_fillna_inplace_series_impl(is_binary=False):
    if is_binary:
        wdkxq__yupq = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        wdkxq__yupq = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    jfhn__nfueo = 'def impl(\n'
    jfhn__nfueo += '    S,\n'
    jfhn__nfueo += '    value=None,\n'
    jfhn__nfueo += '    method=None,\n'
    jfhn__nfueo += '    axis=None,\n'
    jfhn__nfueo += '    inplace=False,\n'
    jfhn__nfueo += '    limit=None,\n'
    jfhn__nfueo += '    downcast=None,\n'
    jfhn__nfueo += '):  # pragma: no cover\n'
    jfhn__nfueo += (
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    jfhn__nfueo += (
        '    fill_arr = bodo.hiframes.pd_series_ext.get_series_data(value)\n')
    jfhn__nfueo += '    n = len(in_arr)\n'
    jfhn__nfueo += f'    out_arr = {wdkxq__yupq}(n, -1)\n'
    jfhn__nfueo += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    jfhn__nfueo += '        s = in_arr[j]\n'
    jfhn__nfueo += """        if bodo.libs.array_kernels.isna(in_arr, j) and not bodo.libs.array_kernels.isna(
"""
    jfhn__nfueo += '            fill_arr, j\n'
    jfhn__nfueo += '        ):\n'
    jfhn__nfueo += '            s = fill_arr[j]\n'
    jfhn__nfueo += '        out_arr[j] = s\n'
    jfhn__nfueo += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    dzvhi__oswb = dict()
    exec(jfhn__nfueo, {'bodo': bodo, 'numba': numba}, dzvhi__oswb)
    mbx__hurr = dzvhi__oswb['impl']
    return mbx__hurr


def binary_str_fillna_inplace_impl(is_binary=False):
    if is_binary:
        wdkxq__yupq = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        wdkxq__yupq = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    jfhn__nfueo = 'def impl(S,\n'
    jfhn__nfueo += '     value=None,\n'
    jfhn__nfueo += '    method=None,\n'
    jfhn__nfueo += '    axis=None,\n'
    jfhn__nfueo += '    inplace=False,\n'
    jfhn__nfueo += '    limit=None,\n'
    jfhn__nfueo += '   downcast=None,\n'
    jfhn__nfueo += '):\n'
    jfhn__nfueo += (
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    jfhn__nfueo += '    n = len(in_arr)\n'
    jfhn__nfueo += f'    out_arr = {wdkxq__yupq}(n, -1)\n'
    jfhn__nfueo += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    jfhn__nfueo += '        s = in_arr[j]\n'
    jfhn__nfueo += '        if bodo.libs.array_kernels.isna(in_arr, j):\n'
    jfhn__nfueo += '            s = value\n'
    jfhn__nfueo += '        out_arr[j] = s\n'
    jfhn__nfueo += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    dzvhi__oswb = dict()
    exec(jfhn__nfueo, {'bodo': bodo, 'numba': numba}, dzvhi__oswb)
    mbx__hurr = dzvhi__oswb['impl']
    return mbx__hurr


def fillna_inplace_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    jplow__zfi = bodo.hiframes.pd_series_ext.get_series_data(S)
    thz__vrtk = bodo.hiframes.pd_series_ext.get_series_data(value)
    for wccx__zmgv in numba.parfors.parfor.internal_prange(len(jplow__zfi)):
        s = jplow__zfi[wccx__zmgv]
        if bodo.libs.array_kernels.isna(jplow__zfi, wccx__zmgv
            ) and not bodo.libs.array_kernels.isna(thz__vrtk, wccx__zmgv):
            s = thz__vrtk[wccx__zmgv]
        jplow__zfi[wccx__zmgv] = s


def fillna_inplace_impl(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    jplow__zfi = bodo.hiframes.pd_series_ext.get_series_data(S)
    for wccx__zmgv in numba.parfors.parfor.internal_prange(len(jplow__zfi)):
        s = jplow__zfi[wccx__zmgv]
        if bodo.libs.array_kernels.isna(jplow__zfi, wccx__zmgv):
            s = value
        jplow__zfi[wccx__zmgv] = s


def str_fillna_alloc_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    jplow__zfi = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    thz__vrtk = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(jplow__zfi)
    pnuib__vcui = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
    for mwmx__rozju in numba.parfors.parfor.internal_prange(n):
        s = jplow__zfi[mwmx__rozju]
        if bodo.libs.array_kernels.isna(jplow__zfi, mwmx__rozju
            ) and not bodo.libs.array_kernels.isna(thz__vrtk, mwmx__rozju):
            s = thz__vrtk[mwmx__rozju]
        pnuib__vcui[mwmx__rozju] = s
        if bodo.libs.array_kernels.isna(jplow__zfi, mwmx__rozju
            ) and bodo.libs.array_kernels.isna(thz__vrtk, mwmx__rozju):
            bodo.libs.array_kernels.setna(pnuib__vcui, mwmx__rozju)
    return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui, index, name)


def fillna_series_impl(S, value=None, method=None, axis=None, inplace=False,
    limit=None, downcast=None):
    jplow__zfi = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    thz__vrtk = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(jplow__zfi)
    pnuib__vcui = bodo.utils.utils.alloc_type(n, jplow__zfi.dtype, (-1,))
    for wccx__zmgv in numba.parfors.parfor.internal_prange(n):
        s = jplow__zfi[wccx__zmgv]
        if bodo.libs.array_kernels.isna(jplow__zfi, wccx__zmgv
            ) and not bodo.libs.array_kernels.isna(thz__vrtk, wccx__zmgv):
            s = thz__vrtk[wccx__zmgv]
        pnuib__vcui[wccx__zmgv] = s
    return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui, index, name)


@overload_method(SeriesType, 'fillna', no_unliteral=True)
def overload_series_fillna(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    zrc__izp = dict(limit=limit, downcast=downcast)
    mio__xes = dict(limit=None, downcast=None)
    check_unsupported_args('Series.fillna', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')
    prk__dkp = not is_overload_none(value)
    hyh__umxgw = not is_overload_none(method)
    if prk__dkp and hyh__umxgw:
        raise BodoError(
            "Series.fillna(): Cannot specify both 'value' and 'method'.")
    if not prk__dkp and not hyh__umxgw:
        raise BodoError(
            "Series.fillna(): Must specify one of 'value' and 'method'.")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.fillna(): axis argument not supported')
    elif is_iterable_type(value) and not isinstance(value, SeriesType):
        raise BodoError('Series.fillna(): "value" parameter cannot be a list')
    elif is_var_size_item_array_type(S.data
        ) and not S.dtype == bodo.string_type:
        raise BodoError(
            f'Series.fillna() with inplace=True not supported for {S.dtype} values yet.'
            )
    if not is_overload_constant_bool(inplace):
        raise_bodo_error(
            "Series.fillna(): 'inplace' argument must be a constant boolean")
    if hyh__umxgw:
        if is_overload_true(inplace):
            raise BodoError(
                "Series.fillna() with inplace=True not supported with 'method' argument yet."
                )
        dwu__jsj = (
            "Series.fillna(): 'method' argument if provided must be a constant string and one of ('backfill', 'bfill', 'pad' 'ffill')."
            )
        if not is_overload_constant_str(method):
            raise_bodo_error(dwu__jsj)
        elif get_overload_const_str(method) not in ('backfill', 'bfill',
            'pad', 'ffill'):
            raise BodoError(dwu__jsj)
    ohr__jxewb = element_type(S.data)
    dpt__ghllh = None
    if prk__dkp:
        dpt__ghllh = element_type(types.unliteral(value))
    if dpt__ghllh and not can_replace(ohr__jxewb, dpt__ghllh):
        raise BodoError(
            f'Series.fillna(): Cannot use value type {dpt__ghllh} with series type {ohr__jxewb}'
            )
    if is_overload_true(inplace):
        if S.dtype == bodo.string_type:
            if is_overload_constant_str(value) and get_overload_const_str(value
                ) == '':
                return (lambda S, value=None, method=None, axis=None,
                    inplace=False, limit=None, downcast=None: bodo.libs.
                    str_arr_ext.set_null_bits_to_value(bodo.hiframes.
                    pd_series_ext.get_series_data(S), -1))
            if isinstance(value, SeriesType):
                return binary_str_fillna_inplace_series_impl(is_binary=False)
            return binary_str_fillna_inplace_impl(is_binary=False)
        if S.dtype == bodo.bytes_type:
            if is_overload_constant_bytes(value) and get_overload_const_bytes(
                value) == b'':
                return (lambda S, value=None, method=None, axis=None,
                    inplace=False, limit=None, downcast=None: bodo.libs.
                    str_arr_ext.set_null_bits_to_value(bodo.hiframes.
                    pd_series_ext.get_series_data(S), -1))
            if isinstance(value, SeriesType):
                return binary_str_fillna_inplace_series_impl(is_binary=True)
            return binary_str_fillna_inplace_impl(is_binary=True)
        else:
            if isinstance(value, SeriesType):
                return fillna_inplace_series_impl
            return fillna_inplace_impl
    else:
        gis__mrv = S.data
        if isinstance(value, SeriesType):

            def fillna_series_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                jplow__zfi = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                thz__vrtk = bodo.hiframes.pd_series_ext.get_series_data(value)
                n = len(jplow__zfi)
                pnuib__vcui = bodo.utils.utils.alloc_type(n, gis__mrv, (-1,))
                for wccx__zmgv in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(jplow__zfi, wccx__zmgv
                        ) and bodo.libs.array_kernels.isna(thz__vrtk,
                        wccx__zmgv):
                        bodo.libs.array_kernels.setna(pnuib__vcui, wccx__zmgv)
                        continue
                    if bodo.libs.array_kernels.isna(jplow__zfi, wccx__zmgv):
                        pnuib__vcui[wccx__zmgv
                            ] = bodo.utils.conversion.unbox_if_timestamp(
                            thz__vrtk[wccx__zmgv])
                        continue
                    pnuib__vcui[wccx__zmgv
                        ] = bodo.utils.conversion.unbox_if_timestamp(jplow__zfi
                        [wccx__zmgv])
                return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                    index, name)
            return fillna_series_impl
        if hyh__umxgw:
            fxqw__cgp = (types.unicode_type, types.bool_, bodo.datetime64ns,
                bodo.timedelta64ns)
            if not isinstance(ohr__jxewb, (types.Integer, types.Float)
                ) and ohr__jxewb not in fxqw__cgp:
                raise BodoError(
                    f"Series.fillna(): series of type {ohr__jxewb} are not supported with 'method' argument."
                    )

            def fillna_method_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                jplow__zfi = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                pnuib__vcui = bodo.libs.array_kernels.ffill_bfill_arr(
                    jplow__zfi, method)
                return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                    index, name)
            return fillna_method_impl

        def fillna_impl(S, value=None, method=None, axis=None, inplace=
            False, limit=None, downcast=None):
            value = bodo.utils.conversion.unbox_if_timestamp(value)
            jplow__zfi = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(jplow__zfi)
            pnuib__vcui = bodo.utils.utils.alloc_type(n, gis__mrv, (-1,))
            for wccx__zmgv in numba.parfors.parfor.internal_prange(n):
                s = bodo.utils.conversion.unbox_if_timestamp(jplow__zfi[
                    wccx__zmgv])
                if bodo.libs.array_kernels.isna(jplow__zfi, wccx__zmgv):
                    s = value
                pnuib__vcui[wccx__zmgv] = s
            return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                index, name)
        return fillna_impl


def create_fillna_specific_method_overload(overload_name):

    def overload_series_fillna_specific_method(S, axis=None, inplace=False,
        limit=None, downcast=None):
        plk__pkabu = {'ffill': 'ffill', 'bfill': 'bfill', 'pad': 'ffill',
            'backfill': 'bfill'}[overload_name]
        zrc__izp = dict(limit=limit, downcast=downcast)
        mio__xes = dict(limit=None, downcast=None)
        check_unsupported_args(f'Series.{overload_name}', zrc__izp,
            mio__xes, package_name='pandas', module_name='Series')
        if not (is_overload_none(axis) or is_overload_zero(axis)):
            raise BodoError(
                f'Series.{overload_name}(): axis argument not supported')
        ohr__jxewb = element_type(S.data)
        fxqw__cgp = (types.unicode_type, types.bool_, bodo.datetime64ns,
            bodo.timedelta64ns)
        if not isinstance(ohr__jxewb, (types.Integer, types.Float)
            ) and ohr__jxewb not in fxqw__cgp:
            raise BodoError(
                f'Series.{overload_name}(): series of type {ohr__jxewb} are not supported.'
                )

        def impl(S, axis=None, inplace=False, limit=None, downcast=None):
            jplow__zfi = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            pnuib__vcui = bodo.libs.array_kernels.ffill_bfill_arr(jplow__zfi,
                plk__pkabu)
            return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                index, name)
        return impl
    return overload_series_fillna_specific_method


fillna_specific_methods = 'ffill', 'bfill', 'pad', 'backfill'


def _install_fillna_specific_methods():
    for overload_name in fillna_specific_methods:
        fnk__oqjmi = create_fillna_specific_method_overload(overload_name)
        overload_method(SeriesType, overload_name, no_unliteral=True)(
            fnk__oqjmi)


_install_fillna_specific_methods()


def check_unsupported_types(S, to_replace, value):
    if any(bodo.utils.utils.is_array_typ(x, True) for x in [S.dtype,
        to_replace, value]):
        lfpid__dab = (
            'Series.replace(): only support with Scalar, List, or Dictionary')
        raise BodoError(lfpid__dab)
    elif isinstance(to_replace, types.DictType) and not is_overload_none(value
        ):
        lfpid__dab = (
            "Series.replace(): 'value' must be None when 'to_replace' is a dictionary"
            )
        raise BodoError(lfpid__dab)
    elif any(isinstance(x, (PandasTimestampType, PDTimeDeltaType)) for x in
        [to_replace, value]):
        lfpid__dab = (
            f'Series.replace(): Not supported for types {to_replace} and {value}'
            )
        raise BodoError(lfpid__dab)


def series_replace_error_checking(S, to_replace, value, inplace, limit,
    regex, method):
    zrc__izp = dict(inplace=inplace, limit=limit, regex=regex, method=method)
    otxw__xcxaq = dict(inplace=False, limit=None, regex=False, method='pad')
    check_unsupported_args('Series.replace', zrc__izp, otxw__xcxaq,
        package_name='pandas', module_name='Series')
    check_unsupported_types(S, to_replace, value)


@overload_method(SeriesType, 'replace', inline='always', no_unliteral=True)
def overload_series_replace(S, to_replace=None, value=None, inplace=False,
    limit=None, regex=False, method='pad'):
    series_replace_error_checking(S, to_replace, value, inplace, limit,
        regex, method)
    ohr__jxewb = element_type(S.data)
    if isinstance(to_replace, types.DictType):
        oba__acbp = element_type(to_replace.key_type)
        dpt__ghllh = element_type(to_replace.value_type)
    else:
        oba__acbp = element_type(to_replace)
        dpt__ghllh = element_type(value)
    hkm__jhyzk = None
    if ohr__jxewb != types.unliteral(oba__acbp):
        if bodo.utils.typing.equality_always_false(ohr__jxewb, types.
            unliteral(oba__acbp)
            ) or not bodo.utils.typing.types_equality_exists(ohr__jxewb,
            oba__acbp):

            def impl(S, to_replace=None, value=None, inplace=False, limit=
                None, regex=False, method='pad'):
                return S.copy()
            return impl
        if isinstance(ohr__jxewb, (types.Float, types.Integer)
            ) or ohr__jxewb == np.bool_:
            hkm__jhyzk = ohr__jxewb
    if not can_replace(ohr__jxewb, types.unliteral(dpt__ghllh)):

        def impl(S, to_replace=None, value=None, inplace=False, limit=None,
            regex=False, method='pad'):
            return S.copy()
        return impl
    qbgjl__yclrs = S.data
    if isinstance(qbgjl__yclrs, CategoricalArrayType):

        def cat_impl(S, to_replace=None, value=None, inplace=False, limit=
            None, regex=False, method='pad'):
            jplow__zfi = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(jplow__zfi.
                replace(to_replace, value), index, name)
        return cat_impl

    def impl(S, to_replace=None, value=None, inplace=False, limit=None,
        regex=False, method='pad'):
        jplow__zfi = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        n = len(jplow__zfi)
        pnuib__vcui = bodo.utils.utils.alloc_type(n, qbgjl__yclrs, (-1,))
        fjew__xrx = build_replace_dict(to_replace, value, hkm__jhyzk)
        for wccx__zmgv in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(jplow__zfi, wccx__zmgv):
                bodo.libs.array_kernels.setna(pnuib__vcui, wccx__zmgv)
                continue
            s = jplow__zfi[wccx__zmgv]
            if s in fjew__xrx:
                s = fjew__xrx[s]
            pnuib__vcui[wccx__zmgv] = s
        return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui, index, name
            )
    return impl


def build_replace_dict(to_replace, value, key_dtype_conv):
    pass


@overload(build_replace_dict)
def _build_replace_dict(to_replace, value, key_dtype_conv):
    mtxz__shhm = isinstance(to_replace, (types.Number, Decimal128Type)
        ) or to_replace in [bodo.string_type, types.boolean, bodo.bytes_type]
    ymmp__ujuy = is_iterable_type(to_replace)
    bov__lqi = isinstance(value, (types.Number, Decimal128Type)) or value in [
        bodo.string_type, bodo.bytes_type, types.boolean]
    lyjuu__rxaqb = is_iterable_type(value)
    if mtxz__shhm and bov__lqi:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                fjew__xrx = {}
                fjew__xrx[key_dtype_conv(to_replace)] = value
                return fjew__xrx
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            fjew__xrx = {}
            fjew__xrx[to_replace] = value
            return fjew__xrx
        return impl
    if ymmp__ujuy and bov__lqi:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                fjew__xrx = {}
                for ndbeg__zlent in to_replace:
                    fjew__xrx[key_dtype_conv(ndbeg__zlent)] = value
                return fjew__xrx
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            fjew__xrx = {}
            for ndbeg__zlent in to_replace:
                fjew__xrx[ndbeg__zlent] = value
            return fjew__xrx
        return impl
    if ymmp__ujuy and lyjuu__rxaqb:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                fjew__xrx = {}
                assert len(to_replace) == len(value
                    ), 'To_replace and value lengths must be the same'
                for wccx__zmgv in range(len(to_replace)):
                    fjew__xrx[key_dtype_conv(to_replace[wccx__zmgv])] = value[
                        wccx__zmgv]
                return fjew__xrx
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            fjew__xrx = {}
            assert len(to_replace) == len(value
                ), 'To_replace and value lengths must be the same'
            for wccx__zmgv in range(len(to_replace)):
                fjew__xrx[to_replace[wccx__zmgv]] = value[wccx__zmgv]
            return fjew__xrx
        return impl
    if isinstance(to_replace, numba.types.DictType) and is_overload_none(value
        ):
        return lambda to_replace, value, key_dtype_conv: to_replace
    raise BodoError(
        'Series.replace(): Not supported for types to_replace={} and value={}'
        .format(to_replace, value))


@overload_method(SeriesType, 'diff', inline='always', no_unliteral=True)
def overload_series_diff(S, periods=1):
    if not (isinstance(S.data, types.Array) and (isinstance(S.data.dtype,
        types.Number) or S.data.dtype == bodo.datetime64ns)):
        raise BodoError(
            f'Series.diff() column input type {S.data} not supported.')
    if not is_overload_int(periods):
        raise BodoError("Series.diff(): 'periods' input must be an integer.")
    if S.data == types.Array(bodo.datetime64ns, 1, 'C'):

        def impl_datetime(S, periods=1):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            pnuib__vcui = bodo.hiframes.series_impl.dt64_arr_sub(arr, bodo.
                hiframes.rolling.shift(arr, periods, False))
            return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                index, name)
        return impl_datetime

    def impl(S, periods=1):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        pnuib__vcui = arr - bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui, index, name
            )
    return impl


@overload_method(SeriesType, 'explode', inline='always', no_unliteral=True)
def overload_series_explode(S, ignore_index=False):
    from bodo.hiframes.split_impl import string_array_split_view_type
    zrc__izp = dict(ignore_index=ignore_index)
    lmk__geclm = dict(ignore_index=False)
    check_unsupported_args('Series.explode', zrc__izp, lmk__geclm,
        package_name='pandas', module_name='Series')
    if not (isinstance(S.data, ArrayItemArrayType) or S.data ==
        string_array_split_view_type):
        return lambda S, ignore_index=False: S.copy()

    def impl(S, ignore_index=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        rfkp__tlsav = bodo.utils.conversion.index_to_array(index)
        pnuib__vcui, hexe__dor = bodo.libs.array_kernels.explode(arr,
            rfkp__tlsav)
        sbyn__ejk = bodo.utils.conversion.index_from_array(hexe__dor)
        return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
            sbyn__ejk, name)
    return impl


@overload(np.digitize, inline='always', no_unliteral=True)
def overload_series_np_digitize(x, bins, right=False):
    if isinstance(x, SeriesType):

        def impl(x, bins, right=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(x)
            return np.digitize(arr, bins, right)
        return impl


@overload(np.argmax, inline='always', no_unliteral=True)
def argmax_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            gpsoh__kjjkh = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for wccx__zmgv in numba.parfors.parfor.internal_prange(n):
                gpsoh__kjjkh[wccx__zmgv] = np.argmax(a[wccx__zmgv])
            return gpsoh__kjjkh
        return impl


@overload(np.argmin, inline='always', no_unliteral=True)
def argmin_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            nwqez__ohbvd = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for wccx__zmgv in numba.parfors.parfor.internal_prange(n):
                nwqez__ohbvd[wccx__zmgv] = np.argmin(a[wccx__zmgv])
            return nwqez__ohbvd
        return impl


def overload_series_np_dot(a, b, out=None):
    if (isinstance(a, SeriesType) or isinstance(b, SeriesType)
        ) and not is_overload_none(out):
        raise BodoError("np.dot(): 'out' parameter not supported yet")
    if isinstance(a, SeriesType):

        def impl(a, b, out=None):
            arr = bodo.hiframes.pd_series_ext.get_series_data(a)
            return np.dot(arr, b)
        return impl
    if isinstance(b, SeriesType):

        def impl(a, b, out=None):
            arr = bodo.hiframes.pd_series_ext.get_series_data(b)
            return np.dot(a, arr)
        return impl


overload(np.dot, inline='always', no_unliteral=True)(overload_series_np_dot)
overload(operator.matmul, inline='always', no_unliteral=True)(
    overload_series_np_dot)


@overload_method(SeriesType, 'dropna', inline='always', no_unliteral=True)
def overload_series_dropna(S, axis=0, inplace=False, how=None):
    zrc__izp = dict(axis=axis, inplace=inplace, how=how)
    cpp__ovm = dict(axis=0, inplace=False, how=None)
    check_unsupported_args('Series.dropna', zrc__izp, cpp__ovm,
        package_name='pandas', module_name='Series')
    if S.dtype == bodo.string_type:

        def dropna_str_impl(S, axis=0, inplace=False, how=None):
            jplow__zfi = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            hegp__xtpi = S.notna().values
            rfkp__tlsav = bodo.utils.conversion.extract_index_array(S)
            sbyn__ejk = bodo.utils.conversion.convert_to_index(rfkp__tlsav[
                hegp__xtpi])
            pnuib__vcui = (bodo.hiframes.series_kernels.
                _series_dropna_str_alloc_impl_inner(jplow__zfi))
            return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                sbyn__ejk, name)
        return dropna_str_impl
    else:

        def dropna_impl(S, axis=0, inplace=False, how=None):
            jplow__zfi = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            rfkp__tlsav = bodo.utils.conversion.extract_index_array(S)
            hegp__xtpi = S.notna().values
            sbyn__ejk = bodo.utils.conversion.convert_to_index(rfkp__tlsav[
                hegp__xtpi])
            pnuib__vcui = jplow__zfi[hegp__xtpi]
            return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                sbyn__ejk, name)
        return dropna_impl


@overload_method(SeriesType, 'shift', inline='always', no_unliteral=True)
def overload_series_shift(S, periods=1, freq=None, axis=0, fill_value=None):
    zrc__izp = dict(freq=freq, axis=axis, fill_value=fill_value)
    mio__xes = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('Series.shift', zrc__izp, mio__xes, package_name
        ='pandas', module_name='Series')
    if not is_supported_shift_array_type(S.data):
        raise BodoError(
            f"Series.shift(): Series input type '{S.data.dtype}' not supported yet."
            )
    if not is_overload_int(periods):
        raise BodoError("Series.shift(): 'periods' input must be an integer.")

    def impl(S, periods=1, freq=None, axis=0, fill_value=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        pnuib__vcui = bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui, index, name
            )
    return impl


@overload_method(SeriesType, 'pct_change', inline='always', no_unliteral=True)
def overload_series_pct_change(S, periods=1, fill_method='pad', limit=None,
    freq=None):
    zrc__izp = dict(fill_method=fill_method, limit=limit, freq=freq)
    mio__xes = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('Series.pct_change', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')
    if not is_overload_int(periods):
        raise BodoError(
            'Series.pct_change(): periods argument must be an Integer')

    def impl(S, periods=1, fill_method='pad', limit=None, freq=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        pnuib__vcui = bodo.hiframes.rolling.pct_change(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui, index, name
            )
    return impl


@overload_method(SeriesType, 'where', inline='always', no_unliteral=True)
def overload_series_where(S, cond, other=np.nan, inplace=False, axis=None,
    level=None, errors='raise', try_cast=False):
    _validate_arguments_mask_where('Series.where', S, cond, other, inplace,
        axis, level, errors, try_cast)

    def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None,
        errors='raise', try_cast=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        pnuib__vcui = bodo.hiframes.series_impl.where_impl(cond, arr, other)
        return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui, index, name
            )
    return impl


@overload_method(SeriesType, 'mask', inline='always', no_unliteral=True)
def overload_series_mask(S, cond, other=np.nan, inplace=False, axis=None,
    level=None, errors='raise', try_cast=False):
    _validate_arguments_mask_where('Series.mask', S, cond, other, inplace,
        axis, level, errors, try_cast)

    def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None,
        errors='raise', try_cast=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        pnuib__vcui = bodo.hiframes.series_impl.where_impl(~cond, arr, other)
        return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui, index, name
            )
    return impl


def _validate_arguments_mask_where(func_name, S, cond, other, inplace, axis,
    level, errors, try_cast):
    zrc__izp = dict(inplace=inplace, level=level, errors=errors, try_cast=
        try_cast)
    mio__xes = dict(inplace=False, level=None, errors='raise', try_cast=False)
    check_unsupported_args(f'{func_name}', zrc__izp, mio__xes, package_name
        ='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error(f'{func_name}(): axis argument not supported')
    if not (isinstance(S.data, types.Array) or isinstance(S.data,
        BooleanArrayType) or isinstance(S.data, IntegerArrayType) or bodo.
        utils.utils.is_array_typ(S.data, False) and S.dtype in [bodo.
        string_type, bodo.bytes_type] or isinstance(S.data, bodo.
        CategoricalArrayType) and S.dtype.elem_type not in [bodo.
        datetime64ns, bodo.timedelta64ns, bodo.pd_timestamp_type, bodo.
        pd_timedelta_type]):
        raise BodoError(
            f'{func_name}() Series data with type {S.data} not yet supported')
    if not (isinstance(cond, (SeriesType, types.Array, BooleanArrayType)) and
        cond.ndim == 1 and cond.dtype == types.bool_):
        raise BodoError(
            f"{func_name}() 'cond' argument must be a Series or 1-dim array of booleans"
            )
    porgy__jzh = is_overload_constant_nan(other)
    if not (porgy__jzh or is_scalar_type(other) or isinstance(other, types.
        Array) and other.ndim == 1 or isinstance(other, SeriesType) and (
        isinstance(S.data, types.Array) or S.dtype in [bodo.string_type,
        bodo.bytes_type]) or isinstance(other, StringArrayType) and (S.
        dtype == bodo.string_type or isinstance(S.data, bodo.
        CategoricalArrayType) and S.dtype.elem_type == bodo.string_type) or
        isinstance(other, BinaryArrayType) and (S.dtype == bodo.bytes_type or
        isinstance(S.data, bodo.CategoricalArrayType) and S.dtype.elem_type ==
        bodo.bytes_type) or (not isinstance(other, (StringArrayType,
        BinaryArrayType)) and (isinstance(S.data.dtype, types.Integer) and
        (bodo.utils.utils.is_array_typ(other) and isinstance(other.dtype,
        types.Integer) or is_series_type(other) and isinstance(other.data.
        dtype, types.Integer))) or (bodo.utils.utils.is_array_typ(other) and
        S.data.dtype == other.dtype or is_series_type(other) and S.data.
        dtype == other.data.dtype)) and (isinstance(S.data,
        BooleanArrayType) or isinstance(S.data, IntegerArrayType))):
        raise BodoError(
            f"{func_name}() 'other' must be a scalar, non-categorical series, 1-dim numpy array or StringArray with a matching type for Series."
            )
    if isinstance(S.dtype, bodo.PDCategoricalDtype):
        tqz__otpxv = S.dtype.elem_type
    else:
        tqz__otpxv = S.dtype
    if is_iterable_type(other):
        qiasi__vsmui = other.dtype
    elif porgy__jzh:
        qiasi__vsmui = types.float64
    else:
        qiasi__vsmui = types.unliteral(other)
    if not is_common_scalar_dtype([tqz__otpxv, qiasi__vsmui]):
        raise BodoError(
            f"{func_name}() series and 'other' must share a common type.")


def create_explicit_binary_op_overload(op):

    def overload_series_explicit_binary_op(S, other, level=None, fill_value
        =None, axis=0):
        zrc__izp = dict(level=level, axis=axis)
        mio__xes = dict(level=None, axis=0)
        check_unsupported_args('series.{}'.format(op.__name__), zrc__izp,
            mio__xes, package_name='pandas', module_name='Series')
        xbg__xljh = other == string_type or is_overload_constant_str(other)
        tycgt__enrnc = is_iterable_type(other) and other.dtype == string_type
        gdth__nkvar = S.dtype == string_type and (op == operator.add and (
            xbg__xljh or tycgt__enrnc) or op == operator.mul and isinstance
            (other, types.Integer))
        ovj__mxe = S.dtype == bodo.timedelta64ns
        xynak__rcqxa = S.dtype == bodo.datetime64ns
        lmed__wmpr = is_iterable_type(other) and (other.dtype ==
            datetime_timedelta_type or other.dtype == bodo.timedelta64ns)
        zkf__qjlsi = is_iterable_type(other) and (other.dtype ==
            datetime_datetime_type or other.dtype == pd_timestamp_type or 
            other.dtype == bodo.datetime64ns)
        lryof__szpp = ovj__mxe and (lmed__wmpr or zkf__qjlsi
            ) or xynak__rcqxa and lmed__wmpr
        lryof__szpp = lryof__szpp and op == operator.add
        if not (isinstance(S.dtype, types.Number) or gdth__nkvar or lryof__szpp
            ):
            raise BodoError(f'Unsupported types for Series.{op.__name__}')
        eoe__ikml = numba.core.registry.cpu_target.typing_context
        if is_scalar_type(other):
            args = S.data, other
            qbgjl__yclrs = eoe__ikml.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and qbgjl__yclrs == types.Array(types.bool_, 1, 'C'):
                qbgjl__yclrs = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                other = bodo.utils.conversion.unbox_if_timestamp(other)
                n = len(arr)
                pnuib__vcui = bodo.utils.utils.alloc_type(n, qbgjl__yclrs,
                    (-1,))
                for wccx__zmgv in numba.parfors.parfor.internal_prange(n):
                    ernu__mpfpq = bodo.libs.array_kernels.isna(arr, wccx__zmgv)
                    if ernu__mpfpq:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(pnuib__vcui,
                                wccx__zmgv)
                        else:
                            pnuib__vcui[wccx__zmgv] = op(fill_value, other)
                    else:
                        pnuib__vcui[wccx__zmgv] = op(arr[wccx__zmgv], other)
                return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                    index, name)
            return impl_scalar
        args = S.data, types.Array(other.dtype, 1, 'C')
        qbgjl__yclrs = eoe__ikml.resolve_function_type(op, args, {}
            ).return_type
        if isinstance(S.data, IntegerArrayType
            ) and qbgjl__yclrs == types.Array(types.bool_, 1, 'C'):
            qbgjl__yclrs = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            rdh__xlbil = bodo.utils.conversion.coerce_to_array(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            pnuib__vcui = bodo.utils.utils.alloc_type(n, qbgjl__yclrs, (-1,))
            for wccx__zmgv in numba.parfors.parfor.internal_prange(n):
                ernu__mpfpq = bodo.libs.array_kernels.isna(arr, wccx__zmgv)
                boqrj__pbk = bodo.libs.array_kernels.isna(rdh__xlbil,
                    wccx__zmgv)
                if ernu__mpfpq and boqrj__pbk:
                    bodo.libs.array_kernels.setna(pnuib__vcui, wccx__zmgv)
                elif ernu__mpfpq:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(pnuib__vcui, wccx__zmgv)
                    else:
                        pnuib__vcui[wccx__zmgv] = op(fill_value, rdh__xlbil
                            [wccx__zmgv])
                elif boqrj__pbk:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(pnuib__vcui, wccx__zmgv)
                    else:
                        pnuib__vcui[wccx__zmgv] = op(arr[wccx__zmgv],
                            fill_value)
                else:
                    pnuib__vcui[wccx__zmgv] = op(arr[wccx__zmgv],
                        rdh__xlbil[wccx__zmgv])
            return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                index, name)
        return impl
    return overload_series_explicit_binary_op


def create_explicit_binary_reverse_op_overload(op):

    def overload_series_explicit_binary_reverse_op(S, other, level=None,
        fill_value=None, axis=0):
        if not is_overload_none(level):
            raise BodoError('level argument not supported')
        if not is_overload_zero(axis):
            raise BodoError('axis argument not supported')
        if not isinstance(S.dtype, types.Number):
            raise BodoError('only numeric values supported')
        eoe__ikml = numba.core.registry.cpu_target.typing_context
        if isinstance(other, types.Number):
            args = other, S.data
            qbgjl__yclrs = eoe__ikml.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and qbgjl__yclrs == types.Array(types.bool_, 1, 'C'):
                qbgjl__yclrs = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                n = len(arr)
                pnuib__vcui = bodo.utils.utils.alloc_type(n, qbgjl__yclrs, None
                    )
                for wccx__zmgv in numba.parfors.parfor.internal_prange(n):
                    ernu__mpfpq = bodo.libs.array_kernels.isna(arr, wccx__zmgv)
                    if ernu__mpfpq:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(pnuib__vcui,
                                wccx__zmgv)
                        else:
                            pnuib__vcui[wccx__zmgv] = op(other, fill_value)
                    else:
                        pnuib__vcui[wccx__zmgv] = op(other, arr[wccx__zmgv])
                return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                    index, name)
            return impl_scalar
        args = types.Array(other.dtype, 1, 'C'), S.data
        qbgjl__yclrs = eoe__ikml.resolve_function_type(op, args, {}
            ).return_type
        if isinstance(S.data, IntegerArrayType
            ) and qbgjl__yclrs == types.Array(types.bool_, 1, 'C'):
            qbgjl__yclrs = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            rdh__xlbil = bodo.hiframes.pd_series_ext.get_series_data(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            pnuib__vcui = bodo.utils.utils.alloc_type(n, qbgjl__yclrs, None)
            for wccx__zmgv in numba.parfors.parfor.internal_prange(n):
                ernu__mpfpq = bodo.libs.array_kernels.isna(arr, wccx__zmgv)
                boqrj__pbk = bodo.libs.array_kernels.isna(rdh__xlbil,
                    wccx__zmgv)
                pnuib__vcui[wccx__zmgv] = op(rdh__xlbil[wccx__zmgv], arr[
                    wccx__zmgv])
                if ernu__mpfpq and boqrj__pbk:
                    bodo.libs.array_kernels.setna(pnuib__vcui, wccx__zmgv)
                elif ernu__mpfpq:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(pnuib__vcui, wccx__zmgv)
                    else:
                        pnuib__vcui[wccx__zmgv] = op(rdh__xlbil[wccx__zmgv],
                            fill_value)
                elif boqrj__pbk:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(pnuib__vcui, wccx__zmgv)
                    else:
                        pnuib__vcui[wccx__zmgv] = op(fill_value, arr[
                            wccx__zmgv])
                else:
                    pnuib__vcui[wccx__zmgv] = op(rdh__xlbil[wccx__zmgv],
                        arr[wccx__zmgv])
            return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                index, name)
        return impl
    return overload_series_explicit_binary_reverse_op


explicit_binop_funcs_two_ways = {operator.add: {'add'}, operator.sub: {
    'sub'}, operator.mul: {'mul'}, operator.truediv: {'div', 'truediv'},
    operator.floordiv: {'floordiv'}, operator.mod: {'mod'}, operator.pow: {
    'pow'}}
explicit_binop_funcs_single = {operator.lt: 'lt', operator.gt: 'gt',
    operator.le: 'le', operator.ge: 'ge', operator.ne: 'ne', operator.eq: 'eq'}
explicit_binop_funcs = set()
split_logical_binops_funcs = [operator.or_, operator.and_]


def _install_explicit_binary_ops():
    for op, love__boh in explicit_binop_funcs_two_ways.items():
        for name in love__boh:
            fnk__oqjmi = create_explicit_binary_op_overload(op)
            putgs__fao = create_explicit_binary_reverse_op_overload(op)
            eidw__owbit = 'r' + name
            overload_method(SeriesType, name, no_unliteral=True)(fnk__oqjmi)
            overload_method(SeriesType, eidw__owbit, no_unliteral=True)(
                putgs__fao)
            explicit_binop_funcs.add(name)
    for op, name in explicit_binop_funcs_single.items():
        fnk__oqjmi = create_explicit_binary_op_overload(op)
        overload_method(SeriesType, name, no_unliteral=True)(fnk__oqjmi)
        explicit_binop_funcs.add(name)


_install_explicit_binary_ops()


def create_binary_op_overload(op):

    def overload_series_binary_op(lhs, rhs):
        if (isinstance(lhs, SeriesType) and isinstance(rhs, SeriesType) and
            lhs.dtype == bodo.datetime64ns and rhs.dtype == bodo.
            datetime64ns and op == operator.sub):

            def impl_dt64(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                rphby__ohy = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                pnuib__vcui = dt64_arr_sub(arr, rphby__ohy)
                return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                    index, name)
            return impl_dt64
        if op in [operator.add, operator.sub] and isinstance(lhs, SeriesType
            ) and lhs.dtype == bodo.datetime64ns and is_offsets_type(rhs):

            def impl_offsets(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                pnuib__vcui = np.empty(n, np.dtype('datetime64[ns]'))
                for wccx__zmgv in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(arr, wccx__zmgv):
                        bodo.libs.array_kernels.setna(pnuib__vcui, wccx__zmgv)
                        continue
                    dej__xeh = (bodo.hiframes.pd_timestamp_ext.
                        convert_datetime64_to_timestamp(arr[wccx__zmgv]))
                    wjbf__kjkz = op(dej__xeh, rhs)
                    pnuib__vcui[wccx__zmgv
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        wjbf__kjkz.value)
                return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                    index, name)
            return impl_offsets
        if op == operator.add and is_offsets_type(lhs) and isinstance(rhs,
            SeriesType) and rhs.dtype == bodo.datetime64ns:

            def impl(lhs, rhs):
                return op(rhs, lhs)
            return impl
        if isinstance(lhs, SeriesType):
            if lhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                    rphby__ohy = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    pnuib__vcui = op(arr, bodo.utils.conversion.
                        unbox_if_timestamp(rphby__ohy))
                    return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                rphby__ohy = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                pnuib__vcui = op(arr, rphby__ohy)
                return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                    index, name)
            return impl
        if isinstance(rhs, SeriesType):
            if rhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                    naz__bbv = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    pnuib__vcui = op(bodo.utils.conversion.
                        unbox_if_timestamp(naz__bbv), arr)
                    return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                naz__bbv = bodo.utils.conversion.get_array_if_series_or_index(
                    lhs)
                pnuib__vcui = op(naz__bbv, arr)
                return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                    index, name)
            return impl
    return overload_series_binary_op


skips = list(explicit_binop_funcs_two_ways.keys()) + list(
    explicit_binop_funcs_single.keys()) + split_logical_binops_funcs


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        fnk__oqjmi = create_binary_op_overload(op)
        overload(op)(fnk__oqjmi)


_install_binary_ops()


def dt64_arr_sub(arg1, arg2):
    return arg1 - arg2


@overload(dt64_arr_sub, no_unliteral=True)
def overload_dt64_arr_sub(arg1, arg2):
    assert arg1 == types.Array(bodo.datetime64ns, 1, 'C'
        ) and arg2 == types.Array(bodo.datetime64ns, 1, 'C')
    sqgy__eoflb = np.dtype('timedelta64[ns]')

    def impl(arg1, arg2):
        numba.parfors.parfor.init_prange()
        n = len(arg1)
        S = np.empty(n, sqgy__eoflb)
        for wccx__zmgv in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg1, wccx__zmgv
                ) or bodo.libs.array_kernels.isna(arg2, wccx__zmgv):
                bodo.libs.array_kernels.setna(S, wccx__zmgv)
                continue
            S[wccx__zmgv
                ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg1[
                wccx__zmgv]) - bodo.hiframes.pd_timestamp_ext.
                dt64_to_integer(arg2[wccx__zmgv]))
        return S
    return impl


def create_inplace_binary_op_overload(op):

    def overload_series_inplace_binary_op(S, other):
        if isinstance(S, SeriesType) or isinstance(other, SeriesType):

            def impl(S, other):
                arr = bodo.utils.conversion.get_array_if_series_or_index(S)
                rdh__xlbil = (bodo.utils.conversion.
                    get_array_if_series_or_index(other))
                op(arr, rdh__xlbil)
                return S
            return impl
    return overload_series_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        fnk__oqjmi = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(fnk__oqjmi)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_series_unary_op(S):
        if isinstance(S, SeriesType):

            def impl(S):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                pnuib__vcui = op(arr)
                return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                    index, name)
            return impl
    return overload_series_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        fnk__oqjmi = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(fnk__oqjmi)


_install_unary_ops()


def create_ufunc_overload(ufunc):
    if ufunc.nin == 1:

        def overload_series_ufunc_nin_1(S):
            if isinstance(S, SeriesType):

                def impl(S):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S)
                    pnuib__vcui = ufunc(arr)
                    return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                        index, name)
                return impl
        return overload_series_ufunc_nin_1
    elif ufunc.nin == 2:

        def overload_series_ufunc_nin_2(S1, S2):
            if isinstance(S1, SeriesType):

                def impl(S1, S2):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S1)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S1)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S1)
                    rdh__xlbil = (bodo.utils.conversion.
                        get_array_if_series_or_index(S2))
                    pnuib__vcui = ufunc(arr, rdh__xlbil)
                    return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                        index, name)
                return impl
            elif isinstance(S2, SeriesType):

                def impl(S1, S2):
                    arr = bodo.utils.conversion.get_array_if_series_or_index(S1
                        )
                    rdh__xlbil = bodo.hiframes.pd_series_ext.get_series_data(S2
                        )
                    index = bodo.hiframes.pd_series_ext.get_series_index(S2)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S2)
                    pnuib__vcui = ufunc(arr, rdh__xlbil)
                    return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                        index, name)
                return impl
        return overload_series_ufunc_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for ufunc in numba.np.ufunc_db.get_ufuncs():
        fnk__oqjmi = create_ufunc_overload(ufunc)
        overload(ufunc, no_unliteral=True)(fnk__oqjmi)


_install_np_ufuncs()


def argsort(A):
    return np.argsort(A)


@overload(argsort, no_unliteral=True)
def overload_argsort(A):

    def impl(A):
        n = len(A)
        yba__hlvna = bodo.libs.str_arr_ext.to_list_if_immutable_arr((A.copy(),)
            )
        lgr__hwz = np.arange(n),
        bodo.libs.timsort.sort(yba__hlvna, 0, n, lgr__hwz)
        return lgr__hwz[0]
    return impl


@overload(pd.to_numeric, inline='always', no_unliteral=True)
def overload_to_numeric(arg_a, errors='raise', downcast=None):
    if not is_overload_none(downcast) and not (is_overload_constant_str(
        downcast) and get_overload_const_str(downcast) in ('integer',
        'signed', 'unsigned', 'float')):
        raise BodoError(
            'pd.to_numeric(): invalid downcasting method provided {}'.
            format(downcast))
    out_dtype = types.float64
    if not is_overload_none(downcast):
        omt__koau = get_overload_const_str(downcast)
        if omt__koau in ('integer', 'signed'):
            out_dtype = types.int64
        elif omt__koau == 'unsigned':
            out_dtype = types.uint64
        else:
            assert omt__koau == 'float'
    if isinstance(arg_a, (types.Array, IntegerArrayType)):
        return lambda arg_a, errors='raise', downcast=None: arg_a.astype(
            out_dtype)
    if isinstance(arg_a, SeriesType):

        def impl_series(arg_a, errors='raise', downcast=None):
            jplow__zfi = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            index = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            name = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            pnuib__vcui = pd.to_numeric(jplow__zfi, errors, downcast)
            return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                index, name)
        return impl_series
    if arg_a != string_array_type:
        raise BodoError('pd.to_numeric(): invalid argument type {}'.format(
            arg_a))
    if out_dtype == types.float64:

        def to_numeric_float_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            qkifd__gfrr = np.empty(n, np.float64)
            for wccx__zmgv in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, wccx__zmgv):
                    bodo.libs.array_kernels.setna(qkifd__gfrr, wccx__zmgv)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(qkifd__gfrr,
                        wccx__zmgv, arg_a, wccx__zmgv)
            return qkifd__gfrr
        return to_numeric_float_impl
    else:

        def to_numeric_int_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            qkifd__gfrr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)
            for wccx__zmgv in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, wccx__zmgv):
                    bodo.libs.array_kernels.setna(qkifd__gfrr, wccx__zmgv)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(qkifd__gfrr,
                        wccx__zmgv, arg_a, wccx__zmgv)
            return qkifd__gfrr
        return to_numeric_int_impl


def series_filter_bool(arr, bool_arr):
    return arr[bool_arr]


@infer_global(series_filter_bool)
class SeriesFilterBoolInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        qdcyt__ohsg = if_series_to_array_type(args[0])
        if isinstance(qdcyt__ohsg, types.Array) and isinstance(qdcyt__ohsg.
            dtype, types.Integer):
            qdcyt__ohsg = types.Array(types.float64, 1, 'C')
        return qdcyt__ohsg(*args)


def where_impl_one_arg(c):
    return np.where(c)


@overload(where_impl_one_arg, no_unliteral=True)
def overload_where_unsupported_one_arg(condition):
    if isinstance(condition, SeriesType) or bodo.utils.utils.is_array_typ(
        condition, False):
        return lambda condition: np.where(condition)


def overload_np_where_one_arg(condition):
    if isinstance(condition, SeriesType):

        def impl_series(condition):
            condition = bodo.hiframes.pd_series_ext.get_series_data(condition)
            return bodo.libs.array_kernels.nonzero(condition)
        return impl_series
    elif bodo.utils.utils.is_array_typ(condition, False):

        def impl(condition):
            return bodo.libs.array_kernels.nonzero(condition)
        return impl


overload(np.where, inline='always', no_unliteral=True)(
    overload_np_where_one_arg)
overload(where_impl_one_arg, inline='always', no_unliteral=True)(
    overload_np_where_one_arg)


def where_impl(c, x, y):
    return np.where(c, x, y)


@overload(where_impl, no_unliteral=True)
def overload_where_unsupported(condition, x, y):
    if not isinstance(condition, (SeriesType, types.Array, BooleanArrayType)
        ) or condition.ndim != 1:
        return lambda condition, x, y: np.where(condition, x, y)


@overload(where_impl, no_unliteral=True)
@overload(np.where, no_unliteral=True)
def overload_np_where(condition, x, y):
    if not isinstance(condition, (SeriesType, types.Array, BooleanArrayType)
        ) or condition.ndim != 1:
        return
    assert condition.dtype == types.bool_, 'invalid condition dtype'
    rpf__zqtr = bodo.utils.utils.is_array_typ(x, True)
    cebmp__brk = bodo.utils.utils.is_array_typ(y, True)
    jfhn__nfueo = 'def _impl(condition, x, y):\n'
    if isinstance(condition, SeriesType):
        jfhn__nfueo += (
            '  condition = bodo.hiframes.pd_series_ext.get_series_data(condition)\n'
            )
    if rpf__zqtr and not bodo.utils.utils.is_array_typ(x, False):
        jfhn__nfueo += '  x = bodo.utils.conversion.coerce_to_array(x)\n'
    if cebmp__brk and not bodo.utils.utils.is_array_typ(y, False):
        jfhn__nfueo += '  y = bodo.utils.conversion.coerce_to_array(y)\n'
    jfhn__nfueo += '  n = len(condition)\n'
    rpnt__wfhov = x.dtype if rpf__zqtr else types.unliteral(x)
    tkda__axbb = y.dtype if cebmp__brk else types.unliteral(y)
    if not isinstance(x, CategoricalArrayType):
        rpnt__wfhov = element_type(x)
    if not isinstance(y, CategoricalArrayType):
        tkda__axbb = element_type(y)

    def get_data(x):
        if isinstance(x, SeriesType):
            return x.data
        elif isinstance(x, types.Array):
            return x
        return types.unliteral(x)
    pezt__byi = get_data(x)
    sbcn__wonat = get_data(y)
    is_nullable = any(bodo.utils.typing.is_nullable(lgr__hwz) for lgr__hwz in
        [pezt__byi, sbcn__wonat])
    if pezt__byi == sbcn__wonat and not is_nullable:
        out_dtype = dtype_to_array_type(rpnt__wfhov)
    elif rpnt__wfhov == string_type or tkda__axbb == string_type:
        out_dtype = bodo.string_array_type
    elif pezt__byi == bytes_type or (rpf__zqtr and rpnt__wfhov == bytes_type
        ) and (sbcn__wonat == bytes_type or cebmp__brk and tkda__axbb ==
        bytes_type):
        out_dtype = binary_array_type
    elif isinstance(rpnt__wfhov, bodo.PDCategoricalDtype):
        out_dtype = None
    elif rpnt__wfhov in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(rpnt__wfhov, 1, 'C')
    elif tkda__axbb in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(tkda__axbb, 1, 'C')
    else:
        out_dtype = numba.from_dtype(np.promote_types(numba.np.
            numpy_support.as_dtype(rpnt__wfhov), numba.np.numpy_support.
            as_dtype(tkda__axbb)))
        out_dtype = types.Array(out_dtype, 1, 'C')
        if is_nullable:
            out_dtype = bodo.utils.typing.to_nullable_type(out_dtype)
    if isinstance(rpnt__wfhov, bodo.PDCategoricalDtype):
        hpfqm__aumod = 'x'
    else:
        hpfqm__aumod = 'out_dtype'
    jfhn__nfueo += (
        f'  out_arr = bodo.utils.utils.alloc_type(n, {hpfqm__aumod}, (-1,))\n')
    if isinstance(rpnt__wfhov, bodo.PDCategoricalDtype):
        jfhn__nfueo += """  out_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(out_arr)
"""
        jfhn__nfueo += """  x_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(x)
"""
    jfhn__nfueo += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    jfhn__nfueo += (
        '    if not bodo.libs.array_kernels.isna(condition, j) and condition[j]:\n'
        )
    if rpf__zqtr:
        jfhn__nfueo += '      if bodo.libs.array_kernels.isna(x, j):\n'
        jfhn__nfueo += '        setna(out_arr, j)\n'
        jfhn__nfueo += '        continue\n'
    if isinstance(rpnt__wfhov, bodo.PDCategoricalDtype):
        jfhn__nfueo += '      out_codes[j] = x_codes[j]\n'
    else:
        jfhn__nfueo += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('x[j]' if rpf__zqtr else 'x'))
    jfhn__nfueo += '    else:\n'
    if cebmp__brk:
        jfhn__nfueo += '      if bodo.libs.array_kernels.isna(y, j):\n'
        jfhn__nfueo += '        setna(out_arr, j)\n'
        jfhn__nfueo += '        continue\n'
    jfhn__nfueo += (
        '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
        .format('y[j]' if cebmp__brk else 'y'))
    jfhn__nfueo += '  return out_arr\n'
    hqlb__oxys = {}
    exec(jfhn__nfueo, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'out_dtype': out_dtype}, hqlb__oxys)
    ypfup__wies = hqlb__oxys['_impl']
    return ypfup__wies


def _verify_np_select_arg_typs(condlist, choicelist, default):
    if isinstance(condlist, (types.List, types.UniTuple)):
        if not (bodo.utils.utils.is_np_array_typ(condlist.dtype) and 
            condlist.dtype.dtype == types.bool_):
            raise BodoError(
                "np.select(): 'condlist' argument must be list or tuple of boolean ndarrays. If passing a Series, please convert with pd.Series.to_numpy()."
                )
    else:
        raise BodoError(
            "np.select(): 'condlist' argument must be list or tuple of boolean ndarrays. If passing a Series, please convert with pd.Series.to_numpy()."
            )
    if not isinstance(choicelist, (types.List, types.UniTuple, types.BaseTuple)
        ):
        raise BodoError(
            "np.select(): 'choicelist' argument must be list or tuple type")
    if isinstance(choicelist, (types.List, types.UniTuple)):
        monk__vbsbd = choicelist.dtype
        if not bodo.utils.utils.is_array_typ(monk__vbsbd, True):
            raise BodoError(
                "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                )
        if is_series_type(monk__vbsbd):
            dgb__nsi = monk__vbsbd.data.dtype
        else:
            dgb__nsi = monk__vbsbd.dtype
        if isinstance(dgb__nsi, bodo.PDCategoricalDtype):
            raise BodoError(
                'np.select(): data with choicelist of type Categorical not yet supported'
                )
        zokwc__eqf = monk__vbsbd
    else:
        lzh__rgm = []
        for monk__vbsbd in choicelist:
            if not bodo.utils.utils.is_array_typ(monk__vbsbd, True):
                raise BodoError(
                    "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                    )
            if is_series_type(monk__vbsbd):
                dgb__nsi = monk__vbsbd.data.dtype
            else:
                dgb__nsi = monk__vbsbd.dtype
            if isinstance(dgb__nsi, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            lzh__rgm.append(dgb__nsi)
        if not is_common_scalar_dtype(lzh__rgm):
            raise BodoError(
                f"np.select(): 'choicelist' items must be arrays with a commmon data type. Found a tuple with the following data types {choicelist}."
                )
        zokwc__eqf = choicelist[0]
    if is_series_type(zokwc__eqf):
        zokwc__eqf = zokwc__eqf.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        pass
    else:
        if not is_scalar_type(default):
            raise BodoError(
                "np.select(): 'default' argument must be scalar type")
        if not (is_common_scalar_dtype([default, zokwc__eqf.dtype]) or 
            default == types.none or is_overload_constant_nan(default)):
            raise BodoError(
                f"np.select(): 'default' is not type compatible with the array types in choicelist. Choicelist type: {choicelist}, Default type: {default}"
                )
    if not (isinstance(zokwc__eqf, types.Array) or isinstance(zokwc__eqf,
        BooleanArrayType) or isinstance(zokwc__eqf, IntegerArrayType) or 
        bodo.utils.utils.is_array_typ(zokwc__eqf, False) and zokwc__eqf.
        dtype in [bodo.string_type, bodo.bytes_type]):
        raise BodoError(
            f'np.select(): data with choicelist of type {zokwc__eqf} not yet supported'
            )


@overload(np.select)
def overload_np_select(condlist, choicelist, default=0):
    _verify_np_select_arg_typs(condlist, choicelist, default)
    bvn__bpq = isinstance(choicelist, (types.List, types.UniTuple)
        ) and isinstance(condlist, (types.List, types.UniTuple))
    if isinstance(choicelist, (types.List, types.UniTuple)):
        euga__hvu = choicelist.dtype
    else:
        icfp__jyoam = False
        lzh__rgm = []
        for monk__vbsbd in choicelist:
            if is_nullable_type(monk__vbsbd):
                icfp__jyoam = True
            if is_series_type(monk__vbsbd):
                dgb__nsi = monk__vbsbd.data.dtype
            else:
                dgb__nsi = monk__vbsbd.dtype
            if isinstance(dgb__nsi, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            lzh__rgm.append(dgb__nsi)
        vtp__bihpn, qht__vxai = get_common_scalar_dtype(lzh__rgm)
        if not qht__vxai:
            raise BodoError('Internal error in overload_np_select')
        ufa__ueuk = dtype_to_array_type(vtp__bihpn)
        if icfp__jyoam:
            ufa__ueuk = to_nullable_type(ufa__ueuk)
        euga__hvu = ufa__ueuk
    if isinstance(euga__hvu, SeriesType):
        euga__hvu = euga__hvu.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        knr__mghv = True
    else:
        knr__mghv = False
    dcux__uyqa = False
    ndue__flryc = False
    if knr__mghv:
        if isinstance(euga__hvu.dtype, types.Number):
            pass
        elif euga__hvu.dtype == types.bool_:
            ndue__flryc = True
        else:
            dcux__uyqa = True
            euga__hvu = to_nullable_type(euga__hvu)
    elif default == types.none or is_overload_constant_nan(default):
        dcux__uyqa = True
        euga__hvu = to_nullable_type(euga__hvu)
    jfhn__nfueo = 'def np_select_impl(condlist, choicelist, default=0):\n'
    jfhn__nfueo += '  if len(condlist) != len(choicelist):\n'
    jfhn__nfueo += """    raise ValueError('list of cases must be same length as list of conditions')
"""
    jfhn__nfueo += '  output_len = len(choicelist[0])\n'
    jfhn__nfueo += (
        '  out = bodo.utils.utils.alloc_type(output_len, alloc_typ, (-1,))\n')
    jfhn__nfueo += '  for i in range(output_len):\n'
    if dcux__uyqa:
        jfhn__nfueo += '    bodo.libs.array_kernels.setna(out, i)\n'
    elif ndue__flryc:
        jfhn__nfueo += '    out[i] = False\n'
    else:
        jfhn__nfueo += '    out[i] = default\n'
    if bvn__bpq:
        jfhn__nfueo += '  for i in range(len(condlist) - 1, -1, -1):\n'
        jfhn__nfueo += '    cond = condlist[i]\n'
        jfhn__nfueo += '    choice = choicelist[i]\n'
        jfhn__nfueo += '    out = np.where(cond, choice, out)\n'
    else:
        for wccx__zmgv in range(len(choicelist) - 1, -1, -1):
            jfhn__nfueo += f'  cond = condlist[{wccx__zmgv}]\n'
            jfhn__nfueo += f'  choice = choicelist[{wccx__zmgv}]\n'
            jfhn__nfueo += f'  out = np.where(cond, choice, out)\n'
    jfhn__nfueo += '  return out'
    hqlb__oxys = dict()
    exec(jfhn__nfueo, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'alloc_typ': euga__hvu}, hqlb__oxys)
    impl = hqlb__oxys['np_select_impl']
    return impl


@overload_method(SeriesType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_series_drop_duplicates(S, subset=None, keep='first', inplace=False
    ):
    zrc__izp = dict(subset=subset, keep=keep, inplace=inplace)
    mio__xes = dict(subset=None, keep='first', inplace=False)
    check_unsupported_args('Series.drop_duplicates', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')

    def impl(S, subset=None, keep='first', inplace=False):
        vvwrt__ckr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        (vvwrt__ckr,), rfkp__tlsav = bodo.libs.array_kernels.drop_duplicates((
            vvwrt__ckr,), index, 1)
        index = bodo.utils.conversion.index_from_array(rfkp__tlsav)
        return bodo.hiframes.pd_series_ext.init_series(vvwrt__ckr, index, name)
    return impl


@overload_method(SeriesType, 'between', inline='always', no_unliteral=True)
def overload_series_between(S, left, right, inclusive='both'):
    cbmlk__fmarw = element_type(S.data)
    if not is_common_scalar_dtype([cbmlk__fmarw, left]):
        raise_bodo_error(
            "Series.between(): 'left' must be compariable with the Series data"
            )
    if not is_common_scalar_dtype([cbmlk__fmarw, right]):
        raise_bodo_error(
            "Series.between(): 'right' must be compariable with the Series data"
            )
    if not is_overload_constant_str(inclusive) or get_overload_const_str(
        inclusive) not in ('both', 'neither'):
        raise_bodo_error(
            "Series.between(): 'inclusive' must be a constant string and one of ('both', 'neither')"
            )

    def impl(S, left, right, inclusive='both'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(arr)
        pnuib__vcui = np.empty(n, np.bool_)
        for wccx__zmgv in numba.parfors.parfor.internal_prange(n):
            dvauy__gss = bodo.utils.conversion.box_if_dt64(arr[wccx__zmgv])
            if inclusive == 'both':
                pnuib__vcui[wccx__zmgv
                    ] = dvauy__gss <= right and dvauy__gss >= left
            else:
                pnuib__vcui[wccx__zmgv
                    ] = dvauy__gss < right and dvauy__gss > left
        return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui, index, name
            )
    return impl


@overload_method(SeriesType, 'repeat', inline='always', no_unliteral=True)
def overload_series_repeat(S, repeats, axis=None):
    zrc__izp = dict(axis=axis)
    mio__xes = dict(axis=None)
    check_unsupported_args('Series.repeat', zrc__izp, mio__xes,
        package_name='pandas', module_name='Series')
    if not (isinstance(repeats, types.Integer) or is_iterable_type(repeats) and
        isinstance(repeats.dtype, types.Integer)):
        raise BodoError(
            "Series.repeat(): 'repeats' should be an integer or array of integers"
            )
    if isinstance(repeats, types.Integer):

        def impl_int(S, repeats, axis=None):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            rfkp__tlsav = bodo.utils.conversion.index_to_array(index)
            pnuib__vcui = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
            hexe__dor = bodo.libs.array_kernels.repeat_kernel(rfkp__tlsav,
                repeats)
            sbyn__ejk = bodo.utils.conversion.index_from_array(hexe__dor)
            return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
                sbyn__ejk, name)
        return impl_int

    def impl_arr(S, repeats, axis=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        rfkp__tlsav = bodo.utils.conversion.index_to_array(index)
        repeats = bodo.utils.conversion.coerce_to_array(repeats)
        pnuib__vcui = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
        hexe__dor = bodo.libs.array_kernels.repeat_kernel(rfkp__tlsav, repeats)
        sbyn__ejk = bodo.utils.conversion.index_from_array(hexe__dor)
        return bodo.hiframes.pd_series_ext.init_series(pnuib__vcui,
            sbyn__ejk, name)
    return impl_arr


@overload_method(SeriesType, 'to_dict', no_unliteral=True)
def overload_to_dict(S, into=None):

    def impl(S, into=None):
        lgr__hwz = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        n = len(lgr__hwz)
        mldp__jhrn = {}
        for wccx__zmgv in range(n):
            dvauy__gss = bodo.utils.conversion.box_if_dt64(lgr__hwz[wccx__zmgv]
                )
            mldp__jhrn[index[wccx__zmgv]] = dvauy__gss
        return mldp__jhrn
    return impl


@overload_method(SeriesType, 'to_frame', inline='always', no_unliteral=True)
def overload_series_to_frame(S, name=None):
    dwu__jsj = (
        "Series.to_frame(): output column name should be known at compile time. Set 'name' to a constant value."
        )
    if is_overload_none(name):
        if is_literal_type(S.name_typ):
            nsg__uln = get_literal_value(S.name_typ)
        else:
            raise_bodo_error(dwu__jsj)
    elif is_literal_type(name):
        nsg__uln = get_literal_value(name)
    else:
        raise_bodo_error(dwu__jsj)
    nsg__uln = 0 if nsg__uln is None else nsg__uln

    def impl(S, name=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,), index,
            (nsg__uln,))
    return impl


@overload_method(SeriesType, 'keys', inline='always', no_unliteral=True)
def overload_series_keys(S):

    def impl(S):
        return bodo.hiframes.pd_series_ext.get_series_index(S)
    return impl
