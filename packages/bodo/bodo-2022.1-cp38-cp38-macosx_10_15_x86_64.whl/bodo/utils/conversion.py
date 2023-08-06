"""
Utility functions for conversion of data such as list to array.
Need to be inlined for better optimization.
"""
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.binary_arr_ext import bytes_type
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.typing import BodoError, dtype_to_array_type, get_overload_const_list, get_overload_const_str, is_heterogeneous_tuple_type, is_np_arr_typ, is_overload_constant_list, is_overload_constant_str, is_overload_none, is_overload_true, to_nullable_type
NS_DTYPE = np.dtype('M8[ns]')
TD_DTYPE = np.dtype('m8[ns]')


def coerce_to_ndarray(data, error_on_nonarray=True, use_nullable_array=None,
    scalar_to_arr_len=None):
    return data


@overload(coerce_to_ndarray)
def overload_coerce_to_ndarray(data, error_on_nonarray=True,
    use_nullable_array=None, scalar_to_arr_len=None):
    from bodo.hiframes.pd_index_ext import DatetimeIndexType, NumericIndexType, RangeIndexType, TimedeltaIndexType
    from bodo.hiframes.pd_series_ext import SeriesType
    data = types.unliteral(data)
    if isinstance(data, types.Optional) and bodo.utils.typing.is_scalar_type(
        data.type):
        data = data.type
        use_nullable_array = True
    if isinstance(data, bodo.libs.int_arr_ext.IntegerArrayType
        ) and not is_overload_none(use_nullable_array):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.int_arr_ext.
            get_int_arr_data(data))
    if data == bodo.libs.bool_arr_ext.boolean_array and not is_overload_none(
        use_nullable_array):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.bool_arr_ext.
            get_bool_arr_data(data))
    if isinstance(data, types.Array):
        if not is_overload_none(use_nullable_array) and isinstance(data.
            dtype, (types.Boolean, types.Integer)):
            if data.dtype == types.bool_:
                if data.layout != 'C':
                    return (lambda data, error_on_nonarray=True,
                        use_nullable_array=None, scalar_to_arr_len=None:
                        bodo.libs.bool_arr_ext.init_bool_array(np.
                        ascontiguousarray(data), np.full(len(data) + 7 >> 3,
                        255, np.uint8)))
                else:
                    return (lambda data, error_on_nonarray=True,
                        use_nullable_array=None, scalar_to_arr_len=None:
                        bodo.libs.bool_arr_ext.init_bool_array(data, np.
                        full(len(data) + 7 >> 3, 255, np.uint8)))
            elif data.layout != 'C':
                return (lambda data, error_on_nonarray=True,
                    use_nullable_array=None, scalar_to_arr_len=None: bodo.
                    libs.int_arr_ext.init_integer_array(np.
                    ascontiguousarray(data), np.full(len(data) + 7 >> 3, 
                    255, np.uint8)))
            else:
                return (lambda data, error_on_nonarray=True,
                    use_nullable_array=None, scalar_to_arr_len=None: bodo.
                    libs.int_arr_ext.init_integer_array(data, np.full(len(
                    data) + 7 >> 3, 255, np.uint8)))
        if data.layout != 'C':
            return (lambda data, error_on_nonarray=True, use_nullable_array
                =None, scalar_to_arr_len=None: np.ascontiguousarray(data))
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: data)
    if isinstance(data, (types.List, types.UniTuple)):
        bqsu__nnck = data.dtype
        if isinstance(bqsu__nnck, types.Optional):
            bqsu__nnck = bqsu__nnck.type
            if bodo.utils.typing.is_scalar_type(bqsu__nnck):
                use_nullable_array = True
        if isinstance(bqsu__nnck, (types.Boolean, types.Integer,
            Decimal128Type)) or bqsu__nnck in [bodo.hiframes.
            pd_timestamp_ext.pd_timestamp_type, bodo.hiframes.
            datetime_date_ext.datetime_date_type, bodo.hiframes.
            datetime_timedelta_ext.datetime_timedelta_type]:
            jccqe__kav = dtype_to_array_type(bqsu__nnck)
            if not is_overload_none(use_nullable_array):
                jccqe__kav = to_nullable_type(jccqe__kav)

            def impl(data, error_on_nonarray=True, use_nullable_array=None,
                scalar_to_arr_len=None):
                rnitv__ilv = len(data)
                A = bodo.utils.utils.alloc_type(rnitv__ilv, jccqe__kav, (-1,))
                bodo.utils.utils.tuple_list_to_array(A, data, bqsu__nnck)
                return A
            return impl
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.asarray(data))
    if isinstance(data, SeriesType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_series_ext.
            get_series_data(data))
    if isinstance(data, (NumericIndexType, DatetimeIndexType,
        TimedeltaIndexType)):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_index_ext.
            get_index_data(data))
    if isinstance(data, RangeIndexType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.arange(data._start, data._stop,
            data._step))
    if isinstance(data, types.RangeType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.arange(data.start, data.stop,
            data.step))
    if not is_overload_none(scalar_to_arr_len):
        if isinstance(data, Decimal128Type):
            rto__uyiji = data.precision
            sskpr__ucvd = data.scale

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                rnitv__ilv = scalar_to_arr_len
                A = bodo.libs.decimal_arr_ext.alloc_decimal_array(rnitv__ilv,
                    rto__uyiji, sskpr__ucvd)
                for etgrd__lbx in numba.parfors.parfor.internal_prange(
                    rnitv__ilv):
                    A[etgrd__lbx] = data
                return A
            return impl_ts
        if data == bodo.hiframes.datetime_datetime_ext.datetime_datetime_type:
            sfsg__ihxo = np.dtype('datetime64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                rnitv__ilv = scalar_to_arr_len
                A = np.empty(rnitv__ilv, sfsg__ihxo)
                eaxl__oen = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(data))
                vdi__uaug = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    eaxl__oen)
                for etgrd__lbx in numba.parfors.parfor.internal_prange(
                    rnitv__ilv):
                    A[etgrd__lbx] = vdi__uaug
                return A
            return impl_ts
        if (data == bodo.hiframes.datetime_timedelta_ext.
            datetime_timedelta_type):
            tjr__jzlk = np.dtype('timedelta64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                rnitv__ilv = scalar_to_arr_len
                A = np.empty(rnitv__ilv, tjr__jzlk)
                hbo__pxu = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(data))
                for etgrd__lbx in numba.parfors.parfor.internal_prange(
                    rnitv__ilv):
                    A[etgrd__lbx] = hbo__pxu
                return A
            return impl_ts
        if data == bodo.hiframes.datetime_date_ext.datetime_date_type:

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                rnitv__ilv = scalar_to_arr_len
                A = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
                    rnitv__ilv)
                for etgrd__lbx in numba.parfors.parfor.internal_prange(
                    rnitv__ilv):
                    A[etgrd__lbx] = data
                return A
            return impl_ts
        if data == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            sfsg__ihxo = np.dtype('datetime64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                rnitv__ilv = scalar_to_arr_len
                A = np.empty(scalar_to_arr_len, sfsg__ihxo)
                eaxl__oen = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(data
                    .value)
                for etgrd__lbx in numba.parfors.parfor.internal_prange(
                    rnitv__ilv):
                    A[etgrd__lbx] = eaxl__oen
                return A
            return impl_ts
        dtype = types.unliteral(data)
        if not is_overload_none(use_nullable_array) and isinstance(dtype,
            types.Integer):

            def impl_null_integer(data, error_on_nonarray=True,
                use_nullable_array=None, scalar_to_arr_len=None):
                numba.parfors.parfor.init_prange()
                rnitv__ilv = scalar_to_arr_len
                zbr__kbee = bodo.libs.int_arr_ext.alloc_int_array(rnitv__ilv,
                    dtype)
                for etgrd__lbx in numba.parfors.parfor.internal_prange(
                    rnitv__ilv):
                    zbr__kbee[etgrd__lbx] = data
                return zbr__kbee
            return impl_null_integer
        if not is_overload_none(use_nullable_array) and dtype == types.bool_:

            def impl_null_bool(data, error_on_nonarray=True,
                use_nullable_array=None, scalar_to_arr_len=None):
                numba.parfors.parfor.init_prange()
                rnitv__ilv = scalar_to_arr_len
                zbr__kbee = bodo.libs.bool_arr_ext.alloc_bool_array(rnitv__ilv)
                for etgrd__lbx in numba.parfors.parfor.internal_prange(
                    rnitv__ilv):
                    zbr__kbee[etgrd__lbx] = data
                return zbr__kbee
            return impl_null_bool

        def impl_num(data, error_on_nonarray=True, use_nullable_array=None,
            scalar_to_arr_len=None):
            numba.parfors.parfor.init_prange()
            rnitv__ilv = scalar_to_arr_len
            zbr__kbee = np.empty(rnitv__ilv, dtype)
            for etgrd__lbx in numba.parfors.parfor.internal_prange(rnitv__ilv):
                zbr__kbee[etgrd__lbx] = data
            return zbr__kbee
        return impl_num
    if isinstance(data, types.BaseTuple) and all(isinstance(whtmh__taxgd, (
        types.Float, types.Integer)) for whtmh__taxgd in data.types):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.array(data))
    if bodo.utils.utils.is_array_typ(data, False):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: data)
    if is_overload_true(error_on_nonarray):
        raise BodoError(f'cannot coerce {data} to array')
    return (lambda data, error_on_nonarray=True, use_nullable_array=None,
        scalar_to_arr_len=None: data)


