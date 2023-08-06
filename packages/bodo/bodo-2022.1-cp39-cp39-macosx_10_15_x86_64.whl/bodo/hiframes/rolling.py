"""implementations of rolling window functions (sequential and parallel)
"""
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.core.imputils import impl_ret_borrowed
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_builtin, overload, register_jitable
import bodo
from bodo.libs.distributed_api import Reduce_Type
from bodo.utils.typing import BodoError, get_overload_const_func, get_overload_const_str, is_const_func_type, is_overload_constant_bool, is_overload_constant_str, is_overload_none, is_overload_true
from bodo.utils.utils import unliteral_all
supported_rolling_funcs = ('sum', 'mean', 'var', 'std', 'count', 'median',
    'min', 'max', 'cov', 'corr', 'apply')
unsupported_rolling_methods = ['skew', 'kurt', 'aggregate', 'quantile', 'sem']


def rolling_fixed(arr, win):
    return arr


def rolling_variable(arr, on_arr, win):
    return arr


def rolling_cov(arr, arr2, win):
    return arr


def rolling_corr(arr, arr2, win):
    return arr


@infer_global(rolling_cov)
@infer_global(rolling_corr)
class RollingCovType(AbstractTemplate):

    def generic(self, args, kws):
        arr = args[0]
        xkwlc__grp = arr.copy(dtype=types.float64)
        return signature(xkwlc__grp, *unliteral_all(args))


@lower_builtin(rolling_corr, types.VarArg(types.Any))
@lower_builtin(rolling_cov, types.VarArg(types.Any))
def lower_rolling_corr_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


@overload(rolling_fixed, no_unliteral=True)
def overload_rolling_fixed(arr, index_arr, win, minp, center, fname, raw=
    True, parallel=False):
    assert is_overload_constant_bool(raw
        ), 'raw argument should be constant bool'
    if is_const_func_type(fname):
        func = _get_apply_func(fname)
        return (lambda arr, index_arr, win, minp, center, fname, raw=True,
            parallel=False: roll_fixed_apply(arr, index_arr, win, minp,
            center, parallel, func, raw))
    assert is_overload_constant_str(fname)
    ooo__iohf = get_overload_const_str(fname)
    if ooo__iohf not in ('sum', 'mean', 'var', 'std', 'count', 'median',
        'min', 'max'):
        raise BodoError('invalid rolling (fixed window) function {}'.format
            (ooo__iohf))
    if ooo__iohf in ('median', 'min', 'max'):
        njdfj__dkef = 'def kernel_func(A):\n'
        njdfj__dkef += '  if np.isnan(A).sum() != 0: return np.nan\n'
        njdfj__dkef += '  return np.{}(A)\n'.format(ooo__iohf)
        qwj__iute = {}
        exec(njdfj__dkef, {'np': np}, qwj__iute)
        kernel_func = register_jitable(qwj__iute['kernel_func'])
        return (lambda arr, index_arr, win, minp, center, fname, raw=True,
            parallel=False: roll_fixed_apply(arr, index_arr, win, minp,
            center, parallel, kernel_func))
    init_kernel, add_kernel, remove_kernel, calc_kernel = linear_kernels[
        ooo__iohf]
    return (lambda arr, index_arr, win, minp, center, fname, raw=True,
        parallel=False: roll_fixed_linear_generic(arr, win, minp, center,
        parallel, init_kernel, add_kernel, remove_kernel, calc_kernel))


@overload(rolling_variable, no_unliteral=True)
def overload_rolling_variable(arr, on_arr, index_arr, win, minp, center,
    fname, raw=True, parallel=False):
    assert is_overload_constant_bool(raw)
    if is_const_func_type(fname):
        func = _get_apply_func(fname)
        return (lambda arr, on_arr, index_arr, win, minp, center, fname,
            raw=True, parallel=False: roll_variable_apply(arr, on_arr,
            index_arr, win, minp, center, parallel, func, raw))
    assert is_overload_constant_str(fname)
    ooo__iohf = get_overload_const_str(fname)
    if ooo__iohf not in ('sum', 'mean', 'var', 'std', 'count', 'median',
        'min', 'max'):
        raise BodoError('invalid rolling (variable window) function {}'.
            format(ooo__iohf))
    if ooo__iohf in ('median', 'min', 'max'):
        njdfj__dkef = 'def kernel_func(A):\n'
        njdfj__dkef += '  arr  = dropna(A)\n'
        njdfj__dkef += '  if len(arr) == 0: return np.nan\n'
        njdfj__dkef += '  return np.{}(arr)\n'.format(ooo__iohf)
        qwj__iute = {}
        exec(njdfj__dkef, {'np': np, 'dropna': _dropna}, qwj__iute)
        kernel_func = register_jitable(qwj__iute['kernel_func'])
        return (lambda arr, on_arr, index_arr, win, minp, center, fname,
            raw=True, parallel=False: roll_variable_apply(arr, on_arr,
            index_arr, win, minp, center, parallel, kernel_func))
    init_kernel, add_kernel, remove_kernel, calc_kernel = linear_kernels[
        ooo__iohf]
    return (lambda arr, on_arr, index_arr, win, minp, center, fname, raw=
        True, parallel=False: roll_var_linear_generic(arr, on_arr, win,
        minp, center, parallel, init_kernel, add_kernel, remove_kernel,
        calc_kernel))


def _get_apply_func(f_type):
    func = get_overload_const_func(f_type, None)
    return bodo.compiler.udf_jit(func)


comm_border_tag = 22


@register_jitable
def roll_fixed_linear_generic(in_arr, win, minp, center, parallel,
    init_data, add_obs, remove_obs, calc_out):
    _validate_roll_fixed_args(win, minp)
    in_arr = prep_values(in_arr)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    if parallel:
        halo_size = np.int32(win // 2) if center else np.int32(win - 1)
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data(in_arr, win, minp, center, rank,
                n_pes, init_data, add_obs, remove_obs, calc_out)
        eulj__wsqm = _border_icomm(in_arr, rank, n_pes, halo_size, True, center
            )
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            vqoz__eqho) = eulj__wsqm
    output, data = roll_fixed_linear_generic_seq(in_arr, win, minp, center,
        init_data, add_obs, remove_obs, calc_out)
    if parallel:
        _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, center)
        if center and rank != n_pes - 1:
            bodo.libs.distributed_api.wait(vqoz__eqho, True)
            for xvevg__akld in range(0, halo_size):
                data = add_obs(r_recv_buff[xvevg__akld], *data)
                kskx__xegdf = in_arr[N + xvevg__akld - win]
                data = remove_obs(kskx__xegdf, *data)
                output[N + xvevg__akld - offset] = calc_out(minp, *data)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            data = init_data()
            for xvevg__akld in range(0, halo_size):
                data = add_obs(l_recv_buff[xvevg__akld], *data)
            for xvevg__akld in range(0, win - 1):
                data = add_obs(in_arr[xvevg__akld], *data)
                if xvevg__akld > offset:
                    kskx__xegdf = l_recv_buff[xvevg__akld - offset - 1]
                    data = remove_obs(kskx__xegdf, *data)
                if xvevg__akld >= offset:
                    output[xvevg__akld - offset] = calc_out(minp, *data)
    return output


