"""Support for MultiIndex type of Pandas
"""
import operator
import numba
import pandas as pd
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, register_model, typeof_impl, unbox
from bodo.utils.typing import BodoError, check_unsupported_args, dtype_to_array_type, get_val_type_maybe_str_literal, is_overload_none


class MultiIndexType(types.Type):

    def __init__(self, array_types, names_typ=None, name_typ=None):
        names_typ = (types.none,) * len(array_types
            ) if names_typ is None else names_typ
        name_typ = types.none if name_typ is None else name_typ
        self.array_types = array_types
        self.names_typ = names_typ
        self.name_typ = name_typ
        super(MultiIndexType, self).__init__(name=
            'MultiIndexType({}, {}, {})'.format(array_types, names_typ,
            name_typ))
    ndim = 1

    def copy(self):
        return MultiIndexType(self.array_types, self.names_typ, self.name_typ)

    @property
    def nlevels(self):
        return len(self.array_types)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(MultiIndexType)
class MultiIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        otv__qqhd = [('data', types.Tuple(fe_type.array_types)), ('names',
            types.Tuple(fe_type.names_typ)), ('name', fe_type.name_typ)]
        super(MultiIndexModel, self).__init__(dmm, fe_type, otv__qqhd)


make_attribute_wrapper(MultiIndexType, 'data', '_data')
make_attribute_wrapper(MultiIndexType, 'names', '_names')
make_attribute_wrapper(MultiIndexType, 'name', '_name')


@typeof_impl.register(pd.MultiIndex)
def typeof_multi_index(val, c):
    array_types = tuple(numba.typeof(val.levels[oghg__gryv].values) for
        oghg__gryv in range(val.nlevels))
    return MultiIndexType(array_types, tuple(get_val_type_maybe_str_literal
        (tqjr__fgom) for tqjr__fgom in val.names), numba.typeof(val.name))


@box(MultiIndexType)
def box_multi_index(typ, val, c):
    ncr__xqv = c.context.insert_const_string(c.builder.module, 'pandas')
    kjn__ani = c.pyapi.import_module_noblock(ncr__xqv)
    fvp__eiebg = c.pyapi.object_getattr_string(kjn__ani, 'MultiIndex')
    bom__jycw = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Tuple(typ.array_types), bom__jycw
        .data)
    data = c.pyapi.from_native_value(types.Tuple(typ.array_types),
        bom__jycw.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Tuple(typ.names_typ), bom__jycw.names
        )
    names = c.pyapi.from_native_value(types.Tuple(typ.names_typ), bom__jycw
        .names, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, bom__jycw.name)
    name = c.pyapi.from_native_value(typ.name_typ, bom__jycw.name, c.
        env_manager)
    sortorder = c.pyapi.make_none()
    bzke__dhn = c.pyapi.call_method(fvp__eiebg, 'from_arrays', (data,
        sortorder, names))
    c.pyapi.object_setattr_string(bzke__dhn, 'name', name)
    c.pyapi.decref(kjn__ani)
    c.pyapi.decref(fvp__eiebg)
    c.context.nrt.decref(c.builder, typ, val)
    return bzke__dhn


@unbox(MultiIndexType)
def unbox_multi_index(typ, val, c):
    fhyqc__aey = []
    yav__tavq = []
    for oghg__gryv in range(typ.nlevels):
        iuoqu__fse = c.pyapi.unserialize(c.pyapi.serialize_object(oghg__gryv))
        upd__ancfb = c.pyapi.call_method(val, 'get_level_values', (iuoqu__fse,)
            )
        rux__gir = c.pyapi.object_getattr_string(upd__ancfb, 'values')
        c.pyapi.decref(upd__ancfb)
        c.pyapi.decref(iuoqu__fse)
        bmp__dgod = c.pyapi.to_native_value(typ.array_types[oghg__gryv],
            rux__gir).value
        fhyqc__aey.append(bmp__dgod)
        yav__tavq.append(rux__gir)
    if isinstance(types.Tuple(typ.array_types), types.UniTuple):
        data = cgutils.pack_array(c.builder, fhyqc__aey)
    else:
        data = cgutils.pack_struct(c.builder, fhyqc__aey)
    ldsoy__torcf = c.pyapi.object_getattr_string(val, 'names')
    caum__fzp = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    pysos__yaui = c.pyapi.call_function_objargs(caum__fzp, (ldsoy__torcf,))
    names = c.pyapi.to_native_value(types.Tuple(typ.names_typ), pysos__yaui
        ).value
    pwp__vsmd = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, pwp__vsmd).value
    bom__jycw = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    bom__jycw.data = data
    bom__jycw.names = names
    bom__jycw.name = name
    for rux__gir in yav__tavq:
        c.pyapi.decref(rux__gir)
    c.pyapi.decref(ldsoy__torcf)
    c.pyapi.decref(caum__fzp)
    c.pyapi.decref(pysos__yaui)
    c.pyapi.decref(pwp__vsmd)
    return NativeValue(bom__jycw._getvalue())


