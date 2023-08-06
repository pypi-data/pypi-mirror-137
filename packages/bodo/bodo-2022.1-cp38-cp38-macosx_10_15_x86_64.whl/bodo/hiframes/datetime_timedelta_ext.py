"""Numba extension support for datetime.timedelta objects and their arrays.
"""
import datetime
import operator
from collections import namedtuple
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.libs import hdatetime_ext
from bodo.utils.indexing import get_new_null_mask_bool_index, get_new_null_mask_int_index, get_new_null_mask_slice_index, setitem_slice_index_null_bits
from bodo.utils.typing import BodoError, get_overload_const_str, is_iterable_type, is_list_like_index_type, is_overload_constant_str
ll.add_symbol('box_datetime_timedelta_array', hdatetime_ext.
    box_datetime_timedelta_array)
ll.add_symbol('unbox_datetime_timedelta_array', hdatetime_ext.
    unbox_datetime_timedelta_array)


class NoInput:
    pass


_no_input = NoInput()


class NoInputType(types.Type):

    def __init__(self):
        super(NoInputType, self).__init__(name='NoInput')


register_model(NoInputType)(models.OpaqueModel)


@typeof_impl.register(NoInput)
def _typ_no_input(val, c):
    return NoInputType()


@lower_constant(NoInputType)
def constant_no_input(context, builder, ty, pyval):
    return context.get_dummy_value()


class PDTimeDeltaType(types.Type):

    def __init__(self):
        super(PDTimeDeltaType, self).__init__(name='PDTimeDeltaType()')


pd_timedelta_type = PDTimeDeltaType()
types.pd_timedelta_type = pd_timedelta_type


@typeof_impl.register(pd.Timedelta)
def typeof_pd_timedelta(val, c):
    return pd_timedelta_type


@register_model(PDTimeDeltaType)
class PDTimeDeltaModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ioedq__nviu = [('value', types.int64)]
        super(PDTimeDeltaModel, self).__init__(dmm, fe_type, ioedq__nviu)


@box(PDTimeDeltaType)
def box_pd_timedelta(typ, val, c):
    uvtb__iah = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    jntve__dqu = c.pyapi.long_from_longlong(uvtb__iah.value)
    sdkud__mav = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timedelta))
    res = c.pyapi.call_function_objargs(sdkud__mav, (jntve__dqu,))
    c.pyapi.decref(jntve__dqu)
    c.pyapi.decref(sdkud__mav)
    return res


@unbox(PDTimeDeltaType)
def unbox_pd_timedelta(typ, val, c):
    jntve__dqu = c.pyapi.object_getattr_string(val, 'value')
    dzr__vtptw = c.pyapi.long_as_longlong(jntve__dqu)
    uvtb__iah = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    uvtb__iah.value = dzr__vtptw
    c.pyapi.decref(jntve__dqu)
    hafr__eie = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(uvtb__iah._getvalue(), is_error=hafr__eie)


@lower_constant(PDTimeDeltaType)
def lower_constant_pd_timedelta(context, builder, ty, pyval):
    value = context.get_constant(types.int64, pyval.value)
    return lir.Constant.literal_struct([value])


