""" Implementation of binary operators for the different types.
    Currently implemented operators:
        arith: add, sub, mul, truediv, floordiv, mod, pow
        cmp: lt, le, eq, ne, ge, gt
"""
import operator
import numba
from numba.core import types
from numba.core.imputils import lower_builtin
from numba.core.typing.builtins import machine_ints
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import overload
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type, datetime_date_type, datetime_timedelta_type
from bodo.hiframes.datetime_timedelta_ext import datetime_datetime_type, datetime_timedelta_array_type, pd_timedelta_type
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import DatetimeIndexType, HeterogeneousIndexType, is_index_type
from bodo.hiframes.pd_offsets_ext import date_offset_type, month_begin_type, month_end_type, week_type
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_type
from bodo.hiframes.series_impl import SeriesType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import Decimal128Type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.utils.typing import BodoError, is_overload_bool, is_timedelta_type


class SeriesCmpOpTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        lhs, rhs = args
        if cmp_timeseries(lhs, rhs) or (isinstance(lhs, DataFrameType) or
            isinstance(rhs, DataFrameType)) or not (isinstance(lhs,
            SeriesType) or isinstance(rhs, SeriesType)):
            return
        cnfdz__swwl = lhs.data if isinstance(lhs, SeriesType) else lhs
        resv__rbwg = rhs.data if isinstance(rhs, SeriesType) else rhs
        if cnfdz__swwl in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and resv__rbwg.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            cnfdz__swwl = resv__rbwg.dtype
        elif resv__rbwg in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and cnfdz__swwl.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            resv__rbwg = cnfdz__swwl.dtype
        hsqk__huf = cnfdz__swwl, resv__rbwg
        bvaka__mbqq = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            pgr__zleg = self.context.resolve_function_type(self.key,
                hsqk__huf, {}).return_type
        except Exception as nuv__oetjz:
            raise BodoError(bvaka__mbqq)
        if is_overload_bool(pgr__zleg):
            raise BodoError(bvaka__mbqq)
        wwkal__pyx = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        vzla__jsqfr = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        lmh__hcnip = types.bool_
        cuoo__zbna = SeriesType(lmh__hcnip, pgr__zleg, wwkal__pyx, vzla__jsqfr)
        return cuoo__zbna(*args)


def series_cmp_op_lower(op):

    def lower_impl(context, builder, sig, args):
        cpi__mkkdt = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if cpi__mkkdt is None:
            cpi__mkkdt = create_overload_cmp_operator(op)(*sig.args)
        return context.compile_internal(builder, cpi__mkkdt, sig, args)
    return lower_impl


class SeriesAndOrTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        lhs, rhs = args
        if not (isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType)):
            return
        cnfdz__swwl = lhs.data if isinstance(lhs, SeriesType) else lhs
        resv__rbwg = rhs.data if isinstance(rhs, SeriesType) else rhs
        hsqk__huf = cnfdz__swwl, resv__rbwg
        bvaka__mbqq = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            pgr__zleg = self.context.resolve_function_type(self.key,
                hsqk__huf, {}).return_type
        except Exception as yrita__yfhp:
            raise BodoError(bvaka__mbqq)
        wwkal__pyx = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        vzla__jsqfr = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        lmh__hcnip = pgr__zleg.dtype
        cuoo__zbna = SeriesType(lmh__hcnip, pgr__zleg, wwkal__pyx, vzla__jsqfr)
        return cuoo__zbna(*args)


def lower_series_and_or(op):

    def lower_and_or_impl(context, builder, sig, args):
        cpi__mkkdt = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if cpi__mkkdt is None:
            lhs, rhs = sig.args
            if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType
                ):
                cpi__mkkdt = (bodo.hiframes.dataframe_impl.
                    create_binary_op_overload(op)(*sig.args))
        return context.compile_internal(builder, cpi__mkkdt, sig, args)
    return lower_and_or_impl


