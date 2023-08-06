"""
Implements array kernels such as median and quantile.
"""
import hashlib
import inspect
import math
import operator
import re
import warnings
from math import sqrt
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types, typing
from numba.core.imputils import lower_builtin
from numba.core.ir_utils import find_const, guard
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import overload, overload_attribute, register_jitable
from numba.np.arrayobj import make_array
from numba.np.numpy_support import as_dtype
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, init_categorical_array
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.libs import quantile_alg
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_info_decref_array, delete_table, delete_table_decref_arrays, drop_duplicates_table, info_from_table, info_to_array, sample_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, offset_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.distributed_api import Reduce_Type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import str_arr_set_na, string_array_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.shuffle import getitem_arr_tup_single
from bodo.utils.typing import BodoError, check_unsupported_args, element_type, find_common_np_dtype, get_overload_const_bool, get_overload_const_list, get_overload_const_str, is_overload_none, raise_bodo_error
from bodo.utils.utils import build_set_seen_na, check_and_propagate_cpp_exception, numba_to_c_type, unliteral_all
ll.add_symbol('quantile_sequential', quantile_alg.quantile_sequential)
ll.add_symbol('quantile_parallel', quantile_alg.quantile_parallel)
MPI_ROOT = 0
sum_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value)


def isna(arr, i):
    return False


@overload(isna)
def overload_isna(arr, i):
    i = types.unliteral(i)
    if arr == string_array_type:
        return lambda arr, i: bodo.libs.str_arr_ext.str_arr_is_na(arr, i)
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type,
        datetime_timedelta_array_type, string_array_split_view_type):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr
            ._null_bitmap, i)
    if isinstance(arr, ArrayItemArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.array_item_arr_ext.get_null_bitmap(arr), i)
    if isinstance(arr, StructArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.struct_arr_ext.get_null_bitmap(arr), i)
    if isinstance(arr, TupleArrayType):
        return lambda arr, i: bodo.libs.array_kernels.isna(arr._data, i)
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        return lambda arr, i: arr.codes[i] == -1
    if arr == bodo.binary_array_type:
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.array_item_arr_ext.get_null_bitmap(arr._data), i)
    if isinstance(arr, types.List):
        if arr.dtype == types.none:
            return lambda arr, i: True
        elif isinstance(arr.dtype, types.optional):
            return lambda arr, i: arr[i] is None
        else:
            return lambda arr, i: False
    if isinstance(arr, bodo.NullableTupleType):
        return lambda arr, i: arr._null_values[i]
    assert isinstance(arr, types.Array)
    dtype = arr.dtype
    if isinstance(dtype, types.Float):
        return lambda arr, i: np.isnan(arr[i])
    if isinstance(dtype, (types.NPDatetime, types.NPTimedelta)):
        return lambda arr, i: np.isnat(arr[i])
    return lambda arr, i: False


def setna(arr, ind, int_nan_const=0):
    arr[ind] = np.nan


@overload(setna, no_unliteral=True)
def setna_overload(arr, ind, int_nan_const=0):
    if isinstance(arr.dtype, types.Float):
        return setna
    if isinstance(arr.dtype, (types.NPDatetime, types.NPTimedelta)):
        nbym__nls = arr.dtype('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr[ind] = nbym__nls
        return _setnan_impl
    if arr == string_array_type:

        def impl(arr, ind, int_nan_const=0):
            arr[ind] = ''
            str_arr_set_na(arr, ind)
        return impl
    if arr == boolean_array:

        def impl(arr, ind, int_nan_const=0):
            arr[ind] = False
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)):
        return (lambda arr, ind, int_nan_const=0: bodo.libs.int_arr_ext.
            set_bit_to_arr(arr._null_bitmap, ind, 0))
    if arr == bodo.binary_array_type:

        def impl_binary_arr(arr, ind, int_nan_const=0):
            giw__vvldy = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            giw__vvldy[ind + 1] = giw__vvldy[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_binary_arr
    if isinstance(arr, bodo.libs.array_item_arr_ext.ArrayItemArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            giw__vvldy = bodo.libs.array_item_arr_ext.get_offsets(arr)
            giw__vvldy[ind + 1] = giw__vvldy[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr), ind, 0)
        return impl_arr_item
    if isinstance(arr, bodo.libs.struct_arr_ext.StructArrayType):

        def impl(arr, ind, int_nan_const=0):
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.struct_arr_ext.
                get_null_bitmap(arr), ind, 0)
            data = bodo.libs.struct_arr_ext.get_data(arr)
            setna_tup(data, ind)
        return impl
    if isinstance(arr, TupleArrayType):

        def impl(arr, ind, int_nan_const=0):
            bodo.libs.array_kernels.setna(arr._data, ind)
        return impl
    if arr.dtype == types.bool_:

        def b_set(arr, ind, int_nan_const=0):
            arr[ind] = False
        return b_set
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):

        def setna_cat(arr, ind, int_nan_const=0):
            arr.codes[ind] = -1
        return setna_cat
    if isinstance(arr.dtype, types.Integer):

        def setna_int(arr, ind, int_nan_const=0):
            arr[ind] = int_nan_const
        return setna_int
    if arr == datetime_date_array_type:

        def setna_datetime_date(arr, ind, int_nan_const=0):
            arr._data[ind] = (1970 << 32) + (1 << 16) + 1
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return setna_datetime_date
    if arr == datetime_timedelta_array_type:

        def setna_datetime_timedelta(arr, ind, int_nan_const=0):
            bodo.libs.array_kernels.setna(arr._days_data, ind)
            bodo.libs.array_kernels.setna(arr._seconds_data, ind)
            bodo.libs.array_kernels.setna(arr._microseconds_data, ind)
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return setna_datetime_timedelta
    return lambda arr, ind, int_nan_const=0: None


def setna_tup(arr_tup, ind, int_nan_const=0):
    for arr in arr_tup:
        arr[ind] = np.nan


@overload(setna_tup, no_unliteral=True)
def overload_setna_tup(arr_tup, ind, int_nan_const=0):
    kuma__wncl = arr_tup.count
    jka__ihr = 'def f(arr_tup, ind, int_nan_const=0):\n'
    for i in range(kuma__wncl):
        jka__ihr += '  setna(arr_tup[{}], ind, int_nan_const)\n'.format(i)
    jka__ihr += '  return\n'
    ohgz__dmpvb = {}
    exec(jka__ihr, {'setna': setna}, ohgz__dmpvb)
    impl = ohgz__dmpvb['f']
    return impl


def setna_slice(arr, s):
    arr[s] = np.nan


@overload(setna_slice, no_unliteral=True)
def overload_setna_slice(arr, s):

    def impl(arr, s):
        hitw__pnr = numba.cpython.unicode._normalize_slice(s, len(arr))
        for i in range(hitw__pnr.start, hitw__pnr.stop, hitw__pnr.step):
            setna(arr, i)
    return impl


ll.add_symbol('median_series_computation', quantile_alg.
    median_series_computation)
_median_series_computation = types.ExternalFunction('median_series_computation'
    , types.void(types.voidptr, bodo.libs.array.array_info_type, types.
    bool_, types.bool_))


@numba.njit
def median_series_computation(res, arr, is_parallel, skipna):
    lwa__wxwh = array_to_info(arr)
    _median_series_computation(res, lwa__wxwh, is_parallel, skipna)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(lwa__wxwh)


ll.add_symbol('autocorr_series_computation', quantile_alg.
    autocorr_series_computation)
_autocorr_series_computation = types.ExternalFunction(
    'autocorr_series_computation', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def autocorr_series_computation(res, arr, lag, is_parallel):
    lwa__wxwh = array_to_info(arr)
    _autocorr_series_computation(res, lwa__wxwh, lag, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(lwa__wxwh)


@numba.njit
def autocorr(arr, lag=1, parallel=False):
    res = np.empty(1, types.float64)
    autocorr_series_computation(res.ctypes, arr, lag, parallel)
    return res[0]


ll.add_symbol('compute_series_monotonicity', quantile_alg.
    compute_series_monotonicity)
_compute_series_monotonicity = types.ExternalFunction(
    'compute_series_monotonicity', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def series_monotonicity_call(res, arr, inc_dec, is_parallel):
    lwa__wxwh = array_to_info(arr)
    _compute_series_monotonicity(res, lwa__wxwh, inc_dec, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(lwa__wxwh)


@numba.njit
def series_monotonicity(arr, inc_dec, parallel=False):
    res = np.empty(1, types.float64)
    series_monotonicity_call(res.ctypes, arr, inc_dec, parallel)
    tmdxp__pipfe = res[0] > 0.5
    return tmdxp__pipfe


@numba.generated_jit(nopython=True)
def get_valid_entries_from_date_offset(index_arr, offset, initial_date,
    is_last, is_parallel=False):
    if get_overload_const_bool(is_last):
        elu__ala = '-'
        hroby__kbyx = 'index_arr[0] > threshhold_date'
        ficg__mtao = '1, n+1'
        dzgb__drxg = 'index_arr[-i] <= threshhold_date'
        plnmd__zssv = 'i - 1'
    else:
        elu__ala = '+'
        hroby__kbyx = 'index_arr[-1] < threshhold_date'
        ficg__mtao = 'n'
        dzgb__drxg = 'index_arr[i] >= threshhold_date'
        plnmd__zssv = 'i'
    jka__ihr = (
        'def impl(index_arr, offset, initial_date, is_last, is_parallel=False):\n'
        )
    if types.unliteral(offset) == types.unicode_type:
        jka__ihr += (
            '  with numba.objmode(threshhold_date=bodo.pd_timestamp_type):\n')
        jka__ihr += (
            '    date_offset = pd.tseries.frequencies.to_offset(offset)\n')
        if not get_overload_const_bool(is_last):
            jka__ihr += """    if not isinstance(date_offset, pd._libs.tslibs.Tick) and date_offset.is_on_offset(index_arr[0]):
"""
            jka__ihr += (
                '      threshhold_date = initial_date - date_offset.base + date_offset\n'
                )
            jka__ihr += '    else:\n'
            jka__ihr += '      threshhold_date = initial_date + date_offset\n'
        else:
            jka__ihr += (
                f'    threshhold_date = initial_date {elu__ala} date_offset\n')
    else:
        jka__ihr += f'  threshhold_date = initial_date {elu__ala} offset\n'
    jka__ihr += '  local_valid = 0\n'
    jka__ihr += f'  n = len(index_arr)\n'
    jka__ihr += f'  if n:\n'
    jka__ihr += f'    if {hroby__kbyx}:\n'
    jka__ihr += '      loc_valid = n\n'
    jka__ihr += '    else:\n'
    jka__ihr += f'      for i in range({ficg__mtao}):\n'
    jka__ihr += f'        if {dzgb__drxg}:\n'
    jka__ihr += f'          loc_valid = {plnmd__zssv}\n'
    jka__ihr += '          break\n'
    jka__ihr += '  if is_parallel:\n'
    jka__ihr += (
        '    total_valid = bodo.libs.distributed_api.dist_reduce(loc_valid, sum_op)\n'
        )
    jka__ihr += '    return total_valid\n'
    jka__ihr += '  else:\n'
    jka__ihr += '    return loc_valid\n'
    ohgz__dmpvb = {}
    exec(jka__ihr, {'bodo': bodo, 'pd': pd, 'numba': numba, 'sum_op':
        sum_op}, ohgz__dmpvb)
    return ohgz__dmpvb['impl']


def quantile(A, q):
    return 0


def quantile_parallel(A, q):
    return 0


@infer_global(quantile)
@infer_global(quantile_parallel)
class QuantileType(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) in [2, 3]
        return signature(types.float64, *unliteral_all(args))


@lower_builtin(quantile, types.Array, types.float64)
@lower_builtin(quantile, IntegerArrayType, types.float64)
@lower_builtin(quantile, BooleanArrayType, types.float64)
def lower_dist_quantile_seq(context, builder, sig, args):
    therl__ccxn = numba_to_c_type(sig.args[0].dtype)
    mqaul__kjfs = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), therl__ccxn))
    mbdd__nsdnt = args[0]
    sjyxn__zug = sig.args[0]
    if isinstance(sjyxn__zug, (IntegerArrayType, BooleanArrayType)):
        mbdd__nsdnt = cgutils.create_struct_proxy(sjyxn__zug)(context,
            builder, mbdd__nsdnt).data
        sjyxn__zug = types.Array(sjyxn__zug.dtype, 1, 'C')
    assert sjyxn__zug.ndim == 1
    arr = make_array(sjyxn__zug)(context, builder, mbdd__nsdnt)
    igru__cyxws = builder.extract_value(arr.shape, 0)
    rrru__ghrrp = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        igru__cyxws, args[1], builder.load(mqaul__kjfs)]
    nio__mbc = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        DoubleType(), lir.IntType(32)]
    qod__tur = lir.FunctionType(lir.DoubleType(), nio__mbc)
    qijox__nust = cgutils.get_or_insert_function(builder.module, qod__tur,
        name='quantile_sequential')
    qyn__cmoid = builder.call(qijox__nust, rrru__ghrrp)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return qyn__cmoid