@overload(pd.Timedelta, no_unliteral=True)
def pd_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
    microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    if value == _no_input:

        def impl_timedelta_kw(value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
            days += weeks * 7
            hours += days * 24
            minutes += 60 * hours
            seconds += 60 * minutes
            milliseconds += 1000 * seconds
            microseconds += 1000 * milliseconds
            lyp__pnkkf = 1000 * microseconds
            return init_pd_timedelta(lyp__pnkkf)
        return impl_timedelta_kw
    if value == bodo.string_type or is_overload_constant_str(value):

        def impl_str(value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
            with numba.objmode(res='pd_timedelta_type'):
                res = pd.Timedelta(value)
            return res
        return impl_str
    if value == pd_timedelta_type:
        return (lambda value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0: value)
    if value == datetime_timedelta_type:

        def impl_timedelta_datetime(value=_no_input, unit='ns', days=0,
            seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0,
            weeks=0):
            days = value.days
            seconds = 60 * 60 * 24 * days + value.seconds
            microseconds = 1000 * 1000 * seconds + value.microseconds
            lyp__pnkkf = 1000 * microseconds
            return init_pd_timedelta(lyp__pnkkf)
        return impl_timedelta_datetime
    if not is_overload_constant_str(unit):
        raise BodoError('pd.to_timedelta(): unit should be a constant string')
    unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
        get_overload_const_str(unit))
    sdqna__oqtu, hof__gqdut = pd._libs.tslibs.conversion.precision_from_unit(
        unit)

    def impl_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
        microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return init_pd_timedelta(value * sdqna__oqtu)
    return impl_timedelta


@intrinsic
def init_pd_timedelta(typingctx, value):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        timedelta = cgutils.create_struct_proxy(typ)(context, builder)
        timedelta.value = args[0]
        return timedelta._getvalue()
    return PDTimeDeltaType()(value), codegen


make_attribute_wrapper(PDTimeDeltaType, 'value', '_value')


@overload_attribute(PDTimeDeltaType, 'value')
@overload_attribute(PDTimeDeltaType, 'delta')
def pd_timedelta_get_value(td):

    def impl(td):
        return td._value
    return impl


@overload_attribute(PDTimeDeltaType, 'days')
def pd_timedelta_get_days(td):

    def impl(td):
        return td._value // (1000 * 1000 * 1000 * 60 * 60 * 24)
    return impl


@overload_attribute(PDTimeDeltaType, 'seconds')
def pd_timedelta_get_seconds(td):

    def impl(td):
        return td._value // (1000 * 1000 * 1000) % (60 * 60 * 24)
    return impl


@overload_attribute(PDTimeDeltaType, 'microseconds')
def pd_timedelta_get_microseconds(td):

    def impl(td):
        return td._value // 1000 % 1000000
    return impl


@overload_attribute(PDTimeDeltaType, 'nanoseconds')
def pd_timedelta_get_nanoseconds(td):

    def impl(td):
        return td._value % 1000
    return impl


@register_jitable
def _to_hours_pd_td(td):
    return td._value // (1000 * 1000 * 1000 * 60 * 60) % 24


@register_jitable
def _to_minutes_pd_td(td):
    return td._value // (1000 * 1000 * 1000 * 60) % 60


@register_jitable
def _to_seconds_pd_td(td):
    return td._value // (1000 * 1000 * 1000) % 60


@register_jitable
def _to_milliseconds_pd_td(td):
    return td._value // (1000 * 1000) % 1000


@register_jitable
def _to_microseconds_pd_td(td):
    return td._value // 1000 % 1000


Components = namedtuple('Components', ['days', 'hours', 'minutes',
    'seconds', 'milliseconds', 'microseconds', 'nanoseconds'], defaults=[0,
    0, 0, 0, 0, 0, 0])


@overload_attribute(PDTimeDeltaType, 'components', no_unliteral=True)
def pd_timedelta_get_components(td):

    def impl(td):
        a = Components(td.days, _to_hours_pd_td(td), _to_minutes_pd_td(td),
            _to_seconds_pd_td(td), _to_milliseconds_pd_td(td),
            _to_microseconds_pd_td(td), td.nanoseconds)
        return a
    return impl


@overload_method(PDTimeDeltaType, '__hash__', no_unliteral=True)
def pd_td___hash__(td):

    def impl(td):
        return hash(td._value)
    return impl


@overload_method(PDTimeDeltaType, 'to_numpy', no_unliteral=True)
@overload_method(PDTimeDeltaType, 'to_timedelta64', no_unliteral=True)
def pd_td_to_numpy(td):
    from bodo.hiframes.pd_timestamp_ext import integer_to_timedelta64

    def impl(td):
        return integer_to_timedelta64(td.value)
    return impl


@overload_method(PDTimeDeltaType, 'to_pytimedelta', no_unliteral=True)
def pd_td_to_pytimedelta(td):

    def impl(td):
        return datetime.timedelta(microseconds=np.int64(td._value / 1000))
    return impl


@overload_method(PDTimeDeltaType, 'total_seconds', no_unliteral=True)
def pd_td_total_seconds(td):

    def impl(td):
        return td._value // 1000 / 10 ** 6
    return impl


def overload_add_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            val = lhs.value + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            kwta__ttl = (rhs.microseconds + (rhs.seconds + rhs.days * 60 * 
                60 * 24) * 1000 * 1000) * 1000
            val = lhs.value + kwta__ttl
            return pd.Timedelta(val)
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            eyw__rnhd = (lhs.microseconds + (lhs.seconds + lhs.days * 60 * 
                60 * 24) * 1000 * 1000) * 1000
            val = eyw__rnhd + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_datetime_type:
        from bodo.hiframes.pd_timestamp_ext import compute_pd_timestamp

        def impl(lhs, rhs):
            krr__wdka = rhs.toordinal()
            ypdr__bqz = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            sbbgw__vylit = rhs.microsecond
            hkvjo__jpurh = lhs.value // 1000
            oppv__bfsx = lhs.nanoseconds
            iedcr__cjtf = sbbgw__vylit + hkvjo__jpurh
            cxevo__avc = 1000000 * (krr__wdka * 86400 + ypdr__bqz
                ) + iedcr__cjtf
            pywvh__ibunu = oppv__bfsx
            return compute_pd_timestamp(cxevo__avc, pywvh__ibunu)
        return impl
    if lhs == datetime_datetime_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + rhs.to_pytimedelta()
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs.days + rhs.days
            s = lhs.seconds + rhs.seconds
            us = lhs.microseconds + rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            pig__lede = datetime.timedelta(rhs.toordinal(), hours=rhs.hour,
                minutes=rhs.minute, seconds=rhs.second, microseconds=rhs.
                microsecond)
            pig__lede = pig__lede + lhs
            rxk__lmsoe, rdk__ywgo = divmod(pig__lede.seconds, 3600)
            hifg__dsbv, fvnc__smcwk = divmod(rdk__ywgo, 60)
            if 0 < pig__lede.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(pig__lede
                    .days)
                return datetime.datetime(d.year, d.month, d.day, rxk__lmsoe,
                    hifg__dsbv, fvnc__smcwk, pig__lede.microseconds)
            raise OverflowError('result out of range')
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            pig__lede = datetime.timedelta(lhs.toordinal(), hours=lhs.hour,
                minutes=lhs.minute, seconds=lhs.second, microseconds=lhs.
                microsecond)
            pig__lede = pig__lede + rhs
            rxk__lmsoe, rdk__ywgo = divmod(pig__lede.seconds, 3600)
            hifg__dsbv, fvnc__smcwk = divmod(rdk__ywgo, 60)
            if 0 < pig__lede.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(pig__lede
                    .days)
                return datetime.datetime(d.year, d.month, d.day, rxk__lmsoe,
                    hifg__dsbv, fvnc__smcwk, pig__lede.microseconds)
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            nukx__lrvp = lhs.value - rhs.value
            return pd.Timedelta(nukx__lrvp)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_datetime_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs.days - rhs.days
            s = lhs.seconds - rhs.seconds
            us = lhs.microseconds - rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_array_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            tgyf__wqigm = lhs
            numba.parfors.parfor.init_prange()
            n = len(tgyf__wqigm)
            A = alloc_datetime_timedelta_array(n)
            for frghq__mnyg in numba.parfors.parfor.internal_prange(n):
                A[frghq__mnyg] = tgyf__wqigm[frghq__mnyg] - rhs
            return A
        return impl


def overload_mul_operator_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value * rhs)
        return impl
    elif isinstance(lhs, types.Integer) and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return pd.Timedelta(rhs.value * lhs)
        return impl
    if lhs == datetime_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            d = lhs.days * rhs
            s = lhs.seconds * rhs
            us = lhs.microseconds * rhs
            return datetime.timedelta(d, s, us)
        return impl
    elif isinstance(lhs, types.Integer) and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs * rhs.days
            s = lhs * rhs.seconds
            us = lhs * rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl


def overload_floordiv_operator_pd_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs.value // rhs.value
        return impl
    elif lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value // rhs)
        return impl


def overload_truediv_operator_pd_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs.value / rhs.value
        return impl
    elif lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(int(lhs.value / rhs))
        return impl


def overload_mod_operator_timedeltas(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value % rhs.value)
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            fmva__wpfkl = _to_microseconds(lhs) % _to_microseconds(rhs)
            return datetime.timedelta(0, 0, fmva__wpfkl)
        return impl


def pd_create_cmp_op_overload(op):

    def overload_pd_timedelta_cmp(lhs, rhs):
        if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

            def impl(lhs, rhs):
                return op(lhs.value, rhs.value)
            return impl
        if lhs == pd_timedelta_type and rhs == bodo.timedelta64ns:
            return lambda lhs, rhs: op(bodo.hiframes.pd_timestamp_ext.
                integer_to_timedelta64(lhs.value), rhs)
        if lhs == bodo.timedelta64ns and rhs == pd_timedelta_type:
            return lambda lhs, rhs: op(lhs, bodo.hiframes.pd_timestamp_ext.
                integer_to_timedelta64(rhs.value))
    return overload_pd_timedelta_cmp


@overload(operator.neg, no_unliteral=True)
def pd_timedelta_neg(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            return pd.Timedelta(-lhs.value)
        return impl


@overload(operator.pos, no_unliteral=True)
def pd_timedelta_pos(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            return lhs
        return impl


@overload(divmod, no_unliteral=True)
def pd_timedelta_divmod(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            xeb__yblb, fmva__wpfkl = divmod(lhs.value, rhs.value)
            return xeb__yblb, pd.Timedelta(fmva__wpfkl)
        return impl


@overload(abs, no_unliteral=True)
def pd_timedelta_abs(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            if lhs.value < 0:
                return -lhs
            else:
                return lhs
        return impl


class DatetimeTimeDeltaType(types.Type):

    def __init__(self):
        super(DatetimeTimeDeltaType, self).__init__(name=
            'DatetimeTimeDeltaType()')


datetime_timedelta_type = DatetimeTimeDeltaType()


@typeof_impl.register(datetime.timedelta)
def typeof_datetime_timedelta(val, c):
    return datetime_timedelta_type


@register_model(DatetimeTimeDeltaType)
class DatetimeTimeDeltaModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ioedq__nviu = [('days', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64)]
        super(DatetimeTimeDeltaModel, self).__init__(dmm, fe_type, ioedq__nviu)


@box(DatetimeTimeDeltaType)
def box_datetime_timedelta(typ, val, c):
    uvtb__iah = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    otkqm__iocd = c.pyapi.long_from_longlong(uvtb__iah.days)
    jyveq__owodd = c.pyapi.long_from_longlong(uvtb__iah.seconds)
    pwj__mkx = c.pyapi.long_from_longlong(uvtb__iah.microseconds)
    sdkud__mav = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        timedelta))
    res = c.pyapi.call_function_objargs(sdkud__mav, (otkqm__iocd,
        jyveq__owodd, pwj__mkx))
    c.pyapi.decref(otkqm__iocd)
    c.pyapi.decref(jyveq__owodd)
    c.pyapi.decref(pwj__mkx)
    c.pyapi.decref(sdkud__mav)
    return res


@unbox(DatetimeTimeDeltaType)
def unbox_datetime_timedelta(typ, val, c):
    otkqm__iocd = c.pyapi.object_getattr_string(val, 'days')
    jyveq__owodd = c.pyapi.object_getattr_string(val, 'seconds')
    pwj__mkx = c.pyapi.object_getattr_string(val, 'microseconds')
    frec__aaen = c.pyapi.long_as_longlong(otkqm__iocd)
    ggg__diau = c.pyapi.long_as_longlong(jyveq__owodd)
    qtsq__nkcrv = c.pyapi.long_as_longlong(pwj__mkx)
    uvtb__iah = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    uvtb__iah.days = frec__aaen
    uvtb__iah.seconds = ggg__diau
    uvtb__iah.microseconds = qtsq__nkcrv
    c.pyapi.decref(otkqm__iocd)
    c.pyapi.decref(jyveq__owodd)
    c.pyapi.decref(pwj__mkx)
    hafr__eie = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(uvtb__iah._getvalue(), is_error=hafr__eie)


@lower_constant(DatetimeTimeDeltaType)
def lower_constant_datetime_timedelta(context, builder, ty, pyval):
    days = context.get_constant(types.int64, pyval.days)
    seconds = context.get_constant(types.int64, pyval.seconds)
    microseconds = context.get_constant(types.int64, pyval.microseconds)
    return lir.Constant.literal_struct([days, seconds, microseconds])


@overload(datetime.timedelta, no_unliteral=True)
def datetime_timedelta(days=0, seconds=0, microseconds=0, milliseconds=0,
    minutes=0, hours=0, weeks=0):

    def impl_timedelta(days=0, seconds=0, microseconds=0, milliseconds=0,
        minutes=0, hours=0, weeks=0):
        d = s = us = 0
        days += weeks * 7
        seconds += minutes * 60 + hours * 3600
        microseconds += milliseconds * 1000
        d = days
        days, seconds = divmod(seconds, 24 * 3600)
        d += days
        s += int(seconds)
        seconds, us = divmod(microseconds, 1000000)
        days, seconds = divmod(seconds, 24 * 3600)
        d += days
        s += seconds
        return init_timedelta(d, s, us)
    return impl_timedelta


@intrinsic
def init_timedelta(typingctx, d, s, us):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        timedelta = cgutils.create_struct_proxy(typ)(context, builder)
        timedelta.days = args[0]
        timedelta.seconds = args[1]
        timedelta.microseconds = args[2]
        return timedelta._getvalue()
    return DatetimeTimeDeltaType()(d, s, us), codegen


make_attribute_wrapper(DatetimeTimeDeltaType, 'days', '_days')
make_attribute_wrapper(DatetimeTimeDeltaType, 'seconds', '_seconds')
make_attribute_wrapper(DatetimeTimeDeltaType, 'microseconds', '_microseconds')


@overload_attribute(DatetimeTimeDeltaType, 'days')
def timedelta_get_days(td):

    def impl(td):
        return td._days
    return impl


@overload_attribute(DatetimeTimeDeltaType, 'seconds')
def timedelta_get_seconds(td):

    def impl(td):
        return td._seconds
    return impl


@overload_attribute(DatetimeTimeDeltaType, 'microseconds')
def timedelta_get_microseconds(td):

    def impl(td):
        return td._microseconds
    return impl


@overload_method(DatetimeTimeDeltaType, 'total_seconds', no_unliteral=True)
def total_seconds(td):

    def impl(td):
        return ((td._days * 86400 + td._seconds) * 10 ** 6 + td._microseconds
            ) / 10 ** 6
    return impl


@overload_method(DatetimeTimeDeltaType, '__hash__', no_unliteral=True)
def __hash__(td):

    def impl(td):
        return hash((td._days, td._seconds, td._microseconds))
    return impl


@register_jitable
def _to_nanoseconds(td):
    return np.int64(((td._days * 86400 + td._seconds) * 1000000 + td.
        _microseconds) * 1000)


@register_jitable
def _to_microseconds(td):
    return (td._days * (24 * 3600) + td._seconds) * 1000000 + td._microseconds


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


@register_jitable
def _getstate(td):
    return td._days, td._seconds, td._microseconds


@register_jitable
def _divide_and_round(a, b):
    xeb__yblb, fmva__wpfkl = divmod(a, b)
    fmva__wpfkl *= 2
    afp__ypb = fmva__wpfkl > b if b > 0 else fmva__wpfkl < b
    if afp__ypb or fmva__wpfkl == b and xeb__yblb % 2 == 1:
        xeb__yblb += 1
    return xeb__yblb


_MAXORDINAL = 3652059


def overload_floordiv_operator_dt_timedelta(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return us // _to_microseconds(rhs)
        return impl
    elif lhs == datetime_timedelta_type and rhs == types.int64:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return datetime.timedelta(0, 0, us // rhs)
        return impl


def overload_truediv_operator_dt_timedelta(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return us / _to_microseconds(rhs)
        return impl
    elif lhs == datetime_timedelta_type and rhs == types.int64:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return datetime.timedelta(0, 0, _divide_and_round(us, rhs))
        return impl


def create_cmp_op_overload(op):

    def overload_timedelta_cmp(lhs, rhs):
        if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

            def impl(lhs, rhs):
                mtb__crvc = _cmp(_getstate(lhs), _getstate(rhs))
                return op(mtb__crvc, 0)
            return impl
    return overload_timedelta_cmp


@overload(operator.neg, no_unliteral=True)
def timedelta_neg(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            return datetime.timedelta(-lhs.days, -lhs.seconds, -lhs.
                microseconds)
        return impl


@overload(operator.pos, no_unliteral=True)
def timedelta_pos(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            return lhs
        return impl


@overload(divmod, no_unliteral=True)
def timedelta_divmod(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            xeb__yblb, fmva__wpfkl = divmod(_to_microseconds(lhs),
                _to_microseconds(rhs))
            return xeb__yblb, datetime.timedelta(0, 0, fmva__wpfkl)
        return impl


@overload(abs, no_unliteral=True)
def timedelta_abs(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            if lhs.days < 0:
                return -lhs
            else:
                return lhs
        return impl


@intrinsic
def cast_numpy_timedelta_to_int(typingctx, val=None):
    assert val in (types.NPTimedelta('ns'), types.int64)

    def codegen(context, builder, signature, args):
        return args[0]
    return types.int64(val), codegen


@overload(bool, no_unliteral=True)
def timedelta_to_bool(timedelta):
    if timedelta != datetime_timedelta_type:
        return
    lxaq__iozuj = datetime.timedelta(0)

    def impl(timedelta):
        return timedelta != lxaq__iozuj
    return impl


class DatetimeTimeDeltaArrayType(types.ArrayCompatible):

    def __init__(self):
        super(DatetimeTimeDeltaArrayType, self).__init__(name=
            'DatetimeTimeDeltaArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return datetime_timedelta_type

    def copy(self):
        return DatetimeTimeDeltaArrayType()


datetime_timedelta_array_type = DatetimeTimeDeltaArrayType()
types.datetime_timedelta_array_type = datetime_timedelta_array_type
days_data_type = types.Array(types.int64, 1, 'C')
seconds_data_type = types.Array(types.int64, 1, 'C')
microseconds_data_type = types.Array(types.int64, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(DatetimeTimeDeltaArrayType)
class DatetimeTimeDeltaArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ioedq__nviu = [('days_data', days_data_type), ('seconds_data',
            seconds_data_type), ('microseconds_data',
            microseconds_data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, ioedq__nviu)


make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'days_data', '_days_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'seconds_data',
    '_seconds_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'microseconds_data',
    '_microseconds_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'null_bitmap',
    '_null_bitmap')


@overload_method(DatetimeTimeDeltaArrayType, 'copy', no_unliteral=True)
def overload_datetime_timedelta_arr_copy(A):
    return (lambda A: bodo.hiframes.datetime_timedelta_ext.
        init_datetime_timedelta_array(A._days_data.copy(), A._seconds_data.
        copy(), A._microseconds_data.copy(), A._null_bitmap.copy()))


@unbox(DatetimeTimeDeltaArrayType)
def unbox_datetime_timedelta_array(typ, val, c):
    n = bodo.utils.utils.object_length(c, val)
    aze__hibpx = types.Array(types.intp, 1, 'C')
    emik__ikufd = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        aze__hibpx, [n])
    gkf__ukhpi = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        aze__hibpx, [n])
    zkv__ftmpa = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        aze__hibpx, [n])
    jpm__vsss = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(64
        ), 7)), lir.Constant(lir.IntType(64), 8))
    dddp__qynb = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [jpm__vsss])
    njqe__psxo = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64), lir.IntType(64).as_pointer(), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (8).as_pointer()])
    cbf__ygny = cgutils.get_or_insert_function(c.builder.module, njqe__psxo,
        name='unbox_datetime_timedelta_array')
    c.builder.call(cbf__ygny, [val, n, emik__ikufd.data, gkf__ukhpi.data,
        zkv__ftmpa.data, dddp__qynb.data])
    gbe__pqb = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    gbe__pqb.days_data = emik__ikufd._getvalue()
    gbe__pqb.seconds_data = gkf__ukhpi._getvalue()
    gbe__pqb.microseconds_data = zkv__ftmpa._getvalue()
    gbe__pqb.null_bitmap = dddp__qynb._getvalue()
    hafr__eie = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(gbe__pqb._getvalue(), is_error=hafr__eie)


@box(DatetimeTimeDeltaArrayType)
def box_datetime_timedelta_array(typ, val, c):
    tgyf__wqigm = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    emik__ikufd = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, tgyf__wqigm.days_data)
    gkf__ukhpi = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, tgyf__wqigm.seconds_data).data
    zkv__ftmpa = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, tgyf__wqigm.microseconds_data).data
    kcdum__maht = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, tgyf__wqigm.null_bitmap).data
    n = c.builder.extract_value(emik__ikufd.shape, 0)
    njqe__psxo = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (64).as_pointer(), lir.IntType(8).as_pointer()])
    tdkv__zvp = cgutils.get_or_insert_function(c.builder.module, njqe__psxo,
        name='box_datetime_timedelta_array')
    njfbs__odit = c.builder.call(tdkv__zvp, [n, emik__ikufd.data,
        gkf__ukhpi, zkv__ftmpa, kcdum__maht])
    c.context.nrt.decref(c.builder, typ, val)
    return njfbs__odit


