"""
Implement support for the various classes in pd.tseries.offsets.
"""
import operator
import llvmlite.binding as ll
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.hiframes.pd_timestamp_ext import get_days_in_month, pd_timestamp_type
from bodo.libs import hdatetime_ext
from bodo.utils.typing import BodoError, create_unsupported_overload, is_overload_none
ll.add_symbol('box_date_offset', hdatetime_ext.box_date_offset)
ll.add_symbol('unbox_date_offset', hdatetime_ext.unbox_date_offset)


class MonthBeginType(types.Type):

    def __init__(self):
        super(MonthBeginType, self).__init__(name='MonthBeginType()')


month_begin_type = MonthBeginType()


@typeof_impl.register(pd.tseries.offsets.MonthBegin)
def typeof_month_begin(val, c):
    return month_begin_type


@register_model(MonthBeginType)
class MonthBeginModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nae__qsct = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthBeginModel, self).__init__(dmm, fe_type, nae__qsct)


@box(MonthBeginType)
def box_month_begin(typ, val, c):
    lnhaq__lzezu = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    exx__ufd = c.pyapi.long_from_longlong(lnhaq__lzezu.n)
    cldf__mcfos = c.pyapi.from_native_value(types.boolean, lnhaq__lzezu.
        normalize, c.env_manager)
    ddum__lhxwc = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthBegin))
    nzon__dab = c.pyapi.call_function_objargs(ddum__lhxwc, (exx__ufd,
        cldf__mcfos))
    c.pyapi.decref(exx__ufd)
    c.pyapi.decref(cldf__mcfos)
    c.pyapi.decref(ddum__lhxwc)
    return nzon__dab


@unbox(MonthBeginType)
def unbox_month_begin(typ, val, c):
    exx__ufd = c.pyapi.object_getattr_string(val, 'n')
    cldf__mcfos = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(exx__ufd)
    normalize = c.pyapi.to_native_value(types.bool_, cldf__mcfos).value
    lnhaq__lzezu = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lnhaq__lzezu.n = n
    lnhaq__lzezu.normalize = normalize
    c.pyapi.decref(exx__ufd)
    c.pyapi.decref(cldf__mcfos)
    zlge__dqnia = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(lnhaq__lzezu._getvalue(), is_error=zlge__dqnia)


@overload(pd.tseries.offsets.MonthBegin, no_unliteral=True)
def MonthBegin(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_begin(n, normalize)
    return impl


@intrinsic
def init_month_begin(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        lnhaq__lzezu = cgutils.create_struct_proxy(typ)(context, builder)
        lnhaq__lzezu.n = args[0]
        lnhaq__lzezu.normalize = args[1]
        return lnhaq__lzezu._getvalue()
    return MonthBeginType()(n, normalize), codegen


make_attribute_wrapper(MonthBeginType, 'n', 'n')
make_attribute_wrapper(MonthBeginType, 'normalize', 'normalize')


@register_jitable
def calculate_month_begin_date(year, month, day, n):
    if n <= 0:
        if day > 1:
            n += 1
    month = month + n
    month -= 1
    year += month // 12
    month = month % 12 + 1
    day = 1
    return year, month, day


def overload_add_operator_month_begin_offset_type(lhs, rhs):
    if lhs == month_begin_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond)
        return impl
    if lhs == month_begin_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond)
        return impl
    if lhs == month_begin_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            return pd.Timestamp(year=year, month=month, day=day)
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == month_begin_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


class MonthEndType(types.Type):

    def __init__(self):
        super(MonthEndType, self).__init__(name='MonthEndType()')


month_end_type = MonthEndType()


@typeof_impl.register(pd.tseries.offsets.MonthEnd)
def typeof_month_end(val, c):
    return month_end_type


@register_model(MonthEndType)
class MonthEndModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nae__qsct = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthEndModel, self).__init__(dmm, fe_type, nae__qsct)


@box(MonthEndType)
def box_month_end(typ, val, c):
    tem__xhbq = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    exx__ufd = c.pyapi.long_from_longlong(tem__xhbq.n)
    cldf__mcfos = c.pyapi.from_native_value(types.boolean, tem__xhbq.
        normalize, c.env_manager)
    eltee__oae = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthEnd))
    nzon__dab = c.pyapi.call_function_objargs(eltee__oae, (exx__ufd,
        cldf__mcfos))
    c.pyapi.decref(exx__ufd)
    c.pyapi.decref(cldf__mcfos)
    c.pyapi.decref(eltee__oae)
    return nzon__dab


