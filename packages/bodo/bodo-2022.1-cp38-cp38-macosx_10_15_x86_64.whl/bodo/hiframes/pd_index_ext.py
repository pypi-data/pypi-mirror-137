import datetime
import operator
import warnings
import llvmlite.llvmpy.core as lc
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_new_ref, lower_constant
from numba.core.typing.templates import AttributeTemplate, signature
from numba.extending import NativeValue, box, infer_getattr, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
import bodo.hiframes
import bodo.utils.conversion
from bodo.hiframes.datetime_timedelta_ext import pd_timedelta_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_type
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.utils.transform import get_const_func_output_type
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, dtype_to_array_type, get_overload_const_func, get_overload_const_str, get_udf_error_msg, get_udf_out_arr_type, get_val_type_maybe_str_literal, is_const_func_type, is_heterogeneous_tuple_type, is_iterable_type, is_overload_false, is_overload_none, is_overload_true, parse_dtype, raise_bodo_error
from bodo.utils.utils import is_null_value
_dt_index_data_typ = types.Array(types.NPDatetime('ns'), 1, 'C')
_timedelta_index_data_typ = types.Array(types.NPTimedelta('ns'), 1, 'C')
iNaT = pd._libs.tslibs.iNaT
NaT = types.NPDatetime('ns')('NaT')
idx_cpy_arg_defaults = dict(deep=False, dtype=None, names=None)
idx_typ_to_format_str_map = dict()


@typeof_impl.register(pd.Index)
def typeof_pd_index(val, c):
    if val.inferred_type == 'string' or pd._libs.lib.infer_dtype(val, True
        ) == 'string':
        return StringIndexType(get_val_type_maybe_str_literal(val.name))
    if val.inferred_type == 'bytes' or pd._libs.lib.infer_dtype(val, True
        ) == 'bytes':
        return BinaryIndexType(get_val_type_maybe_str_literal(val.name))
    if val.equals(pd.Index([])):
        return StringIndexType(get_val_type_maybe_str_literal(val.name))
    if val.inferred_type == 'date':
        return DatetimeIndexType(get_val_type_maybe_str_literal(val.name))
    if val.inferred_type == 'integer' or pd._libs.lib.infer_dtype(val, True
        ) == 'integer':
        return NumericIndexType(types.int64, get_val_type_maybe_str_literal
            (val.name), IntegerArrayType(types.int64))
    if val.inferred_type == 'boolean' or pd._libs.lib.infer_dtype(val, True
        ) == 'boolean':
        return NumericIndexType(types.bool_, get_val_type_maybe_str_literal
            (val.name), boolean_array)
    raise NotImplementedError(f'unsupported pd.Index type {val}')


class DatetimeIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None, data=None):
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = types.Array(bodo.datetime64ns, 1, 'C'
            ) if data is None else data
        super(DatetimeIndexType, self).__init__(name=
            f'DatetimeIndex({name_typ}, {self.data})')
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.NPDatetime('ns')

    def copy(self):
        return DatetimeIndexType(self.name_typ)

    @property
    def key(self):
        return self.name_typ, self.data

    @property
    def iterator_type(self):
        return types.iterators.ArrayIterator(_dt_index_data_typ)

    @property
    def pandas_type_name(self):
        return 'datetime64'

    @property
    def numpy_type_name(self):
        return 'datetime64[ns]'


types.datetime_index = DatetimeIndexType()


@typeof_impl.register(pd.DatetimeIndex)
def typeof_datetime_index(val, c):
    return DatetimeIndexType(get_val_type_maybe_str_literal(val.name))


@register_model(DatetimeIndexType)
class DatetimeIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        bagk__apz = [('data', _dt_index_data_typ), ('name', fe_type.
            name_typ), ('dict', types.DictType(_dt_index_data_typ.dtype,
            types.int64))]
        super(DatetimeIndexModel, self).__init__(dmm, fe_type, bagk__apz)


make_attribute_wrapper(DatetimeIndexType, 'data', '_data')
make_attribute_wrapper(DatetimeIndexType, 'name', '_name')
make_attribute_wrapper(DatetimeIndexType, 'dict', '_dict')


@overload_method(DatetimeIndexType, 'copy', no_unliteral=True)
def overload_datetime_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    imb__fgxdc = dict(deep=deep, dtype=dtype, names=names)
    nmz__jklhr = idx_typ_to_format_str_map[DatetimeIndexType].format('copy()')
    check_unsupported_args('copy', imb__fgxdc, idx_cpy_arg_defaults, fn_str
        =nmz__jklhr, package_name='pandas', module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_datetime_index(A._data.
                copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_datetime_index(A._data.
                copy(), A._name)
    return impl


@box(DatetimeIndexType)
def box_dt_index(typ, val, c):
    msaih__qjh = c.context.insert_const_string(c.builder.module, 'pandas')
    nved__gunq = c.pyapi.import_module_noblock(msaih__qjh)
    yzyiv__nurx = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, _dt_index_data_typ, yzyiv__nurx.data)
    esrs__dyqv = c.pyapi.from_native_value(_dt_index_data_typ, yzyiv__nurx.
        data, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, yzyiv__nurx.name)
    hqslu__vqos = c.pyapi.from_native_value(typ.name_typ, yzyiv__nurx.name,
        c.env_manager)
    args = c.pyapi.tuple_pack([esrs__dyqv])
    kws = c.pyapi.dict_pack([('name', hqslu__vqos)])
    ecozs__ydz = c.pyapi.object_getattr_string(nved__gunq, 'DatetimeIndex')
    ovnjl__sfp = c.pyapi.call(ecozs__ydz, args, kws)
    c.pyapi.decref(esrs__dyqv)
    c.pyapi.decref(hqslu__vqos)
    c.pyapi.decref(nved__gunq)
    c.pyapi.decref(ecozs__ydz)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return ovnjl__sfp


@unbox(DatetimeIndexType)
def unbox_datetime_index(typ, val, c):
    rntco__uxvls = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(_dt_index_data_typ, rntco__uxvls).value
    hqslu__vqos = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, hqslu__vqos).value
    c.pyapi.decref(rntco__uxvls)
    c.pyapi.decref(hqslu__vqos)
    fsl__jyzo = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    fsl__jyzo.data = data
    fsl__jyzo.name = name
    dtype = _dt_index_data_typ.dtype
    hpki__zofg, xhae__qgdtp = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    fsl__jyzo.dict = xhae__qgdtp
    return NativeValue(fsl__jyzo._getvalue())


@intrinsic
def init_datetime_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        hbh__dooi, uchpx__mljc = args
        yzyiv__nurx = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        yzyiv__nurx.data = hbh__dooi
        yzyiv__nurx.name = uchpx__mljc
        context.nrt.incref(builder, signature.args[0], hbh__dooi)
        context.nrt.incref(builder, signature.args[1], uchpx__mljc)
        dtype = _dt_index_data_typ.dtype
        yzyiv__nurx.dict = context.compile_internal(builder, lambda : numba
            .typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return yzyiv__nurx._getvalue()
    qisew__yxm = DatetimeIndexType(name)
    sig = signature(qisew__yxm, data, name)
    return sig, codegen


def init_index_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) >= 1 and not kws
    phk__tknt = args[0]
    if equiv_set.has_shape(phk__tknt):
        return ArrayAnalysis.AnalyzeResult(shape=phk__tknt, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_datetime_index
    ) = init_index_equiv


def gen_dti_field_impl(field):
    pti__dai = 'def impl(dti):\n'
    pti__dai += '    numba.parfors.parfor.init_prange()\n'
    pti__dai += '    A = bodo.hiframes.pd_index_ext.get_index_data(dti)\n'
    pti__dai += '    name = bodo.hiframes.pd_index_ext.get_index_name(dti)\n'
    pti__dai += '    n = len(A)\n'
    pti__dai += '    S = np.empty(n, np.int64)\n'
    pti__dai += '    for i in numba.parfors.parfor.internal_prange(n):\n'
    pti__dai += (
        '        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(A[i])\n'
        )
    pti__dai += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
    if field in ['weekday']:
        pti__dai += '        S[i] = ts.' + field + '()\n'
    else:
        pti__dai += '        S[i] = ts.' + field + '\n'
    pti__dai += (
        '    return bodo.hiframes.pd_index_ext.init_numeric_index(S, name)\n')
    ikpw__fvvvr = {}
    exec(pti__dai, {'numba': numba, 'np': np, 'bodo': bodo}, ikpw__fvvvr)
    impl = ikpw__fvvvr['impl']
    return impl


def _install_dti_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        if field in ['is_leap_year']:
            continue
        impl = gen_dti_field_impl(field)
        overload_attribute(DatetimeIndexType, field)(lambda dti: impl)


_install_dti_date_fields()