@register_jitable
def roll_fixed_linear_generic_seq(in_arr, win, minp, center, init_data,
    add_obs, remove_obs, calc_out):
    data = init_data()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    output = np.empty(N, dtype=np.float64)
    ommej__tcgom = max(minp, 1) - 1
    ommej__tcgom = min(ommej__tcgom, N)
    for xvevg__akld in range(0, ommej__tcgom):
        data = add_obs(in_arr[xvevg__akld], *data)
        if xvevg__akld >= offset:
            output[xvevg__akld - offset] = calc_out(minp, *data)
    for xvevg__akld in range(ommej__tcgom, N):
        val = in_arr[xvevg__akld]
        data = add_obs(val, *data)
        if xvevg__akld > win - 1:
            kskx__xegdf = in_arr[xvevg__akld - win]
            data = remove_obs(kskx__xegdf, *data)
        output[xvevg__akld - offset] = calc_out(minp, *data)
    ytup__eee = data
    for xvevg__akld in range(N, N + offset):
        if xvevg__akld > win - 1:
            kskx__xegdf = in_arr[xvevg__akld - win]
            data = remove_obs(kskx__xegdf, *data)
        output[xvevg__akld - offset] = calc_out(minp, *data)
    return output, ytup__eee


def roll_fixed_apply(in_arr, index_arr, win, minp, center, parallel,
    kernel_func, raw=True):
    pass


@overload(roll_fixed_apply, no_unliteral=True)
def overload_roll_fixed_apply(in_arr, index_arr, win, minp, center,
    parallel, kernel_func, raw=True):
    assert is_overload_constant_bool(raw)
    return roll_fixed_apply_impl


def roll_fixed_apply_impl(in_arr, index_arr, win, minp, center, parallel,
    kernel_func, raw=True):
    _validate_roll_fixed_args(win, minp)
    in_arr = prep_values(in_arr)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    index_arr = fix_index_arr(index_arr)
    if parallel:
        halo_size = np.int32(win // 2) if center else np.int32(win - 1)
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data_apply(in_arr, index_arr, win, minp,
                center, rank, n_pes, kernel_func, raw)
        eulj__wsqm = _border_icomm(in_arr, rank, n_pes, halo_size, True, center
            )
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            vqoz__eqho) = eulj__wsqm
        if raw == False:
            yew__hwpo = _border_icomm(index_arr, rank, n_pes, halo_size, 
                True, center)
            (l_recv_buff_idx, r_recv_buff_idx, ifl__uklss, hszyc__kylf,
                qhi__cpy, nkg__yoh) = yew__hwpo
    output = roll_fixed_apply_seq(in_arr, index_arr, win, minp, center,
        kernel_func, raw)
    if parallel:
        _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, center)
        if raw == False:
            _border_send_wait(hszyc__kylf, ifl__uklss, rank, n_pes, True,
                center)
        if center and rank != n_pes - 1:
            bodo.libs.distributed_api.wait(vqoz__eqho, True)
            if raw == False:
                bodo.libs.distributed_api.wait(nkg__yoh, True)
            recv_right_compute(output, in_arr, index_arr, N, win, minp,
                offset, r_recv_buff, r_recv_buff_idx, kernel_func, raw)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            if raw == False:
                bodo.libs.distributed_api.wait(qhi__cpy, True)
            recv_left_compute(output, in_arr, index_arr, win, minp, offset,
                l_recv_buff, l_recv_buff_idx, kernel_func, raw)
    return output


def recv_right_compute(output, in_arr, index_arr, N, win, minp, offset,
    r_recv_buff, r_recv_buff_idx, kernel_func, raw):
    pass


@overload(recv_right_compute, no_unliteral=True)
def overload_recv_right_compute(output, in_arr, index_arr, N, win, minp,
    offset, r_recv_buff, r_recv_buff_idx, kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):

        def impl(output, in_arr, index_arr, N, win, minp, offset,
            r_recv_buff, r_recv_buff_idx, kernel_func, raw):
            ytup__eee = np.concatenate((in_arr[N - win + 1:], r_recv_buff))
            ktv__ppj = 0
            for xvevg__akld in range(max(N - offset, 0), N):
                data = ytup__eee[ktv__ppj:ktv__ppj + win]
                if win - np.isnan(data).sum() < minp:
                    output[xvevg__akld] = np.nan
                else:
                    output[xvevg__akld] = kernel_func(data)
                ktv__ppj += 1
        return impl

    def impl_series(output, in_arr, index_arr, N, win, minp, offset,
        r_recv_buff, r_recv_buff_idx, kernel_func, raw):
        ytup__eee = np.concatenate((in_arr[N - win + 1:], r_recv_buff))
        ihgab__whwv = np.concatenate((index_arr[N - win + 1:], r_recv_buff_idx)
            )
        ktv__ppj = 0
        for xvevg__akld in range(max(N - offset, 0), N):
            data = ytup__eee[ktv__ppj:ktv__ppj + win]
            if win - np.isnan(data).sum() < minp:
                output[xvevg__akld] = np.nan
            else:
                output[xvevg__akld] = kernel_func(pd.Series(data,
                    ihgab__whwv[ktv__ppj:ktv__ppj + win]))
            ktv__ppj += 1
    return impl_series


def recv_left_compute(output, in_arr, index_arr, win, minp, offset,
    l_recv_buff, l_recv_buff_idx, kernel_func, raw):
    pass


