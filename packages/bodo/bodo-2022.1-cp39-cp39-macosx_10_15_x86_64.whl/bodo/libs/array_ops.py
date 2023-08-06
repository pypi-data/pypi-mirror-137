"""
Implements array operations for usage by DataFrames and Series
such as count and max.
"""
import numba
import numpy as np
import pandas as pd
from numba import generated_jit
from numba.core import types
from numba.extending import overload
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.utils.typing import element_type, is_hashable_type, is_iterable_type, is_overload_true, is_overload_zero


@numba.njit
def array_op_median(arr, skipna=True, parallel=False):
    nfgtq__yoxqn = np.empty(1, types.float64)
    bodo.libs.array_kernels.median_series_computation(nfgtq__yoxqn.ctypes,
        arr, parallel, skipna)
    return nfgtq__yoxqn[0]


def array_op_isna(arr):
    pass


@overload(array_op_isna)
def overload_array_op_isna(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        qqq__zts = len(arr)
        moamz__gegzr = np.empty(qqq__zts, np.bool_)
        for wcxa__vwm in numba.parfors.parfor.internal_prange(qqq__zts):
            moamz__gegzr[wcxa__vwm] = bodo.libs.array_kernels.isna(arr,
                wcxa__vwm)
        return moamz__gegzr
    return impl


def array_op_count(arr):
    pass


@overload(array_op_count)
def overload_array_op_count(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        vylu__suf = 0
        for wcxa__vwm in numba.parfors.parfor.internal_prange(len(arr)):
            kdor__uysr = 0
            if not bodo.libs.array_kernels.isna(arr, wcxa__vwm):
                kdor__uysr = 1
            vylu__suf += kdor__uysr
        nfgtq__yoxqn = vylu__suf
        return nfgtq__yoxqn
    return impl


def array_op_describe(arr):
    pass


def array_op_describe_impl(arr):
    itkv__pys = array_op_count(arr)
    aiap__tkkqd = array_op_min(arr)
    qbfsj__secny = array_op_max(arr)
    xow__bvno = array_op_mean(arr)
    ajpis__vtqej = array_op_std(arr)
    dfq__drxv = array_op_quantile(arr, 0.25)
    czfpk__yzrdl = array_op_quantile(arr, 0.5)
    teeh__ttht = array_op_quantile(arr, 0.75)
    return (itkv__pys, xow__bvno, ajpis__vtqej, aiap__tkkqd, dfq__drxv,
        czfpk__yzrdl, teeh__ttht, qbfsj__secny)


def array_op_describe_dt_impl(arr):
    itkv__pys = array_op_count(arr)
    aiap__tkkqd = array_op_min(arr)
    qbfsj__secny = array_op_max(arr)
    xow__bvno = array_op_mean(arr)
    dfq__drxv = array_op_quantile(arr, 0.25)
    czfpk__yzrdl = array_op_quantile(arr, 0.5)
    teeh__ttht = array_op_quantile(arr, 0.75)
    return (itkv__pys, xow__bvno, aiap__tkkqd, dfq__drxv, czfpk__yzrdl,
        teeh__ttht, qbfsj__secny)


@overload(array_op_describe)
def overload_array_op_describe(arr):
    if arr.dtype == bodo.datetime64ns:
        return array_op_describe_dt_impl
    return array_op_describe_impl


def array_op_min(arr):
    pass


@overload(array_op_min)
def overload_array_op_min(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            lxpm__wxmbv = numba.cpython.builtins.get_type_max_value(np.int64)
            vylu__suf = 0
            for wcxa__vwm in numba.parfors.parfor.internal_prange(len(arr)):
                ako__txoy = lxpm__wxmbv
                kdor__uysr = 0
                if not bodo.libs.array_kernels.isna(arr, wcxa__vwm):
                    ako__txoy = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[wcxa__vwm]))
                    kdor__uysr = 1
                lxpm__wxmbv = min(lxpm__wxmbv, ako__txoy)
                vylu__suf += kdor__uysr
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(lxpm__wxmbv,
                vylu__suf)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            lxpm__wxmbv = numba.cpython.builtins.get_type_max_value(np.int64)
            vylu__suf = 0
            for wcxa__vwm in numba.parfors.parfor.internal_prange(len(arr)):
                ako__txoy = lxpm__wxmbv
                kdor__uysr = 0
                if not bodo.libs.array_kernels.isna(arr, wcxa__vwm):
                    ako__txoy = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        arr[wcxa__vwm])
                    kdor__uysr = 1
                lxpm__wxmbv = min(lxpm__wxmbv, ako__txoy)
                vylu__suf += kdor__uysr
            return bodo.hiframes.pd_index_ext._dti_val_finalize(lxpm__wxmbv,
                vylu__suf)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            pvzg__see = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            lxpm__wxmbv = numba.cpython.builtins.get_type_max_value(np.int64)
            vylu__suf = 0
            for wcxa__vwm in numba.parfors.parfor.internal_prange(len(
                pvzg__see)):
                sgv__ifyt = pvzg__see[wcxa__vwm]
                if sgv__ifyt == -1:
                    continue
                lxpm__wxmbv = min(lxpm__wxmbv, sgv__ifyt)
                vylu__suf += 1
            nfgtq__yoxqn = bodo.hiframes.series_kernels._box_cat_val(
                lxpm__wxmbv, arr.dtype, vylu__suf)
            return nfgtq__yoxqn
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            lxpm__wxmbv = bodo.hiframes.series_kernels._get_date_max_value()
            vylu__suf = 0
            for wcxa__vwm in numba.parfors.parfor.internal_prange(len(arr)):
                ako__txoy = lxpm__wxmbv
                kdor__uysr = 0
                if not bodo.libs.array_kernels.isna(arr, wcxa__vwm):
                    ako__txoy = arr[wcxa__vwm]
                    kdor__uysr = 1
                lxpm__wxmbv = min(lxpm__wxmbv, ako__txoy)
                vylu__suf += kdor__uysr
            nfgtq__yoxqn = bodo.hiframes.series_kernels._sum_handle_nan(
                lxpm__wxmbv, vylu__suf)
            return nfgtq__yoxqn
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        lxpm__wxmbv = bodo.hiframes.series_kernels._get_type_max_value(arr.
            dtype)
        vylu__suf = 0
        for wcxa__vwm in numba.parfors.parfor.internal_prange(len(arr)):
            ako__txoy = lxpm__wxmbv
            kdor__uysr = 0
            if not bodo.libs.array_kernels.isna(arr, wcxa__vwm):
                ako__txoy = arr[wcxa__vwm]
                kdor__uysr = 1
            lxpm__wxmbv = min(lxpm__wxmbv, ako__txoy)
            vylu__suf += kdor__uysr
        nfgtq__yoxqn = bodo.hiframes.series_kernels._sum_handle_nan(lxpm__wxmbv
            , vylu__suf)
        return nfgtq__yoxqn
    return impl


