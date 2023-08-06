"""
helper data structures and functions for shuffle (alltoall).
"""
import os
from collections import namedtuple
import numba
import numpy as np
from numba import generated_jit
from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.array_item_arr_ext import offset_type
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import convert_len_arr_to_offset, convert_len_arr_to_offset32, get_bit_bitmap, get_data_ptr, get_null_bitmap_ptr, get_offset_ptr, get_str_arr_item_length, num_total_chars, print_str_arr, set_bit_to, string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.timsort import getitem_arr_tup, setitem_arr_tup
from bodo.utils.utils import alloc_arr_tup, get_ctypes_ptr, numba_to_c_type
PreShuffleMeta = namedtuple('PreShuffleMeta',
    'send_counts, send_counts_char_tup, send_arr_lens_tup, send_arr_nulls_tup')
ShuffleMeta = namedtuple('ShuffleMeta',
    'send_counts, recv_counts, n_send, n_out, send_disp, recv_disp, send_disp_nulls, recv_disp_nulls, tmp_offset, send_buff_tup, out_arr_tup, send_counts_char_tup, recv_counts_char_tup, send_arr_lens_tup, send_arr_nulls_tup, send_arr_chars_tup, send_disp_char_tup, recv_disp_char_tup, tmp_offset_char_tup, send_arr_chars_arr_tup'
    )


def alloc_pre_shuffle_metadata(arr, data, n_pes, is_contig):
    return PreShuffleMeta(np.zeros(n_pes, np.int32), ())


@overload(alloc_pre_shuffle_metadata, no_unliteral=True)
def alloc_pre_shuffle_metadata_overload(key_arrs, data, n_pes, is_contig):
    jxm__ibgt = 'def f(key_arrs, data, n_pes, is_contig):\n'
    jxm__ibgt += '  send_counts = np.zeros(n_pes, np.int32)\n'
    gur__mfrs = len(key_arrs.types)
    hnl__cmweo = gur__mfrs + len(data.types)
    for i, zvvrg__qcpn in enumerate(key_arrs.types + data.types):
        jxm__ibgt += '  arr = key_arrs[{}]\n'.format(i
            ) if i < gur__mfrs else '  arr = data[{}]\n'.format(i - gur__mfrs)
        if zvvrg__qcpn in [string_array_type, binary_array_type]:
            jxm__ibgt += ('  send_counts_char_{} = np.zeros(n_pes, np.int32)\n'
                .format(i))
            jxm__ibgt += ('  send_arr_lens_{} = np.empty(0, np.uint32)\n'.
                format(i))
            jxm__ibgt += '  if is_contig:\n'
            jxm__ibgt += (
                '    send_arr_lens_{} = np.empty(len(arr), np.uint32)\n'.
                format(i))
        else:
            jxm__ibgt += '  send_counts_char_{} = None\n'.format(i)
            jxm__ibgt += '  send_arr_lens_{} = None\n'.format(i)
        if is_null_masked_type(zvvrg__qcpn):
            jxm__ibgt += ('  send_arr_nulls_{} = np.empty(0, np.uint8)\n'.
                format(i))
            jxm__ibgt += '  if is_contig:\n'
            jxm__ibgt += '    n_bytes = (len(arr) + 7) >> 3\n'
            jxm__ibgt += (
                '    send_arr_nulls_{} = np.full(n_bytes + 2 * n_pes, 255, np.uint8)\n'
                .format(i))
        else:
            jxm__ibgt += '  send_arr_nulls_{} = None\n'.format(i)
    wywlt__gklo = ', '.join('send_counts_char_{}'.format(i) for i in range(
        hnl__cmweo))
    omj__ickn = ', '.join('send_arr_lens_{}'.format(i) for i in range(
        hnl__cmweo))
    nbwuj__bcq = ', '.join('send_arr_nulls_{}'.format(i) for i in range(
        hnl__cmweo))
    oicy__ikpug = ',' if hnl__cmweo == 1 else ''
    jxm__ibgt += (
        '  return PreShuffleMeta(send_counts, ({}{}), ({}{}), ({}{}))\n'.
        format(wywlt__gklo, oicy__ikpug, omj__ickn, oicy__ikpug, nbwuj__bcq,
        oicy__ikpug))
    oue__ywogq = {}
    exec(jxm__ibgt, {'np': np, 'PreShuffleMeta': PreShuffleMeta}, oue__ywogq)
    fygxz__jcxrc = oue__ywogq['f']
    return fygxz__jcxrc