@unbox(MonthEndType)
def unbox_month_end(typ, val, c):
    exx__ufd = c.pyapi.object_getattr_string(val, 'n')
    cldf__mcfos = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(exx__ufd)
    normalize = c.pyapi.to_native_value(types.bool_, cldf__mcfos).value
    tem__xhbq = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    tem__xhbq.n = n
    tem__xhbq.normalize = normalize
    c.pyapi.decref(exx__ufd)
    c.pyapi.decref(cldf__mcfos)
    zlge__dqnia = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(tem__xhbq._getvalue(), is_error=zlge__dqnia)


@overload(pd.tseries.offsets.MonthEnd, no_unliteral=True)
def MonthEnd(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_end(n, normalize)
    return impl


@intrinsic
def init_month_end(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        tem__xhbq = cgutils.create_struct_proxy(typ)(context, builder)
        tem__xhbq.n = args[0]
        tem__xhbq.normalize = args[1]
        return tem__xhbq._getvalue()
    return MonthEndType()(n, normalize), codegen


make_attribute_wrapper(MonthEndType, 'n', 'n')
make_attribute_wrapper(MonthEndType, 'normalize', 'normalize')


@lower_constant(MonthBeginType)
@lower_constant(MonthEndType)
def lower_constant_month_end(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    return lir.Constant.literal_struct([n, normalize])


@register_jitable
def calculate_month_end_date(year, month, day, n):
    if n > 0:
        tem__xhbq = get_days_in_month(year, month)
        if tem__xhbq > day:
            n -= 1
    month = month + n
    month -= 1
    year += month // 12
    month = month % 12 + 1
    day = get_days_in_month(year, month)
    return year, month, day


def overload_add_operator_month_end_offset_type(lhs, rhs):
    if lhs == month_end_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond)
        return impl
    if lhs == month_end_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond)
        return impl
    if lhs == month_end_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            return pd.Timestamp(year=year, month=month, day=day)
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == month_end_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


def overload_mul_date_offset_types(lhs, rhs):
    if lhs == month_begin_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.MonthBegin(lhs.n * rhs, lhs.normalize)
    if lhs == month_end_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.MonthEnd(lhs.n * rhs, lhs.normalize)
    if lhs == week_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.Week(lhs.n * rhs, lhs.normalize, lhs.
                weekday)
    if lhs == date_offset_type:

        def impl(lhs, rhs):
            n = lhs.n * rhs
            normalize = lhs.normalize
            nanoseconds = lhs._nanoseconds
            nanosecond = lhs._nanosecond
            if lhs._has_kws:
                years = lhs._years
                months = lhs._months
                weeks = lhs._weeks
                days = lhs._days
                hours = lhs._hours
                minutes = lhs._minutes
                seconds = lhs._seconds
                microseconds = lhs._microseconds
                year = lhs._year
                month = lhs._month
                day = lhs._day
                weekday = lhs._weekday
                hour = lhs._hour
                minute = lhs._minute
                second = lhs._second
                microsecond = lhs._microsecond
                return pd.tseries.offsets.DateOffset(n, normalize, years,
                    months, weeks, days, hours, minutes, seconds,
                    microseconds, nanoseconds, year, month, day, weekday,
                    hour, minute, second, microsecond, nanosecond)
            else:
                return pd.tseries.offsets.DateOffset(n, normalize,
                    nanoseconds=nanoseconds, nanosecond=nanosecond)
    if rhs in [week_type, month_end_type, month_begin_type, date_offset_type]:

        def impl(lhs, rhs):
            return rhs * lhs
        return impl
    return impl


class DateOffsetType(types.Type):

    def __init__(self):
        super(DateOffsetType, self).__init__(name='DateOffsetType()')


date_offset_type = DateOffsetType()
date_offset_fields = ['years', 'months', 'weeks', 'days', 'hours',
    'minutes', 'seconds', 'microseconds', 'nanoseconds', 'year', 'month',
    'day', 'weekday', 'hour', 'minute', 'second', 'microsecond', 'nanosecond']


@typeof_impl.register(pd.tseries.offsets.DateOffset)
def type_of_date_offset(val, c):
    return date_offset_type


@register_model(DateOffsetType)
class DateOffsetModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nae__qsct = [('n', types.int64), ('normalize', types.boolean), (
            'years', types.int64), ('months', types.int64), ('weeks', types
            .int64), ('days', types.int64), ('hours', types.int64), (
            'minutes', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64), ('nanoseconds', types.int64), (
            'year', types.int64), ('month', types.int64), ('day', types.
            int64), ('weekday', types.int64), ('hour', types.int64), (
            'minute', types.int64), ('second', types.int64), ('microsecond',
            types.int64), ('nanosecond', types.int64), ('has_kws', types.
            boolean)]
        super(DateOffsetModel, self).__init__(dmm, fe_type, nae__qsct)


@box(DateOffsetType)
def box_date_offset(typ, val, c):
    ipi__ljkvv = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    tiwe__ndgm = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    for esg__yqrk, kfk__gbdsl in enumerate(date_offset_fields):
        c.builder.store(getattr(ipi__ljkvv, kfk__gbdsl), c.builder.inttoptr
            (c.builder.add(c.builder.ptrtoint(tiwe__ndgm, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * esg__yqrk)), lir.IntType(64).
            as_pointer()))
    ibh__pjq = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(1), lir.IntType(64).as_pointer(), lir.IntType(1)])
    wkz__fbc = cgutils.get_or_insert_function(c.builder.module, ibh__pjq,
        name='box_date_offset')
    cvjr__ngdev = c.builder.call(wkz__fbc, [ipi__ljkvv.n, ipi__ljkvv.
        normalize, tiwe__ndgm, ipi__ljkvv.has_kws])
    c.context.nrt.decref(c.builder, typ, val)
    return cvjr__ngdev