@overload_attribute(DatetimeIndexType, 'is_leap_year')
def overload_datetime_index_is_leap_year(dti):

    def impl(dti):
        numba.parfors.parfor.init_prange()
        A = bodo.hiframes.pd_index_ext.get_index_data(dti)
        tqjc__xfk = len(A)
        S = np.empty(tqjc__xfk, np.bool_)
        for i in numba.parfors.parfor.internal_prange(tqjc__xfk):
            rmnvh__ntvw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(A[i])
            voddd__xyrv = (bodo.hiframes.pd_timestamp_ext.
                convert_datetime64_to_timestamp(rmnvh__ntvw))
            S[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(voddd__xyrv.year
                )
        return S
    return impl


@overload_attribute(DatetimeIndexType, 'date')
def overload_datetime_index_date(dti):

    def impl(dti):
        numba.parfors.parfor.init_prange()
        A = bodo.hiframes.pd_index_ext.get_index_data(dti)
        tqjc__xfk = len(A)
        S = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(tqjc__xfk
            )
        for i in numba.parfors.parfor.internal_prange(tqjc__xfk):
            rmnvh__ntvw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(A[i])
            voddd__xyrv = (bodo.hiframes.pd_timestamp_ext.
                convert_datetime64_to_timestamp(rmnvh__ntvw))
            S[i] = datetime.date(voddd__xyrv.year, voddd__xyrv.month,
                voddd__xyrv.day)
        return S
    return impl


@numba.njit(no_cpython_wrapper=True)
def _dti_val_finalize(s, count):
    if not count:
        s = iNaT
    return bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(s)


@numba.njit(no_cpython_wrapper=True)
def _tdi_val_finalize(s, count):
    return pd.Timedelta('nan') if not count else pd.Timedelta(s)


@overload_method(DatetimeIndexType, 'min', no_unliteral=True)
def overload_datetime_index_min(dti, axis=None, skipna=True):
    semue__ijsg = dict(axis=axis, skipna=skipna)
    kikhd__ufek = dict(axis=None, skipna=True)
    check_unsupported_args('DatetimeIndex.min', semue__ijsg, kikhd__ufek,
        package_name='pandas', module_name='Index')

    def impl(dti, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        cashn__lew = bodo.hiframes.pd_index_ext.get_index_data(dti)
        s = numba.cpython.builtins.get_type_max_value(numba.core.types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(len(cashn__lew)):
            if not bodo.libs.array_kernels.isna(cashn__lew, i):
                val = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(cashn__lew
                    [i])
                s = min(s, val)
                count += 1
        return bodo.hiframes.pd_index_ext._dti_val_finalize(s, count)
    return impl


@overload_method(DatetimeIndexType, 'max', no_unliteral=True)
def overload_datetime_index_max(dti, axis=None, skipna=True):
    semue__ijsg = dict(axis=axis, skipna=skipna)
    kikhd__ufek = dict(axis=None, skipna=True)
    check_unsupported_args('DatetimeIndex.max', semue__ijsg, kikhd__ufek,
        package_name='pandas', module_name='Index')

    def impl(dti, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        cashn__lew = bodo.hiframes.pd_index_ext.get_index_data(dti)
        s = numba.cpython.builtins.get_type_min_value(numba.core.types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(len(cashn__lew)):
            if not bodo.libs.array_kernels.isna(cashn__lew, i):
                val = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(cashn__lew
                    [i])
                s = max(s, val)
                count += 1
        return bodo.hiframes.pd_index_ext._dti_val_finalize(s, count)
    return impl


@infer_getattr
class DatetimeIndexAttribute(AttributeTemplate):
    key = DatetimeIndexType

    def resolve_values(self, ary):
        return _dt_index_data_typ


@overload(pd.DatetimeIndex, no_unliteral=True)
def pd_datetimeindex_overload(data=None, freq=None, tz=None, normalize=
    False, closed=None, ambiguous='raise', dayfirst=False, yearfirst=False,
    dtype=None, copy=False, name=None):
    if is_overload_none(data):
        raise BodoError('data argument in pd.DatetimeIndex() expected')
    semue__ijsg = dict(freq=freq, tz=tz, normalize=normalize, closed=closed,
        ambiguous=ambiguous, dayfirst=dayfirst, yearfirst=yearfirst, dtype=
        dtype, copy=copy)
    kikhd__ufek = dict(freq=None, tz=None, normalize=False, closed=None,
        ambiguous='raise', dayfirst=False, yearfirst=False, dtype=None,
        copy=False)
    check_unsupported_args('pandas.DatetimeIndex', semue__ijsg, kikhd__ufek,
        package_name='pandas', module_name='Index')

    def f(data=None, freq=None, tz=None, normalize=False, closed=None,
        ambiguous='raise', dayfirst=False, yearfirst=False, dtype=None,
        copy=False, name=None):
        axs__zsie = bodo.utils.conversion.coerce_to_array(data)
        S = bodo.utils.conversion.convert_to_dt64ns(axs__zsie)
        return bodo.hiframes.pd_index_ext.init_datetime_index(S, name)
    return f


def overload_sub_operator_datetime_index(lhs, rhs):
    if isinstance(lhs, DatetimeIndexType
        ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        zzr__dam = np.dtype('timedelta64[ns]')

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            cashn__lew = bodo.hiframes.pd_index_ext.get_index_data(lhs)
            name = bodo.hiframes.pd_index_ext.get_index_name(lhs)
            tqjc__xfk = len(cashn__lew)
            S = np.empty(tqjc__xfk, zzr__dam)
            qhna__ihyr = rhs.value
            for i in numba.parfors.parfor.internal_prange(tqjc__xfk):
                S[i] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    cashn__lew[i]) - qhna__ihyr)
            return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
        return impl
    if isinstance(rhs, DatetimeIndexType
        ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        zzr__dam = np.dtype('timedelta64[ns]')

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            cashn__lew = bodo.hiframes.pd_index_ext.get_index_data(rhs)
            name = bodo.hiframes.pd_index_ext.get_index_name(rhs)
            tqjc__xfk = len(cashn__lew)
            S = np.empty(tqjc__xfk, zzr__dam)
            qhna__ihyr = lhs.value
            for i in numba.parfors.parfor.internal_prange(tqjc__xfk):
                S[i] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    qhna__ihyr - bodo.hiframes.pd_timestamp_ext.
                    dt64_to_integer(cashn__lew[i]))
            return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
        return impl


def gen_dti_str_binop_impl(op, is_lhs_dti):
    athxw__sgy = numba.core.utils.OPERATORS_TO_BUILTINS[op]
    pti__dai = 'def impl(lhs, rhs):\n'
    if is_lhs_dti:
        pti__dai += '  dt_index, _str = lhs, rhs\n'
        zzmq__hkq = 'arr[i] {} other'.format(athxw__sgy)
    else:
        pti__dai += '  dt_index, _str = rhs, lhs\n'
        zzmq__hkq = 'other {} arr[i]'.format(athxw__sgy)
    pti__dai += '  arr = bodo.hiframes.pd_index_ext.get_index_data(dt_index)\n'
    pti__dai += '  l = len(arr)\n'
    pti__dai += (
        '  other = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(_str)\n')
    pti__dai += '  S = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    pti__dai += '  for i in numba.parfors.parfor.internal_prange(l):\n'
    pti__dai += '    S[i] = {}\n'.format(zzmq__hkq)
    pti__dai += '  return S\n'
    ikpw__fvvvr = {}
    exec(pti__dai, {'bodo': bodo, 'numba': numba, 'np': np}, ikpw__fvvvr)
    impl = ikpw__fvvvr['impl']
    return impl


def overload_binop_dti_str(op):

    def overload_impl(lhs, rhs):
        if isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
            ) == string_type:
            return gen_dti_str_binop_impl(op, True)
        if isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
            ) == string_type:
            return gen_dti_str_binop_impl(op, False)
    return overload_impl


@overload(pd.Index, inline='always', no_unliteral=True)
def pd_index_overload(data=None, dtype=None, copy=False, name=None,
    tupleize_cols=True):
    data = types.unliteral(data) if not isinstance(data, types.LiteralList
        ) else data
    zifk__fbc = getattr(data, 'dtype', None)
    if not is_overload_none(dtype):
        qep__spdjp = parse_dtype(dtype, 'pandas.Index')
    else:
        qep__spdjp = zifk__fbc
    if isinstance(qep__spdjp, types.misc.PyObject):
        raise BodoError(
            "pd.Index() object 'dtype' is not specific enough for typing. Please provide a more exact type (e.g. str)."
            )
    if isinstance(data, RangeIndexType):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.RangeIndex(data, name=name)
    elif isinstance(data, DatetimeIndexType) or qep__spdjp == types.NPDatetime(
        'ns'):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.DatetimeIndex(data, name=name)
    elif isinstance(data, TimedeltaIndexType
        ) or qep__spdjp == types.NPTimedelta('ns'):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.TimedeltaIndex(data, name=name)
    elif is_heterogeneous_tuple_type(data):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return bodo.hiframes.pd_index_ext.init_heter_index(data, name)
        return impl
    elif bodo.utils.utils.is_array_typ(data, False) or isinstance(data, (
        SeriesType, types.List, types.UniTuple)):
        if isinstance(qep__spdjp, (types.Integer, types.Float, types.Boolean)):

            def impl(data=None, dtype=None, copy=False, name=None,
                tupleize_cols=True):
                axs__zsie = bodo.utils.conversion.coerce_to_array(data)
                lgo__zje = bodo.utils.conversion.fix_arr_dtype(axs__zsie,
                    qep__spdjp)
                return bodo.hiframes.pd_index_ext.init_numeric_index(lgo__zje,
                    name)
        elif qep__spdjp in [types.string, bytes_type]:

            def impl(data=None, dtype=None, copy=False, name=None,
                tupleize_cols=True):
                return bodo.hiframes.pd_index_ext.init_binary_str_index(bodo
                    .utils.conversion.coerce_to_array(data), name)
        else:
            raise BodoError(
                'pd.Index(): provided array is of unsupported type.')
    elif is_overload_none(data):
        raise BodoError(
            'data argument in pd.Index() is invalid: None or scalar is not acceptable'
            )
    else:
        raise BodoError(
            f'pd.Index(): the provided argument type {data} is not supported')
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_datetime_index_getitem(dti, ind):
    if isinstance(dti, DatetimeIndexType):
        if isinstance(ind, types.Integer):

            def impl(dti, ind):
                tkz__kvmla = bodo.hiframes.pd_index_ext.get_index_data(dti)
                rmnvh__ntvw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    tkz__kvmla[ind])
                return (bodo.hiframes.pd_timestamp_ext.
                    convert_datetime64_to_timestamp(rmnvh__ntvw))
            return impl
        else:

            def impl(dti, ind):
                tkz__kvmla = bodo.hiframes.pd_index_ext.get_index_data(dti)
                name = bodo.hiframes.pd_index_ext.get_index_name(dti)
                hqzfg__bzuik = tkz__kvmla[ind]
                return bodo.hiframes.pd_index_ext.init_datetime_index(
                    hqzfg__bzuik, name)
            return impl


@overload(operator.getitem, no_unliteral=True)
def overload_timedelta_index_getitem(I, ind):
    if not isinstance(I, TimedeltaIndexType):
        return
    if isinstance(ind, types.Integer):

        def impl(I, ind):
            ovmfx__kekfj = bodo.hiframes.pd_index_ext.get_index_data(I)
            return pd.Timedelta(ovmfx__kekfj[ind])
        return impl

    def impl(I, ind):
        ovmfx__kekfj = bodo.hiframes.pd_index_ext.get_index_data(I)
        name = bodo.hiframes.pd_index_ext.get_index_name(I)
        hqzfg__bzuik = ovmfx__kekfj[ind]
        return bodo.hiframes.pd_index_ext.init_timedelta_index(hqzfg__bzuik,
            name)
    return impl


@numba.njit(no_cpython_wrapper=True)
def validate_endpoints(closed):
    jlvg__eilo = False
    bsbo__wciu = False
    if closed is None:
        jlvg__eilo = True
        bsbo__wciu = True
    elif closed == 'left':
        jlvg__eilo = True
    elif closed == 'right':
        bsbo__wciu = True
    else:
        raise ValueError("Closed has to be either 'left', 'right' or None")
    return jlvg__eilo, bsbo__wciu


@numba.njit(no_cpython_wrapper=True)
def to_offset_value(freq):
    if freq is None:
        return None
    with numba.objmode(r='int64'):
        r = pd.tseries.frequencies.to_offset(freq).nanos
    return r


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _dummy_convert_none_to_int(val):
    if is_overload_none(val):

        def impl(val):
            return 0
        return impl
    if isinstance(val, types.Optional):

        def impl(val):
            if val is None:
                return 0
            return bodo.utils.indexing.unoptional(val)
        return impl
    return lambda val: val


@overload(pd.date_range, no_unliteral=True)
def pd_date_range_overload(start=None, end=None, periods=None, freq=None,
    tz=None, normalize=False, name=None, closed=None):
    semue__ijsg = dict(tz=tz, normalize=normalize)
    kikhd__ufek = dict(tz=None, normalize=False)
    check_unsupported_args('pandas.date_range', semue__ijsg, kikhd__ufek,
        package_name='pandas', module_name='General')
    if not is_overload_none(tz):
        raise BodoError('pd.date_range(): tz argument not supported yet')
    if is_overload_none(freq) and any(is_overload_none(t) for t in (start,
        end, periods)):
        freq = 'D'
    if sum(not is_overload_none(t) for t in (start, end, periods, freq)) != 3:
        raise BodoError(
            'Of the four parameters: start, end, periods, and freq, exactly three must be specified'
            )

    def f(start=None, end=None, periods=None, freq=None, tz=None, normalize
        =False, name=None, closed=None):
        if freq is None and (start is None or end is None or periods is None):
            freq = 'D'
        freq = bodo.hiframes.pd_index_ext.to_offset_value(freq)
        mqnk__vbum = pd.Timestamp('2018-01-01')
        if start is not None:
            mqnk__vbum = pd.Timestamp(start)
        wrpef__myk = pd.Timestamp('2018-01-01')
        if end is not None:
            wrpef__myk = pd.Timestamp(end)
        if start is None and end is None and closed is not None:
            raise ValueError(
                'Closed has to be None if not both of startand end are defined'
                )
        jlvg__eilo, bsbo__wciu = bodo.hiframes.pd_index_ext.validate_endpoints(
            closed)
        if freq is not None:
            jsm__ndtuz = _dummy_convert_none_to_int(freq)
            if periods is None:
                b = mqnk__vbum.value
                iyhv__lzrs = b + (wrpef__myk.value - b
                    ) // jsm__ndtuz * jsm__ndtuz + jsm__ndtuz // 2 + 1
            elif start is not None:
                periods = _dummy_convert_none_to_int(periods)
                b = mqnk__vbum.value
                rxyod__bgjo = np.int64(periods) * np.int64(jsm__ndtuz)
                iyhv__lzrs = np.int64(b) + rxyod__bgjo
            elif end is not None:
                periods = _dummy_convert_none_to_int(periods)
                iyhv__lzrs = wrpef__myk.value + jsm__ndtuz
                rxyod__bgjo = np.int64(periods) * np.int64(-jsm__ndtuz)
                b = np.int64(iyhv__lzrs) + rxyod__bgjo
            else:
                raise ValueError(
                    "at least 'start' or 'end' should be specified if a 'period' is given."
                    )
            mgs__uxh = np.arange(b, iyhv__lzrs, jsm__ndtuz, np.int64)
        else:
            periods = _dummy_convert_none_to_int(periods)
            ddk__qqqrd = wrpef__myk.value - mqnk__vbum.value
            step = ddk__qqqrd / (periods - 1)
            uhxha__ibbjd = np.arange(0, periods, 1, np.float64)
            uhxha__ibbjd *= step
            uhxha__ibbjd += mqnk__vbum.value
            mgs__uxh = uhxha__ibbjd.astype(np.int64)
            mgs__uxh[-1] = wrpef__myk.value
        if not jlvg__eilo and len(mgs__uxh) and mgs__uxh[0
            ] == mqnk__vbum.value:
            mgs__uxh = mgs__uxh[1:]
        if not bsbo__wciu and len(mgs__uxh) and mgs__uxh[-1
            ] == wrpef__myk.value:
            mgs__uxh = mgs__uxh[:-1]
        S = bodo.utils.conversion.convert_to_dt64ns(mgs__uxh)
        return bodo.hiframes.pd_index_ext.init_datetime_index(S, name)
    return f


@overload(pd.timedelta_range, no_unliteral=True)
def pd_timedelta_range_overload(start=None, end=None, periods=None, freq=
    None, name=None, closed=None):
    if is_overload_none(freq) and any(is_overload_none(t) for t in (start,
        end, periods)):
        freq = 'D'
    if sum(not is_overload_none(t) for t in (start, end, periods, freq)) != 3:
        raise BodoError(
            'Of the four parameters: start, end, periods, and freq, exactly three must be specified'
            )

    def f(start=None, end=None, periods=None, freq=None, name=None, closed=None
        ):
        if freq is None and (start is None or end is None or periods is None):
            freq = 'D'
        freq = bodo.hiframes.pd_index_ext.to_offset_value(freq)
        mqnk__vbum = pd.Timedelta('1 day')
        if start is not None:
            mqnk__vbum = pd.Timedelta(start)
        wrpef__myk = pd.Timedelta('1 day')
        if end is not None:
            wrpef__myk = pd.Timedelta(end)
        if start is None and end is None and closed is not None:
            raise ValueError(
                'Closed has to be None if not both of start and end are defined'
                )
        jlvg__eilo, bsbo__wciu = bodo.hiframes.pd_index_ext.validate_endpoints(
            closed)
        if freq is not None:
            jsm__ndtuz = _dummy_convert_none_to_int(freq)
            if periods is None:
                b = mqnk__vbum.value
                iyhv__lzrs = b + (wrpef__myk.value - b
                    ) // jsm__ndtuz * jsm__ndtuz + jsm__ndtuz // 2 + 1
            elif start is not None:
                periods = _dummy_convert_none_to_int(periods)
                b = mqnk__vbum.value
                rxyod__bgjo = np.int64(periods) * np.int64(jsm__ndtuz)
                iyhv__lzrs = np.int64(b) + rxyod__bgjo
            elif end is not None:
                periods = _dummy_convert_none_to_int(periods)
                iyhv__lzrs = wrpef__myk.value + jsm__ndtuz
                rxyod__bgjo = np.int64(periods) * np.int64(-jsm__ndtuz)
                b = np.int64(iyhv__lzrs) + rxyod__bgjo
            else:
                raise ValueError(
                    "at least 'start' or 'end' should be specified if a 'period' is given."
                    )
            mgs__uxh = np.arange(b, iyhv__lzrs, jsm__ndtuz, np.int64)
        else:
            periods = _dummy_convert_none_to_int(periods)
            ddk__qqqrd = wrpef__myk.value - mqnk__vbum.value
            step = ddk__qqqrd / (periods - 1)
            uhxha__ibbjd = np.arange(0, periods, 1, np.float64)
            uhxha__ibbjd *= step
            uhxha__ibbjd += mqnk__vbum.value
            mgs__uxh = uhxha__ibbjd.astype(np.int64)
            mgs__uxh[-1] = wrpef__myk.value
        if not jlvg__eilo and len(mgs__uxh) and mgs__uxh[0
            ] == mqnk__vbum.value:
            mgs__uxh = mgs__uxh[1:]
        if not bsbo__wciu and len(mgs__uxh) and mgs__uxh[-1
            ] == wrpef__myk.value:
            mgs__uxh = mgs__uxh[:-1]
        S = bodo.utils.conversion.convert_to_dt64ns(mgs__uxh)
        return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
    return f


@overload_method(DatetimeIndexType, 'isocalendar', inline='always',
    no_unliteral=True)
def overload_pd_timestamp_isocalendar(idx):

    def impl(idx):
        A = bodo.hiframes.pd_index_ext.get_index_data(idx)
        numba.parfors.parfor.init_prange()
        tqjc__xfk = len(A)
        wxv__nnp = bodo.libs.int_arr_ext.alloc_int_array(tqjc__xfk, np.uint32)
        vzcm__psc = bodo.libs.int_arr_ext.alloc_int_array(tqjc__xfk, np.uint32)
        far__ook = bodo.libs.int_arr_ext.alloc_int_array(tqjc__xfk, np.uint32)
        for i in numba.parfors.parfor.internal_prange(tqjc__xfk):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(wxv__nnp, i)
                bodo.libs.array_kernels.setna(vzcm__psc, i)
                bodo.libs.array_kernels.setna(far__ook, i)
                continue
            wxv__nnp[i], vzcm__psc[i], far__ook[i
                ] = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(
                A[i]).isocalendar()
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((wxv__nnp,
            vzcm__psc, far__ook), idx, ('year', 'week', 'day'))
    return impl


class TimedeltaIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None, data=None):
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = types.Array(bodo.timedelta64ns, 1, 'C'
            ) if data is None else data
        super(TimedeltaIndexType, self).__init__(name=
            f'TimedeltaIndexType({name_typ}, {self.data})')
    ndim = 1

    def copy(self):
        return TimedeltaIndexType(self.name_typ)

    @property
    def dtype(self):
        return types.NPTimedelta('ns')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def key(self):
        return self.name_typ, self.data

    @property
    def iterator_type(self):
        return types.iterators.ArrayIterator(_timedelta_index_data_typ)

    @property
    def pandas_type_name(self):
        return 'timedelta'

    @property
    def numpy_type_name(self):
        return 'timedelta64[ns]'