def overload_add_operator_scalars(lhs, rhs):
    if lhs == week_type or rhs == week_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_week_offset_type(lhs, rhs))
    if lhs == month_begin_type or rhs == month_begin_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_month_begin_offset_type(lhs, rhs))
    if lhs == month_end_type or rhs == month_end_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_month_end_offset_type(lhs, rhs))
    if lhs == date_offset_type or rhs == date_offset_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_date_offset_type(lhs, rhs))
    if add_timestamp(lhs, rhs):
        return bodo.hiframes.pd_timestamp_ext.overload_add_operator_timestamp(
            lhs, rhs)
    if add_dt_td_and_dt_date(lhs, rhs):
        return (bodo.hiframes.datetime_date_ext.
            overload_add_operator_datetime_date(lhs, rhs))
    if add_datetime_and_timedeltas(lhs, rhs):
        return (bodo.hiframes.datetime_timedelta_ext.
            overload_add_operator_datetime_timedelta(lhs, rhs))
    raise_error_if_not_numba_supported(operator.add, lhs, rhs)


def overload_sub_operator_scalars(lhs, rhs):
    if sub_offset_to_datetime_or_timestamp(lhs, rhs):
        return bodo.hiframes.pd_offsets_ext.overload_sub_operator_offsets(lhs,
            rhs)
    if lhs == pd_timestamp_type and rhs in [pd_timestamp_type,
        datetime_timedelta_type, pd_timedelta_type]:
        return bodo.hiframes.pd_timestamp_ext.overload_sub_operator_timestamp(
            lhs, rhs)
    if sub_dt_or_td(lhs, rhs):
        return (bodo.hiframes.datetime_date_ext.
            overload_sub_operator_datetime_date(lhs, rhs))
    if sub_datetime_and_timedeltas(lhs, rhs):
        return (bodo.hiframes.datetime_timedelta_ext.
            overload_sub_operator_datetime_timedelta(lhs, rhs))
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:
        return (bodo.hiframes.datetime_datetime_ext.
            overload_sub_operator_datetime_datetime(lhs, rhs))
    raise_error_if_not_numba_supported(operator.sub, lhs, rhs)


