"""
Array of intervals corresponding to IntervalArray of Pandas.
Used for IntervalIndex, which is necessary for Series.value_counts() with 'bins'
argument.
"""
import numba
import pandas as pd
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo


class IntervalType(types.Type):

    def __init__(self):
        super(IntervalType, self).__init__('IntervalType()')


class IntervalArrayType(types.ArrayCompatible):

    def __init__(self, arr_type):
        self.arr_type = arr_type
        self.dtype = IntervalType()
        super(IntervalArrayType, self).__init__(name=
            f'IntervalArrayType({arr_type})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return IntervalArrayType(self.arr_type)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(IntervalArrayType)
class IntervalArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ugbp__okzo = [('left', fe_type.arr_type), ('right', fe_type.arr_type)]
        models.StructModel.__init__(self, dmm, fe_type, ugbp__okzo)


make_attribute_wrapper(IntervalArrayType, 'left', '_left')
make_attribute_wrapper(IntervalArrayType, 'right', '_right')


@typeof_impl.register(pd.arrays.IntervalArray)
def typeof_interval_array(val, c):
    arr_type = bodo.typeof(val._left)
    return IntervalArrayType(arr_type)


@intrinsic
def init_interval_array(typingctx, left, right=None):
    assert left == right, 'Interval left/right array types should be the same'

    def codegen(context, builder, signature, args):
        vzup__umhu, bjc__hib = args
        akhbz__mspdi = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        akhbz__mspdi.left = vzup__umhu
        akhbz__mspdi.right = bjc__hib
        context.nrt.incref(builder, signature.args[0], vzup__umhu)
        context.nrt.incref(builder, signature.args[1], bjc__hib)
        return akhbz__mspdi._getvalue()
    bxv__xxb = IntervalArrayType(left)
    tbfy__jiz = bxv__xxb(left, right)
    return tbfy__jiz, codegen


def init_interval_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    zwf__bubw = []
    for ryh__iqcfc in args:
        zea__vhidg = equiv_set.get_shape(ryh__iqcfc)
        if zea__vhidg is not None:
            zwf__bubw.append(zea__vhidg[0])
    if len(zwf__bubw) > 1:
        equiv_set.insert_equiv(*zwf__bubw)
    left = args[0]
    if equiv_set.has_shape(left):
        return ArrayAnalysis.AnalyzeResult(shape=left, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_libs_interval_arr_ext_init_interval_array
    ) = init_interval_array_equiv


def alias_ext_init_interval_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_interval_array',
    'bodo.libs.int_arr_ext'] = alias_ext_init_interval_array


@box(IntervalArrayType)
def box_interval_arr(typ, val, c):
    akhbz__mspdi = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.arr_type, akhbz__mspdi.left)
    rwgsv__jdf = c.pyapi.from_native_value(typ.arr_type, akhbz__mspdi.left,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.arr_type, akhbz__mspdi.right)
    vfbr__mppvb = c.pyapi.from_native_value(typ.arr_type, akhbz__mspdi.
        right, c.env_manager)
    brkh__ize = c.context.insert_const_string(c.builder.module, 'pandas')
    hveoa__czoc = c.pyapi.import_module_noblock(brkh__ize)
    tfm__kqyk = c.pyapi.object_getattr_string(hveoa__czoc, 'arrays')
    klu__xpue = c.pyapi.object_getattr_string(tfm__kqyk, 'IntervalArray')
    evvfh__kwdwy = c.pyapi.call_method(klu__xpue, 'from_arrays', (
        rwgsv__jdf, vfbr__mppvb))
    c.pyapi.decref(rwgsv__jdf)
    c.pyapi.decref(vfbr__mppvb)
    c.pyapi.decref(hveoa__czoc)
    c.pyapi.decref(tfm__kqyk)
    c.pyapi.decref(klu__xpue)
    c.context.nrt.decref(c.builder, typ, val)
    return evvfh__kwdwy


@unbox(IntervalArrayType)
def unbox_interval_arr(typ, val, c):
    rwgsv__jdf = c.pyapi.object_getattr_string(val, '_left')
    left = c.pyapi.to_native_value(typ.arr_type, rwgsv__jdf).value
    c.pyapi.decref(rwgsv__jdf)
    vfbr__mppvb = c.pyapi.object_getattr_string(val, '_right')
    right = c.pyapi.to_native_value(typ.arr_type, vfbr__mppvb).value
    c.pyapi.decref(vfbr__mppvb)
    akhbz__mspdi = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    akhbz__mspdi.left = left
    akhbz__mspdi.right = right
    hhxnw__zfw = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(akhbz__mspdi._getvalue(), is_error=hhxnw__zfw)


@overload(len, no_unliteral=True)
def overload_interval_arr_len(A):
    if isinstance(A, IntervalArrayType):
        return lambda A: len(A._left)


@overload_attribute(IntervalArrayType, 'shape')
def overload_interval_arr_shape(A):
    return lambda A: (len(A._left),)


@overload_attribute(IntervalArrayType, 'ndim')
def overload_interval_arr_ndim(A):
    return lambda A: 1


@overload_attribute(IntervalArrayType, 'nbytes')
def overload_interval_arr_nbytes(A):
    return lambda A: A._left.nbytes + A._right.nbytes


@overload_method(IntervalArrayType, 'copy', no_unliteral=True)
def overload_interval_arr_copy(A):
    return lambda A: bodo.libs.interval_arr_ext.init_interval_array(A._left
        .copy(), A._right.copy())