@intrinsic
def init_datetime_timedelta_array(typingctx, days_data, seconds_data,
    microseconds_data, nulls=None):
    assert days_data == types.Array(types.int64, 1, 'C')
    assert seconds_data == types.Array(types.int64, 1, 'C')
    assert microseconds_data == types.Array(types.int64, 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        hos__vthok, ydyu__hgy, uqg__ynn, lkne__bnl = args
        dlrf__cvkt = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        dlrf__cvkt.days_data = hos__vthok
        dlrf__cvkt.seconds_data = ydyu__hgy
        dlrf__cvkt.microseconds_data = uqg__ynn
        dlrf__cvkt.null_bitmap = lkne__bnl
        context.nrt.incref(builder, signature.args[0], hos__vthok)
        context.nrt.incref(builder, signature.args[1], ydyu__hgy)
        context.nrt.incref(builder, signature.args[2], uqg__ynn)
        context.nrt.incref(builder, signature.args[3], lkne__bnl)
        return dlrf__cvkt._getvalue()
    xndi__yws = datetime_timedelta_array_type(days_data, seconds_data,
        microseconds_data, nulls)
    return xndi__yws, codegen


@lower_constant(DatetimeTimeDeltaArrayType)
def lower_constant_datetime_timedelta_arr(context, builder, typ, pyval):
    n = len(pyval)
    emik__ikufd = np.empty(n, np.int64)
    gkf__ukhpi = np.empty(n, np.int64)
    zkv__ftmpa = np.empty(n, np.int64)
    eveg__hzaum = np.empty(n + 7 >> 3, np.uint8)
    for frghq__mnyg, s in enumerate(pyval):
        dee__jgklo = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(eveg__hzaum, frghq__mnyg, int(
            not dee__jgklo))
        if not dee__jgklo:
            emik__ikufd[frghq__mnyg] = s.days
            gkf__ukhpi[frghq__mnyg] = s.seconds
            zkv__ftmpa[frghq__mnyg] = s.microseconds
    lccp__nsu = context.get_constant_generic(builder, days_data_type,
        emik__ikufd)
    atc__gaze = context.get_constant_generic(builder, seconds_data_type,
        gkf__ukhpi)
    dzl__zmsxf = context.get_constant_generic(builder,
        microseconds_data_type, zkv__ftmpa)
    tmm__xyju = context.get_constant_generic(builder, nulls_type, eveg__hzaum)
    return lir.Constant.literal_struct([lccp__nsu, atc__gaze, dzl__zmsxf,
        tmm__xyju])


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_timedelta_array(n):
    emik__ikufd = np.empty(n, dtype=np.int64)
    gkf__ukhpi = np.empty(n, dtype=np.int64)
    zkv__ftmpa = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_timedelta_array(emik__ikufd, gkf__ukhpi,
        zkv__ftmpa, nulls)


def alloc_datetime_timedelta_array_equiv(self, scope, equiv_set, loc, args, kws
    ):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_datetime_timedelta_ext_alloc_datetime_timedelta_array
    ) = alloc_datetime_timedelta_array_equiv