@overload(recv_left_compute, no_unliteral=True)
def overload_recv_left_compute(output, in_arr, index_arr, win, minp, offset,
    l_recv_buff, l_recv_buff_idx, kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):

        def impl(output, in_arr, index_arr, win, minp, offset, l_recv_buff,
            l_recv_buff_idx, kernel_func, raw):
            ytup__eee = np.concatenate((l_recv_buff, in_arr[:win - 1]))
            for xvevg__akld in range(0, win - offset - 1):
                data = ytup__eee[xvevg__akld:xvevg__akld + win]
                if win - np.isnan(data).sum() < minp:
                    output[xvevg__akld] = np.nan
                else:
                    output[xvevg__akld] = kernel_func(data)
        return impl

    def impl_series(output, in_arr, index_arr, win, minp, offset,
        l_recv_buff, l_recv_buff_idx, kernel_func, raw):
        ytup__eee = np.concatenate((l_recv_buff, in_arr[:win - 1]))
        ihgab__whwv = np.concatenate((l_recv_buff_idx, index_arr[:win - 1]))
        for xvevg__akld in range(0, win - offset - 1):
            data = ytup__eee[xvevg__akld:xvevg__akld + win]
            if win - np.isnan(data).sum() < minp:
                output[xvevg__akld] = np.nan
            else:
                output[xvevg__akld] = kernel_func(pd.Series(data,
                    ihgab__whwv[xvevg__akld:xvevg__akld + win]))
    return impl_series


def roll_fixed_apply_seq(in_arr, index_arr, win, minp, center, kernel_func,
    raw=True):
    pass


@overload(roll_fixed_apply_seq, no_unliteral=True)
def overload_roll_fixed_apply_seq(in_arr, index_arr, win, minp, center,
    kernel_func, raw=True):
    assert is_overload_constant_bool(raw), "'raw' should be constant bool"

    def roll_fixed_apply_seq_impl(in_arr, index_arr, win, minp, center,
        kernel_func, raw=True):
        N = len(in_arr)
        output = np.empty(N, dtype=np.float64)
        offset = (win - 1) // 2 if center else 0
        for xvevg__akld in range(0, N):
            start = max(xvevg__akld - win + 1 + offset, 0)
            end = min(xvevg__akld + 1 + offset, N)
            data = in_arr[start:end]
            if end - start - np.isnan(data).sum() < minp:
                output[xvevg__akld] = np.nan
            else:
                output[xvevg__akld] = apply_func(kernel_func, data,
                    index_arr, start, end, raw)
        return output
    return roll_fixed_apply_seq_impl


def apply_func(kernel_func, data, index_arr, start, end, raw):
    return kernel_func(data)


@overload(apply_func, no_unliteral=True)
def overload_apply_func(kernel_func, data, index_arr, start, end, raw):
    assert is_overload_constant_bool(raw), "'raw' should be constant bool"
    if is_overload_true(raw):
        return (lambda kernel_func, data, index_arr, start, end, raw:
            kernel_func(data))
    return lambda kernel_func, data, index_arr, start, end, raw: kernel_func(pd
        .Series(data, index_arr[start:end]))


def fix_index_arr(A):
    return A


@overload(fix_index_arr)
def overload_fix_index_arr(A):
    if is_overload_none(A):
        return lambda A: np.zeros(3)
    return lambda A: A


def get_offset_nanos(w):
    out = status = 0
    try:
        out = pd.tseries.frequencies.to_offset(w).nanos
    except:
        status = 1
    return out, status


def offset_to_nanos(w):
    return w


@overload(offset_to_nanos)
def overload_offset_to_nanos(w):
    if isinstance(w, types.Integer):
        return lambda w: w

    def impl(w):
        with numba.objmode(out='int64', status='int64'):
            out, status = get_offset_nanos(w)
        if status != 0:
            raise ValueError('Invalid offset value')
        return out
    return impl


@register_jitable
def roll_var_linear_generic(in_arr, on_arr_dt, win, minp, center, parallel,
    init_data, add_obs, remove_obs, calc_out):
    _validate_roll_var_args(minp, center)
    in_arr = prep_values(in_arr)
    win = offset_to_nanos(win)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    on_arr = cast_dt64_arr_to_int(on_arr_dt)
    N = len(in_arr)
    left_closed = False
    right_closed = True
    if parallel:
        if _is_small_for_parallel_variable(on_arr, win):
            return _handle_small_data_variable(in_arr, on_arr, win, minp,
                rank, n_pes, init_data, add_obs, remove_obs, calc_out)
        eulj__wsqm = _border_icomm_var(in_arr, on_arr, rank, n_pes, win)
        (l_recv_buff, l_recv_t_buff, r_send_req, mdht__fsc, l_recv_req,
            ntbo__oky) = eulj__wsqm
    start, end = _build_indexer(on_arr, N, win, left_closed, right_closed)
    output = roll_var_linear_generic_seq(in_arr, on_arr, win, minp, start,
        end, init_data, add_obs, remove_obs, calc_out)
    if parallel:
        _border_send_wait(r_send_req, r_send_req, rank, n_pes, True, False)
        _border_send_wait(mdht__fsc, mdht__fsc, rank, n_pes, True, False)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            bodo.libs.distributed_api.wait(ntbo__oky, True)
            num_zero_starts = 0
            for xvevg__akld in range(0, N):
                if start[xvevg__akld] != 0:
                    break
                num_zero_starts += 1
            if num_zero_starts == 0:
                return output
            recv_starts = _get_var_recv_starts(on_arr, l_recv_t_buff,
                num_zero_starts, win)
            data = init_data()
            for gzhv__sbp in range(recv_starts[0], len(l_recv_t_buff)):
                data = add_obs(l_recv_buff[gzhv__sbp], *data)
            if right_closed:
                data = add_obs(in_arr[0], *data)
            output[0] = calc_out(minp, *data)
            for xvevg__akld in range(1, num_zero_starts):
                s = recv_starts[xvevg__akld]
                tjso__jlizh = end[xvevg__akld]
                for gzhv__sbp in range(recv_starts[xvevg__akld - 1], s):
                    data = remove_obs(l_recv_buff[gzhv__sbp], *data)
                for gzhv__sbp in range(end[xvevg__akld - 1], tjso__jlizh):
                    data = add_obs(in_arr[gzhv__sbp], *data)
                output[xvevg__akld] = calc_out(minp, *data)
    return output


