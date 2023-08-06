import atexit
import datetime
import operator
import sys
import time
import warnings
from collections import defaultdict
from decimal import Decimal
from enum import Enum
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from mpi4py import MPI
from numba.core import cgutils, ir_utils, types
from numba.core.typing import signature
from numba.core.typing.builtins import IndexValueType
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, models, overload, register_jitable, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.libs import hdist
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, np_offset_type, offset_type
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType, set_bit_to_arr
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import convert_len_arr_to_offset, get_bit_bitmap, get_data_ptr, get_null_bitmap_ptr, get_offset_ptr, num_total_chars, pre_alloc_string_array, set_bit_to, string_array_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoError, BodoWarning, is_overload_false, is_overload_none, raise_bodo_error
from bodo.utils.utils import CTypeEnum, check_and_propagate_cpp_exception, empty_like_type, numba_to_c_type, tuple_to_scalar
ll.add_symbol('dist_get_time', hdist.dist_get_time)
ll.add_symbol('get_time', hdist.get_time)
ll.add_symbol('dist_reduce', hdist.dist_reduce)
ll.add_symbol('dist_arr_reduce', hdist.dist_arr_reduce)
ll.add_symbol('dist_exscan', hdist.dist_exscan)
ll.add_symbol('dist_irecv', hdist.dist_irecv)
ll.add_symbol('dist_isend', hdist.dist_isend)
ll.add_symbol('dist_wait', hdist.dist_wait)
ll.add_symbol('dist_get_item_pointer', hdist.dist_get_item_pointer)
ll.add_symbol('get_dummy_ptr', hdist.get_dummy_ptr)
ll.add_symbol('allgather', hdist.allgather)
ll.add_symbol('comm_req_alloc', hdist.comm_req_alloc)
ll.add_symbol('comm_req_dealloc', hdist.comm_req_dealloc)
ll.add_symbol('req_array_setitem', hdist.req_array_setitem)
ll.add_symbol('dist_waitall', hdist.dist_waitall)
ll.add_symbol('oneD_reshape_shuffle', hdist.oneD_reshape_shuffle)
ll.add_symbol('permutation_int', hdist.permutation_int)
ll.add_symbol('permutation_array_index', hdist.permutation_array_index)
ll.add_symbol('c_get_rank', hdist.dist_get_rank)
ll.add_symbol('c_get_size', hdist.dist_get_size)
ll.add_symbol('c_barrier', hdist.barrier)
ll.add_symbol('c_alltoall', hdist.c_alltoall)
ll.add_symbol('c_gather_scalar', hdist.c_gather_scalar)
ll.add_symbol('c_gatherv', hdist.c_gatherv)
ll.add_symbol('c_scatterv', hdist.c_scatterv)
ll.add_symbol('c_allgatherv', hdist.c_allgatherv)
ll.add_symbol('c_bcast', hdist.c_bcast)
ll.add_symbol('c_recv', hdist.dist_recv)
ll.add_symbol('c_send', hdist.dist_send)
mpi_req_numba_type = getattr(types, 'int' + str(8 * hdist.mpi_req_num_bytes))
MPI_ROOT = 0
ANY_SOURCE = np.int32(hdist.ANY_SOURCE)


class Reduce_Type(Enum):
    Sum = 0
    Prod = 1
    Min = 2
    Max = 3
    Argmin = 4
    Argmax = 5
    Or = 6
    Concat = 7
    No_Op = 8


_get_rank = types.ExternalFunction('c_get_rank', types.int32())
_get_size = types.ExternalFunction('c_get_size', types.int32())
_barrier = types.ExternalFunction('c_barrier', types.int32())


@numba.njit
def get_rank():
    return _get_rank()


@numba.njit
def get_size():
    return _get_size()


@numba.njit
def barrier():
    _barrier()


_get_time = types.ExternalFunction('get_time', types.float64())
dist_time = types.ExternalFunction('dist_get_time', types.float64())


@overload(time.time, no_unliteral=True)
def overload_time_time():
    return lambda : _get_time()


@numba.generated_jit(nopython=True)
def get_type_enum(arr):
    arr = arr.instance_type if isinstance(arr, types.TypeRef) else arr
    dtype = arr.dtype
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):
        dtype = bodo.hiframes.pd_categorical_ext.get_categories_int_type(dtype)
    typ_val = numba_to_c_type(dtype)
    return lambda arr: np.int32(typ_val)