def create_overload_arith_op(op):

    def overload_arith_operator(lhs, rhs):
        if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType):
            return bodo.hiframes.dataframe_impl.create_binary_op_overload(op)(
                lhs, rhs)
        if time_series_operation(lhs, rhs) and op in [operator.add,
            operator.sub]:
            return bodo.hiframes.series_dt_impl.create_bin_op_overload(op)(lhs,
                rhs)
        if isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType):
            return bodo.hiframes.series_impl.create_binary_op_overload(op)(lhs,
                rhs)
        if sub_dt_index_and_timestamp(lhs, rhs) and op == operator.sub:
            return (bodo.hiframes.pd_index_ext.
                overload_sub_operator_datetime_index(lhs, rhs))
        if operand_is_index(lhs) or operand_is_index(rhs):
            return bodo.hiframes.pd_index_ext.create_binary_op_overload(op)(lhs
                , rhs)
        if args_td_and_int_array(lhs, rhs):
            return bodo.libs.int_arr_ext.get_int_array_op_pd_td(op)(lhs, rhs)
        if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
            IntegerArrayType):
            return bodo.libs.int_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if lhs == boolean_array or rhs == boolean_array:
            return bodo.libs.bool_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if op == operator.add and (lhs == string_array_type or types.
            unliteral(lhs) == string_type):
            return bodo.libs.str_arr_ext.overload_add_operator_string_array(lhs
                , rhs)
        if op == operator.add:
            return overload_add_operator_scalars(lhs, rhs)
        if op == operator.sub:
            return overload_sub_operator_scalars(lhs, rhs)
        if op == operator.mul:
            if mul_timedelta_and_int(lhs, rhs):
                return (bodo.hiframes.datetime_timedelta_ext.
                    overload_mul_operator_timedelta(lhs, rhs))
            if mul_string_arr_and_int(lhs, rhs):
                return bodo.libs.str_arr_ext.overload_mul_operator_str_arr(lhs,
                    rhs)
            if mul_date_offset_and_int(lhs, rhs):
                return (bodo.hiframes.pd_offsets_ext.
                    overload_mul_date_offset_types(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op in [operator.truediv, operator.floordiv]:
            if div_timedelta_and_int(lhs, rhs):
                if op == operator.truediv:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_truediv_operator_pd_timedelta(lhs, rhs))
                else:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_floordiv_operator_pd_timedelta(lhs, rhs))
            if div_datetime_timedelta(lhs, rhs):
                if op == operator.truediv:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_truediv_operator_dt_timedelta(lhs, rhs))
                else:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_floordiv_operator_dt_timedelta(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op == operator.mod:
            if mod_timedeltas(lhs, rhs):
                return (bodo.hiframes.datetime_timedelta_ext.
                    overload_mod_operator_timedeltas(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op == operator.pow:
            raise_error_if_not_numba_supported(op, lhs, rhs)
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_arith_operator


def create_overload_cmp_operator(op):

    def overload_cmp_operator(lhs, rhs):
        if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType):
            return bodo.hiframes.dataframe_impl.create_binary_op_overload(op)(
                lhs, rhs)
        if cmp_timeseries(lhs, rhs):
            return bodo.hiframes.series_dt_impl.create_cmp_op_overload(op)(lhs,
                rhs)
        if isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType):
            return
        if lhs == datetime_date_array_type or rhs == datetime_date_array_type:
            return bodo.hiframes.datetime_date_ext.create_cmp_op_overload_arr(
                op)(lhs, rhs)
        if (lhs == datetime_timedelta_array_type or rhs ==
            datetime_timedelta_array_type):
            cpi__mkkdt = (bodo.hiframes.datetime_timedelta_ext.
                create_cmp_op_overload(op))
            return cpi__mkkdt(lhs, rhs)
        if lhs == string_array_type or rhs == string_array_type:
            return bodo.libs.str_arr_ext.create_binary_op_overload(op)(lhs, rhs
                )
        if isinstance(lhs, Decimal128Type) and isinstance(rhs, Decimal128Type):
            return bodo.libs.decimal_arr_ext.decimal_create_cmp_op_overload(op
                )(lhs, rhs)
        if lhs == boolean_array or rhs == boolean_array:
            return bodo.libs.bool_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
            IntegerArrayType):
            return bodo.libs.int_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if binary_array_cmp(lhs, rhs):
            return bodo.libs.binary_arr_ext.create_binary_cmp_op_overload(op)(
                lhs, rhs)
        if cmp_dt_index_to_string(lhs, rhs):
            return bodo.hiframes.pd_index_ext.overload_binop_dti_str(op)(lhs,
                rhs)
        if operand_is_index(lhs) or operand_is_index(rhs):
            return bodo.hiframes.pd_index_ext.create_binary_op_overload(op)(lhs
                , rhs)
        if lhs == datetime_date_type and rhs == datetime_date_type:
            return bodo.hiframes.datetime_date_ext.create_cmp_op_overload(op)(
                lhs, rhs)
        if can_cmp_date_datetime(lhs, rhs, op):
            return (bodo.hiframes.datetime_date_ext.
                create_datetime_date_cmp_op_overload(op)(lhs, rhs))
        if lhs == datetime_datetime_type and rhs == datetime_datetime_type:
            return bodo.hiframes.datetime_datetime_ext.create_cmp_op_overload(
                op)(lhs, rhs)
        if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:
            return bodo.hiframes.datetime_timedelta_ext.create_cmp_op_overload(
                op)(lhs, rhs)
        if cmp_timedeltas(lhs, rhs):
            cpi__mkkdt = (bodo.hiframes.datetime_timedelta_ext.
                pd_create_cmp_op_overload(op))
            return cpi__mkkdt(lhs, rhs)
        if cmp_timestamp_or_date(lhs, rhs):
            return (bodo.hiframes.pd_timestamp_ext.
                create_timestamp_cmp_op_overload(op)(lhs, rhs))
        if cmp_op_supported_by_numba(lhs, rhs):
            return
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_cmp_operator