@overload(operator.getitem, no_unliteral=True)
def dt_timedelta_arr_getitem(A, ind):
    if A != datetime_timedelta_array_type:
        return
    if isinstance(ind, types.Integer):

        def impl_int(A, ind):
            return datetime.timedelta(days=A._days_data[ind], seconds=A.
                _seconds_data[ind], microseconds=A._microseconds_data[ind])
        return impl_int
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            ldm__gud = bodo.utils.conversion.coerce_to_ndarray(ind)
            lvdwa__qnzhf = A._null_bitmap
            arbw__buam = A._days_data[ldm__gud]
            bcwdg__vzzn = A._seconds_data[ldm__gud]
            gpa__tiph = A._microseconds_data[ldm__gud]
            n = len(arbw__buam)
            gomia__sii = get_new_null_mask_bool_index(lvdwa__qnzhf, ind, n)
            return init_datetime_timedelta_array(arbw__buam, bcwdg__vzzn,
                gpa__tiph, gomia__sii)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            ldm__gud = bodo.utils.conversion.coerce_to_ndarray(ind)
            lvdwa__qnzhf = A._null_bitmap
            arbw__buam = A._days_data[ldm__gud]
            bcwdg__vzzn = A._seconds_data[ldm__gud]
            gpa__tiph = A._microseconds_data[ldm__gud]
            n = len(arbw__buam)
            gomia__sii = get_new_null_mask_int_index(lvdwa__qnzhf, ldm__gud, n)
            return init_datetime_timedelta_array(arbw__buam, bcwdg__vzzn,
                gpa__tiph, gomia__sii)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            n = len(A._days_data)
            lvdwa__qnzhf = A._null_bitmap
            arbw__buam = np.ascontiguousarray(A._days_data[ind])
            bcwdg__vzzn = np.ascontiguousarray(A._seconds_data[ind])
            gpa__tiph = np.ascontiguousarray(A._microseconds_data[ind])
            gomia__sii = get_new_null_mask_slice_index(lvdwa__qnzhf, ind, n)
            return init_datetime_timedelta_array(arbw__buam, bcwdg__vzzn,
                gpa__tiph, gomia__sii)
        return impl_slice
    raise BodoError(
        f'getitem for DatetimeTimedeltaArray with indexing type {ind} not supported.'
        )