def array_op_max(arr):
    pass


@overload(array_op_max)
def overload_array_op_max(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            lxpm__wxmbv = numba.cpython.builtins.get_type_min_value(np.int64)
            vylu__suf = 0
            for wcxa__vwm in numba.parfors.parfor.internal_prange(len(arr)):
                ako__txoy = lxpm__wxmbv
                kdor__uysr = 0
                if not bodo.libs.array_kernels.isna(arr, wcxa__vwm):
                    ako__txoy = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[wcxa__vwm]))
                    kdor__uysr = 1
                lxpm__wxmbv = max(lxpm__wxmbv, ako__txoy)
                vylu__suf += kdor__uysr
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(lxpm__wxmbv,
                vylu__suf)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            lxpm__wxmbv = numba.cpython.builtins.get_type_min_value(np.int64)
            vylu__suf = 0
            for wcxa__vwm in numba.parfors.parfor.internal_prange(len(arr)):
                ako__txoy = lxpm__wxmbv
                kdor__uysr = 0
                if not bodo.libs.array_kernels.isna(arr, wcxa__vwm):
                    ako__txoy = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        arr[wcxa__vwm])
                    kdor__uysr = 1
                lxpm__wxmbv = max(lxpm__wxmbv, ako__txoy)
                vylu__suf += kdor__uysr
            return bodo.hiframes.pd_index_ext._dti_val_finalize(lxpm__wxmbv,
                vylu__suf)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            pvzg__see = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            lxpm__wxmbv = -1
            for wcxa__vwm in numba.parfors.parfor.internal_prange(len(
                pvzg__see)):
                lxpm__wxmbv = max(lxpm__wxmbv, pvzg__see[wcxa__vwm])
            nfgtq__yoxqn = bodo.hiframes.series_kernels._box_cat_val(
                lxpm__wxmbv, arr.dtype, 1)
            return nfgtq__yoxqn
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            lxpm__wxmbv = bodo.hiframes.series_kernels._get_date_min_value()
            vylu__suf = 0
            for wcxa__vwm in numba.parfors.parfor.internal_prange(len(arr)):
                ako__txoy = lxpm__wxmbv
                kdor__uysr = 0
                if not bodo.libs.array_kernels.isna(arr, wcxa__vwm):
                    ako__txoy = arr[wcxa__vwm]
                    kdor__uysr = 1
                lxpm__wxmbv = max(lxpm__wxmbv, ako__txoy)
                vylu__suf += kdor__uysr
            nfgtq__yoxqn = bodo.hiframes.series_kernels._sum_handle_nan(
                lxpm__wxmbv, vylu__suf)
            return nfgtq__yoxqn
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        lxpm__wxmbv = bodo.hiframes.series_kernels._get_type_min_value(arr.
            dtype)
        vylu__suf = 0
        for wcxa__vwm in numba.parfors.parfor.internal_prange(len(arr)):
            ako__txoy = lxpm__wxmbv
            kdor__uysr = 0
            if not bodo.libs.array_kernels.isna(arr, wcxa__vwm):
                ako__txoy = arr[wcxa__vwm]
                kdor__uysr = 1
            lxpm__wxmbv = max(lxpm__wxmbv, ako__txoy)
            vylu__suf += kdor__uysr
        nfgtq__yoxqn = bodo.hiframes.series_kernels._sum_handle_nan(lxpm__wxmbv
            , vylu__suf)
        return nfgtq__yoxqn
    return impl