timedelta_index = TimedeltaIndexType()
types.timedelta_index = timedelta_index


@register_model(TimedeltaIndexType)
class TimedeltaIndexTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        bagk__apz = [('data', _timedelta_index_data_typ), ('name', fe_type.
            name_typ), ('dict', types.DictType(_timedelta_index_data_typ.
            dtype, types.int64))]
        super(TimedeltaIndexTypeModel, self).__init__(dmm, fe_type, bagk__apz)


@typeof_impl.register(pd.TimedeltaIndex)
def typeof_timedelta_index(val, c):
    return TimedeltaIndexType(get_val_type_maybe_str_literal(val.name))


@box(TimedeltaIndexType)
def box_timedelta_index(typ, val, c):
    msaih__qjh = c.context.insert_const_string(c.builder.module, 'pandas')
    nved__gunq = c.pyapi.import_module_noblock(msaih__qjh)
    timedelta_index = numba.core.cgutils.create_struct_proxy(typ)(c.context,
        c.builder, val)
    c.context.nrt.incref(c.builder, _timedelta_index_data_typ,
        timedelta_index.data)
    esrs__dyqv = c.pyapi.from_native_value(_timedelta_index_data_typ,
        timedelta_index.data, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, timedelta_index.name)
    hqslu__vqos = c.pyapi.from_native_value(typ.name_typ, timedelta_index.
        name, c.env_manager)
    args = c.pyapi.tuple_pack([esrs__dyqv])
    kws = c.pyapi.dict_pack([('name', hqslu__vqos)])
    ecozs__ydz = c.pyapi.object_getattr_string(nved__gunq, 'TimedeltaIndex')
    ovnjl__sfp = c.pyapi.call(ecozs__ydz, args, kws)
    c.pyapi.decref(esrs__dyqv)
    c.pyapi.decref(hqslu__vqos)
    c.pyapi.decref(nved__gunq)
    c.pyapi.decref(ecozs__ydz)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return ovnjl__sfp


@unbox(TimedeltaIndexType)
def unbox_timedelta_index(typ, val, c):
    rntco__uxvls = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(_timedelta_index_data_typ, rntco__uxvls
        ).value
    hqslu__vqos = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, hqslu__vqos).value
    c.pyapi.decref(rntco__uxvls)
    c.pyapi.decref(hqslu__vqos)
    fsl__jyzo = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    fsl__jyzo.data = data
    fsl__jyzo.name = name
    dtype = _timedelta_index_data_typ.dtype
    hpki__zofg, xhae__qgdtp = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    fsl__jyzo.dict = xhae__qgdtp
    return NativeValue(fsl__jyzo._getvalue())


@intrinsic
def init_timedelta_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        hbh__dooi, uchpx__mljc = args
        timedelta_index = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        timedelta_index.data = hbh__dooi
        timedelta_index.name = uchpx__mljc
        context.nrt.incref(builder, signature.args[0], hbh__dooi)
        context.nrt.incref(builder, signature.args[1], uchpx__mljc)
        dtype = _timedelta_index_data_typ.dtype
        timedelta_index.dict = context.compile_internal(builder, lambda :
            numba.typed.Dict.empty(dtype, types.int64), types.DictType(
            dtype, types.int64)(), [])
        return timedelta_index._getvalue()
    qisew__yxm = TimedeltaIndexType(name)
    sig = signature(qisew__yxm, data, name)
    return sig, codegen


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_timedelta_index
    ) = init_index_equiv


@infer_getattr
class TimedeltaIndexAttribute(AttributeTemplate):
    key = TimedeltaIndexType

    def resolve_values(self, ary):
        return _timedelta_index_data_typ


make_attribute_wrapper(TimedeltaIndexType, 'data', '_data')
make_attribute_wrapper(TimedeltaIndexType, 'name', '_name')
make_attribute_wrapper(TimedeltaIndexType, 'dict', '_dict')