def add_dt_td_and_dt_date(lhs, rhs):
    noyi__ebj = lhs == datetime_timedelta_type and rhs == datetime_date_type
    ytmy__izbgr = rhs == datetime_timedelta_type and lhs == datetime_date_type
    return noyi__ebj or ytmy__izbgr


def add_timestamp(lhs, rhs):
    oqqz__mmhh = lhs == pd_timestamp_type and is_timedelta_type(rhs)
    nob__pts = is_timedelta_type(lhs) and rhs == pd_timestamp_type
    return oqqz__mmhh or nob__pts


def add_datetime_and_timedeltas(lhs, rhs):
    set__tqms = [datetime_timedelta_type, pd_timedelta_type]
    gwhq__bvc = [datetime_timedelta_type, pd_timedelta_type,
        datetime_datetime_type]
    dcy__eqec = lhs in set__tqms and rhs in set__tqms
    ltmhf__owb = (lhs == datetime_datetime_type and rhs in set__tqms or rhs ==
        datetime_datetime_type and lhs in set__tqms)
    return dcy__eqec or ltmhf__owb


def mul_string_arr_and_int(lhs, rhs):
    resv__rbwg = isinstance(lhs, types.Integer) and rhs == string_array_type
    cnfdz__swwl = lhs == string_array_type and isinstance(rhs, types.Integer)
    return resv__rbwg or cnfdz__swwl


def mul_timedelta_and_int(lhs, rhs):
    noyi__ebj = lhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(rhs, types.Integer)
    ytmy__izbgr = rhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(lhs, types.Integer)
    return noyi__ebj or ytmy__izbgr


def mul_date_offset_and_int(lhs, rhs):
    jlgkg__nzhlb = lhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(rhs, types.Integer)
    hylur__pmus = rhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(lhs, types.Integer)
    return jlgkg__nzhlb or hylur__pmus


def sub_offset_to_datetime_or_timestamp(lhs, rhs):
    okd__silq = [datetime_datetime_type, pd_timestamp_type, datetime_date_type]
    cvc__mwmbq = [date_offset_type, month_begin_type, month_end_type, week_type
        ]
    return rhs in cvc__mwmbq and lhs in okd__silq


def sub_dt_index_and_timestamp(lhs, rhs):
    xtbgg__ocltd = isinstance(lhs, DatetimeIndexType
        ) and rhs == pd_timestamp_type
    eryxx__hjoco = isinstance(rhs, DatetimeIndexType
        ) and lhs == pd_timestamp_type
    return xtbgg__ocltd or eryxx__hjoco


def sub_dt_or_td(lhs, rhs):
    ixho__fof = lhs == datetime_date_type and rhs == datetime_timedelta_type
    xtat__ahg = lhs == datetime_date_type and rhs == datetime_date_type
    bli__dnsb = (lhs == datetime_date_array_type and rhs ==
        datetime_timedelta_type)
    return ixho__fof or xtat__ahg or bli__dnsb


def sub_datetime_and_timedeltas(lhs, rhs):
    vqxa__jihag = (is_timedelta_type(lhs) or lhs == datetime_datetime_type
        ) and is_timedelta_type(rhs)
    abqb__ebdl = (lhs == datetime_timedelta_array_type and rhs ==
        datetime_timedelta_type)
    return vqxa__jihag or abqb__ebdl


def div_timedelta_and_int(lhs, rhs):
    dcy__eqec = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    hcfzq__nze = lhs == pd_timedelta_type and isinstance(rhs, types.Integer)
    return dcy__eqec or hcfzq__nze


def div_datetime_timedelta(lhs, rhs):
    dcy__eqec = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    hcfzq__nze = lhs == datetime_timedelta_type and rhs == types.int64
    return dcy__eqec or hcfzq__nze


def mod_timedeltas(lhs, rhs):
    xbv__dikh = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    dvdod__gbwe = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    return xbv__dikh or dvdod__gbwe