def array_op_mean(arr):
    pass


@overload(array_op_mean)
def overload_array_op_mean(arr):
    if arr.dtype == bodo.datetime64ns:

        def impl(arr):
            return pd.Timestamp(types.int64(bodo.libs.array_ops.
                array_op_mean(arr.view(np.int64))))
        return impl
    ros__pzy = types.float64
    nqb__mhclc = types.float64
    if isinstance(arr, types.Array) and arr.dtype == types.float32:
        ros__pzy = types.float32
        nqb__mhclc = types.float32
    nop__ezms = ros__pzy(0)
    kkz__bcmsc = nqb__mhclc(0)
    ejy__ufwup = nqb__mhclc(1)

    def impl(arr):
        numba.parfors.parfor.init_prange()
        lxpm__wxmbv = nop__ezms
        vylu__suf = kkz__bcmsc
        for wcxa__vwm in numba.parfors.parfor.internal_prange(len(arr)):
            ako__txoy = nop__ezms
            kdor__uysr = kkz__bcmsc
            if not bodo.libs.array_kernels.isna(arr, wcxa__vwm):
                ako__txoy = arr[wcxa__vwm]
                kdor__uysr = ejy__ufwup
            lxpm__wxmbv += ako__txoy
            vylu__suf += kdor__uysr
        nfgtq__yoxqn = bodo.hiframes.series_kernels._mean_handle_nan(
            lxpm__wxmbv, vylu__suf)
        return nfgtq__yoxqn
    return impl


def array_op_var(arr, skipna, ddof):
    pass


@overload(array_op_var)
def overload_array_op_var(arr, skipna, ddof):

    def impl(arr, skipna, ddof):
        numba.parfors.parfor.init_prange()
        ttvng__hfsj = 0.0
        mfc__lfjmy = 0.0
        vylu__suf = 0
        for wcxa__vwm in numba.parfors.parfor.internal_prange(len(arr)):
            ako__txoy = 0.0
            kdor__uysr = 0
            if not bodo.libs.array_kernels.isna(arr, wcxa__vwm) or not skipna:
                ako__txoy = arr[wcxa__vwm]
                kdor__uysr = 1
            ttvng__hfsj += ako__txoy
            mfc__lfjmy += ako__txoy * ako__txoy
            vylu__suf += kdor__uysr
        lxpm__wxmbv = mfc__lfjmy - ttvng__hfsj * ttvng__hfsj / vylu__suf
        nfgtq__yoxqn = bodo.hiframes.series_kernels._handle_nan_count_ddof(
            lxpm__wxmbv, vylu__suf, ddof)
        return nfgtq__yoxqn
    return impl


def array_op_std(arr, skipna=True, ddof=1):
    pass


@overload(array_op_std)
def overload_array_op_std(arr, skipna=True, ddof=1):
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr, skipna=True, ddof=1):
            return pd.Timedelta(types.int64(array_op_var(arr.view(np.int64),
                skipna, ddof) ** 0.5))
        return impl_dt64
    return lambda arr, skipna=True, ddof=1: array_op_var(arr, skipna, ddof
        ) ** 0.5


def array_op_quantile(arr, q):
    pass