@unbox(DateOffsetType)
def unbox_date_offset(typ, val, c):
    exx__ufd = c.pyapi.object_getattr_string(val, 'n')
    cldf__mcfos = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(exx__ufd)
    normalize = c.pyapi.to_native_value(types.bool_, cldf__mcfos).value
    tiwe__ndgm = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    ibh__pjq = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer(
        ), lir.IntType(64).as_pointer()])
    fui__mzjb = cgutils.get_or_insert_function(c.builder.module, ibh__pjq,
        name='unbox_date_offset')
    has_kws = c.builder.call(fui__mzjb, [val, tiwe__ndgm])
    ipi__ljkvv = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ipi__ljkvv.n = n
    ipi__ljkvv.normalize = normalize
    for esg__yqrk, kfk__gbdsl in enumerate(date_offset_fields):
        setattr(ipi__ljkvv, kfk__gbdsl, c.builder.load(c.builder.inttoptr(c
            .builder.add(c.builder.ptrtoint(tiwe__ndgm, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * esg__yqrk)), lir.IntType(64).
            as_pointer())))
    ipi__ljkvv.has_kws = has_kws
    c.pyapi.decref(exx__ufd)
    c.pyapi.decref(cldf__mcfos)
    zlge__dqnia = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ipi__ljkvv._getvalue(), is_error=zlge__dqnia)