@register_jitable(cache=True)
def _get_var_recv_starts(on_arr, l_recv_t_buff, num_zero_starts, win):
    recv_starts = np.zeros(num_zero_starts, np.int64)
    halo_size = len(l_recv_t_buff)
    rjee__dicq = cast_dt64_arr_to_int(on_arr)
    left_closed = False
    ydahc__gbq = rjee__dicq[0] - win
    if left_closed:
        ydahc__gbq -= 1
    recv_starts[0] = halo_size
    for gzhv__sbp in range(0, halo_size):
        if l_recv_t_buff[gzhv__sbp] > ydahc__gbq:
            recv_starts[0] = gzhv__sbp
            break
    for xvevg__akld in range(1, num_zero_starts):
        ydahc__gbq = rjee__dicq[xvevg__akld] - win
        if left_closed:
            ydahc__gbq -= 1
        recv_starts[xvevg__akld] = halo_size
        for gzhv__sbp in range(recv_starts[xvevg__akld - 1], halo_size):
            if l_recv_t_buff[gzhv__sbp] > ydahc__gbq:
                recv_starts[xvevg__akld] = gzhv__sbp
                break
    return recv_starts


@register_jitable
def roll_var_linear_generic_seq(in_arr, on_arr, win, minp, start, end,
    init_data, add_obs, remove_obs, calc_out):
    N = len(in_arr)
    output = np.empty(N, np.float64)
    data = init_data()
    for gzhv__sbp in range(start[0], end[0]):
        data = add_obs(in_arr[gzhv__sbp], *data)
    output[0] = calc_out(minp, *data)
    for xvevg__akld in range(1, N):
        s = start[xvevg__akld]
        tjso__jlizh = end[xvevg__akld]
        for gzhv__sbp in range(start[xvevg__akld - 1], s):
            data = remove_obs(in_arr[gzhv__sbp], *data)
        for gzhv__sbp in range(end[xvevg__akld - 1], tjso__jlizh):
            data = add_obs(in_arr[gzhv__sbp], *data)
        output[xvevg__akld] = calc_out(minp, *data)
    return output


def roll_variable_apply(in_arr, on_arr_dt, index_arr, win, minp, center,
    parallel, kernel_func, raw=True):
    pass


@overload(roll_variable_apply, no_unliteral=True)
def overload_roll_variable_apply(in_arr, on_arr_dt, index_arr, win, minp,
    center, parallel, kernel_func, raw=True):
    assert is_overload_constant_bool(raw)
    return roll_variable_apply_impl


def roll_variable_apply_impl(in_arr, on_arr_dt, index_arr, win, minp,
    center, parallel, kernel_func, raw=True):
    _validate_roll_var_args(minp, center)
    in_arr = prep_values(in_arr)
    win = offset_to_nanos(win)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    on_arr = cast_dt64_arr_to_int(on_arr_dt)
    index_arr = fix_index_arr(index_arr)
    N = len(in_arr)
    left_closed = False
    right_closed = True
    if parallel:
        if _is_small_for_parallel_variable(on_arr, win):
            return _handle_small_data_variable_apply(in_arr, on_arr,
                index_arr, win, minp, rank, n_pes, kernel_func, raw)
        eulj__wsqm = _border_icomm_var(in_arr, on_arr, rank, n_pes, win)
        (l_recv_buff, l_recv_t_buff, r_send_req, mdht__fsc, l_recv_req,
            ntbo__oky) = eulj__wsqm
        if raw == False:
            yew__hwpo = _border_icomm_var(index_arr, on_arr, rank, n_pes, win)
            (l_recv_buff_idx, bug__ucjya, hszyc__kylf, glfo__fuauy,
                qhi__cpy, tze__fznp) = yew__hwpo
    start, end = _build_indexer(on_arr, N, win, left_closed, right_closed)
    output = roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp,
        start, end, kernel_func, raw)
    if parallel:
        _border_send_wait(r_send_req, r_send_req, rank, n_pes, True, False)
        _border_send_wait(mdht__fsc, mdht__fsc, rank, n_pes, True, False)
        if raw == False:
            _border_send_wait(hszyc__kylf, hszyc__kylf, rank, n_pes, True, 
                False)
            _border_send_wait(glfo__fuauy, glfo__fuauy, rank, n_pes, True, 
                False)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            bodo.libs.distributed_api.wait(ntbo__oky, True)
            if raw == False:
                bodo.libs.distributed_api.wait(qhi__cpy, True)
                bodo.libs.distributed_api.wait(tze__fznp, True)
            num_zero_starts = 0
            for xvevg__akld in range(0, N):
                if start[xvevg__akld] != 0:
                    break
                num_zero_starts += 1
            if num_zero_starts == 0:
                return output
            recv_starts = _get_var_recv_starts(on_arr, l_recv_t_buff,
                num_zero_starts, win)
            recv_left_var_compute(output, in_arr, index_arr,
                num_zero_starts, recv_starts, l_recv_buff, l_recv_buff_idx,
                minp, kernel_func, raw)
    return output