@overload(array_op_quantile)
def overload_array_op_quantile(arr, q):
    if is_iterable_type(q):
        if arr.dtype == bodo.datetime64ns:

            def _impl_list_dt(arr, q):
                moamz__gegzr = np.empty(len(q), np.int64)
                for wcxa__vwm in range(len(q)):
                    uypkc__qgrf = np.float64(q[wcxa__vwm])
                    moamz__gegzr[wcxa__vwm] = bodo.libs.array_kernels.quantile(
                        arr.view(np.int64), uypkc__qgrf)
                return moamz__gegzr.view(np.dtype('datetime64[ns]'))
            return _impl_list_dt

        def impl_list(arr, q):
            moamz__gegzr = np.empty(len(q), np.float64)
            for wcxa__vwm in range(len(q)):
                uypkc__qgrf = np.float64(q[wcxa__vwm])
                moamz__gegzr[wcxa__vwm] = bodo.libs.array_kernels.quantile(arr,
                    uypkc__qgrf)
            return moamz__gegzr
        return impl_list
    if arr.dtype == bodo.datetime64ns:

        def _impl_dt(arr, q):
            return pd.Timestamp(bodo.libs.array_kernels.quantile(arr.view(
                np.int64), np.float64(q)))
        return _impl_dt

    def impl(arr, q):
        return bodo.libs.array_kernels.quantile(arr, np.float64(q))
    return impl


def array_op_sum(arr, skipna, min_count):
    pass


@overload(array_op_sum, no_unliteral=True)
def overload_array_op_sum(arr, skipna, min_count):
    if isinstance(arr.dtype, types.Integer):
        rgl__itx = types.intp
    elif arr.dtype == types.bool_:
        rgl__itx = np.int64
    else:
        rgl__itx = arr.dtype
    qtnzp__pxa = rgl__itx(0)
    if isinstance(arr.dtype, types.Float) and (not is_overload_true(skipna) or
        not is_overload_zero(min_count)):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            lxpm__wxmbv = qtnzp__pxa
            qqq__zts = len(arr)
            vylu__suf = 0
            for wcxa__vwm in numba.parfors.parfor.internal_prange(qqq__zts):
                ako__txoy = qtnzp__pxa
                kdor__uysr = 0
                if not bodo.libs.array_kernels.isna(arr, wcxa__vwm
                    ) or not skipna:
                    ako__txoy = arr[wcxa__vwm]
                    kdor__uysr = 1
                lxpm__wxmbv += ako__txoy
                vylu__suf += kdor__uysr
            nfgtq__yoxqn = bodo.hiframes.series_kernels._var_handle_mincount(
                lxpm__wxmbv, vylu__suf, min_count)
            return nfgtq__yoxqn
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            lxpm__wxmbv = qtnzp__pxa
            qqq__zts = len(arr)
            for wcxa__vwm in numba.parfors.parfor.internal_prange(qqq__zts):
                ako__txoy = qtnzp__pxa
                if not bodo.libs.array_kernels.isna(arr, wcxa__vwm):
                    ako__txoy = arr[wcxa__vwm]
                lxpm__wxmbv += ako__txoy
            return lxpm__wxmbv
    return impl


def array_op_prod(arr, skipna, min_count):
    pass


@overload(array_op_prod)
def overload_array_op_prod(arr, skipna, min_count):
    uhr__pvyp = arr.dtype(1)
    if arr.dtype == types.bool_:
        uhr__pvyp = 1
    if isinstance(arr.dtype, types.Float):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            lxpm__wxmbv = uhr__pvyp
            vylu__suf = 0
            for wcxa__vwm in numba.parfors.parfor.internal_prange(len(arr)):
                ako__txoy = uhr__pvyp
                kdor__uysr = 0
                if not bodo.libs.array_kernels.isna(arr, wcxa__vwm
                    ) or not skipna:
                    ako__txoy = arr[wcxa__vwm]
                    kdor__uysr = 1
                vylu__suf += kdor__uysr
                lxpm__wxmbv *= ako__txoy
            nfgtq__yoxqn = bodo.hiframes.series_kernels._var_handle_mincount(
                lxpm__wxmbv, vylu__suf, min_count)
            return nfgtq__yoxqn
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            lxpm__wxmbv = uhr__pvyp
            for wcxa__vwm in numba.parfors.parfor.internal_prange(len(arr)):
                ako__txoy = uhr__pvyp
                if not bodo.libs.array_kernels.isna(arr, wcxa__vwm):
                    ako__txoy = arr[wcxa__vwm]
                lxpm__wxmbv *= ako__txoy
            return lxpm__wxmbv
    return impl


def array_op_idxmax(arr, index):
    pass