def update_shuffle_meta(pre_shuffle_meta, node_id, ind, key_arrs, data,
    is_contig=True, padded_bits=0):
    pre_shuffle_meta.send_counts[node_id] += 1


@overload(update_shuffle_meta, no_unliteral=True)
def update_shuffle_meta_overload(pre_shuffle_meta, node_id, ind, key_arrs,
    data, is_contig=True, padded_bits=0):
    lhwv__ncr = 'BODO_DEBUG_LEVEL'
    ypo__qdd = 0
    try:
        ypo__qdd = int(os.environ[lhwv__ncr])
    except:
        pass
    jxm__ibgt = """def f(pre_shuffle_meta, node_id, ind, key_arrs, data, is_contig=True, padded_bits=0):
"""
    jxm__ibgt += '  pre_shuffle_meta.send_counts[node_id] += 1\n'
    if ypo__qdd > 0:
        jxm__ibgt += ('  if pre_shuffle_meta.send_counts[node_id] >= {}:\n'
            .format(bodo.libs.distributed_api.INT_MAX))
        jxm__ibgt += "    print('large shuffle error')\n"
    gur__mfrs = len(key_arrs.types)
    for i, zvvrg__qcpn in enumerate(key_arrs.types + data.types):
        if zvvrg__qcpn in (string_type, string_array_type, bytes_type,
            binary_array_type):
            arr = 'key_arrs[{}]'.format(i
                ) if i < gur__mfrs else 'data[{}]'.format(i - gur__mfrs)
            jxm__ibgt += ('  n_chars = get_str_arr_item_length({}, ind)\n'.
                format(arr))
            jxm__ibgt += (
                '  pre_shuffle_meta.send_counts_char_tup[{}][node_id] += n_chars\n'
                .format(i))
            if ypo__qdd > 0:
                jxm__ibgt += (
                    '  if pre_shuffle_meta.send_counts_char_tup[{}][node_id] >= {}:\n'
                    .format(i, bodo.libs.distributed_api.INT_MAX))
                jxm__ibgt += "    print('large shuffle error')\n"
            jxm__ibgt += '  if is_contig:\n'
            jxm__ibgt += (
                '    pre_shuffle_meta.send_arr_lens_tup[{}][ind] = n_chars\n'
                .format(i))
        if is_null_masked_type(zvvrg__qcpn):
            jxm__ibgt += '  if is_contig:\n'
            jxm__ibgt += (
                '    out_bitmap = pre_shuffle_meta.send_arr_nulls_tup[{}].ctypes\n'
                .format(i))
            if i < gur__mfrs:
                jxm__ibgt += ('    bit_val = get_mask_bit(key_arrs[{}], ind)\n'
                    .format(i))
            else:
                jxm__ibgt += ('    bit_val = get_mask_bit(data[{}], ind)\n'
                    .format(i - gur__mfrs))
            jxm__ibgt += (
                '    set_bit_to(out_bitmap, padded_bits + ind, bit_val)\n')
    oue__ywogq = {}
    exec(jxm__ibgt, {'set_bit_to': set_bit_to, 'get_bit_bitmap':
        get_bit_bitmap, 'get_null_bitmap_ptr': get_null_bitmap_ptr,
        'getitem_arr_tup': getitem_arr_tup, 'get_mask_bit': get_mask_bit,
        'get_str_arr_item_length': get_str_arr_item_length}, oue__ywogq)
    saf__uzq = oue__ywogq['f']
    return saf__uzq


@numba.njit
def calc_disp_nulls(arr):
    qhcov__fda = np.empty_like(arr)
    qhcov__fda[0] = 0
    for i in range(1, len(arr)):
        xzsr__ugnz = arr[i - 1] + 7 >> 3
        qhcov__fda[i] = qhcov__fda[i - 1] + xzsr__ugnz
    return qhcov__fda


