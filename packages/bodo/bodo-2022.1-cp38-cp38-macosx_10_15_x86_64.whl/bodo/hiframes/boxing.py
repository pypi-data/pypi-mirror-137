"""
Boxing and unboxing support for DataFrame, Series, etc.
"""
import datetime
import decimal
import warnings
from enum import Enum
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.ir_utils import GuardException, guard
from numba.core.typing import signature
from numba.cpython.listobj import ListInstance
from numba.extending import NativeValue, box, intrinsic, typeof_impl, unbox
from numba.np import numpy_support
from numba.typed.typeddict import Dict
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import PDCategoricalDtype
from bodo.hiframes.pd_dataframe_ext import DataFramePayloadType, DataFrameType, check_runtime_cols_unsupported, construct_dataframe
from bodo.hiframes.pd_index_ext import BinaryIndexType, CategoricalIndexType, DatetimeIndexType, NumericIndexType, PeriodIndexType, RangeIndexType, StringIndexType, TimedeltaIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType, typeof_pd_int_dtype
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type, string_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType, StructType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.typing import BodoError, BodoWarning, dtype_to_array_type, get_overload_const_bool, get_overload_const_int, get_overload_const_str, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_str, raise_bodo_error, to_nullable_type
ll.add_symbol('array_size', hstr_ext.array_size)
ll.add_symbol('array_getptr1', hstr_ext.array_getptr1)
TABLE_FORMAT_THRESHOLD = 20


def _set_bodo_meta_in_pandas():
    if '_bodo_meta' not in pd.Series._metadata:
        pd.Series._metadata.append('_bodo_meta')
    if '_bodo_meta' not in pd.DataFrame._metadata:
        pd.DataFrame._metadata.append('_bodo_meta')


_set_bodo_meta_in_pandas()


@typeof_impl.register(pd.DataFrame)
def typeof_pd_dataframe(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    ody__awzj = tuple(val.columns.to_list())
    jibs__bclep = get_hiframes_dtypes(val)
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and len(val._bodo_meta['type_metadata'
        ][1]) == len(val.columns) and val._bodo_meta['type_metadata'][0] is not
        None):
        sijki__wlos = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        sijki__wlos = numba.typeof(val.index)
    mpk__bef = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    xhw__ybg = len(jibs__bclep) >= TABLE_FORMAT_THRESHOLD
    return DataFrameType(jibs__bclep, sijki__wlos, ody__awzj, mpk__bef,
        is_table_format=xhw__ybg)


@typeof_impl.register(pd.Series)
def typeof_pd_series(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    mpk__bef = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and val._bodo_meta['type_metadata'][0]
         is not None):
        kjc__osrwf = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        kjc__osrwf = numba.typeof(val.index)
    return SeriesType(_infer_series_dtype(val), index=kjc__osrwf, name_typ=
        numba.typeof(val.name), dist=mpk__bef)


@unbox(DataFrameType)
def unbox_dataframe(typ, val, c):
    check_runtime_cols_unsupported(typ, 'Unboxing')
    syoy__afog = c.pyapi.object_getattr_string(val, 'index')
    kbki__bzrzy = c.pyapi.to_native_value(typ.index, syoy__afog).value
    c.pyapi.decref(syoy__afog)
    if typ.is_table_format:
        fyjt__kbl = cgutils.create_struct_proxy(typ.table_type)(c.context,
            c.builder)
        fyjt__kbl.parent = val
        for fnnod__ccg, vhymz__qfdpk in typ.table_type.type_to_blk.items():
            uuso__ggwm = c.context.get_constant(types.int64, len(typ.
                table_type.block_to_arr_ind[vhymz__qfdpk]))
            kasin__whu, kqxw__mppb = ListInstance.allocate_ex(c.context, c.
                builder, types.List(fnnod__ccg), uuso__ggwm)
            kqxw__mppb.size = uuso__ggwm
            setattr(fyjt__kbl, f'block_{vhymz__qfdpk}', kqxw__mppb.value)
        xge__bxw = c.context.make_tuple(c.builder, types.Tuple([typ.
            table_type]), [fyjt__kbl._getvalue()])
    else:
        ddneo__yvn = [c.context.get_constant_null(fnnod__ccg) for
            fnnod__ccg in typ.data]
        xge__bxw = c.context.make_tuple(c.builder, types.Tuple(typ.data),
            ddneo__yvn)
    bxo__ksw = construct_dataframe(c.context, c.builder, typ, xge__bxw,
        kbki__bzrzy, val, None)
    return NativeValue(bxo__ksw)


def get_hiframes_dtypes(df):
    if (hasattr(df, '_bodo_meta') and df._bodo_meta is not None and 
        'type_metadata' in df._bodo_meta and df._bodo_meta['type_metadata']
         is not None and len(df._bodo_meta['type_metadata'][1]) == len(df.
        columns)):
        xhy__wcxqr = df._bodo_meta['type_metadata'][1]
    else:
        xhy__wcxqr = [None] * len(df.columns)
    znlil__gfhwm = [dtype_to_array_type(_infer_series_dtype(df.iloc[:, (i)],
        array_metadata=xhy__wcxqr[i])) for i in range(len(df.columns))]
    return tuple(znlil__gfhwm)