def cmp_dt_index_to_string(lhs, rhs):
    xtbgg__ocltd = isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
        ) == string_type
    eryxx__hjoco = isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
        ) == string_type
    return xtbgg__ocltd or eryxx__hjoco


def cmp_timestamp_or_date(lhs, rhs):
    vsnv__lmki = (lhs == pd_timestamp_type and rhs == bodo.hiframes.
        datetime_date_ext.datetime_date_type)
    ppfm__imxhe = (lhs == bodo.hiframes.datetime_date_ext.
        datetime_date_type and rhs == pd_timestamp_type)
    udjdu__zztb = lhs == pd_timestamp_type and rhs == pd_timestamp_type
    dmv__vxix = lhs == pd_timestamp_type and rhs == bodo.datetime64ns
    bvz__pxnel = rhs == pd_timestamp_type and lhs == bodo.datetime64ns
    return vsnv__lmki or ppfm__imxhe or udjdu__zztb or dmv__vxix or bvz__pxnel


def cmp_timeseries(lhs, rhs):
    piou__tkvu = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (bodo
        .utils.typing.is_overload_constant_str(lhs) or lhs == bodo.libs.
        str_ext.string_type or lhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    qrp__lkv = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (bodo
        .utils.typing.is_overload_constant_str(rhs) or rhs == bodo.libs.
        str_ext.string_type or rhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    cddp__uitik = piou__tkvu or qrp__lkv
    fixoj__taz = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    nwk__cyi = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    qkd__jsw = fixoj__taz or nwk__cyi
    return cddp__uitik or qkd__jsw


def cmp_timedeltas(lhs, rhs):
    dcy__eqec = [pd_timedelta_type, bodo.timedelta64ns]
    return lhs in dcy__eqec and rhs in dcy__eqec


def operand_is_index(operand):
    return is_index_type(operand) or isinstance(operand, HeterogeneousIndexType
        )


def helper_time_series_checks(operand):
    eoi__dhf = bodo.hiframes.pd_series_ext.is_dt64_series_typ(operand
        ) or bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(operand
        ) or operand in [datetime_timedelta_type, datetime_datetime_type,
        pd_timestamp_type]
    return eoi__dhf


def binary_array_cmp(lhs, rhs):
    return lhs == binary_array_type and rhs in [bytes_type, binary_array_type
        ] or lhs in [bytes_type, binary_array_type
        ] and rhs == binary_array_type


def can_cmp_date_datetime(lhs, rhs, op):
    return op in (operator.eq, operator.ne) and (lhs == datetime_date_type and
        rhs == datetime_datetime_type or lhs == datetime_datetime_type and 
        rhs == datetime_date_type)


def time_series_operation(lhs, rhs):
    biyi__hgab = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == datetime_timedelta_type
    knl__ilfgh = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == datetime_timedelta_type
    bavo__iri = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
        ) and helper_time_series_checks(rhs)
    nzdo__qygv = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
        ) and helper_time_series_checks(lhs)
    return biyi__hgab or knl__ilfgh or bavo__iri or nzdo__qygv


def args_td_and_int_array(lhs, rhs):
    sej__knmq = (isinstance(lhs, IntegerArrayType) or isinstance(lhs, types
        .Array) and isinstance(lhs.dtype, types.Integer)) or (isinstance(
        rhs, IntegerArrayType) or isinstance(rhs, types.Array) and
        isinstance(rhs.dtype, types.Integer))
    zycl__etrv = lhs in [pd_timedelta_type] or rhs in [pd_timedelta_type]
    return sej__knmq and zycl__etrv