def finalize_shuffle_meta(arrs, data, pre_shuffle_meta, n_pes, is_contig,
    init_vals=()):
    return ShuffleMeta()


@overload(finalize_shuffle_meta, no_unliteral=True)
def finalize_shuffle_meta_overload(key_arrs, data, pre_shuffle_meta, n_pes,
    is_contig, init_vals=()):
    jxm__ibgt = (
        'def f(key_arrs, data, pre_shuffle_meta, n_pes, is_contig, init_vals=()):\n'
        )
    jxm__ibgt += '  send_counts = pre_shuffle_meta.send_counts\n'
    jxm__ibgt += '  recv_counts = np.empty(n_pes, np.int32)\n'
    jxm__ibgt += '  tmp_offset = np.zeros(n_pes, np.int32)\n'
    jxm__ibgt += (
        '  bodo.libs.distributed_api.alltoall(send_counts, recv_counts, 1)\n')
    jxm__ibgt += '  n_out = recv_counts.sum()\n'
    jxm__ibgt += '  n_send = send_counts.sum()\n'
    jxm__ibgt += '  send_disp = bodo.ir.join.calc_disp(send_counts)\n'
    jxm__ibgt += '  recv_disp = bodo.ir.join.calc_disp(recv_counts)\n'
    jxm__ibgt += '  send_disp_nulls = calc_disp_nulls(send_counts)\n'
    jxm__ibgt += '  recv_disp_nulls = calc_disp_nulls(recv_counts)\n'
    gur__mfrs = len(key_arrs.types)
    hnl__cmweo = len(key_arrs.types + data.types)
    for i, zvvrg__qcpn in enumerate(key_arrs.types + data.types):
        jxm__ibgt += '  arr = key_arrs[{}]\n'.format(i
            ) if i < gur__mfrs else '  arr = data[{}]\n'.format(i - gur__mfrs)
        if zvvrg__qcpn in [string_array_type, binary_array_type]:
            if zvvrg__qcpn == string_array_type:
                cgvi__yki = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
            else:
                cgvi__yki = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
            jxm__ibgt += '  send_buff_{} = None\n'.format(i)
            jxm__ibgt += (
                '  send_counts_char_{} = pre_shuffle_meta.send_counts_char_tup[{}]\n'
                .format(i, i))
            jxm__ibgt += ('  recv_counts_char_{} = np.empty(n_pes, np.int32)\n'
                .format(i))
            jxm__ibgt += (
                """  bodo.libs.distributed_api.alltoall(send_counts_char_{}, recv_counts_char_{}, 1)
"""
                .format(i, i))
            jxm__ibgt += '  n_all_chars = recv_counts_char_{}.sum()\n'.format(i
                )
            jxm__ibgt += '  out_arr_{} = {}(n_out, n_all_chars)\n'.format(i,
                cgvi__yki)
            jxm__ibgt += (
                '  send_disp_char_{} = bodo.ir.join.calc_disp(send_counts_char_{})\n'
                .format(i, i))
            jxm__ibgt += (
                '  recv_disp_char_{} = bodo.ir.join.calc_disp(recv_counts_char_{})\n'
                .format(i, i))
            jxm__ibgt += ('  tmp_offset_char_{} = np.zeros(n_pes, np.int32)\n'
                .format(i))
            jxm__ibgt += (
                '  send_arr_lens_{} = pre_shuffle_meta.send_arr_lens_tup[{}]\n'
                .format(i, i))
            jxm__ibgt += ('  send_arr_chars_arr_{} = np.empty(0, np.uint8)\n'
                .format(i))
            jxm__ibgt += (
                '  send_arr_chars_{} = get_ctypes_ptr(get_data_ptr(arr))\n'
                .format(i))
            jxm__ibgt += '  if not is_contig:\n'
            jxm__ibgt += (
                '    send_arr_lens_{} = np.empty(n_send, np.uint32)\n'.
                format(i))
            jxm__ibgt += ('    s_n_all_chars = send_counts_char_{}.sum()\n'
                .format(i))
            jxm__ibgt += (
                '    send_arr_chars_arr_{} = np.empty(s_n_all_chars, np.uint8)\n'
                .format(i))
            jxm__ibgt += (
                '    send_arr_chars_{} = get_ctypes_ptr(send_arr_chars_arr_{}.ctypes)\n'
                .format(i, i))
        else:
            assert isinstance(zvvrg__qcpn, (types.Array, IntegerArrayType,
                BooleanArrayType, bodo.CategoricalArrayType))
            jxm__ibgt += (
                '  out_arr_{} = bodo.utils.utils.alloc_type(n_out, arr)\n'.
                format(i))
            jxm__ibgt += '  send_buff_{} = arr\n'.format(i)
            jxm__ibgt += '  if not is_contig:\n'
            if i >= gur__mfrs and init_vals != ():
                jxm__ibgt += (
                    """    send_buff_{} = bodo.utils.utils.full_type(n_send, init_vals[{}], arr)
"""
                    .format(i, i - gur__mfrs))
            else:
                jxm__ibgt += (
                    '    send_buff_{} = bodo.utils.utils.alloc_type(n_send, arr)\n'
                    .format(i))
            jxm__ibgt += '  send_counts_char_{} = None\n'.format(i)
            jxm__ibgt += '  recv_counts_char_{} = None\n'.format(i)
            jxm__ibgt += '  send_arr_lens_{} = None\n'.format(i)
            jxm__ibgt += '  send_arr_chars_{} = None\n'.format(i)
            jxm__ibgt += '  send_disp_char_{} = None\n'.format(i)
            jxm__ibgt += '  recv_disp_char_{} = None\n'.format(i)
            jxm__ibgt += '  tmp_offset_char_{} = None\n'.format(i)
            jxm__ibgt += '  send_arr_chars_arr_{} = None\n'.format(i)
        if is_null_masked_type(zvvrg__qcpn):
            jxm__ibgt += (
                '  send_arr_nulls_{} = pre_shuffle_meta.send_arr_nulls_tup[{}]\n'
                .format(i, i))
            jxm__ibgt += '  if not is_contig:\n'
            jxm__ibgt += '    n_bytes = (n_send + 7) >> 3\n'
            jxm__ibgt += (
                '    send_arr_nulls_{} = np.full(n_bytes + 2 * n_pes, 255, np.uint8)\n'
                .format(i))
        else:
            jxm__ibgt += '  send_arr_nulls_{} = None\n'.format(i)
    mjc__pad = ', '.join('send_buff_{}'.format(i) for i in range(hnl__cmweo))
    ogi__rhow = ', '.join('out_arr_{}'.format(i) for i in range(hnl__cmweo))
    qpm__wornr = ',' if hnl__cmweo == 1 else ''
    qtwm__rda = ', '.join('send_counts_char_{}'.format(i) for i in range(
        hnl__cmweo))
    edfz__fng = ', '.join('recv_counts_char_{}'.format(i) for i in range(
        hnl__cmweo))
    ylqem__azqk = ', '.join('send_arr_lens_{}'.format(i) for i in range(
        hnl__cmweo))
    irort__lnxma = ', '.join('send_arr_nulls_{}'.format(i) for i in range(
        hnl__cmweo))
    azp__wkqqm = ', '.join('send_arr_chars_{}'.format(i) for i in range(
        hnl__cmweo))
    xcql__ruqb = ', '.join('send_disp_char_{}'.format(i) for i in range(
        hnl__cmweo))
    jurb__uacyb = ', '.join('recv_disp_char_{}'.format(i) for i in range(
        hnl__cmweo))
    foskl__bqucq = ', '.join('tmp_offset_char_{}'.format(i) for i in range(
        hnl__cmweo))
    ciw__phlk = ', '.join('send_arr_chars_arr_{}'.format(i) for i in range(
        hnl__cmweo))
    jxm__ibgt += (
        """  return ShuffleMeta(send_counts, recv_counts, n_send, n_out, send_disp, recv_disp, send_disp_nulls, recv_disp_nulls, tmp_offset, ({}{}), ({}{}), ({}{}), ({}{}), ({}{}), ({}{}), ({}{}), ({}{}), ({}{}), ({}{}), ({}{}), )
"""
        .format(mjc__pad, qpm__wornr, ogi__rhow, qpm__wornr, qtwm__rda,
        qpm__wornr, edfz__fng, qpm__wornr, ylqem__azqk, qpm__wornr,
        irort__lnxma, qpm__wornr, azp__wkqqm, qpm__wornr, xcql__ruqb,
        qpm__wornr, jurb__uacyb, qpm__wornr, foskl__bqucq, qpm__wornr,
        ciw__phlk, qpm__wornr))
    oue__ywogq = {}
    exec(jxm__ibgt, {'np': np, 'bodo': bodo, 'num_total_chars':
        num_total_chars, 'get_data_ptr': get_data_ptr, 'ShuffleMeta':
        ShuffleMeta, 'get_ctypes_ptr': get_ctypes_ptr, 'calc_disp_nulls':
        calc_disp_nulls}, oue__ywogq)
    mspaj__rdntt = oue__ywogq['f']
    return mspaj__rdntt