def recv_left_var_compute(output, in_arr, index_arr, num_zero_starts,
    recv_starts, l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
    pass


@overload(recv_left_var_compute)
def overload_recv_left_var_compute(output, in_arr, index_arr,
    num_zero_starts, recv_starts, l_recv_buff, l_recv_buff_idx, minp,
    kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):

        def impl(output, in_arr, index_arr, num_zero_starts, recv_starts,
            l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
            for xvevg__akld in range(0, num_zero_starts):
                oeqh__iecns = recv_starts[xvevg__akld]
                evei__oaxra = np.concatenate((l_recv_buff[oeqh__iecns:],
                    in_arr[:xvevg__akld + 1]))
                if len(evei__oaxra) - np.isnan(evei__oaxra).sum() >= minp:
                    output[xvevg__akld] = kernel_func(evei__oaxra)
                else:
                    output[xvevg__akld] = np.nan
        return impl

    def impl_series(output, in_arr, index_arr, num_zero_starts, recv_starts,
        l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
        for xvevg__akld in range(0, num_zero_starts):
            oeqh__iecns = recv_starts[xvevg__akld]
            evei__oaxra = np.concatenate((l_recv_buff[oeqh__iecns:], in_arr
                [:xvevg__akld + 1]))
            dhofu__npwe = np.concatenate((l_recv_buff_idx[oeqh__iecns:],
                index_arr[:xvevg__akld + 1]))
            if len(evei__oaxra) - np.isnan(evei__oaxra).sum() >= minp:
                output[xvevg__akld] = kernel_func(pd.Series(evei__oaxra,
                    dhofu__npwe))
            else:
                output[xvevg__akld] = np.nan
    return impl_series


def roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp, start,
    end, kernel_func, raw):
    pass


@overload(roll_variable_apply_seq)
def overload_roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp,
    start, end, kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):
        return roll_variable_apply_seq_impl
    return roll_variable_apply_seq_impl_series


def roll_variable_apply_seq_impl(in_arr, on_arr, index_arr, win, minp,
    start, end, kernel_func, raw):
    N = len(in_arr)
    output = np.empty(N, dtype=np.float64)
    for xvevg__akld in range(0, N):
        s = start[xvevg__akld]
        tjso__jlizh = end[xvevg__akld]
        data = in_arr[s:tjso__jlizh]
        if tjso__jlizh - s - np.isnan(data).sum() >= minp:
            output[xvevg__akld] = kernel_func(data)
        else:
            output[xvevg__akld] = np.nan
    return output


def roll_variable_apply_seq_impl_series(in_arr, on_arr, index_arr, win,
    minp, start, end, kernel_func, raw):
    N = len(in_arr)
    output = np.empty(N, dtype=np.float64)
    for xvevg__akld in range(0, N):
        s = start[xvevg__akld]
        tjso__jlizh = end[xvevg__akld]
        data = in_arr[s:tjso__jlizh]
        if tjso__jlizh - s - np.isnan(data).sum() >= minp:
            output[xvevg__akld] = kernel_func(pd.Series(data, index_arr[s:
                tjso__jlizh]))
        else:
            output[xvevg__akld] = np.nan
    return output


@register_jitable(cache=True)
def _build_indexer(on_arr, N, win, left_closed, right_closed):
    rjee__dicq = cast_dt64_arr_to_int(on_arr)
    start = np.empty(N, np.int64)
    end = np.empty(N, np.int64)
    start[0] = 0
    if right_closed:
        end[0] = 1
    else:
        end[0] = 0
    for xvevg__akld in range(1, N):
        rrbfl__mtdnw = rjee__dicq[xvevg__akld]
        ydahc__gbq = rjee__dicq[xvevg__akld] - win
        if left_closed:
            ydahc__gbq -= 1
        start[xvevg__akld] = xvevg__akld
        for gzhv__sbp in range(start[xvevg__akld - 1], xvevg__akld):
            if rjee__dicq[gzhv__sbp] > ydahc__gbq:
                start[xvevg__akld] = gzhv__sbp
                break
        if rjee__dicq[end[xvevg__akld - 1]] <= rrbfl__mtdnw:
            end[xvevg__akld] = xvevg__akld + 1
        else:
            end[xvevg__akld] = end[xvevg__akld - 1]
        if not right_closed:
            end[xvevg__akld] -= 1
    return start, end


@register_jitable
def init_data_sum():
    return 0, 0.0


@register_jitable
def add_sum(val, nobs, sum_x):
    if not np.isnan(val):
        nobs += 1
        sum_x += val
    return nobs, sum_x


@register_jitable
def remove_sum(val, nobs, sum_x):
    if not np.isnan(val):
        nobs -= 1
        sum_x -= val
    return nobs, sum_x


@register_jitable
def calc_sum(minp, nobs, sum_x):
    return sum_x if nobs >= minp else np.nan


@register_jitable
def init_data_mean():
    return 0, 0.0, 0


@register_jitable
def add_mean(val, nobs, sum_x, neg_ct):
    if not np.isnan(val):
        nobs += 1
        sum_x += val
        if val < 0:
            neg_ct += 1
    return nobs, sum_x, neg_ct


@register_jitable
def remove_mean(val, nobs, sum_x, neg_ct):
    if not np.isnan(val):
        nobs -= 1
        sum_x -= val
        if val < 0:
            neg_ct -= 1
    return nobs, sum_x, neg_ct


@register_jitable
def calc_mean(minp, nobs, sum_x, neg_ct):
    if nobs >= minp:
        mrupc__koc = sum_x / nobs
        if neg_ct == 0 and mrupc__koc < 0.0:
            mrupc__koc = 0
        elif neg_ct == nobs and mrupc__koc > 0.0:
            mrupc__koc = 0
    else:
        mrupc__koc = np.nan
    return mrupc__koc


@register_jitable
def init_data_var():
    return 0, 0.0, 0.0


@register_jitable
def add_var(val, nobs, mean_x, ssqdm_x):
    if not np.isnan(val):
        nobs += 1
        omhm__opy = val - mean_x
        mean_x += omhm__opy / nobs
        ssqdm_x += (nobs - 1) * omhm__opy ** 2 / nobs
    return nobs, mean_x, ssqdm_x


@register_jitable
def remove_var(val, nobs, mean_x, ssqdm_x):
    if not np.isnan(val):
        nobs -= 1
        if nobs != 0:
            omhm__opy = val - mean_x
            mean_x -= omhm__opy / nobs
            ssqdm_x -= (nobs + 1) * omhm__opy ** 2 / nobs
        else:
            mean_x = 0.0
            ssqdm_x = 0.0
    return nobs, mean_x, ssqdm_x


@register_jitable
def calc_var(minp, nobs, mean_x, ssqdm_x):
    wwqvu__heit = 1.0
    mrupc__koc = np.nan
    if nobs >= minp and nobs > wwqvu__heit:
        if nobs == 1:
            mrupc__koc = 0.0
        else:
            mrupc__koc = ssqdm_x / (nobs - wwqvu__heit)
            if mrupc__koc < 0.0:
                mrupc__koc = 0.0
    return mrupc__koc


@register_jitable
def calc_std(minp, nobs, mean_x, ssqdm_x):
    auwbt__vdqss = calc_var(minp, nobs, mean_x, ssqdm_x)
    return np.sqrt(auwbt__vdqss)


@register_jitable
def init_data_count():
    return 0.0,


@register_jitable
def add_count(val, count_x):
    if not np.isnan(val):
        count_x += 1.0
    return count_x,


@register_jitable
def remove_count(val, count_x):
    if not np.isnan(val):
        count_x -= 1.0
    return count_x,


@register_jitable
def calc_count(minp, count_x):
    return count_x


@register_jitable
def calc_count_var(minp, count_x):
    return count_x if count_x >= minp else np.nan


linear_kernels = {'sum': (init_data_sum, add_sum, remove_sum, calc_sum),
    'mean': (init_data_mean, add_mean, remove_mean, calc_mean), 'var': (
    init_data_var, add_var, remove_var, calc_var), 'std': (init_data_var,
    add_var, remove_var, calc_std), 'count': (init_data_count, add_count,
    remove_count, calc_count)}


def shift():
    return


@overload(shift, jit_options={'cache': True})
def shift_overload(in_arr, shift, parallel):
    if not isinstance(parallel, types.Literal):
        return shift_impl


def shift_impl(in_arr, shift, parallel):
    N = len(in_arr)
    output = alloc_shift(N, in_arr, (-1,))
    send_right = shift > 0
    send_left = shift <= 0
    is_parallel_str = False
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        halo_size = np.int32(abs(shift))
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data_shift(in_arr, shift, rank, n_pes)
        eulj__wsqm = _border_icomm(in_arr, rank, n_pes, halo_size,
            send_right, send_left)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            vqoz__eqho) = eulj__wsqm
        if send_right and is_str_binary_array(in_arr):
            is_parallel_str = True
            shift_left_recv(r_send_req, l_send_req, rank, n_pes, halo_size,
                l_recv_req, l_recv_buff, output)
    shift_seq(in_arr, shift, output, is_parallel_str)
    if parallel:
        if send_right:
            if not is_str_binary_array(in_arr):
                shift_left_recv(r_send_req, l_send_req, rank, n_pes,
                    halo_size, l_recv_req, l_recv_buff, output)
        else:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, False, True)
            if rank != n_pes - 1:
                bodo.libs.distributed_api.wait(vqoz__eqho, True)
                for xvevg__akld in range(0, halo_size):
                    if bodo.libs.array_kernels.isna(r_recv_buff, xvevg__akld):
                        bodo.libs.array_kernels.setna(output, N - halo_size +
                            xvevg__akld)
                        continue
                    output[N - halo_size + xvevg__akld] = r_recv_buff[
                        xvevg__akld]
    return output