@overload_method(TimedeltaIndexType, 'copy', no_unliteral=True)
def overload_timedelta_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    imb__fgxdc = dict(deep=deep, dtype=dtype, names=names)
    nmz__jklhr = idx_typ_to_format_str_map[TimedeltaIndexType].format('copy()')
    check_unsupported_args('TimedeltaIndex.copy', imb__fgxdc,
        idx_cpy_arg_defaults, fn_str=nmz__jklhr, package_name='pandas',
        module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_timedelta_index(A._data.
                copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_timedelta_index(A._data.
                copy(), A._name)
    return impl


@overload_method(TimedeltaIndexType, 'min', inline='always', no_unliteral=True)
def overload_timedelta_index_min(tdi, axis=None, skipna=True):
    semue__ijsg = dict(axis=axis, skipna=skipna)
    kikhd__ufek = dict(axis=None, skipna=True)
    check_unsupported_args('TimedeltaIndex.min', semue__ijsg, kikhd__ufek,
        package_name='pandas', module_name='Index')

    def impl(tdi, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        data = bodo.hiframes.pd_index_ext.get_index_data(tdi)
        tqjc__xfk = len(data)
        jepx__awl = numba.cpython.builtins.get_type_max_value(numba.core.
            types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(tqjc__xfk):
            if bodo.libs.array_kernels.isna(data, i):
                continue
            val = (bodo.hiframes.datetime_timedelta_ext.
                cast_numpy_timedelta_to_int(data[i]))
            count += 1
            jepx__awl = min(jepx__awl, val)
        qxcu__xhph = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
            jepx__awl)
        return bodo.hiframes.pd_index_ext._tdi_val_finalize(qxcu__xhph, count)
    return impl


@overload_method(TimedeltaIndexType, 'max', inline='always', no_unliteral=True)
def overload_timedelta_index_max(tdi, axis=None, skipna=True):
    semue__ijsg = dict(axis=axis, skipna=skipna)
    kikhd__ufek = dict(axis=None, skipna=True)
    check_unsupported_args('TimedeltaIndex.max', semue__ijsg, kikhd__ufek,
        package_name='pandas', module_name='Index')
    if not is_overload_none(axis) or not is_overload_true(skipna):
        raise BodoError(
            'Index.min(): axis and skipna arguments not supported yet')

    def impl(tdi, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        data = bodo.hiframes.pd_index_ext.get_index_data(tdi)
        tqjc__xfk = len(data)
        dugr__jbibg = numba.cpython.builtins.get_type_min_value(numba.core.
            types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(tqjc__xfk):
            if bodo.libs.array_kernels.isna(data, i):
                continue
            val = (bodo.hiframes.datetime_timedelta_ext.
                cast_numpy_timedelta_to_int(data[i]))
            count += 1
            dugr__jbibg = max(dugr__jbibg, val)
        qxcu__xhph = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
            dugr__jbibg)
        return bodo.hiframes.pd_index_ext._tdi_val_finalize(qxcu__xhph, count)
    return impl


def gen_tdi_field_impl(field):
    pti__dai = 'def impl(tdi):\n'
    pti__dai += '    numba.parfors.parfor.init_prange()\n'
    pti__dai += '    A = bodo.hiframes.pd_index_ext.get_index_data(tdi)\n'
    pti__dai += '    name = bodo.hiframes.pd_index_ext.get_index_name(tdi)\n'
    pti__dai += '    n = len(A)\n'
    pti__dai += '    S = np.empty(n, np.int64)\n'
    pti__dai += '    for i in numba.parfors.parfor.internal_prange(n):\n'
    pti__dai += (
        '        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])\n'
        )
    if field == 'nanoseconds':
        pti__dai += '        S[i] = td64 % 1000\n'
    elif field == 'microseconds':
        pti__dai += '        S[i] = td64 // 1000 % 100000\n'
    elif field == 'seconds':
        pti__dai += (
            '        S[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
    elif field == 'days':
        pti__dai += '        S[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n'
    else:
        assert False, 'invalid timedelta field'
    pti__dai += (
        '    return bodo.hiframes.pd_index_ext.init_numeric_index(S, name)\n')
    ikpw__fvvvr = {}
    exec(pti__dai, {'numba': numba, 'np': np, 'bodo': bodo}, ikpw__fvvvr)
    impl = ikpw__fvvvr['impl']
    return impl


def _install_tdi_time_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        impl = gen_tdi_field_impl(field)
        overload_attribute(TimedeltaIndexType, field)(lambda tdi: impl)


_install_tdi_time_fields()


@overload(pd.TimedeltaIndex, no_unliteral=True)
def pd_timedelta_index_overload(data=None, unit=None, freq=None, dtype=None,
    copy=False, name=None):
    if is_overload_none(data):
        raise BodoError('data argument in pd.TimedeltaIndex() expected')
    semue__ijsg = dict(unit=unit, freq=freq, dtype=dtype, copy=copy)
    kikhd__ufek = dict(unit=None, freq=None, dtype=None, copy=False)
    check_unsupported_args('pandas.TimedeltaIndex', semue__ijsg,
        kikhd__ufek, package_name='pandas', module_name='Index')

    def impl(data=None, unit=None, freq=None, dtype=None, copy=False, name=None
        ):
        axs__zsie = bodo.utils.conversion.coerce_to_array(data)
        S = bodo.utils.conversion.convert_to_td64ns(axs__zsie)
        return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
    return impl


class RangeIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None):
        if name_typ is None:
            name_typ = types.none
        self.name_typ = name_typ
        super(RangeIndexType, self).__init__(name='RangeIndexType({})'.
            format(name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return RangeIndexType(self.name_typ)

    @property
    def iterator_type(self):
        return types.iterators.RangeIteratorType(types.int64)

    @property
    def dtype(self):
        return types.int64

    @property
    def pandas_type_name(self):
        return str(self.dtype)

    @property
    def numpy_type_name(self):
        return str(self.dtype)

    def unify(self, typingctx, other):
        if isinstance(other, NumericIndexType):
            name_typ = self.name_typ.unify(typingctx, other.name_typ)
            if name_typ is None:
                name_typ = types.none
            return NumericIndexType(types.int64, name_typ)


@typeof_impl.register(pd.RangeIndex)
def typeof_pd_range_index(val, c):
    return RangeIndexType(get_val_type_maybe_str_literal(val.name))


@register_model(RangeIndexType)
class RangeIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        bagk__apz = [('start', types.int64), ('stop', types.int64), ('step',
            types.int64), ('name', fe_type.name_typ)]
        super(RangeIndexModel, self).__init__(dmm, fe_type, bagk__apz)


make_attribute_wrapper(RangeIndexType, 'start', '_start')
make_attribute_wrapper(RangeIndexType, 'stop', '_stop')
make_attribute_wrapper(RangeIndexType, 'step', '_step')
make_attribute_wrapper(RangeIndexType, 'name', '_name')


@overload_method(RangeIndexType, 'copy', no_unliteral=True)
def overload_range_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    imb__fgxdc = dict(deep=deep, dtype=dtype, names=names)
    nmz__jklhr = idx_typ_to_format_str_map[RangeIndexType].format('copy()')
    check_unsupported_args('RangeIndex.copy', imb__fgxdc,
        idx_cpy_arg_defaults, fn_str=nmz__jklhr, package_name='pandas',
        module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_range_index(A._start, A.
                _stop, A._step, name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_range_index(A._start, A.
                _stop, A._step, A._name)
    return impl


@box(RangeIndexType)
def box_range_index(typ, val, c):
    msaih__qjh = c.context.insert_const_string(c.builder.module, 'pandas')
    fmg__imf = c.pyapi.import_module_noblock(msaih__qjh)
    pxona__tchhl = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    dntaz__ulem = c.pyapi.from_native_value(types.int64, pxona__tchhl.start,
        c.env_manager)
    amx__zxu = c.pyapi.from_native_value(types.int64, pxona__tchhl.stop, c.
        env_manager)
    nbp__zbyl = c.pyapi.from_native_value(types.int64, pxona__tchhl.step, c
        .env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, pxona__tchhl.name)
    hqslu__vqos = c.pyapi.from_native_value(typ.name_typ, pxona__tchhl.name,
        c.env_manager)
    args = c.pyapi.tuple_pack([dntaz__ulem, amx__zxu, nbp__zbyl])
    kws = c.pyapi.dict_pack([('name', hqslu__vqos)])
    ecozs__ydz = c.pyapi.object_getattr_string(fmg__imf, 'RangeIndex')
    zlxty__jdjxu = c.pyapi.call(ecozs__ydz, args, kws)
    c.pyapi.decref(dntaz__ulem)
    c.pyapi.decref(amx__zxu)
    c.pyapi.decref(nbp__zbyl)
    c.pyapi.decref(hqslu__vqos)
    c.pyapi.decref(fmg__imf)
    c.pyapi.decref(ecozs__ydz)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return zlxty__jdjxu


@intrinsic
def init_range_index(typingctx, start, stop, step, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        assert len(args) == 4
        pxona__tchhl = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        pxona__tchhl.start = args[0]
        pxona__tchhl.stop = args[1]
        pxona__tchhl.step = args[2]
        pxona__tchhl.name = args[3]
        context.nrt.incref(builder, signature.return_type.name_typ, args[3])
        return pxona__tchhl._getvalue()
    return RangeIndexType(name)(start, stop, step, name), codegen


def init_range_index_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 4 and not kws
    start, stop, step, mfgvy__dcl = args
    if self.typemap[start.name] == types.IntegerLiteral(0) and self.typemap[
        step.name] == types.IntegerLiteral(1) and equiv_set.has_shape(stop):
        return ArrayAnalysis.AnalyzeResult(shape=stop, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_range_index
    ) = init_range_index_equiv


@unbox(RangeIndexType)
def unbox_range_index(typ, val, c):
    dntaz__ulem = c.pyapi.object_getattr_string(val, 'start')
    start = c.pyapi.to_native_value(types.int64, dntaz__ulem).value
    amx__zxu = c.pyapi.object_getattr_string(val, 'stop')
    stop = c.pyapi.to_native_value(types.int64, amx__zxu).value
    nbp__zbyl = c.pyapi.object_getattr_string(val, 'step')
    step = c.pyapi.to_native_value(types.int64, nbp__zbyl).value
    hqslu__vqos = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, hqslu__vqos).value
    c.pyapi.decref(dntaz__ulem)
    c.pyapi.decref(amx__zxu)
    c.pyapi.decref(nbp__zbyl)
    c.pyapi.decref(hqslu__vqos)
    pxona__tchhl = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    pxona__tchhl.start = start
    pxona__tchhl.stop = stop
    pxona__tchhl.step = step
    pxona__tchhl.name = name
    return NativeValue(pxona__tchhl._getvalue())


@lower_constant(RangeIndexType)
def lower_constant_range_index(context, builder, ty, pyval):
    start = context.get_constant(types.int64, pyval.start)
    stop = context.get_constant(types.int64, pyval.stop)
    step = context.get_constant(types.int64, pyval.step)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    return lir.Constant.literal_struct([start, stop, step, name])


@overload(pd.RangeIndex, no_unliteral=True, inline='always')
def range_index_overload(start=None, stop=None, step=None, dtype=None, copy
    =False, name=None):

    def _ensure_int_or_none(value, field):
        qtyk__qedmf = (
            'RangeIndex(...) must be called with integers, {value} was passed for {field}'
            )
        if not is_overload_none(value) and not isinstance(value, types.
            IntegerLiteral) and not isinstance(value, types.Integer):
            raise BodoError(qtyk__qedmf.format(value=value, field=field))
    _ensure_int_or_none(start, 'start')
    _ensure_int_or_none(stop, 'stop')
    _ensure_int_or_none(step, 'step')
    if is_overload_none(start) and is_overload_none(stop) and is_overload_none(
        step):
        qtyk__qedmf = 'RangeIndex(...) must be called with integers'
        raise BodoError(qtyk__qedmf)
    fhmj__ocod = 'start'
    etc__belef = 'stop'
    yeuv__tzvfo = 'step'
    if is_overload_none(start):
        fhmj__ocod = '0'
    if is_overload_none(stop):
        etc__belef = 'start'
        fhmj__ocod = '0'
    if is_overload_none(step):
        yeuv__tzvfo = '1'
    pti__dai = """def _pd_range_index_imp(start=None, stop=None, step=None, dtype=None, copy=False, name=None):
"""
    pti__dai += '  return init_range_index({}, {}, {}, name)\n'.format(
        fhmj__ocod, etc__belef, yeuv__tzvfo)
    ikpw__fvvvr = {}
    exec(pti__dai, {'init_range_index': init_range_index}, ikpw__fvvvr)
    ryb__azcom = ikpw__fvvvr['_pd_range_index_imp']
    return ryb__azcom


@overload(pd.CategoricalIndex, no_unliteral=True, inline='always')
def categorical_index_overload(data=None, categories=None, ordered=None,
    dtype=None, copy=False, name=None):
    raise BodoError('pd.CategoricalIndex() initializer not yet supported.')


@overload_attribute(RangeIndexType, 'start')
def rangeIndex_get_start(ri):

    def impl(ri):
        return ri._start
    return impl


@overload_attribute(RangeIndexType, 'stop')
def rangeIndex_get_stop(ri):

    def impl(ri):
        return ri._stop
    return impl


@overload_attribute(RangeIndexType, 'step')
def rangeIndex_get_step(ri):

    def impl(ri):
        return ri._step
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_range_index_getitem(I, idx):
    if isinstance(I, RangeIndexType):
        if isinstance(types.unliteral(idx), types.Integer):
            return lambda I, idx: idx * I._step + I._start
        if isinstance(idx, types.SliceType):

            def impl(I, idx):
                wcyhs__czr = numba.cpython.unicode._normalize_slice(idx, len(I)
                    )
                name = bodo.hiframes.pd_index_ext.get_index_name(I)
                start = I._start + I._step * wcyhs__czr.start
                stop = I._start + I._step * wcyhs__czr.stop
                step = I._step * wcyhs__czr.step
                return bodo.hiframes.pd_index_ext.init_range_index(start,
                    stop, step, name)
            return impl
        return lambda I, idx: bodo.hiframes.pd_index_ext.init_numeric_index(np
            .arange(I._start, I._stop, I._step, np.int64)[idx], bodo.
            hiframes.pd_index_ext.get_index_name(I))


@overload(len, no_unliteral=True)
def overload_range_len(r):
    if isinstance(r, RangeIndexType):
        return lambda r: max(0, -(-(r._stop - r._start) // r._step))


class PeriodIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, freq, name_typ=None):
        name_typ = types.none if name_typ is None else name_typ
        self.freq = freq
        self.name_typ = name_typ
        super(PeriodIndexType, self).__init__(name=
            'PeriodIndexType({}, {})'.format(freq, name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return PeriodIndexType(self.freq, self.name_typ)

    @property
    def iterator_type(self):
        return types.iterators.ArrayIterator(types.Array(types.int64, 1, 'C'))

    @property
    def pandas_type_name(self):
        return 'object'

    @property
    def numpy_type_name(self):
        return f'period[{self.freq}]'


@typeof_impl.register(pd.PeriodIndex)
def typeof_pd_period_index(val, c):
    return PeriodIndexType(val.freqstr, get_val_type_maybe_str_literal(val.
        name))


@register_model(PeriodIndexType)
class PeriodIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        bagk__apz = [('data', bodo.IntegerArrayType(types.int64)), ('name',
            fe_type.name_typ), ('dict', types.DictType(types.int64, types.
            int64))]
        super(PeriodIndexModel, self).__init__(dmm, fe_type, bagk__apz)


make_attribute_wrapper(PeriodIndexType, 'data', '_data')
make_attribute_wrapper(PeriodIndexType, 'name', '_name')
make_attribute_wrapper(PeriodIndexType, 'dict', '_dict')


@overload_method(PeriodIndexType, 'copy', no_unliteral=True)
def overload_period_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    freq = A.freq
    imb__fgxdc = dict(deep=deep, dtype=dtype, names=names)
    nmz__jklhr = idx_typ_to_format_str_map[PeriodIndexType].format('copy()')
    check_unsupported_args('PeriodIndex.copy', imb__fgxdc,
        idx_cpy_arg_defaults, fn_str=nmz__jklhr, package_name='pandas',
        module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_period_index(A._data.
                copy(), name, freq)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_period_index(A._data.
                copy(), A._name, freq)
    return impl


@intrinsic
def init_period_index(typingctx, data, name, freq):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        hbh__dooi, uchpx__mljc, mfgvy__dcl = args
        vpc__qnkj = signature.return_type
        quzk__bmj = cgutils.create_struct_proxy(vpc__qnkj)(context, builder)
        quzk__bmj.data = hbh__dooi
        quzk__bmj.name = uchpx__mljc
        context.nrt.incref(builder, signature.args[0], args[0])
        context.nrt.incref(builder, signature.args[1], args[1])
        quzk__bmj.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(types.int64, types.int64), types.DictType(
            types.int64, types.int64)(), [])
        return quzk__bmj._getvalue()
    apwwf__lnl = get_overload_const_str(freq)
    qisew__yxm = PeriodIndexType(apwwf__lnl, name)
    sig = signature(qisew__yxm, data, name, freq)
    return sig, codegen


@box(PeriodIndexType)
def box_period_index(typ, val, c):
    msaih__qjh = c.context.insert_const_string(c.builder.module, 'pandas')
    fmg__imf = c.pyapi.import_module_noblock(msaih__qjh)
    fsl__jyzo = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, bodo.IntegerArrayType(types.int64),
        fsl__jyzo.data)
    mzim__zhfm = c.pyapi.from_native_value(bodo.IntegerArrayType(types.
        int64), fsl__jyzo.data, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, fsl__jyzo.name)
    hqslu__vqos = c.pyapi.from_native_value(typ.name_typ, fsl__jyzo.name, c
        .env_manager)
    qydel__ypqtt = c.pyapi.string_from_constant_string(typ.freq)
    args = c.pyapi.tuple_pack([])
    kws = c.pyapi.dict_pack([('ordinal', mzim__zhfm), ('name', hqslu__vqos),
        ('freq', qydel__ypqtt)])
    ecozs__ydz = c.pyapi.object_getattr_string(fmg__imf, 'PeriodIndex')
    zlxty__jdjxu = c.pyapi.call(ecozs__ydz, args, kws)
    c.pyapi.decref(mzim__zhfm)
    c.pyapi.decref(hqslu__vqos)
    c.pyapi.decref(qydel__ypqtt)
    c.pyapi.decref(fmg__imf)
    c.pyapi.decref(ecozs__ydz)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return zlxty__jdjxu


@unbox(PeriodIndexType)
def unbox_period_index(typ, val, c):
    arr_typ = bodo.IntegerArrayType(types.int64)
    zkil__fea = c.pyapi.object_getattr_string(val, 'asi8')
    rts__mvzy = c.pyapi.call_method(val, 'isna', ())
    hqslu__vqos = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, hqslu__vqos).value
    msaih__qjh = c.context.insert_const_string(c.builder.module, 'pandas')
    nved__gunq = c.pyapi.import_module_noblock(msaih__qjh)
    ceea__bul = c.pyapi.object_getattr_string(nved__gunq, 'arrays')
    mzim__zhfm = c.pyapi.call_method(ceea__bul, 'IntegerArray', (zkil__fea,
        rts__mvzy))
    data = c.pyapi.to_native_value(arr_typ, mzim__zhfm).value
    c.pyapi.decref(zkil__fea)
    c.pyapi.decref(rts__mvzy)
    c.pyapi.decref(hqslu__vqos)
    c.pyapi.decref(nved__gunq)
    c.pyapi.decref(ceea__bul)
    c.pyapi.decref(mzim__zhfm)
    fsl__jyzo = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    fsl__jyzo.data = data
    fsl__jyzo.name = name
    hpki__zofg, xhae__qgdtp = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(types.int64, types.int64), types.DictType(types.int64,
        types.int64)(), [])
    fsl__jyzo.dict = xhae__qgdtp
    return NativeValue(fsl__jyzo._getvalue())


class CategoricalIndexType(types.ArrayCompatible):

    def __init__(self, data, name_typ=None):
        from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
        assert isinstance(data, CategoricalArrayType
            ), 'CategoricalIndexType expects CategoricalArrayType'
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = data
        super(CategoricalIndexType, self).__init__(name=
            f'CategoricalIndexType(data={self.data}, name={name_typ})')
    ndim = 1

    def copy(self):
        return CategoricalIndexType(self.data, self.name_typ)

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return self.data.dtype

    @property
    def key(self):
        return self.data, self.name_typ

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def pandas_type_name(self):
        return 'categorical'

    @property
    def numpy_type_name(self):
        from bodo.hiframes.pd_categorical_ext import get_categories_int_type
        return str(get_categories_int_type(self.dtype))


@register_model(CategoricalIndexType)
class CategoricalIndexTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        from bodo.hiframes.pd_categorical_ext import get_categories_int_type
        tul__uiet = get_categories_int_type(fe_type.data.dtype)
        bagk__apz = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(tul__uiet, types.int64))]
        super(CategoricalIndexTypeModel, self).__init__(dmm, fe_type, bagk__apz
            )


@typeof_impl.register(pd.CategoricalIndex)
def typeof_categorical_index(val, c):
    return CategoricalIndexType(bodo.typeof(val.values),
        get_val_type_maybe_str_literal(val.name))


@box(CategoricalIndexType)
def box_categorical_index(typ, val, c):
    msaih__qjh = c.context.insert_const_string(c.builder.module, 'pandas')
    nved__gunq = c.pyapi.import_module_noblock(msaih__qjh)
    pvif__ealw = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, typ.data, pvif__ealw.data)
    esrs__dyqv = c.pyapi.from_native_value(typ.data, pvif__ealw.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, pvif__ealw.name)
    hqslu__vqos = c.pyapi.from_native_value(typ.name_typ, pvif__ealw.name,
        c.env_manager)
    args = c.pyapi.tuple_pack([esrs__dyqv])
    kws = c.pyapi.dict_pack([('name', hqslu__vqos)])
    ecozs__ydz = c.pyapi.object_getattr_string(nved__gunq, 'CategoricalIndex')
    ovnjl__sfp = c.pyapi.call(ecozs__ydz, args, kws)
    c.pyapi.decref(esrs__dyqv)
    c.pyapi.decref(hqslu__vqos)
    c.pyapi.decref(nved__gunq)
    c.pyapi.decref(ecozs__ydz)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return ovnjl__sfp


@unbox(CategoricalIndexType)
def unbox_categorical_index(typ, val, c):
    from bodo.hiframes.pd_categorical_ext import get_categories_int_type
    rntco__uxvls = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, rntco__uxvls).value
    hqslu__vqos = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, hqslu__vqos).value
    c.pyapi.decref(rntco__uxvls)
    c.pyapi.decref(hqslu__vqos)
    fsl__jyzo = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    fsl__jyzo.data = data
    fsl__jyzo.name = name
    dtype = get_categories_int_type(typ.data.dtype)
    hpki__zofg, xhae__qgdtp = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    fsl__jyzo.dict = xhae__qgdtp
    return NativeValue(fsl__jyzo._getvalue())


@intrinsic
def init_categorical_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        from bodo.hiframes.pd_categorical_ext import get_categories_int_type
        hbh__dooi, uchpx__mljc = args
        pvif__ealw = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        pvif__ealw.data = hbh__dooi
        pvif__ealw.name = uchpx__mljc
        context.nrt.incref(builder, signature.args[0], hbh__dooi)
        context.nrt.incref(builder, signature.args[1], uchpx__mljc)
        dtype = get_categories_int_type(signature.return_type.data.dtype)
        pvif__ealw.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return pvif__ealw._getvalue()
    qisew__yxm = CategoricalIndexType(data, name)
    sig = signature(qisew__yxm, data, name)
    return sig, codegen


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_index_ext_init_categorical_index
    ) = init_index_equiv
make_attribute_wrapper(CategoricalIndexType, 'data', '_data')
make_attribute_wrapper(CategoricalIndexType, 'name', '_name')
make_attribute_wrapper(CategoricalIndexType, 'dict', '_dict')


@overload_method(CategoricalIndexType, 'copy', no_unliteral=True)
def overload_categorical_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    nmz__jklhr = idx_typ_to_format_str_map[CategoricalIndexType].format(
        'copy()')
    imb__fgxdc = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('CategoricalIndex.copy', imb__fgxdc,
        idx_cpy_arg_defaults, fn_str=nmz__jklhr, package_name='pandas',
        module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_categorical_index(A.
                _data.copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_categorical_index(A.
                _data.copy(), A._name)
    return impl


class IntervalIndexType(types.ArrayCompatible):

    def __init__(self, data, name_typ=None):
        from bodo.libs.interval_arr_ext import IntervalArrayType
        assert isinstance(data, IntervalArrayType
            ), 'IntervalIndexType expects IntervalArrayType'
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = data
        super(IntervalIndexType, self).__init__(name=
            f'IntervalIndexType(data={self.data}, name={name_typ})')
    ndim = 1

    def copy(self):
        return IntervalIndexType(self.data, self.name_typ)

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def key(self):
        return self.data, self.name_typ

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def pandas_type_name(self):
        return 'object'

    @property
    def numpy_type_name(self):
        return f'interval[{self.data.arr_type.dtype}, right]'


@register_model(IntervalIndexType)
class IntervalIndexTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        bagk__apz = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(types.UniTuple(fe_type.data.arr_type.
            dtype, 2), types.int64))]
        super(IntervalIndexTypeModel, self).__init__(dmm, fe_type, bagk__apz)


@typeof_impl.register(pd.IntervalIndex)
def typeof_interval_index(val, c):
    return IntervalIndexType(bodo.typeof(val.values),
        get_val_type_maybe_str_literal(val.name))


@box(IntervalIndexType)
def box_interval_index(typ, val, c):
    msaih__qjh = c.context.insert_const_string(c.builder.module, 'pandas')
    nved__gunq = c.pyapi.import_module_noblock(msaih__qjh)
    hjj__qlsxf = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, typ.data, hjj__qlsxf.data)
    esrs__dyqv = c.pyapi.from_native_value(typ.data, hjj__qlsxf.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, hjj__qlsxf.name)
    hqslu__vqos = c.pyapi.from_native_value(typ.name_typ, hjj__qlsxf.name,
        c.env_manager)
    args = c.pyapi.tuple_pack([esrs__dyqv])
    kws = c.pyapi.dict_pack([('name', hqslu__vqos)])
    ecozs__ydz = c.pyapi.object_getattr_string(nved__gunq, 'IntervalIndex')
    ovnjl__sfp = c.pyapi.call(ecozs__ydz, args, kws)
    c.pyapi.decref(esrs__dyqv)
    c.pyapi.decref(hqslu__vqos)
    c.pyapi.decref(nved__gunq)
    c.pyapi.decref(ecozs__ydz)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return ovnjl__sfp


@unbox(IntervalIndexType)
def unbox_interval_index(typ, val, c):
    rntco__uxvls = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, rntco__uxvls).value
    hqslu__vqos = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, hqslu__vqos).value
    c.pyapi.decref(rntco__uxvls)
    c.pyapi.decref(hqslu__vqos)
    fsl__jyzo = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    fsl__jyzo.data = data
    fsl__jyzo.name = name
    dtype = types.UniTuple(typ.data.arr_type.dtype, 2)
    hpki__zofg, xhae__qgdtp = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    fsl__jyzo.dict = xhae__qgdtp
    return NativeValue(fsl__jyzo._getvalue())