@lower_builtin(quantile_parallel, types.Array, types.float64, types.intp)
@lower_builtin(quantile_parallel, IntegerArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, BooleanArrayType, types.float64, types.intp)
def lower_dist_quantile_parallel(context, builder, sig, args):
    therl__ccxn = numba_to_c_type(sig.args[0].dtype)
    mqaul__kjfs = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), therl__ccxn))
    mbdd__nsdnt = args[0]
    sjyxn__zug = sig.args[0]
    if isinstance(sjyxn__zug, (IntegerArrayType, BooleanArrayType)):
        mbdd__nsdnt = cgutils.create_struct_proxy(sjyxn__zug)(context,
            builder, mbdd__nsdnt).data
        sjyxn__zug = types.Array(sjyxn__zug.dtype, 1, 'C')
    assert sjyxn__zug.ndim == 1
    arr = make_array(sjyxn__zug)(context, builder, mbdd__nsdnt)
    igru__cyxws = builder.extract_value(arr.shape, 0)
    if len(args) == 3:
        nyyg__jil = args[2]
    else:
        nyyg__jil = igru__cyxws
    rrru__ghrrp = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        igru__cyxws, nyyg__jil, args[1], builder.load(mqaul__kjfs)]
    nio__mbc = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.IntType(
        64), lir.DoubleType(), lir.IntType(32)]
    qod__tur = lir.FunctionType(lir.DoubleType(), nio__mbc)
    qijox__nust = cgutils.get_or_insert_function(builder.module, qod__tur,
        name='quantile_parallel')
    qyn__cmoid = builder.call(qijox__nust, rrru__ghrrp)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return qyn__cmoid


@numba.njit
def min_heapify(arr, ind_arr, n, start, cmp_f):
    hhxrt__vdzp = start
    szr__mtfdh = 2 * start + 1
    aromy__txeqj = 2 * start + 2
    if szr__mtfdh < n and not cmp_f(arr[szr__mtfdh], arr[hhxrt__vdzp]):
        hhxrt__vdzp = szr__mtfdh
    if aromy__txeqj < n and not cmp_f(arr[aromy__txeqj], arr[hhxrt__vdzp]):
        hhxrt__vdzp = aromy__txeqj
    if hhxrt__vdzp != start:
        arr[start], arr[hhxrt__vdzp] = arr[hhxrt__vdzp], arr[start]
        ind_arr[start], ind_arr[hhxrt__vdzp] = ind_arr[hhxrt__vdzp], ind_arr[
            start]
        min_heapify(arr, ind_arr, n, hhxrt__vdzp, cmp_f)


def select_k_nonan(A, index_arr, m, k):
    return A[:k]


@overload(select_k_nonan, no_unliteral=True)
def select_k_nonan_overload(A, index_arr, m, k):
    dtype = A.dtype
    if isinstance(dtype, types.Integer):
        return lambda A, index_arr, m, k: (A[:k].copy(), index_arr[:k].copy
            (), k)

    def select_k_nonan_float(A, index_arr, m, k):
        rmrov__wpufb = np.empty(k, A.dtype)
        xauvq__zdpui = np.empty(k, index_arr.dtype)
        i = 0
        ind = 0
        while i < m and ind < k:
            if not bodo.libs.array_kernels.isna(A, i):
                rmrov__wpufb[ind] = A[i]
                xauvq__zdpui[ind] = index_arr[i]
                ind += 1
            i += 1
        if ind < k:
            rmrov__wpufb = rmrov__wpufb[:ind]
            xauvq__zdpui = xauvq__zdpui[:ind]
        return rmrov__wpufb, xauvq__zdpui, i
    return select_k_nonan_float


@numba.njit
def nlargest(A, index_arr, k, is_largest, cmp_f):
    m = len(A)
    if k == 0:
        return A[:0], index_arr[:0]
    if k >= m:
        twosb__podjn = np.sort(A)
        sogml__ntqna = index_arr[np.argsort(A)]
        enpgr__awtlx = pd.Series(twosb__podjn).notna().values
        twosb__podjn = twosb__podjn[enpgr__awtlx]
        sogml__ntqna = sogml__ntqna[enpgr__awtlx]
        if is_largest:
            twosb__podjn = twosb__podjn[::-1]
            sogml__ntqna = sogml__ntqna[::-1]
        return np.ascontiguousarray(twosb__podjn), np.ascontiguousarray(
            sogml__ntqna)
    rmrov__wpufb, xauvq__zdpui, start = select_k_nonan(A, index_arr, m, k)
    xauvq__zdpui = xauvq__zdpui[rmrov__wpufb.argsort()]
    rmrov__wpufb.sort()
    if not is_largest:
        rmrov__wpufb = np.ascontiguousarray(rmrov__wpufb[::-1])
        xauvq__zdpui = np.ascontiguousarray(xauvq__zdpui[::-1])
    for i in range(start, m):
        if cmp_f(A[i], rmrov__wpufb[0]):
            rmrov__wpufb[0] = A[i]
            xauvq__zdpui[0] = index_arr[i]
            min_heapify(rmrov__wpufb, xauvq__zdpui, k, 0, cmp_f)
    xauvq__zdpui = xauvq__zdpui[rmrov__wpufb.argsort()]
    rmrov__wpufb.sort()
    if is_largest:
        rmrov__wpufb = rmrov__wpufb[::-1]
        xauvq__zdpui = xauvq__zdpui[::-1]
    return np.ascontiguousarray(rmrov__wpufb), np.ascontiguousarray(
        xauvq__zdpui)


@numba.njit
def nlargest_parallel(A, I, k, is_largest, cmp_f):
    wkucu__xlk = bodo.libs.distributed_api.get_rank()
    bwgy__vdnu, juc__cxb = nlargest(A, I, k, is_largest, cmp_f)
    gyqnf__ekgd = bodo.libs.distributed_api.gatherv(bwgy__vdnu)
    mnbz__get = bodo.libs.distributed_api.gatherv(juc__cxb)
    if wkucu__xlk == MPI_ROOT:
        res, eriy__ofehi = nlargest(gyqnf__ekgd, mnbz__get, k, is_largest,
            cmp_f)
    else:
        res = np.empty(k, A.dtype)
        eriy__ofehi = np.empty(k, I.dtype)
    bodo.libs.distributed_api.bcast(res)
    bodo.libs.distributed_api.bcast(eriy__ofehi)
    return res, eriy__ofehi