@lower_constant(DateOffsetType)
def lower_constant_date_offset(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    caems__whrm = [n, normalize]
    has_kws = False
    icd__letej = [0] * 9 + [-1] * 9
    for esg__yqrk, kfk__gbdsl in enumerate(date_offset_fields):
        if hasattr(pyval, kfk__gbdsl):
            smer__zae = context.get_constant(types.int64, getattr(pyval,
                kfk__gbdsl))
            if kfk__gbdsl != 'nanoseconds' and kfk__gbdsl != 'nanosecond':
                has_kws = True
        else:
            smer__zae = context.get_constant(types.int64, icd__letej[esg__yqrk]
                )
        caems__whrm.append(smer__zae)
    has_kws = context.get_constant(types.boolean, has_kws)
    caems__whrm.append(has_kws)
    return lir.Constant.literal_struct(caems__whrm)


@overload(pd.tseries.offsets.DateOffset, no_unliteral=True)
def DateOffset(n=1, normalize=False, years=None, months=None, weeks=None,
    days=None, hours=None, minutes=None, seconds=None, microseconds=None,
    nanoseconds=None, year=None, month=None, day=None, weekday=None, hour=
    None, minute=None, second=None, microsecond=None, nanosecond=None):
    has_kws = False
    wkx__cbjv = [years, months, weeks, days, hours, minutes, seconds,
        microseconds, year, month, day, weekday, hour, minute, second,
        microsecond]
    for hmys__rihvd in wkx__cbjv:
        if not is_overload_none(hmys__rihvd):
            has_kws = True
            break

    def impl(n=1, normalize=False, years=None, months=None, weeks=None,
        days=None, hours=None, minutes=None, seconds=None, microseconds=
        None, nanoseconds=None, year=None, month=None, day=None, weekday=
        None, hour=None, minute=None, second=None, microsecond=None,
        nanosecond=None):
        years = 0 if years is None else years
        months = 0 if months is None else months
        weeks = 0 if weeks is None else weeks
        days = 0 if days is None else days
        hours = 0 if hours is None else hours
        minutes = 0 if minutes is None else minutes
        seconds = 0 if seconds is None else seconds
        microseconds = 0 if microseconds is None else microseconds
        nanoseconds = 0 if nanoseconds is None else nanoseconds
        year = -1 if year is None else year
        month = -1 if month is None else month
        weekday = -1 if weekday is None else weekday
        day = -1 if day is None else day
        hour = -1 if hour is None else hour
        minute = -1 if minute is None else minute
        second = -1 if second is None else second
        microsecond = -1 if microsecond is None else microsecond
        nanosecond = -1 if nanosecond is None else nanosecond
        return init_date_offset(n, normalize, years, months, weeks, days,
            hours, minutes, seconds, microseconds, nanoseconds, year, month,
            day, weekday, hour, minute, second, microsecond, nanosecond,
            has_kws)
    return impl


@intrinsic
def init_date_offset(typingctx, n, normalize, years, months, weeks, days,
    hours, minutes, seconds, microseconds, nanoseconds, year, month, day,
    weekday, hour, minute, second, microsecond, nanosecond, has_kws):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        ipi__ljkvv = cgutils.create_struct_proxy(typ)(context, builder)
        ipi__ljkvv.n = args[0]
        ipi__ljkvv.normalize = args[1]
        ipi__ljkvv.years = args[2]
        ipi__ljkvv.months = args[3]
        ipi__ljkvv.weeks = args[4]
        ipi__ljkvv.days = args[5]
        ipi__ljkvv.hours = args[6]
        ipi__ljkvv.minutes = args[7]
        ipi__ljkvv.seconds = args[8]
        ipi__ljkvv.microseconds = args[9]
        ipi__ljkvv.nanoseconds = args[10]
        ipi__ljkvv.year = args[11]
        ipi__ljkvv.month = args[12]
        ipi__ljkvv.day = args[13]
        ipi__ljkvv.weekday = args[14]
        ipi__ljkvv.hour = args[15]
        ipi__ljkvv.minute = args[16]
        ipi__ljkvv.second = args[17]
        ipi__ljkvv.microsecond = args[18]
        ipi__ljkvv.nanosecond = args[19]
        ipi__ljkvv.has_kws = args[20]
        return ipi__ljkvv._getvalue()
    return DateOffsetType()(n, normalize, years, months, weeks, days, hours,
        minutes, seconds, microseconds, nanoseconds, year, month, day,
        weekday, hour, minute, second, microsecond, nanosecond, has_kws
        ), codegen


make_attribute_wrapper(DateOffsetType, 'n', 'n')
make_attribute_wrapper(DateOffsetType, 'normalize', 'normalize')
make_attribute_wrapper(DateOffsetType, 'years', '_years')
make_attribute_wrapper(DateOffsetType, 'months', '_months')
make_attribute_wrapper(DateOffsetType, 'weeks', '_weeks')
make_attribute_wrapper(DateOffsetType, 'days', '_days')
make_attribute_wrapper(DateOffsetType, 'hours', '_hours')
make_attribute_wrapper(DateOffsetType, 'minutes', '_minutes')
make_attribute_wrapper(DateOffsetType, 'seconds', '_seconds')
make_attribute_wrapper(DateOffsetType, 'microseconds', '_microseconds')
make_attribute_wrapper(DateOffsetType, 'nanoseconds', '_nanoseconds')
make_attribute_wrapper(DateOffsetType, 'year', '_year')
make_attribute_wrapper(DateOffsetType, 'month', '_month')
make_attribute_wrapper(DateOffsetType, 'weekday', '_weekday')
make_attribute_wrapper(DateOffsetType, 'day', '_day')
make_attribute_wrapper(DateOffsetType, 'hour', '_hour')
make_attribute_wrapper(DateOffsetType, 'minute', '_minute')
make_attribute_wrapper(DateOffsetType, 'second', '_second')
make_attribute_wrapper(DateOffsetType, 'microsecond', '_microsecond')
make_attribute_wrapper(DateOffsetType, 'nanosecond', '_nanosecond')
make_attribute_wrapper(DateOffsetType, 'has_kws', '_has_kws')


@register_jitable
def relative_delta_addition(dateoffset, ts):
    if dateoffset._has_kws:
        uvsi__yji = -1 if dateoffset.n < 0 else 1
        for racm__hdmv in range(np.abs(dateoffset.n)):
            year = ts.year
            month = ts.month
            day = ts.day
            hour = ts.hour
            minute = ts.minute
            second = ts.second
            microsecond = ts.microsecond
            nanosecond = ts.nanosecond
            if dateoffset._year != -1:
                year = dateoffset._year
            year += uvsi__yji * dateoffset._years
            if dateoffset._month != -1:
                month = dateoffset._month
            month += uvsi__yji * dateoffset._months
            year, month, ftotv__hzy = calculate_month_end_date(year, month,
                day, 0)
            if day > ftotv__hzy:
                day = ftotv__hzy
            if dateoffset._day != -1:
                day = dateoffset._day
            if dateoffset._hour != -1:
                hour = dateoffset._hour
            if dateoffset._minute != -1:
                minute = dateoffset._minute
            if dateoffset._second != -1:
                second = dateoffset._second
            if dateoffset._microsecond != -1:
                microsecond = dateoffset._microsecond
            ts = pd.Timestamp(year=year, month=month, day=day, hour=hour,
                minute=minute, second=second, microsecond=microsecond,
                nanosecond=nanosecond)
            ycyow__gjir = pd.Timedelta(days=dateoffset._days + 7 *
                dateoffset._weeks, hours=dateoffset._hours, minutes=
                dateoffset._minutes, seconds=dateoffset._seconds,
                microseconds=dateoffset._microseconds)
            if uvsi__yji == -1:
                ycyow__gjir = -ycyow__gjir
            ts = ts + ycyow__gjir
            if dateoffset._weekday != -1:
                ntm__apku = ts.weekday()
                dkyhd__mmqo = (dateoffset._weekday - ntm__apku) % 7
                ts = ts + pd.Timedelta(days=dkyhd__mmqo)
        return ts
    else:
        return pd.Timedelta(days=dateoffset.n) + ts


def overload_add_operator_date_offset_type(lhs, rhs):
    if lhs == date_offset_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            ts = relative_delta_addition(lhs, rhs)
            if lhs.normalize:
                return ts.normalize()
            return ts
        return impl
    if lhs == date_offset_type and rhs in [datetime_date_type,
        datetime_datetime_type]:

        def impl(lhs, rhs):
            ts = relative_delta_addition(lhs, pd.Timestamp(rhs))
            if lhs.normalize:
                return ts.normalize()
            return ts
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == date_offset_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


def overload_sub_operator_offsets(lhs, rhs):
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs in [date_offset_type, month_begin_type, month_end_type,
        week_type]:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl


@overload(operator.neg, no_unliteral=True)
def overload_neg(lhs):
    if lhs == month_begin_type:

        def impl(lhs):
            return pd.tseries.offsets.MonthBegin(-lhs.n, lhs.normalize)
    if lhs == month_end_type:

        def impl(lhs):
            return pd.tseries.offsets.MonthEnd(-lhs.n, lhs.normalize)
    if lhs == week_type:

        def impl(lhs):
            return pd.tseries.offsets.Week(-lhs.n, lhs.normalize, lhs.weekday)
    if lhs == date_offset_type:

        def impl(lhs):
            n = -lhs.n
            normalize = lhs.normalize
            nanoseconds = lhs._nanoseconds
            nanosecond = lhs._nanosecond
            if lhs._has_kws:
                years = lhs._years
                months = lhs._months
                weeks = lhs._weeks
                days = lhs._days
                hours = lhs._hours
                minutes = lhs._minutes
                seconds = lhs._seconds
                microseconds = lhs._microseconds
                year = lhs._year
                month = lhs._month
                day = lhs._day
                weekday = lhs._weekday
                hour = lhs._hour
                minute = lhs._minute
                second = lhs._second
                microsecond = lhs._microsecond
                return pd.tseries.offsets.DateOffset(n, normalize, years,
                    months, weeks, days, hours, minutes, seconds,
                    microseconds, nanoseconds, year, month, day, weekday,
                    hour, minute, second, microsecond, nanosecond)
            else:
                return pd.tseries.offsets.DateOffset(n, normalize,
                    nanoseconds=nanoseconds, nanosecond=nanosecond)
    return impl


def is_offsets_type(val):
    return val in [date_offset_type, month_begin_type, month_end_type,
        week_type]


class WeekType(types.Type):

    def __init__(self):
        super(WeekType, self).__init__(name='WeekType()')


week_type = WeekType()


@typeof_impl.register(pd.tseries.offsets.Week)
def typeof_week(val, c):
    return week_type


@register_model(WeekType)
class WeekModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nae__qsct = [('n', types.int64), ('normalize', types.boolean), (
            'weekday', types.int64)]
        super(WeekModel, self).__init__(dmm, fe_type, nae__qsct)


make_attribute_wrapper(WeekType, 'n', 'n')
make_attribute_wrapper(WeekType, 'normalize', 'normalize')
make_attribute_wrapper(WeekType, 'weekday', 'weekday')


@overload(pd.tseries.offsets.Week, no_unliteral=True)
def Week(n=1, normalize=False, weekday=None):

    def impl(n=1, normalize=False, weekday=None):
        dvt__vwqc = -1 if weekday is None else weekday
        return init_week(n, normalize, dvt__vwqc)
    return impl


@intrinsic
def init_week(typingctx, n, normalize, weekday):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        yzc__trsrv = cgutils.create_struct_proxy(typ)(context, builder)
        yzc__trsrv.n = args[0]
        yzc__trsrv.normalize = args[1]
        yzc__trsrv.weekday = args[2]
        return yzc__trsrv._getvalue()
    return WeekType()(n, normalize, weekday), codegen


@lower_constant(WeekType)
def lower_constant_week(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    if pyval.weekday is not None:
        weekday = context.get_constant(types.int64, pyval.weekday)
    else:
        weekday = context.get_constant(types.int64, -1)
    return lir.Constant.literal_struct([n, normalize, weekday])


@box(WeekType)
def box_week(typ, val, c):
    yzc__trsrv = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    exx__ufd = c.pyapi.long_from_longlong(yzc__trsrv.n)
    cldf__mcfos = c.pyapi.from_native_value(types.boolean, yzc__trsrv.
        normalize, c.env_manager)
    cej__beq = c.pyapi.long_from_longlong(yzc__trsrv.weekday)
    uxfc__voy = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.Week))
    tdt__ihkv = c.builder.icmp_signed('!=', lir.Constant(lir.IntType(64), -
        1), yzc__trsrv.weekday)
    with c.builder.if_else(tdt__ihkv) as (weekday_defined, weekday_undefined):
        with weekday_defined:
            psq__rdxl = c.pyapi.call_function_objargs(uxfc__voy, (exx__ufd,
                cldf__mcfos, cej__beq))
            xwzu__jnsl = c.builder.block
        with weekday_undefined:
            inirl__ypuar = c.pyapi.call_function_objargs(uxfc__voy, (
                exx__ufd, cldf__mcfos))
            bixg__jdmq = c.builder.block
    nzon__dab = c.builder.phi(psq__rdxl.type)
    nzon__dab.add_incoming(psq__rdxl, xwzu__jnsl)
    nzon__dab.add_incoming(inirl__ypuar, bixg__jdmq)
    c.pyapi.decref(cej__beq)
    c.pyapi.decref(exx__ufd)
    c.pyapi.decref(cldf__mcfos)
    c.pyapi.decref(uxfc__voy)
    return nzon__dab