@register_jitable(cache=True)
def shift_seq(in_arr, shift, output, is_parallel_str=False):
    N = len(in_arr)
    kep__tdhl = 1 if shift > 0 else -1
    shift = kep__tdhl * min(abs(shift), N)
    if shift > 0 and (not is_parallel_str or bodo.get_rank() == 0):
        bodo.libs.array_kernels.setna_slice(output, slice(None, shift))
    start = max(shift, 0)
    end = min(N, N + shift)
    for xvevg__akld in range(start, end):
        if bodo.libs.array_kernels.isna(in_arr, xvevg__akld - shift):
            bodo.libs.array_kernels.setna(output, xvevg__akld)
            continue
        output[xvevg__akld] = in_arr[xvevg__akld - shift]
    if shift < 0:
        bodo.libs.array_kernels.setna_slice(output, slice(shift, None))
    return output


@register_jitable
def shift_left_recv(r_send_req, l_send_req, rank, n_pes, halo_size,
    l_recv_req, l_recv_buff, output):
    _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, False)
    if rank != 0:
        bodo.libs.distributed_api.wait(l_recv_req, True)
        for xvevg__akld in range(0, halo_size):
            if bodo.libs.array_kernels.isna(l_recv_buff, xvevg__akld):
                bodo.libs.array_kernels.setna(output, xvevg__akld)
                continue
            output[xvevg__akld] = l_recv_buff[xvevg__akld]


def is_str_binary_array(arr):
    return False


@overload(is_str_binary_array)
def overload_is_str_binary_array(arr):
    if arr in [bodo.string_array_type, bodo.binary_array_type]:
        return lambda arr: True
    return lambda arr: False


def is_supported_shift_array_type(arr_type):
    return isinstance(arr_type, types.Array) and (isinstance(arr_type.dtype,
        types.Number) or arr_type.dtype in [bodo.datetime64ns, bodo.
        timedelta64ns]) or isinstance(arr_type, (bodo.IntegerArrayType,
        bodo.DecimalArrayType)) or arr_type in (bodo.boolean_array, bodo.
        datetime_date_array_type, bodo.string_array_type, bodo.
        binary_array_type)


def pct_change():
    return


@overload(pct_change, jit_options={'cache': True})
def pct_change_overload(in_arr, shift, parallel):
    if not isinstance(parallel, types.Literal):
        return pct_change_impl


def pct_change_impl(in_arr, shift, parallel):
    N = len(in_arr)
    send_right = shift > 0
    send_left = shift <= 0
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        halo_size = np.int32(abs(shift))
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data_pct_change(in_arr, shift, rank, n_pes)
        eulj__wsqm = _border_icomm(in_arr, rank, n_pes, halo_size,
            send_right, send_left)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            vqoz__eqho) = eulj__wsqm
    output = pct_change_seq(in_arr, shift)
    if parallel:
        if send_right:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, False)
            if rank != 0:
                bodo.libs.distributed_api.wait(l_recv_req, True)
                for xvevg__akld in range(0, halo_size):
                    mgc__grfuw = l_recv_buff[xvevg__akld]
                    output[xvevg__akld] = (in_arr[xvevg__akld] - mgc__grfuw
                        ) / mgc__grfuw
        else:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, False, True)
            if rank != n_pes - 1:
                bodo.libs.distributed_api.wait(vqoz__eqho, True)
                for xvevg__akld in range(0, halo_size):
                    mgc__grfuw = r_recv_buff[xvevg__akld]
                    output[N - halo_size + xvevg__akld] = (in_arr[N -
                        halo_size + xvevg__akld] - mgc__grfuw) / mgc__grfuw
    return output


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_first_non_na(arr):
    if isinstance(arr.dtype, (types.Integer, types.Boolean)):
        zero = arr.dtype(0)
        return lambda arr: zero if len(arr) == 0 else arr[0]
    assert isinstance(arr.dtype, types.Float)
    iycvu__dbld = np.nan
    if arr.dtype == types.float32:
        iycvu__dbld = np.float32('nan')

    def impl(arr):
        for xvevg__akld in range(len(arr)):
            if not bodo.libs.array_kernels.isna(arr, xvevg__akld):
                return arr[xvevg__akld]
        return iycvu__dbld
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_last_non_na(arr):
    if isinstance(arr.dtype, (types.Integer, types.Boolean)):
        zero = arr.dtype(0)
        return lambda arr: zero if len(arr) == 0 else arr[-1]
    assert isinstance(arr.dtype, types.Float)
    iycvu__dbld = np.nan
    if arr.dtype == types.float32:
        iycvu__dbld = np.float32('nan')

    def impl(arr):
        pmlxm__tnxp = len(arr)
        for xvevg__akld in range(len(arr)):
            ktv__ppj = pmlxm__tnxp - xvevg__akld - 1
            if not bodo.libs.array_kernels.isna(arr, ktv__ppj):
                return arr[ktv__ppj]
        return iycvu__dbld
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_one_from_arr_dtype(arr):
    one = arr.dtype(1)
    return lambda arr: one