@numba.njit(no_cpython_wrapper=True, cache=True)
def nancorr(mat, cov=0, minpv=1, parallel=False):
    qzh__xjhuw, wzyo__mogql = mat.shape
    wdpaw__gcerf = np.empty((wzyo__mogql, wzyo__mogql), dtype=np.float64)
    for uzi__kli in range(wzyo__mogql):
        for opbef__jllqn in range(uzi__kli + 1):
            ppyfj__pkse = 0
            bzz__gjy = shxq__alnpm = rmwhu__gfq = wxcr__bzyyi = 0.0
            for i in range(qzh__xjhuw):
                if np.isfinite(mat[i, uzi__kli]) and np.isfinite(mat[i,
                    opbef__jllqn]):
                    uzsdf__yff = mat[i, uzi__kli]
                    itg__vnj = mat[i, opbef__jllqn]
                    ppyfj__pkse += 1
                    rmwhu__gfq += uzsdf__yff
                    wxcr__bzyyi += itg__vnj
            if parallel:
                ppyfj__pkse = bodo.libs.distributed_api.dist_reduce(ppyfj__pkse
                    , sum_op)
                rmwhu__gfq = bodo.libs.distributed_api.dist_reduce(rmwhu__gfq,
                    sum_op)
                wxcr__bzyyi = bodo.libs.distributed_api.dist_reduce(wxcr__bzyyi
                    , sum_op)
            if ppyfj__pkse < minpv:
                wdpaw__gcerf[uzi__kli, opbef__jllqn] = wdpaw__gcerf[
                    opbef__jllqn, uzi__kli] = np.nan
            else:
                ojqet__qdof = rmwhu__gfq / ppyfj__pkse
                pdnwp__zoy = wxcr__bzyyi / ppyfj__pkse
                rmwhu__gfq = 0.0
                for i in range(qzh__xjhuw):
                    if np.isfinite(mat[i, uzi__kli]) and np.isfinite(mat[i,
                        opbef__jllqn]):
                        uzsdf__yff = mat[i, uzi__kli] - ojqet__qdof
                        itg__vnj = mat[i, opbef__jllqn] - pdnwp__zoy
                        rmwhu__gfq += uzsdf__yff * itg__vnj
                        bzz__gjy += uzsdf__yff * uzsdf__yff
                        shxq__alnpm += itg__vnj * itg__vnj
                if parallel:
                    rmwhu__gfq = bodo.libs.distributed_api.dist_reduce(
                        rmwhu__gfq, sum_op)
                    bzz__gjy = bodo.libs.distributed_api.dist_reduce(bzz__gjy,
                        sum_op)
                    shxq__alnpm = bodo.libs.distributed_api.dist_reduce(
                        shxq__alnpm, sum_op)
                iryt__adrkr = ppyfj__pkse - 1.0 if cov else sqrt(bzz__gjy *
                    shxq__alnpm)
                if iryt__adrkr != 0.0:
                    wdpaw__gcerf[uzi__kli, opbef__jllqn] = wdpaw__gcerf[
                        opbef__jllqn, uzi__kli] = rmwhu__gfq / iryt__adrkr
                else:
                    wdpaw__gcerf[uzi__kli, opbef__jllqn] = wdpaw__gcerf[
                        opbef__jllqn, uzi__kli] = np.nan
    return wdpaw__gcerf


@numba.njit(no_cpython_wrapper=True)
def duplicated(data, ind_arr, parallel=False):
    if parallel:
        data, (ind_arr,) = bodo.ir.join.parallel_shuffle(data, (ind_arr,))
    data = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data)
    n = len(data[0])
    out = np.empty(n, np.bool_)
    maoaw__uvxrk = dict()
    for i in range(n):
        val = getitem_arr_tup_single(data, i)
        if val in maoaw__uvxrk:
            out[i] = True
        else:
            out[i] = False
            maoaw__uvxrk[val] = 0
    return out, ind_arr


def sample_table_operation(data, ind_arr, n, frac, replace, parallel=False):
    return data, ind_arr


@overload(sample_table_operation, no_unliteral=True)
def overload_sample_table_operation(data, ind_arr, n, frac, replace,
    parallel=False):
    kuma__wncl = len(data)
    jka__ihr = 'def impl(data, ind_arr, n, frac, replace, parallel=False):\n'
    jka__ihr += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        kuma__wncl)))
    jka__ihr += '  table_total = arr_info_list_to_table(info_list_total)\n'
    jka__ihr += (
        '  out_table = sample_table(table_total, n, frac, replace, parallel)\n'
        .format(kuma__wncl))
    for klij__lcjva in range(kuma__wncl):
        jka__ihr += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(klij__lcjva, klij__lcjva, klij__lcjva))
    jka__ihr += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(kuma__wncl))
    jka__ihr += '  delete_table(out_table)\n'
    jka__ihr += '  delete_table(table_total)\n'
    jka__ihr += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(kuma__wncl)))
    ohgz__dmpvb = {}
    exec(jka__ihr, {'np': np, 'bodo': bodo, 'array_to_info': array_to_info,
        'sample_table': sample_table, 'arr_info_list_to_table':
        arr_info_list_to_table, 'info_from_table': info_from_table,
        'info_to_array': info_to_array, 'delete_table': delete_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, ohgz__dmpvb)
    impl = ohgz__dmpvb['impl']
    return impl


def drop_duplicates(data, ind_arr, ncols, parallel=False):
    return data, ind_arr


@overload(drop_duplicates, no_unliteral=True)
def overload_drop_duplicates(data, ind_arr, ncols, parallel=False):
    kuma__wncl = len(data)
    jka__ihr = 'def impl(data, ind_arr, ncols, parallel=False):\n'
    jka__ihr += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        kuma__wncl)))
    jka__ihr += '  table_total = arr_info_list_to_table(info_list_total)\n'
    jka__ihr += '  keep_i = 0\n'
    jka__ihr += """  out_table = drop_duplicates_table(table_total, parallel, ncols, keep_i, False)
"""
    for klij__lcjva in range(kuma__wncl):
        jka__ihr += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(klij__lcjva, klij__lcjva, klij__lcjva))
    jka__ihr += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(kuma__wncl))
    jka__ihr += '  delete_table(out_table)\n'
    jka__ihr += '  delete_table(table_total)\n'
    jka__ihr += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(kuma__wncl)))
    ohgz__dmpvb = {}
    exec(jka__ihr, {'np': np, 'bodo': bodo, 'array_to_info': array_to_info,
        'drop_duplicates_table': drop_duplicates_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, ohgz__dmpvb)
    impl = ohgz__dmpvb['impl']
    return impl


def drop_duplicates_array(data_arr, parallel=False):
    return data_arr


@overload(drop_duplicates_array, no_unliteral=True)
def overload_drop_duplicates_array(data_arr, parallel=False):

    def impl(data_arr, parallel=False):
        cgyoh__bhhg = [array_to_info(data_arr)]
        ezzjc__ijhpy = arr_info_list_to_table(cgyoh__bhhg)
        pjt__blxei = 0
        bxkwj__holgl = drop_duplicates_table(ezzjc__ijhpy, parallel, 1,
            pjt__blxei, False)
        kcxqi__hepb = info_to_array(info_from_table(bxkwj__holgl, 0), data_arr)
        delete_table(bxkwj__holgl)
        delete_table(ezzjc__ijhpy)
        return kcxqi__hepb
    return impl


def dropna(data, how, thresh, subset, parallel=False):
    return data


@overload(dropna, no_unliteral=True)
def overload_dropna(data, how, thresh, subset):
    krt__plq = len(data.types)
    vuc__nsqn = [('out' + str(i)) for i in range(krt__plq)]
    usol__niadq = get_overload_const_list(subset)
    how = get_overload_const_str(how)
    erklb__xbj = ['isna(data[{}], i)'.format(i) for i in usol__niadq]
    bbg__ixvgt = 'not ({})'.format(' or '.join(erklb__xbj))
    if not is_overload_none(thresh):
        bbg__ixvgt = '(({}) <= ({}) - thresh)'.format(' + '.join(erklb__xbj
            ), krt__plq - 1)
    elif how == 'all':
        bbg__ixvgt = 'not ({})'.format(' and '.join(erklb__xbj))
    jka__ihr = 'def _dropna_imp(data, how, thresh, subset):\n'
    jka__ihr += '  old_len = len(data[0])\n'
    jka__ihr += '  new_len = 0\n'
    jka__ihr += '  for i in range(old_len):\n'
    jka__ihr += '    if {}:\n'.format(bbg__ixvgt)
    jka__ihr += '      new_len += 1\n'
    for i, out in enumerate(vuc__nsqn):
        if isinstance(data[i], bodo.CategoricalArrayType):
            jka__ihr += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, data[{1}], (-1,))\n'
                .format(out, i))
        else:
            jka__ihr += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, t{1}, (-1,))\n'
                .format(out, i))
    jka__ihr += '  curr_ind = 0\n'
    jka__ihr += '  for i in range(old_len):\n'
    jka__ihr += '    if {}:\n'.format(bbg__ixvgt)
    for i in range(krt__plq):
        jka__ihr += '      if isna(data[{}], i):\n'.format(i)
        jka__ihr += '        setna({}, curr_ind)\n'.format(vuc__nsqn[i])
        jka__ihr += '      else:\n'
        jka__ihr += '        {}[curr_ind] = data[{}][i]\n'.format(vuc__nsqn
            [i], i)
    jka__ihr += '      curr_ind += 1\n'
    jka__ihr += '  return {}\n'.format(', '.join(vuc__nsqn))
    ohgz__dmpvb = {}
    rpnxg__edclm = {'t{}'.format(i): tkcxx__hctq for i, tkcxx__hctq in
        enumerate(data.types)}
    rpnxg__edclm.update({'isna': isna, 'setna': setna, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'bodo': bodo})
    exec(jka__ihr, rpnxg__edclm, ohgz__dmpvb)
    djj__eqwom = ohgz__dmpvb['_dropna_imp']
    return djj__eqwom


def get(arr, ind):
    return pd.Series(arr).str.get(ind)


@overload(get, no_unliteral=True)
def overload_get(arr, ind):
    if isinstance(arr, ArrayItemArrayType):
        sjyxn__zug = arr.dtype
        olorw__nbm = sjyxn__zug.dtype

        def get_arr_item(arr, ind):
            n = len(arr)
            hogtf__fprro = init_nested_counts(olorw__nbm)
            for k in range(n):
                if bodo.libs.array_kernels.isna(arr, k):
                    continue
                val = arr[k]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    continue
                hogtf__fprro = add_nested_counts(hogtf__fprro, val[ind])
            kcxqi__hepb = bodo.utils.utils.alloc_type(n, sjyxn__zug,
                hogtf__fprro)
            for vetct__pnbxm in range(n):
                if bodo.libs.array_kernels.isna(arr, vetct__pnbxm):
                    setna(kcxqi__hepb, vetct__pnbxm)
                    continue
                val = arr[vetct__pnbxm]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    setna(kcxqi__hepb, vetct__pnbxm)
                    continue
                kcxqi__hepb[vetct__pnbxm] = val[ind]
            return kcxqi__hepb
        return get_arr_item


def concat(arr_list):
    return pd.concat(arr_list)