def arith_op_supported_by_numba(op, lhs, rhs):
    if op == operator.mul:
        ytmy__izbgr = isinstance(lhs, (types.Integer, types.Float)
            ) and isinstance(rhs, types.NPTimedelta)
        noyi__ebj = isinstance(rhs, (types.Integer, types.Float)
            ) and isinstance(lhs, types.NPTimedelta)
        uyb__fzv = ytmy__izbgr or noyi__ebj
        ywjzu__lppw = isinstance(rhs, types.UnicodeType) and isinstance(lhs,
            types.Integer)
        ypjzq__dsqii = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.Integer)
        kshul__pznz = ywjzu__lppw or ypjzq__dsqii
        cvz__jwrx = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        eqlf__cbo = isinstance(lhs, types.Float) and isinstance(rhs, types.
            Float)
        oqp__gsdhe = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        edvd__cdimf = cvz__jwrx or eqlf__cbo or oqp__gsdhe
        qas__kwfv = isinstance(lhs, types.List) and isinstance(rhs, types.
            Integer)
        tys = types.UnicodeCharSeq, types.CharSeq, types.Bytes
        tff__svt = isinstance(lhs, tys) or isinstance(rhs, tys)
        jsvhz__iki = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (uyb__fzv or kshul__pznz or edvd__cdimf or qas__kwfv or
            tff__svt or jsvhz__iki)
    if op == operator.pow:
        ijili__xst = isinstance(lhs, types.Integer) and isinstance(rhs, (
            types.IntegerLiteral, types.Integer))
        amse__akp = isinstance(lhs, types.Float) and isinstance(rhs, (types
            .IntegerLiteral, types.Float, types.Integer) or rhs in types.
            unsigned_domain or rhs in types.signed_domain)
        oqp__gsdhe = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        jsvhz__iki = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return ijili__xst or amse__akp or oqp__gsdhe or jsvhz__iki
    if op == operator.floordiv:
        eqlf__cbo = lhs in types.real_domain and rhs in types.real_domain
        cvz__jwrx = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        pjmv__fpic = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        dcy__eqec = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        jsvhz__iki = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return eqlf__cbo or cvz__jwrx or pjmv__fpic or dcy__eqec or jsvhz__iki
    if op == operator.truediv:
        hhpjc__rkl = lhs in machine_ints and rhs in machine_ints
        eqlf__cbo = lhs in types.real_domain and rhs in types.real_domain
        oqp__gsdhe = (lhs in types.complex_domain and rhs in types.
            complex_domain)
        cvz__jwrx = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        pjmv__fpic = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        fxxlb__vzy = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        dcy__eqec = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        jsvhz__iki = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (hhpjc__rkl or eqlf__cbo or oqp__gsdhe or cvz__jwrx or
            pjmv__fpic or fxxlb__vzy or dcy__eqec or jsvhz__iki)
    if op == operator.mod:
        hhpjc__rkl = lhs in machine_ints and rhs in machine_ints
        eqlf__cbo = lhs in types.real_domain and rhs in types.real_domain
        cvz__jwrx = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        pjmv__fpic = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        jsvhz__iki = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return hhpjc__rkl or eqlf__cbo or cvz__jwrx or pjmv__fpic or jsvhz__iki
    if op == operator.add or op == operator.sub:
        uyb__fzv = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            types.NPTimedelta)
        myhml__msay = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPDatetime)
        iqoib__dypx = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPTimedelta)
        buhma__exnu = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
        cvz__jwrx = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        eqlf__cbo = isinstance(lhs, types.Float) and isinstance(rhs, types.
            Float)
        oqp__gsdhe = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        edvd__cdimf = cvz__jwrx or eqlf__cbo or oqp__gsdhe
        jsvhz__iki = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        nwg__wemig = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
            types.BaseTuple)
        qas__kwfv = isinstance(lhs, types.List) and isinstance(rhs, types.List)
        xffo__tnm = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeType)
        pndu__mhon = isinstance(rhs, types.UnicodeCharSeq) and isinstance(lhs,
            types.UnicodeType)
        ztpu__vgj = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeCharSeq)
        acdp__gxpik = isinstance(lhs, (types.CharSeq, types.Bytes)
            ) and isinstance(rhs, (types.CharSeq, types.Bytes))
        qxho__ufgm = xffo__tnm or pndu__mhon or ztpu__vgj or acdp__gxpik
        kshul__pznz = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeType)
        tbrb__aai = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeCharSeq)
        qinz__wqeow = kshul__pznz or tbrb__aai
        olarm__yduj = lhs == types.NPTimedelta and rhs == types.NPDatetime
        fmf__wlzoz = (nwg__wemig or qas__kwfv or qxho__ufgm or qinz__wqeow or
            olarm__yduj)
        vmywr__nehx = op == operator.add and fmf__wlzoz
        return (uyb__fzv or myhml__msay or iqoib__dypx or buhma__exnu or
            edvd__cdimf or jsvhz__iki or vmywr__nehx)