@intrinsic
def init_interval_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        hbh__dooi, uchpx__mljc = args
        hjj__qlsxf = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        hjj__qlsxf.data = hbh__dooi
        hjj__qlsxf.name = uchpx__mljc
        context.nrt.incref(builder, signature.args[0], hbh__dooi)
        context.nrt.incref(builder, signature.args[1], uchpx__mljc)
        dtype = types.UniTuple(data.arr_type.dtype, 2)
        hjj__qlsxf.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return hjj__qlsxf._getvalue()
    qisew__yxm = IntervalIndexType(data, name)
    sig = signature(qisew__yxm, data, name)
    return sig, codegen


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_interval_index
    ) = init_index_equiv
make_attribute_wrapper(IntervalIndexType, 'data', '_data')
make_attribute_wrapper(IntervalIndexType, 'name', '_name')
make_attribute_wrapper(IntervalIndexType, 'dict', '_dict')


class NumericIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, dtype, name_typ=None, data=None):
        name_typ = types.none if name_typ is None else name_typ
        self.dtype = dtype
        self.name_typ = name_typ
        data = dtype_to_array_type(dtype) if data is None else data
        self.data = data
        super(NumericIndexType, self).__init__(name=
            f'NumericIndexType({dtype}, {name_typ}, {data})')
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return NumericIndexType(self.dtype, self.name_typ, self.data)

    @property
    def iterator_type(self):
        return types.iterators.ArrayIterator(types.Array(self.dtype, 1, 'C'))

    @property
    def pandas_type_name(self):
        return str(self.dtype)

    @property
    def numpy_type_name(self):
        return str(self.dtype)


@typeof_impl.register(pd.Int64Index)
def typeof_pd_int64_index(val, c):
    return NumericIndexType(types.int64, get_val_type_maybe_str_literal(val
        .name))


@typeof_impl.register(pd.UInt64Index)
def typeof_pd_uint64_index(val, c):
    return NumericIndexType(types.uint64, get_val_type_maybe_str_literal(
        val.name))


@typeof_impl.register(pd.Float64Index)
def typeof_pd_float64_index(val, c):
    return NumericIndexType(types.float64, get_val_type_maybe_str_literal(
        val.name))


@register_model(NumericIndexType)
class NumericIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        bagk__apz = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(fe_type.dtype, types.int64))]
        super(NumericIndexModel, self).__init__(dmm, fe_type, bagk__apz)


make_attribute_wrapper(NumericIndexType, 'data', '_data')
make_attribute_wrapper(NumericIndexType, 'name', '_name')
make_attribute_wrapper(NumericIndexType, 'dict', '_dict')


@overload_method(NumericIndexType, 'copy', no_unliteral=True)
def overload_numeric_index_copy(A, name=None, deep=False, dtype=None, names
    =None):
    nmz__jklhr = idx_typ_to_format_str_map[NumericIndexType].format('copy()')
    imb__fgxdc = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', imb__fgxdc, idx_cpy_arg_defaults,
        fn_str=nmz__jklhr, package_name='pandas', module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_numeric_index(A._data.
                copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_numeric_index(A._data.
                copy(), A._name)
    return impl


@box(NumericIndexType)
def box_numeric_index(typ, val, c):
    msaih__qjh = c.context.insert_const_string(c.builder.module, 'pandas')
    fmg__imf = c.pyapi.import_module_noblock(msaih__qjh)
    fsl__jyzo = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.data, fsl__jyzo.data)
    mzim__zhfm = c.pyapi.from_native_value(typ.data, fsl__jyzo.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, fsl__jyzo.name)
    hqslu__vqos = c.pyapi.from_native_value(typ.name_typ, fsl__jyzo.name, c
        .env_manager)
    vso__jjvd = c.pyapi.make_none()
    pcuy__czpm = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    zlxty__jdjxu = c.pyapi.call_method(fmg__imf, 'Index', (mzim__zhfm,
        vso__jjvd, pcuy__czpm, hqslu__vqos))
    c.pyapi.decref(mzim__zhfm)
    c.pyapi.decref(vso__jjvd)
    c.pyapi.decref(pcuy__czpm)
    c.pyapi.decref(hqslu__vqos)
    c.pyapi.decref(fmg__imf)
    c.context.nrt.decref(c.builder, typ, val)
    return zlxty__jdjxu


@intrinsic
def init_numeric_index(typingctx, data, name=None):
    name = types.none if is_overload_none(name) else name

    def codegen(context, builder, signature, args):
        assert len(args) == 2
        vpc__qnkj = signature.return_type
        fsl__jyzo = cgutils.create_struct_proxy(vpc__qnkj)(context, builder)
        fsl__jyzo.data = args[0]
        fsl__jyzo.name = args[1]
        context.nrt.incref(builder, vpc__qnkj.data, args[0])
        context.nrt.incref(builder, vpc__qnkj.name_typ, args[1])
        dtype = vpc__qnkj.dtype
        fsl__jyzo.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return fsl__jyzo._getvalue()
    return NumericIndexType(data.dtype, name, data)(data, name), codegen


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_numeric_index
    ) = init_index_equiv


@unbox(NumericIndexType)
def unbox_numeric_index(typ, val, c):
    rntco__uxvls = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, rntco__uxvls).value
    hqslu__vqos = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, hqslu__vqos).value
    c.pyapi.decref(rntco__uxvls)
    c.pyapi.decref(hqslu__vqos)
    fsl__jyzo = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    fsl__jyzo.data = data
    fsl__jyzo.name = name
    dtype = typ.dtype
    hpki__zofg, xhae__qgdtp = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    fsl__jyzo.dict = xhae__qgdtp
    return NativeValue(fsl__jyzo._getvalue())


def create_numeric_constructor(func, func_str, default_dtype):

    def overload_impl(data=None, dtype=None, copy=False, name=None):
        pau__voupt = dict(dtype=dtype)
        ltckm__zlffs = dict(dtype=None)
        check_unsupported_args(func_str, pau__voupt, ltckm__zlffs,
            package_name='pandas', module_name='Index')
        if is_overload_false(copy):

            def impl(data=None, dtype=None, copy=False, name=None):
                axs__zsie = bodo.utils.conversion.coerce_to_ndarray(data)
                zbceq__jgaw = bodo.utils.conversion.fix_arr_dtype(axs__zsie,
                    np.dtype(default_dtype))
                return bodo.hiframes.pd_index_ext.init_numeric_index(
                    zbceq__jgaw, name)
        else:

            def impl(data=None, dtype=None, copy=False, name=None):
                axs__zsie = bodo.utils.conversion.coerce_to_ndarray(data)
                if copy:
                    axs__zsie = axs__zsie.copy()
                zbceq__jgaw = bodo.utils.conversion.fix_arr_dtype(axs__zsie,
                    np.dtype(default_dtype))
                return bodo.hiframes.pd_index_ext.init_numeric_index(
                    zbceq__jgaw, name)
        return impl
    return overload_impl


def _install_numeric_constructors():
    for func, func_str, default_dtype in ((pd.Int64Index,
        'pandas.Int64Index', np.int64), (pd.UInt64Index,
        'pandas.UInt64Index', np.uint64), (pd.Float64Index,
        'pandas.Float64Index', np.float64)):
        overload_impl = create_numeric_constructor(func, func_str,
            default_dtype)
        overload(func, no_unliteral=True)(overload_impl)


_install_numeric_constructors()


class StringIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None):
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = string_array_type
        super(StringIndexType, self).__init__(name='StringIndexType({})'.
            format(name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return StringIndexType(self.name_typ)

    @property
    def dtype(self):
        return string_type

    @property
    def pandas_type_name(self):
        return 'unicode'

    @property
    def numpy_type_name(self):
        return 'object'

    @property
    def iterator_type(self):
        return bodo.libs.str_arr_ext.StringArrayIterator()


@register_model(StringIndexType)
class StringIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        bagk__apz = [('data', string_array_type), ('name', fe_type.name_typ
            ), ('dict', types.DictType(string_type, types.int64))]
        super(StringIndexModel, self).__init__(dmm, fe_type, bagk__apz)


make_attribute_wrapper(StringIndexType, 'data', '_data')
make_attribute_wrapper(StringIndexType, 'name', '_name')
make_attribute_wrapper(StringIndexType, 'dict', '_dict')


class BinaryIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None):
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = binary_array_type
        super(BinaryIndexType, self).__init__(name='BinaryIndexType({})'.
            format(name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return BinaryIndexType(self.name_typ)

    @property
    def dtype(self):
        return bytes_type

    @property
    def pandas_type_name(self):
        return 'bytes'

    @property
    def numpy_type_name(self):
        return 'object'

    @property
    def iterator_type(self):
        return bodo.libs.binary_arr_ext.BinaryArrayIterator()


@register_model(BinaryIndexType)
class BinaryIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        bagk__apz = [('data', binary_array_type), ('name', fe_type.name_typ
            ), ('dict', types.DictType(bytes_type, types.int64))]
        super(BinaryIndexModel, self).__init__(dmm, fe_type, bagk__apz)


make_attribute_wrapper(BinaryIndexType, 'data', '_data')
make_attribute_wrapper(BinaryIndexType, 'name', '_name')
make_attribute_wrapper(BinaryIndexType, 'dict', '_dict')


@unbox(BinaryIndexType)
@unbox(StringIndexType)
def unbox_binary_str_index(typ, val, c):
    vzwm__dxy = typ.data
    scalar_type = typ.data.dtype
    rntco__uxvls = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(vzwm__dxy, rntco__uxvls).value
    hqslu__vqos = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, hqslu__vqos).value
    c.pyapi.decref(rntco__uxvls)
    c.pyapi.decref(hqslu__vqos)
    fsl__jyzo = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    fsl__jyzo.data = data
    fsl__jyzo.name = name
    hpki__zofg, xhae__qgdtp = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(scalar_type, types.int64), types.DictType(scalar_type,
        types.int64)(), [])
    fsl__jyzo.dict = xhae__qgdtp
    return NativeValue(fsl__jyzo._getvalue())


@box(BinaryIndexType)
@box(StringIndexType)
def box_binary_str_index(typ, val, c):
    vzwm__dxy = typ.data
    msaih__qjh = c.context.insert_const_string(c.builder.module, 'pandas')
    fmg__imf = c.pyapi.import_module_noblock(msaih__qjh)
    fsl__jyzo = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, vzwm__dxy, fsl__jyzo.data)
    mzim__zhfm = c.pyapi.from_native_value(vzwm__dxy, fsl__jyzo.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, fsl__jyzo.name)
    hqslu__vqos = c.pyapi.from_native_value(typ.name_typ, fsl__jyzo.name, c
        .env_manager)
    vso__jjvd = c.pyapi.make_none()
    pcuy__czpm = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    zlxty__jdjxu = c.pyapi.call_method(fmg__imf, 'Index', (mzim__zhfm,
        vso__jjvd, pcuy__czpm, hqslu__vqos))
    c.pyapi.decref(mzim__zhfm)
    c.pyapi.decref(vso__jjvd)
    c.pyapi.decref(pcuy__czpm)
    c.pyapi.decref(hqslu__vqos)
    c.pyapi.decref(fmg__imf)
    c.context.nrt.decref(c.builder, typ, val)
    return zlxty__jdjxu