@overload(operator.setitem, no_unliteral=True)
def dt_timedelta_arr_setitem(A, ind, val):
    if A != datetime_timedelta_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    pas__iylh = (
        f"setitem for DatetimeTimedeltaArray with indexing type {ind} received an incorrect 'value' type {val}."
        )
    if isinstance(ind, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl(A, ind, val):
                A._days_data[ind] = val._days
                A._seconds_data[ind] = val._seconds
                A._microseconds_data[ind] = val._microseconds
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, ind, 1)
            return impl
        else:
            raise BodoError(pas__iylh)
    if not (is_iterable_type(val) and val.dtype == bodo.
        datetime_timedelta_type or types.unliteral(val) ==
        datetime_timedelta_type):
        raise BodoError(pas__iylh)
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_arr_ind_scalar(A, ind, val):
                n = len(A)
                for frghq__mnyg in range(n):
                    A._days_data[ind[frghq__mnyg]] = val._days
                    A._seconds_data[ind[frghq__mnyg]] = val._seconds
                    A._microseconds_data[ind[frghq__mnyg]] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[frghq__mnyg], 1)
            return impl_arr_ind_scalar
        else:

            def impl_arr_ind(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(val._days_data)
                for frghq__mnyg in range(n):
                    A._days_data[ind[frghq__mnyg]] = val._days_data[frghq__mnyg
                        ]
                    A._seconds_data[ind[frghq__mnyg]] = val._seconds_data[
                        frghq__mnyg]
                    A._microseconds_data[ind[frghq__mnyg]
                        ] = val._microseconds_data[frghq__mnyg]
                    sxdl__xpiju = bodo.libs.int_arr_ext.get_bit_bitmap_arr(val
                        ._null_bitmap, frghq__mnyg)
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[frghq__mnyg], sxdl__xpiju)
            return impl_arr_ind
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_bool_ind_mask_scalar(A, ind, val):
                n = len(ind)
                for frghq__mnyg in range(n):
                    if not bodo.libs.array_kernels.isna(ind, frghq__mnyg
                        ) and ind[frghq__mnyg]:
                        A._days_data[frghq__mnyg] = val._days
                        A._seconds_data[frghq__mnyg] = val._seconds
                        A._microseconds_data[frghq__mnyg] = val._microseconds
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            frghq__mnyg, 1)
            return impl_bool_ind_mask_scalar
        else:

            def impl_bool_ind_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(ind)
                tzwcd__jhgdb = 0
                for frghq__mnyg in range(n):
                    if not bodo.libs.array_kernels.isna(ind, frghq__mnyg
                        ) and ind[frghq__mnyg]:
                        A._days_data[frghq__mnyg] = val._days_data[tzwcd__jhgdb
                            ]
                        A._seconds_data[frghq__mnyg] = val._seconds_data[
                            tzwcd__jhgdb]
                        A._microseconds_data[frghq__mnyg
                            ] = val._microseconds_data[tzwcd__jhgdb]
                        sxdl__xpiju = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                            val._null_bitmap, tzwcd__jhgdb)
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            frghq__mnyg, sxdl__xpiju)
                        tzwcd__jhgdb += 1
            return impl_bool_ind_mask
    if isinstance(ind, types.SliceType):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_slice_scalar(A, ind, val):
                hbpb__itgm = numba.cpython.unicode._normalize_slice(ind, len(A)
                    )
                for frghq__mnyg in range(hbpb__itgm.start, hbpb__itgm.stop,
                    hbpb__itgm.step):
                    A._days_data[frghq__mnyg] = val._days
                    A._seconds_data[frghq__mnyg] = val._seconds
                    A._microseconds_data[frghq__mnyg] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        frghq__mnyg, 1)
            return impl_slice_scalar
        else:

            def impl_slice_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(A._days_data)
                A._days_data[ind] = val._days_data
                A._seconds_data[ind] = val._seconds_data
                A._microseconds_data[ind] = val._microseconds_data
                orwml__qoit = val._null_bitmap.copy()
                setitem_slice_index_null_bits(A._null_bitmap, orwml__qoit,
                    ind, n)
            return impl_slice_mask
    raise BodoError(
        f'setitem for DatetimeTimedeltaArray with indexing type {ind} not supported.'
        )