def alltoallv_tup(arrs, shuffle_meta, key_arrs):
    return arrs


@overload(alltoallv_tup, no_unliteral=True)
def alltoallv_tup_overload(arrs, meta, key_arrs):
    gur__mfrs = len(key_arrs.types)
    jxm__ibgt = 'def f(arrs, meta, key_arrs):\n'
    if any(is_null_masked_type(t) for t in arrs.types):
        jxm__ibgt += (
            '  send_counts_nulls = np.empty(len(meta.send_counts), np.int32)\n'
            )
        jxm__ibgt += '  for i in range(len(meta.send_counts)):\n'
        jxm__ibgt += (
            '    send_counts_nulls[i] = (meta.send_counts[i] + 7) >> 3\n')
        jxm__ibgt += (
            '  recv_counts_nulls = np.empty(len(meta.recv_counts), np.int32)\n'
            )
        jxm__ibgt += '  for i in range(len(meta.recv_counts)):\n'
        jxm__ibgt += (
            '    recv_counts_nulls[i] = (meta.recv_counts[i] + 7) >> 3\n')
        jxm__ibgt += (
            '  tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)\n')
    jxm__ibgt += '  lens = np.empty(meta.n_out, np.uint32)\n'
    for i, zvvrg__qcpn in enumerate(arrs.types):
        if isinstance(zvvrg__qcpn, (types.Array, IntegerArrayType,
            BooleanArrayType, bodo.CategoricalArrayType)):
            jxm__ibgt += (
                """  bodo.libs.distributed_api.alltoallv(meta.send_buff_tup[{}], meta.out_arr_tup[{}], meta.send_counts,meta.recv_counts, meta.send_disp, meta.recv_disp)
"""
                .format(i, i))
        else:
            assert zvvrg__qcpn in [string_array_type, binary_array_type]
            jxm__ibgt += (
                '  offset_ptr_{} = get_offset_ptr(meta.out_arr_tup[{}])\n'.
                format(i, i))
            if offset_type.bitwidth == 32:
                jxm__ibgt += (
                    """  bodo.libs.distributed_api.c_alltoallv(meta.send_arr_lens_tup[{}].ctypes, offset_ptr_{}, meta.send_counts.ctypes, meta.recv_counts.ctypes, meta.send_disp.ctypes, meta.recv_disp.ctypes, int32_typ_enum)
"""
                    .format(i, i))
            else:
                jxm__ibgt += (
                    """  bodo.libs.distributed_api.c_alltoallv(meta.send_arr_lens_tup[{}].ctypes, lens.ctypes, meta.send_counts.ctypes, meta.recv_counts.ctypes, meta.send_disp.ctypes, meta.recv_disp.ctypes, int32_typ_enum)
"""
                    .format(i))
            jxm__ibgt += (
                """  bodo.libs.distributed_api.c_alltoallv(meta.send_arr_chars_tup[{}], get_data_ptr(meta.out_arr_tup[{}]), meta.send_counts_char_tup[{}].ctypes,meta.recv_counts_char_tup[{}].ctypes, meta.send_disp_char_tup[{}].ctypes,meta.recv_disp_char_tup[{}].ctypes, char_typ_enum)
"""
                .format(i, i, i, i, i, i))
            if offset_type.bitwidth == 32:
                jxm__ibgt += (
                    '  convert_len_arr_to_offset32(offset_ptr_{}, meta.n_out)\n'
                    .format(i))
            else:
                jxm__ibgt += (
                    """  convert_len_arr_to_offset(lens.ctypes, offset_ptr_{}, meta.n_out)
"""
                    .format(i))
        if is_null_masked_type(zvvrg__qcpn):
            jxm__ibgt += (
                '  null_bitmap_ptr_{} = get_arr_null_ptr(meta.out_arr_tup[{}])\n'
                .format(i, i))
            jxm__ibgt += (
                """  bodo.libs.distributed_api.c_alltoallv(meta.send_arr_nulls_tup[{}].ctypes, tmp_null_bytes.ctypes, send_counts_nulls.ctypes, recv_counts_nulls.ctypes, meta.send_disp_nulls.ctypes, meta.recv_disp_nulls.ctypes, char_typ_enum)
"""
                .format(i))
            jxm__ibgt += (
                """  copy_gathered_null_bytes(null_bitmap_ptr_{}, tmp_null_bytes, recv_counts_nulls, meta.recv_counts)
"""
                .format(i))
    jxm__ibgt += '  return ({}{})\n'.format(','.join([
        'meta.out_arr_tup[{}]'.format(i) for i in range(arrs.count)]), ',' if
        arrs.count == 1 else '')
    wkcqu__gglp = np.int32(numba_to_c_type(types.int32))
    rwuut__oyw = np.int32(numba_to_c_type(types.uint8))
    oue__ywogq = {}
    exec(jxm__ibgt, {'np': np, 'bodo': bodo, 'get_offset_ptr':
        get_offset_ptr, 'get_data_ptr': get_data_ptr, 'int32_typ_enum':
        wkcqu__gglp, 'char_typ_enum': rwuut__oyw,
        'convert_len_arr_to_offset': convert_len_arr_to_offset,
        'convert_len_arr_to_offset32': convert_len_arr_to_offset32,
        'copy_gathered_null_bytes': bodo.libs.distributed_api.
        copy_gathered_null_bytes, 'get_arr_null_ptr': get_arr_null_ptr,
        'print_str_arr': print_str_arr}, oue__ywogq)
    rzfci__pxmo = oue__ywogq['f']
    return rzfci__pxmo