@overload(concat, no_unliteral=True)
def concat_overload(arr_list):
    if isinstance(arr_list, bodo.NullableTupleType):
        return lambda arr_list: bodo.libs.array_kernels.concat(arr_list._data)
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, ArrayItemArrayType):
        gea__hryy = arr_list.dtype.dtype

        def array_item_concat_impl(arr_list):
            oien__qwubn = 0
            pqs__zlbmm = []
            for A in arr_list:
                qvcmg__bonfo = len(A)
                bodo.libs.array_item_arr_ext.trim_excess_data(A)
                pqs__zlbmm.append(bodo.libs.array_item_arr_ext.get_data(A))
                oien__qwubn += qvcmg__bonfo
            oky__yvsn = np.empty(oien__qwubn + 1, offset_type)
            wrg__lahv = bodo.libs.array_kernels.concat(pqs__zlbmm)
            gsm__ixt = np.empty(oien__qwubn + 7 >> 3, np.uint8)
            elbxj__rme = 0
            xusc__hidu = 0
            for A in arr_list:
                dgccl__hvcvd = bodo.libs.array_item_arr_ext.get_offsets(A)
                uxv__hyh = bodo.libs.array_item_arr_ext.get_null_bitmap(A)
                qvcmg__bonfo = len(A)
                oxkl__jrgb = dgccl__hvcvd[qvcmg__bonfo]
                for i in range(qvcmg__bonfo):
                    oky__yvsn[i + elbxj__rme] = dgccl__hvcvd[i] + xusc__hidu
                    kru__oogcs = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        uxv__hyh, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(gsm__ixt, i +
                        elbxj__rme, kru__oogcs)
                elbxj__rme += qvcmg__bonfo
                xusc__hidu += oxkl__jrgb
            oky__yvsn[elbxj__rme] = xusc__hidu
            kcxqi__hepb = bodo.libs.array_item_arr_ext.init_array_item_array(
                oien__qwubn, wrg__lahv, oky__yvsn, gsm__ixt)
            return kcxqi__hepb
        return array_item_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.StructArrayType):
        mgh__vswe = arr_list.dtype.names
        jka__ihr = 'def struct_array_concat_impl(arr_list):\n'
        jka__ihr += f'    n_all = 0\n'
        for i in range(len(mgh__vswe)):
            jka__ihr += f'    concat_list{i} = []\n'
        jka__ihr += '    for A in arr_list:\n'
        jka__ihr += (
            '        data_tuple = bodo.libs.struct_arr_ext.get_data(A)\n')
        for i in range(len(mgh__vswe)):
            jka__ihr += f'        concat_list{i}.append(data_tuple[{i}])\n'
        jka__ihr += '        n_all += len(A)\n'
        jka__ihr += '    n_bytes = (n_all + 7) >> 3\n'
        jka__ihr += '    new_mask = np.empty(n_bytes, np.uint8)\n'
        jka__ihr += '    curr_bit = 0\n'
        jka__ihr += '    for A in arr_list:\n'
        jka__ihr += (
            '        old_mask = bodo.libs.struct_arr_ext.get_null_bitmap(A)\n')
        jka__ihr += '        for j in range(len(A)):\n'
        jka__ihr += (
            '            bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        jka__ihr += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        jka__ihr += '            curr_bit += 1\n'
        jka__ihr += '    return bodo.libs.struct_arr_ext.init_struct_arr(\n'
        gvgd__vhm = ', '.join([
            f'bodo.libs.array_kernels.concat(concat_list{i})' for i in
            range(len(mgh__vswe))])
        jka__ihr += f'        ({gvgd__vhm},),\n'
        jka__ihr += '        new_mask,\n'
        jka__ihr += f'        {mgh__vswe},\n'
        jka__ihr += '    )\n'
        ohgz__dmpvb = {}
        exec(jka__ihr, {'bodo': bodo, 'np': np}, ohgz__dmpvb)
        return ohgz__dmpvb['struct_array_concat_impl']
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_date_array_type:

        def datetime_date_array_concat_impl(arr_list):
            eumli__gbwhd = 0
            for A in arr_list:
                eumli__gbwhd += len(A)
            ovkp__fbfjm = (bodo.hiframes.datetime_date_ext.
                alloc_datetime_date_array(eumli__gbwhd))
            qbab__rcc = 0
            for A in arr_list:
                for i in range(len(A)):
                    ovkp__fbfjm._data[i + qbab__rcc] = A._data[i]
                    kru__oogcs = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(ovkp__fbfjm.
                        _null_bitmap, i + qbab__rcc, kru__oogcs)
                qbab__rcc += len(A)
            return ovkp__fbfjm
        return datetime_date_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_timedelta_array_type:

        def datetime_timedelta_array_concat_impl(arr_list):
            eumli__gbwhd = 0
            for A in arr_list:
                eumli__gbwhd += len(A)
            ovkp__fbfjm = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(eumli__gbwhd))
            qbab__rcc = 0
            for A in arr_list:
                for i in range(len(A)):
                    ovkp__fbfjm._days_data[i + qbab__rcc] = A._days_data[i]
                    ovkp__fbfjm._seconds_data[i + qbab__rcc] = A._seconds_data[
                        i]
                    ovkp__fbfjm._microseconds_data[i + qbab__rcc
                        ] = A._microseconds_data[i]
                    kru__oogcs = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(ovkp__fbfjm.
                        _null_bitmap, i + qbab__rcc, kru__oogcs)
                qbab__rcc += len(A)
            return ovkp__fbfjm
        return datetime_timedelta_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, DecimalArrayType):
        oqb__ovlt = arr_list.dtype.precision
        rjevd__kizc = arr_list.dtype.scale

        def decimal_array_concat_impl(arr_list):
            eumli__gbwhd = 0
            for A in arr_list:
                eumli__gbwhd += len(A)
            ovkp__fbfjm = bodo.libs.decimal_arr_ext.alloc_decimal_array(
                eumli__gbwhd, oqb__ovlt, rjevd__kizc)
            qbab__rcc = 0
            for A in arr_list:
                for i in range(len(A)):
                    ovkp__fbfjm._data[i + qbab__rcc] = A._data[i]
                    kru__oogcs = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(ovkp__fbfjm.
                        _null_bitmap, i + qbab__rcc, kru__oogcs)
                qbab__rcc += len(A)
            return ovkp__fbfjm
        return decimal_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype in [string_array_type, bodo.binary_array_type]:
        if arr_list.dtype == bodo.binary_array_type:
            zyabt__dmw = 'bodo.libs.str_arr_ext.pre_alloc_binary_array'
        elif arr_list.dtype == string_array_type:
            zyabt__dmw = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        jka__ihr = 'def impl(arr_list):  # pragma: no cover\n'
        jka__ihr += '    # preallocate the output\n'
        jka__ihr += '    num_strs = 0\n'
        jka__ihr += '    num_chars = 0\n'
        jka__ihr += '    for A in arr_list:\n'
        jka__ihr += '        arr = A\n'
        jka__ihr += '        num_strs += len(arr)\n'
        jka__ihr += '        # this should work for both binary and string\n'
        jka__ihr += (
            '        num_chars += bodo.libs.str_arr_ext.num_total_chars(arr)\n'
            )
        jka__ihr += f'    out_arr = {zyabt__dmw}(\n'
        jka__ihr += '        num_strs, num_chars\n'
        jka__ihr += '    )\n'
        jka__ihr += (
            '    bodo.libs.str_arr_ext.set_null_bits_to_value(out_arr, -1)\n')
        jka__ihr += '    # copy data to output\n'
        jka__ihr += '    curr_str_ind = 0\n'
        jka__ihr += '    curr_chars_ind = 0\n'
        jka__ihr += '    for A in arr_list:\n'
        jka__ihr += '        arr = A\n'
        jka__ihr += '        # This will probably need to be extended\n'
        jka__ihr += '        bodo.libs.str_arr_ext.set_string_array_range(\n'
        jka__ihr += '            out_arr, arr, curr_str_ind, curr_chars_ind\n'
        jka__ihr += '        )\n'
        jka__ihr += '        curr_str_ind += len(arr)\n'
        jka__ihr += '        # this should work for both binary and string\n'
        jka__ihr += (
            '        curr_chars_ind += bodo.libs.str_arr_ext.num_total_chars(arr)\n'
            )
        jka__ihr += '    return out_arr\n'
        hyjkz__ermoi = dict()
        exec(jka__ihr, {'bodo': bodo}, hyjkz__ermoi)
        gaoaa__bsw = hyjkz__ermoi['impl']
        return gaoaa__bsw
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, IntegerArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(tkcxx__hctq.dtype, types.Integer) for
        tkcxx__hctq in arr_list.types) and any(isinstance(tkcxx__hctq,
        IntegerArrayType) for tkcxx__hctq in arr_list.types):

        def impl_int_arr_list(arr_list):
            fapn__pxqt = convert_to_nullable_tup(arr_list)
            jbuc__zuwe = []
            gnfld__bdbjw = 0
            for A in fapn__pxqt:
                jbuc__zuwe.append(A._data)
                gnfld__bdbjw += len(A)
            wrg__lahv = bodo.libs.array_kernels.concat(jbuc__zuwe)
            yiwlu__owaw = gnfld__bdbjw + 7 >> 3
            rggc__dqwpy = np.empty(yiwlu__owaw, np.uint8)
            ohvbz__opxje = 0
            for A in fapn__pxqt:
                uzzr__wjrz = A._null_bitmap
                for vetct__pnbxm in range(len(A)):
                    kru__oogcs = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        uzzr__wjrz, vetct__pnbxm)
                    bodo.libs.int_arr_ext.set_bit_to_arr(rggc__dqwpy,
                        ohvbz__opxje, kru__oogcs)
                    ohvbz__opxje += 1
            return bodo.libs.int_arr_ext.init_integer_array(wrg__lahv,
                rggc__dqwpy)
        return impl_int_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == boolean_array or isinstance(arr_list, types
        .BaseTuple) and all(tkcxx__hctq.dtype == types.bool_ for
        tkcxx__hctq in arr_list.types) and any(tkcxx__hctq == boolean_array for
        tkcxx__hctq in arr_list.types):

        def impl_bool_arr_list(arr_list):
            fapn__pxqt = convert_to_nullable_tup(arr_list)
            jbuc__zuwe = []
            gnfld__bdbjw = 0
            for A in fapn__pxqt:
                jbuc__zuwe.append(A._data)
                gnfld__bdbjw += len(A)
            wrg__lahv = bodo.libs.array_kernels.concat(jbuc__zuwe)
            yiwlu__owaw = gnfld__bdbjw + 7 >> 3
            rggc__dqwpy = np.empty(yiwlu__owaw, np.uint8)
            ohvbz__opxje = 0
            for A in fapn__pxqt:
                uzzr__wjrz = A._null_bitmap
                for vetct__pnbxm in range(len(A)):
                    kru__oogcs = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        uzzr__wjrz, vetct__pnbxm)
                    bodo.libs.int_arr_ext.set_bit_to_arr(rggc__dqwpy,
                        ohvbz__opxje, kru__oogcs)
                    ohvbz__opxje += 1
            return bodo.libs.bool_arr_ext.init_bool_array(wrg__lahv,
                rggc__dqwpy)
        return impl_bool_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, CategoricalArrayType):

        def cat_array_concat_impl(arr_list):
            gvj__kyibo = []
            for A in arr_list:
                gvj__kyibo.append(A.codes)
            return init_categorical_array(bodo.libs.array_kernels.concat(
                gvj__kyibo), arr_list[0].dtype)
        return cat_array_concat_impl
    if isinstance(arr_list, types.List) and isinstance(arr_list.dtype,
        types.Array) and arr_list.dtype.ndim == 1:
        dtype = arr_list.dtype.dtype

        def impl_np_arr_list(arr_list):
            gnfld__bdbjw = 0
            for A in arr_list:
                gnfld__bdbjw += len(A)
            kcxqi__hepb = np.empty(gnfld__bdbjw, dtype)
            sboue__ufpyv = 0
            for A in arr_list:
                n = len(A)
                kcxqi__hepb[sboue__ufpyv:sboue__ufpyv + n] = A
                sboue__ufpyv += n
            return kcxqi__hepb
        return impl_np_arr_list
    if isinstance(arr_list, types.BaseTuple) and any(isinstance(tkcxx__hctq,
        (types.Array, IntegerArrayType)) and isinstance(tkcxx__hctq.dtype,
        types.Integer) for tkcxx__hctq in arr_list.types) and any(
        isinstance(tkcxx__hctq, types.Array) and isinstance(tkcxx__hctq.
        dtype, types.Float) for tkcxx__hctq in arr_list.types):
        return lambda arr_list: np.concatenate(astype_float_tup(arr_list))
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.MapArrayType):

        def impl_map_arr_list(arr_list):
            wpqlx__bph = []
            for A in arr_list:
                wpqlx__bph.append(A._data)
            isym__wcxyr = bodo.libs.array_kernels.concat(wpqlx__bph)
            wdpaw__gcerf = bodo.libs.map_arr_ext.init_map_arr(isym__wcxyr)
            return wdpaw__gcerf
        return impl_map_arr_list
    for mrz__pygx in arr_list:
        if not isinstance(mrz__pygx, types.Array):
            raise_bodo_error('concat of array types {} not supported'.
                format(arr_list))
    return lambda arr_list: np.concatenate(arr_list)