@intrinsic
def init_binary_str_index(typingctx, data, name=None):
    name = types.none if name is None else name
    sig = type(bodo.utils.typing.get_index_type_from_dtype(data.dtype))(name)(
        data, name)
    qyome__fov = get_binary_str_codegen(is_binary=data.dtype == bytes_type)
    return sig, qyome__fov


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_index_ext_init_binary_str_index
    ) = init_index_equiv


def get_binary_str_codegen(is_binary=False):
    if is_binary:
        yfw__kycwo = 'binary_array_type'
        dxfb__oewum = 'bytes_type'
    else:
        yfw__kycwo = 'string_array_type'
        dxfb__oewum = 'string_type'
    pti__dai = 'def impl(context, builder, signature, args):\n'
    pti__dai += '    assert len(args) == 2\n'
    pti__dai += '    index_typ = signature.return_type\n'
    pti__dai += (
        '    index_val = cgutils.create_struct_proxy(index_typ)(context, builder)\n'
        )
    pti__dai += '    index_val.data = args[0]\n'
    pti__dai += '    index_val.name = args[1]\n'
    pti__dai += '    # increase refcount of stored values\n'
    pti__dai += f'    context.nrt.incref(builder, {yfw__kycwo}, args[0])\n'
    pti__dai += (
        '    context.nrt.incref(builder, index_typ.name_typ, args[1])\n')
    pti__dai += '    # create empty dict for get_loc hashmap\n'
    pti__dai += '    index_val.dict = context.compile_internal(\n'
    pti__dai += '       builder,\n'
    pti__dai += (
        f'       lambda: numba.typed.Dict.empty({dxfb__oewum}, types.int64),\n'
        )
    pti__dai += f'        types.DictType({dxfb__oewum}, types.int64)(), [],)\n'
    pti__dai += '    return index_val._getvalue()\n'
    ikpw__fvvvr = {}
    exec(pti__dai, {'bodo': bodo, 'signature': signature, 'cgutils':
        cgutils, 'numba': numba, 'types': types, 'bytes_type': bytes_type,
        'string_type': string_type, 'string_array_type': string_array_type,
        'binary_array_type': binary_array_type}, ikpw__fvvvr)
    impl = ikpw__fvvvr['impl']
    return impl