def shuffle_with_index_impl(key_arrs, node_arr, data):
    n_pes = bodo.libs.distributed_api.get_size()
    pre_shuffle_meta = alloc_pre_shuffle_metadata(key_arrs, data, n_pes, False)
    eqmjz__cojj = len(key_arrs[0])
    orig_indices = np.arange(eqmjz__cojj)
    lfhbn__zpekp = np.empty(eqmjz__cojj, np.int32)
    for i in range(eqmjz__cojj):
        val = getitem_arr_tup_single(key_arrs, i)
        node_id = node_arr[i]
        lfhbn__zpekp[i] = node_id
        update_shuffle_meta(pre_shuffle_meta, node_id, i, key_arrs, data, False
            )
    shuffle_meta = finalize_shuffle_meta(key_arrs, data, pre_shuffle_meta,
        n_pes, False)
    for i in range(eqmjz__cojj):
        val = getitem_arr_tup_single(key_arrs, i)
        node_id = lfhbn__zpekp[i]
        ornj__clzdr = bodo.ir.join.write_send_buff(shuffle_meta, node_id, i,
            key_arrs, data)
        orig_indices[ornj__clzdr] = i
        shuffle_meta.tmp_offset[node_id] += 1
    recvs = alltoallv_tup(key_arrs + data, shuffle_meta, key_arrs)
    ajs__cdrrj = _get_keys_tup(recvs, key_arrs)
    nzt__lhqir = _get_data_tup(recvs, key_arrs)
    return ajs__cdrrj, nzt__lhqir, orig_indices, shuffle_meta