class SeriesDtypeEnum(Enum):
    Int8 = 0
    UInt8 = 1
    Int32 = 2
    UInt32 = 3
    Int64 = 4
    UInt64 = 7
    Float32 = 5
    Float64 = 6
    Int16 = 8
    UInt16 = 9
    STRING = 10
    Bool = 11
    Decimal = 12
    Datime_Date = 13
    NP_Datetime64ns = 14
    NP_Timedelta64ns = 15
    Int128 = 16
    LIST = 18
    STRUCT = 19
    BINARY = 21
    ARRAY = 22
    PD_nullable_Int8 = 23
    PD_nullable_UInt8 = 24
    PD_nullable_Int16 = 25
    PD_nullable_UInt16 = 26
    PD_nullable_Int32 = 27
    PD_nullable_UInt32 = 28
    PD_nullable_Int64 = 29
    PD_nullable_UInt64 = 30
    PD_nullable_bool = 31
    CategoricalType = 32
    NoneType = 33
    Literal = 34
    IntegerArray = 35
    RangeIndexType = 36
    DatetimeIndexType = 37
    NumericIndexType = 38
    PeriodIndexType = 39
    IntervalIndexType = 40
    CategoricalIndexType = 41
    StringIndexType = 42
    BinaryIndexType = 43
    TimedeltaIndexType = 44
    LiteralType = 45


_one_to_one_type_to_enum_map = {types.int8: SeriesDtypeEnum.Int8.value,
    types.uint8: SeriesDtypeEnum.UInt8.value, types.int32: SeriesDtypeEnum.
    Int32.value, types.uint32: SeriesDtypeEnum.UInt32.value, types.int64:
    SeriesDtypeEnum.Int64.value, types.uint64: SeriesDtypeEnum.UInt64.value,
    types.float32: SeriesDtypeEnum.Float32.value, types.float64:
    SeriesDtypeEnum.Float64.value, types.NPDatetime('ns'): SeriesDtypeEnum.
    NP_Datetime64ns.value, types.NPTimedelta('ns'): SeriesDtypeEnum.
    NP_Timedelta64ns.value, types.bool_: SeriesDtypeEnum.Bool.value, types.
    int16: SeriesDtypeEnum.Int16.value, types.uint16: SeriesDtypeEnum.
    UInt16.value, types.Integer('int128', 128): SeriesDtypeEnum.Int128.
    value, bodo.hiframes.datetime_date_ext.datetime_date_type:
    SeriesDtypeEnum.Datime_Date.value, IntDtype(types.int8):
    SeriesDtypeEnum.PD_nullable_Int8.value, IntDtype(types.uint8):
    SeriesDtypeEnum.PD_nullable_UInt8.value, IntDtype(types.int16):
    SeriesDtypeEnum.PD_nullable_Int16.value, IntDtype(types.uint16):
    SeriesDtypeEnum.PD_nullable_UInt16.value, IntDtype(types.int32):
    SeriesDtypeEnum.PD_nullable_Int32.value, IntDtype(types.uint32):
    SeriesDtypeEnum.PD_nullable_UInt32.value, IntDtype(types.int64):
    SeriesDtypeEnum.PD_nullable_Int64.value, IntDtype(types.uint64):
    SeriesDtypeEnum.PD_nullable_UInt64.value, bytes_type: SeriesDtypeEnum.
    BINARY.value, string_type: SeriesDtypeEnum.STRING.value, bodo.bool_:
    SeriesDtypeEnum.Bool.value, types.none: SeriesDtypeEnum.NoneType.value}
_one_to_one_enum_to_type_map = {SeriesDtypeEnum.Int8.value: types.int8,
    SeriesDtypeEnum.UInt8.value: types.uint8, SeriesDtypeEnum.Int32.value:
    types.int32, SeriesDtypeEnum.UInt32.value: types.uint32,
    SeriesDtypeEnum.Int64.value: types.int64, SeriesDtypeEnum.UInt64.value:
    types.uint64, SeriesDtypeEnum.Float32.value: types.float32,
    SeriesDtypeEnum.Float64.value: types.float64, SeriesDtypeEnum.
    NP_Datetime64ns.value: types.NPDatetime('ns'), SeriesDtypeEnum.
    NP_Timedelta64ns.value: types.NPTimedelta('ns'), SeriesDtypeEnum.Int16.
    value: types.int16, SeriesDtypeEnum.UInt16.value: types.uint16,
    SeriesDtypeEnum.Int128.value: types.Integer('int128', 128),
    SeriesDtypeEnum.Datime_Date.value: bodo.hiframes.datetime_date_ext.
    datetime_date_type, SeriesDtypeEnum.PD_nullable_Int8.value: IntDtype(
    types.int8), SeriesDtypeEnum.PD_nullable_UInt8.value: IntDtype(types.
    uint8), SeriesDtypeEnum.PD_nullable_Int16.value: IntDtype(types.int16),
    SeriesDtypeEnum.PD_nullable_UInt16.value: IntDtype(types.uint16),
    SeriesDtypeEnum.PD_nullable_Int32.value: IntDtype(types.int32),
    SeriesDtypeEnum.PD_nullable_UInt32.value: IntDtype(types.uint32),
    SeriesDtypeEnum.PD_nullable_Int64.value: IntDtype(types.int64),
    SeriesDtypeEnum.PD_nullable_UInt64.value: IntDtype(types.uint64),
    SeriesDtypeEnum.BINARY.value: bytes_type, SeriesDtypeEnum.STRING.value:
    string_type, SeriesDtypeEnum.Bool.value: bodo.bool_, SeriesDtypeEnum.
    NoneType.value: types.none}


def _dtype_from_type_enum_list(typ_enum_list):
    cxvzk__nlid, typ = _dtype_from_type_enum_list_recursor(typ_enum_list)
    if len(cxvzk__nlid) != 0:
        raise_bodo_error(
            f"""Unexpected Internal Error while converting typing metadata: Dtype list was not fully consumed.
 Input typ_enum_list: {typ_enum_list}.
Remainder: {cxvzk__nlid}. Please file the error here: https://github.com/Bodo-inc/Feedback"""
            )
    return typ


