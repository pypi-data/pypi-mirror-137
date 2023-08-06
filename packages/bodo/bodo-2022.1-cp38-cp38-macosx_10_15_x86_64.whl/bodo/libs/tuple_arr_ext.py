"""Array of tuple values, implemented by reusing array of structs implementation.
"""
import operator
import numba
import numpy as np
from numba.core import types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs.struct_arr_ext import StructArrayType, box_struct_arr, unbox_struct_array


class TupleArrayType(types.ArrayCompatible):

    def __init__(self, data):
        self.data = data
        super(TupleArrayType, self).__init__(name='TupleArrayType({})'.
            format(data))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.BaseTuple.from_types(tuple(zbn__pwt.dtype for zbn__pwt in
            self.data))

    def copy(self):
        return TupleArrayType(self.data)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(TupleArrayType)
class TupleArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        bsu__fanm = [('data', StructArrayType(fe_type.data))]
        models.StructModel.__init__(self, dmm, fe_type, bsu__fanm)


make_attribute_wrapper(TupleArrayType, 'data', '_data')


@intrinsic
def init_tuple_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, StructArrayType)
    knl__skah = TupleArrayType(data_typ.data)

    def codegen(context, builder, sig, args):
        eybo__dcl, = args
        des__emnpj = context.make_helper(builder, knl__skah)
        des__emnpj.data = eybo__dcl
        context.nrt.incref(builder, data_typ, eybo__dcl)
        return des__emnpj._getvalue()
    return knl__skah(data_typ), codegen


@unbox(TupleArrayType)
def unbox_tuple_array(typ, val, c):
    data_typ = StructArrayType(typ.data)
    kewsm__xlnb = unbox_struct_array(data_typ, val, c, is_tuple_array=True)
    eybo__dcl = kewsm__xlnb.value
    des__emnpj = c.context.make_helper(c.builder, typ)
    des__emnpj.data = eybo__dcl
    ose__mnnf = kewsm__xlnb.is_error
    return NativeValue(des__emnpj._getvalue(), is_error=ose__mnnf)


@box(TupleArrayType)
def box_tuple_arr(typ, val, c):
    data_typ = StructArrayType(typ.data)
    des__emnpj = c.context.make_helper(c.builder, typ, val)
    arr = box_struct_arr(data_typ, des__emnpj.data, c, is_tuple_array=True)
    return arr


@numba.njit
def pre_alloc_tuple_array(n, nested_counts, dtypes):
    return init_tuple_arr(bodo.libs.struct_arr_ext.pre_alloc_struct_array(n,
        nested_counts, dtypes, None))


def pre_alloc_tuple_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_tuple_arr_ext_pre_alloc_tuple_array
    ) = pre_alloc_tuple_array_equiv


@overload(operator.getitem, no_unliteral=True)
def tuple_arr_getitem(arr, ind):
    if not isinstance(arr, TupleArrayType):
        return
    if isinstance(ind, types.Integer):
        jsjey__fqm = 'def impl(arr, ind):\n'
        rsq__euhx = ','.join(f'get_data(arr._data)[{gdhd__dcs}][ind]' for
            gdhd__dcs in range(len(arr.data)))
        jsjey__fqm += f'  return ({rsq__euhx})\n'
        esj__xny = {}
        exec(jsjey__fqm, {'get_data': bodo.libs.struct_arr_ext.get_data},
            esj__xny)
        mvwsz__ixgfg = esj__xny['impl']
        return mvwsz__ixgfg

    def impl_arr(arr, ind):
        return init_tuple_arr(arr._data[ind])
    return impl_arr


@overload(operator.setitem, no_unliteral=True)
def tuple_arr_setitem(arr, ind, val):
    if not isinstance(arr, TupleArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if isinstance(ind, types.Integer):
        zqwyb__twt = len(arr.data)
        jsjey__fqm = 'def impl(arr, ind, val):\n'
        jsjey__fqm += '  data = get_data(arr._data)\n'
        jsjey__fqm += '  null_bitmap = get_null_bitmap(arr._data)\n'
        jsjey__fqm += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for gdhd__dcs in range(zqwyb__twt):
            jsjey__fqm += f'  data[{gdhd__dcs}][ind] = val[{gdhd__dcs}]\n'
        esj__xny = {}
        exec(jsjey__fqm, {'get_data': bodo.libs.struct_arr_ext.get_data,
            'get_null_bitmap': bodo.libs.struct_arr_ext.get_null_bitmap,
            'set_bit_to_arr': bodo.libs.int_arr_ext.set_bit_to_arr}, esj__xny)
        mvwsz__ixgfg = esj__xny['impl']
        return mvwsz__ixgfg

    def impl_arr(arr, ind, val):
        val = bodo.utils.conversion.coerce_to_array(val, use_nullable_array
            =True)
        arr._data[ind] = val._data
    return impl_arr


@overload(len, no_unliteral=True)
def overload_tuple_arr_len(A):
    if isinstance(A, TupleArrayType):
        return lambda A: len(A._data)


@overload_attribute(TupleArrayType, 'shape')
def overload_tuple_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(TupleArrayType, 'dtype')
def overload_tuple_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(TupleArrayType, 'ndim')
def overload_tuple_arr_ndim(A):
    return lambda A: 1


@overload_attribute(TupleArrayType, 'nbytes')
def overload_tuple_arr_nbytes(A):
    return lambda A: A._data.nbytes


@overload_method(TupleArrayType, 'copy', no_unliteral=True)
def overload_tuple_arr_copy(A):

    def copy_impl(A):
        return init_tuple_arr(A._data.copy())
    return copy_impl