def astype_float_tup(arr_tup):
    return tuple(tkcxx__hctq.astype(np.float64) for tkcxx__hctq in arr_tup)


@overload(astype_float_tup, no_unliteral=True)
def overload_astype_float_tup(arr_tup):
    assert isinstance(arr_tup, types.BaseTuple)
    kuma__wncl = len(arr_tup.types)
    jka__ihr = 'def f(arr_tup):\n'
    jka__ihr += '  return ({}{})\n'.format(','.join(
        'arr_tup[{}].astype(np.float64)'.format(i) for i in range(
        kuma__wncl)), ',' if kuma__wncl == 1 else '')
    ohgz__dmpvb = {}
    exec(jka__ihr, {'np': np}, ohgz__dmpvb)
    pnasc__ecipp = ohgz__dmpvb['f']
    return pnasc__ecipp


def convert_to_nullable_tup(arr_tup):
    return arr_tup


@overload(convert_to_nullable_tup, no_unliteral=True)
def overload_convert_to_nullable_tup(arr_tup):
    if isinstance(arr_tup, (types.UniTuple, types.List)) and isinstance(arr_tup
        .dtype, (IntegerArrayType, BooleanArrayType)):
        return lambda arr_tup: arr_tup
    assert isinstance(arr_tup, types.BaseTuple)
    kuma__wncl = len(arr_tup.types)
    wwg__mypzu = find_common_np_dtype(arr_tup.types)
    olorw__nbm = None
    lxj__qwnjw = ''
    if isinstance(wwg__mypzu, types.Integer):
        olorw__nbm = bodo.libs.int_arr_ext.IntDtype(wwg__mypzu)
        lxj__qwnjw = '.astype(out_dtype, False)'
    jka__ihr = 'def f(arr_tup):\n'
    jka__ihr += '  return ({}{})\n'.format(','.join(
        'bodo.utils.conversion.coerce_to_array(arr_tup[{}], use_nullable_array=True){}'
        .format(i, lxj__qwnjw) for i in range(kuma__wncl)), ',' if 
        kuma__wncl == 1 else '')
    ohgz__dmpvb = {}
    exec(jka__ihr, {'bodo': bodo, 'out_dtype': olorw__nbm}, ohgz__dmpvb)
    lhmdx__spi = ohgz__dmpvb['f']
    return lhmdx__spi


def nunique(A, dropna):
    return len(set(A))


def nunique_parallel(A, dropna):
    return len(set(A))


@overload(nunique, no_unliteral=True)
def nunique_overload(A, dropna):

    def nunique_seq(A, dropna):
        s, rlgzw__wuxes = build_set_seen_na(A)
        return len(s) + int(not dropna and rlgzw__wuxes)
    return nunique_seq


@overload(nunique_parallel, no_unliteral=True)
def nunique_overload_parallel(A, dropna):
    sum_op = bodo.libs.distributed_api.Reduce_Type.Sum.value

    def nunique_par(A, dropna):
        wrdu__xrw = bodo.libs.array_kernels.unique(A, dropna, parallel=True)
        kdx__sqkqt = len(wrdu__xrw)
        return bodo.libs.distributed_api.dist_reduce(kdx__sqkqt, np.int32(
            sum_op))
    return nunique_par


def unique(A, dropna=False, parallel=False):
    return np.array([egwuf__vqly for egwuf__vqly in set(A)]).astype(A.dtype)


def cummin(A):
    return A


@overload(cummin, no_unliteral=True)
def cummin_overload(A):
    if isinstance(A.dtype, types.Float):
        oyly__bjb = np.finfo(A.dtype(1).dtype).max
    else:
        oyly__bjb = np.iinfo(A.dtype(1).dtype).max

    def impl(A):
        n = len(A)
        kcxqi__hepb = np.empty(n, A.dtype)
        mllm__mwzpz = oyly__bjb
        for i in range(n):
            mllm__mwzpz = min(mllm__mwzpz, A[i])
            kcxqi__hepb[i] = mllm__mwzpz
        return kcxqi__hepb
    return impl


def cummax(A):
    return A


@overload(cummax, no_unliteral=True)
def cummax_overload(A):
    if isinstance(A.dtype, types.Float):
        oyly__bjb = np.finfo(A.dtype(1).dtype).min
    else:
        oyly__bjb = np.iinfo(A.dtype(1).dtype).min

    def impl(A):
        n = len(A)
        kcxqi__hepb = np.empty(n, A.dtype)
        mllm__mwzpz = oyly__bjb
        for i in range(n):
            mllm__mwzpz = max(mllm__mwzpz, A[i])
            kcxqi__hepb[i] = mllm__mwzpz
        return kcxqi__hepb
    return impl


@overload(unique, no_unliteral=True)
def unique_overload(A, dropna=False, parallel=False):

    def unique_impl(A, dropna=False, parallel=False):
        qmqks__eprfh = arr_info_list_to_table([array_to_info(A)])
        kpd__bfhe = 1
        pjt__blxei = 0
        bxkwj__holgl = drop_duplicates_table(qmqks__eprfh, parallel,
            kpd__bfhe, pjt__blxei, dropna)
        kcxqi__hepb = info_to_array(info_from_table(bxkwj__holgl, 0), A)
        delete_table(qmqks__eprfh)
        delete_table(bxkwj__holgl)
        return kcxqi__hepb
    return unique_impl


def explode(arr, index_arr):
    return pd.Series(arr, index_arr).explode()


@overload(explode, no_unliteral=True)
def overload_explode(arr, index_arr):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    gea__hryy = bodo.utils.typing.to_nullable_type(arr.dtype)
    dpnt__bgxnw = index_arr
    evc__agkln = dpnt__bgxnw.dtype

    def impl(arr, index_arr):
        n = len(arr)
        hogtf__fprro = init_nested_counts(gea__hryy)
        mfcao__psn = init_nested_counts(evc__agkln)
        for i in range(n):
            ywzx__ammtm = index_arr[i]
            if isna(arr, i):
                hogtf__fprro = (hogtf__fprro[0] + 1,) + hogtf__fprro[1:]
                mfcao__psn = add_nested_counts(mfcao__psn, ywzx__ammtm)
                continue
            tgp__zddfq = arr[i]
            if len(tgp__zddfq) == 0:
                hogtf__fprro = (hogtf__fprro[0] + 1,) + hogtf__fprro[1:]
                mfcao__psn = add_nested_counts(mfcao__psn, ywzx__ammtm)
                continue
            hogtf__fprro = add_nested_counts(hogtf__fprro, tgp__zddfq)
            for oewp__przn in range(len(tgp__zddfq)):
                mfcao__psn = add_nested_counts(mfcao__psn, ywzx__ammtm)
        kcxqi__hepb = bodo.utils.utils.alloc_type(hogtf__fprro[0],
            gea__hryy, hogtf__fprro[1:])
        vjz__skxt = bodo.utils.utils.alloc_type(hogtf__fprro[0],
            dpnt__bgxnw, mfcao__psn)
        xusc__hidu = 0
        for i in range(n):
            if isna(arr, i):
                setna(kcxqi__hepb, xusc__hidu)
                vjz__skxt[xusc__hidu] = index_arr[i]
                xusc__hidu += 1
                continue
            tgp__zddfq = arr[i]
            oxkl__jrgb = len(tgp__zddfq)
            if oxkl__jrgb == 0:
                setna(kcxqi__hepb, xusc__hidu)
                vjz__skxt[xusc__hidu] = index_arr[i]
                xusc__hidu += 1
                continue
            kcxqi__hepb[xusc__hidu:xusc__hidu + oxkl__jrgb] = tgp__zddfq
            vjz__skxt[xusc__hidu:xusc__hidu + oxkl__jrgb] = index_arr[i]
            xusc__hidu += oxkl__jrgb
        return kcxqi__hepb, vjz__skxt
    return impl


def explode_str_split(arr, pat, n, index_arr):
    return pd.Series(arr, index_arr).str.split(pat, n).explode()


