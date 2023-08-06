import datetime
import numba
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
"""
Implementation is based on
https://github.com/python/cpython/blob/39a5c889d30d03a88102e56f03ee0c95db198fb3/Lib/datetime.py
"""


class DatetimeDatetimeType(types.Type):

    def __init__(self):
        super(DatetimeDatetimeType, self).__init__(name=
            'DatetimeDatetimeType()')


datetime_datetime_type = DatetimeDatetimeType()
types.datetime_datetime_type = datetime_datetime_type


@typeof_impl.register(datetime.datetime)
def typeof_datetime_datetime(val, c):
    return datetime_datetime_type


@register_model(DatetimeDatetimeType)
class DatetimeDateTimeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        uljv__eubu = [('year', types.int64), ('month', types.int64), ('day',
            types.int64), ('hour', types.int64), ('minute', types.int64), (
            'second', types.int64), ('microsecond', types.int64)]
        super(DatetimeDateTimeModel, self).__init__(dmm, fe_type, uljv__eubu)


@box(DatetimeDatetimeType)
def box_datetime_datetime(typ, val, c):
    vez__qak = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val
        )
    yonk__zbmp = c.pyapi.long_from_longlong(vez__qak.year)
    kwcng__qvaz = c.pyapi.long_from_longlong(vez__qak.month)
    sika__mlmhl = c.pyapi.long_from_longlong(vez__qak.day)
    byz__fzqdq = c.pyapi.long_from_longlong(vez__qak.hour)
    ffx__yue = c.pyapi.long_from_longlong(vez__qak.minute)
    uywn__eidn = c.pyapi.long_from_longlong(vez__qak.second)
    kvmbb__aff = c.pyapi.long_from_longlong(vez__qak.microsecond)
    ecor__mnsru = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        datetime))
    zpwqf__wgua = c.pyapi.call_function_objargs(ecor__mnsru, (yonk__zbmp,
        kwcng__qvaz, sika__mlmhl, byz__fzqdq, ffx__yue, uywn__eidn, kvmbb__aff)
        )
    c.pyapi.decref(yonk__zbmp)
    c.pyapi.decref(kwcng__qvaz)
    c.pyapi.decref(sika__mlmhl)
    c.pyapi.decref(byz__fzqdq)
    c.pyapi.decref(ffx__yue)
    c.pyapi.decref(uywn__eidn)
    c.pyapi.decref(kvmbb__aff)
    c.pyapi.decref(ecor__mnsru)
    return zpwqf__wgua


@unbox(DatetimeDatetimeType)
def unbox_datetime_datetime(typ, val, c):
    yonk__zbmp = c.pyapi.object_getattr_string(val, 'year')
    kwcng__qvaz = c.pyapi.object_getattr_string(val, 'month')
    sika__mlmhl = c.pyapi.object_getattr_string(val, 'day')
    byz__fzqdq = c.pyapi.object_getattr_string(val, 'hour')
    ffx__yue = c.pyapi.object_getattr_string(val, 'minute')
    uywn__eidn = c.pyapi.object_getattr_string(val, 'second')
    kvmbb__aff = c.pyapi.object_getattr_string(val, 'microsecond')
    vez__qak = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    vez__qak.year = c.pyapi.long_as_longlong(yonk__zbmp)
    vez__qak.month = c.pyapi.long_as_longlong(kwcng__qvaz)
    vez__qak.day = c.pyapi.long_as_longlong(sika__mlmhl)
    vez__qak.hour = c.pyapi.long_as_longlong(byz__fzqdq)
    vez__qak.minute = c.pyapi.long_as_longlong(ffx__yue)
    vez__qak.second = c.pyapi.long_as_longlong(uywn__eidn)
    vez__qak.microsecond = c.pyapi.long_as_longlong(kvmbb__aff)
    c.pyapi.decref(yonk__zbmp)
    c.pyapi.decref(kwcng__qvaz)
    c.pyapi.decref(sika__mlmhl)
    c.pyapi.decref(byz__fzqdq)
    c.pyapi.decref(ffx__yue)
    c.pyapi.decref(uywn__eidn)
    c.pyapi.decref(kvmbb__aff)
    sfda__mxnf = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(vez__qak._getvalue(), is_error=sfda__mxnf)


@lower_constant(DatetimeDatetimeType)
def constant_datetime(context, builder, ty, pyval):
    year = context.get_constant(types.int64, pyval.year)
    month = context.get_constant(types.int64, pyval.month)
    day = context.get_constant(types.int64, pyval.day)
    hour = context.get_constant(types.int64, pyval.hour)
    minute = context.get_constant(types.int64, pyval.minute)
    second = context.get_constant(types.int64, pyval.second)
    microsecond = context.get_constant(types.int64, pyval.microsecond)
    return lir.Constant.literal_struct([year, month, day, hour, minute,
        second, microsecond])


@overload(datetime.datetime, no_unliteral=True)
def datetime_datetime(year, month, day, hour=0, minute=0, second=0,
    microsecond=0):

    def impl_datetime(year, month, day, hour=0, minute=0, second=0,
        microsecond=0):
        return init_datetime(year, month, day, hour, minute, second,
            microsecond)
    return impl_datetime