@unbox(WeekType)
def unbox_week(typ, val, c):
    exx__ufd = c.pyapi.object_getattr_string(val, 'n')
    cldf__mcfos = c.pyapi.object_getattr_string(val, 'normalize')
    cej__beq = c.pyapi.object_getattr_string(val, 'weekday')
    n = c.pyapi.long_as_longlong(exx__ufd)
    normalize = c.pyapi.to_native_value(types.bool_, cldf__mcfos).value
    yjimu__emxv = c.pyapi.make_none()
    her__tajgz = c.builder.icmp_unsigned('==', cej__beq, yjimu__emxv)
    with c.builder.if_else(her__tajgz) as (weekday_undefined, weekday_defined):
        with weekday_defined:
            psq__rdxl = c.pyapi.long_as_longlong(cej__beq)
            xwzu__jnsl = c.builder.block
        with weekday_undefined:
            inirl__ypuar = lir.Constant(lir.IntType(64), -1)
            bixg__jdmq = c.builder.block
    nzon__dab = c.builder.phi(psq__rdxl.type)
    nzon__dab.add_incoming(psq__rdxl, xwzu__jnsl)
    nzon__dab.add_incoming(inirl__ypuar, bixg__jdmq)
    yzc__trsrv = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    yzc__trsrv.n = n
    yzc__trsrv.normalize = normalize
    yzc__trsrv.weekday = nzon__dab
    c.pyapi.decref(exx__ufd)
    c.pyapi.decref(cldf__mcfos)
    c.pyapi.decref(cej__beq)
    zlge__dqnia = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(yzc__trsrv._getvalue(), is_error=zlge__dqnia)