@overload(explode_str_split, no_unliteral=True)
def overload_explode_str_split(arr, pat, n, index_arr):
    assert arr == string_array_type
    dpnt__bgxnw = index_arr
    evc__agkln = dpnt__bgxnw.dtype

    def impl(arr, pat, n, index_arr):
        zfles__gcze = pat is not None and len(pat) > 1
        if zfles__gcze:
            zib__zdppc = re.compile(pat)
            if n == -1:
                n = 0
        elif n == 0:
            n = -1
        soekb__gyfwe = len(arr)
        khhef__tcoe = 0
        hlr__bifg = 0
        mfcao__psn = init_nested_counts(evc__agkln)
        for i in range(soekb__gyfwe):
            ywzx__ammtm = index_arr[i]
            if bodo.libs.array_kernels.isna(arr, i):
                khhef__tcoe += 1
                mfcao__psn = add_nested_counts(mfcao__psn, ywzx__ammtm)
                continue
            if zfles__gcze:
                klfl__ishwg = zib__zdppc.split(arr[i], maxsplit=n)
            else:
                klfl__ishwg = arr[i].split(pat, n)
            khhef__tcoe += len(klfl__ishwg)
            for s in klfl__ishwg:
                mfcao__psn = add_nested_counts(mfcao__psn, ywzx__ammtm)
                hlr__bifg += bodo.libs.str_arr_ext.get_utf8_size(s)
        kcxqi__hepb = bodo.libs.str_arr_ext.pre_alloc_string_array(khhef__tcoe,
            hlr__bifg)
        vjz__skxt = bodo.utils.utils.alloc_type(khhef__tcoe, dpnt__bgxnw,
            mfcao__psn)
        qxo__oqrq = 0
        for vetct__pnbxm in range(soekb__gyfwe):
            if isna(arr, vetct__pnbxm):
                kcxqi__hepb[qxo__oqrq] = ''
                bodo.libs.array_kernels.setna(kcxqi__hepb, qxo__oqrq)
                vjz__skxt[qxo__oqrq] = index_arr[vetct__pnbxm]
                qxo__oqrq += 1
                continue
            if zfles__gcze:
                klfl__ishwg = zib__zdppc.split(arr[vetct__pnbxm], maxsplit=n)
            else:
                klfl__ishwg = arr[vetct__pnbxm].split(pat, n)
            sxlmj__lklf = len(klfl__ishwg)
            kcxqi__hepb[qxo__oqrq:qxo__oqrq + sxlmj__lklf] = klfl__ishwg
            vjz__skxt[qxo__oqrq:qxo__oqrq + sxlmj__lklf] = index_arr[
                vetct__pnbxm]
            qxo__oqrq += sxlmj__lklf
        return kcxqi__hepb, vjz__skxt
    return impl


def gen_na_array(n, arr):
    return np.full(n, np.nan)


@overload(gen_na_array, no_unliteral=True)
def overload_gen_na_array(n, arr):
    if isinstance(arr, types.TypeRef):
        arr = arr.instance_type
    dtype = arr.dtype
    if isinstance(dtype, (types.Integer, types.Float)):
        dtype = dtype if isinstance(dtype, types.Float) else types.float64

        def impl_float(n, arr):
            numba.parfors.parfor.init_prange()
            kcxqi__hepb = np.empty(n, dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                kcxqi__hepb[i] = np.nan
            return kcxqi__hepb
        return impl_float

    def impl(n, arr):
        numba.parfors.parfor.init_prange()
        kcxqi__hepb = bodo.utils.utils.alloc_type(n, arr, (0,))
        for i in numba.parfors.parfor.internal_prange(n):
            setna(kcxqi__hepb, i)
        return kcxqi__hepb
    return impl


def gen_na_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_array_kernels_gen_na_array = (
    gen_na_array_equiv)


def resize_and_copy(A, new_len):
    return A


@overload(resize_and_copy, no_unliteral=True)
def overload_resize_and_copy(A, old_size, new_len):
    nkbu__jyeqa = A
    if A == types.Array(types.uint8, 1, 'C'):

        def impl_char(A, old_size, new_len):
            kcxqi__hepb = bodo.utils.utils.alloc_type(new_len, nkbu__jyeqa)
            bodo.libs.str_arr_ext.str_copy_ptr(kcxqi__hepb.ctypes, 0, A.
                ctypes, old_size)
            return kcxqi__hepb
        return impl_char

    def impl(A, old_size, new_len):
        kcxqi__hepb = bodo.utils.utils.alloc_type(new_len, nkbu__jyeqa, (-1,))
        kcxqi__hepb[:old_size] = A[:old_size]
        return kcxqi__hepb
    return impl


@register_jitable
def calc_nitems(start, stop, step):
    jdqqw__gbfm = math.ceil((stop - start) / step)
    return int(max(jdqqw__gbfm, 0))


def calc_nitems_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    if guard(find_const, self.func_ir, args[0]) == 0 and guard(find_const,
        self.func_ir, args[2]) == 1:
        return ArrayAnalysis.AnalyzeResult(shape=args[1], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_array_kernels_calc_nitems = (
    calc_nitems_equiv)


def arange_parallel_impl(return_type, *args):
    dtype = as_dtype(return_type.dtype)

    def arange_1(stop):
        return np.arange(0, stop, 1, dtype)

    def arange_2(start, stop):
        return np.arange(start, stop, 1, dtype)

    def arange_3(start, stop, step):
        return np.arange(start, stop, step, dtype)
    if any(isinstance(egwuf__vqly, types.Complex) for egwuf__vqly in args):

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            iujw__wzjji = (stop - start) / step
            jdqqw__gbfm = math.ceil(iujw__wzjji.real)
            qxte__wah = math.ceil(iujw__wzjji.imag)
            knhj__laclh = int(max(min(qxte__wah, jdqqw__gbfm), 0))
            arr = np.empty(knhj__laclh, dtype)
            for i in numba.parfors.parfor.internal_prange(knhj__laclh):
                arr[i] = start + i * step
            return arr
    else:

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            knhj__laclh = bodo.libs.array_kernels.calc_nitems(start, stop, step
                )
            arr = np.empty(knhj__laclh, dtype)
            for i in numba.parfors.parfor.internal_prange(knhj__laclh):
                arr[i] = start + i * step
            return arr
    if len(args) == 1:
        return arange_1
    elif len(args) == 2:
        return arange_2
    elif len(args) == 3:
        return arange_3
    elif len(args) == 4:
        return arange_4
    else:
        raise BodoError('parallel arange with types {}'.format(args))


if bodo.numba_compat._check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.arange_parallel_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c72b0390b4f3e52dcc5426bd42c6b55ff96bae5a425381900985d36e7527a4bd':
        warnings.warn('numba.parfors.parfor.arange_parallel_impl has changed')
numba.parfors.parfor.swap_functions_map['arange', 'numpy'
    ] = arange_parallel_impl


def sort(arr, ascending, inplace):
    return np.sort(arr)


@overload(sort, no_unliteral=True)
def overload_sort(arr, ascending, inplace):

    def impl(arr, ascending, inplace):
        n = len(arr)
        data = np.arange(n),
        jim__zngex = arr,
        if not inplace:
            jim__zngex = arr.copy(),
        yxxjs__kgf = bodo.libs.str_arr_ext.to_list_if_immutable_arr(jim__zngex)
        vfj__jzxt = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data, True)
        bodo.libs.timsort.sort(yxxjs__kgf, 0, n, vfj__jzxt)
        if not ascending:
            bodo.libs.timsort.reverseRange(yxxjs__kgf, 0, n, vfj__jzxt)
        bodo.libs.str_arr_ext.cp_str_list_to_array(jim__zngex, yxxjs__kgf)
        return jim__zngex[0]
    return impl


def overload_array_max(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).max()
        return impl


overload(np.max, inline='always', no_unliteral=True)(overload_array_max)
overload(max, inline='always', no_unliteral=True)(overload_array_max)


def overload_array_min(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).min()
        return impl


overload(np.min, inline='always', no_unliteral=True)(overload_array_min)
overload(min, inline='always', no_unliteral=True)(overload_array_min)


def overload_array_sum(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).sum()
    return impl


overload(np.sum, inline='always', no_unliteral=True)(overload_array_sum)
overload(sum, inline='always', no_unliteral=True)(overload_array_sum)


@overload(np.prod, inline='always', no_unliteral=True)
def overload_array_prod(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).prod()
    return impl


def nonzero(arr):
    return arr,


@overload(nonzero, no_unliteral=True)
def nonzero_overload(A, parallel=False):
    if not bodo.utils.utils.is_array_typ(A, False):
        return

    def impl(A, parallel=False):
        n = len(A)
        if parallel:
            offset = bodo.libs.distributed_api.dist_exscan(n, Reduce_Type.
                Sum.value)
        else:
            offset = 0
        wdpaw__gcerf = []
        for i in range(n):
            if A[i]:
                wdpaw__gcerf.append(i + offset)
        return np.array(wdpaw__gcerf, np.int64),
    return impl


def ffill_bfill_arr(arr):
    return arr


@overload(ffill_bfill_arr, no_unliteral=True)
def ffill_bfill_overload(A, method, parallel=False):
    nkbu__jyeqa = element_type(A)
    if nkbu__jyeqa == types.unicode_type:
        null_value = '""'
    elif nkbu__jyeqa == types.bool_:
        null_value = 'False'
    elif nkbu__jyeqa == bodo.datetime64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_datetime(0))')
    elif nkbu__jyeqa == bodo.timedelta64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_timedelta(0))')
    else:
        null_value = '0'
    qxo__oqrq = 'i'
    lhy__nyoua = False
    hgpwg__xnlf = get_overload_const_str(method)
    if hgpwg__xnlf in ('ffill', 'pad'):
        vjoq__pnvc = 'n'
        send_right = True
    elif hgpwg__xnlf in ('backfill', 'bfill'):
        vjoq__pnvc = 'n-1, -1, -1'
        send_right = False
        if nkbu__jyeqa == types.unicode_type:
            qxo__oqrq = '(n - 1) - i'
            lhy__nyoua = True
    jka__ihr = 'def impl(A, method, parallel=False):\n'
    jka__ihr += '  has_last_value = False\n'
    jka__ihr += f'  last_value = {null_value}\n'
    jka__ihr += '  if parallel:\n'
    jka__ihr += '    rank = bodo.libs.distributed_api.get_rank()\n'
    jka__ihr += '    n_pes = bodo.libs.distributed_api.get_size()\n'
    jka__ihr += f"""    has_last_value, last_value = null_border_icomm(A, rank, n_pes, {null_value}, {send_right})
"""
    jka__ihr += '  n = len(A)\n'
    jka__ihr += '  out_arr = bodo.utils.utils.alloc_type(n, A, (-1,))\n'
    jka__ihr += f'  for i in range({vjoq__pnvc}):\n'
    jka__ihr += (
        '    if (bodo.libs.array_kernels.isna(A, i) and not has_last_value):\n'
        )
    jka__ihr += f'      bodo.libs.array_kernels.setna(out_arr, {qxo__oqrq})\n'
    jka__ihr += '      continue\n'
    jka__ihr += '    s = A[i]\n'
    jka__ihr += '    if bodo.libs.array_kernels.isna(A, i):\n'
    jka__ihr += '      s = last_value\n'
    jka__ihr += f'    out_arr[{qxo__oqrq}] = s\n'
    jka__ihr += '    last_value = s\n'
    jka__ihr += '    has_last_value = True\n'
    if lhy__nyoua:
        jka__ihr += '  return out_arr[::-1]\n'
    else:
        jka__ihr += '  return out_arr\n'
    vos__bmhg = {}
    exec(jka__ihr, {'bodo': bodo, 'numba': numba, 'pd': pd,
        'null_border_icomm': null_border_icomm}, vos__bmhg)
    impl = vos__bmhg['impl']
    return impl