INT_MAX = np.iinfo(np.int32).max
_send = types.ExternalFunction('c_send', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def send(val, rank, tag):
    send_arr = np.full(1, val)
    sbio__ltnv = get_type_enum(send_arr)
    _send(send_arr.ctypes, 1, sbio__ltnv, rank, tag)


_recv = types.ExternalFunction('c_recv', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def recv(dtype, rank, tag):
    recv_arr = np.empty(1, dtype)
    sbio__ltnv = get_type_enum(recv_arr)
    _recv(recv_arr.ctypes, 1, sbio__ltnv, rank, tag)
    return recv_arr[0]


_isend = types.ExternalFunction('dist_isend', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def isend(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            sbio__ltnv = get_type_enum(arr)
            return _isend(arr.ctypes, size, sbio__ltnv, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        sbio__ltnv = np.int32(numba_to_c_type(arr.dtype))
        sbzyt__tuf = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            hox__gwou = size + 7 >> 3
            rej__mmz = _isend(arr._data.ctypes, size, sbio__ltnv, pe, tag, cond
                )
            kscf__ryw = _isend(arr._null_bitmap.ctypes, hox__gwou,
                sbzyt__tuf, pe, tag, cond)
            return rej__mmz, kscf__ryw
        return impl_nullable
    if arr in [binary_array_type, string_array_type]:
        dlzr__xyit = np.int32(numba_to_c_type(offset_type))
        sbzyt__tuf = np.int32(numba_to_c_type(types.uint8))

        def impl_str_arr(arr, size, pe, tag, cond=True):
            lrbb__pny = np.int64(bodo.libs.str_arr_ext.num_total_chars(arr))
            send(lrbb__pny, pe, tag - 1)
            hox__gwou = size + 7 >> 3
            _send(bodo.libs.str_arr_ext.get_offset_ptr(arr), size + 1,
                dlzr__xyit, pe, tag)
            _send(bodo.libs.str_arr_ext.get_data_ptr(arr), lrbb__pny,
                sbzyt__tuf, pe, tag)
            _send(bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr), hox__gwou,
                sbzyt__tuf, pe, tag)
            return None
        return impl_str_arr
    typ_enum = numba_to_c_type(types.uint8)

    def impl_voidptr(arr, size, pe, tag, cond=True):
        return _isend(arr, size, typ_enum, pe, tag, cond)
    return impl_voidptr


_irecv = types.ExternalFunction('dist_irecv', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def irecv(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            sbio__ltnv = get_type_enum(arr)
            return _irecv(arr.ctypes, size, sbio__ltnv, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        sbio__ltnv = np.int32(numba_to_c_type(arr.dtype))
        sbzyt__tuf = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            hox__gwou = size + 7 >> 3
            rej__mmz = _irecv(arr._data.ctypes, size, sbio__ltnv, pe, tag, cond
                )
            kscf__ryw = _irecv(arr._null_bitmap.ctypes, hox__gwou,
                sbzyt__tuf, pe, tag, cond)
            return rej__mmz, kscf__ryw
        return impl_nullable
    if arr in [binary_array_type, string_array_type]:
        dlzr__xyit = np.int32(numba_to_c_type(offset_type))
        sbzyt__tuf = np.int32(numba_to_c_type(types.uint8))
        if arr == binary_array_type:
            tqmih__umu = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            tqmih__umu = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        qyoq__ftmxe = f"""def impl(arr, size, pe, tag, cond=True):
            # recv the number of string characters and resize buffer to proper size
            n_chars = bodo.libs.distributed_api.recv(np.int64, pe, tag - 1)
            new_arr = {tqmih__umu}(size, n_chars)
            bodo.libs.str_arr_ext.move_str_binary_arr_payload(arr, new_arr)

            n_bytes = (size + 7) >> 3
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_offset_ptr(arr),
                size + 1,
                offset_typ_enum,
                pe,
                tag,
            )
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_data_ptr(arr), n_chars, char_typ_enum, pe, tag
            )
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr),
                n_bytes,
                char_typ_enum,
                pe,
                tag,
            )
            return None"""
        jhgbi__fmi = dict()
        exec(qyoq__ftmxe, {'bodo': bodo, 'np': np, 'offset_typ_enum':
            dlzr__xyit, 'char_typ_enum': sbzyt__tuf}, jhgbi__fmi)
        impl = jhgbi__fmi['impl']
        return impl
    raise BodoError(f'irecv(): array type {arr} not supported yet')


_alltoall = types.ExternalFunction('c_alltoall', types.void(types.voidptr,
    types.voidptr, types.int32, types.int32))


@numba.njit
def alltoall(send_arr, recv_arr, count):
    assert count < INT_MAX
    sbio__ltnv = get_type_enum(send_arr)
    _alltoall(send_arr.ctypes, recv_arr.ctypes, np.int32(count), sbio__ltnv)


@numba.generated_jit(nopython=True)
def gather_scalar(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    data = types.unliteral(data)
    typ_val = numba_to_c_type(data)
    dtype = data

    def gather_scalar_impl(data, allgather=False, warn_if_rep=True, root=
        MPI_ROOT):
        n_pes = bodo.libs.distributed_api.get_size()
        rank = bodo.libs.distributed_api.get_rank()
        send = np.full(1, data, dtype)
        xctrh__dzrd = n_pes if rank == root or allgather else 0
        vgwbn__mxk = np.empty(xctrh__dzrd, dtype)
        c_gather_scalar(send.ctypes, vgwbn__mxk.ctypes, np.int32(typ_val),
            allgather, np.int32(root))
        return vgwbn__mxk
    return gather_scalar_impl


c_gather_scalar = types.ExternalFunction('c_gather_scalar', types.void(
    types.voidptr, types.voidptr, types.int32, types.bool_, types.int32))
c_gatherv = types.ExternalFunction('c_gatherv', types.void(types.voidptr,
    types.int32, types.voidptr, types.voidptr, types.voidptr, types.int32,
    types.bool_, types.int32))
c_scatterv = types.ExternalFunction('c_scatterv', types.void(types.voidptr,
    types.voidptr, types.voidptr, types.voidptr, types.int32, types.int32))


@intrinsic
def value_to_ptr(typingctx, val_tp=None):

    def codegen(context, builder, sig, args):
        qxor__ynjrb = cgutils.alloca_once(builder, args[0].type)
        builder.store(args[0], qxor__ynjrb)
        return builder.bitcast(qxor__ynjrb, lir.IntType(8).as_pointer())
    return types.voidptr(val_tp), codegen


@intrinsic
def load_val_ptr(typingctx, ptr_tp, val_tp=None):

    def codegen(context, builder, sig, args):
        qxor__ynjrb = builder.bitcast(args[0], args[1].type.as_pointer())
        return builder.load(qxor__ynjrb)
    return val_tp(ptr_tp, val_tp), codegen


_dist_reduce = types.ExternalFunction('dist_reduce', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))
_dist_arr_reduce = types.ExternalFunction('dist_arr_reduce', types.void(
    types.voidptr, types.int64, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_reduce(value, reduce_op):
    if isinstance(value, types.Array):
        typ_enum = np.int32(numba_to_c_type(value.dtype))

        def impl_arr(value, reduce_op):
            A = np.ascontiguousarray(value)
            _dist_arr_reduce(A.ctypes, A.size, reduce_op, typ_enum)
            return A
        return impl_arr
    mbujx__thh = types.unliteral(value)
    if isinstance(mbujx__thh, IndexValueType):
        mbujx__thh = mbujx__thh.val_typ
        fbuvt__dvna = [types.bool_, types.uint8, types.int8, types.uint16,
            types.int16, types.uint32, types.int32, types.float32, types.
            float64]
        if not sys.platform.startswith('win'):
            fbuvt__dvna.append(types.int64)
            fbuvt__dvna.append(bodo.datetime64ns)
            fbuvt__dvna.append(bodo.timedelta64ns)
            fbuvt__dvna.append(bodo.datetime_date_type)
        if mbujx__thh not in fbuvt__dvna:
            raise BodoError('argmin/argmax not supported for type {}'.
                format(mbujx__thh))
    typ_enum = np.int32(numba_to_c_type(mbujx__thh))

    def impl(value, reduce_op):
        bztv__ggx = value_to_ptr(value)
        nxx__vztzq = value_to_ptr(value)
        _dist_reduce(bztv__ggx, nxx__vztzq, reduce_op, typ_enum)
        return load_val_ptr(nxx__vztzq, value)
    return impl


_dist_exscan = types.ExternalFunction('dist_exscan', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_exscan(value, reduce_op):
    mbujx__thh = types.unliteral(value)
    typ_enum = np.int32(numba_to_c_type(mbujx__thh))
    piqw__rzyu = mbujx__thh(0)

    def impl(value, reduce_op):
        bztv__ggx = value_to_ptr(value)
        nxx__vztzq = value_to_ptr(piqw__rzyu)
        _dist_exscan(bztv__ggx, nxx__vztzq, reduce_op, typ_enum)
        return load_val_ptr(nxx__vztzq, value)
    return impl


@numba.njit
def get_bit(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@numba.njit
def copy_gathered_null_bytes(null_bitmap_ptr, tmp_null_bytes,
    recv_counts_nulls, recv_counts):
    glmxp__unl = 0
    uqlkv__umevo = 0
    for i in range(len(recv_counts)):
        egh__hdj = recv_counts[i]
        hox__gwou = recv_counts_nulls[i]
        dyy__sxl = tmp_null_bytes[glmxp__unl:glmxp__unl + hox__gwou]
        for lau__njwbh in range(egh__hdj):
            set_bit_to(null_bitmap_ptr, uqlkv__umevo, get_bit(dyy__sxl,
                lau__njwbh))
            uqlkv__umevo += 1
        glmxp__unl += hox__gwou


@numba.generated_jit(nopython=True)
def gatherv(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    from bodo.libs.csr_matrix_ext import CSRMatrixType
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.gatherv()')
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            engfp__kuz = bodo.gatherv(data.codes, allgather, root=root)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                engfp__kuz, data.dtype)
        return impl_cat
    if isinstance(data, types.Array):
        typ_val = numba_to_c_type(data.dtype)

        def gatherv_impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            data = np.ascontiguousarray(data)
            rank = bodo.libs.distributed_api.get_rank()
            hcob__xzh = data.size
            recv_counts = gather_scalar(np.int32(hcob__xzh), allgather,
                root=root)
            ptvp__svfbw = recv_counts.sum()
            ufdng__wyy = empty_like_type(ptvp__svfbw, data)
            nfapy__rnp = np.empty(1, np.int32)
            if rank == root or allgather:
                nfapy__rnp = bodo.ir.join.calc_disp(recv_counts)
            c_gatherv(data.ctypes, np.int32(hcob__xzh), ufdng__wyy.ctypes,
                recv_counts.ctypes, nfapy__rnp.ctypes, np.int32(typ_val),
                allgather, np.int32(root))
            return ufdng__wyy.reshape((-1,) + data.shape[1:])
        return gatherv_impl
    if data == string_array_type:

        def gatherv_str_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            ufdng__wyy = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.str_arr_ext.init_str_arr(ufdng__wyy)
        return gatherv_str_arr_impl
    if data == binary_array_type:

        def gatherv_binary_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            ufdng__wyy = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(ufdng__wyy)
        return gatherv_binary_arr_impl
    if data == datetime_timedelta_array_type:
        typ_val = numba_to_c_type(types.int64)
        sbzyt__tuf = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            hcob__xzh = len(data)
            hox__gwou = hcob__xzh + 7 >> 3
            recv_counts = gather_scalar(np.int32(hcob__xzh), allgather,
                root=root)
            ptvp__svfbw = recv_counts.sum()
            ufdng__wyy = empty_like_type(ptvp__svfbw, data)
            nfapy__rnp = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            egibb__pjlwi = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                nfapy__rnp = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                egibb__pjlwi = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._days_data.ctypes, np.int32(hcob__xzh),
                ufdng__wyy._days_data.ctypes, recv_counts.ctypes,
                nfapy__rnp.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._seconds_data.ctypes, np.int32(hcob__xzh),
                ufdng__wyy._seconds_data.ctypes, recv_counts.ctypes,
                nfapy__rnp.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._microseconds_data.ctypes, np.int32(hcob__xzh),
                ufdng__wyy._microseconds_data.ctypes, recv_counts.ctypes,
                nfapy__rnp.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._null_bitmap.ctypes, np.int32(hox__gwou),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes,
                egibb__pjlwi.ctypes, sbzyt__tuf, allgather, np.int32(root))
            copy_gathered_null_bytes(ufdng__wyy._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return ufdng__wyy
        return gatherv_impl_int_arr
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        typ_val = numba_to_c_type(data.dtype)
        sbzyt__tuf = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            hcob__xzh = len(data)
            hox__gwou = hcob__xzh + 7 >> 3
            recv_counts = gather_scalar(np.int32(hcob__xzh), allgather,
                root=root)
            ptvp__svfbw = recv_counts.sum()
            ufdng__wyy = empty_like_type(ptvp__svfbw, data)
            nfapy__rnp = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            egibb__pjlwi = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                nfapy__rnp = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                egibb__pjlwi = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._data.ctypes, np.int32(hcob__xzh), ufdng__wyy.
                _data.ctypes, recv_counts.ctypes, nfapy__rnp.ctypes, np.
                int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(hox__gwou),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes,
                egibb__pjlwi.ctypes, sbzyt__tuf, allgather, np.int32(root))
            copy_gathered_null_bytes(ufdng__wyy._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return ufdng__wyy
        return gatherv_impl_int_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, allgather=False, warn_if_rep=True, root
            =MPI_ROOT):
            wpo__maetb = bodo.gatherv(data._left, allgather, warn_if_rep, root)
            qtfp__apje = bodo.gatherv(data._right, allgather, warn_if_rep, root
                )
            return bodo.libs.interval_arr_ext.init_interval_array(wpo__maetb,
                qtfp__apje)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            tjyx__aemmp = bodo.hiframes.pd_series_ext.get_series_name(data)
            out_arr = bodo.libs.distributed_api.gatherv(arr, allgather,
                warn_if_rep, root)
            rnp__spqtk = bodo.gatherv(index, allgather, warn_if_rep, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rnp__spqtk, tjyx__aemmp)
        return impl
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):
        lbp__dvv = np.iinfo(np.int64).max
        dxszy__jvgf = np.iinfo(np.int64).min

        def impl_range_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            start = data._start
            stop = data._stop
            if len(data) == 0:
                start = lbp__dvv
                stop = dxszy__jvgf
            start = bodo.libs.distributed_api.dist_reduce(start, np.int32(
                Reduce_Type.Min.value))
            stop = bodo.libs.distributed_api.dist_reduce(stop, np.int32(
                Reduce_Type.Max.value))
            total_len = bodo.libs.distributed_api.dist_reduce(len(data), np
                .int32(Reduce_Type.Sum.value))
            if start == lbp__dvv and stop == dxszy__jvgf:
                start = 0
                stop = 0
            qkugv__ogxbj = max(0, -(-(stop - start) // data._step))
            if qkugv__ogxbj < total_len:
                stop = start + data._step * total_len
            if bodo.get_rank() != root and not allgather:
                start = 0
                stop = 0
            return bodo.hiframes.pd_index_ext.init_range_index(start, stop,
                data._step, data._name)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        from bodo.hiframes.pd_index_ext import PeriodIndexType
        if isinstance(data, PeriodIndexType):
            jdga__ccra = data.freq

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.hiframes.pd_index_ext.init_period_index(arr,
                    data._name, jdga__ccra)
        else:

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.utils.conversion.index_from_array(arr, data._name)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            ufdng__wyy = bodo.gatherv(data._data, allgather, root=root)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(ufdng__wyy
                , data._names, data._name)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.table.TableType):
        iknki__sff = {'bodo': bodo, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like, 'init_table': bodo.hiframes.table.init_table}
        qyoq__ftmxe = (
            f'def impl_table(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):\n'
            )
        qyoq__ftmxe += '  T = data\n'
        qyoq__ftmxe += '  T2 = init_table(T)\n'
        for beclt__yfml in data.type_to_blk.values():
            iknki__sff[f'arr_inds_{beclt__yfml}'] = np.array(data.
                block_to_arr_ind[beclt__yfml], dtype=np.int64)
            qyoq__ftmxe += (
                f'  arr_list_{beclt__yfml} = get_table_block(T, {beclt__yfml})\n'
                )
            qyoq__ftmxe += f"""  out_arr_list_{beclt__yfml} = alloc_list_like(arr_list_{beclt__yfml})
"""
            qyoq__ftmxe += f'  for i in range(len(arr_list_{beclt__yfml})):\n'
            qyoq__ftmxe += (
                f'    arr_ind_{beclt__yfml} = arr_inds_{beclt__yfml}[i]\n')
            qyoq__ftmxe += f"""    ensure_column_unboxed(T, arr_list_{beclt__yfml}, i, arr_ind_{beclt__yfml})
"""
            qyoq__ftmxe += f"""    out_arr_{beclt__yfml} = bodo.gatherv(arr_list_{beclt__yfml}[i], allgather, warn_if_rep, root)
"""
            qyoq__ftmxe += (
                f'    out_arr_list_{beclt__yfml}[i] = out_arr_{beclt__yfml}\n')
            qyoq__ftmxe += f"""  T2 = set_table_block(T2, out_arr_list_{beclt__yfml}, {beclt__yfml})
"""
        qyoq__ftmxe += (
            f'  length = T._len if bodo.get_rank() == root or allgather else 0\n'
            )
        qyoq__ftmxe += f'  T2 = set_table_len(T2, length)\n'
        qyoq__ftmxe += f'  return T2\n'
        jhgbi__fmi = {}
        exec(qyoq__ftmxe, iknki__sff, jhgbi__fmi)
        flq__isjss = jhgbi__fmi['impl_table']
        return flq__isjss
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        omz__dnke = len(data.columns)
        if omz__dnke == 0:
            return (lambda data, allgather=False, warn_if_rep=True, root=
                MPI_ROOT: bodo.hiframes.pd_dataframe_ext.init_dataframe((),
                bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data), ()))
        rgopz__ulpm = ', '.join(f'g_data_{i}' for i in range(omz__dnke))
        esqem__tgjw = bodo.utils.transform.gen_const_tup(data.columns)
        qyoq__ftmxe = (
            'def impl_df(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        if data.is_table_format:
            from bodo.transforms.distributed_analysis import Distribution
            xjjn__ersp = bodo.hiframes.pd_dataframe_ext.DataFrameType(data.
                data, data.index, data.columns, Distribution.REP, True)
            iknki__sff = {'bodo': bodo, 'df_type': xjjn__ersp}
            rgopz__ulpm = 'T2'
            esqem__tgjw = 'df_type'
            qyoq__ftmxe += (
                '  T = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            qyoq__ftmxe += (
                '  T2 = bodo.gatherv(T, allgather, warn_if_rep, root)\n')
        else:
            iknki__sff = {'bodo': bodo}
            for i in range(omz__dnke):
                qyoq__ftmxe += (
                    """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                    .format(i, i))
                qyoq__ftmxe += (
                    """  g_data_{} = bodo.gatherv(data_{}, allgather, warn_if_rep, root)
"""
                    .format(i, i))
        qyoq__ftmxe += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        qyoq__ftmxe += (
            '  g_index = bodo.gatherv(index, allgather, warn_if_rep, root)\n')
        qyoq__ftmxe += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})
"""
            .format(rgopz__ulpm, esqem__tgjw))
        jhgbi__fmi = {}
        exec(qyoq__ftmxe, iknki__sff, jhgbi__fmi)
        yaf__vrds = jhgbi__fmi['impl_df']
        return yaf__vrds
    if isinstance(data, ArrayItemArrayType):
        xlgsr__sgsyi = np.int32(numba_to_c_type(types.int32))
        sbzyt__tuf = np.int32(numba_to_c_type(types.uint8))

        def gatherv_array_item_arr_impl(data, allgather=False, warn_if_rep=
            True, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            pqjl__pzn = bodo.libs.array_item_arr_ext.get_offsets(data)
            hmk__nedu = bodo.libs.array_item_arr_ext.get_data(data)
            rwyer__mosho = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            hcob__xzh = len(data)
            vomxs__cfs = np.empty(hcob__xzh, np.uint32)
            hox__gwou = hcob__xzh + 7 >> 3
            for i in range(hcob__xzh):
                vomxs__cfs[i] = pqjl__pzn[i + 1] - pqjl__pzn[i]
            recv_counts = gather_scalar(np.int32(hcob__xzh), allgather,
                root=root)
            ptvp__svfbw = recv_counts.sum()
            nfapy__rnp = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            egibb__pjlwi = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                nfapy__rnp = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for lff__fzbm in range(len(recv_counts)):
                    recv_counts_nulls[lff__fzbm] = recv_counts[lff__fzbm
                        ] + 7 >> 3
                egibb__pjlwi = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            arpz__roxsz = np.empty(ptvp__svfbw + 1, np.uint32)
            niccd__mwk = bodo.gatherv(hmk__nedu, allgather, warn_if_rep, root)
            msau__zgwv = np.empty(ptvp__svfbw + 7 >> 3, np.uint8)
            c_gatherv(vomxs__cfs.ctypes, np.int32(hcob__xzh), arpz__roxsz.
                ctypes, recv_counts.ctypes, nfapy__rnp.ctypes, xlgsr__sgsyi,
                allgather, np.int32(root))
            c_gatherv(rwyer__mosho.ctypes, np.int32(hox__gwou),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes,
                egibb__pjlwi.ctypes, sbzyt__tuf, allgather, np.int32(root))
            dummy_use(data)
            tym__qcfhh = np.empty(ptvp__svfbw + 1, np.uint64)
            convert_len_arr_to_offset(arpz__roxsz.ctypes, tym__qcfhh.ctypes,
                ptvp__svfbw)
            copy_gathered_null_bytes(msau__zgwv.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                ptvp__svfbw, niccd__mwk, tym__qcfhh, msau__zgwv)
            return out_arr
        return gatherv_array_item_arr_impl
    if isinstance(data, StructArrayType):
        ves__dua = data.names
        sbzyt__tuf = np.int32(numba_to_c_type(types.uint8))

        def impl_struct_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            obnvo__rswq = bodo.libs.struct_arr_ext.get_data(data)
            ohz__dommw = bodo.libs.struct_arr_ext.get_null_bitmap(data)
            cdg__riofz = bodo.gatherv(obnvo__rswq, allgather=allgather,
                root=root)
            rank = bodo.libs.distributed_api.get_rank()
            hcob__xzh = len(data)
            hox__gwou = hcob__xzh + 7 >> 3
            recv_counts = gather_scalar(np.int32(hcob__xzh), allgather,
                root=root)
            ptvp__svfbw = recv_counts.sum()
            rmfo__hgkxg = np.empty(ptvp__svfbw + 7 >> 3, np.uint8)
            recv_counts_nulls = np.empty(1, np.int32)
            egibb__pjlwi = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                egibb__pjlwi = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(ohz__dommw.ctypes, np.int32(hox__gwou),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes,
                egibb__pjlwi.ctypes, sbzyt__tuf, allgather, np.int32(root))
            copy_gathered_null_bytes(rmfo__hgkxg.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            return bodo.libs.struct_arr_ext.init_struct_arr(cdg__riofz,
                rmfo__hgkxg, ves__dua)
        return impl_struct_arr
    if data == binary_array_type:

        def impl_bin_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            ufdng__wyy = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(ufdng__wyy)
        return impl_bin_arr
    if isinstance(data, TupleArrayType):

        def impl_tuple_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            ufdng__wyy = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.tuple_arr_ext.init_tuple_arr(ufdng__wyy)
        return impl_tuple_arr
    if isinstance(data, MapArrayType):

        def impl_map_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            ufdng__wyy = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.map_arr_ext.init_map_arr(ufdng__wyy)
        return impl_map_arr
    if isinstance(data, CSRMatrixType):

        def impl_csr_matrix(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            ufdng__wyy = bodo.gatherv(data.data, allgather, warn_if_rep, root)
            sxlo__ajavx = bodo.gatherv(data.indices, allgather, warn_if_rep,
                root)
            wkkfw__ssq = bodo.gatherv(data.indptr, allgather, warn_if_rep, root
                )
            qhs__ufii = gather_scalar(data.shape[0], allgather, root=root)
            kxi__tvn = qhs__ufii.sum()
            omz__dnke = bodo.libs.distributed_api.dist_reduce(data.shape[1],
                np.int32(Reduce_Type.Max.value))
            vybs__fltvk = np.empty(kxi__tvn + 1, np.int64)
            sxlo__ajavx = sxlo__ajavx.astype(np.int64)
            vybs__fltvk[0] = 0
            uhcxe__wven = 1
            ebqte__atl = 0
            for kpj__mha in qhs__ufii:
                for tlk__ufjd in range(kpj__mha):
                    ltxl__hmlkc = wkkfw__ssq[ebqte__atl + 1] - wkkfw__ssq[
                        ebqte__atl]
                    vybs__fltvk[uhcxe__wven] = vybs__fltvk[uhcxe__wven - 1
                        ] + ltxl__hmlkc
                    uhcxe__wven += 1
                    ebqte__atl += 1
                ebqte__atl += 1
            return bodo.libs.csr_matrix_ext.init_csr_matrix(ufdng__wyy,
                sxlo__ajavx, vybs__fltvk, (kxi__tvn, omz__dnke))
        return impl_csr_matrix
    if isinstance(data, types.BaseTuple):
        qyoq__ftmxe = (
            'def impl_tuple(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        qyoq__ftmxe += '  return ({}{})\n'.format(', '.join(
            'bodo.gatherv(data[{}], allgather, warn_if_rep, root)'.format(i
            ) for i in range(len(data))), ',' if len(data) > 0 else '')
        jhgbi__fmi = {}
        exec(qyoq__ftmxe, {'bodo': bodo}, jhgbi__fmi)
        hfu__ear = jhgbi__fmi['impl_tuple']
        return hfu__ear
    if data is types.none:
        return (lambda data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT: None)
    raise BodoError('gatherv() not available for {}'.format(data))


@numba.generated_jit(nopython=True)
def rebalance(data, dests=None, random=False, random_seed=None, parallel=False
    ):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.rebalance()')
    qyoq__ftmxe = (
        'def impl(data, dests=None, random=False, random_seed=None, parallel=False):\n'
        )
    qyoq__ftmxe += '    if random:\n'
    qyoq__ftmxe += '        if random_seed is None:\n'
    qyoq__ftmxe += '            random = 1\n'
    qyoq__ftmxe += '        else:\n'
    qyoq__ftmxe += '            random = 2\n'
    qyoq__ftmxe += '    if random_seed is None:\n'
    qyoq__ftmxe += '        random_seed = -1\n'
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        uuucm__elkze = data
        omz__dnke = len(uuucm__elkze.columns)
        for i in range(omz__dnke):
            qyoq__ftmxe += f"""    data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
        qyoq__ftmxe += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data))
"""
        rgopz__ulpm = ', '.join(f'data_{i}' for i in range(omz__dnke))
        qyoq__ftmxe += ('    info_list_total = [{}, array_to_info(ind_arr)]\n'
            .format(', '.join('array_to_info(data_{})'.format(klch__zzype) for
            klch__zzype in range(omz__dnke))))
        qyoq__ftmxe += (
            '    table_total = arr_info_list_to_table(info_list_total)\n')
        qyoq__ftmxe += '    if dests is None:\n'
        qyoq__ftmxe += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        qyoq__ftmxe += '    else:\n'
        qyoq__ftmxe += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        for oced__yhhp in range(omz__dnke):
            qyoq__ftmxe += (
                """    out_arr_{0} = info_to_array(info_from_table(out_table, {0}), data_{0})
"""
                .format(oced__yhhp))
        qyoq__ftmxe += (
            """    out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)
"""
            .format(omz__dnke))
        qyoq__ftmxe += '    delete_table(out_table)\n'
        qyoq__ftmxe += '    if parallel:\n'
        qyoq__ftmxe += '        delete_table(table_total)\n'
        rgopz__ulpm = ', '.join('out_arr_{}'.format(i) for i in range(
            omz__dnke))
        esqem__tgjw = bodo.utils.transform.gen_const_tup(uuucm__elkze.columns)
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        qyoq__ftmxe += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), {}, {})\n'
            .format(rgopz__ulpm, index, esqem__tgjw))
    elif isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):
        qyoq__ftmxe += (
            '    data_0 = bodo.hiframes.pd_series_ext.get_series_data(data)\n')
        qyoq__ftmxe += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(data))
"""
        qyoq__ftmxe += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(data)\n')
        qyoq__ftmxe += """    table_total = arr_info_list_to_table([array_to_info(data_0), array_to_info(ind_arr)])
"""
        qyoq__ftmxe += '    if dests is None:\n'
        qyoq__ftmxe += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        qyoq__ftmxe += '    else:\n'
        qyoq__ftmxe += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        qyoq__ftmxe += (
            '    out_arr_0 = info_to_array(info_from_table(out_table, 0), data_0)\n'
            )
        qyoq__ftmxe += """    out_arr_index = info_to_array(info_from_table(out_table, 1), ind_arr)
"""
        qyoq__ftmxe += '    delete_table(out_table)\n'
        qyoq__ftmxe += '    if parallel:\n'
        qyoq__ftmxe += '        delete_table(table_total)\n'
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        qyoq__ftmxe += f"""    return bodo.hiframes.pd_series_ext.init_series(out_arr_0, {index}, name)
"""
    elif isinstance(data, types.Array):
        assert is_overload_false(random
            ), 'Call random_shuffle instead of rebalance'
        qyoq__ftmxe += '    if not parallel:\n'
        qyoq__ftmxe += '        return data\n'
        qyoq__ftmxe += """    dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        qyoq__ftmxe += '    if dests is None:\n'
        qyoq__ftmxe += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        qyoq__ftmxe += '    elif bodo.get_rank() not in dests:\n'
        qyoq__ftmxe += '        dim0_local_size = 0\n'
        qyoq__ftmxe += '    else:\n'
        qyoq__ftmxe += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, len(dests), dests.index(bodo.get_rank()))
"""
        qyoq__ftmxe += """    out = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        qyoq__ftmxe += """    bodo.libs.distributed_api.dist_oneD_reshape_shuffle(out, data, dim0_global_size, dests)
"""
        qyoq__ftmxe += '    return out\n'
    elif bodo.utils.utils.is_array_typ(data, False):
        qyoq__ftmxe += (
            '    table_total = arr_info_list_to_table([array_to_info(data)])\n'
            )
        qyoq__ftmxe += '    if dests is None:\n'
        qyoq__ftmxe += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        qyoq__ftmxe += '    else:\n'
        qyoq__ftmxe += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        qyoq__ftmxe += (
            '    out_arr = info_to_array(info_from_table(out_table, 0), data)\n'
            )
        qyoq__ftmxe += '    delete_table(out_table)\n'
        qyoq__ftmxe += '    if parallel:\n'
        qyoq__ftmxe += '        delete_table(table_total)\n'
        qyoq__ftmxe += '    return out_arr\n'
    else:
        raise BodoError(f'Type {data} not supported for bodo.rebalance')
    jhgbi__fmi = {}
    exec(qyoq__ftmxe, {'np': np, 'bodo': bodo, 'array_to_info': bodo.libs.
        array.array_to_info, 'shuffle_renormalization': bodo.libs.array.
        shuffle_renormalization, 'shuffle_renormalization_group': bodo.libs
        .array.shuffle_renormalization_group, 'arr_info_list_to_table':
        bodo.libs.array.arr_info_list_to_table, 'info_from_table': bodo.
        libs.array.info_from_table, 'info_to_array': bodo.libs.array.
        info_to_array, 'delete_table': bodo.libs.array.delete_table},
        jhgbi__fmi)
    impl = jhgbi__fmi['impl']
    return impl


@numba.generated_jit(nopython=True)
def random_shuffle(data, seed=None, dests=None, parallel=False):
    qyoq__ftmxe = 'def impl(data, seed=None, dests=None, parallel=False):\n'
    if isinstance(data, types.Array):
        if not is_overload_none(dests):
            raise BodoError('not supported')
        qyoq__ftmxe += '    if seed is None:\n'
        qyoq__ftmxe += """        seed = bodo.libs.distributed_api.bcast_scalar(np.random.randint(0, 2**31))
"""
        qyoq__ftmxe += '    np.random.seed(seed)\n'
        qyoq__ftmxe += '    if not parallel:\n'
        qyoq__ftmxe += '        data = data.copy()\n'
        qyoq__ftmxe += '        np.random.shuffle(data)\n'
        qyoq__ftmxe += '        return data\n'
        qyoq__ftmxe += '    else:\n'
        qyoq__ftmxe += """        dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        qyoq__ftmxe += '        permutation = np.arange(dim0_global_size)\n'
        qyoq__ftmxe += '        np.random.shuffle(permutation)\n'
        qyoq__ftmxe += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        qyoq__ftmxe += """        output = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        qyoq__ftmxe += (
            '        dtype_size = bodo.io.np_io.get_dtype_size(data.dtype)\n')
        qyoq__ftmxe += """        bodo.libs.distributed_api.dist_permutation_array_index(output, dim0_global_size, dtype_size, data, permutation, len(permutation))
"""
        qyoq__ftmxe += '        return output\n'
    else:
        qyoq__ftmxe += """    return bodo.libs.distributed_api.rebalance(data, dests=dests, random=True, random_seed=seed, parallel=parallel)
"""
    jhgbi__fmi = {}
    exec(qyoq__ftmxe, {'np': np, 'bodo': bodo}, jhgbi__fmi)
    impl = jhgbi__fmi['impl']
    return impl


@numba.generated_jit(nopython=True)
def allgatherv(data, warn_if_rep=True, root=MPI_ROOT):
    return lambda data, warn_if_rep=True, root=MPI_ROOT: gatherv(data, True,
        warn_if_rep, root)


@numba.njit
def get_scatter_null_bytes_buff(null_bitmap_ptr, sendcounts, sendcounts_nulls):
    if bodo.get_rank() != MPI_ROOT:
        return np.empty(1, np.uint8)
    jutw__sblzx = np.empty(sendcounts_nulls.sum(), np.uint8)
    glmxp__unl = 0
    uqlkv__umevo = 0
    for sdl__ztute in range(len(sendcounts)):
        egh__hdj = sendcounts[sdl__ztute]
        hox__gwou = sendcounts_nulls[sdl__ztute]
        dyy__sxl = jutw__sblzx[glmxp__unl:glmxp__unl + hox__gwou]
        for lau__njwbh in range(egh__hdj):
            set_bit_to_arr(dyy__sxl, lau__njwbh, get_bit_bitmap(
                null_bitmap_ptr, uqlkv__umevo))
            uqlkv__umevo += 1
        glmxp__unl += hox__gwou
    return jutw__sblzx


def _bcast_dtype(data):
    try:
        from mpi4py import MPI
    except:
        raise BodoError('mpi4py is required for scatterv')
    atn__olbp = MPI.COMM_WORLD
    data = atn__olbp.bcast(data)
    return data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_scatterv_send_counts(send_counts, n_pes, n):
    if not is_overload_none(send_counts):
        return lambda send_counts, n_pes, n: send_counts

    def impl(send_counts, n_pes, n):
        send_counts = np.empty(n_pes, np.int32)
        for i in range(n_pes):
            send_counts[i] = get_node_portion(n, n_pes, i)
        return send_counts
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _scatterv_np(data, send_counts=None, warn_if_dist=True):
    typ_val = numba_to_c_type(data.dtype)
    zsxex__axsc = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    ofv__epxda = (0,) * zsxex__axsc

    def scatterv_arr_impl(data, send_counts=None, warn_if_dist=True):
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        qvwm__lnr = np.ascontiguousarray(data)
        rtfn__ouxp = data.ctypes
        elva__leokf = ofv__epxda
        if rank == MPI_ROOT:
            elva__leokf = qvwm__lnr.shape
        elva__leokf = bcast_tuple(elva__leokf)
        ejv__zwsh = get_tuple_prod(elva__leokf[1:])
        send_counts = _get_scatterv_send_counts(send_counts, n_pes,
            elva__leokf[0])
        send_counts *= ejv__zwsh
        hcob__xzh = send_counts[rank]
        dqy__nfn = np.empty(hcob__xzh, dtype)
        nfapy__rnp = bodo.ir.join.calc_disp(send_counts)
        c_scatterv(rtfn__ouxp, send_counts.ctypes, nfapy__rnp.ctypes,
            dqy__nfn.ctypes, np.int32(hcob__xzh), np.int32(typ_val))
        return dqy__nfn.reshape((-1,) + elva__leokf[1:])
    return scatterv_arr_impl


def _get_name_value_for_type(name_typ):
    assert isinstance(name_typ, (types.UnicodeType, types.StringLiteral)
        ) or name_typ == types.none
    return None if name_typ == types.none else '_' + str(ir_utils.next_label())


def get_value_for_type(dtype):
    if isinstance(dtype, types.Array):
        return np.zeros((1,) * dtype.ndim, numba.np.numpy_support.as_dtype(
            dtype.dtype))
    if dtype == string_array_type:
        return pd.array(['A'], 'string')
    if dtype == binary_array_type:
        return np.array([b'A'], dtype=object)
    if isinstance(dtype, IntegerArrayType):
        ldvb__gjrtb = '{}Int{}'.format('' if dtype.dtype.signed else 'U',
            dtype.dtype.bitwidth)
        return pd.array([3], ldvb__gjrtb)
    if dtype == boolean_array:
        return pd.array([True], 'boolean')
    if isinstance(dtype, DecimalArrayType):
        return np.array([Decimal('32.1')])
    if dtype == datetime_date_array_type:
        return np.array([datetime.date(2011, 8, 9)])
    if dtype == datetime_timedelta_array_type:
        return np.array([datetime.timedelta(33)])
    if bodo.hiframes.pd_index_ext.is_pd_index_type(dtype):
        tjyx__aemmp = _get_name_value_for_type(dtype.name_typ)
        if isinstance(dtype, bodo.hiframes.pd_index_ext.RangeIndexType):
            return pd.RangeIndex(1, name=tjyx__aemmp)
        soed__ocrhb = bodo.utils.typing.get_index_data_arr_types(dtype)[0]
        arr = get_value_for_type(soed__ocrhb)
        return pd.Index(arr, name=tjyx__aemmp)
    if isinstance(dtype, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        tjyx__aemmp = _get_name_value_for_type(dtype.name_typ)
        ves__dua = tuple(_get_name_value_for_type(t) for t in dtype.names_typ)
        zvfv__dzljn = tuple(get_value_for_type(t) for t in dtype.array_types)
        val = pd.MultiIndex.from_arrays(zvfv__dzljn, names=ves__dua)
        val.name = tjyx__aemmp
        return val
    if isinstance(dtype, bodo.hiframes.pd_series_ext.SeriesType):
        tjyx__aemmp = _get_name_value_for_type(dtype.name_typ)
        arr = get_value_for_type(dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.Series(arr, index, name=tjyx__aemmp)
    if isinstance(dtype, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        zvfv__dzljn = tuple(get_value_for_type(t) for t in dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.DataFrame({tjyx__aemmp: arr for tjyx__aemmp, arr in zip(
            dtype.columns, zvfv__dzljn)}, index)
    if isinstance(dtype, CategoricalArrayType):
        return pd.Categorical.from_codes([0], dtype.dtype.categories)
    if isinstance(dtype, types.BaseTuple):
        return tuple(get_value_for_type(t) for t in dtype.types)
    if isinstance(dtype, ArrayItemArrayType):
        return pd.Series([get_value_for_type(dtype.dtype),
            get_value_for_type(dtype.dtype)]).values
    if isinstance(dtype, IntervalArrayType):
        soed__ocrhb = get_value_for_type(dtype.arr_type)
        return pd.arrays.IntervalArray([pd.Interval(soed__ocrhb[0],
            soed__ocrhb[0])])
    raise BodoError(f'get_value_for_type(dtype): Missing data type {dtype}')


def scatterv(data, send_counts=None, warn_if_dist=True):
    rank = bodo.libs.distributed_api.get_rank()
    if rank != MPI_ROOT and data is not None:
        warnings.warn(BodoWarning(
            "bodo.scatterv(): A non-None value for 'data' was found on a rank other than the root. This data won't be sent to any other ranks and will be overwritten with data from rank 0."
            ))
    dtype = bodo.typeof(data)
    dtype = _bcast_dtype(dtype)
    if rank != MPI_ROOT:
        data = get_value_for_type(dtype)
    return scatterv_impl(data, send_counts)


@overload(scatterv)
def scatterv_overload(data, send_counts=None, warn_if_dist=True):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.scatterv()')
    return lambda data, send_counts=None, warn_if_dist=True: scatterv_impl(data
        , send_counts)


@numba.generated_jit(nopython=True)
def scatterv_impl(data, send_counts=None, warn_if_dist=True):
    if isinstance(data, types.Array):
        return lambda data, send_counts=None, warn_if_dist=True: _scatterv_np(
            data, send_counts)
    if data in [binary_array_type, string_array_type]:
        xlgsr__sgsyi = np.int32(numba_to_c_type(types.int32))
        sbzyt__tuf = np.int32(numba_to_c_type(types.uint8))
        if data == binary_array_type:
            tqmih__umu = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            tqmih__umu = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        qyoq__ftmxe = f"""def impl(
            data, send_counts=None, warn_if_dist=True
        ):  # pragma: no cover
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            n_all = bodo.libs.distributed_api.bcast_scalar(len(data))

            # convert offsets to lengths of strings
            send_arr_lens = np.empty(
                len(data), np.uint32
            )  # XXX offset type is offset_type, lengths for comm are uint32
            for i in range(len(data)):
                send_arr_lens[i] = bodo.libs.str_arr_ext.get_str_arr_item_length(
                    data, i
                )

            # ------- calculate buffer counts -------

            send_counts = bodo.libs.distributed_api._get_scatterv_send_counts(send_counts, n_pes, n_all)

            # displacements
            displs = bodo.ir.join.calc_disp(send_counts)

            # compute send counts for characters
            send_counts_char = np.empty(n_pes, np.int32)
            if rank == 0:
                curr_str = 0
                for i in range(n_pes):
                    c = 0
                    for _ in range(send_counts[i]):
                        c += send_arr_lens[curr_str]
                        curr_str += 1
                    send_counts_char[i] = c

            bodo.libs.distributed_api.bcast(send_counts_char)

            # displacements for characters
            displs_char = bodo.ir.join.calc_disp(send_counts_char)

            # compute send counts for nulls
            send_counts_nulls = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                send_counts_nulls[i] = (send_counts[i] + 7) >> 3

            # displacements for nulls
            displs_nulls = bodo.ir.join.calc_disp(send_counts_nulls)

            # alloc output array
            n_loc = send_counts[rank]  # total number of elements on this PE
            n_loc_char = send_counts_char[rank]
            recv_arr = {tqmih__umu}(n_loc, n_loc_char)

            # ----- string lengths -----------

            recv_lens = np.empty(n_loc, np.uint32)
            bodo.libs.distributed_api.c_scatterv(
                send_arr_lens.ctypes,
                send_counts.ctypes,
                displs.ctypes,
                recv_lens.ctypes,
                np.int32(n_loc),
                int32_typ_enum,
            )

            # TODO: don't hardcode offset type. Also, if offset is 32 bit we can
            # use the same buffer
            bodo.libs.str_arr_ext.convert_len_arr_to_offset(recv_lens.ctypes, bodo.libs.str_arr_ext.get_offset_ptr(recv_arr), n_loc)

            # ----- string characters -----------

            bodo.libs.distributed_api.c_scatterv(
                bodo.libs.str_arr_ext.get_data_ptr(data),
                send_counts_char.ctypes,
                displs_char.ctypes,
                bodo.libs.str_arr_ext.get_data_ptr(recv_arr),
                np.int32(n_loc_char),
                char_typ_enum,
            )

            # ----------- null bitmap -------------

            n_recv_bytes = (n_loc + 7) >> 3

            send_null_bitmap = bodo.libs.distributed_api.get_scatter_null_bytes_buff(
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(data), send_counts, send_counts_nulls
            )

            bodo.libs.distributed_api.c_scatterv(
                send_null_bitmap.ctypes,
                send_counts_nulls.ctypes,
                displs_nulls.ctypes,
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(recv_arr),
                np.int32(n_recv_bytes),
                char_typ_enum,
            )

            return recv_arr"""
        jhgbi__fmi = dict()
        exec(qyoq__ftmxe, {'bodo': bodo, 'np': np, 'int32_typ_enum':
            xlgsr__sgsyi, 'char_typ_enum': sbzyt__tuf}, jhgbi__fmi)
        impl = jhgbi__fmi['impl']
        return impl
    if isinstance(data, ArrayItemArrayType):
        xlgsr__sgsyi = np.int32(numba_to_c_type(types.int32))
        sbzyt__tuf = np.int32(numba_to_c_type(types.uint8))

        def scatterv_array_item_impl(data, send_counts=None, warn_if_dist=True
            ):
            jdv__qsj = bodo.libs.array_item_arr_ext.get_offsets(data)
            jadwj__gfx = bodo.libs.array_item_arr_ext.get_data(data)
            cgxpk__kkzmn = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            jjh__kzg = bcast_scalar(len(data))
            hmeh__xrkz = np.empty(len(data), np.uint32)
            for i in range(len(data)):
                hmeh__xrkz[i] = jdv__qsj[i + 1] - jdv__qsj[i]
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                jjh__kzg)
            nfapy__rnp = bodo.ir.join.calc_disp(send_counts)
            whx__obs = np.empty(n_pes, np.int32)
            if rank == 0:
                tzyz__pjc = 0
                for i in range(n_pes):
                    vpazv__gelr = 0
                    for tlk__ufjd in range(send_counts[i]):
                        vpazv__gelr += hmeh__xrkz[tzyz__pjc]
                        tzyz__pjc += 1
                    whx__obs[i] = vpazv__gelr
            bcast(whx__obs)
            ueold__helw = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                ueold__helw[i] = send_counts[i] + 7 >> 3
            egibb__pjlwi = bodo.ir.join.calc_disp(ueold__helw)
            hcob__xzh = send_counts[rank]
            bobk__hkxwc = np.empty(hcob__xzh + 1, np_offset_type)
            iyxw__onj = bodo.libs.distributed_api.scatterv_impl(jadwj__gfx,
                whx__obs)
            jywrl__wit = hcob__xzh + 7 >> 3
            euzs__vtzy = np.empty(jywrl__wit, np.uint8)
            otv__xhm = np.empty(hcob__xzh, np.uint32)
            c_scatterv(hmeh__xrkz.ctypes, send_counts.ctypes, nfapy__rnp.
                ctypes, otv__xhm.ctypes, np.int32(hcob__xzh), xlgsr__sgsyi)
            convert_len_arr_to_offset(otv__xhm.ctypes, bobk__hkxwc.ctypes,
                hcob__xzh)
            encw__jsej = get_scatter_null_bytes_buff(cgxpk__kkzmn.ctypes,
                send_counts, ueold__helw)
            c_scatterv(encw__jsej.ctypes, ueold__helw.ctypes, egibb__pjlwi.
                ctypes, euzs__vtzy.ctypes, np.int32(jywrl__wit), sbzyt__tuf)
            return bodo.libs.array_item_arr_ext.init_array_item_array(hcob__xzh
                , iyxw__onj, bobk__hkxwc, euzs__vtzy)
        return scatterv_array_item_impl
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        sbzyt__tuf = np.int32(numba_to_c_type(types.uint8))
        if isinstance(data, IntegerArrayType):
            kdkxw__khwa = bodo.libs.int_arr_ext.init_integer_array
        if isinstance(data, DecimalArrayType):
            precision = data.precision
            scale = data.scale
            kdkxw__khwa = numba.njit(no_cpython_wrapper=True)(lambda d, b:
                bodo.libs.decimal_arr_ext.init_decimal_array(d, b,
                precision, scale))
        if data == boolean_array:
            kdkxw__khwa = bodo.libs.bool_arr_ext.init_bool_array
        if data == datetime_date_array_type:
            kdkxw__khwa = (bodo.hiframes.datetime_date_ext.
                init_datetime_date_array)

        def scatterv_impl_int_arr(data, send_counts=None, warn_if_dist=True):
            n_pes = bodo.libs.distributed_api.get_size()
            qvwm__lnr = data._data
            ohz__dommw = data._null_bitmap
            tikh__lubm = len(qvwm__lnr)
            zqfrz__nhjwp = _scatterv_np(qvwm__lnr, send_counts)
            jjh__kzg = bcast_scalar(tikh__lubm)
            towi__klpj = len(zqfrz__nhjwp) + 7 >> 3
            tzhvt__txggo = np.empty(towi__klpj, np.uint8)
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                jjh__kzg)
            ueold__helw = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                ueold__helw[i] = send_counts[i] + 7 >> 3
            egibb__pjlwi = bodo.ir.join.calc_disp(ueold__helw)
            encw__jsej = get_scatter_null_bytes_buff(ohz__dommw.ctypes,
                send_counts, ueold__helw)
            c_scatterv(encw__jsej.ctypes, ueold__helw.ctypes, egibb__pjlwi.
                ctypes, tzhvt__txggo.ctypes, np.int32(towi__klpj), sbzyt__tuf)
            return kdkxw__khwa(zqfrz__nhjwp, tzhvt__txggo)
        return scatterv_impl_int_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, send_counts=None, warn_if_dist=True):
            ovewz__rbpsn = bodo.libs.distributed_api.scatterv_impl(data.
                _left, send_counts)
            xsa__qfhsx = bodo.libs.distributed_api.scatterv_impl(data.
                _right, send_counts)
            return bodo.libs.interval_arr_ext.init_interval_array(ovewz__rbpsn,
                xsa__qfhsx)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, send_counts=None, warn_if_dist=True):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            start = data._start
            stop = data._stop
            reok__iiil = data._step
            tjyx__aemmp = data._name
            tjyx__aemmp = bcast_scalar(tjyx__aemmp)
            start = bcast_scalar(start)
            stop = bcast_scalar(stop)
            reok__iiil = bcast_scalar(reok__iiil)
            yin__akset = bodo.libs.array_kernels.calc_nitems(start, stop,
                reok__iiil)
            chunk_start = bodo.libs.distributed_api.get_start(yin__akset,
                n_pes, rank)
            chunk_count = bodo.libs.distributed_api.get_node_portion(yin__akset
                , n_pes, rank)
            epd__exgn = start + reok__iiil * chunk_start
            xgvsl__bja = start + reok__iiil * (chunk_start + chunk_count)
            xgvsl__bja = min(xgvsl__bja, stop)
            return bodo.hiframes.pd_index_ext.init_range_index(epd__exgn,
                xgvsl__bja, reok__iiil, tjyx__aemmp)
        return impl_range_index
    if isinstance(data, bodo.hiframes.pd_index_ext.PeriodIndexType):
        jdga__ccra = data.freq

        def impl_period_index(data, send_counts=None, warn_if_dist=True):
            qvwm__lnr = data._data
            tjyx__aemmp = data._name
            tjyx__aemmp = bcast_scalar(tjyx__aemmp)
            arr = bodo.libs.distributed_api.scatterv_impl(qvwm__lnr,
                send_counts)
            return bodo.hiframes.pd_index_ext.init_period_index(arr,
                tjyx__aemmp, jdga__ccra)
        return impl_period_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, send_counts=None, warn_if_dist=True):
            qvwm__lnr = data._data
            tjyx__aemmp = data._name
            tjyx__aemmp = bcast_scalar(tjyx__aemmp)
            arr = bodo.libs.distributed_api.scatterv_impl(qvwm__lnr,
                send_counts)
            return bodo.utils.conversion.index_from_array(arr, tjyx__aemmp)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, send_counts=None, warn_if_dist=True):
            ufdng__wyy = bodo.libs.distributed_api.scatterv_impl(data._data,
                send_counts)
            tjyx__aemmp = bcast_scalar(data._name)
            ves__dua = bcast_tuple(data._names)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(ufdng__wyy
                , ves__dua, tjyx__aemmp)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, send_counts=None, warn_if_dist=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            tjyx__aemmp = bodo.hiframes.pd_series_ext.get_series_name(data)
            gfazi__swm = bcast_scalar(tjyx__aemmp)
            out_arr = bodo.libs.distributed_api.scatterv_impl(arr, send_counts)
            rnp__spqtk = bodo.libs.distributed_api.scatterv_impl(index,
                send_counts)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rnp__spqtk, gfazi__swm)
        return impl_series
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        omz__dnke = len(data.columns)
        rgopz__ulpm = ', '.join('g_data_{}'.format(i) for i in range(omz__dnke)
            )
        esqem__tgjw = bodo.utils.transform.gen_const_tup(data.columns)
        qyoq__ftmxe = (
            'def impl_df(data, send_counts=None, warn_if_dist=True):\n')
        for i in range(omz__dnke):
            qyoq__ftmxe += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            qyoq__ftmxe += (
                """  g_data_{} = bodo.libs.distributed_api.scatterv_impl(data_{}, send_counts)
"""
                .format(i, i))
        qyoq__ftmxe += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        qyoq__ftmxe += (
            '  g_index = bodo.libs.distributed_api.scatterv_impl(index, send_counts)\n'
            )
        qyoq__ftmxe += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})
"""
            .format(rgopz__ulpm, esqem__tgjw))
        jhgbi__fmi = {}
        exec(qyoq__ftmxe, {'bodo': bodo}, jhgbi__fmi)
        yaf__vrds = jhgbi__fmi['impl_df']
        return yaf__vrds
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, send_counts=None, warn_if_dist=True):
            engfp__kuz = bodo.libs.distributed_api.scatterv_impl(data.codes,
                send_counts)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                engfp__kuz, data.dtype)
        return impl_cat
    if isinstance(data, types.BaseTuple):
        qyoq__ftmxe = (
            'def impl_tuple(data, send_counts=None, warn_if_dist=True):\n')
        qyoq__ftmxe += '  return ({}{})\n'.format(', '.join(
            'bodo.libs.distributed_api.scatterv_impl(data[{}], send_counts)'
            .format(i) for i in range(len(data))), ',' if len(data) > 0 else ''
            )
        jhgbi__fmi = {}
        exec(qyoq__ftmxe, {'bodo': bodo}, jhgbi__fmi)
        hfu__ear = jhgbi__fmi['impl_tuple']
        return hfu__ear
    if data is types.none:
        return lambda data, send_counts=None, warn_if_dist=True: None
    raise BodoError('scatterv() not available for {}'.format(data))


@intrinsic
def cptr_to_voidptr(typingctx, cptr_tp=None):

    def codegen(context, builder, sig, args):
        return builder.bitcast(args[0], lir.IntType(8).as_pointer())
    return types.voidptr(cptr_tp), codegen


def bcast(data):
    return


@overload(bcast, no_unliteral=True)
def bcast_overload(data):
    if isinstance(data, types.Array):

        def bcast_impl(data):
            typ_enum = get_type_enum(data)
            count = data.size
            assert count < INT_MAX
            c_bcast(data.ctypes, np.int32(count), typ_enum, np.array([-1]).
                ctypes, 0)
            return
        return bcast_impl
    if isinstance(data, DecimalArrayType):

        def bcast_decimal_arr(data):
            count = data._data.size
            assert count < INT_MAX
            c_bcast(data._data.ctypes, np.int32(count), CTypeEnum.Int128.
                value, np.array([-1]).ctypes, 0)
            bcast(data._null_bitmap)
            return
        return bcast_decimal_arr
    if isinstance(data, IntegerArrayType) or data in (boolean_array,
        datetime_date_array_type):

        def bcast_impl_int_arr(data):
            bcast(data._data)
            bcast(data._null_bitmap)
            return
        return bcast_impl_int_arr
    if data in [binary_array_type, string_array_type]:
        dlzr__xyit = np.int32(numba_to_c_type(offset_type))
        sbzyt__tuf = np.int32(numba_to_c_type(types.uint8))

        def bcast_str_impl(data):
            hcob__xzh = len(data)
            mhogr__pktk = num_total_chars(data)
            assert hcob__xzh < INT_MAX
            assert mhogr__pktk < INT_MAX
            lkndm__etn = get_offset_ptr(data)
            rtfn__ouxp = get_data_ptr(data)
            null_bitmap_ptr = get_null_bitmap_ptr(data)
            hox__gwou = hcob__xzh + 7 >> 3
            c_bcast(lkndm__etn, np.int32(hcob__xzh + 1), dlzr__xyit, np.
                array([-1]).ctypes, 0)
            c_bcast(rtfn__ouxp, np.int32(mhogr__pktk), sbzyt__tuf, np.array
                ([-1]).ctypes, 0)
            c_bcast(null_bitmap_ptr, np.int32(hox__gwou), sbzyt__tuf, np.
                array([-1]).ctypes, 0)
        return bcast_str_impl


c_bcast = types.ExternalFunction('c_bcast', types.void(types.voidptr, types
    .int32, types.int32, types.voidptr, types.int32))


def bcast_scalar(val):
    return val


@overload(bcast_scalar, no_unliteral=True)
def bcast_scalar_overload(val):
    val = types.unliteral(val)
    if not (isinstance(val, (types.Integer, types.Float)) or val in [bodo.
        datetime64ns, bodo.timedelta64ns, bodo.string_type, types.none,
        types.bool_]):
        raise_bodo_error(
            f'bcast_scalar requires an argument of type Integer, Float, datetime64ns, timedelta64ns, string, None, or Bool. Found type {val}'
            )
    if val == types.none:
        return lambda val: None
    if val == bodo.string_type:
        sbzyt__tuf = np.int32(numba_to_c_type(types.uint8))

        def impl_str(val):
            rank = bodo.libs.distributed_api.get_rank()
            if rank != MPI_ROOT:
                iko__alfoq = 0
                tcbq__dbvl = np.empty(0, np.uint8).ctypes
            else:
                tcbq__dbvl, iko__alfoq = (bodo.libs.str_ext.
                    unicode_to_utf8_and_len(val))
            iko__alfoq = bodo.libs.distributed_api.bcast_scalar(iko__alfoq)
            if rank != MPI_ROOT:
                vrgxr__sztek = np.empty(iko__alfoq + 1, np.uint8)
                vrgxr__sztek[iko__alfoq] = 0
                tcbq__dbvl = vrgxr__sztek.ctypes
            c_bcast(tcbq__dbvl, np.int32(iko__alfoq), sbzyt__tuf, np.array(
                [-1]).ctypes, 0)
            return bodo.libs.str_arr_ext.decode_utf8(tcbq__dbvl, iko__alfoq)
        return impl_str
    typ_val = numba_to_c_type(val)
    qyoq__ftmxe = (
        """def bcast_scalar_impl(val):
  send = np.empty(1, dtype)
  send[0] = val
  c_bcast(send.ctypes, np.int32(1), np.int32({}), np.array([-1]).ctypes, 0)
  return send[0]
"""
        .format(typ_val))
    dtype = numba.np.numpy_support.as_dtype(val)
    jhgbi__fmi = {}
    exec(qyoq__ftmxe, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast, 'dtype':
        dtype}, jhgbi__fmi)
    kim__snh = jhgbi__fmi['bcast_scalar_impl']
    return kim__snh


def bcast_tuple(val):
    return val


@overload(bcast_tuple, no_unliteral=True)
def overload_bcast_tuple(val):
    assert isinstance(val, types.BaseTuple)
    ytlw__gix = len(val)
    qyoq__ftmxe = 'def bcast_tuple_impl(val):\n'
    qyoq__ftmxe += '  return ({}{})'.format(','.join(
        'bcast_scalar(val[{}])'.format(i) for i in range(ytlw__gix)), ',' if
        ytlw__gix else '')
    jhgbi__fmi = {}
    exec(qyoq__ftmxe, {'bcast_scalar': bcast_scalar}, jhgbi__fmi)
    qlsxa__kdmy = jhgbi__fmi['bcast_tuple_impl']
    return qlsxa__kdmy


def prealloc_str_for_bcast(arr):
    return arr


@overload(prealloc_str_for_bcast, no_unliteral=True)
def prealloc_str_for_bcast_overload(arr):
    if arr == string_array_type:

        def prealloc_impl(arr):
            rank = bodo.libs.distributed_api.get_rank()
            hcob__xzh = bcast_scalar(len(arr))
            upimt__foq = bcast_scalar(np.int64(num_total_chars(arr)))
            if rank != MPI_ROOT:
                arr = pre_alloc_string_array(hcob__xzh, upimt__foq)
            return arr
        return prealloc_impl
    return lambda arr: arr


def get_local_slice(idx, arr_start, total_len):
    return idx


@overload(get_local_slice, no_unliteral=True, jit_options={'cache': True,
    'no_cpython_wrapper': True})
def get_local_slice_overload(idx, arr_start, total_len):

    def impl(idx, arr_start, total_len):
        slice_index = numba.cpython.unicode._normalize_slice(idx, total_len)
        start = slice_index.start
        reok__iiil = slice_index.step
        rekfn__psl = 0 if reok__iiil == 1 or start > arr_start else abs(
            reok__iiil - arr_start % reok__iiil) % reok__iiil
        epd__exgn = max(arr_start, slice_index.start) - arr_start + rekfn__psl
        xgvsl__bja = max(slice_index.stop - arr_start, 0)
        return slice(epd__exgn, xgvsl__bja, reok__iiil)
    return impl


def slice_getitem(arr, slice_index, arr_start, total_len):
    return arr[slice_index]


@overload(slice_getitem, no_unliteral=True, jit_options={'cache': True})
def slice_getitem_overload(arr, slice_index, arr_start, total_len):

    def getitem_impl(arr, slice_index, arr_start, total_len):
        ong__yffkt = get_local_slice(slice_index, arr_start, total_len)
        return bodo.utils.conversion.ensure_contig_if_np(arr[ong__yffkt])
    return getitem_impl


def slice_getitem_from_start(arr, slice_index):
    return arr[slice_index]


@overload(slice_getitem_from_start, no_unliteral=True)
def slice_getitem_from_start_overload(arr, slice_index):
    if arr == bodo.hiframes.datetime_date_ext.datetime_date_array_type:

        def getitem_datetime_date_impl(arr, slice_index):
            rank = bodo.libs.distributed_api.get_rank()
            lff__fzbm = slice_index.stop
            A = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
                lff__fzbm)
            if rank == 0:
                A = arr[:lff__fzbm]
            bodo.libs.distributed_api.bcast(A)
            return A
        return getitem_datetime_date_impl
    if (arr == bodo.hiframes.datetime_timedelta_ext.
        datetime_timedelta_array_type):

        def getitem_datetime_timedelta_impl(arr, slice_index):
            rank = bodo.libs.distributed_api.get_rank()
            lff__fzbm = slice_index.stop
            A = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(lff__fzbm))
            if rank == 0:
                A = arr[:lff__fzbm]
            bodo.libs.distributed_api.bcast(A)
            return A
        return getitem_datetime_timedelta_impl
    if isinstance(arr.dtype, Decimal128Type):
        precision = arr.dtype.precision
        scale = arr.dtype.scale

        def getitem_decimal_impl(arr, slice_index):
            rank = bodo.libs.distributed_api.get_rank()
            lff__fzbm = slice_index.stop
            A = bodo.libs.decimal_arr_ext.alloc_decimal_array(lff__fzbm,
                precision, scale)
            if rank == 0:
                for i in range(lff__fzbm):
                    A._data[i] = arr._data[i]
                    ffh__lxmrj = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, i,
                        ffh__lxmrj)
            bodo.libs.distributed_api.bcast(A)
            return A
        return getitem_decimal_impl
    if arr == string_array_type:

        def getitem_str_impl(arr, slice_index):
            rank = bodo.libs.distributed_api.get_rank()
            lff__fzbm = slice_index.stop
            lrbb__pny = np.uint64(0)
            if rank == 0:
                out_arr = arr[:lff__fzbm]
                lrbb__pny = num_total_chars(out_arr)
            lrbb__pny = bcast_scalar(lrbb__pny)
            if rank != 0:
                out_arr = pre_alloc_string_array(lff__fzbm, lrbb__pny)
            bodo.libs.distributed_api.bcast(out_arr)
            return out_arr
        return getitem_str_impl
    soed__ocrhb = arr

    def getitem_impl(arr, slice_index):
        rank = bodo.libs.distributed_api.get_rank()
        lff__fzbm = slice_index.stop
        out_arr = bodo.utils.utils.alloc_type(tuple_to_scalar((lff__fzbm,) +
            arr.shape[1:]), soed__ocrhb)
        if rank == 0:
            out_arr = arr[:lff__fzbm]
        bodo.libs.distributed_api.bcast(out_arr)
        return out_arr
    return getitem_impl


dummy_use = numba.njit(lambda a: None)


def int_getitem(arr, ind, arr_start, total_len, is_1D):
    return arr[ind]


def transform_str_getitem_output(data, length):
    pass


@overload(transform_str_getitem_output)
def overload_transform_str_getitem_output(data, length):
    if data == bodo.string_type:
        return lambda data, length: bodo.libs.str_arr_ext.decode_utf8(data.
            _data, length)
    if data == types.Array(types.uint8, 1, 'C'):
        return lambda data, length: bodo.libs.binary_arr_ext.init_bytes_type(
            data, length)
    raise BodoError(
        f'Internal Error: Expected String or Uint8 Array, found {data}')


@overload(int_getitem, no_unliteral=True)
def int_getitem_overload(arr, ind, arr_start, total_len, is_1D):
    if arr in [bodo.binary_array_type, string_array_type]:
        kep__jazm = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND
        sbzyt__tuf = np.int32(numba_to_c_type(types.uint8))
        lxaoa__ggpjm = arr.dtype

        def str_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            wsj__mifu = np.int32(10)
            tag = np.int32(11)
            yov__spea = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                ind = ind - arr_start
                hmk__nedu = arr._data
                jzqqa__wuw = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    hmk__nedu, ind)
                vapqc__strul = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    hmk__nedu, ind + 1)
                length = vapqc__strul - jzqqa__wuw
                qxor__ynjrb = hmk__nedu[ind]
                yov__spea[0] = length
                isend(yov__spea, np.int32(1), root, wsj__mifu, True)
                isend(qxor__ynjrb, np.int32(length), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                lxaoa__ggpjm, kep__jazm, 0, 1)
            qkugv__ogxbj = 0
            if rank == root:
                qkugv__ogxbj = recv(np.int64, ANY_SOURCE, wsj__mifu)
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    lxaoa__ggpjm, kep__jazm, qkugv__ogxbj, 1)
                rtfn__ouxp = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
                _recv(rtfn__ouxp, np.int32(qkugv__ogxbj), sbzyt__tuf,
                    ANY_SOURCE, tag)
            dummy_use(yov__spea)
            qkugv__ogxbj = bcast_scalar(qkugv__ogxbj)
            if rank != root:
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    lxaoa__ggpjm, kep__jazm, qkugv__ogxbj, 1)
            rtfn__ouxp = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
            c_bcast(rtfn__ouxp, np.int32(qkugv__ogxbj), sbzyt__tuf, np.
                array([-1]).ctypes, 0)
            val = transform_str_getitem_output(val, qkugv__ogxbj)
            return val
        return str_getitem_impl
    if isinstance(arr, bodo.CategoricalArrayType):
        ype__ttei = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def cat_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, ype__ttei)
            if arr_start <= ind < arr_start + len(arr):
                engfp__kuz = (bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(arr))
                data = engfp__kuz[ind - arr_start]
                send_arr = np.full(1, data, ype__ttei)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = ype__ttei(-1)
            if rank == root:
                val = recv(ype__ttei, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            jsher__yii = arr.dtype.categories[max(val, 0)]
            return jsher__yii
        return cat_getitem_impl
    guja__wrtc = arr.dtype

    def getitem_impl(arr, ind, arr_start, total_len, is_1D):
        if ind >= total_len:
            raise IndexError('index out of bounds')
        ind = ind % total_len
        root = np.int32(0)
        tag = np.int32(11)
        send_arr = np.zeros(1, guja__wrtc)
        if arr_start <= ind < arr_start + len(arr):
            data = arr[ind - arr_start]
            send_arr = np.full(1, data)
            isend(send_arr, np.int32(1), root, tag, True)
        rank = bodo.libs.distributed_api.get_rank()
        val = np.zeros(1, guja__wrtc)[0]
        if rank == root:
            val = recv(guja__wrtc, ANY_SOURCE, tag)
        dummy_use(send_arr)
        val = bcast_scalar(val)
        return val
    return getitem_impl


c_alltoallv = types.ExternalFunction('c_alltoallv', types.void(types.
    voidptr, types.voidptr, types.voidptr, types.voidptr, types.voidptr,
    types.voidptr, types.int32))


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def alltoallv(send_data, out_data, send_counts, recv_counts, send_disp,
    recv_disp):
    typ_enum = get_type_enum(send_data)
    ndohv__ihj = get_type_enum(out_data)
    assert typ_enum == ndohv__ihj
    if isinstance(send_data, (IntegerArrayType, DecimalArrayType)
        ) or send_data in (boolean_array, datetime_date_array_type):
        return (lambda send_data, out_data, send_counts, recv_counts,
            send_disp, recv_disp: c_alltoallv(send_data._data.ctypes,
            out_data._data.ctypes, send_counts.ctypes, recv_counts.ctypes,
            send_disp.ctypes, recv_disp.ctypes, typ_enum))
    if isinstance(send_data, bodo.CategoricalArrayType):
        return (lambda send_data, out_data, send_counts, recv_counts,
            send_disp, recv_disp: c_alltoallv(send_data.codes.ctypes,
            out_data.codes.ctypes, send_counts.ctypes, recv_counts.ctypes,
            send_disp.ctypes, recv_disp.ctypes, typ_enum))
    return (lambda send_data, out_data, send_counts, recv_counts, send_disp,
        recv_disp: c_alltoallv(send_data.ctypes, out_data.ctypes,
        send_counts.ctypes, recv_counts.ctypes, send_disp.ctypes, recv_disp
        .ctypes, typ_enum))


def alltoallv_tup(send_data, out_data, send_counts, recv_counts, send_disp,
    recv_disp):
    return


@overload(alltoallv_tup, no_unliteral=True)
def alltoallv_tup_overload(send_data, out_data, send_counts, recv_counts,
    send_disp, recv_disp):
    count = send_data.count
    assert out_data.count == count
    qyoq__ftmxe = (
        'def f(send_data, out_data, send_counts, recv_counts, send_disp, recv_disp):\n'
        )
    for i in range(count):
        qyoq__ftmxe += (
            """  alltoallv(send_data[{}], out_data[{}], send_counts, recv_counts, send_disp, recv_disp)
"""
            .format(i, i))
    qyoq__ftmxe += '  return\n'
    jhgbi__fmi = {}
    exec(qyoq__ftmxe, {'alltoallv': alltoallv}, jhgbi__fmi)
    hqin__xecta = jhgbi__fmi['f']
    return hqin__xecta


@numba.njit
def get_start_count(n):
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    start = bodo.libs.distributed_api.get_start(n, n_pes, rank)
    count = bodo.libs.distributed_api.get_node_portion(n, n_pes, rank)
    return start, count


@numba.njit
def get_start(total_size, pes, rank):
    vgwbn__mxk = total_size % pes
    oqtcs__txtf = (total_size - vgwbn__mxk) // pes
    return rank * oqtcs__txtf + min(rank, vgwbn__mxk)


@numba.njit
def get_end(total_size, pes, rank):
    vgwbn__mxk = total_size % pes
    oqtcs__txtf = (total_size - vgwbn__mxk) // pes
    return (rank + 1) * oqtcs__txtf + min(rank + 1, vgwbn__mxk)


@numba.njit
def get_node_portion(total_size, pes, rank):
    vgwbn__mxk = total_size % pes
    oqtcs__txtf = (total_size - vgwbn__mxk) // pes
    if rank < vgwbn__mxk:
        return oqtcs__txtf + 1
    else:
        return oqtcs__txtf


@numba.generated_jit(nopython=True)
def dist_cumsum(in_arr, out_arr):
    piqw__rzyu = in_arr.dtype(0)
    sto__jiwh = np.int32(Reduce_Type.Sum.value)

    def cumsum_impl(in_arr, out_arr):
        vpazv__gelr = piqw__rzyu
        for gtv__ftv in np.nditer(in_arr):
            vpazv__gelr += gtv__ftv.item()
        fdh__qty = dist_exscan(vpazv__gelr, sto__jiwh)
        for i in range(in_arr.size):
            fdh__qty += in_arr[i]
            out_arr[i] = fdh__qty
        return 0
    return cumsum_impl


@numba.generated_jit(nopython=True)
def dist_cumprod(in_arr, out_arr):
    wff__nps = in_arr.dtype(1)
    sto__jiwh = np.int32(Reduce_Type.Prod.value)

    def cumprod_impl(in_arr, out_arr):
        vpazv__gelr = wff__nps
        for gtv__ftv in np.nditer(in_arr):
            vpazv__gelr *= gtv__ftv.item()
        fdh__qty = dist_exscan(vpazv__gelr, sto__jiwh)
        if get_rank() == 0:
            fdh__qty = wff__nps
        for i in range(in_arr.size):
            fdh__qty *= in_arr[i]
            out_arr[i] = fdh__qty
        return 0
    return cumprod_impl


@numba.generated_jit(nopython=True)
def dist_cummin(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        wff__nps = np.finfo(in_arr.dtype(1).dtype).max
    else:
        wff__nps = np.iinfo(in_arr.dtype(1).dtype).max
    sto__jiwh = np.int32(Reduce_Type.Min.value)

    def cummin_impl(in_arr, out_arr):
        vpazv__gelr = wff__nps
        for gtv__ftv in np.nditer(in_arr):
            vpazv__gelr = min(vpazv__gelr, gtv__ftv.item())
        fdh__qty = dist_exscan(vpazv__gelr, sto__jiwh)
        if get_rank() == 0:
            fdh__qty = wff__nps
        for i in range(in_arr.size):
            fdh__qty = min(fdh__qty, in_arr[i])
            out_arr[i] = fdh__qty
        return 0
    return cummin_impl


@numba.generated_jit(nopython=True)
def dist_cummax(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        wff__nps = np.finfo(in_arr.dtype(1).dtype).min
    else:
        wff__nps = np.iinfo(in_arr.dtype(1).dtype).min
    wff__nps = in_arr.dtype(1)
    sto__jiwh = np.int32(Reduce_Type.Max.value)

    def cummax_impl(in_arr, out_arr):
        vpazv__gelr = wff__nps
        for gtv__ftv in np.nditer(in_arr):
            vpazv__gelr = max(vpazv__gelr, gtv__ftv.item())
        fdh__qty = dist_exscan(vpazv__gelr, sto__jiwh)
        if get_rank() == 0:
            fdh__qty = wff__nps
        for i in range(in_arr.size):
            fdh__qty = max(fdh__qty, in_arr[i])
            out_arr[i] = fdh__qty
        return 0
    return cummax_impl


_allgather = types.ExternalFunction('allgather', types.void(types.voidptr,
    types.int32, types.voidptr, types.int32))


@numba.njit
def allgather(arr, val):
    sbio__ltnv = get_type_enum(arr)
    _allgather(arr.ctypes, 1, value_to_ptr(val), sbio__ltnv)


def dist_return(A):
    return A


def dist_return_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    xkic__ieotl = args[0]
    if equiv_set.has_shape(xkic__ieotl):
        return ArrayAnalysis.AnalyzeResult(shape=xkic__ieotl, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_distributed_api_dist_return = (
    dist_return_equiv)


def threaded_return(A):
    return A


@numba.njit
def set_arr_local(arr, ind, val):
    arr[ind] = val


@numba.njit
def local_alloc_size(n, in_arr):
    return n


@infer_global(threaded_return)
@infer_global(dist_return)
class ThreadedRetTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        return signature(args[0], *args)


@numba.njit
def parallel_print(*args):
    print(*args)


@numba.njit
def single_print(*args):
    if bodo.libs.distributed_api.get_rank() == 0:
        print(*args)


@numba.njit(no_cpython_wrapper=True)
def print_if_not_empty(arg):
    if len(arg) != 0 or bodo.get_rank() == 0:
        print(arg)


_wait = types.ExternalFunction('dist_wait', types.void(mpi_req_numba_type,
    types.bool_))


@numba.generated_jit(nopython=True)
def wait(req, cond=True):
    if isinstance(req, types.BaseTuple):
        count = len(req.types)
        qpjyw__kbzk = ','.join(f'_wait(req[{i}], cond)' for i in range(count))
        qyoq__ftmxe = 'def f(req, cond=True):\n'
        qyoq__ftmxe += f'  return {qpjyw__kbzk}\n'
        jhgbi__fmi = {}
        exec(qyoq__ftmxe, {'_wait': _wait}, jhgbi__fmi)
        impl = jhgbi__fmi['f']
        return impl
    if is_overload_none(req):
        return lambda req, cond=True: None
    return lambda req, cond=True: _wait(req, cond)


class ReqArrayType(types.Type):

    def __init__(self):
        super(ReqArrayType, self).__init__(name='ReqArrayType()')


req_array_type = ReqArrayType()
register_model(ReqArrayType)(models.OpaqueModel)
waitall = types.ExternalFunction('dist_waitall', types.void(types.int32,
    req_array_type))
comm_req_alloc = types.ExternalFunction('comm_req_alloc', req_array_type(
    types.int32))
comm_req_dealloc = types.ExternalFunction('comm_req_dealloc', types.void(
    req_array_type))
req_array_setitem = types.ExternalFunction('req_array_setitem', types.void(
    req_array_type, types.int64, mpi_req_numba_type))


@overload(operator.setitem, no_unliteral=True)
def overload_req_arr_setitem(A, idx, val):
    if A == req_array_type:
        assert val == mpi_req_numba_type
        return lambda A, idx, val: req_array_setitem(A, idx, val)


@numba.njit
def _get_local_range(start, stop, chunk_start, chunk_count):
    assert start >= 0 and stop > 0
    epd__exgn = max(start, chunk_start)
    xgvsl__bja = min(stop, chunk_start + chunk_count)
    gprz__rmewz = epd__exgn - chunk_start
    lap__cqhto = xgvsl__bja - chunk_start
    if gprz__rmewz < 0 or lap__cqhto < 0:
        gprz__rmewz = 1
        lap__cqhto = 0
    return gprz__rmewz, lap__cqhto


@register_jitable
def _set_if_in_range(A, val, index, chunk_start):
    if index >= chunk_start and index < chunk_start + len(A):
        A[index - chunk_start] = val


@register_jitable
def _root_rank_select(old_val, new_val):
    if get_rank() == 0:
        return old_val
    return new_val


def get_tuple_prod(t):
    return np.prod(t)


@overload(get_tuple_prod, no_unliteral=True)
def get_tuple_prod_overload(t):
    if t == numba.core.types.containers.Tuple(()):
        return lambda t: 1

    def get_tuple_prod_impl(t):
        vgwbn__mxk = 1
        for a in t:
            vgwbn__mxk *= a
        return vgwbn__mxk
    return get_tuple_prod_impl


sig = types.void(types.voidptr, types.voidptr, types.intp, types.intp,
    types.intp, types.intp, types.int32, types.voidptr)
oneD_reshape_shuffle = types.ExternalFunction('oneD_reshape_shuffle', sig)


@numba.njit(no_cpython_wrapper=True, cache=True)
def dist_oneD_reshape_shuffle(lhs, in_arr, new_dim0_global_len, dest_ranks=None
    ):
    pzpr__vlrj = np.ascontiguousarray(in_arr)
    awhtx__jewb = get_tuple_prod(pzpr__vlrj.shape[1:])
    vtti__pikga = get_tuple_prod(lhs.shape[1:])
    if dest_ranks is not None:
        wped__gcvq = np.array(dest_ranks, dtype=np.int32)
    else:
        wped__gcvq = np.empty(0, dtype=np.int32)
    dtype_size = bodo.io.np_io.get_dtype_size(in_arr.dtype)
    oneD_reshape_shuffle(lhs.ctypes, pzpr__vlrj.ctypes, new_dim0_global_len,
        len(in_arr), dtype_size * vtti__pikga, dtype_size * awhtx__jewb,
        len(wped__gcvq), wped__gcvq.ctypes)
    check_and_propagate_cpp_exception()


permutation_int = types.ExternalFunction('permutation_int', types.void(
    types.voidptr, types.intp))


@numba.njit
def dist_permutation_int(lhs, n):
    permutation_int(lhs.ctypes, n)


permutation_array_index = types.ExternalFunction('permutation_array_index',
    types.void(types.voidptr, types.intp, types.intp, types.voidptr, types.
    int64, types.voidptr, types.intp))


@numba.njit
def dist_permutation_array_index(lhs, lhs_len, dtype_size, rhs, p, p_len):
    sjhx__ceyfd = np.ascontiguousarray(rhs)
    gccd__udaf = get_tuple_prod(sjhx__ceyfd.shape[1:])
    yxwuv__lks = dtype_size * gccd__udaf
    permutation_array_index(lhs.ctypes, lhs_len, yxwuv__lks, sjhx__ceyfd.
        ctypes, sjhx__ceyfd.shape[0], p.ctypes, p_len)
    check_and_propagate_cpp_exception()


from bodo.io import fsspec_reader, hdfs_reader, s3_reader
ll.add_symbol('finalize', hdist.finalize)
finalize = types.ExternalFunction('finalize', types.int32())
ll.add_symbol('finalize_s3', s3_reader.finalize_s3)
finalize_s3 = types.ExternalFunction('finalize_s3', types.int32())
ll.add_symbol('finalize_fsspec', fsspec_reader.finalize_fsspec)
finalize_fsspec = types.ExternalFunction('finalize_fsspec', types.int32())
ll.add_symbol('disconnect_hdfs', hdfs_reader.disconnect_hdfs)
disconnect_hdfs = types.ExternalFunction('disconnect_hdfs', types.int32())


def _check_for_cpp_errors():
    pass


@overload(_check_for_cpp_errors)
def overload_check_for_cpp_errors():
    return lambda : check_and_propagate_cpp_exception()


@numba.njit
def call_finalize():
    finalize()
    finalize_s3()
    finalize_fsspec()
    _check_for_cpp_errors()
    disconnect_hdfs()


def flush_stdout():
    if not sys.stdout.closed:
        sys.stdout.flush()


atexit.register(call_finalize)
atexit.register(flush_stdout)


def bcast_comm(data, comm_ranks, nranks):
    rank = bodo.libs.distributed_api.get_rank()
    dtype = bodo.typeof(data)
    dtype = _bcast_dtype(dtype)
    if rank != MPI_ROOT:
        data = get_value_for_type(dtype)
    return bcast_comm_impl(data, comm_ranks, nranks)


@overload(bcast_comm)
def bcast_comm_overload(data, comm_ranks, nranks):
    return lambda data, comm_ranks, nranks: bcast_comm_impl(data,
        comm_ranks, nranks)


@numba.generated_jit(nopython=True)
def bcast_comm_impl(data, comm_ranks, nranks):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.bcast_comm()')
    if isinstance(data, (types.Integer, types.Float)):
        typ_val = numba_to_c_type(data)
        qyoq__ftmxe = (
            """def bcast_scalar_impl(data, comm_ranks, nranks):
  send = np.empty(1, dtype)
  send[0] = data
  c_bcast(send.ctypes, np.int32(1), np.int32({}), comm_ranks,ctypes, np.int32({}))
  return send[0]
"""
            .format(typ_val, nranks))
        dtype = numba.np.numpy_support.as_dtype(data)
        jhgbi__fmi = {}
        exec(qyoq__ftmxe, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast,
            'dtype': dtype}, jhgbi__fmi)
        kim__snh = jhgbi__fmi['bcast_scalar_impl']
        return kim__snh
    if isinstance(data, types.Array):
        return lambda data, comm_ranks, nranks: _bcast_np(data, comm_ranks,
            nranks)
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        omz__dnke = len(data.columns)
        rgopz__ulpm = ', '.join('g_data_{}'.format(i) for i in range(omz__dnke)
            )
        esqem__tgjw = bodo.utils.transform.gen_const_tup(data.columns)
        qyoq__ftmxe = 'def impl_df(data, comm_ranks, nranks):\n'
        for i in range(omz__dnke):
            qyoq__ftmxe += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            qyoq__ftmxe += (
                """  g_data_{} = bodo.libs.distributed_api.bcast_comm_impl(data_{}, comm_ranks, nranks)
"""
                .format(i, i))
        qyoq__ftmxe += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        qyoq__ftmxe += """  g_index = bodo.libs.distributed_api.bcast_comm_impl(index, comm_ranks, nranks)
"""
        qyoq__ftmxe += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})
"""
            .format(rgopz__ulpm, esqem__tgjw))
        jhgbi__fmi = {}
        exec(qyoq__ftmxe, {'bodo': bodo}, jhgbi__fmi)
        yaf__vrds = jhgbi__fmi['impl_df']
        return yaf__vrds
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, comm_ranks, nranks):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            start = data._start
            stop = data._stop
            reok__iiil = data._step
            tjyx__aemmp = data._name
            tjyx__aemmp = bcast_scalar(tjyx__aemmp)
            start = bcast_scalar(start)
            stop = bcast_scalar(stop)
            reok__iiil = bcast_scalar(reok__iiil)
            yin__akset = bodo.libs.array_kernels.calc_nitems(start, stop,
                reok__iiil)
            chunk_start = bodo.libs.distributed_api.get_start(yin__akset,
                n_pes, rank)
            chunk_count = bodo.libs.distributed_api.get_node_portion(yin__akset
                , n_pes, rank)
            epd__exgn = start + reok__iiil * chunk_start
            xgvsl__bja = start + reok__iiil * (chunk_start + chunk_count)
            xgvsl__bja = min(xgvsl__bja, stop)
            return bodo.hiframes.pd_index_ext.init_range_index(epd__exgn,
                xgvsl__bja, reok__iiil, tjyx__aemmp)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, comm_ranks, nranks):
            qvwm__lnr = data._data
            tjyx__aemmp = data._name
            arr = bodo.libs.distributed_api.bcast_comm_impl(qvwm__lnr,
                comm_ranks, nranks)
            return bodo.utils.conversion.index_from_array(arr, tjyx__aemmp)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, comm_ranks, nranks):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            tjyx__aemmp = bodo.hiframes.pd_series_ext.get_series_name(data)
            gfazi__swm = bodo.libs.distributed_api.bcast_comm_impl(tjyx__aemmp,
                comm_ranks, nranks)
            out_arr = bodo.libs.distributed_api.bcast_comm_impl(arr,
                comm_ranks, nranks)
            rnp__spqtk = bodo.libs.distributed_api.bcast_comm_impl(index,
                comm_ranks, nranks)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rnp__spqtk, gfazi__swm)
        return impl_series
    if isinstance(data, types.BaseTuple):
        qyoq__ftmxe = 'def impl_tuple(data, comm_ranks, nranks):\n'
        qyoq__ftmxe += '  return ({}{})\n'.format(', '.join(
            'bcast_comm_impl(data[{}], comm_ranks, nranks)'.format(i) for i in
            range(len(data))), ',' if len(data) > 0 else '')
        jhgbi__fmi = {}
        exec(qyoq__ftmxe, {'bcast_comm_impl': bcast_comm_impl}, jhgbi__fmi)
        hfu__ear = jhgbi__fmi['impl_tuple']
        return hfu__ear
    if data is types.none:
        return lambda data, comm_ranks, nranks: None


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _bcast_np(data, comm_ranks, nranks):
    typ_val = numba_to_c_type(data.dtype)
    zsxex__axsc = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    ofv__epxda = (0,) * zsxex__axsc

    def bcast_arr_impl(data, comm_ranks, nranks):
        rank = bodo.libs.distributed_api.get_rank()
        qvwm__lnr = np.ascontiguousarray(data)
        rtfn__ouxp = data.ctypes
        elva__leokf = ofv__epxda
        if rank == MPI_ROOT:
            elva__leokf = qvwm__lnr.shape
        elva__leokf = bcast_tuple(elva__leokf)
        ejv__zwsh = get_tuple_prod(elva__leokf[1:])
        send_counts = elva__leokf[0] * ejv__zwsh
        dqy__nfn = np.empty(send_counts, dtype)
        if rank == MPI_ROOT:
            c_bcast(rtfn__ouxp, np.int32(send_counts), np.int32(typ_val),
                comm_ranks.ctypes, np.int32(nranks))
            return data
        else:
            c_bcast(dqy__nfn.ctypes, np.int32(send_counts), np.int32(
                typ_val), comm_ranks.ctypes, np.int32(nranks))
            return dqy__nfn.reshape((-1,) + elva__leokf[1:])
    return bcast_arr_impl


node_ranks = None


def get_host_ranks():
    global node_ranks
    if node_ranks is None:
        atn__olbp = MPI.COMM_WORLD
        ickj__dhxye = MPI.Get_processor_name()
        setl__nub = atn__olbp.allgather(ickj__dhxye)
        node_ranks = defaultdict(list)
        for i, qms__anm in enumerate(setl__nub):
            node_ranks[qms__anm].append(i)
    return node_ranks


def create_subcomm_mpi4py(comm_ranks):
    atn__olbp = MPI.COMM_WORLD
    xsyrn__ntpr = atn__olbp.Get_group()
    vgkr__bvaa = xsyrn__ntpr.Incl(comm_ranks)
    unbnj__gke = atn__olbp.Create_group(vgkr__bvaa)
    return unbnj__gke


def get_nodes_first_ranks():
    reg__fgk = get_host_ranks()
    return np.array([kccnw__czc[0] for kccnw__czc in reg__fgk.values()],
        dtype='int32')


def get_num_nodes():
    return len(get_host_ranks())