@intrinsic
def init_datetime(typingctx, year, month, day, hour, minute, second,
    microsecond):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        vez__qak = cgutils.create_struct_proxy(typ)(context, builder)
        vez__qak.year = args[0]
        vez__qak.month = args[1]
        vez__qak.day = args[2]
        vez__qak.hour = args[3]
        vez__qak.minute = args[4]
        vez__qak.second = args[5]
        vez__qak.microsecond = args[6]
        return vez__qak._getvalue()
    return DatetimeDatetimeType()(year, month, day, hour, minute, second,
        microsecond), codegen


make_attribute_wrapper(DatetimeDatetimeType, 'year', '_year')
make_attribute_wrapper(DatetimeDatetimeType, 'month', '_month')
make_attribute_wrapper(DatetimeDatetimeType, 'day', '_day')
make_attribute_wrapper(DatetimeDatetimeType, 'hour', '_hour')
make_attribute_wrapper(DatetimeDatetimeType, 'minute', '_minute')
make_attribute_wrapper(DatetimeDatetimeType, 'second', '_second')
make_attribute_wrapper(DatetimeDatetimeType, 'microsecond', '_microsecond')


@overload_attribute(DatetimeDatetimeType, 'year')
def datetime_get_year(dt):

    def impl(dt):
        return dt._year
    return impl


@overload_attribute(DatetimeDatetimeType, 'month')
def datetime_get_month(dt):

    def impl(dt):
        return dt._month
    return impl


@overload_attribute(DatetimeDatetimeType, 'day')
def datetime_get_day(dt):

    def impl(dt):
        return dt._day
    return impl


@overload_attribute(DatetimeDatetimeType, 'hour')
def datetime_get_hour(dt):

    def impl(dt):
        return dt._hour
    return impl


@overload_attribute(DatetimeDatetimeType, 'minute')
def datetime_get_minute(dt):

    def impl(dt):
        return dt._minute
    return impl


@overload_attribute(DatetimeDatetimeType, 'second')
def datetime_get_second(dt):

    def impl(dt):
        return dt._second
    return impl


@overload_attribute(DatetimeDatetimeType, 'microsecond')
def datetime_get_microsecond(dt):

    def impl(dt):
        return dt._microsecond
    return impl


@overload_method(DatetimeDatetimeType, 'date', no_unliteral=True)
def date(dt):

    def impl(dt):
        return datetime.date(dt.year, dt.month, dt.day)
    return impl


@register_jitable
def now_impl():
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.now()
    return d


@register_jitable
def today_impl():
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.today()
    return d


@register_jitable
def strptime_impl(date_string, dtformat):
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.strptime(date_string, dtformat)
    return d


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


def create_cmp_op_overload(op):

    def overload_datetime_cmp(lhs, rhs):
        if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

            def impl(lhs, rhs):
                y, ssaze__vajo = lhs.year, rhs.year
                quk__koq, urp__wqe = lhs.month, rhs.month
                d, qahqh__kutld = lhs.day, rhs.day
                bwzma__zpsf, fuwbi__qhcel = lhs.hour, rhs.hour
                csob__rsea, dhvb__qxg = lhs.minute, rhs.minute
                usou__pqww, uspxv__fsz = lhs.second, rhs.second
                etrk__lnxoe, nopy__lqzc = lhs.microsecond, rhs.microsecond
                return op(_cmp((y, quk__koq, d, bwzma__zpsf, csob__rsea,
                    usou__pqww, etrk__lnxoe), (ssaze__vajo, urp__wqe,
                    qahqh__kutld, fuwbi__qhcel, dhvb__qxg, uspxv__fsz,
                    nopy__lqzc)), 0)
            return impl
    return overload_datetime_cmp


def overload_sub_operator_datetime_datetime(lhs, rhs):
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            mhwtc__mqi = lhs.toordinal()
            bpibg__zra = rhs.toordinal()
            gvsef__mootm = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            fss__jyw = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            nbpu__cyc = datetime.timedelta(mhwtc__mqi - bpibg__zra, 
                gvsef__mootm - fss__jyw, lhs.microsecond - rhs.microsecond)
            return nbpu__cyc
        return impl


@lower_cast(types.Optional(numba.core.types.NPTimedelta('ns')), numba.core.
    types.NPTimedelta('ns'))
@lower_cast(types.Optional(numba.core.types.NPDatetime('ns')), numba.core.
    types.NPDatetime('ns'))
def optional_dt64_to_dt64(context, builder, fromty, toty, val):
    fvt__gpahy = context.make_helper(builder, fromty, value=val)
    tkcf__xyxm = cgutils.as_bool_bit(builder, fvt__gpahy.valid)
    with builder.if_else(tkcf__xyxm) as (then, orelse):
        with then:
            nglu__fvy = context.cast(builder, fvt__gpahy.data, fromty.type,
                toty)
            cyud__zpprd = builder.block
        with orelse:
            emy__xhrva = numba.np.npdatetime.NAT
            wbk__edpb = builder.block
    zpwqf__wgua = builder.phi(nglu__fvy.type)
    zpwqf__wgua.add_incoming(nglu__fvy, cyud__zpprd)
    zpwqf__wgua.add_incoming(emy__xhrva, wbk__edpb)
    return zpwqf__wgua