@register_jitable(cache=True)
def null_border_icomm(in_arr, rank, n_pes, null_value, send_right=True):
    if send_right:
        cmctc__oic = 0
        lgqc__uia = n_pes - 1
        swwrh__byho = np.int32(rank + 1)
        pjwz__prgha = np.int32(rank - 1)
        fdfi__xrxch = len(in_arr) - 1
        tubs__ortaz = -1
        ofv__ktcf = -1
    else:
        cmctc__oic = n_pes - 1
        lgqc__uia = 0
        swwrh__byho = np.int32(rank - 1)
        pjwz__prgha = np.int32(rank + 1)
        fdfi__xrxch = 0
        tubs__ortaz = len(in_arr)
        ofv__ktcf = 1
    dzwy__osj = np.int32(bodo.hiframes.rolling.comm_border_tag)
    ukuwd__zamux = np.empty(1, dtype=np.bool_)
    tkr__teaib = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    xjsuc__zfib = np.empty(1, dtype=np.bool_)
    cespb__qrkhf = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    faflv__dij = False
    fbm__vki = null_value
    for i in range(fdfi__xrxch, tubs__ortaz, ofv__ktcf):
        if not isna(in_arr, i):
            faflv__dij = True
            fbm__vki = in_arr[i]
            break
    if rank != cmctc__oic:
        yoa__tqy = bodo.libs.distributed_api.irecv(ukuwd__zamux, 1,
            pjwz__prgha, dzwy__osj, True)
        bodo.libs.distributed_api.wait(yoa__tqy, True)
        zvrrt__knl = bodo.libs.distributed_api.irecv(tkr__teaib, 1,
            pjwz__prgha, dzwy__osj, True)
        bodo.libs.distributed_api.wait(zvrrt__knl, True)
        yedq__hjo = ukuwd__zamux[0]
        mqpeb__spk = tkr__teaib[0]
    else:
        yedq__hjo = False
        mqpeb__spk = null_value
    if faflv__dij:
        xjsuc__zfib[0] = faflv__dij
        cespb__qrkhf[0] = fbm__vki
    else:
        xjsuc__zfib[0] = yedq__hjo
        cespb__qrkhf[0] = mqpeb__spk
    if rank != lgqc__uia:
        nwjt__kupoy = bodo.libs.distributed_api.isend(xjsuc__zfib, 1,
            swwrh__byho, dzwy__osj, True)
        dizab__xio = bodo.libs.distributed_api.isend(cespb__qrkhf, 1,
            swwrh__byho, dzwy__osj, True)
    return yedq__hjo, mqpeb__spk


@overload(np.sort, inline='always', no_unliteral=True)
def np_sort(A, axis=-1, kind=None, order=None):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    rzsoa__lyet = {'axis': axis, 'kind': kind, 'order': order}
    vsv__aizie = {'axis': -1, 'kind': None, 'order': None}
    check_unsupported_args('np.sort', rzsoa__lyet, vsv__aizie, 'numpy')

    def impl(A, axis=-1, kind=None, order=None):
        return pd.Series(A).sort_values().values
    return impl


def repeat_kernel(A, repeats):
    return A


@overload(repeat_kernel, no_unliteral=True)
def repeat_kernel_overload(A, repeats):
    nkbu__jyeqa = A
    if isinstance(repeats, types.Integer):

        def impl_int(A, repeats):
            soekb__gyfwe = len(A)
            kcxqi__hepb = bodo.utils.utils.alloc_type(soekb__gyfwe *
                repeats, nkbu__jyeqa, (-1,))
            for i in range(soekb__gyfwe):
                qxo__oqrq = i * repeats
                if bodo.libs.array_kernels.isna(A, i):
                    for vetct__pnbxm in range(repeats):
                        bodo.libs.array_kernels.setna(kcxqi__hepb, 
                            qxo__oqrq + vetct__pnbxm)
                else:
                    kcxqi__hepb[qxo__oqrq:qxo__oqrq + repeats] = A[i]
            return kcxqi__hepb
        return impl_int

    def impl_arr(A, repeats):
        soekb__gyfwe = len(A)
        kcxqi__hepb = bodo.utils.utils.alloc_type(repeats.sum(),
            nkbu__jyeqa, (-1,))
        qxo__oqrq = 0
        for i in range(soekb__gyfwe):
            zvoi__elstt = repeats[i]
            if bodo.libs.array_kernels.isna(A, i):
                for vetct__pnbxm in range(zvoi__elstt):
                    bodo.libs.array_kernels.setna(kcxqi__hepb, qxo__oqrq +
                        vetct__pnbxm)
            else:
                kcxqi__hepb[qxo__oqrq:qxo__oqrq + zvoi__elstt] = A[i]
            qxo__oqrq += zvoi__elstt
        return kcxqi__hepb
    return impl_arr


@overload(np.repeat, inline='always', no_unliteral=True)
def np_repeat(A, repeats):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    if not isinstance(repeats, types.Integer):
        raise BodoError(
            'Only integer type supported for repeats in np.repeat()')

    def impl(A, repeats):
        return bodo.libs.array_kernels.repeat_kernel(A, repeats)
    return impl


@overload(np.unique, inline='always', no_unliteral=True)
def np_unique(A):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return

    def impl(A):
        rhfle__kcwfg = bodo.libs.array_kernels.unique(A)
        return bodo.allgatherv(rhfle__kcwfg, False)
    return impl


@overload(np.union1d, inline='always', no_unliteral=True)
def overload_union1d(A1, A2):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.union1d()')

    def impl(A1, A2):
        kvcb__lsvr = bodo.libs.array_kernels.concat([A1, A2])
        omha__rhzvu = bodo.libs.array_kernels.unique(kvcb__lsvr)
        return pd.Series(omha__rhzvu).sort_values().values
    return impl