def _dtype_from_type_enum_list_recursor(typ_enum_list):
    if len(typ_enum_list) == 0:
        raise_bodo_error('Unable to infer dtype from empty typ_enum_list')
    elif typ_enum_list[0] in _one_to_one_enum_to_type_map:
        return typ_enum_list[1:], _one_to_one_enum_to_type_map[typ_enum_list[0]
            ]
    elif typ_enum_list[0] == SeriesDtypeEnum.IntegerArray.value:
        bddfp__jchd, typ = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        return bddfp__jchd, IntegerArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.ARRAY.value:
        bddfp__jchd, typ = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        return bddfp__jchd, dtype_to_array_type(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.Decimal.value:
        pxrl__yovou = typ_enum_list[1]
        minf__hgwot = typ_enum_list[2]
        return typ_enum_list[3:], Decimal128Type(pxrl__yovou, minf__hgwot)
    elif typ_enum_list[0] == SeriesDtypeEnum.STRUCT.value:
        seg__wdaz = typ_enum_list[1]
        tof__thfu = tuple(typ_enum_list[2:2 + seg__wdaz])
        boc__wauhj = typ_enum_list[2 + seg__wdaz:]
        bpy__uaoe = []
        for i in range(seg__wdaz):
            boc__wauhj, fqob__pki = _dtype_from_type_enum_list_recursor(
                boc__wauhj)
            bpy__uaoe.append(fqob__pki)
        return boc__wauhj, StructType(tuple(bpy__uaoe), tof__thfu)
    elif typ_enum_list[0] == SeriesDtypeEnum.Literal.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'Literal' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        jprs__ejeww = typ_enum_list[1]
        boc__wauhj = typ_enum_list[2:]
        return boc__wauhj, jprs__ejeww
    elif typ_enum_list[0] == SeriesDtypeEnum.LiteralType.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'LiteralType' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        jprs__ejeww = typ_enum_list[1]
        boc__wauhj = typ_enum_list[2:]
        return boc__wauhj, numba.types.literal(jprs__ejeww)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalType.value:
        boc__wauhj, tzudn__vgf = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        boc__wauhj, bvwe__oqq = _dtype_from_type_enum_list_recursor(boc__wauhj)
        boc__wauhj, ycrk__ybzk = _dtype_from_type_enum_list_recursor(boc__wauhj
            )
        boc__wauhj, pescu__lktz = _dtype_from_type_enum_list_recursor(
            boc__wauhj)
        boc__wauhj, raf__xbwk = _dtype_from_type_enum_list_recursor(boc__wauhj)
        return boc__wauhj, PDCategoricalDtype(tzudn__vgf, bvwe__oqq,
            ycrk__ybzk, pescu__lktz, raf__xbwk)
    elif typ_enum_list[0] == SeriesDtypeEnum.DatetimeIndexType.value:
        boc__wauhj, xwtre__jjh = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return boc__wauhj, DatetimeIndexType(xwtre__jjh)
    elif typ_enum_list[0] == SeriesDtypeEnum.NumericIndexType.value:
        boc__wauhj, dtype = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        boc__wauhj, xwtre__jjh = _dtype_from_type_enum_list_recursor(boc__wauhj
            )
        boc__wauhj, pescu__lktz = _dtype_from_type_enum_list_recursor(
            boc__wauhj)
        return boc__wauhj, NumericIndexType(dtype, xwtre__jjh, pescu__lktz)
    elif typ_enum_list[0] == SeriesDtypeEnum.PeriodIndexType.value:
        boc__wauhj, hvbw__tjk = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        boc__wauhj, xwtre__jjh = _dtype_from_type_enum_list_recursor(boc__wauhj
            )
        return boc__wauhj, PeriodIndexType(hvbw__tjk, xwtre__jjh)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalIndexType.value:
        boc__wauhj, pescu__lktz = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        boc__wauhj, xwtre__jjh = _dtype_from_type_enum_list_recursor(boc__wauhj
            )
        return boc__wauhj, CategoricalIndexType(pescu__lktz, xwtre__jjh)
    elif typ_enum_list[0] == SeriesDtypeEnum.RangeIndexType.value:
        boc__wauhj, xwtre__jjh = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return boc__wauhj, RangeIndexType(xwtre__jjh)
    elif typ_enum_list[0] == SeriesDtypeEnum.StringIndexType.value:
        boc__wauhj, xwtre__jjh = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return boc__wauhj, StringIndexType(xwtre__jjh)
    elif typ_enum_list[0] == SeriesDtypeEnum.BinaryIndexType.value:
        boc__wauhj, xwtre__jjh = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return boc__wauhj, BinaryIndexType(xwtre__jjh)
    elif typ_enum_list[0] == SeriesDtypeEnum.TimedeltaIndexType.value:
        boc__wauhj, xwtre__jjh = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return boc__wauhj, TimedeltaIndexType(xwtre__jjh)
    else:
        raise_bodo_error(
            f'Unexpected Internal Error while converting typing metadata: unable to infer dtype for type enum {typ_enum_list[0]}. Please file the error here: https://github.com/Bodo-inc/Feedback'
            )


def _dtype_to_type_enum_list(typ):
    return guard(_dtype_to_type_enum_list_recursor, typ)


def _dtype_to_type_enum_list_recursor(typ, upcast_numeric_index=True):
    if typ.__hash__ and typ in _one_to_one_type_to_enum_map:
        return [_one_to_one_type_to_enum_map[typ]]
    if isinstance(typ, (dict, int, list, tuple, str, bool, bytes, float)):
        return [SeriesDtypeEnum.Literal.value, typ]
    elif typ is None:
        return [SeriesDtypeEnum.Literal.value, typ]
    elif is_overload_constant_int(typ):
        ier__tnxon = get_overload_const_int(typ)
        if numba.types.maybe_literal(ier__tnxon) == typ:
            return [SeriesDtypeEnum.LiteralType.value, ier__tnxon]
    elif is_overload_constant_str(typ):
        ier__tnxon = get_overload_const_str(typ)
        if numba.types.maybe_literal(ier__tnxon) == typ:
            return [SeriesDtypeEnum.LiteralType.value, ier__tnxon]
    elif is_overload_constant_bool(typ):
        ier__tnxon = get_overload_const_bool(typ)
        if numba.types.maybe_literal(ier__tnxon) == typ:
            return [SeriesDtypeEnum.LiteralType.value, ier__tnxon]
    elif isinstance(typ, IntegerArrayType):
        return [SeriesDtypeEnum.IntegerArray.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif bodo.utils.utils.is_array_typ(typ, False):
        return [SeriesDtypeEnum.ARRAY.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif isinstance(typ, StructType):
        oog__wjlg = [SeriesDtypeEnum.STRUCT.value, len(typ.names)]
        for gmaz__die in typ.names:
            oog__wjlg.append(gmaz__die)
        for hzj__rkrb in typ.data:
            oog__wjlg += _dtype_to_type_enum_list_recursor(hzj__rkrb)
        return oog__wjlg
    elif isinstance(typ, bodo.libs.decimal_arr_ext.Decimal128Type):
        return [SeriesDtypeEnum.Decimal.value, typ.precision, typ.scale]
    elif isinstance(typ, PDCategoricalDtype):
        rpc__kxy = _dtype_to_type_enum_list_recursor(typ.categories)
        yxiq__wwhq = _dtype_to_type_enum_list_recursor(typ.elem_type)
        inpe__xjbl = _dtype_to_type_enum_list_recursor(typ.ordered)
        onlc__apfp = _dtype_to_type_enum_list_recursor(typ.data)
        zqq__uiu = _dtype_to_type_enum_list_recursor(typ.int_type)
        return [SeriesDtypeEnum.CategoricalType.value
            ] + rpc__kxy + yxiq__wwhq + inpe__xjbl + onlc__apfp + zqq__uiu
    elif isinstance(typ, DatetimeIndexType):
        return [SeriesDtypeEnum.DatetimeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, NumericIndexType):
        if upcast_numeric_index:
            if isinstance(typ.dtype, types.Float):
                xkqd__fdmuz = types.float64
                qjeas__xjdyi = types.Array(xkqd__fdmuz, 1, 'C')
            elif typ.dtype in {types.int8, types.int16, types.int32, types.
                int64}:
                xkqd__fdmuz = types.int64
                qjeas__xjdyi = types.Array(xkqd__fdmuz, 1, 'C')
            elif typ.dtype in {types.uint8, types.uint16, types.uint32,
                types.uint64}:
                xkqd__fdmuz = types.uint64
                qjeas__xjdyi = types.Array(xkqd__fdmuz, 1, 'C')
            elif typ.dtype == types.bool_:
                xkqd__fdmuz = typ.dtype
                qjeas__xjdyi = typ.data
            else:
                raise GuardException('Unable to convert type')
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(xkqd__fdmuz
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(qjeas__xjdyi)
        else:
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(typ.dtype
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(typ.data)
    elif isinstance(typ, PeriodIndexType):
        return [SeriesDtypeEnum.PeriodIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.freq
            ) + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, CategoricalIndexType):
        return [SeriesDtypeEnum.CategoricalIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.data
            ) + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, RangeIndexType):
        return [SeriesDtypeEnum.RangeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, StringIndexType):
        return [SeriesDtypeEnum.StringIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, BinaryIndexType):
        return [SeriesDtypeEnum.BinaryIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, TimedeltaIndexType):
        return [SeriesDtypeEnum.TimedeltaIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    else:
        raise GuardException('Unable to convert type')


def _infer_series_dtype(S, array_metadata=None):
    if S.dtype == np.dtype('O'):
        if len(S.values) == 0:
            if (hasattr(S, '_bodo_meta') and S._bodo_meta is not None and 
                'type_metadata' in S._bodo_meta and S._bodo_meta[
                'type_metadata'][1] is not None):
                zfaow__ydf = S._bodo_meta['type_metadata'][1]
                return _dtype_from_type_enum_list(zfaow__ydf)
            elif array_metadata != None:
                return _dtype_from_type_enum_list(array_metadata).dtype
        return numba.typeof(S.values).dtype
    if isinstance(S.dtype, pd.core.arrays.integer._IntegerDtype):
        return typeof_pd_int_dtype(S.dtype, None)
    elif isinstance(S.dtype, pd.CategoricalDtype):
        return bodo.typeof(S.dtype)
    elif isinstance(S.dtype, pd.StringDtype):
        return string_type
    elif isinstance(S.dtype, pd.BooleanDtype):
        return types.bool_
    if isinstance(S.dtype, pd.DatetimeTZDtype):
        raise BodoError('Timezone-aware datetime data type not supported yet')
    try:
        return numpy_support.from_dtype(S.dtype)
    except:
        raise BodoError(
            f'data type {S.dtype} for column {S.name} not supported yet')


def _get_use_df_parent_obj_flag(builder, context, pyapi, parent_obj, n_cols):
    if n_cols is None:
        return context.get_constant(types.bool_, False)
    wqad__jitjj = cgutils.is_not_null(builder, parent_obj)
    xvi__kbhne = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with builder.if_then(wqad__jitjj):
        itqyp__grlw = pyapi.object_getattr_string(parent_obj, 'columns')
        dpjv__znul = pyapi.call_method(itqyp__grlw, '__len__', ())
        builder.store(pyapi.long_as_longlong(dpjv__znul), xvi__kbhne)
        pyapi.decref(dpjv__znul)
        pyapi.decref(itqyp__grlw)
    use_parent_obj = builder.and_(wqad__jitjj, builder.icmp_unsigned('==',
        builder.load(xvi__kbhne), context.get_constant(types.int64, n_cols)))
    return use_parent_obj


def _get_df_columns_obj(c, builder, context, pyapi, df_typ, dataframe_payload):
    if df_typ.has_runtime_cols:
        muxrh__jfg = df_typ.runtime_colname_typ
        context.nrt.incref(builder, muxrh__jfg, dataframe_payload.columns)
        return pyapi.from_native_value(muxrh__jfg, dataframe_payload.
            columns, c.env_manager)
    if all(isinstance(c, int) for c in df_typ.columns):
        iss__txb = np.array(df_typ.columns, 'int64')
    elif all(isinstance(c, str) for c in df_typ.columns):
        iss__txb = pd.array(df_typ.columns, 'string')
    else:
        iss__txb = df_typ.columns
    jwk__kbpyn = numba.typeof(iss__txb)
    fix__cqob = context.get_constant_generic(builder, jwk__kbpyn, iss__txb)
    njqe__pmlv = pyapi.from_native_value(jwk__kbpyn, fix__cqob, c.env_manager)
    return njqe__pmlv


def _create_initial_df_object(builder, context, pyapi, c, df_typ, obj,
    dataframe_payload, res, use_parent_obj):
    with c.builder.if_else(use_parent_obj) as (use_parent, otherwise):
        with use_parent:
            pyapi.incref(obj)
            pneic__wddow = context.insert_const_string(c.builder.module,
                'numpy')
            kyd__ncq = pyapi.import_module_noblock(pneic__wddow)
            if df_typ.has_runtime_cols:
                pka__nqazy = 0
            else:
                pka__nqazy = len(df_typ.columns)
            mkjcy__izfpv = pyapi.long_from_longlong(lir.Constant(lir.
                IntType(64), pka__nqazy))
            vodk__dkal = pyapi.call_method(kyd__ncq, 'arange', (mkjcy__izfpv,))
            pyapi.object_setattr_string(obj, 'columns', vodk__dkal)
            pyapi.decref(kyd__ncq)
            pyapi.decref(vodk__dkal)
            pyapi.decref(mkjcy__izfpv)
        with otherwise:
            context.nrt.incref(builder, df_typ.index, dataframe_payload.index)
            akle__obpci = c.pyapi.from_native_value(df_typ.index,
                dataframe_payload.index, c.env_manager)
            pneic__wddow = context.insert_const_string(c.builder.module,
                'pandas')
            kyd__ncq = pyapi.import_module_noblock(pneic__wddow)
            df_obj = pyapi.call_method(kyd__ncq, 'DataFrame', (pyapi.
                borrow_none(), akle__obpci))
            pyapi.decref(kyd__ncq)
            pyapi.decref(akle__obpci)
            builder.store(df_obj, res)


@box(DataFrameType)
def box_dataframe(typ, val, c):
    from bodo.hiframes.table import box_table
    context = c.context
    builder = c.builder
    pyapi = c.pyapi
    dataframe_payload = bodo.hiframes.pd_dataframe_ext.get_dataframe_payload(c
        .context, c.builder, typ, val)
    oha__iyapk = cgutils.create_struct_proxy(typ)(context, builder, value=val)
    n_cols = len(typ.columns) if not typ.has_runtime_cols else None
    obj = oha__iyapk.parent
    res = cgutils.alloca_once_value(builder, obj)
    use_parent_obj = _get_use_df_parent_obj_flag(builder, context, pyapi,
        obj, n_cols)
    _create_initial_df_object(builder, context, pyapi, c, typ, obj,
        dataframe_payload, res, use_parent_obj)
    if typ.is_table_format:
        pme__evxe = typ.table_type
        fyjt__kbl = builder.extract_value(dataframe_payload.data, 0)
        context.nrt.incref(builder, pme__evxe, fyjt__kbl)
        uycc__zkkl = box_table(pme__evxe, fyjt__kbl, c, builder.not_(
            use_parent_obj))
        with builder.if_else(use_parent_obj) as (then, orelse):
            with then:
                nam__mtuz = pyapi.object_getattr_string(uycc__zkkl, 'arrays')
                njctn__wqhia = c.pyapi.make_none()
                if n_cols is None:
                    dpjv__znul = pyapi.call_method(nam__mtuz, '__len__', ())
                    uuso__ggwm = pyapi.long_as_longlong(dpjv__znul)
                    pyapi.decref(dpjv__znul)
                else:
                    uuso__ggwm = context.get_constant(types.int64, n_cols)
                with cgutils.for_range(builder, uuso__ggwm) as loop:
                    i = loop.index
                    udnh__ailj = pyapi.list_getitem(nam__mtuz, i)
                    ltw__ttysb = c.builder.icmp_unsigned('!=', udnh__ailj,
                        njctn__wqhia)
                    with builder.if_then(ltw__ttysb):
                        kqi__inp = pyapi.long_from_longlong(i)
                        df_obj = builder.load(res)
                        pyapi.object_setitem(df_obj, kqi__inp, udnh__ailj)
                        pyapi.decref(kqi__inp)
                pyapi.decref(nam__mtuz)
                pyapi.decref(njctn__wqhia)
            with orelse:
                df_obj = builder.load(res)
                akle__obpci = pyapi.object_getattr_string(df_obj, 'index')
                dxpv__zcvc = c.pyapi.call_method(uycc__zkkl, 'to_pandas', (
                    akle__obpci,))
                builder.store(dxpv__zcvc, res)
                pyapi.decref(df_obj)
                pyapi.decref(akle__obpci)
        pyapi.decref(uycc__zkkl)
    else:
        slnfv__xqshc = [builder.extract_value(dataframe_payload.data, i) for
            i in range(n_cols)]
        qkoi__evus = typ.data
        for i, hqd__xbfp, wlq__kgfa in zip(range(n_cols), slnfv__xqshc,
            qkoi__evus):
            evhf__bjzpe = cgutils.alloca_once_value(builder, hqd__xbfp)
            jveu__qsjyg = cgutils.alloca_once_value(builder, context.
                get_constant_null(wlq__kgfa))
            ltw__ttysb = builder.not_(is_ll_eq(builder, evhf__bjzpe,
                jveu__qsjyg))
            hsfcv__elzo = builder.or_(builder.not_(use_parent_obj), builder
                .and_(use_parent_obj, ltw__ttysb))
            with builder.if_then(hsfcv__elzo):
                kqi__inp = pyapi.long_from_longlong(context.get_constant(
                    types.int64, i))
                context.nrt.incref(builder, wlq__kgfa, hqd__xbfp)
                arr_obj = pyapi.from_native_value(wlq__kgfa, hqd__xbfp, c.
                    env_manager)
                df_obj = builder.load(res)
                pyapi.object_setitem(df_obj, kqi__inp, arr_obj)
                pyapi.decref(arr_obj)
                pyapi.decref(kqi__inp)
    df_obj = builder.load(res)
    njqe__pmlv = _get_df_columns_obj(c, builder, context, pyapi, typ,
        dataframe_payload)
    pyapi.object_setattr_string(df_obj, 'columns', njqe__pmlv)
    pyapi.decref(njqe__pmlv)
    if not typ.has_runtime_cols and (not typ.is_table_format or len(typ.
        columns) < TABLE_FORMAT_THRESHOLD):
        _set_bodo_meta_dataframe(c, df_obj, typ)
    c.context.nrt.decref(c.builder, typ, val)
    return df_obj


def get_df_obj_column_codegen(context, builder, pyapi, df_obj, col_ind,
    data_typ):
    njctn__wqhia = pyapi.borrow_none()
    taw__ejbv = pyapi.unserialize(pyapi.serialize_object(slice))
    kqxeh__oyyn = pyapi.call_function_objargs(taw__ejbv, [njctn__wqhia])
    dtglh__budvt = pyapi.long_from_longlong(col_ind)
    mvezy__omlwn = pyapi.tuple_pack([kqxeh__oyyn, dtglh__budvt])
    cvco__ipwn = pyapi.object_getattr_string(df_obj, 'iloc')
    tooe__egh = pyapi.object_getitem(cvco__ipwn, mvezy__omlwn)
    ytzm__ujnih = pyapi.object_getattr_string(tooe__egh, 'values')
    if isinstance(data_typ, types.Array):
        dvba__rhskz = context.insert_const_string(builder.module, 'numpy')
        rmdm__vmo = pyapi.import_module_noblock(dvba__rhskz)
        arr_obj = pyapi.call_method(rmdm__vmo, 'ascontiguousarray', (
            ytzm__ujnih,))
        pyapi.decref(ytzm__ujnih)
        pyapi.decref(rmdm__vmo)
    else:
        arr_obj = ytzm__ujnih
    pyapi.decref(taw__ejbv)
    pyapi.decref(kqxeh__oyyn)
    pyapi.decref(dtglh__budvt)
    pyapi.decref(mvezy__omlwn)
    pyapi.decref(cvco__ipwn)
    pyapi.decref(tooe__egh)
    return arr_obj


@intrinsic
def unbox_dataframe_column(typingctx, df, i=None):
    assert isinstance(df, DataFrameType) and is_overload_constant_int(i)

    def codegen(context, builder, sig, args):
        pyapi = context.get_python_api(builder)
        c = numba.core.pythonapi._UnboxContext(context, builder, pyapi)
        df_typ = sig.args[0]
        col_ind = get_overload_const_int(sig.args[1])
        data_typ = df_typ.data[col_ind]
        oha__iyapk = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        arr_obj = get_df_obj_column_codegen(context, builder, pyapi,
            oha__iyapk.parent, args[1], data_typ)
        wyukd__vuh = _unbox_series_data(data_typ.dtype, data_typ, arr_obj, c)
        c.pyapi.decref(arr_obj)
        dataframe_payload = (bodo.hiframes.pd_dataframe_ext.
            get_dataframe_payload(c.context, c.builder, df_typ, args[0]))
        if df_typ.is_table_format:
            fyjt__kbl = cgutils.create_struct_proxy(df_typ.table_type)(c.
                context, c.builder, builder.extract_value(dataframe_payload
                .data, 0))
            vhymz__qfdpk = df_typ.table_type.type_to_blk[data_typ]
            yexww__bib = getattr(fyjt__kbl, f'block_{vhymz__qfdpk}')
            wdttu__sbll = ListInstance(c.context, c.builder, types.List(
                data_typ), yexww__bib)
            ouae__ykum = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[col_ind])
            wdttu__sbll.inititem(ouae__ykum, wyukd__vuh.value, incref=False)
        else:
            dataframe_payload.data = builder.insert_value(dataframe_payload
                .data, wyukd__vuh.value, col_ind)
        uhfhp__efzsh = DataFramePayloadType(df_typ)
        fgq__equ = context.nrt.meminfo_data(builder, oha__iyapk.meminfo)
        gguja__ofgw = context.get_value_type(uhfhp__efzsh).as_pointer()
        fgq__equ = builder.bitcast(fgq__equ, gguja__ofgw)
        builder.store(dataframe_payload._getvalue(), fgq__equ)
    return signature(types.none, df, i), codegen


@unbox(SeriesType)
def unbox_series(typ, val, c):
    ytzm__ujnih = c.pyapi.object_getattr_string(val, 'values')
    if isinstance(typ.data, types.Array):
        dvba__rhskz = c.context.insert_const_string(c.builder.module, 'numpy')
        rmdm__vmo = c.pyapi.import_module_noblock(dvba__rhskz)
        arr_obj = c.pyapi.call_method(rmdm__vmo, 'ascontiguousarray', (
            ytzm__ujnih,))
        c.pyapi.decref(ytzm__ujnih)
        c.pyapi.decref(rmdm__vmo)
    else:
        arr_obj = ytzm__ujnih
    vsxbo__lgiw = _unbox_series_data(typ.dtype, typ.data, arr_obj, c).value
    akle__obpci = c.pyapi.object_getattr_string(val, 'index')
    kbki__bzrzy = c.pyapi.to_native_value(typ.index, akle__obpci).value
    afyds__airc = c.pyapi.object_getattr_string(val, 'name')
    aca__huvc = c.pyapi.to_native_value(typ.name_typ, afyds__airc).value
    bbtli__lspc = bodo.hiframes.pd_series_ext.construct_series(c.context, c
        .builder, typ, vsxbo__lgiw, kbki__bzrzy, aca__huvc)
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(akle__obpci)
    c.pyapi.decref(afyds__airc)
    return NativeValue(bbtli__lspc)


def _unbox_series_data(dtype, data_typ, arr_obj, c):
    if data_typ == string_array_split_view_type:
        eigsu__hhlmr = c.context.make_helper(c.builder,
            string_array_split_view_type)
        return NativeValue(eigsu__hhlmr._getvalue())
    return c.pyapi.to_native_value(data_typ, arr_obj)


@box(HeterogeneousSeriesType)
@box(SeriesType)
def box_series(typ, val, c):
    pneic__wddow = c.context.insert_const_string(c.builder.module, 'pandas')
    gpxy__bdmd = c.pyapi.import_module_noblock(pneic__wddow)
    ion__obw = bodo.hiframes.pd_series_ext.get_series_payload(c.context, c.
        builder, typ, val)
    c.context.nrt.incref(c.builder, typ.data, ion__obw.data)
    c.context.nrt.incref(c.builder, typ.index, ion__obw.index)
    c.context.nrt.incref(c.builder, typ.name_typ, ion__obw.name)
    arr_obj = c.pyapi.from_native_value(typ.data, ion__obw.data, c.env_manager)
    akle__obpci = c.pyapi.from_native_value(typ.index, ion__obw.index, c.
        env_manager)
    afyds__airc = c.pyapi.from_native_value(typ.name_typ, ion__obw.name, c.
        env_manager)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        dtype = c.pyapi.unserialize(c.pyapi.serialize_object(object))
    else:
        dtype = c.pyapi.make_none()
    res = c.pyapi.call_method(gpxy__bdmd, 'Series', (arr_obj, akle__obpci,
        dtype, afyds__airc))
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(akle__obpci)
    c.pyapi.decref(afyds__airc)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        c.pyapi.decref(dtype)
    _set_bodo_meta_series(res, c, typ)
    c.pyapi.decref(gpxy__bdmd)
    c.context.nrt.decref(c.builder, typ, val)
    return res


def type_enum_list_to_py_list_obj(pyapi, context, builder, env_manager,
    typ_list):
    trb__kwi = []
    for tzpf__fcdul in typ_list:
        if isinstance(tzpf__fcdul, int) and not isinstance(tzpf__fcdul, bool):
            bptsh__pcqkl = pyapi.long_from_longlong(lir.Constant(lir.
                IntType(64), tzpf__fcdul))
        else:
            koyji__zddzo = numba.typeof(tzpf__fcdul)
            tmohp__hfq = context.get_constant_generic(builder, koyji__zddzo,
                tzpf__fcdul)
            bptsh__pcqkl = pyapi.from_native_value(koyji__zddzo, tmohp__hfq,
                env_manager)
        trb__kwi.append(bptsh__pcqkl)
    wjdd__pzqrq = pyapi.list_pack(trb__kwi)
    for val in trb__kwi:
        pyapi.decref(val)
    return wjdd__pzqrq


def _set_bodo_meta_dataframe(c, obj, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    vdj__guwi = _dtype_to_type_enum_list(typ.index)
    if vdj__guwi != None:
        tly__jkzy = type_enum_list_to_py_list_obj(pyapi, context, builder,
            c.env_manager, vdj__guwi)
    else:
        tly__jkzy = pyapi.make_none()
    wab__bhpp = []
    for dtype in typ.data:
        typ_list = _dtype_to_type_enum_list(dtype)
        if typ_list != None:
            wjdd__pzqrq = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, typ_list)
        else:
            wjdd__pzqrq = pyapi.make_none()
        wab__bhpp.append(wjdd__pzqrq)
    busyo__cupo = pyapi.dict_new(2)
    sjqzc__zpcgz = pyapi.list_pack(wab__bhpp)
    jruxf__wmums = pyapi.list_pack([tly__jkzy, sjqzc__zpcgz])
    for val in wab__bhpp:
        pyapi.decref(val)
    ymvef__tes = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ
        .dist.value))
    pyapi.dict_setitem_string(busyo__cupo, 'dist', ymvef__tes)
    pyapi.dict_setitem_string(busyo__cupo, 'type_metadata', jruxf__wmums)
    pyapi.object_setattr_string(obj, '_bodo_meta', busyo__cupo)
    pyapi.decref(busyo__cupo)
    pyapi.decref(ymvef__tes)


def get_series_dtype_handle_null_int_and_hetrogenous(series_typ):
    if isinstance(series_typ, HeterogeneousSeriesType):
        return None
    if isinstance(series_typ.dtype, types.Number) and isinstance(series_typ
        .data, IntegerArrayType):
        return IntDtype(series_typ.dtype)
    return series_typ.dtype


def _set_bodo_meta_series(obj, c, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    busyo__cupo = pyapi.dict_new(2)
    ymvef__tes = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ
        .dist.value))
    vdj__guwi = _dtype_to_type_enum_list(typ.index)
    if vdj__guwi != None:
        tly__jkzy = type_enum_list_to_py_list_obj(pyapi, context, builder,
            c.env_manager, vdj__guwi)
    else:
        tly__jkzy = pyapi.make_none()
    dtype = get_series_dtype_handle_null_int_and_hetrogenous(typ)
    if dtype != None:
        typ_list = _dtype_to_type_enum_list(dtype)
        if typ_list != None:
            dpxo__ioz = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, typ_list)
        else:
            dpxo__ioz = pyapi.make_none()
    else:
        dpxo__ioz = pyapi.make_none()
    lwsf__bsbhk = pyapi.list_pack([tly__jkzy, dpxo__ioz])
    pyapi.dict_setitem_string(busyo__cupo, 'type_metadata', lwsf__bsbhk)
    pyapi.decref(lwsf__bsbhk)
    pyapi.dict_setitem_string(busyo__cupo, 'dist', ymvef__tes)
    pyapi.object_setattr_string(obj, '_bodo_meta', busyo__cupo)
    pyapi.decref(busyo__cupo)
    pyapi.decref(ymvef__tes)