@overload(len, no_unliteral=True)
def overload_len_datetime_timedelta_arr(A):
    if A == datetime_timedelta_array_type:
        return lambda A: len(A._days_data)


@overload_attribute(DatetimeTimeDeltaArrayType, 'shape')
def overload_datetime_timedelta_arr_shape(A):
    return lambda A: (len(A._days_data),)


@overload_attribute(DatetimeTimeDeltaArrayType, 'nbytes')
def timedelta_arr_nbytes_overload(A):
    return (lambda A: A._days_data.nbytes + A._seconds_data.nbytes + A.
        _microseconds_data.nbytes + A._null_bitmap.nbytes)


def overload_datetime_timedelta_arr_sub(arg1, arg2):
    if (arg1 == datetime_timedelta_array_type and arg2 ==
        datetime_timedelta_type):

        def impl(arg1, arg2):
            tgyf__wqigm = arg1
            numba.parfors.parfor.init_prange()
            n = len(tgyf__wqigm)
            A = alloc_datetime_timedelta_array(n)
            for frghq__mnyg in numba.parfors.parfor.internal_prange(n):
                A[frghq__mnyg] = tgyf__wqigm[frghq__mnyg] - arg2
            return A
        return impl


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            xjs__dpk = True
        else:
            xjs__dpk = False
        if (lhs == datetime_timedelta_array_type and rhs ==
            datetime_timedelta_array_type):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                tugj__oadzj = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for frghq__mnyg in numba.parfors.parfor.internal_prange(n):
                    xro__qzp = bodo.libs.array_kernels.isna(lhs, frghq__mnyg)
                    jxnm__wdbxf = bodo.libs.array_kernels.isna(rhs, frghq__mnyg
                        )
                    if xro__qzp or jxnm__wdbxf:
                        vsyv__aearp = xjs__dpk
                    else:
                        vsyv__aearp = op(lhs[frghq__mnyg], rhs[frghq__mnyg])
                    tugj__oadzj[frghq__mnyg] = vsyv__aearp
                return tugj__oadzj
            return impl
        elif lhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                tugj__oadzj = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for frghq__mnyg in numba.parfors.parfor.internal_prange(n):
                    sxdl__xpiju = bodo.libs.array_kernels.isna(lhs, frghq__mnyg
                        )
                    if sxdl__xpiju:
                        vsyv__aearp = xjs__dpk
                    else:
                        vsyv__aearp = op(lhs[frghq__mnyg], rhs)
                    tugj__oadzj[frghq__mnyg] = vsyv__aearp
                return tugj__oadzj
            return impl
        elif rhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                tugj__oadzj = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for frghq__mnyg in numba.parfors.parfor.internal_prange(n):
                    sxdl__xpiju = bodo.libs.array_kernels.isna(rhs, frghq__mnyg
                        )
                    if sxdl__xpiju:
                        vsyv__aearp = xjs__dpk
                    else:
                        vsyv__aearp = op(lhs, rhs[frghq__mnyg])
                    tugj__oadzj[frghq__mnyg] = vsyv__aearp
                return tugj__oadzj
            return impl
    return overload_date_arr_cmp


timedelta_unsupported_attrs = ['asm8', 'resolution_string', 'freq',
    'is_populated']
timedelta_unsupported_methods = ['isoformat']


def _intstall_pd_timedelta_unsupported():
    from bodo.utils.typing import create_unsupported_overload
    for ctr__tjgo in timedelta_unsupported_attrs:
        kaeg__svr = 'pandas.Timedelta.' + ctr__tjgo
        overload_attribute(PDTimeDeltaType, ctr__tjgo)(
            create_unsupported_overload(kaeg__svr))
    for npop__tznf in timedelta_unsupported_methods:
        kaeg__svr = 'pandas.Timedelta.' + npop__tznf
        overload_method(PDTimeDeltaType, npop__tznf)(
            create_unsupported_overload(kaeg__svr + '()'))


_intstall_pd_timedelta_unsupported()