@overload(array_op_idxmax, inline='always')
def overload_array_op_idxmax(arr, index):

    def impl(arr, index):
        wcxa__vwm = bodo.libs.array_kernels._nan_argmax(arr)
        return index[wcxa__vwm]
    return impl


def array_op_idxmin(arr, index):
    pass


@overload(array_op_idxmin, inline='always')
def overload_array_op_idxmin(arr, index):

    def impl(arr, index):
        wcxa__vwm = bodo.libs.array_kernels._nan_argmin(arr)
        return index[wcxa__vwm]
    return impl


def _convert_isin_values(values, use_hash_impl):
    pass


@overload(_convert_isin_values, no_unliteral=True)
def overload_convert_isin_values(values, use_hash_impl):
    if is_overload_true(use_hash_impl):

        def impl(values, use_hash_impl):
            tiv__rorxl = {}
            for hbd__yqi in values:
                tiv__rorxl[bodo.utils.conversion.box_if_dt64(hbd__yqi)] = 0
            return tiv__rorxl
        return impl
    else:

        def impl(values, use_hash_impl):
            return values
        return impl


def array_op_isin(arr, values):
    pass


@overload(array_op_isin, inline='always')
def overload_array_op_isin(arr, values):
    use_hash_impl = element_type(values) == element_type(arr
        ) and is_hashable_type(element_type(values))

    def impl(arr, values):
        values = bodo.libs.array_ops._convert_isin_values(values, use_hash_impl
            )
        numba.parfors.parfor.init_prange()
        qqq__zts = len(arr)
        moamz__gegzr = np.empty(qqq__zts, np.bool_)
        for wcxa__vwm in numba.parfors.parfor.internal_prange(qqq__zts):
            moamz__gegzr[wcxa__vwm] = bodo.utils.conversion.box_if_dt64(arr
                [wcxa__vwm]) in values
        return moamz__gegzr
    return impl


@generated_jit(nopython=True)
def array_unique_vector_map(in_arr):
    ryl__dlc = 'def impl(in_arr):\n'
    ryl__dlc += '  n = len(in_arr)\n'
    ryl__dlc += '  arr_map = {in_arr[0]: 0 for _ in range(0)}\n'
    ryl__dlc += '  in_lst = []\n'
    ryl__dlc += '  map_vector = np.empty(n, np.int64)\n'
    ryl__dlc += '  is_na = 0\n'
    if in_arr == bodo.string_array_type:
        ryl__dlc += '  total_len = 0\n'
    ryl__dlc += '  for i in range(n):\n'
    ryl__dlc += '    if bodo.libs.array_kernels.isna(in_arr, i):\n'
    ryl__dlc += '      is_na = 1\n'
    ryl__dlc += (
        '      # Always put NA in the last location. We can safely use\n')
    ryl__dlc += '      # -1 because in_arr[-1] == in_arr[len(in_arr) - 1]\n'
    ryl__dlc += '      set_val = -1\n'
    ryl__dlc += '    else:\n'
    ryl__dlc += '      data_val = in_arr[i]\n'
    ryl__dlc += '      if data_val not in arr_map:\n'
    ryl__dlc += '        set_val = len(arr_map)\n'
    ryl__dlc += '        # Add the data to index info\n'
    ryl__dlc += '        in_lst.append(data_val)\n'
    ryl__dlc += '        arr_map[data_val] = len(arr_map)\n'
    if in_arr == bodo.string_array_type:
        ryl__dlc += '        total_len += len(data_val)\n'
    ryl__dlc += '      else:\n'
    ryl__dlc += '        set_val = arr_map[data_val]\n'
    ryl__dlc += '    map_vector[i] = set_val\n'
    ryl__dlc += '  n_rows = len(arr_map) + is_na\n'
    if in_arr == bodo.string_array_type:
        ryl__dlc += (
            '  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len)\n'
            )
    else:
        ryl__dlc += (
            '  out_arr = bodo.utils.utils.alloc_type(n_rows, in_arr, (-1,))\n')
    ryl__dlc += '  for j in range(len(arr_map)):\n'
    ryl__dlc += '    out_arr[j] = in_lst[j]\n'
    ryl__dlc += '  if is_na:\n'
    ryl__dlc += '    bodo.libs.array_kernels.setna(out_arr, n_rows - 1)\n'
    ryl__dlc += '  return out_arr, map_vector\n'
    vzz__xqa = {}
    exec(ryl__dlc, {'bodo': bodo, 'np': np}, vzz__xqa)
    impl = vzz__xqa['impl']
    return impl
