"""
Wrapper class for Tuples that supports tracking null entries.
This is primarily used for maintaining null information for
Series values used in df.apply
"""
import operator
from numba.core import cgutils, types
from numba.extending import box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, register_model


class NullableTupleType(types.IterableType):

    def __init__(self, tuple_typ, null_typ):
        self._tuple_typ = tuple_typ
        self._null_typ = null_typ
        super(NullableTupleType, self).__init__(name=
            f'NullableTupleType({tuple_typ}, {null_typ})')

    @property
    def tuple_typ(self):
        return self._tuple_typ

    @property
    def null_typ(self):
        return self._null_typ

    def __getitem__(self, i):
        return self._tuple_typ[i]

    @property
    def key(self):
        return self._tuple_typ

    @property
    def dtype(self):
        return self.tuple_typ.dtype

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def iterator_type(self):
        return self.tuple_typ.iterator_type


@register_model(NullableTupleType)
class NullableTupleModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        josfc__fwuz = [('data', fe_type.tuple_typ), ('null_values', fe_type
            .null_typ)]
        super(NullableTupleModel, self).__init__(dmm, fe_type, josfc__fwuz)


make_attribute_wrapper(NullableTupleType, 'data', '_data')
make_attribute_wrapper(NullableTupleType, 'null_values', '_null_values')


@intrinsic
def build_nullable_tuple(typingctx, data_tuple, null_values):
    assert isinstance(data_tuple, types.BaseTuple
        ), "build_nullable_tuple 'data_tuple' argument must be a tuple"
    assert isinstance(null_values, types.BaseTuple
        ), "build_nullable_tuple 'null_values' argument must be a tuple"

    def codegen(context, builder, signature, args):
        data_tuple, null_values = args
        agsh__jnpj = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        agsh__jnpj.data = data_tuple
        agsh__jnpj.null_values = null_values
        context.nrt.incref(builder, signature.args[0], data_tuple)
        context.nrt.incref(builder, signature.args[1], null_values)
        return agsh__jnpj._getvalue()
    sig = NullableTupleType(data_tuple, null_values)(data_tuple, null_values)
    return sig, codegen


@box(NullableTupleType)
def box_nullable_tuple(typ, val, c):
    tnn__ymuh = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    c.context.nrt.incref(c.builder, typ.tuple_typ, tnn__ymuh.data)
    c.context.nrt.incref(c.builder, typ.null_typ, tnn__ymuh.null_values)
    qpm__lnb = c.pyapi.from_native_value(typ.tuple_typ, tnn__ymuh.data, c.
        env_manager)
    sus__njpiz = c.pyapi.from_native_value(typ.null_typ, tnn__ymuh.
        null_values, c.env_manager)
    goe__hdox = c.context.get_constant(types.int64, len(typ.tuple_typ))
    ucv__ounc = c.pyapi.list_new(goe__hdox)
    with cgutils.for_range(c.builder, goe__hdox) as loop:
        i = loop.index
        dduf__nlxgg = c.pyapi.long_from_longlong(i)
        ycpg__ylj = c.pyapi.object_getitem(sus__njpiz, dduf__nlxgg)
        ctk__yclio = c.pyapi.to_native_value(types.bool_, ycpg__ylj).value
        with c.builder.if_else(ctk__yclio) as (then, orelse):
            with then:
                c.pyapi.list_setitem(ucv__ounc, i, c.pyapi.make_none())
            with orelse:
                wxgjn__orjgm = c.pyapi.object_getitem(qpm__lnb, dduf__nlxgg)
                c.pyapi.list_setitem(ucv__ounc, i, wxgjn__orjgm)
        c.pyapi.decref(dduf__nlxgg)
        c.pyapi.decref(ycpg__ylj)
    geh__bxehm = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    pjji__ypt = c.pyapi.call_function_objargs(geh__bxehm, (ucv__ounc,))
    c.pyapi.decref(qpm__lnb)
    c.pyapi.decref(sus__njpiz)
    c.pyapi.decref(geh__bxehm)
    c.pyapi.decref(ucv__ounc)
    c.context.nrt.decref(c.builder, typ, val)
    return pjji__ypt


@overload(operator.getitem)
def overload_getitem(A, idx):
    if not isinstance(A, NullableTupleType):
        return
    return lambda A, idx: A._data[idx]


@overload(len)
def overload_len(A):
    if not isinstance(A, NullableTupleType):
        return
    return lambda A: len(A._data)


@lower_builtin('getiter', NullableTupleType)
def nullable_tuple_getiter(context, builder, sig, args):
    agsh__jnpj = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    mpgix__eemsc = context.get_function('getiter', sig.return_type(sig.args
        [0].tuple_typ))
    return mpgix__eemsc(builder, (agsh__jnpj.data,))