@register_jitable(cache=True)
def pct_change_seq(in_arr, shift):
    N = len(in_arr)
    output = alloc_pct_change(N, in_arr)
    kep__tdhl = 1 if shift > 0 else -1
    shift = kep__tdhl * min(abs(shift), N)
    if shift > 0:
        bodo.libs.array_kernels.setna_slice(output, slice(None, shift))
    else:
        bodo.libs.array_kernels.setna_slice(output, slice(shift, None))
    if shift > 0:
        dcs__mtvzb = get_first_non_na(in_arr[:shift])
        xqmlp__aaj = get_last_non_na(in_arr[:shift])
    else:
        dcs__mtvzb = get_last_non_na(in_arr[:-shift])
        xqmlp__aaj = get_first_non_na(in_arr[:-shift])
    one = get_one_from_arr_dtype(output)
    start = max(shift, 0)
    end = min(N, N + shift)
    for xvevg__akld in range(start, end):
        mgc__grfuw = in_arr[xvevg__akld - shift]
        if np.isnan(mgc__grfuw):
            mgc__grfuw = dcs__mtvzb
        else:
            dcs__mtvzb = mgc__grfuw
        val = in_arr[xvevg__akld]
        if np.isnan(val):
            val = xqmlp__aaj
        else:
            xqmlp__aaj = val
        output[xvevg__akld] = val / mgc__grfuw - one
    return output


@register_jitable(cache=True)
def _border_icomm(in_arr, rank, n_pes, halo_size, send_right=True,
    send_left=False):
    okfju__eis = np.int32(comm_border_tag)
    l_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr, (-1,))
    r_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr, (-1,))
    if send_right and rank != n_pes - 1:
        r_send_req = bodo.libs.distributed_api.isend(in_arr[-halo_size:],
            halo_size, np.int32(rank + 1), okfju__eis, True)
    if send_right and rank != 0:
        l_recv_req = bodo.libs.distributed_api.irecv(l_recv_buff, halo_size,
            np.int32(rank - 1), okfju__eis, True)
    if send_left and rank != 0:
        l_send_req = bodo.libs.distributed_api.isend(in_arr[:halo_size],
            halo_size, np.int32(rank - 1), okfju__eis, True)
    if send_left and rank != n_pes - 1:
        vqoz__eqho = bodo.libs.distributed_api.irecv(r_recv_buff, halo_size,
            np.int32(rank + 1), okfju__eis, True)
    return (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
        vqoz__eqho)


@register_jitable(cache=True)
def _border_icomm_var(in_arr, on_arr, rank, n_pes, win_size):
    okfju__eis = np.int32(comm_border_tag)
    N = len(on_arr)
    halo_size = N
    end = on_arr[-1]
    for gzhv__sbp in range(-2, -N, -1):
        nhdv__hdlvr = on_arr[gzhv__sbp]
        if end - nhdv__hdlvr >= win_size:
            halo_size = -gzhv__sbp
            break
    if rank != n_pes - 1:
        bodo.libs.distributed_api.send(halo_size, np.int32(rank + 1),
            okfju__eis)
        r_send_req = bodo.libs.distributed_api.isend(in_arr[-halo_size:],
            np.int32(halo_size), np.int32(rank + 1), okfju__eis, True)
        mdht__fsc = bodo.libs.distributed_api.isend(on_arr[-halo_size:], np
            .int32(halo_size), np.int32(rank + 1), okfju__eis, True)
    if rank != 0:
        halo_size = bodo.libs.distributed_api.recv(np.int64, np.int32(rank -
            1), okfju__eis)
        l_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr)
        l_recv_req = bodo.libs.distributed_api.irecv(l_recv_buff, np.int32(
            halo_size), np.int32(rank - 1), okfju__eis, True)
        l_recv_t_buff = np.empty(halo_size, np.int64)
        ntbo__oky = bodo.libs.distributed_api.irecv(l_recv_t_buff, np.int32
            (halo_size), np.int32(rank - 1), okfju__eis, True)
    return (l_recv_buff, l_recv_t_buff, r_send_req, mdht__fsc, l_recv_req,
        ntbo__oky)


@register_jitable
def _border_send_wait(r_send_req, l_send_req, rank, n_pes, right, left):
    if right and rank != n_pes - 1:
        bodo.libs.distributed_api.wait(r_send_req, True)
    if left and rank != 0:
        bodo.libs.distributed_api.wait(l_send_req, True)


@register_jitable
def _is_small_for_parallel(N, halo_size):
    ofe__hik = bodo.libs.distributed_api.dist_reduce(int(N <= 2 * halo_size +
        1), np.int32(Reduce_Type.Sum.value))
    return ofe__hik != 0


@register_jitable
def _handle_small_data(in_arr, win, minp, center, rank, n_pes, init_data,
    add_obs, remove_obs, calc_out):
    N = len(in_arr)
    lmsy__uzmc = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    ttkxh__tvzow = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        utv__huit, tremy__lrewo = roll_fixed_linear_generic_seq(ttkxh__tvzow,
            win, minp, center, init_data, add_obs, remove_obs, calc_out)
    else:
        utv__huit = np.empty(lmsy__uzmc, np.float64)
    bodo.libs.distributed_api.bcast(utv__huit)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return utv__huit[start:end]


@register_jitable
def _handle_small_data_apply(in_arr, index_arr, win, minp, center, rank,
    n_pes, kernel_func, raw=True):
    N = len(in_arr)
    lmsy__uzmc = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    ttkxh__tvzow = bodo.libs.distributed_api.gatherv(in_arr)
    vbkl__qplqr = bodo.libs.distributed_api.gatherv(index_arr)
    if rank == 0:
        utv__huit = roll_fixed_apply_seq(ttkxh__tvzow, vbkl__qplqr, win,
            minp, center, kernel_func, raw)
    else:
        utv__huit = np.empty(lmsy__uzmc, np.float64)
    bodo.libs.distributed_api.bcast(utv__huit)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return utv__huit[start:end]


def bcast_n_chars_if_str_binary_arr(arr):
    pass