@overload_method(BinaryIndexType, 'copy', no_unliteral=True)
@overload_method(StringIndexType, 'copy', no_unliteral=True)
def overload_binary_string_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    typ = type(A)
    nmz__jklhr = idx_typ_to_format_str_map[typ].format('copy()')
    imb__fgxdc = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', imb__fgxdc, idx_cpy_arg_defaults,
        fn_str=nmz__jklhr, package_name='pandas', module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_binary_str_index(A._data
                .copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_binary_str_index(A._data
                .copy(), A._name)
    return impl


@overload_attribute(BinaryIndexType, 'name')
@overload_attribute(StringIndexType, 'name')
@overload_attribute(DatetimeIndexType, 'name')
@overload_attribute(TimedeltaIndexType, 'name')
@overload_attribute(RangeIndexType, 'name')
@overload_attribute(PeriodIndexType, 'name')
@overload_attribute(NumericIndexType, 'name')
@overload_attribute(IntervalIndexType, 'name')
@overload_attribute(CategoricalIndexType, 'name')
@overload_attribute(MultiIndexType, 'name')
def Index_get_name(i):

    def impl(i):
        return i._name
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_index_getitem(I, ind):
    if isinstance(I, (NumericIndexType, StringIndexType, BinaryIndexType)
        ) and isinstance(ind, types.Integer):
        return lambda I, ind: bodo.hiframes.pd_index_ext.get_index_data(I)[ind]
    if isinstance(I, NumericIndexType):
        return lambda I, ind: bodo.hiframes.pd_index_ext.init_numeric_index(
            bodo.hiframes.pd_index_ext.get_index_data(I)[ind], bodo.
            hiframes.pd_index_ext.get_index_name(I))
    if isinstance(I, (StringIndexType, BinaryIndexType)):
        return lambda I, ind: bodo.hiframes.pd_index_ext.init_binary_str_index(
            bodo.hiframes.pd_index_ext.get_index_data(I)[ind], bodo.
            hiframes.pd_index_ext.get_index_name(I))


def array_type_to_index(arr_typ, name_typ=None):
    if arr_typ == bodo.string_array_type:
        return StringIndexType(name_typ)
    if arr_typ == bodo.binary_array_type:
        return BinaryIndexType(name_typ)
    assert isinstance(arr_typ, (types.Array, IntegerArrayType, bodo.
        CategoricalArrayType)) or arr_typ in (bodo.datetime_date_array_type,
        bodo.boolean_array
        ), f'Converting array type {arr_typ} to index not supported'
    if (arr_typ == bodo.datetime_date_array_type or arr_typ.dtype == types.
        NPDatetime('ns')):
        return DatetimeIndexType(name_typ)
    if isinstance(arr_typ, bodo.CategoricalArrayType):
        return CategoricalIndexType(arr_typ, name_typ)
    if arr_typ.dtype == types.NPTimedelta('ns'):
        return TimedeltaIndexType(name_typ)
    if isinstance(arr_typ.dtype, (types.Integer, types.Float, types.Boolean)):
        return NumericIndexType(arr_typ.dtype, name_typ, arr_typ)
    raise BodoError(f'invalid index type {arr_typ}')


def is_pd_index_type(t):
    return isinstance(t, (NumericIndexType, DatetimeIndexType,
        TimedeltaIndexType, IntervalIndexType, CategoricalIndexType,
        PeriodIndexType, StringIndexType, BinaryIndexType, RangeIndexType,
        HeterogeneousIndexType))


@overload_method(RangeIndexType, 'take', no_unliteral=True)
@overload_method(NumericIndexType, 'take', no_unliteral=True)
@overload_method(StringIndexType, 'take', no_unliteral=True)
@overload_method(BinaryIndexType, 'take', no_unliteral=True)
@overload_method(CategoricalIndexType, 'take', no_unliteral=True)
@overload_method(PeriodIndexType, 'take', no_unliteral=True)
@overload_method(DatetimeIndexType, 'take', no_unliteral=True)
@overload_method(TimedeltaIndexType, 'take', no_unliteral=True)
def overload_index_take(I, indices, axis=0, allow_fill=True, fill_value=None):
    semue__ijsg = dict(axis=axis, allow_fill=allow_fill, fill_value=fill_value)
    rtgy__wjt = dict(axis=0, allow_fill=True, fill_value=None)
    check_unsupported_args('Index.take', semue__ijsg, rtgy__wjt,
        package_name='pandas', module_name='Index')
    return lambda I, indices: I[indices]


@numba.njit(no_cpython_wrapper=True)
def _init_engine(I):
    if len(I) > 0 and not I._dict:
        mgs__uxh = bodo.utils.conversion.coerce_to_array(I)
        for i in range(len(mgs__uxh)):
            val = mgs__uxh[i]
            if val in I._dict:
                raise ValueError(
                    'Index.get_loc(): non-unique Index not supported yet')
            I._dict[val] = i


@overload(operator.contains, no_unliteral=True)
def index_contains(I, val):
    if not is_index_type(I):
        return
    if isinstance(I, RangeIndexType):
        return lambda I, val: range_contains(I.start, I.stop, I.step, val)

    def impl(I, val):
        key = bodo.utils.conversion.unbox_if_timestamp(val)
        if not is_null_value(I._dict):
            _init_engine(I)
            return key in I._dict
        else:
            qtyk__qedmf = (
                'Global Index objects can be slow (pass as argument to JIT function for better performance).'
                )
            warnings.warn(qtyk__qedmf)
            mgs__uxh = bodo.utils.conversion.coerce_to_array(I)
            ind = -1
            for i in range(len(mgs__uxh)):
                if mgs__uxh[i] == key:
                    if ind != -1:
                        raise ValueError(
                            'Index.get_loc(): non-unique Index not supported yet'
                            )
                    ind = i
        return ind != -1
    return impl


@register_jitable
def range_contains(start, stop, step, val):
    if step > 0 and not start <= val < stop:
        return False
    if step < 0 and not stop <= val < start:
        return False
    return (val - start) % step == 0


@overload_method(RangeIndexType, 'get_loc', no_unliteral=True)
@overload_method(NumericIndexType, 'get_loc', no_unliteral=True)
@overload_method(StringIndexType, 'get_loc', no_unliteral=True)
@overload_method(BinaryIndexType, 'get_loc', no_unliteral=True)
@overload_method(PeriodIndexType, 'get_loc', no_unliteral=True)
@overload_method(DatetimeIndexType, 'get_loc', no_unliteral=True)
@overload_method(TimedeltaIndexType, 'get_loc', no_unliteral=True)
def overload_index_get_loc(I, key, method=None, tolerance=None):
    semue__ijsg = dict(method=method, tolerance=tolerance)
    kikhd__ufek = dict(method=None, tolerance=None)
    check_unsupported_args('Index.get_loc', semue__ijsg, kikhd__ufek,
        package_name='pandas', module_name='Index')
    key = types.unliteral(key)
    if key == pd_timestamp_type:
        key = bodo.datetime64ns
    if key == pd_timedelta_type:
        key = bodo.timedelta64ns
    if key != I.dtype:
        raise_bodo_error(
            'Index.get_loc(): invalid label type in Index.get_loc()')
    if isinstance(I, RangeIndexType):

        def impl_range(I, key, method=None, tolerance=None):
            if not range_contains(I.start, I.stop, I.step, key):
                raise KeyError('Index.get_loc(): key not found')
            return key - I.start if I.step == 1 else (key - I.start) // I.step
        return impl_range

    def impl(I, key, method=None, tolerance=None):
        key = bodo.utils.conversion.unbox_if_timestamp(key)
        if not is_null_value(I._dict):
            _init_engine(I)
            ind = I._dict.get(key, -1)
        else:
            qtyk__qedmf = (
                'Index.get_loc() can be slow for global Index objects (pass as argument to JIT function for better performance).'
                )
            warnings.warn(qtyk__qedmf)
            mgs__uxh = bodo.utils.conversion.coerce_to_array(I)
            ind = -1
            for i in range(len(mgs__uxh)):
                if mgs__uxh[i] == key:
                    if ind != -1:
                        raise ValueError(
                            'Index.get_loc(): non-unique Index not supported yet'
                            )
                    ind = i
        if ind == -1:
            raise KeyError('Index.get_loc(): key not found')
        return ind
    return impl


def create_isna_specific_method(overload_name):

    def overload_index_isna_specific_method(I):
        svy__qmt = overload_name in {'isna', 'isnull'}
        if isinstance(I, RangeIndexType):

            def impl(I):
                numba.parfors.parfor.init_prange()
                tqjc__xfk = len(I)
                kjku__eek = np.empty(tqjc__xfk, np.bool_)
                for i in numba.parfors.parfor.internal_prange(tqjc__xfk):
                    kjku__eek[i] = not svy__qmt
                return kjku__eek
            return impl
        pti__dai = f"""def impl(I):
    numba.parfors.parfor.init_prange()
    arr = bodo.hiframes.pd_index_ext.get_index_data(I)
    n = len(arr)
    out_arr = np.empty(n, np.bool_)
    for i in numba.parfors.parfor.internal_prange(n):
       out_arr[i] = {'' if svy__qmt else 'not '}bodo.libs.array_kernels.isna(arr, i)
    return out_arr
"""
        ikpw__fvvvr = {}
        exec(pti__dai, {'bodo': bodo, 'np': np, 'numba': numba}, ikpw__fvvvr)
        impl = ikpw__fvvvr['impl']
        return impl
    return overload_index_isna_specific_method


isna_overload_types = (RangeIndexType, NumericIndexType, StringIndexType,
    BinaryIndexType, CategoricalIndexType, PeriodIndexType,
    DatetimeIndexType, TimedeltaIndexType)
isna_specific_methods = 'isna', 'notna', 'isnull', 'notnull'


def _install_isna_specific_methods():
    for jvxh__xzh in isna_overload_types:
        for overload_name in isna_specific_methods:
            overload_impl = create_isna_specific_method(overload_name)
            overload_method(jvxh__xzh, overload_name, no_unliteral=True,
                inline='always')(overload_impl)


_install_isna_specific_methods()


@overload_attribute(RangeIndexType, 'values')
@overload_attribute(NumericIndexType, 'values')
@overload_attribute(StringIndexType, 'values')
@overload_attribute(BinaryIndexType, 'values')
@overload_attribute(CategoricalIndexType, 'values')
@overload_attribute(PeriodIndexType, 'values')
@overload_attribute(DatetimeIndexType, 'values')
@overload_attribute(TimedeltaIndexType, 'values')
def overload_values(I):
    return lambda I: bodo.utils.conversion.coerce_to_array(I)


@overload(len, no_unliteral=True)
def overload_index_len(I):
    if isinstance(I, (NumericIndexType, StringIndexType, BinaryIndexType,
        PeriodIndexType, IntervalIndexType, CategoricalIndexType,
        DatetimeIndexType, TimedeltaIndexType, HeterogeneousIndexType)):
        return lambda I: len(bodo.hiframes.pd_index_ext.get_index_data(I))


@overload_attribute(DatetimeIndexType, 'shape')
@overload_attribute(NumericIndexType, 'shape')
@overload_attribute(StringIndexType, 'shape')
@overload_attribute(BinaryIndexType, 'shape')
@overload_attribute(PeriodIndexType, 'shape')
@overload_attribute(TimedeltaIndexType, 'shape')
@overload_attribute(IntervalIndexType, 'shape')
@overload_attribute(CategoricalIndexType, 'shape')
def overload_index_shape(s):
    return lambda s: (len(bodo.hiframes.pd_index_ext.get_index_data(s)),)


@overload_attribute(RangeIndexType, 'shape')
def overload_range_index_shape(s):
    return lambda s: (len(s),)


@overload_attribute(NumericIndexType, 'is_monotonic', inline='always')
@overload_attribute(RangeIndexType, 'is_monotonic', inline='always')
@overload_attribute(DatetimeIndexType, 'is_monotonic', inline='always')
@overload_attribute(TimedeltaIndexType, 'is_monotonic', inline='always')
@overload_attribute(NumericIndexType, 'is_monotonic_increasing', inline=
    'always')
@overload_attribute(RangeIndexType, 'is_monotonic_increasing', inline='always')
@overload_attribute(DatetimeIndexType, 'is_monotonic_increasing', inline=
    'always')
@overload_attribute(TimedeltaIndexType, 'is_monotonic_increasing', inline=
    'always')
def overload_index_is_montonic(I):
    if isinstance(I, (NumericIndexType, DatetimeIndexType, TimedeltaIndexType)
        ):

        def impl(I):
            mgs__uxh = bodo.hiframes.pd_index_ext.get_index_data(I)
            return bodo.libs.array_kernels.series_monotonicity(mgs__uxh, 1)
        return impl
    elif isinstance(I, RangeIndexType):

        def impl(I):
            return I._step > 0 or len(I) <= 1
        return impl


@overload_attribute(NumericIndexType, 'is_monotonic_decreasing', inline=
    'always')
@overload_attribute(RangeIndexType, 'is_monotonic_decreasing', inline='always')
@overload_attribute(DatetimeIndexType, 'is_monotonic_decreasing', inline=
    'always')
@overload_attribute(TimedeltaIndexType, 'is_monotonic_decreasing', inline=
    'always')
def overload_index_is_montonic_decreasing(I):
    if isinstance(I, (NumericIndexType, DatetimeIndexType, TimedeltaIndexType)
        ):

        def impl(I):
            mgs__uxh = bodo.hiframes.pd_index_ext.get_index_data(I)
            return bodo.libs.array_kernels.series_monotonicity(mgs__uxh, 2)
        return impl
    elif isinstance(I, RangeIndexType):

        def impl(I):
            return I._step < 0 or len(I) <= 1
        return impl


@overload_method(RangeIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(NumericIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(StringIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(BinaryIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(CategoricalIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(PeriodIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(DatetimeIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(TimedeltaIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
def overload_index_drop_duplicates(I, keep='first'):
    semue__ijsg = dict(keep=keep)
    kikhd__ufek = dict(keep='first')
    check_unsupported_args('Index.drop_duplicates', semue__ijsg,
        kikhd__ufek, package_name='pandas', module_name='Index')
    if isinstance(I, RangeIndexType):
        return lambda I, keep='first': I.copy()
    pti__dai = """def impl(I, keep='first'):
    data = bodo.hiframes.pd_index_ext.get_index_data(I)
    arr = bodo.libs.array_kernels.drop_duplicates_array(data)
    name = bodo.hiframes.pd_index_ext.get_index_name(I)
"""
    if isinstance(I, PeriodIndexType):
        pti__dai += f"""    return bodo.hiframes.pd_index_ext.init_period_index(arr, name, '{I.freq}')
"""
    else:
        pti__dai += (
            '    return bodo.utils.conversion.index_from_array(arr, name)')
    ikpw__fvvvr = {}
    exec(pti__dai, {'bodo': bodo}, ikpw__fvvvr)
    impl = ikpw__fvvvr['impl']
    return impl


@numba.generated_jit(nopython=True)
def get_index_data(S):
    return lambda S: S._data


@numba.generated_jit(nopython=True)
def get_index_name(S):
    return lambda S: S._name


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_index_data',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_datetime_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_timedelta_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_numeric_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_binary_str_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_categorical_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func


def get_index_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    phk__tknt = args[0]
    if isinstance(self.typemap[phk__tknt.name], HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(phk__tknt):
        return ArrayAnalysis.AnalyzeResult(shape=phk__tknt, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_get_index_data
    ) = get_index_data_equiv


@overload_method(RangeIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(NumericIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(StringIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(BinaryIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(CategoricalIndexType, 'map', inline='always', no_unliteral
    =True)
@overload_method(PeriodIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(DatetimeIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(TimedeltaIndexType, 'map', inline='always', no_unliteral=True)
def overload_index_map(I, mapper, na_action=None):
    if not is_const_func_type(mapper):
        raise BodoError("Index.map(): 'mapper' should be a function")
    dtype = I.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = pd_timestamp_type
    if dtype == types.NPTimedelta('ns'):
        dtype = pd_timedelta_type
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):
        dtype = dtype.elem_type
    kwwg__kdab = numba.core.registry.cpu_target.typing_context
    hpby__jaiq = numba.core.registry.cpu_target.target_context
    try:
        ytkvv__ymijt = get_const_func_output_type(mapper, (dtype,), {},
            kwwg__kdab, hpby__jaiq)
    except Exception as iyhv__lzrs:
        raise_bodo_error(get_udf_error_msg('Index.map()', iyhv__lzrs))
    agevg__zirf = get_udf_out_arr_type(ytkvv__ymijt)
    func = get_overload_const_func(mapper, None)
    pti__dai = 'def f(I, mapper, na_action=None):\n'
    pti__dai += '  name = bodo.hiframes.pd_index_ext.get_index_name(I)\n'
    pti__dai += '  A = bodo.utils.conversion.coerce_to_array(I)\n'
    pti__dai += '  numba.parfors.parfor.init_prange()\n'
    pti__dai += '  n = len(A)\n'
    pti__dai += '  S = bodo.utils.utils.alloc_type(n, _arr_typ, (-1,))\n'
    pti__dai += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    pti__dai += '    t2 = bodo.utils.conversion.box_if_dt64(A[i])\n'
    pti__dai += '    v = map_func(t2)\n'
    pti__dai += '    S[i] = bodo.utils.conversion.unbox_if_timestamp(v)\n'
    pti__dai += '  return bodo.utils.conversion.index_from_array(S, name)\n'
    qvj__nisvk = bodo.compiler.udf_jit(func)
    ikpw__fvvvr = {}
    exec(pti__dai, {'numba': numba, 'np': np, 'pd': pd, 'bodo': bodo,
        'map_func': qvj__nisvk, '_arr_typ': agevg__zirf,
        'init_nested_counts': bodo.utils.indexing.init_nested_counts,
        'add_nested_counts': bodo.utils.indexing.add_nested_counts,
        'data_arr_type': agevg__zirf.dtype}, ikpw__fvvvr)
    f = ikpw__fvvvr['f']
    return f


@lower_builtin(operator.is_, NumericIndexType, NumericIndexType)
@lower_builtin(operator.is_, StringIndexType, StringIndexType)
@lower_builtin(operator.is_, BinaryIndexType, BinaryIndexType)
@lower_builtin(operator.is_, PeriodIndexType, PeriodIndexType)
@lower_builtin(operator.is_, DatetimeIndexType, DatetimeIndexType)
@lower_builtin(operator.is_, TimedeltaIndexType, TimedeltaIndexType)
@lower_builtin(operator.is_, IntervalIndexType, IntervalIndexType)
@lower_builtin(operator.is_, CategoricalIndexType, CategoricalIndexType)
def index_is(context, builder, sig, args):
    lzmek__wpfut, nty__kbrw = sig.args
    if lzmek__wpfut != nty__kbrw:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return a._data is b._data and a._name is b._name
    return context.compile_internal(builder, index_is_impl, sig, args)


@lower_builtin(operator.is_, RangeIndexType, RangeIndexType)
def range_index_is(context, builder, sig, args):
    lzmek__wpfut, nty__kbrw = sig.args
    if lzmek__wpfut != nty__kbrw:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._start == b._start and a._stop == b._stop and a._step ==
            b._step and a._name is b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)


def create_binary_op_overload(op):

    def overload_index_binary_op(lhs, rhs):
        if is_index_type(lhs):

            def impl(lhs, rhs):
                mgs__uxh = bodo.utils.conversion.coerce_to_array(lhs)
                aczu__nsj = bodo.utils.conversion.get_array_if_series_or_index(
                    rhs)
                kjku__eek = op(mgs__uxh, aczu__nsj)
                return kjku__eek
            return impl
        if is_index_type(rhs):

            def impl2(lhs, rhs):
                mgs__uxh = bodo.utils.conversion.coerce_to_array(rhs)
                aczu__nsj = bodo.utils.conversion.get_array_if_series_or_index(
                    lhs)
                kjku__eek = op(aczu__nsj, mgs__uxh)
                return kjku__eek
            return impl2
        if isinstance(lhs, HeterogeneousIndexType):
            if not is_heterogeneous_tuple_type(lhs.data):

                def impl3(lhs, rhs):
                    data = bodo.utils.conversion.coerce_to_array(lhs)
                    mgs__uxh = bodo.utils.conversion.coerce_to_array(data)
                    aczu__nsj = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    kjku__eek = op(mgs__uxh, aczu__nsj)
                    return kjku__eek
                return impl3
            count = len(lhs.data.types)
            pti__dai = 'def f(lhs, rhs):\n'
            pti__dai += '  return [{}]\n'.format(','.join(
                'op(lhs[{}], rhs{})'.format(i, f'[{i}]' if is_iterable_type
                (rhs) else '') for i in range(count)))
            ikpw__fvvvr = {}
            exec(pti__dai, {'op': op, 'np': np}, ikpw__fvvvr)
            impl = ikpw__fvvvr['f']
            return impl
        if isinstance(rhs, HeterogeneousIndexType):
            if not is_heterogeneous_tuple_type(rhs.data):

                def impl4(lhs, rhs):
                    data = bodo.hiframes.pd_index_ext.get_index_data(rhs)
                    mgs__uxh = bodo.utils.conversion.coerce_to_array(data)
                    aczu__nsj = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    kjku__eek = op(aczu__nsj, mgs__uxh)
                    return kjku__eek
                return impl4
            count = len(rhs.data.types)
            pti__dai = 'def f(lhs, rhs):\n'
            pti__dai += '  return [{}]\n'.format(','.join(
                'op(lhs{}, rhs[{}])'.format(f'[{i}]' if is_iterable_type(
                lhs) else '', i) for i in range(count)))
            ikpw__fvvvr = {}
            exec(pti__dai, {'op': op, 'np': np}, ikpw__fvvvr)
            impl = ikpw__fvvvr['f']
            return impl
    return overload_index_binary_op


skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        overload_impl = create_binary_op_overload(op)
        overload(op, inline='always')(overload_impl)


_install_binary_ops()


def is_index_type(t):
    return isinstance(t, (RangeIndexType, NumericIndexType, StringIndexType,
        BinaryIndexType, PeriodIndexType, DatetimeIndexType,
        TimedeltaIndexType, IntervalIndexType, CategoricalIndexType))


@lower_cast(RangeIndexType, NumericIndexType)
def cast_range_index_to_int_index(context, builder, fromty, toty, val):
    f = lambda I: init_numeric_index(np.arange(I._start, I._stop, I._step),
        bodo.hiframes.pd_index_ext.get_index_name(I))
    return context.compile_internal(builder, f, toty(fromty), [val])


class HeterogeneousIndexType(types.Type):
    ndim = 1

    def __init__(self, data=None, name_type=None):
        self.data = data
        name_type = types.none if name_type is None else name_type
        self.name_type = name_type
        super(HeterogeneousIndexType, self).__init__(name=
            f'heter_index({data}, {name_type})')

    def copy(self):
        return HeterogeneousIndexType(self.data, self.name_type)

    @property
    def key(self):
        return self.data, self.name_type

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def pandas_type_name(self):
        return 'object'

    @property
    def numpy_type_name(self):
        return 'object'


@register_model(HeterogeneousIndexType)
class HeterogeneousIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        bagk__apz = [('data', fe_type.data), ('name', fe_type.name_type)]
        super(HeterogeneousIndexModel, self).__init__(dmm, fe_type, bagk__apz)


make_attribute_wrapper(HeterogeneousIndexType, 'data', '_data')
make_attribute_wrapper(HeterogeneousIndexType, 'name', '_name')


@overload_method(HeterogeneousIndexType, 'copy', no_unliteral=True)
def overload_heter_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    nmz__jklhr = idx_typ_to_format_str_map[HeterogeneousIndexType].format(
        'copy()')
    imb__fgxdc = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', imb__fgxdc, idx_cpy_arg_defaults,
        fn_str=nmz__jklhr, package_name='pandas', module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_numeric_index(A._data.
                copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_numeric_index(A._data.
                copy(), A._name)
    return impl


@box(HeterogeneousIndexType)
def box_heter_index(typ, val, c):
    msaih__qjh = c.context.insert_const_string(c.builder.module, 'pandas')
    fmg__imf = c.pyapi.import_module_noblock(msaih__qjh)
    fsl__jyzo = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.data, fsl__jyzo.data)
    mzim__zhfm = c.pyapi.from_native_value(typ.data, fsl__jyzo.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_type, fsl__jyzo.name)
    hqslu__vqos = c.pyapi.from_native_value(typ.name_type, fsl__jyzo.name,
        c.env_manager)
    vso__jjvd = c.pyapi.make_none()
    pcuy__czpm = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    zlxty__jdjxu = c.pyapi.call_method(fmg__imf, 'Index', (mzim__zhfm,
        vso__jjvd, pcuy__czpm, hqslu__vqos))
    c.pyapi.decref(mzim__zhfm)
    c.pyapi.decref(vso__jjvd)
    c.pyapi.decref(pcuy__czpm)
    c.pyapi.decref(hqslu__vqos)
    c.pyapi.decref(fmg__imf)
    c.context.nrt.decref(c.builder, typ, val)
    return zlxty__jdjxu


@intrinsic
def init_heter_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        assert len(args) == 2
        vpc__qnkj = signature.return_type
        fsl__jyzo = cgutils.create_struct_proxy(vpc__qnkj)(context, builder)
        fsl__jyzo.data = args[0]
        fsl__jyzo.name = args[1]
        context.nrt.incref(builder, vpc__qnkj.data, args[0])
        context.nrt.incref(builder, vpc__qnkj.name_type, args[1])
        return fsl__jyzo._getvalue()
    return HeterogeneousIndexType(data, name)(data, name), codegen


@overload_attribute(HeterogeneousIndexType, 'name')
def heter_index_get_name(i):

    def impl(i):
        return i._name
    return impl


@overload_attribute(NumericIndexType, 'nbytes')
@overload_attribute(DatetimeIndexType, 'nbytes')
@overload_attribute(TimedeltaIndexType, 'nbytes')
@overload_attribute(RangeIndexType, 'nbytes')
@overload_attribute(StringIndexType, 'nbytes')
@overload_attribute(BinaryIndexType, 'nbytes')
@overload_attribute(CategoricalIndexType, 'nbytes')
@overload_attribute(PeriodIndexType, 'nbytes')
def overload_nbytes(I):
    if isinstance(I, RangeIndexType):

        def _impl_nbytes(I):
            return bodo.io.np_io.get_dtype_size(type(I._start)
                ) + bodo.io.np_io.get_dtype_size(type(I._step)
                ) + bodo.io.np_io.get_dtype_size(type(I._stop))
        return _impl_nbytes
    else:

        def _impl_nbytes(I):
            return I._data.nbytes
        return _impl_nbytes


@overload_method(NumericIndexType, 'rename', inline='always')
@overload_method(DatetimeIndexType, 'rename', inline='always')
@overload_method(TimedeltaIndexType, 'rename', inline='always')
@overload_method(RangeIndexType, 'rename', inline='always')
@overload_method(StringIndexType, 'rename', inline='always')
@overload_method(BinaryIndexType, 'rename', inline='always')
@overload_method(CategoricalIndexType, 'rename', inline='always')
@overload_method(PeriodIndexType, 'rename', inline='always')
@overload_method(IntervalIndexType, 'rename', inline='always')
@overload_method(HeterogeneousIndexType, 'rename', inline='always')
def overload_rename(I, name, inplace=False):
    if is_overload_true(inplace):
        raise BodoError('Index.rename(): inplace index renaming unsupported')
    return init_index(I, name)


def init_index(I, name):
    xbxpm__psm = {NumericIndexType: bodo.hiframes.pd_index_ext.
        init_numeric_index, DatetimeIndexType: bodo.hiframes.pd_index_ext.
        init_datetime_index, TimedeltaIndexType: bodo.hiframes.pd_index_ext
        .init_timedelta_index, StringIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, BinaryIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, CategoricalIndexType: bodo.hiframes.
        pd_index_ext.init_categorical_index, IntervalIndexType: bodo.
        hiframes.pd_index_ext.init_interval_index}
    if type(I) in xbxpm__psm:
        init_func = xbxpm__psm[type(I)]
        return lambda I, name, inplace=False: init_func(I._data.copy(), name)
    if isinstance(I, RangeIndexType):
        return lambda I, name, inplace=False: I.copy(name=name)
    if isinstance(I, PeriodIndexType):
        freq = I.freq
        return (lambda I, name, inplace=False: bodo.hiframes.pd_index_ext.
            init_period_index(I._data.copy(), name, freq))
    if isinstance(I, HeterogeneousIndexType):
        return (lambda I, name, inplace=False: bodo.hiframes.pd_index_ext.
            init_heter_index(bodo.hiframes.pd_index_ext.get_index_data(I),
            name))
    raise TypeError(f'init_index(): Unknown type {type(I)}')


@overload(operator.getitem, no_unliteral=True)
def overload_heter_index_getitem(I, ind):
    if not isinstance(I, HeterogeneousIndexType):
        return
    if isinstance(ind, types.Integer):
        return lambda I, ind: bodo.hiframes.pd_index_ext.get_index_data(I)[ind]
    if isinstance(I, HeterogeneousIndexType):
        return lambda I, ind: bodo.hiframes.pd_index_ext.init_heter_index(bodo
            .hiframes.pd_index_ext.get_index_data(I)[ind], bodo.hiframes.
            pd_index_ext.get_index_name(I))


@lower_constant(DatetimeIndexType)
@lower_constant(TimedeltaIndexType)
def lower_constant_time_index(context, builder, ty, pyval):
    data = context.get_constant_generic(builder, types.Array(types.int64, 1,
        'C'), pyval.values.view(np.int64))
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    dtype = ty.dtype
    ebm__ipez = context.get_constant_null(types.DictType(dtype, types.int64))
    return lir.Constant.literal_struct([data, name, ebm__ipez])


@lower_constant(PeriodIndexType)
def lower_constant_period_index(context, builder, ty, pyval):
    data = context.get_constant_generic(builder, bodo.IntegerArrayType(
        types.int64), pd.arrays.IntegerArray(pyval.asi8, pyval.isna()))
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    ebm__ipez = context.get_constant_null(types.DictType(types.int64, types
        .int64))
    return lir.Constant.literal_struct([data, name, ebm__ipez])


@lower_constant(NumericIndexType)
def lower_constant_numeric_index(context, builder, ty, pyval):
    assert isinstance(ty.dtype, (types.Integer, types.Float, types.Boolean))
    data = context.get_constant_generic(builder, types.Array(ty.dtype, 1,
        'C'), pyval.values)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    dtype = ty.dtype
    ebm__ipez = context.get_constant_null(types.DictType(dtype, types.int64))
    return lir.Constant.literal_struct([data, name, ebm__ipez])


@lower_constant(StringIndexType)
@lower_constant(BinaryIndexType)
def lower_constant_binary_string_index(context, builder, ty, pyval):
    vzwm__dxy = ty.data
    scalar_type = ty.data.dtype
    data = context.get_constant_generic(builder, vzwm__dxy, pyval.values)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    ebm__ipez = context.get_constant_null(types.DictType(scalar_type, types
        .int64))
    return lir.Constant.literal_struct([data, name, ebm__ipez])


@lower_builtin('getiter', RangeIndexType)
def getiter_range_index(context, builder, sig, args):
    [uqdv__pdl] = sig.args
    [ibfg__jcd] = args
    fqyti__wig = context.make_helper(builder, uqdv__pdl, value=ibfg__jcd)
    kcdxb__vwlxr = context.make_helper(builder, sig.return_type)
    rmnx__oshz = cgutils.alloca_once_value(builder, fqyti__wig.start)
    prt__hus = context.get_constant(types.intp, 0)
    zprvy__sfpwn = cgutils.alloca_once_value(builder, prt__hus)
    kcdxb__vwlxr.iter = rmnx__oshz
    kcdxb__vwlxr.stop = fqyti__wig.stop
    kcdxb__vwlxr.step = fqyti__wig.step
    kcdxb__vwlxr.count = zprvy__sfpwn
    diu__epqob = builder.sub(fqyti__wig.stop, fqyti__wig.start)
    wkc__zbfl = context.get_constant(types.intp, 1)
    ghg__wzvc = builder.icmp(lc.ICMP_SGT, diu__epqob, prt__hus)
    oppy__nqkcl = builder.icmp(lc.ICMP_SGT, fqyti__wig.step, prt__hus)
    ttva__gam = builder.not_(builder.xor(ghg__wzvc, oppy__nqkcl))
    with builder.if_then(ttva__gam):
        aci__hizm = builder.srem(diu__epqob, fqyti__wig.step)
        aci__hizm = builder.select(ghg__wzvc, aci__hizm, builder.neg(aci__hizm)
            )
        ers__bljy = builder.icmp(lc.ICMP_SGT, aci__hizm, prt__hus)
        vjtz__pyont = builder.add(builder.sdiv(diu__epqob, fqyti__wig.step),
            builder.select(ers__bljy, wkc__zbfl, prt__hus))
        builder.store(vjtz__pyont, zprvy__sfpwn)
    ovnjl__sfp = kcdxb__vwlxr._getvalue()
    welhb__hhy = impl_ret_new_ref(context, builder, sig.return_type, ovnjl__sfp
        )
    return welhb__hhy


def getiter_index(context, builder, sig, args):
    [uqdv__pdl] = sig.args
    [ibfg__jcd] = args
    fqyti__wig = context.make_helper(builder, uqdv__pdl, value=ibfg__jcd)
    return numba.np.arrayobj.getiter_array(context, builder, signature(sig.
        return_type, sig.args[0].data), (fqyti__wig.data,))


def _install_index_getiter():
    index_types = [NumericIndexType, StringIndexType, BinaryIndexType,
        CategoricalIndexType, TimedeltaIndexType, DatetimeIndexType]
    for typ in index_types:
        lower_builtin('getiter', typ)(getiter_index)


_install_index_getiter()
index_unsupported_methods = ['all', 'any', 'append', 'argmax', 'argmin',
    'argsort', 'asof', 'asof_locs', 'astype', 'delete', 'difference',
    'drop', 'droplevel', 'dropna', 'duplicated', 'equals', 'factorize',
    'fillna', 'format', 'get_indexer', 'get_indexer_for',
    'get_indexer_non_unique', 'get_level_values', 'get_slice_bound',
    'get_value', 'groupby', 'holds_integer', 'identical', 'insert',
    'intersection', 'is_', 'is_boolean', 'is_categorical', 'is_floating',
    'is_integer', 'is_interval', 'is_mixed', 'is_numeric', 'is_object',
    'is_type_compatible', 'isin', 'item', 'join', 'memory_usage', 'nunique',
    'putmask', 'ravel', 'reindex', 'repeat', 'searchsorted', 'set_names',
    'set_value', 'shift', 'slice_indexer', 'slice_locs', 'sort',
    'sort_values', 'sortlevel', 'str', 'symmetric_difference',
    'to_flat_index', 'to_frame', 'to_list', 'to_native_types', 'to_numpy',
    'to_series', 'tolist', 'transpose', 'union', 'unique', 'value_counts',
    'view', 'where']
index_unsupported_atrs = ['T', 'array', 'asi8', 'dtype', 'has_duplicates',
    'hasnans', 'inferred_type', 'is_all_dates', 'is_unique', 'ndim',
    'nlevels', 'size', 'names', 'empty']
cat_idx_unsupported_atrs = ['codes', 'categories', 'ordered',
    'is_monotonic', 'is_monotonic_increasing', 'is_monotonic_decreasing']
cat_idx_unsupported_methods = ['rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered', 'get_loc']
interval_idx_unsupported_atrs = ['closed', 'is_empty',
    'is_non_overlapping_monotonic', 'is_overlapping', 'left', 'right',
    'mid', 'length', 'values', 'shape', 'nbytes', 'is_monotonic',
    'is_monotonic_increasing', 'is_monotonic_decreasing']
interval_idx_unsupported_methods = ['contains', 'copy', 'overlaps',
    'set_closed', 'to_tuples', 'take', 'get_loc', 'isna', 'isnull', 'map']
multi_index_unsupported_atrs = ['levshape', 'levels', 'codes', 'dtypes',
    'values', 'shape', 'nbytes', 'is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing']
multi_index_unsupported_methods = ['copy', 'set_levels', 'set_codes',
    'swaplevel', 'reorder_levels', 'remove_unused_levels', 'get_loc',
    'get_locs', 'get_loc_level', 'take', 'isna', 'isnull', 'map']
dt_index_unsupported_atrs = ['time', 'timez', 'tz', 'freq', 'freqstr',
    'inferred_freq']
dt_index_unsupported_methods = ['normalize', 'strftime', 'snap',
    'tz_convert', 'tz_localize', 'round', 'floor', 'ceil', 'to_period',
    'to_perioddelta', 'to_pydatetime', 'month_name', 'day_name', 'mean',
    'indexer_at_time', 'indexer_between', 'indexer_between_time']
td_index_unsupported_atrs = ['components', 'inferred_freq']
td_index_unsupported_methods = ['to_pydatetime', 'round', 'floor', 'ceil',
    'mean']
period_index_unsupported_atrs = ['day', 'dayofweek', 'day_of_week',
    'dayofyear', 'day_of_year', 'days_in_month', 'daysinmonth', 'freq',
    'freqstr', 'hour', 'is_leap_year', 'minute', 'month', 'quarter',
    'second', 'week', 'weekday', 'weekofyear', 'year', 'end_time', 'qyear',
    'start_time', 'is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing']
string_index_unsupported_atrs = ['is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing']
binary_index_unsupported_atrs = ['is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing']
period_index_unsupported_methods = ['asfreq', 'strftime', 'to_timestamp']
index_types = [('pandas.RangeIndex.{}', RangeIndexType), (
    'pandas.Index.{} with numeric data', NumericIndexType), (
    'pandas.Index.{} with string data', StringIndexType), (
    'pandas.Index.{} with binary data', BinaryIndexType), (
    'pandas.TimedeltaIndex.{}', TimedeltaIndexType), (
    'pandas.IntervalIndex.{}', IntervalIndexType), (
    'pandas.CategoricalIndex.{}', CategoricalIndexType), (
    'pandas.PeriodIndex.{}', PeriodIndexType), ('pandas.DatetimeIndex.{}',
    DatetimeIndexType), ('pandas.MultiIndex.{}', MultiIndexType)]
for name, typ in index_types:
    idx_typ_to_format_str_map[typ] = name


def _install_index_unsupported():
    for yfzr__jum in index_unsupported_methods:
        for syrkk__kcii, typ in index_types:
            overload_method(typ, yfzr__jum, no_unliteral=True)(
                create_unsupported_overload(syrkk__kcii.format(yfzr__jum +
                '()')))
    for fkkk__orf in index_unsupported_atrs:
        for syrkk__kcii, typ in index_types:
            overload_attribute(typ, fkkk__orf, no_unliteral=True)(
                create_unsupported_overload(syrkk__kcii.format(fkkk__orf)))
    ays__hcr = [(StringIndexType, string_index_unsupported_atrs), (
        BinaryIndexType, binary_index_unsupported_atrs), (
        CategoricalIndexType, cat_idx_unsupported_atrs), (IntervalIndexType,
        interval_idx_unsupported_atrs), (MultiIndexType,
        multi_index_unsupported_atrs), (DatetimeIndexType,
        dt_index_unsupported_atrs), (TimedeltaIndexType,
        td_index_unsupported_atrs), (PeriodIndexType,
        period_index_unsupported_atrs)]
    xeqx__ybpfr = [(CategoricalIndexType, cat_idx_unsupported_methods), (
        IntervalIndexType, interval_idx_unsupported_methods), (
        MultiIndexType, multi_index_unsupported_methods), (
        DatetimeIndexType, dt_index_unsupported_methods), (
        TimedeltaIndexType, td_index_unsupported_methods), (PeriodIndexType,
        period_index_unsupported_methods)]
    for typ, dxz__uru in xeqx__ybpfr:
        syrkk__kcii = idx_typ_to_format_str_map[typ]
        for inavz__vihk in dxz__uru:
            overload_method(typ, inavz__vihk, no_unliteral=True)(
                create_unsupported_overload(syrkk__kcii.format(inavz__vihk +
                '()')))
    for typ, sghfm__skf in ays__hcr:
        syrkk__kcii = idx_typ_to_format_str_map[typ]
        for fkkk__orf in sghfm__skf:
            overload_attribute(typ, fkkk__orf, no_unliteral=True)(
                create_unsupported_overload(syrkk__kcii.format(fkkk__orf)))
    for gzenv__qqqv in [RangeIndexType, NumericIndexType, StringIndexType,
        BinaryIndexType, IntervalIndexType, CategoricalIndexType,
        PeriodIndexType, MultiIndexType]:
        for inavz__vihk in ['max', 'min']:
            syrkk__kcii = idx_typ_to_format_str_map[gzenv__qqqv]
            overload_method(gzenv__qqqv, inavz__vihk, no_unliteral=True)(
                create_unsupported_overload(syrkk__kcii.format(inavz__vihk +
                '()')))


_install_index_unsupported()