def overload_add_operator_week_offset_type(lhs, rhs):
    if lhs == week_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            slz__xbb = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            if lhs.normalize:
                nrqsb__grb = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                nrqsb__grb = rhs
            return nrqsb__grb + slz__xbb
        return impl
    if lhs == week_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            slz__xbb = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            if lhs.normalize:
                nrqsb__grb = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                nrqsb__grb = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day, hour=rhs.hour, minute=rhs.minute, second=
                    rhs.second, microsecond=rhs.microsecond)
            return nrqsb__grb + slz__xbb
        return impl
    if lhs == week_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            slz__xbb = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            return rhs + slz__xbb
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == week_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


@register_jitable
def calculate_week_date(n, weekday, other_weekday):
    if weekday == -1:
        return pd.Timedelta(weeks=n)
    if weekday != other_weekday:
        qna__wldd = (weekday - other_weekday) % 7
        if n > 0:
            n = n - 1
    return pd.Timedelta(weeks=n, days=qna__wldd)


date_offset_unsupported_attrs = {'base', 'freqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
date_offset_unsupported = {'__call__', 'rollback', 'rollforward',
    'is_month_start', 'is_month_end', 'apply', 'apply_index', 'copy',
    'isAnchored', 'onOffset', 'is_anchored', 'is_on_offset',
    'is_quarter_start', 'is_quarter_end', 'is_year_start', 'is_year_end'}
month_end_unsupported_attrs = {'base', 'freqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
month_end_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
month_begin_unsupported_attrs = {'basefreqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
month_begin_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
week_unsupported_attrs = {'basefreqstr', 'kwds', 'name', 'nanos', 'rule_code'}
week_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
offsets_unsupported = {pd.tseries.offsets.BusinessDay, pd.tseries.offsets.
    BDay, pd.tseries.offsets.BusinessHour, pd.tseries.offsets.
    CustomBusinessDay, pd.tseries.offsets.CDay, pd.tseries.offsets.
    CustomBusinessHour, pd.tseries.offsets.BusinessMonthEnd, pd.tseries.
    offsets.BMonthEnd, pd.tseries.offsets.BusinessMonthBegin, pd.tseries.
    offsets.BMonthBegin, pd.tseries.offsets.CustomBusinessMonthEnd, pd.
    tseries.offsets.CBMonthEnd, pd.tseries.offsets.CustomBusinessMonthBegin,
    pd.tseries.offsets.CBMonthBegin, pd.tseries.offsets.SemiMonthEnd, pd.
    tseries.offsets.SemiMonthBegin, pd.tseries.offsets.WeekOfMonth, pd.
    tseries.offsets.LastWeekOfMonth, pd.tseries.offsets.BQuarterEnd, pd.
    tseries.offsets.BQuarterBegin, pd.tseries.offsets.QuarterEnd, pd.
    tseries.offsets.QuarterBegin, pd.tseries.offsets.BYearEnd, pd.tseries.
    offsets.BYearBegin, pd.tseries.offsets.YearEnd, pd.tseries.offsets.
    YearBegin, pd.tseries.offsets.FY5253, pd.tseries.offsets.FY5253Quarter,
    pd.tseries.offsets.Easter, pd.tseries.offsets.Tick, pd.tseries.offsets.
    Day, pd.tseries.offsets.Hour, pd.tseries.offsets.Minute, pd.tseries.
    offsets.Second, pd.tseries.offsets.Milli, pd.tseries.offsets.Micro, pd.
    tseries.offsets.Nano}
frequencies_unsupported = {pd.tseries.frequencies.to_offset}


def _install_date_offsets_unsupported():
    for keboa__wib in date_offset_unsupported_attrs:
        mxnaj__trd = 'pandas.tseries.offsets.DateOffset.' + keboa__wib
        overload_attribute(DateOffsetType, keboa__wib)(
            create_unsupported_overload(mxnaj__trd))
    for keboa__wib in date_offset_unsupported:
        mxnaj__trd = 'pandas.tseries.offsets.DateOffset.' + keboa__wib
        overload_method(DateOffsetType, keboa__wib)(create_unsupported_overload
            (mxnaj__trd))


def _install_month_begin_unsupported():
    for keboa__wib in month_begin_unsupported_attrs:
        mxnaj__trd = 'pandas.tseries.offsets.MonthBegin.' + keboa__wib
        overload_attribute(MonthBeginType, keboa__wib)(
            create_unsupported_overload(mxnaj__trd))
    for keboa__wib in month_begin_unsupported:
        mxnaj__trd = 'pandas.tseries.offsets.MonthBegin.' + keboa__wib
        overload_method(MonthBeginType, keboa__wib)(create_unsupported_overload
            (mxnaj__trd))


def _install_month_end_unsupported():
    for keboa__wib in date_offset_unsupported_attrs:
        mxnaj__trd = 'pandas.tseries.offsets.MonthEnd.' + keboa__wib
        overload_attribute(MonthEndType, keboa__wib)(
            create_unsupported_overload(mxnaj__trd))
    for keboa__wib in date_offset_unsupported:
        mxnaj__trd = 'pandas.tseries.offsets.MonthEnd.' + keboa__wib
        overload_method(MonthEndType, keboa__wib)(create_unsupported_overload
            (mxnaj__trd))


def _install_week_unsupported():
    for keboa__wib in week_unsupported_attrs:
        mxnaj__trd = 'pandas.tseries.offsets.Week.' + keboa__wib
        overload_attribute(WeekType, keboa__wib)(create_unsupported_overload
            (mxnaj__trd))
    for keboa__wib in week_unsupported:
        mxnaj__trd = 'pandas.tseries.offsets.Week.' + keboa__wib
        overload_method(WeekType, keboa__wib)(create_unsupported_overload(
            mxnaj__trd))


def _install_offsets_unsupported():
    for smer__zae in offsets_unsupported:
        mxnaj__trd = 'pandas.tseries.offsets.' + smer__zae.__name__
        overload(smer__zae)(create_unsupported_overload(mxnaj__trd))


def _install_frequencies_unsupported():
    for smer__zae in frequencies_unsupported:
        mxnaj__trd = 'pandas.tseries.frequencies.' + smer__zae.__name__
        overload(smer__zae)(create_unsupported_overload(mxnaj__trd))


_install_date_offsets_unsupported()
_install_month_begin_unsupported()
_install_month_end_unsupported()
_install_week_unsupported()
_install_offsets_unsupported()
_install_frequencies_unsupported()