@generated_jit(nopython=True, cache=True)
def shuffle_with_index(key_arrs, node_arr, data):
    return shuffle_with_index_impl


@numba.njit(cache=True)
def reverse_shuffle(data, orig_indices, shuffle_meta):
    ogi__rhow = alloc_arr_tup(shuffle_meta.n_send, data)
    swurk__mome = ShuffleMeta(shuffle_meta.recv_counts, shuffle_meta.
        send_counts, shuffle_meta.n_out, shuffle_meta.n_send, shuffle_meta.
        recv_disp, shuffle_meta.send_disp, shuffle_meta.recv_disp_nulls,
        shuffle_meta.send_disp_nulls, shuffle_meta.tmp_offset, data,
        ogi__rhow, shuffle_meta.recv_counts_char_tup, shuffle_meta.
        send_counts_char_tup, shuffle_meta.send_arr_lens_tup, shuffle_meta.
        send_arr_nulls_tup, shuffle_meta.send_arr_chars_tup, shuffle_meta.
        recv_disp_char_tup, shuffle_meta.send_disp_char_tup, shuffle_meta.
        tmp_offset_char_tup, shuffle_meta.send_arr_chars_arr_tup)
    ogi__rhow = alltoallv_tup(data, swurk__mome, ())
    lrwq__lgjr = alloc_arr_tup(shuffle_meta.n_send, data)
    for i in range(len(orig_indices)):
        setitem_arr_tup(lrwq__lgjr, orig_indices[i], getitem_arr_tup(
            ogi__rhow, i))
    return lrwq__lgjr