def cmp_op_supported_by_numba(lhs, rhs):
    jsvhz__iki = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
    qas__kwfv = isinstance(lhs, types.ListType) and isinstance(rhs, types.
        ListType)
    uyb__fzv = isinstance(lhs, types.NPTimedelta) and isinstance(rhs, types
        .NPTimedelta)
    vul__yslwd = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
        types.NPDatetime)
    unicode_types = (types.UnicodeType, types.StringLiteral, types.CharSeq,
        types.Bytes, types.UnicodeCharSeq)
    kshul__pznz = isinstance(lhs, unicode_types) and isinstance(rhs,
        unicode_types)
    nwg__wemig = isinstance(lhs, types.BaseTuple) and isinstance(rhs, types
        .BaseTuple)
    buhma__exnu = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
    edvd__cdimf = isinstance(lhs, types.Number) and isinstance(rhs, types.
        Number)
    auoi__qsxty = isinstance(lhs, types.Boolean) and isinstance(rhs, types.
        Boolean)
    hnwm__eml = isinstance(lhs, types.NoneType) or isinstance(rhs, types.
        NoneType)
    gzdb__cbgjx = isinstance(lhs, types.DictType) and isinstance(rhs, types
        .DictType)
    nyy__jklpi = isinstance(lhs, types.EnumMember) and isinstance(rhs,
        types.EnumMember)
    fvwn__uwitx = isinstance(lhs, types.Literal) and isinstance(rhs, types.
        Literal)
    return (qas__kwfv or uyb__fzv or vul__yslwd or kshul__pznz or
        nwg__wemig or buhma__exnu or edvd__cdimf or auoi__qsxty or
        hnwm__eml or gzdb__cbgjx or jsvhz__iki or nyy__jklpi or fvwn__uwitx)


def raise_error_if_not_numba_supported(op, lhs, rhs):
    if arith_op_supported_by_numba(op, lhs, rhs):
        return
    raise BodoError(
        f'{op} operator not supported for data types {lhs} and {rhs}.')


def _install_series_and_or():
    for op in (operator.or_, operator.and_):
        infer_global(op)(SeriesAndOrTyper)
        lower_impl = lower_series_and_or(op)
        lower_builtin(op, SeriesType, SeriesType)(lower_impl)
        lower_builtin(op, SeriesType, types.Any)(lower_impl)
        lower_builtin(op, types.Any, SeriesType)(lower_impl)


_install_series_and_or()


def _install_cmp_ops():
    for op in (operator.lt, operator.eq, operator.ne, operator.ge, operator
        .gt, operator.le):
        infer_global(op)(SeriesCmpOpTemplate)
        lower_impl = series_cmp_op_lower(op)
        lower_builtin(op, SeriesType, SeriesType)(lower_impl)
        lower_builtin(op, SeriesType, types.Any)(lower_impl)
        lower_builtin(op, types.Any, SeriesType)(lower_impl)
        wtb__jnux = create_overload_cmp_operator(op)
        overload(op, no_unliteral=True)(wtb__jnux)


_install_cmp_ops()


def install_arith_ops():
    for op in (operator.add, operator.sub, operator.mul, operator.truediv,
        operator.floordiv, operator.mod, operator.pow):
        wtb__jnux = create_overload_arith_op(op)
        overload(op, no_unliteral=True)(wtb__jnux)


install_arith_ops()
