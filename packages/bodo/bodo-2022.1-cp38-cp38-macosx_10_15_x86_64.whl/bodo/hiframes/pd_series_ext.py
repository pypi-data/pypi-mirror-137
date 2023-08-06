"""
Implement pd.Series typing and data model handling.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import bound_function, signature
from numba.extending import infer_getattr, intrinsic, lower_builtin, lower_cast, models, overload, overload_attribute, overload_method, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.datetime_timedelta_ext import pd_timedelta_type
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_type
from bodo.io import csv_cpp
from bodo.libs.int_arr_ext import IntDtype
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.transform import get_const_func_output_type
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, dtype_to_array_type, get_overload_const_str, get_overload_const_tuple, get_udf_error_msg, get_udf_out_arr_type, is_heterogeneous_tuple_type, is_overload_constant_str, is_overload_constant_tuple, is_overload_false, is_overload_int, is_overload_none, raise_bodo_error
_csv_output_is_dir = types.ExternalFunction('csv_output_is_dir', types.int8
    (types.voidptr))
ll.add_symbol('csv_output_is_dir', csv_cpp.csv_output_is_dir)


class SeriesType(types.IterableType, types.ArrayCompatible):
    ndim = 1

    def __init__(self, dtype, data=None, index=None, name_typ=None, dist=None):
        from bodo.hiframes.pd_index_ext import RangeIndexType
        from bodo.transforms.distributed_analysis import Distribution
        data = dtype_to_array_type(dtype) if data is None else data
        dtype = dtype.dtype if isinstance(dtype, IntDtype) else dtype
        self.dtype = dtype
        self.data = data
        name_typ = types.none if name_typ is None else name_typ
        index = RangeIndexType(types.none) if index is None else index
        self.index = index
        self.name_typ = name_typ
        dist = Distribution.OneD_Var if dist is None else dist
        self.dist = dist
        super(SeriesType, self).__init__(name=
            f'series({dtype}, {data}, {index}, {name_typ}, {dist})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self, dtype=None, index=None, dist=None):
        if index is None:
            index = self.index
        if dist is None:
            dist = self.dist
        if dtype is None:
            dtype = self.dtype
            data = self.data
        else:
            data = dtype_to_array_type(dtype)
        return SeriesType(dtype, data, index, self.name_typ, dist)

    @property
    def key(self):
        return self.dtype, self.data, self.index, self.name_typ, self.dist

    def unify(self, typingctx, other):
        from bodo.transforms.distributed_analysis import Distribution
        if isinstance(other, SeriesType):
            bqjin__mpmgw = (self.index if self.index == other.index else
                self.index.unify(typingctx, other.index))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if other.dtype == self.dtype or not other.dtype.is_precise():
                return SeriesType(self.dtype, self.data.unify(typingctx,
                    other.data), bqjin__mpmgw, dist=dist)
        return super(SeriesType, self).unify(typingctx, other)

    def can_convert_to(self, typingctx, other):
        from numba.core.typeconv import Conversion
        if (isinstance(other, SeriesType) and self.dtype == other.dtype and
            self.data == other.data and self.index == other.index and self.
            name_typ == other.name_typ and self.dist != other.dist):
            return Conversion.safe

    def is_precise(self):
        return self.dtype.is_precise()

    @property
    def iterator_type(self):
        return self.data.iterator_type

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class HeterogeneousSeriesType(types.Type):
    ndim = 1

    def __init__(self, data=None, index=None, name_typ=None):
        from bodo.hiframes.pd_index_ext import RangeIndexType
        from bodo.transforms.distributed_analysis import Distribution
        self.data = data
        name_typ = types.none if name_typ is None else name_typ
        index = RangeIndexType(types.none) if index is None else index
        self.index = index
        self.name_typ = name_typ
        self.dist = Distribution.REP
        super(HeterogeneousSeriesType, self).__init__(name=
            f'heter_series({data}, {index}, {name_typ})')

    def copy(self, index=None, dist=None):
        from bodo.transforms.distributed_analysis import Distribution
        assert dist == Distribution.REP, 'invalid distribution for HeterogeneousSeriesType'
        if index is None:
            index = self.index.copy()
        return HeterogeneousSeriesType(self.data, index, self.name_typ)

    @property
    def key(self):
        return self.data, self.index, self.name_typ

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@lower_builtin('getiter', SeriesType)
def series_getiter(context, builder, sig, args):
    gviq__rdt = get_series_payload(context, builder, sig.args[0], args[0])
    impl = context.get_function('getiter', sig.return_type(sig.args[0].data))
    return impl(builder, (gviq__rdt.data,))


@infer_getattr
class HeterSeriesAttribute(OverloadedKeyAttributeTemplate):
    key = HeterogeneousSeriesType

    def generic_resolve(self, S, attr):
        from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
        if self._is_existing_attr(attr):
            return
        if isinstance(S.index, HeterogeneousIndexType
            ) and is_overload_constant_tuple(S.index.data):
            sag__npbxx = get_overload_const_tuple(S.index.data)
            if attr in sag__npbxx:
                iwm__kzfn = sag__npbxx.index(attr)
                return S.data[iwm__kzfn]


def is_str_series_typ(t):
    return isinstance(t, SeriesType) and t.dtype == string_type


def is_dt64_series_typ(t):
    return isinstance(t, SeriesType) and t.dtype == types.NPDatetime('ns')


def is_timedelta64_series_typ(t):
    return isinstance(t, SeriesType) and t.dtype == types.NPTimedelta('ns')


def is_datetime_date_series_typ(t):
    return isinstance(t, SeriesType) and t.dtype == datetime_date_type


class SeriesPayloadType(types.Type):

    def __init__(self, series_type):
        self.series_type = series_type
        super(SeriesPayloadType, self).__init__(name=
            f'SeriesPayloadType({series_type})')

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SeriesPayloadType)
class SeriesPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ahg__nbqlc = [('data', fe_type.series_type.data), ('index', fe_type
            .series_type.index), ('name', fe_type.series_type.name_typ)]
        super(SeriesPayloadModel, self).__init__(dmm, fe_type, ahg__nbqlc)


@register_model(HeterogeneousSeriesType)
@register_model(SeriesType)
class SeriesModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = SeriesPayloadType(fe_type)
        ahg__nbqlc = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(SeriesModel, self).__init__(dmm, fe_type, ahg__nbqlc)


def define_series_dtor(context, builder, series_type, payload_type):
    cza__jol = builder.module
    ves__jzac = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    ajlk__wcdi = cgutils.get_or_insert_function(cza__jol, ves__jzac, name=
        '.dtor.series.{}'.format(series_type))
    if not ajlk__wcdi.is_declaration:
        return ajlk__wcdi
    ajlk__wcdi.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(ajlk__wcdi.append_basic_block())
    bme__zqp = ajlk__wcdi.args[0]
    xsiog__bgyu = context.get_value_type(payload_type).as_pointer()
    mpmb__xyndp = builder.bitcast(bme__zqp, xsiog__bgyu)
    secq__hbh = context.make_helper(builder, payload_type, ref=mpmb__xyndp)
    context.nrt.decref(builder, series_type.data, secq__hbh.data)
    context.nrt.decref(builder, series_type.index, secq__hbh.index)
    context.nrt.decref(builder, series_type.name_typ, secq__hbh.name)
    builder.ret_void()
    return ajlk__wcdi


def construct_series(context, builder, series_type, data_val, index_val,
    name_val):
    payload_type = SeriesPayloadType(series_type)
    gviq__rdt = cgutils.create_struct_proxy(payload_type)(context, builder)
    gviq__rdt.data = data_val
    gviq__rdt.index = index_val
    gviq__rdt.name = name_val
    cfvtt__bpf = context.get_value_type(payload_type)
    stnq__zwic = context.get_abi_sizeof(cfvtt__bpf)
    zbsc__utcgm = define_series_dtor(context, builder, series_type,
        payload_type)
    srsyl__rbxtw = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, stnq__zwic), zbsc__utcgm)
    whki__kfhyg = context.nrt.meminfo_data(builder, srsyl__rbxtw)
    yvnoh__rhzd = builder.bitcast(whki__kfhyg, cfvtt__bpf.as_pointer())
    builder.store(gviq__rdt._getvalue(), yvnoh__rhzd)
    series = cgutils.create_struct_proxy(series_type)(context, builder)
    series.meminfo = srsyl__rbxtw
    series.parent = cgutils.get_null_value(series.parent.type)
    return series._getvalue()


@intrinsic
def init_series(typingctx, data, index, name=None):
    from bodo.hiframes.pd_index_ext import is_pd_index_type
    from bodo.hiframes.pd_multi_index_ext import MultiIndexType
    assert is_pd_index_type(index) or isinstance(index, MultiIndexType)
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        data_val, index_val, name_val = args
        series_type = signature.return_type
        kanu__ysmh = construct_series(context, builder, series_type,
            data_val, index_val, name_val)
        context.nrt.incref(builder, signature.args[0], data_val)
        context.nrt.incref(builder, signature.args[1], index_val)
        context.nrt.incref(builder, signature.args[2], name_val)
        return kanu__ysmh
    if is_heterogeneous_tuple_type(data):
        budo__tlen = HeterogeneousSeriesType(data, index, name)
    else:
        dtype = data.dtype
        data = if_series_to_array_type(data)
        budo__tlen = SeriesType(dtype, data, index, name)
    sig = signature(budo__tlen, data, index, name)
    return sig, codegen


def init_series_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) >= 2 and not kws
    data = args[0]
    index = args[1]
    wbjxj__vnn = self.typemap[data.name]
    if is_heterogeneous_tuple_type(wbjxj__vnn) or isinstance(wbjxj__vnn,
        types.BaseTuple):
        return None
    shp__wun = self.typemap[index.name]
    if not isinstance(shp__wun, HeterogeneousIndexType
        ) and equiv_set.has_shape(data) and equiv_set.has_shape(index):
        equiv_set.insert_equiv(data, index)
    if equiv_set.has_shape(data):
        return ArrayAnalysis.AnalyzeResult(shape=data, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_series_ext_init_series = (
    init_series_equiv)


def get_series_payload(context, builder, series_type, value):
    srsyl__rbxtw = cgutils.create_struct_proxy(series_type)(context,
        builder, value).meminfo
    payload_type = SeriesPayloadType(series_type)
    secq__hbh = context.nrt.meminfo_data(builder, srsyl__rbxtw)
    xsiog__bgyu = context.get_value_type(payload_type).as_pointer()
    secq__hbh = builder.bitcast(secq__hbh, xsiog__bgyu)
    return context.make_helper(builder, payload_type, ref=secq__hbh)


@intrinsic
def get_series_data(typingctx, series_typ=None):

    def codegen(context, builder, signature, args):
        gviq__rdt = get_series_payload(context, builder, signature.args[0],
            args[0])
        return impl_ret_borrowed(context, builder, series_typ.data,
            gviq__rdt.data)
    budo__tlen = series_typ.data
    sig = signature(budo__tlen, series_typ)
    return sig, codegen


@intrinsic
def get_series_index(typingctx, series_typ=None):

    def codegen(context, builder, signature, args):
        gviq__rdt = get_series_payload(context, builder, signature.args[0],
            args[0])
        return impl_ret_borrowed(context, builder, series_typ.index,
            gviq__rdt.index)
    budo__tlen = series_typ.index
    sig = signature(budo__tlen, series_typ)
    return sig, codegen


@intrinsic
def get_series_name(typingctx, series_typ=None):

    def codegen(context, builder, signature, args):
        gviq__rdt = get_series_payload(context, builder, signature.args[0],
            args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            gviq__rdt.name)
    sig = signature(series_typ.name_typ, series_typ)
    return sig, codegen


def get_series_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    ckg__nrmf = args[0]
    wbjxj__vnn = self.typemap[ckg__nrmf.name].data
    if is_heterogeneous_tuple_type(wbjxj__vnn) or isinstance(wbjxj__vnn,
        types.BaseTuple):
        return None
    if equiv_set.has_shape(ckg__nrmf):
        return ArrayAnalysis.AnalyzeResult(shape=ckg__nrmf, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_series_ext_get_series_data
    ) = get_series_data_equiv


def get_series_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    ckg__nrmf = args[0]
    shp__wun = self.typemap[ckg__nrmf.name].index
    if isinstance(shp__wun, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(ckg__nrmf):
        return ArrayAnalysis.AnalyzeResult(shape=ckg__nrmf, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_series_ext_get_series_index
    ) = get_series_index_equiv


def alias_ext_init_series(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    if len(args) > 1:
        numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
            arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_series',
    'bodo.hiframes.pd_series_ext'] = alias_ext_init_series


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_series_data',
    'bodo.hiframes.pd_series_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_series_index',
    'bodo.hiframes.pd_series_ext'] = alias_ext_dummy_func


def is_series_type(typ):
    return isinstance(typ, SeriesType)


def if_series_to_array_type(typ):
    if isinstance(typ, SeriesType):
        return typ.data
    return typ


@lower_cast(SeriesType, SeriesType)
def cast_series(context, builder, fromty, toty, val):
    if fromty.copy(index=toty.index) == toty and isinstance(fromty.index,
        bodo.hiframes.pd_index_ext.RangeIndexType) and isinstance(toty.
        index, bodo.hiframes.pd_index_ext.NumericIndexType):
        gviq__rdt = get_series_payload(context, builder, fromty, val)
        bqjin__mpmgw = context.cast(builder, gviq__rdt.index, fromty.index,
            toty.index)
        context.nrt.incref(builder, fromty.data, gviq__rdt.data)
        context.nrt.incref(builder, fromty.name_typ, gviq__rdt.name)
        return construct_series(context, builder, toty, gviq__rdt.data,
            bqjin__mpmgw, gviq__rdt.name)
    if (fromty.dtype == toty.dtype and fromty.data == toty.data and fromty.
        index == toty.index and fromty.name_typ == toty.name_typ and fromty
        .dist != toty.dist):
        return val
    return val


@infer_getattr
class SeriesAttribute(OverloadedKeyAttributeTemplate):
    key = SeriesType

    @bound_function('series.head')
    def resolve_head(self, ary, args, kws):
        lufyb__bbmuo = 'Series.head'
        eawww__byxk = 'n',
        yktj__mur = {'n': 5}
        pysig, nxvie__wut = bodo.utils.typing.fold_typing_args(lufyb__bbmuo,
            args, kws, eawww__byxk, yktj__mur)
        rmjt__ixfdh = nxvie__wut[0]
        if not is_overload_int(rmjt__ixfdh):
            raise BodoError(f"{lufyb__bbmuo}(): 'n' must be an Integer")
        ynrur__lhh = ary
        return ynrur__lhh(*nxvie__wut).replace(pysig=pysig)

    def _resolve_map_func(self, ary, func, pysig, fname, f_args=None, kws=None
        ):
        dtype = ary.dtype
        if dtype == types.NPDatetime('ns'):
            dtype = pd_timestamp_type
        if dtype == types.NPTimedelta('ns'):
            dtype = pd_timedelta_type
        ftqir__ucrgy = dtype,
        if f_args is not None:
            ftqir__ucrgy += tuple(f_args.types)
        if kws is None:
            kws = {}
        dra__ljgj = False
        urqoh__nsyf = True
        if fname == 'map' and isinstance(func, types.DictType):
            dnzn__moww = func.value_type
            dra__ljgj = True
        else:
            try:
                if types.unliteral(func) == types.unicode_type:
                    if not is_overload_constant_str(func):
                        raise BodoError(
                            f'Series.apply(): string argument (for builtins) must be a compile time constant'
                            )
                    dnzn__moww = bodo.utils.transform.get_udf_str_return_type(
                        ary, get_overload_const_str(func), self.context,
                        'Series.apply')
                    urqoh__nsyf = False
                elif bodo.utils.typing.is_numpy_ufunc(func):
                    dnzn__moww = func.get_call_type(self.context, (ary,), {}
                        ).return_type
                    urqoh__nsyf = False
                else:
                    dnzn__moww = get_const_func_output_type(func,
                        ftqir__ucrgy, kws, self.context, numba.core.
                        registry.cpu_target.target_context)
            except Exception as ynmif__bovjc:
                raise BodoError(get_udf_error_msg(f'Series.{fname}()',
                    ynmif__bovjc))
        if urqoh__nsyf:
            if isinstance(dnzn__moww, (SeriesType, HeterogeneousSeriesType)
                ) and dnzn__moww.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(dnzn__moww, HeterogeneousSeriesType):
                mzx__jpadg, xdppe__spdce = dnzn__moww.const_info
                ixmdc__rum = tuple(dtype_to_array_type(t) for t in
                    dnzn__moww.data.types)
                kkxl__yfu = bodo.DataFrameType(ixmdc__rum, ary.index,
                    xdppe__spdce)
            elif isinstance(dnzn__moww, SeriesType):
                ntam__xaadm, xdppe__spdce = dnzn__moww.const_info
                ixmdc__rum = tuple(dtype_to_array_type(dnzn__moww.dtype) for
                    mzx__jpadg in range(ntam__xaadm))
                kkxl__yfu = bodo.DataFrameType(ixmdc__rum, ary.index,
                    xdppe__spdce)
            else:
                fvssj__putf = get_udf_out_arr_type(dnzn__moww, dra__ljgj)
                kkxl__yfu = SeriesType(fvssj__putf.dtype, fvssj__putf, ary.
                    index, ary.name_typ)
        else:
            kkxl__yfu = dnzn__moww
        return signature(kkxl__yfu, (func,)).replace(pysig=pysig)

    @bound_function('series.map', no_unliteral=True)
    def resolve_map(self, ary, args, kws):
        kws = dict(kws)
        func = args[0] if len(args) > 0 else kws['arg']
        kws.pop('arg', None)
        na_action = args[1] if len(args) > 1 else kws.pop('na_action',
            types.none)
        kte__vqrpe = dict(na_action=na_action)
        rlgt__ymxp = dict(na_action=None)
        check_unsupported_args('Series.map', kte__vqrpe, rlgt__ymxp,
            package_name='pandas', module_name='Series')

        def map_stub(arg, na_action=None):
            pass
        pysig = numba.core.utils.pysignature(map_stub)
        return self._resolve_map_func(ary, func, pysig, 'map')

    @bound_function('series.apply', no_unliteral=True)
    def resolve_apply(self, ary, args, kws):
        kws = dict(kws)
        func = args[0] if len(args) > 0 else kws['func']
        kws.pop('func', None)
        hej__swl = args[1] if len(args) > 1 else kws.pop('convert_dtype',
            types.literal(True))
        f_args = args[2] if len(args) > 2 else kws.pop('args', None)
        kte__vqrpe = dict(convert_dtype=hej__swl)
        pjfg__nohts = dict(convert_dtype=True)
        check_unsupported_args('Series.apply', kte__vqrpe, pjfg__nohts,
            package_name='pandas', module_name='Series')
        hwrp__mnegc = ', '.join("{} = ''".format(juus__tpjo) for juus__tpjo in
            kws.keys())
        pihaw__yqkgq = (
            f'def apply_stub(func, convert_dtype=True, args=(), {hwrp__mnegc}):\n'
            )
        pihaw__yqkgq += '    pass\n'
        rim__fhvof = {}
        exec(pihaw__yqkgq, {}, rim__fhvof)
        hvuq__jmhil = rim__fhvof['apply_stub']
        pysig = numba.core.utils.pysignature(hvuq__jmhil)
        return self._resolve_map_func(ary, func, pysig, 'apply', f_args, kws)

    def _resolve_combine_func(self, ary, args, kws):
        kwargs = dict(kws)
        other = args[0] if len(args) > 0 else types.unliteral(kwargs['other'])
        func = args[1] if len(args) > 1 else kwargs['func']
        fill_value = args[2] if len(args) > 2 else types.unliteral(kwargs.
            get('fill_value', types.none))

        def combine_stub(other, func, fill_value=None):
            pass
        pysig = numba.core.utils.pysignature(combine_stub)
        doclc__zjbg = ary.dtype
        if doclc__zjbg == types.NPDatetime('ns'):
            doclc__zjbg = pd_timestamp_type
        crj__llfm = other.dtype
        if crj__llfm == types.NPDatetime('ns'):
            crj__llfm = pd_timestamp_type
        dnzn__moww = get_const_func_output_type(func, (doclc__zjbg,
            crj__llfm), {}, self.context, numba.core.registry.cpu_target.
            target_context)
        sig = signature(SeriesType(dnzn__moww, index=ary.index, name_typ=
            types.none), (other, func, fill_value))
        return sig.replace(pysig=pysig)

    @bound_function('series.combine', no_unliteral=True)
    def resolve_combine(self, ary, args, kws):
        return self._resolve_combine_func(ary, args, kws)

    @bound_function('series.pipe', no_unliteral=True)
    def resolve_pipe(self, ary, args, kws):
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, ary,
            args, kws, 'Series')

    def generic_resolve(self, S, attr):
        from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
        if self._is_existing_attr(attr):
            return
        if isinstance(S.index, HeterogeneousIndexType
            ) and is_overload_constant_tuple(S.index.data):
            sag__npbxx = get_overload_const_tuple(S.index.data)
            if attr in sag__npbxx:
                iwm__kzfn = sag__npbxx.index(attr)
                return S.data[iwm__kzfn]


series_binary_ops = tuple(op for op in numba.core.typing.npydecl.
    NumpyRulesArrayOperator._op_map.keys() if op not in (operator.lshift,
    operator.rshift))
series_inplace_binary_ops = tuple(op for op in numba.core.typing.npydecl.
    NumpyRulesInplaceArrayOperator._op_map.keys() if op not in (operator.
    ilshift, operator.irshift, operator.itruediv))
inplace_binop_to_imm = {operator.iadd: operator.add, operator.isub:
    operator.sub, operator.imul: operator.mul, operator.ifloordiv: operator
    .floordiv, operator.imod: operator.mod, operator.ipow: operator.pow,
    operator.iand: operator.and_, operator.ior: operator.or_, operator.ixor:
    operator.xor}
series_unary_ops = operator.neg, operator.invert, operator.pos
str2str_methods = ('capitalize', 'lower', 'lstrip', 'rstrip', 'strip',
    'swapcase', 'title', 'upper')
str2bool_methods = ('isalnum', 'isalpha', 'isdigit', 'isspace', 'islower',
    'isupper', 'istitle', 'isnumeric', 'isdecimal')


@overload(pd.Series, no_unliteral=True)
def pd_series_overload(data=None, index=None, dtype=None, name=None, copy=
    False, fastpath=False):
    if not is_overload_false(fastpath):
        raise BodoError("pd.Series(): 'fastpath' argument not supported.")
    mjsvo__ldj = is_overload_none(data)
    eqqbw__nqu = is_overload_none(index)
    hbyay__bcfou = is_overload_none(dtype)
    if mjsvo__ldj and eqqbw__nqu and hbyay__bcfou:
        raise BodoError(
            'pd.Series() requires at least 1 of data, index, and dtype to not be none'
            )
    if is_series_type(data) and not eqqbw__nqu:
        raise BodoError(
            'pd.Series() does not support index value when input data is a Series'
            )
    if isinstance(data, types.DictType):
        raise_bodo_error(
            'pd.Series(): When intializing series with a dictionary, it is required that the dict has constant keys'
            )
    if is_heterogeneous_tuple_type(data) and is_overload_none(dtype):

        def impl_heter(data=None, index=None, dtype=None, name=None, copy=
            False, fastpath=False):
            lbfuc__edf = bodo.utils.conversion.extract_index_if_none(data,
                index)
            tedw__ciuqf = bodo.utils.conversion.to_tuple(data)
            return bodo.hiframes.pd_series_ext.init_series(tedw__ciuqf,
                bodo.utils.conversion.convert_to_index(lbfuc__edf), name)
        return impl_heter
    if mjsvo__ldj:
        if hbyay__bcfou:

            def impl(data=None, index=None, dtype=None, name=None, copy=
                False, fastpath=False):
                imet__cish = bodo.utils.conversion.extract_name_if_none(data,
                    name)
                lbfuc__edf = bodo.utils.conversion.extract_index_if_none(data,
                    index)
                numba.parfors.parfor.init_prange()
                tlba__vyn = len(lbfuc__edf)
                tedw__ciuqf = np.empty(tlba__vyn, np.float64)
                for xfo__mcwaj in numba.parfors.parfor.internal_prange(
                    tlba__vyn):
                    bodo.libs.array_kernels.setna(tedw__ciuqf, xfo__mcwaj)
                return bodo.hiframes.pd_series_ext.init_series(tedw__ciuqf,
                    bodo.utils.conversion.convert_to_index(lbfuc__edf),
                    imet__cish)
            return impl
        if bodo.utils.conversion._is_str_dtype(dtype):
            intf__dijqt = bodo.string_array_type
        else:
            miuwj__dzprg = bodo.utils.typing.parse_dtype(dtype, 'pandas.Series'
                )
            if isinstance(miuwj__dzprg, bodo.libs.int_arr_ext.IntDtype):
                intf__dijqt = bodo.IntegerArrayType(miuwj__dzprg.dtype)
            elif miuwj__dzprg == bodo.libs.bool_arr_ext.boolean_dtype:
                intf__dijqt = bodo.boolean_array
            elif isinstance(miuwj__dzprg, types.Number) or miuwj__dzprg in [
                bodo.datetime64ns, bodo.timedelta64ns]:
                intf__dijqt = types.Array(miuwj__dzprg, 1, 'C')
            else:
                raise BodoError(
                    'pd.Series with dtype: {dtype} not currently supported')
        if eqqbw__nqu:

            def impl(data=None, index=None, dtype=None, name=None, copy=
                False, fastpath=False):
                imet__cish = bodo.utils.conversion.extract_name_if_none(data,
                    name)
                lbfuc__edf = bodo.hiframes.pd_index_ext.init_range_index(0,
                    0, 1, None)
                numba.parfors.parfor.init_prange()
                tlba__vyn = len(lbfuc__edf)
                tedw__ciuqf = bodo.utils.utils.alloc_type(tlba__vyn,
                    intf__dijqt, (-1,))
                return bodo.hiframes.pd_series_ext.init_series(tedw__ciuqf,
                    lbfuc__edf, imet__cish)
            return impl
        else:

            def impl(data=None, index=None, dtype=None, name=None, copy=
                False, fastpath=False):
                imet__cish = bodo.utils.conversion.extract_name_if_none(data,
                    name)
                lbfuc__edf = bodo.utils.conversion.extract_index_if_none(data,
                    index)
                numba.parfors.parfor.init_prange()
                tlba__vyn = len(lbfuc__edf)
                tedw__ciuqf = bodo.utils.utils.alloc_type(tlba__vyn,
                    intf__dijqt, (-1,))
                for xfo__mcwaj in numba.parfors.parfor.internal_prange(
                    tlba__vyn):
                    bodo.libs.array_kernels.setna(tedw__ciuqf, xfo__mcwaj)
                return bodo.hiframes.pd_series_ext.init_series(tedw__ciuqf,
                    bodo.utils.conversion.convert_to_index(lbfuc__edf),
                    imet__cish)
            return impl

    def impl(data=None, index=None, dtype=None, name=None, copy=False,
        fastpath=False):
        imet__cish = bodo.utils.conversion.extract_name_if_none(data, name)
        lbfuc__edf = bodo.utils.conversion.extract_index_if_none(data, index)
        ffc__pph = bodo.utils.conversion.coerce_to_array(data, True,
            scalar_to_arr_len=len(lbfuc__edf))
        qcw__svio = bodo.utils.conversion.fix_arr_dtype(ffc__pph, dtype,
            None, False)
        return bodo.hiframes.pd_series_ext.init_series(qcw__svio, bodo.
            utils.conversion.convert_to_index(lbfuc__edf), imet__cish)
    return impl


@overload_method(SeriesType, 'to_csv', no_unliteral=True)
def to_csv_overload(series, path_or_buf=None, sep=',', na_rep='',
    float_format=None, columns=None, header=True, index=True, index_label=
    None, mode='w', encoding=None, compression='infer', quoting=None,
    quotechar='"', line_terminator=None, chunksize=None, date_format=None,
    doublequote=True, escapechar=None, decimal='.', errors='strict',
    _is_parallel=False):
    if not (is_overload_none(path_or_buf) or is_overload_constant_str(
        path_or_buf) or path_or_buf == string_type):
        raise BodoError(
            "Series.to_csv(): 'path_or_buf' argument should be None or string")
    if is_overload_none(path_or_buf):

        def _impl(series, path_or_buf=None, sep=',', na_rep='',
            float_format=None, columns=None, header=True, index=True,
            index_label=None, mode='w', encoding=None, compression='infer',
            quoting=None, quotechar='"', line_terminator=None, chunksize=
            None, date_format=None, doublequote=True, escapechar=None,
            decimal='.', errors='strict', _is_parallel=False):
            with numba.objmode(D='unicode_type'):
                D = series.to_csv(None, sep, na_rep, float_format, columns,
                    header, index, index_label, mode, encoding, compression,
                    quoting, quotechar, line_terminator, chunksize,
                    date_format, doublequote, escapechar, decimal, errors)
            return D
        return _impl

    def _impl(series, path_or_buf=None, sep=',', na_rep='', float_format=
        None, columns=None, header=True, index=True, index_label=None, mode
        ='w', encoding=None, compression='infer', quoting=None, quotechar=
        '"', line_terminator=None, chunksize=None, date_format=None,
        doublequote=True, escapechar=None, decimal='.', errors='strict',
        _is_parallel=False):
        if _is_parallel:
            header &= (bodo.libs.distributed_api.get_rank() == 0
                ) | _csv_output_is_dir(unicode_to_utf8(path_or_buf))
        with numba.objmode(D='unicode_type'):
            D = series.to_csv(None, sep, na_rep, float_format, columns,
                header, index, index_label, mode, encoding, compression,
                quoting, quotechar, line_terminator, chunksize, date_format,
                doublequote, escapechar, decimal, errors)
        bodo.io.fs_io.csv_write(path_or_buf, D, _is_parallel)
    return _impl


@lower_constant(SeriesType)
def lower_constant_series(context, builder, series_type, pyval):
    data_val = context.get_constant_generic(builder, series_type.data,
        pyval.values)
    index_val = context.get_constant_generic(builder, series_type.index,
        pyval.index)
    name_val = context.get_constant_generic(builder, series_type.name_typ,
        pyval.name)
    secq__hbh = lir.Constant.literal_struct([data_val, index_val, name_val])
    secq__hbh = cgutils.global_constant(builder, '.const.payload', secq__hbh
        ).bitcast(cgutils.voidptr_t)
    gjqt__cyt = context.get_constant(types.int64, -1)
    oaqiu__oroqw = context.get_constant_null(types.voidptr)
    srsyl__rbxtw = lir.Constant.literal_struct([gjqt__cyt, oaqiu__oroqw,
        oaqiu__oroqw, secq__hbh, gjqt__cyt])
    srsyl__rbxtw = cgutils.global_constant(builder, '.const.meminfo',
        srsyl__rbxtw).bitcast(cgutils.voidptr_t)
    kanu__ysmh = lir.Constant.literal_struct([srsyl__rbxtw, oaqiu__oroqw])
    return kanu__ysmh


series_unsupported_attrs = {'axes', 'array', 'flags', 'at', 'is_unique',
    'sparse', 'attrs'}
series_unsupported_methods = ('set_flags', 'convert_dtypes', 'bool',
    'to_period', 'to_timestamp', '__array__', 'get', 'at', '__iter__',
    'items', 'iteritems', 'pop', 'item', 'xs', 'combine_first', 'agg',
    'aggregate', 'transform', 'expanding', 'ewm', 'clip', 'factorize',
    'mode', 'rank', 'align', 'drop', 'droplevel', 'duplicated', 'reindex',
    'reindex_like', 'rename_axis', 'sample', 'set_axis', 'truncate',
    'add_prefix', 'add_suffix', 'filter', 'interpolate', 'argmin', 'argmax',
    'reorder_levels', 'swaplevel', 'unstack', 'searchsorted', 'ravel',
    'squeeze', 'view', 'compare', 'update', 'asfreq', 'asof',
    'first_valid_index', 'last_valid_index', 'resample', 'tz_convert',
    'tz_localize', 'at_time', 'between_time', 'tshift', 'slice_shift',
    'plot', 'hist', 'to_pickle', 'to_excel', 'to_xarray', 'to_hdf',
    'to_sql', 'to_json', 'to_string', 'to_clipboard', 'to_latex', 'to_markdown'
    )


def _install_series_unsupported():
    for bha__uugm in series_unsupported_attrs:
        gbbs__kkuq = 'Series.' + bha__uugm
        overload_attribute(SeriesType, bha__uugm)(create_unsupported_overload
            (gbbs__kkuq))
    for fname in series_unsupported_methods:
        gbbs__kkuq = 'Series.' + fname
        overload_method(SeriesType, fname, no_unliteral=True)(
            create_unsupported_overload(gbbs__kkuq))


_install_series_unsupported()
heter_series_unsupported_attrs = {'axes', 'array', 'dtype', 'nbytes',
    'memory_usage', 'hasnans', 'dtypes', 'flags', 'at', 'is_unique',
    'is_monotonic', 'is_monotonic_increasing', 'is_monotonic_decreasing',
    'dt', 'str', 'cat', 'sparse', 'attrs'}
heter_series_unsupported_methods = {'set_flags', 'astype', 'convert_dtypes',
    'infer_objects', 'copy', 'bool', 'to_numpy', 'to_period',
    'to_timestamp', 'to_list', 'tolist', '__array__', 'get', 'at', 'iat',
    'iloc', 'loc', '__iter__', 'items', 'iteritems', 'keys', 'pop', 'item',
    'xs', 'add', 'sub', 'mul', 'div', 'truediv', 'floordiv', 'mod', 'pow',
    'radd', 'rsub', 'rmul', 'rdiv', 'rtruediv', 'rfloordiv', 'rmod', 'rpow',
    'combine', 'combine_first', 'round', 'lt', 'gt', 'le', 'ge', 'ne', 'eq',
    'product', 'dot', 'apply', 'agg', 'aggregate', 'transform', 'map',
    'groupby', 'rolling', 'expanding', 'ewm', 'pipe', 'abs', 'all', 'any',
    'autocorr', 'between', 'clip', 'corr', 'count', 'cov', 'cummax',
    'cummin', 'cumprod', 'cumsum', 'describe', 'diff', 'factorize', 'kurt',
    'mad', 'max', 'mean', 'median', 'min', 'mode', 'nlargest', 'nsmallest',
    'pct_change', 'prod', 'quantile', 'rank', 'sem', 'skew', 'std', 'sum',
    'var', 'kurtosis', 'unique', 'nunique', 'value_counts', 'align', 'drop',
    'droplevel', 'drop_duplicates', 'duplicated', 'equals', 'first', 'head',
    'idxmax', 'idxmin', 'isin', 'last', 'reindex', 'reindex_like', 'rename',
    'rename_axis', 'reset_index', 'sample', 'set_axis', 'take', 'tail',
    'truncate', 'where', 'mask', 'add_prefix', 'add_suffix', 'filter',
    'backfill', 'bfill', 'dropna', 'ffill', 'fillna', 'interpolate', 'isna',
    'isnull', 'notna', 'notnull', 'pad', 'replace', 'argsort', 'argmin',
    'argmax', 'reorder_levels', 'sort_values', 'sort_index', 'swaplevel',
    'unstack', 'explode', 'searchsorted', 'ravel', 'repeat', 'squeeze',
    'view', 'append', 'compare', 'update', 'asfreq', 'asof', 'shift',
    'first_valid_index', 'last_valid_index', 'resample', 'tz_convert',
    'tz_localize', 'at_time', 'between_time', 'tshift', 'slice_shift',
    'plot', 'hist', 'to_pickle', 'to_csv', 'to_dict', 'to_excel',
    'to_frame', 'to_xarray', 'to_hdf', 'to_sql', 'to_json', 'to_string',
    'to_clipboard', 'to_latex', 'to_markdown'}


def _install_heter_series_unsupported():
    for bha__uugm in heter_series_unsupported_attrs:
        gbbs__kkuq = 'HeterogeneousSeries.' + bha__uugm
        overload_attribute(HeterogeneousSeriesType, bha__uugm)(
            create_unsupported_overload(gbbs__kkuq))
    for fname in heter_series_unsupported_methods:
        gbbs__kkuq = 'HeterogeneousSeries.' + fname
        overload_method(HeterogeneousSeriesType, fname, no_unliteral=True)(
            create_unsupported_overload(gbbs__kkuq))


_install_heter_series_unsupported()