def _get_keys_tup(recvs, key_arrs):
    return recvs[:len(key_arrs)]


@overload(_get_keys_tup, no_unliteral=True)
def _get_keys_tup_overload(recvs, key_arrs):
    gur__mfrs = len(key_arrs.types)
    jxm__ibgt = 'def f(recvs, key_arrs):\n'
    zrsk__mopht = ','.join('recvs[{}]'.format(i) for i in range(gur__mfrs))
    jxm__ibgt += '  return ({}{})\n'.format(zrsk__mopht, ',' if gur__mfrs ==
        1 else '')
    oue__ywogq = {}
    exec(jxm__ibgt, {}, oue__ywogq)
    ifvmn__eqk = oue__ywogq['f']
    return ifvmn__eqk


def _get_data_tup(recvs, key_arrs):
    return recvs[len(key_arrs):]


@overload(_get_data_tup, no_unliteral=True)
def _get_data_tup_overload(recvs, key_arrs):
    gur__mfrs = len(key_arrs.types)
    hnl__cmweo = len(recvs.types)
    laevp__oeqi = hnl__cmweo - gur__mfrs
    jxm__ibgt = 'def f(recvs, key_arrs):\n'
    zrsk__mopht = ','.join('recvs[{}]'.format(i) for i in range(gur__mfrs,
        hnl__cmweo))
    jxm__ibgt += '  return ({}{})\n'.format(zrsk__mopht, ',' if laevp__oeqi ==
        1 else '')
    oue__ywogq = {}
    exec(jxm__ibgt, {}, oue__ywogq)
    ifvmn__eqk = oue__ywogq['f']
    return ifvmn__eqk


def getitem_arr_tup_single(arrs, i):
    return arrs[0][i]


@overload(getitem_arr_tup_single, no_unliteral=True)
def getitem_arr_tup_single_overload(arrs, i):
    if len(arrs.types) == 1:
        return lambda arrs, i: arrs[0][i]
    return lambda arrs, i: getitem_arr_tup(arrs, i)


def val_to_tup(val):
    return val,


@overload(val_to_tup, no_unliteral=True)
def val_to_tup_overload(val):
    if isinstance(val, types.BaseTuple):
        return lambda val: val
    return lambda val: (val,)


def is_null_masked_type(t):
    return t in (string_type, string_array_type, bytes_type,
        binary_array_type, boolean_array) or isinstance(t, IntegerArrayType)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_mask_bit(arr, i):
    if arr in [string_array_type, binary_array_type]:
        return lambda arr, i: get_bit_bitmap(get_null_bitmap_ptr(arr), i)
    assert isinstance(arr, IntegerArrayType) or arr == boolean_array
    return lambda arr, i: bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr.
        _null_bitmap, i)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_arr_null_ptr(arr):
    if arr in [string_array_type, binary_array_type]:
        return lambda arr: get_null_bitmap_ptr(arr)
    assert isinstance(arr, IntegerArrayType) or arr == boolean_array
    return lambda arr: arr._null_bitmap.ctypes