@overload(np.intersect1d, inline='always', no_unliteral=True)
def overload_intersect1d(A1, A2, assume_unique=False, return_indices=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    rzsoa__lyet = {'assume_unique': assume_unique, 'return_indices':
        return_indices}
    vsv__aizie = {'assume_unique': False, 'return_indices': False}
    check_unsupported_args('np.intersect1d', rzsoa__lyet, vsv__aizie, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.intersect1d()'
            )
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.intersect1d()')

    def impl(A1, A2, assume_unique=False, return_indices=False):
        vwra__iky = bodo.libs.array_kernels.unique(A1)
        bao__iaz = bodo.libs.array_kernels.unique(A2)
        kvcb__lsvr = bodo.libs.array_kernels.concat([vwra__iky, bao__iaz])
        yzc__fdgko = pd.Series(kvcb__lsvr).sort_values().values
        return slice_array_intersect1d(yzc__fdgko)
    return impl


@register_jitable
def slice_array_intersect1d(arr):
    enpgr__awtlx = arr[1:] == arr[:-1]
    return arr[:-1][enpgr__awtlx]


@overload(np.setdiff1d, inline='always', no_unliteral=True)
def overload_setdiff1d(A1, A2, assume_unique=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    rzsoa__lyet = {'assume_unique': assume_unique}
    vsv__aizie = {'assume_unique': False}
    check_unsupported_args('np.setdiff1d', rzsoa__lyet, vsv__aizie, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.setdiff1d()')
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.setdiff1d()')

    def impl(A1, A2, assume_unique=False):
        vwra__iky = bodo.libs.array_kernels.unique(A1)
        bao__iaz = bodo.libs.array_kernels.unique(A2)
        enpgr__awtlx = calculate_mask_setdiff1d(vwra__iky, bao__iaz)
        return pd.Series(vwra__iky[enpgr__awtlx]).sort_values().values
    return impl


@register_jitable
def calculate_mask_setdiff1d(A1, A2):
    enpgr__awtlx = np.ones(len(A1), np.bool_)
    for i in range(len(A2)):
        enpgr__awtlx &= A1 != A2[i]
    return enpgr__awtlx


@overload(np.linspace, inline='always', no_unliteral=True)
def np_linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=
    None, axis=0):
    rzsoa__lyet = {'retstep': retstep, 'axis': axis}
    vsv__aizie = {'retstep': False, 'axis': 0}
    check_unsupported_args('np.linspace', rzsoa__lyet, vsv__aizie, 'numpy')
    ovhi__yzcjy = False
    if is_overload_none(dtype):
        nkbu__jyeqa = np.promote_types(np.promote_types(numba.np.
            numpy_support.as_dtype(start), numba.np.numpy_support.as_dtype(
            stop)), numba.np.numpy_support.as_dtype(types.float64)).type
    else:
        if isinstance(dtype.dtype, types.Integer):
            ovhi__yzcjy = True
        nkbu__jyeqa = numba.np.numpy_support.as_dtype(dtype).type
    if ovhi__yzcjy:

        def impl_int(start, stop, num=50, endpoint=True, retstep=False,
            dtype=None, axis=0):
            avq__dqvx = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            kcxqi__hepb = np.empty(num, nkbu__jyeqa)
            for i in numba.parfors.parfor.internal_prange(num):
                kcxqi__hepb[i] = nkbu__jyeqa(np.floor(start + i * avq__dqvx))
            return kcxqi__hepb
        return impl_int
    else:

        def impl(start, stop, num=50, endpoint=True, retstep=False, dtype=
            None, axis=0):
            avq__dqvx = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            kcxqi__hepb = np.empty(num, nkbu__jyeqa)
            for i in numba.parfors.parfor.internal_prange(num):
                kcxqi__hepb[i] = nkbu__jyeqa(start + i * avq__dqvx)
            return kcxqi__hepb
        return impl


def np_linspace_get_stepsize(start, stop, num, endpoint):
    return 0


@overload(np_linspace_get_stepsize, no_unliteral=True)
def overload_np_linspace_get_stepsize(start, stop, num, endpoint):

    def impl(start, stop, num, endpoint):
        if num < 0:
            raise ValueError('np.linspace() Num must be >= 0')
        if endpoint:
            num -= 1
        if num > 1:
            return (stop - start) / num
        return 0
    return impl


@overload(operator.contains, no_unliteral=True)
def arr_contains(A, val):
    if not (bodo.utils.utils.is_array_typ(A, False) and A.dtype == types.
        unliteral(val)):
        return

    def impl(A, val):
        numba.parfors.parfor.init_prange()
        kuma__wncl = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                kuma__wncl += A[i] == val
        return kuma__wncl > 0
    return impl


@overload(np.any, inline='always', no_unliteral=True)
def np_any(A, axis=None, out=None, keepdims=None):
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    rzsoa__lyet = {'axis': axis, 'out': out, 'keepdims': keepdims}
    vsv__aizie = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', rzsoa__lyet, vsv__aizie, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        kuma__wncl = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                kuma__wncl += int(bool(A[i]))
        return kuma__wncl > 0
    return impl


@overload(np.all, inline='always', no_unliteral=True)
def np_all(A, axis=None, out=None, keepdims=None):
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    rzsoa__lyet = {'axis': axis, 'out': out, 'keepdims': keepdims}
    vsv__aizie = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', rzsoa__lyet, vsv__aizie, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        kuma__wncl = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                kuma__wncl += int(bool(A[i]))
        return kuma__wncl == n
    return impl


@overload(np.cbrt, inline='always', no_unliteral=True)
def np_cbrt(A, out=None, where=True, casting='same_kind', order='K', dtype=
    None, subok=True):
    if not (isinstance(A, types.Number) or bodo.utils.utils.is_array_typ(A,
        False) and A.ndim == 1 and isinstance(A.dtype, types.Number)):
        return
    rzsoa__lyet = {'out': out, 'where': where, 'casting': casting, 'order':
        order, 'dtype': dtype, 'subok': subok}
    vsv__aizie = {'out': None, 'where': True, 'casting': 'same_kind',
        'order': 'K', 'dtype': None, 'subok': True}
    check_unsupported_args('np.cbrt', rzsoa__lyet, vsv__aizie, 'numpy')
    if bodo.utils.utils.is_array_typ(A, False):
        rdzxs__nstiu = np.promote_types(numba.np.numpy_support.as_dtype(A.
            dtype), numba.np.numpy_support.as_dtype(types.float32)).type

        def impl_arr(A, out=None, where=True, casting='same_kind', order=
            'K', dtype=None, subok=True):
            numba.parfors.parfor.init_prange()
            n = len(A)
            kcxqi__hepb = np.empty(n, rdzxs__nstiu)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(kcxqi__hepb, i)
                    continue
                kcxqi__hepb[i] = np_cbrt_scalar(A[i], rdzxs__nstiu)
            return kcxqi__hepb
        return impl_arr
    rdzxs__nstiu = np.promote_types(numba.np.numpy_support.as_dtype(A),
        numba.np.numpy_support.as_dtype(types.float32)).type

    def impl_scalar(A, out=None, where=True, casting='same_kind', order='K',
        dtype=None, subok=True):
        return np_cbrt_scalar(A, rdzxs__nstiu)
    return impl_scalar


@register_jitable
def np_cbrt_scalar(x, float_dtype):
    if np.isnan(x):
        return np.nan
    vusrt__zeinr = x < 0
    if vusrt__zeinr:
        x = -x
    res = np.power(float_dtype(x), 1.0 / 3.0)
    if vusrt__zeinr:
        return -res
    return res


@overload(np.hstack, no_unliteral=True)
def np_hstack(tup):
    snqui__eqdn = isinstance(tup, (types.BaseTuple, types.List))
    uwf__yflpm = isinstance(tup, (bodo.SeriesType, bodo.hiframes.
        pd_series_ext.HeterogeneousSeriesType)) and isinstance(tup.data, (
        types.BaseTuple, types.List, bodo.NullableTupleType))
    if isinstance(tup, types.BaseTuple):
        for mrz__pygx in tup.types:
            snqui__eqdn = snqui__eqdn and bodo.utils.utils.is_array_typ(
                mrz__pygx, False)
    elif isinstance(tup, types.List):
        snqui__eqdn = bodo.utils.utils.is_array_typ(tup.dtype, False)
    elif uwf__yflpm:
        fqma__gair = tup.data.tuple_typ if isinstance(tup.data, bodo.
            NullableTupleType) else tup.data
        for mrz__pygx in fqma__gair.types:
            uwf__yflpm = uwf__yflpm and bodo.utils.utils.is_array_typ(mrz__pygx
                , False)
    if not (snqui__eqdn or uwf__yflpm):
        return
    if uwf__yflpm:

        def impl_series(tup):
            arr_tup = bodo.hiframes.pd_series_ext.get_series_data(tup)
            return bodo.libs.array_kernels.concat(arr_tup)
        return impl_series

    def impl(tup):
        return bodo.libs.array_kernels.concat(tup)
    return impl


@overload(np.random.multivariate_normal, inline='always', no_unliteral=True)
def np_random_multivariate_normal(mean, cov, size=None, check_valid='warn',
    tol=1e-08):
    rzsoa__lyet = {'check_valid': check_valid, 'tol': tol}
    vsv__aizie = {'check_valid': 'warn', 'tol': 1e-08}
    check_unsupported_args('np.random.multivariate_normal', rzsoa__lyet,
        vsv__aizie, 'numpy')
    if not isinstance(size, types.Integer):
        raise BodoError(
            'np.random.multivariate_normal() size argument is required and must be an integer'
            )
    if not (bodo.utils.utils.is_array_typ(mean, False) and mean.ndim == 1):
        raise BodoError(
            'np.random.multivariate_normal() mean must be a 1 dimensional numpy array'
            )
    if not (bodo.utils.utils.is_array_typ(cov, False) and cov.ndim == 2):
        raise BodoError(
            'np.random.multivariate_normal() cov must be a 2 dimensional square, numpy array'
            )

    def impl(mean, cov, size=None, check_valid='warn', tol=1e-08):
        _validate_multivar_norm(cov)
        qzh__xjhuw = mean.shape[0]
        andn__yifi = size, qzh__xjhuw
        dsp__gkynj = np.random.standard_normal(andn__yifi)
        cov = cov.astype(np.float64)
        wnvsd__xjzs, s, mhc__lwjh = np.linalg.svd(cov)
        res = np.dot(dsp__gkynj, np.sqrt(s).reshape(qzh__xjhuw, 1) * mhc__lwjh)
        ttca__kybb = res + mean
        return ttca__kybb
    return impl


def _validate_multivar_norm(cov):
    return


@overload(_validate_multivar_norm, no_unliteral=True)
def _overload_validate_multivar_norm(cov):

    def impl(cov):
        if cov.shape[0] != cov.shape[1]:
            raise ValueError(
                'np.random.multivariate_normal() cov must be a 2 dimensional square, numpy array'
                )
    return impl


def _nan_argmin(arr):
    return


@overload(_nan_argmin, no_unliteral=True)
def _overload_nan_argmin(arr):
    if isinstance(arr, IntegerArrayType) or arr in [boolean_array,
        datetime_date_array_type] or arr.dtype == bodo.timedelta64ns:

        def impl_bodo_arr(arr):
            numba.parfors.parfor.init_prange()
            gjgq__ggq = bodo.hiframes.series_kernels._get_type_max_value(arr)
            hzbve__anyl = typing.builtins.IndexValue(-1, gjgq__ggq)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                dvgxa__olee = typing.builtins.IndexValue(i, arr[i])
                hzbve__anyl = min(hzbve__anyl, dvgxa__olee)
            return hzbve__anyl.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        ydtxf__lrtwg = (bodo.hiframes.pd_categorical_ext.
            get_categories_int_type(arr.dtype))

        def impl_cat_arr(arr):
            fcv__lkai = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            gjgq__ggq = ydtxf__lrtwg(len(arr.dtype.categories) + 1)
            hzbve__anyl = typing.builtins.IndexValue(-1, gjgq__ggq)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                dvgxa__olee = typing.builtins.IndexValue(i, fcv__lkai[i])
                hzbve__anyl = min(hzbve__anyl, dvgxa__olee)
            return hzbve__anyl.index
        return impl_cat_arr
    return lambda arr: arr.argmin()


def _nan_argmax(arr):
    return


@overload(_nan_argmax, no_unliteral=True)
def _overload_nan_argmax(arr):
    if isinstance(arr, IntegerArrayType) or arr in [boolean_array,
        datetime_date_array_type] or arr.dtype == bodo.timedelta64ns:

        def impl_bodo_arr(arr):
            n = len(arr)
            numba.parfors.parfor.init_prange()
            gjgq__ggq = bodo.hiframes.series_kernels._get_type_min_value(arr)
            hzbve__anyl = typing.builtins.IndexValue(-1, gjgq__ggq)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                dvgxa__olee = typing.builtins.IndexValue(i, arr[i])
                hzbve__anyl = max(hzbve__anyl, dvgxa__olee)
            return hzbve__anyl.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        ydtxf__lrtwg = (bodo.hiframes.pd_categorical_ext.
            get_categories_int_type(arr.dtype))

        def impl_cat_arr(arr):
            n = len(arr)
            fcv__lkai = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            gjgq__ggq = ydtxf__lrtwg(-1)
            hzbve__anyl = typing.builtins.IndexValue(-1, gjgq__ggq)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                dvgxa__olee = typing.builtins.IndexValue(i, fcv__lkai[i])
                hzbve__anyl = max(hzbve__anyl, dvgxa__olee)
            return hzbve__anyl.index
        return impl_cat_arr
    return lambda arr: arr.argmax()


@overload_attribute(types.Array, 'nbytes', inline='always')
def overload_dataframe_index(A):
    return lambda A: A.size * bodo.io.np_io.get_dtype_size(A.dtype)