@typeof_impl.register(np.ndarray)
def _typeof_ndarray(val, c):
    try:
        dtype = numba.np.numpy_support.from_dtype(val.dtype)
    except NotImplementedError as dmeu__vtbt:
        dtype = types.pyobject
    if dtype == types.pyobject:
        return _infer_ndarray_obj_dtype(val)
    suzj__vtyho = numba.np.numpy_support.map_layout(val)
    esrq__qhdu = not val.flags.writeable
    return types.Array(dtype, val.ndim, suzj__vtyho, readonly=esrq__qhdu)


def _infer_ndarray_obj_dtype(val):
    if not val.dtype == np.dtype('O'):
        raise BodoError('Unsupported array dtype: {}'.format(val.dtype))
    i = 0
    while i < len(val) and (pd.api.types.is_scalar(val[i]) and pd.isna(val[
        i]) or not pd.api.types.is_scalar(val[i]) and len(val[i]) == 0):
        i += 1
    if i == len(val):
        warnings.warn(BodoWarning(
            'Empty object array passed to Bodo, which causes ambiguity in typing. This can cause errors in parallel execution.'
            ))
        return string_array_type
    yzazg__kfrzy = val[i]
    if isinstance(yzazg__kfrzy, str):
        return string_array_type
    elif isinstance(yzazg__kfrzy, bytes):
        return binary_array_type
    elif isinstance(yzazg__kfrzy, bool):
        return bodo.libs.bool_arr_ext.boolean_array
    elif isinstance(yzazg__kfrzy, (int, np.int32, np.int64)):
        return bodo.libs.int_arr_ext.IntegerArrayType(numba.typeof(
            yzazg__kfrzy))
    elif isinstance(yzazg__kfrzy, (dict, Dict)) and all(isinstance(
        prf__owhw, str) for prf__owhw in yzazg__kfrzy.keys()):
        tof__thfu = tuple(yzazg__kfrzy.keys())
        iczk__opt = tuple(_get_struct_value_arr_type(v) for v in
            yzazg__kfrzy.values())
        return StructArrayType(iczk__opt, tof__thfu)
    elif isinstance(yzazg__kfrzy, (dict, Dict)):
        pau__hiyua = numba.typeof(_value_to_array(list(yzazg__kfrzy.keys())))
        now__mqg = numba.typeof(_value_to_array(list(yzazg__kfrzy.values())))
        return MapArrayType(pau__hiyua, now__mqg)
    elif isinstance(yzazg__kfrzy, tuple):
        iczk__opt = tuple(_get_struct_value_arr_type(v) for v in yzazg__kfrzy)
        return TupleArrayType(iczk__opt)
    if isinstance(yzazg__kfrzy, (list, np.ndarray, pd.arrays.BooleanArray,
        pd.arrays.IntegerArray, pd.arrays.StringArray)):
        if isinstance(yzazg__kfrzy, list):
            yzazg__kfrzy = _value_to_array(yzazg__kfrzy)
        dacyu__qvpei = numba.typeof(yzazg__kfrzy)
        return ArrayItemArrayType(dacyu__qvpei)
    if isinstance(yzazg__kfrzy, datetime.date):
        return datetime_date_array_type
    if isinstance(yzazg__kfrzy, datetime.timedelta):
        return datetime_timedelta_array_type
    if isinstance(yzazg__kfrzy, decimal.Decimal):
        return DecimalArrayType(38, 18)
    raise BodoError('Unsupported object array with first value: {}'.format(
        yzazg__kfrzy))


def _value_to_array(val):
    assert isinstance(val, (list, dict, Dict))
    if isinstance(val, (dict, Dict)):
        val = dict(val)
        return np.array([val], np.object_)
    cwzv__yqbb = val.copy()
    cwzv__yqbb.append(None)
    hqd__xbfp = np.array(cwzv__yqbb, np.object_)
    if len(val) and isinstance(val[0], float):
        hqd__xbfp = np.array(val, np.float64)
    return hqd__xbfp


def _get_struct_value_arr_type(v):
    if isinstance(v, (dict, Dict)):
        return numba.typeof(_value_to_array(v))
    if isinstance(v, list):
        return dtype_to_array_type(numba.typeof(_value_to_array(v)))
    if pd.api.types.is_scalar(v) and pd.isna(v):
        warnings.warn(BodoWarning(
            'Field value in struct array is NA, which causes ambiguity in typing. This can cause errors in parallel execution.'
            ))
        return string_array_type
    wlq__kgfa = dtype_to_array_type(numba.typeof(v))
    if isinstance(v, (int, bool)):
        wlq__kgfa = to_nullable_type(wlq__kgfa)
    return wlq__kgfa