def coerce_to_array(data, error_on_nonarray=True, use_nullable_array=None,
    scalar_to_arr_len=None):
    return data


@overload(coerce_to_array, no_unliteral=True)
def overload_coerce_to_array(data, error_on_nonarray=True,
    use_nullable_array=None, scalar_to_arr_len=None):
    from bodo.hiframes.pd_index_ext import BinaryIndexType, CategoricalIndexType, StringIndexType
    from bodo.hiframes.pd_series_ext import SeriesType
    data = types.unliteral(data)
    if isinstance(data, types.Optional) and bodo.utils.typing.is_scalar_type(
        data.type):
        data = data.type
        use_nullable_array = True
    if isinstance(data, SeriesType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_series_ext.
            get_series_data(data))
    if isinstance(data, (StringIndexType, BinaryIndexType,
        CategoricalIndexType)):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_index_ext.
            get_index_data(data))
    if isinstance(data, types.List) and data.dtype in (bodo.string_type,
        bodo.bytes_type):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.str_arr_ext.
            str_arr_from_sequence(data))
    if isinstance(data, types.BaseTuple) and data.count == 0:
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.str_arr_ext.
            empty_str_arr(data))
    if isinstance(data, types.UniTuple) and isinstance(data.dtype, (types.
        UnicodeType, types.StringLiteral)) or isinstance(data, types.BaseTuple
        ) and all(isinstance(whtmh__taxgd, types.StringLiteral) for
        whtmh__taxgd in data.types):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.str_arr_ext.
            str_arr_from_sequence(data))
    if data in (bodo.string_array_type, bodo.binary_array_type, bodo.libs.
        bool_arr_ext.boolean_array, bodo.hiframes.datetime_date_ext.
        datetime_date_array_type, bodo.hiframes.datetime_timedelta_ext.
        datetime_timedelta_array_type, bodo.hiframes.split_impl.
        string_array_split_view_type) or isinstance(data, (bodo.libs.
        int_arr_ext.IntegerArrayType, DecimalArrayType, bodo.libs.
        interval_arr_ext.IntervalArrayType, bodo.libs.tuple_arr_ext.
        TupleArrayType, bodo.libs.struct_arr_ext.StructArrayType, bodo.
        hiframes.pd_categorical_ext.CategoricalArrayType, bodo.libs.
        csr_matrix_ext.CSRMatrixType)):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: data)
    if isinstance(data, (types.List, types.UniTuple)) and isinstance(data.
        dtype, types.BaseTuple):
        vzz__mway = tuple(dtype_to_array_type(whtmh__taxgd) for
            whtmh__taxgd in data.dtype.types)

        def impl_tuple_list(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            rnitv__ilv = len(data)
            arr = bodo.libs.tuple_arr_ext.pre_alloc_tuple_array(rnitv__ilv,
                (-1,), vzz__mway)
            for etgrd__lbx in range(rnitv__ilv):
                arr[etgrd__lbx] = data[etgrd__lbx]
            return arr
        return impl_tuple_list
    if isinstance(data, types.List) and (bodo.utils.utils.is_array_typ(data
        .dtype, False) or isinstance(data.dtype, types.List)):
        dofee__ckwpt = dtype_to_array_type(data.dtype.dtype)

        def impl_array_item_arr(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            rnitv__ilv = len(data)
            htzte__iml = init_nested_counts(dofee__ckwpt)
            for etgrd__lbx in range(rnitv__ilv):
                omot__xgjg = bodo.utils.conversion.coerce_to_array(data[
                    etgrd__lbx], use_nullable_array=True)
                htzte__iml = add_nested_counts(htzte__iml, omot__xgjg)
            zbr__kbee = (bodo.libs.array_item_arr_ext.
                pre_alloc_array_item_array(rnitv__ilv, htzte__iml,
                dofee__ckwpt))
            rgi__vrrw = bodo.libs.array_item_arr_ext.get_null_bitmap(zbr__kbee)
            for rfnfu__hgoxb in range(rnitv__ilv):
                omot__xgjg = bodo.utils.conversion.coerce_to_array(data[
                    rfnfu__hgoxb], use_nullable_array=True)
                zbr__kbee[rfnfu__hgoxb] = omot__xgjg
                bodo.libs.int_arr_ext.set_bit_to_arr(rgi__vrrw, rfnfu__hgoxb, 1
                    )
            return zbr__kbee
        return impl_array_item_arr
    if not is_overload_none(scalar_to_arr_len) and isinstance(data, (types.
        UnicodeType, types.StringLiteral)):

        def impl_str(data, error_on_nonarray=True, use_nullable_array=None,
            scalar_to_arr_len=None):
            rnitv__ilv = scalar_to_arr_len
            A = bodo.libs.str_arr_ext.pre_alloc_string_array(rnitv__ilv, -1)
            for etgrd__lbx in numba.parfors.parfor.internal_prange(rnitv__ilv):
                A[etgrd__lbx] = data
            return A
        return impl_str
    if isinstance(data, types.List) and data.dtype == bodo.pd_timestamp_type:

        def impl_list_timestamp(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            rnitv__ilv = len(data)
            A = np.empty(rnitv__ilv, np.dtype('datetime64[ns]'))
            for etgrd__lbx in range(rnitv__ilv):
                A[etgrd__lbx] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    data[etgrd__lbx].value)
            return A
        return impl_list_timestamp
    if isinstance(data, types.List) and data.dtype == bodo.pd_timedelta_type:

        def impl_list_timedelta(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            rnitv__ilv = len(data)
            A = np.empty(rnitv__ilv, np.dtype('timedelta64[ns]'))
            for etgrd__lbx in range(rnitv__ilv):
                A[etgrd__lbx
                    ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    data[etgrd__lbx].value)
            return A
        return impl_list_timedelta
    if not is_overload_none(scalar_to_arr_len) and data in [bodo.
        pd_timestamp_type, bodo.pd_timedelta_type]:
        ebg__bhfm = ('datetime64[ns]' if data == bodo.pd_timestamp_type else
            'timedelta64[ns]')

        def impl_timestamp(data, error_on_nonarray=True, use_nullable_array
            =None, scalar_to_arr_len=None):
            rnitv__ilv = scalar_to_arr_len
            A = np.empty(rnitv__ilv, ebg__bhfm)
            data = bodo.utils.conversion.unbox_if_timestamp(data)
            for etgrd__lbx in numba.parfors.parfor.internal_prange(rnitv__ilv):
                A[etgrd__lbx] = data
            return A
        return impl_timestamp
    return (lambda data, error_on_nonarray=True, use_nullable_array=None,
        scalar_to_arr_len=None: bodo.utils.conversion.coerce_to_ndarray(
        data, error_on_nonarray, use_nullable_array, scalar_to_arr_len))


def _is_str_dtype(dtype):
    return isinstance(dtype, bodo.libs.str_arr_ext.StringDtype) or isinstance(
        dtype, types.Function) and dtype.key[0
        ] == str or is_overload_constant_str(dtype) and get_overload_const_str(
        dtype) == 'str'


def fix_arr_dtype(data, new_dtype, copy=None, nan_to_str=True, from_series=
    False):
    return data


@overload(fix_arr_dtype, no_unliteral=True)
def overload_fix_arr_dtype(data, new_dtype, copy=None, nan_to_str=True,
    from_series=False):
    oswco__oojlx = is_overload_true(copy)
    if is_overload_none(new_dtype):
        if oswco__oojlx:
            return (lambda data, new_dtype, copy=None, nan_to_str=True,
                from_series=False: data.copy())
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data)
    if _is_str_dtype(new_dtype):
        if isinstance(data.dtype, types.Integer):

            def impl_int_str(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                rnitv__ilv = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(rnitv__ilv, -1
                    )
                for ecstv__rgizc in numba.parfors.parfor.internal_prange(
                    rnitv__ilv):
                    if bodo.libs.array_kernels.isna(data, ecstv__rgizc):
                        if nan_to_str:
                            bodo.libs.str_arr_ext.str_arr_setitem_NA_str(A,
                                ecstv__rgizc)
                        else:
                            bodo.libs.array_kernels.setna(A, ecstv__rgizc)
                    else:
                        bodo.libs.str_arr_ext.str_arr_setitem_int_to_str(A,
                            ecstv__rgizc, data[ecstv__rgizc])
                return A
            return impl_int_str
        if data.dtype == bytes_type:

            def impl_binary(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                rnitv__ilv = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(rnitv__ilv, -1
                    )
                for ecstv__rgizc in numba.parfors.parfor.internal_prange(
                    rnitv__ilv):
                    if bodo.libs.array_kernels.isna(data, ecstv__rgizc):
                        bodo.libs.array_kernels.setna(A, ecstv__rgizc)
                    else:
                        A[ecstv__rgizc] = ''.join([chr(vch__vcq) for
                            vch__vcq in data[ecstv__rgizc]])
                return A
            return impl_binary
        if is_overload_true(from_series) and data.dtype in (bodo.
            datetime64ns, bodo.timedelta64ns):

            def impl_str_dt_series(data, new_dtype, copy=None, nan_to_str=
                True, from_series=False):
                numba.parfors.parfor.init_prange()
                rnitv__ilv = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(rnitv__ilv, -1
                    )
                for ecstv__rgizc in numba.parfors.parfor.internal_prange(
                    rnitv__ilv):
                    if bodo.libs.array_kernels.isna(data, ecstv__rgizc):
                        if nan_to_str:
                            A[ecstv__rgizc] = 'NaT'
                        else:
                            bodo.libs.array_kernels.setna(A, ecstv__rgizc)
                        continue
                    A[ecstv__rgizc] = str(box_if_dt64(data[ecstv__rgizc]))
                return A
            return impl_str_dt_series
        else:

            def impl_str_array(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                rnitv__ilv = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(rnitv__ilv, -1
                    )
                for ecstv__rgizc in numba.parfors.parfor.internal_prange(
                    rnitv__ilv):
                    if bodo.libs.array_kernels.isna(data, ecstv__rgizc):
                        if nan_to_str:
                            A[ecstv__rgizc] = 'nan'
                        else:
                            bodo.libs.array_kernels.setna(A, ecstv__rgizc)
                        continue
                    A[ecstv__rgizc] = str(data[ecstv__rgizc])
                return A
            return impl_str_array
    if isinstance(new_dtype, bodo.hiframes.pd_categorical_ext.
        PDCategoricalDtype):

        def impl_cat_dtype(data, new_dtype, copy=None, nan_to_str=True,
            from_series=False):
            rnitv__ilv = len(data)
            numba.parfors.parfor.init_prange()
            vaf__lug = (bodo.hiframes.pd_categorical_ext.
                get_label_dict_from_categories(new_dtype.categories.values))
            A = bodo.hiframes.pd_categorical_ext.alloc_categorical_array(
                rnitv__ilv, new_dtype)
            rupsu__djo = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A))
            for etgrd__lbx in numba.parfors.parfor.internal_prange(rnitv__ilv):
                if bodo.libs.array_kernels.isna(data, etgrd__lbx):
                    bodo.libs.array_kernels.setna(A, etgrd__lbx)
                    continue
                val = data[etgrd__lbx]
                if val not in vaf__lug:
                    bodo.libs.array_kernels.setna(A, etgrd__lbx)
                    continue
                rupsu__djo[etgrd__lbx] = vaf__lug[val]
            return A
        return impl_cat_dtype
    if is_overload_constant_str(new_dtype) and get_overload_const_str(new_dtype
        ) == 'category':

        def impl_category(data, new_dtype, copy=None, nan_to_str=True,
            from_series=False):
            josen__xslkc = bodo.libs.array_kernels.unique(data, dropna=True)
            josen__xslkc = pd.Series(josen__xslkc).sort_values().values
            josen__xslkc = bodo.allgatherv(josen__xslkc, False)
            ubi__jqo = bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo
                .utils.conversion.index_from_array(josen__xslkc, None), 
                False, None, None)
            rnitv__ilv = len(data)
            numba.parfors.parfor.init_prange()
            vaf__lug = (bodo.hiframes.pd_categorical_ext.
                get_label_dict_from_categories_no_duplicates(josen__xslkc))
            A = bodo.hiframes.pd_categorical_ext.alloc_categorical_array(
                rnitv__ilv, ubi__jqo)
            rupsu__djo = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A))
            for etgrd__lbx in numba.parfors.parfor.internal_prange(rnitv__ilv):
                if bodo.libs.array_kernels.isna(data, etgrd__lbx):
                    bodo.libs.array_kernels.setna(A, etgrd__lbx)
                    continue
                val = data[etgrd__lbx]
                rupsu__djo[etgrd__lbx] = vaf__lug[val]
            return A
        return impl_category
    nb_dtype = bodo.utils.typing.parse_dtype(new_dtype)
    if isinstance(data, bodo.libs.int_arr_ext.IntegerArrayType):
        qxrx__ehr = isinstance(nb_dtype, bodo.libs.int_arr_ext.IntDtype
            ) and data.dtype == nb_dtype.dtype
    else:
        qxrx__ehr = data.dtype == nb_dtype
    if oswco__oojlx and qxrx__ehr:
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data.copy())
    if qxrx__ehr:
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data)
    if isinstance(nb_dtype, bodo.libs.int_arr_ext.IntDtype):
        if isinstance(nb_dtype, types.Integer):
            ebg__bhfm = nb_dtype
        else:
            ebg__bhfm = nb_dtype.dtype
        if isinstance(data.dtype, types.Float):

            def impl_float(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                rnitv__ilv = len(data)
                numba.parfors.parfor.init_prange()
                lmjm__rlza = bodo.libs.int_arr_ext.alloc_int_array(rnitv__ilv,
                    ebg__bhfm)
                for etgrd__lbx in numba.parfors.parfor.internal_prange(
                    rnitv__ilv):
                    if bodo.libs.array_kernels.isna(data, etgrd__lbx):
                        bodo.libs.array_kernels.setna(lmjm__rlza, etgrd__lbx)
                    else:
                        lmjm__rlza[etgrd__lbx] = int(data[etgrd__lbx])
                return lmjm__rlza
            return impl_float
        else:

            def impl(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                rnitv__ilv = len(data)
                numba.parfors.parfor.init_prange()
                lmjm__rlza = bodo.libs.int_arr_ext.alloc_int_array(rnitv__ilv,
                    ebg__bhfm)
                for etgrd__lbx in numba.parfors.parfor.internal_prange(
                    rnitv__ilv):
                    if bodo.libs.array_kernels.isna(data, etgrd__lbx):
                        bodo.libs.array_kernels.setna(lmjm__rlza, etgrd__lbx)
                    else:
                        lmjm__rlza[etgrd__lbx] = np.int64(data[etgrd__lbx])
                return lmjm__rlza
            return impl
    if isinstance(nb_dtype, types.Integer) and isinstance(data.dtype, types
        .Integer):

        def impl(data, new_dtype, copy=None, nan_to_str=True, from_series=False
            ):
            return data.astype(nb_dtype)
        return impl
    if nb_dtype == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(data, new_dtype, copy=None, nan_to_str=True,
            from_series=False):
            rnitv__ilv = len(data)
            numba.parfors.parfor.init_prange()
            lmjm__rlza = bodo.libs.bool_arr_ext.alloc_bool_array(rnitv__ilv)
            for etgrd__lbx in numba.parfors.parfor.internal_prange(rnitv__ilv):
                if bodo.libs.array_kernels.isna(data, etgrd__lbx):
                    bodo.libs.array_kernels.setna(lmjm__rlza, etgrd__lbx)
                else:
                    lmjm__rlza[etgrd__lbx] = bool(data[etgrd__lbx])
            return lmjm__rlza
        return impl_bool
    if nb_dtype == bodo.datetime64ns:
        if data.dtype == bodo.string_type:

            def impl_str(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                return bodo.hiframes.pd_timestamp_ext.series_str_dt64_astype(
                    data)
            return impl_str
        if data == bodo.datetime_date_array_type:

            def impl_date(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                return (bodo.hiframes.pd_timestamp_ext.
                    datetime_date_arr_to_dt64_arr(data))
            return impl_date
        if isinstance(data.dtype, types.Number) or data.dtype in [bodo.
            timedelta64ns, types.bool_]:

            def impl_numeric(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                rnitv__ilv = len(data)
                numba.parfors.parfor.init_prange()
                zbr__kbee = np.empty(rnitv__ilv, dtype=np.dtype(
                    'datetime64[ns]'))
                for etgrd__lbx in numba.parfors.parfor.internal_prange(
                    rnitv__ilv):
                    if bodo.libs.array_kernels.isna(data, etgrd__lbx):
                        bodo.libs.array_kernels.setna(zbr__kbee, etgrd__lbx)
                    else:
                        zbr__kbee[etgrd__lbx
                            ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                            np.int64(data[etgrd__lbx]))
                return zbr__kbee
            return impl_numeric
    if nb_dtype == bodo.timedelta64ns:
        if data.dtype == bodo.string_type:

            def impl_str(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                return bodo.hiframes.pd_timestamp_ext.series_str_td64_astype(
                    data)
            return impl_str
        if isinstance(data.dtype, types.Number) or data.dtype in [bodo.
            datetime64ns, types.bool_]:
            if oswco__oojlx:

                def impl_numeric(data, new_dtype, copy=None, nan_to_str=
                    True, from_series=False):
                    rnitv__ilv = len(data)
                    numba.parfors.parfor.init_prange()
                    zbr__kbee = np.empty(rnitv__ilv, dtype=np.dtype(
                        'timedelta64[ns]'))
                    for etgrd__lbx in numba.parfors.parfor.internal_prange(
                        rnitv__ilv):
                        if bodo.libs.array_kernels.isna(data, etgrd__lbx):
                            bodo.libs.array_kernels.setna(zbr__kbee, etgrd__lbx
                                )
                        else:
                            zbr__kbee[etgrd__lbx] = (bodo.hiframes.
                                pd_timestamp_ext.integer_to_timedelta64(np.
                                int64(data[etgrd__lbx])))
                    return zbr__kbee
                return impl_numeric
            else:
                return (lambda data, new_dtype, copy=None, nan_to_str=True,
                    from_series=False: data.view('int64'))
    if nb_dtype == types.int64 and data.dtype in [bodo.datetime64ns, bodo.
        timedelta64ns]:

        def impl_datelike_to_integer(data, new_dtype, copy=None, nan_to_str
            =True, from_series=False):
            rnitv__ilv = len(data)
            numba.parfors.parfor.init_prange()
            A = np.empty(rnitv__ilv, types.int64)
            for etgrd__lbx in numba.parfors.parfor.internal_prange(rnitv__ilv):
                if bodo.libs.array_kernels.isna(data, etgrd__lbx):
                    bodo.libs.array_kernels.setna(A, etgrd__lbx)
                else:
                    A[etgrd__lbx] = np.int64(data[etgrd__lbx])
            return A
        return impl_datelike_to_integer
    if data.dtype != nb_dtype:
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data.astype(nb_dtype))
    raise BodoError(f'Conversion from {data} to {new_dtype} not supported yet')


def array_type_from_dtype(dtype):
    return dtype_to_array_type(bodo.utils.typing.parse_dtype(dtype))


@overload(array_type_from_dtype)
def overload_array_type_from_dtype(dtype):
    arr_type = dtype_to_array_type(bodo.utils.typing.parse_dtype(dtype))
    return lambda dtype: arr_type


@numba.jit
def flatten_array(A):
    wyju__gnnp = []
    rnitv__ilv = len(A)
    for etgrd__lbx in range(rnitv__ilv):
        zuroi__ludph = A[etgrd__lbx]
        for bbqfv__rfj in zuroi__ludph:
            wyju__gnnp.append(bbqfv__rfj)
    return bodo.utils.conversion.coerce_to_array(wyju__gnnp)


def parse_datetimes_from_strings(data):
    return data


@overload(parse_datetimes_from_strings, no_unliteral=True)
def overload_parse_datetimes_from_strings(data):
    assert data == bodo.string_array_type

    def parse_impl(data):
        numba.parfors.parfor.init_prange()
        rnitv__ilv = len(data)
        mgmp__ebpjx = np.empty(rnitv__ilv, bodo.utils.conversion.NS_DTYPE)
        for etgrd__lbx in numba.parfors.parfor.internal_prange(rnitv__ilv):
            mgmp__ebpjx[etgrd__lbx
                ] = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(data[
                etgrd__lbx])
        return mgmp__ebpjx
    return parse_impl


def convert_to_dt64ns(data):
    return data


@overload(convert_to_dt64ns, no_unliteral=True)
def overload_convert_to_dt64ns(data):
    if data == bodo.hiframes.datetime_date_ext.datetime_date_array_type:
        return (lambda data: bodo.hiframes.pd_timestamp_ext.
            datetime_date_arr_to_dt64_arr(data))
    if is_np_arr_typ(data, types.int64):
        return lambda data: data.view(bodo.utils.conversion.NS_DTYPE)
    if is_np_arr_typ(data, types.NPDatetime('ns')):
        return lambda data: data
    if data == bodo.string_array_type:
        return lambda data: bodo.utils.conversion.parse_datetimes_from_strings(
            data)
    raise BodoError(f'invalid data type {data} for dt64 conversion')


def convert_to_td64ns(data):
    return data


@overload(convert_to_td64ns, no_unliteral=True)
def overload_convert_to_td64ns(data):
    if is_np_arr_typ(data, types.int64):
        return lambda data: data.view(bodo.utils.conversion.TD_DTYPE)
    if is_np_arr_typ(data, types.NPTimedelta('ns')):
        return lambda data: data
    if data == bodo.string_array_type:
        raise BodoError('conversion to timedelta from string not supported yet'
            )
    raise BodoError(f'invalid data type {data} for timedelta64 conversion')


def convert_to_index(data, name=None):
    return data


@overload(convert_to_index, no_unliteral=True)
def overload_convert_to_index(data, name=None):
    from bodo.hiframes.pd_index_ext import BinaryIndexType, CategoricalIndexType, DatetimeIndexType, NumericIndexType, PeriodIndexType, RangeIndexType, StringIndexType, TimedeltaIndexType
    if isinstance(data, (RangeIndexType, NumericIndexType,
        DatetimeIndexType, TimedeltaIndexType, StringIndexType,
        BinaryIndexType, CategoricalIndexType, PeriodIndexType, types.NoneType)
        ):
        return lambda data, name=None: data

    def impl(data, name=None):
        min__szrk = bodo.utils.conversion.coerce_to_array(data)
        return bodo.utils.conversion.index_from_array(min__szrk, name)
    return impl


def force_convert_index(I1, I2):
    return I2


@overload(force_convert_index, no_unliteral=True)
def overload_force_convert_index(I1, I2):
    from bodo.hiframes.pd_index_ext import RangeIndexType
    if isinstance(I2, RangeIndexType):
        return lambda I1, I2: pd.RangeIndex(len(I1._data))
    return lambda I1, I2: I1


def index_from_array(data, name=None):
    return data


@overload(index_from_array, no_unliteral=True)
def overload_index_from_array(data, name=None):
    if data in [bodo.string_array_type, bodo.binary_array_type]:
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_binary_str_index(data, name))
    if (data == bodo.hiframes.datetime_date_ext.datetime_date_array_type or
        data.dtype == types.NPDatetime('ns')):
        return lambda data, name=None: pd.DatetimeIndex(data, name=name)
    if data.dtype == types.NPTimedelta('ns'):
        return lambda data, name=None: pd.TimedeltaIndex(data, name=name)
    if isinstance(data.dtype, (types.Integer, types.Float, types.Boolean)):
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_numeric_index(data, name))
    if isinstance(data, bodo.libs.interval_arr_ext.IntervalArrayType):
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_interval_index(data, name))
    if isinstance(data, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_categorical_index(data, name))
    raise BodoError(f'cannot convert {data} to Index')


def index_to_array(data):
    return data


@overload(index_to_array, no_unliteral=True)
def overload_index_to_array(I):
    from bodo.hiframes.pd_index_ext import RangeIndexType
    if isinstance(I, RangeIndexType):
        return lambda I: np.arange(I._start, I._stop, I._step)
    return lambda I: bodo.hiframes.pd_index_ext.get_index_data(I)


def false_if_none(val):
    return False if val is None else val


@overload(false_if_none, no_unliteral=True)
def overload_false_if_none(val):
    if is_overload_none(val):
        return lambda val: False
    return lambda val: val


def extract_name_if_none(data, name):
    return name


@overload(extract_name_if_none, no_unliteral=True)
def overload_extract_name_if_none(data, name):
    from bodo.hiframes.pd_index_ext import CategoricalIndexType, DatetimeIndexType, NumericIndexType, PeriodIndexType, TimedeltaIndexType
    from bodo.hiframes.pd_series_ext import SeriesType
    if not is_overload_none(name):
        return lambda data, name: name
    if isinstance(data, (NumericIndexType, DatetimeIndexType,
        TimedeltaIndexType, PeriodIndexType, CategoricalIndexType)):
        return lambda data, name: bodo.hiframes.pd_index_ext.get_index_name(
            data)
    if isinstance(data, SeriesType):
        return lambda data, name: bodo.hiframes.pd_series_ext.get_series_name(
            data)
    return lambda data, name: name


def extract_index_if_none(data, index):
    return index


@overload(extract_index_if_none, no_unliteral=True)
def overload_extract_index_if_none(data, index):
    from bodo.hiframes.pd_series_ext import SeriesType
    if not is_overload_none(index):
        return lambda data, index: index
    if isinstance(data, SeriesType):
        return (lambda data, index: bodo.hiframes.pd_series_ext.
            get_series_index(data))
    return lambda data, index: bodo.hiframes.pd_index_ext.init_range_index(
        0, len(data), 1, None)


def box_if_dt64(val):
    return val


@overload(box_if_dt64, no_unliteral=True)
def overload_box_if_dt64(val):
    if val == types.NPDatetime('ns'):
        return (lambda val: bodo.hiframes.pd_timestamp_ext.
            convert_datetime64_to_timestamp(val))
    if val == types.NPTimedelta('ns'):
        return (lambda val: bodo.hiframes.pd_timestamp_ext.
            convert_numpy_timedelta64_to_pd_timedelta(val))
    return lambda val: val


def unbox_if_timestamp(val):
    return val


@overload(unbox_if_timestamp, no_unliteral=True)
def overload_unbox_if_timestamp(val):
    if val == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        return lambda val: bodo.hiframes.pd_timestamp_ext.integer_to_dt64(val
            .value)
    if val == bodo.hiframes.datetime_datetime_ext.datetime_datetime_type:
        return lambda val: bodo.hiframes.pd_timestamp_ext.integer_to_dt64(pd
            .Timestamp(val).value)
    if val == bodo.hiframes.datetime_timedelta_ext.pd_timedelta_type:
        return (lambda val: bodo.hiframes.pd_timestamp_ext.
            integer_to_timedelta64(val.value))
    if val == types.Optional(bodo.hiframes.pd_timestamp_ext.pd_timestamp_type):

        def impl_optional(val):
            if val is None:
                ehxj__aaqcr = None
            else:
                ehxj__aaqcr = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    bodo.utils.indexing.unoptional(val).value)
            return ehxj__aaqcr
        return impl_optional
    if val == types.Optional(bodo.hiframes.datetime_timedelta_ext.
        pd_timedelta_type):

        def impl_optional_td(val):
            if val is None:
                ehxj__aaqcr = None
            else:
                ehxj__aaqcr = (bodo.hiframes.pd_timestamp_ext.
                    integer_to_timedelta64(bodo.utils.indexing.unoptional(
                    val).value))
            return ehxj__aaqcr
        return impl_optional_td
    return lambda val: val


def to_tuple(val):
    return val


@overload(to_tuple, no_unliteral=True)
def overload_to_tuple(val):
    if not isinstance(val, types.BaseTuple) and is_overload_constant_list(val):
        fnn__pvuc = len(val.types if isinstance(val, types.LiteralList) else
            get_overload_const_list(val))
        kiey__zbquo = 'def f(val):\n'
        qsus__cqq = ','.join(f'val[{etgrd__lbx}]' for etgrd__lbx in range(
            fnn__pvuc))
        kiey__zbquo += f'  return ({qsus__cqq},)\n'
        mqtc__rrtvd = {}
        exec(kiey__zbquo, {}, mqtc__rrtvd)
        impl = mqtc__rrtvd['f']
        return impl
    assert isinstance(val, types.BaseTuple), 'tuple type expected'
    return lambda val: val


def get_array_if_series_or_index(data):
    return data


@overload(get_array_if_series_or_index)
def overload_get_array_if_series_or_index(data):
    from bodo.hiframes.pd_series_ext import SeriesType
    if isinstance(data, SeriesType):
        return lambda data: bodo.hiframes.pd_series_ext.get_series_data(data)
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        return lambda data: bodo.utils.conversion.coerce_to_array(data)
    if isinstance(data, bodo.hiframes.pd_index_ext.HeterogeneousIndexType):
        if not is_heterogeneous_tuple_type(data.data):

            def impl(data):
                ixh__uzj = bodo.hiframes.pd_index_ext.get_index_data(data)
                return bodo.utils.conversion.coerce_to_array(ixh__uzj)
            return impl

        def impl(data):
            return bodo.hiframes.pd_index_ext.get_index_data(data)
        return impl
    return lambda data: data


def extract_index_array(A):
    return np.arange(len(A))


@overload(extract_index_array, no_unliteral=True)
def overload_extract_index_array(A):
    from bodo.hiframes.pd_series_ext import SeriesType
    if isinstance(A, SeriesType):

        def impl(A):
            index = bodo.hiframes.pd_series_ext.get_series_index(A)
            jjuzf__ahbh = bodo.utils.conversion.coerce_to_array(index)
            return jjuzf__ahbh
        return impl
    return lambda A: np.arange(len(A))


def ensure_contig_if_np(arr):
    return np.ascontiguousarray(arr)


@overload(ensure_contig_if_np, no_unliteral=True)
def overload_ensure_contig_if_np(arr):
    if isinstance(arr, types.Array):
        return lambda arr: np.ascontiguousarray(arr)
    return lambda arr: arr


def struct_if_heter_dict(values, names):
    return {sobdm__fdxb: eaxl__oen for sobdm__fdxb, eaxl__oen in zip(names,
        values)}


@overload(struct_if_heter_dict, no_unliteral=True)
def overload_struct_if_heter_dict(values, names):
    if not types.is_homogeneous(*values.types):
        return lambda values, names: bodo.libs.struct_arr_ext.init_struct(
            values, names)
    gepge__djvlh = len(values.types)
    kiey__zbquo = 'def f(values, names):\n'
    qsus__cqq = ','.join("'{}': values[{}]".format(get_overload_const_str(
        names.types[etgrd__lbx]), etgrd__lbx) for etgrd__lbx in range(
        gepge__djvlh))
    kiey__zbquo += '  return {{{}}}\n'.format(qsus__cqq)
    mqtc__rrtvd = {}
    exec(kiey__zbquo, {}, mqtc__rrtvd)
    impl = mqtc__rrtvd['f']
    return impl
