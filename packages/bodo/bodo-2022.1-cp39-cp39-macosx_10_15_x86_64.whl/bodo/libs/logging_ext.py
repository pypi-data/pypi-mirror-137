"""
JIT support for Python's logging module
"""
import logging
import numba
from numba.core import types
from numba.core.imputils import lower_constant
from numba.core.typing.templates import bound_function
from numba.core.typing.templates import AttributeTemplate, infer_getattr, signature
from numba.extending import NativeValue, box, models, overload_attribute, overload_method, register_model, typeof_impl, unbox
from bodo.utils.typing import create_unsupported_overload, gen_objmode_attr_overload


class LoggingLoggerType(types.Type):

    def __init__(self, is_root=False):
        self.is_root = is_root
        super(LoggingLoggerType, self).__init__(name=
            f'LoggingLoggerType(is_root={is_root})')


@typeof_impl.register(logging.RootLogger)
@typeof_impl.register(logging.Logger)
def typeof_logging(val, c):
    if isinstance(val, logging.RootLogger):
        return LoggingLoggerType(is_root=True)
    else:
        return LoggingLoggerType(is_root=False)


register_model(LoggingLoggerType)(models.OpaqueModel)


@box(LoggingLoggerType)
def box_logging_logger(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(LoggingLoggerType)
def unbox_logging_logger(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@lower_constant(LoggingLoggerType)
def lower_constant_logger(context, builder, ty, pyval):
    pslh__pjzx = context.get_python_api(builder)
    return pslh__pjzx.unserialize(pslh__pjzx.serialize_object(pyval))


gen_objmode_attr_overload(LoggingLoggerType, 'level', None, types.int64)
gen_objmode_attr_overload(LoggingLoggerType, 'name', None, 'unicode_type')
gen_objmode_attr_overload(LoggingLoggerType, 'propagate', None, types.boolean)
gen_objmode_attr_overload(LoggingLoggerType, 'disabled', None, types.boolean)
gen_objmode_attr_overload(LoggingLoggerType, 'parent', None,
    LoggingLoggerType())
gen_objmode_attr_overload(LoggingLoggerType, 'root', None,
    LoggingLoggerType(is_root=True))


@infer_getattr
class LoggingLoggerAttribute(AttributeTemplate):
    key = LoggingLoggerType

    def _resolve_helper(self, logger_typ, args, kws):
        kws = dict(kws)
        borjs__ufpk = ', '.join('e{}'.format(axl__njzl) for axl__njzl in
            range(len(args)))
        if borjs__ufpk:
            borjs__ufpk += ', '
        ipoue__hpm = ', '.join("{} = ''".format(nejo__sfrpv) for
            nejo__sfrpv in kws.keys())
        igt__hyf = f'def format_stub(string, {borjs__ufpk} {ipoue__hpm}):\n'
        igt__hyf += '    pass\n'
        fwuzb__hrdg = {}
        exec(igt__hyf, {}, fwuzb__hrdg)
        obxn__zcuj = fwuzb__hrdg['format_stub']
        cqeq__jvwzh = numba.core.utils.pysignature(obxn__zcuj)
        bged__kfsdb = (logger_typ,) + args + tuple(kws.values())
        return signature(logger_typ, bged__kfsdb).replace(pysig=cqeq__jvwzh)
    func_names = ('debug', 'warning', 'warn', 'info', 'error', 'exception',
        'critical', 'log', 'setLevel')
    for dhcyu__eljus in ('logging.Logger', 'logging.RootLogger'):
        for uizy__rylk in func_names:
            kll__qsqr = f'@bound_function("{dhcyu__eljus}.{uizy__rylk}")\n'
            kll__qsqr += (
                f'def resolve_{uizy__rylk}(self, logger_typ, args, kws):\n')
            kll__qsqr += (
                '    return self._resolve_helper(logger_typ, args, kws)')
            exec(kll__qsqr)


logging_logger_unsupported_attrs = {'filters', 'handlers', 'manager'}
logging_logger_unsupported_methods = {'addHandler', 'callHandlers', 'fatal',
    'findCaller', 'getChild', 'getEffectiveLevel', 'handle', 'hasHandlers',
    'isEnabledFor', 'makeRecord', 'removeHandler'}


def _install_logging_logger_unsupported_objects():
    for lrlfo__rkt in logging_logger_unsupported_attrs:
        kbl__saqnh = 'logging.Logger.' + lrlfo__rkt
        overload_attribute(LoggingLoggerType, lrlfo__rkt)(
            create_unsupported_overload(kbl__saqnh))
    for hgcjd__xpc in logging_logger_unsupported_methods:
        kbl__saqnh = 'logging.Logger.' + hgcjd__xpc
        overload_method(LoggingLoggerType, hgcjd__xpc)(
            create_unsupported_overload(kbl__saqnh))


_install_logging_logger_unsupported_objects()