@overload(bcast_n_chars_if_str_binary_arr)
def overload_bcast_n_chars_if_str_binary_arr(arr):
    if arr in [bodo.binary_array_type, bodo.string_array_type]:

        def impl(arr):
            return bodo.libs.distributed_api.bcast_scalar(np.int64(bodo.
                libs.str_arr_ext.num_total_chars(arr)))
        return impl
    return lambda arr: -1


@register_jitable
def _handle_small_data_shift(in_arr, shift, rank, n_pes):
    N = len(in_arr)
    lmsy__uzmc = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    ttkxh__tvzow = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        utv__huit = alloc_shift(len(ttkxh__tvzow), ttkxh__tvzow, (-1,))
        shift_seq(ttkxh__tvzow, shift, utv__huit)
        wpgdt__gur = bcast_n_chars_if_str_binary_arr(utv__huit)
    else:
        wpgdt__gur = bcast_n_chars_if_str_binary_arr(in_arr)
        utv__huit = alloc_shift(lmsy__uzmc, in_arr, (wpgdt__gur,))
    bodo.libs.distributed_api.bcast(utv__huit)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return utv__huit[start:end]


@register_jitable
def _handle_small_data_pct_change(in_arr, shift, rank, n_pes):
    N = len(in_arr)
    lmsy__uzmc = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    ttkxh__tvzow = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        utv__huit = pct_change_seq(ttkxh__tvzow, shift)
    else:
        utv__huit = alloc_pct_change(lmsy__uzmc, in_arr)
    bodo.libs.distributed_api.bcast(utv__huit)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return utv__huit[start:end]


def cast_dt64_arr_to_int(arr):
    return arr


@infer_global(cast_dt64_arr_to_int)
class DtArrToIntType(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        assert args[0] == types.Array(types.NPDatetime('ns'), 1, 'C') or args[0
            ] == types.Array(types.int64, 1, 'C')
        return signature(types.Array(types.int64, 1, 'C'), *args)


@lower_builtin(cast_dt64_arr_to_int, types.Array(types.NPDatetime('ns'), 1,
    'C'))
@lower_builtin(cast_dt64_arr_to_int, types.Array(types.int64, 1, 'C'))
def lower_cast_dt64_arr_to_int(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@register_jitable
def _is_small_for_parallel_variable(on_arr, win_size):
    if len(on_arr) < 2:
        jflj__csuk = 1
    else:
        start = on_arr[0]
        end = on_arr[-1]
        rjg__fktf = end - start
        jflj__csuk = int(rjg__fktf <= win_size)
    ofe__hik = bodo.libs.distributed_api.dist_reduce(jflj__csuk, np.int32(
        Reduce_Type.Sum.value))
    return ofe__hik != 0


@register_jitable
def _handle_small_data_variable(in_arr, on_arr, win, minp, rank, n_pes,
    init_data, add_obs, remove_obs, calc_out):
    N = len(in_arr)
    lmsy__uzmc = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    ttkxh__tvzow = bodo.libs.distributed_api.gatherv(in_arr)
    hng__awwx = bodo.libs.distributed_api.gatherv(on_arr)
    if rank == 0:
        start, end = _build_indexer(hng__awwx, lmsy__uzmc, win, False, True)
        utv__huit = roll_var_linear_generic_seq(ttkxh__tvzow, hng__awwx,
            win, minp, start, end, init_data, add_obs, remove_obs, calc_out)
    else:
        utv__huit = np.empty(lmsy__uzmc, np.float64)
    bodo.libs.distributed_api.bcast(utv__huit)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return utv__huit[start:end]


@register_jitable
def _handle_small_data_variable_apply(in_arr, on_arr, index_arr, win, minp,
    rank, n_pes, kernel_func, raw):
    N = len(in_arr)
    lmsy__uzmc = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    ttkxh__tvzow = bodo.libs.distributed_api.gatherv(in_arr)
    hng__awwx = bodo.libs.distributed_api.gatherv(on_arr)
    vbkl__qplqr = bodo.libs.distributed_api.gatherv(index_arr)
    if rank == 0:
        start, end = _build_indexer(hng__awwx, lmsy__uzmc, win, False, True)
        utv__huit = roll_variable_apply_seq(ttkxh__tvzow, hng__awwx,
            vbkl__qplqr, win, minp, start, end, kernel_func, raw)
    else:
        utv__huit = np.empty(lmsy__uzmc, np.float64)
    bodo.libs.distributed_api.bcast(utv__huit)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return utv__huit[start:end]


@register_jitable(cache=True)
def _dropna(arr):
    aki__wiw = len(arr)
    hxg__sqn = aki__wiw - np.isnan(arr).sum()
    A = np.empty(hxg__sqn, arr.dtype)
    bcc__jzc = 0
    for xvevg__akld in range(aki__wiw):
        val = arr[xvevg__akld]
        if not np.isnan(val):
            A[bcc__jzc] = val
            bcc__jzc += 1
    return A


def alloc_shift(n, A, s=None):
    return np.empty(n, A.dtype)


@overload(alloc_shift, no_unliteral=True)
def alloc_shift_overload(n, A, s=None):
    if not isinstance(A, types.Array):
        return lambda n, A, s=None: bodo.utils.utils.alloc_type(n, A, s)
    if isinstance(A.dtype, types.Integer):
        return lambda n, A, s=None: np.empty(n, np.float64)
    return lambda n, A, s=None: np.empty(n, A.dtype)


def alloc_pct_change(n, A):
    return np.empty(n, A.dtype)


@overload(alloc_pct_change, no_unliteral=True)
def alloc_pct_change_overload(n, A):
    if isinstance(A.dtype, types.Integer):
        return lambda n, A: np.empty(n, np.float64)
    return lambda n, A: np.empty(n, A.dtype)


def prep_values(A):
    return A.astype('float64')


@overload(prep_values, no_unliteral=True)
def prep_values_overload(A):
    if A == types.Array(types.float64, 1, 'C'):
        return lambda A: A
    return lambda A: A.astype(np.float64)


@register_jitable
def _validate_roll_fixed_args(win, minp):
    if win < 0:
        raise ValueError('window must be non-negative')
    if minp < 0:
        raise ValueError('min_periods must be >= 0')
    if minp > win:
        raise ValueError('min_periods must be <= window')


@register_jitable
def _validate_roll_var_args(minp, center):
    if minp < 0:
        raise ValueError('min_periods must be >= 0')
    if center:
        raise NotImplementedError(
            'rolling: center is not implemented for datetimelike and offset based windows'
            )