def from_product_error_checking(iterables, sortorder, names):
    gzl__jrqwn = 'pandas.MultiIndex.from_product'
    jbqee__bvh = dict(sortorder=sortorder)
    vlwi__vyn = dict(sortorder=None)
    check_unsupported_args(gzl__jrqwn, jbqee__bvh, vlwi__vyn, package_name=
        'pandas', module_name='Index')
    if not (is_overload_none(names) or isinstance(names, types.BaseTuple)):
        raise BodoError(f'{gzl__jrqwn}: names must be None or a tuple.')
    elif not isinstance(iterables, types.BaseTuple):
        raise BodoError(f'{gzl__jrqwn}: iterables must be a tuple.')
    elif not is_overload_none(names) and len(iterables) != len(names):
        raise BodoError(
            f'{gzl__jrqwn}: iterables and names must be of the same length.')


def from_product(iterable, sortorder=None, names=None):
    pass


@overload(from_product)
def from_product_overload(iterables, sortorder=None, names=None):
    from_product_error_checking(iterables, sortorder, names)
    array_types = tuple(dtype_to_array_type(iterable.dtype) for iterable in
        iterables)
    if is_overload_none(names):
        names_typ = tuple([types.none] * len(iterables))
    else:
        names_typ = names.types
    ara__lwi = MultiIndexType(array_types, names_typ)
    wjv__dclc = f'from_product_multiindex{numba.core.ir_utils.next_label()}'
    setattr(types, wjv__dclc, ara__lwi)
    tpxka__ctm = f"""
def impl(iterables, sortorder=None, names=None):
    with numba.objmode(mi='{wjv__dclc}'):
        mi = pd.MultiIndex.from_product(iterables, names=names)
    return mi
"""
    ehmz__arx = {}
    exec(tpxka__ctm, globals(), ehmz__arx)
    lfvf__vvt = ehmz__arx['impl']
    return lfvf__vvt


@intrinsic
def init_multi_index(typingctx, data, names, name=None):
    name = types.none if name is None else name
    names = types.Tuple(names.types)

    def codegen(context, builder, signature, args):
        ffscs__fzsxq, zjd__corn, hzwxp__bse = args
        llgg__liyyu = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        llgg__liyyu.data = ffscs__fzsxq
        llgg__liyyu.names = zjd__corn
        llgg__liyyu.name = hzwxp__bse
        context.nrt.incref(builder, signature.args[0], ffscs__fzsxq)
        context.nrt.incref(builder, signature.args[1], zjd__corn)
        context.nrt.incref(builder, signature.args[2], hzwxp__bse)
        return llgg__liyyu._getvalue()
    vxk__kpsj = MultiIndexType(data.types, names.types, name)
    return vxk__kpsj(data, names, name), codegen


@overload(len, no_unliteral=True)
def overload_len_pd_multiindex(A):
    if isinstance(A, MultiIndexType):
        return lambda A: len(A._data[0])


@overload(operator.getitem, no_unliteral=True)
def overload_multi_index_getitem(I, ind):
    if not isinstance(I, MultiIndexType):
        return
    if not isinstance(ind, types.Integer):
        xxmk__jzskj = len(I.array_types)
        tpxka__ctm = 'def impl(I, ind):\n'
        tpxka__ctm += '  data = I._data\n'
        tpxka__ctm += ('  return init_multi_index(({},), I._names, I._name)\n'
            .format(', '.join(f'data[{oghg__gryv}][ind]' for oghg__gryv in
            range(xxmk__jzskj))))
        ehmz__arx = {}
        exec(tpxka__ctm, {'init_multi_index': init_multi_index}, ehmz__arx)
        lfvf__vvt = ehmz__arx['impl']
        return lfvf__vvt


@lower_builtin(operator.is_, MultiIndexType, MultiIndexType)
def multi_index_is(context, builder, sig, args):
    pfx__ify, zepp__sis = sig.args
    if pfx__ify != zepp__sis:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._data is b._data and a._names is b._names and a._name is
            b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)
