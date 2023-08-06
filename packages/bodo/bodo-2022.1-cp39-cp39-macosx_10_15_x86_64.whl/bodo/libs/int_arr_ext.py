"""Nullable integer array corresponding to Pandas IntegerArray.
However, nulls are stored in bit arrays similar to Arrow's arrays.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs.str_arr_ext import kBitmask
from bodo.libs import array_ext, hstr_ext
ll.add_symbol('mask_arr_to_bitmap', hstr_ext.mask_arr_to_bitmap)
ll.add_symbol('is_pd_int_array', array_ext.is_pd_int_array)
ll.add_symbol('int_array_from_sequence', array_ext.int_array_from_sequence)
from bodo.hiframes.datetime_timedelta_ext import pd_timedelta_type
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, check_unsupported_args, is_iterable_type, is_list_like_index_type, is_overload_false, is_overload_none, is_overload_true, parse_dtype, raise_bodo_error, to_nullable_type


class IntegerArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        self.dtype = dtype
        super(IntegerArrayType, self).__init__(name='IntegerArrayType({})'.
            format(dtype))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return IntegerArrayType(self.dtype)


@register_model(IntegerArrayType)
class IntegerArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ycmhp__asgu = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, ycmhp__asgu)


make_attribute_wrapper(IntegerArrayType, 'data', '_data')
make_attribute_wrapper(IntegerArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.IntegerArray)
def _typeof_pd_int_array(val, c):
    usz__upfia = 8 * val.dtype.itemsize
    yqp__vsfz = '' if val.dtype.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(yqp__vsfz, usz__upfia))
    return IntegerArrayType(dtype)


class IntDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Integer)
        self.dtype = dtype
        peyq__rwxg = '{}Int{}Dtype()'.format('' if dtype.signed else 'U',
            dtype.bitwidth)
        super(IntDtype, self).__init__(peyq__rwxg)


register_model(IntDtype)(models.OpaqueModel)


@box(IntDtype)
def box_intdtype(typ, val, c):
    zukor__vrh = c.context.insert_const_string(c.builder.module, 'pandas')
    ypu__rwvve = c.pyapi.import_module_noblock(zukor__vrh)
    tnunc__gdeax = c.pyapi.call_method(ypu__rwvve, str(typ)[:-2], ())
    c.pyapi.decref(ypu__rwvve)
    return tnunc__gdeax


@unbox(IntDtype)
def unbox_intdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_int_dtype(val, c):
    usz__upfia = 8 * val.itemsize
    yqp__vsfz = '' if val.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(yqp__vsfz, usz__upfia))
    return IntDtype(dtype)


def _register_int_dtype(t):
    typeof_impl.register(t)(typeof_pd_int_dtype)
    int_dtype = typeof_pd_int_dtype(t(), None)
    type_callable(t)(lambda c: lambda : int_dtype)
    lower_builtin(t)(lambda c, b, s, a: c.get_dummy_value())


pd_int_dtype_classes = (pd.Int8Dtype, pd.Int16Dtype, pd.Int32Dtype, pd.
    Int64Dtype, pd.UInt8Dtype, pd.UInt16Dtype, pd.UInt32Dtype, pd.UInt64Dtype)
for t in pd_int_dtype_classes:
    _register_int_dtype(t)


@numba.extending.register_jitable
def mask_arr_to_bitmap(mask_arr):
    n = len(mask_arr)
    qxqm__coo = n + 7 >> 3
    hrap__rzfio = np.empty(qxqm__coo, np.uint8)
    for i in range(n):
        kolqx__wmow = i // 8
        hrap__rzfio[kolqx__wmow] ^= np.uint8(-np.uint8(not mask_arr[i]) ^
            hrap__rzfio[kolqx__wmow]) & kBitmask[i % 8]
    return hrap__rzfio


@unbox(IntegerArrayType)
def unbox_int_array(typ, obj, c):
    qvr__lgclh = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(qvr__lgclh)
    c.pyapi.decref(qvr__lgclh)
    gbfmm__rym = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qxqm__coo = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(64
        ), 7)), lir.Constant(lir.IntType(64), 8))
    pyr__ztlzy = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [qxqm__coo])
    ibker__fcg = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    uimsl__ybu = cgutils.get_or_insert_function(c.builder.module,
        ibker__fcg, name='is_pd_int_array')
    ilbxg__pts = c.builder.call(uimsl__ybu, [obj])
    wbck__syvn = c.builder.icmp_unsigned('!=', ilbxg__pts, ilbxg__pts.type(0))
    with c.builder.if_else(wbck__syvn) as (pd_then, pd_otherwise):
        with pd_then:
            bkng__aqf = c.pyapi.object_getattr_string(obj, '_data')
            gbfmm__rym.data = c.pyapi.to_native_value(types.Array(typ.dtype,
                1, 'C'), bkng__aqf).value
            owbvn__hoos = c.pyapi.object_getattr_string(obj, '_mask')
            mask_arr = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), owbvn__hoos).value
            c.pyapi.decref(bkng__aqf)
            c.pyapi.decref(owbvn__hoos)
            urjx__lwuz = c.context.make_array(types.Array(types.bool_, 1, 'C')
                )(c.context, c.builder, mask_arr)
            ibker__fcg = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            uimsl__ybu = cgutils.get_or_insert_function(c.builder.module,
                ibker__fcg, name='mask_arr_to_bitmap')
            c.builder.call(uimsl__ybu, [pyr__ztlzy.data, urjx__lwuz.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), mask_arr)
        with pd_otherwise:
            qfjmw__hzqpo = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            ibker__fcg = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            ihvs__qpmgf = cgutils.get_or_insert_function(c.builder.module,
                ibker__fcg, name='int_array_from_sequence')
            c.builder.call(ihvs__qpmgf, [obj, c.builder.bitcast(
                qfjmw__hzqpo.data, lir.IntType(8).as_pointer()), pyr__ztlzy
                .data])
            gbfmm__rym.data = qfjmw__hzqpo._getvalue()
    gbfmm__rym.null_bitmap = pyr__ztlzy._getvalue()
    tjmpq__wvq = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(gbfmm__rym._getvalue(), is_error=tjmpq__wvq)


@box(IntegerArrayType)
def box_int_arr(typ, val, c):
    gbfmm__rym = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        gbfmm__rym.data, c.env_manager)
    liez__wygcl = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, gbfmm__rym.null_bitmap).data
    qvr__lgclh = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(qvr__lgclh)
    zukor__vrh = c.context.insert_const_string(c.builder.module, 'numpy')
    mgx__ukyzk = c.pyapi.import_module_noblock(zukor__vrh)
    gjjtb__wvhkv = c.pyapi.object_getattr_string(mgx__ukyzk, 'bool_')
    mask_arr = c.pyapi.call_method(mgx__ukyzk, 'empty', (qvr__lgclh,
        gjjtb__wvhkv))
    snvzm__ssxs = c.pyapi.object_getattr_string(mask_arr, 'ctypes')
    jiu__fip = c.pyapi.object_getattr_string(snvzm__ssxs, 'data')
    pqps__qray = c.builder.inttoptr(c.pyapi.long_as_longlong(jiu__fip), lir
        .IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as loop:
        i = loop.index
        fioak__fda = c.builder.lshr(i, lir.Constant(lir.IntType(64), 3))
        hfaq__zkbb = c.builder.load(cgutils.gep(c.builder, liez__wygcl,
            fioak__fda))
        llxa__rirdl = c.builder.trunc(c.builder.and_(i, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(hfaq__zkbb, llxa__rirdl), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        cebuo__ooftq = cgutils.gep(c.builder, pqps__qray, i)
        c.builder.store(val, cebuo__ooftq)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        gbfmm__rym.null_bitmap)
    zukor__vrh = c.context.insert_const_string(c.builder.module, 'pandas')
    ypu__rwvve = c.pyapi.import_module_noblock(zukor__vrh)
    aygle__lhmhl = c.pyapi.object_getattr_string(ypu__rwvve, 'arrays')
    tnunc__gdeax = c.pyapi.call_method(aygle__lhmhl, 'IntegerArray', (data,
        mask_arr))
    c.pyapi.decref(ypu__rwvve)
    c.pyapi.decref(qvr__lgclh)
    c.pyapi.decref(mgx__ukyzk)
    c.pyapi.decref(gjjtb__wvhkv)
    c.pyapi.decref(snvzm__ssxs)
    c.pyapi.decref(jiu__fip)
    c.pyapi.decref(aygle__lhmhl)
    c.pyapi.decref(data)
    c.pyapi.decref(mask_arr)
    return tnunc__gdeax


@intrinsic
def init_integer_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        tior__shf, dfgt__atqzm = args
        gbfmm__rym = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        gbfmm__rym.data = tior__shf
        gbfmm__rym.null_bitmap = dfgt__atqzm
        context.nrt.incref(builder, signature.args[0], tior__shf)
        context.nrt.incref(builder, signature.args[1], dfgt__atqzm)
        return gbfmm__rym._getvalue()
    tqrk__ecc = IntegerArrayType(data.dtype)
    iywb__vvo = tqrk__ecc(data, null_bitmap)
    return iywb__vvo, codegen


@lower_constant(IntegerArrayType)
def lower_constant_int_arr(context, builder, typ, pyval):
    n = len(pyval)
    luzl__ndk = np.empty(n, pyval.dtype.type)
    wtjv__nxud = np.empty(n + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        thxcg__ycf = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(wtjv__nxud, i, int(not thxcg__ycf)
            )
        if not thxcg__ycf:
            luzl__ndk[i] = s
    ukfbq__cujwg = context.get_constant_generic(builder, types.Array(typ.
        dtype, 1, 'C'), luzl__ndk)
    lzwb__dkfm = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), wtjv__nxud)
    return lir.Constant.literal_struct([ukfbq__cujwg, lzwb__dkfm])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_int_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    hip__gckv = args[0]
    if equiv_set.has_shape(hip__gckv):
        return ArrayAnalysis.AnalyzeResult(shape=hip__gckv, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_get_int_arr_data = (
    get_int_arr_data_equiv)


def init_integer_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    hip__gckv = args[0]
    if equiv_set.has_shape(hip__gckv):
        return ArrayAnalysis.AnalyzeResult(shape=hip__gckv, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_init_integer_array = (
    init_integer_array_equiv)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


def alias_ext_init_integer_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_integer_array',
    'bodo.libs.int_arr_ext'] = alias_ext_init_integer_array
numba.core.ir_utils.alias_func_extensions['get_int_arr_data',
    'bodo.libs.int_arr_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_int_arr_bitmap',
    'bodo.libs.int_arr_ext'] = alias_ext_dummy_func


@numba.njit(no_cpython_wrapper=True)
def alloc_int_array(n, dtype):
    luzl__ndk = np.empty(n, dtype)
    obkh__lskx = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_integer_array(luzl__ndk, obkh__lskx)


def alloc_int_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_alloc_int_array = (
    alloc_int_array_equiv)


@numba.extending.register_jitable
def set_bit_to_arr(bits, i, bit_is_set):
    bits[i // 8] ^= np.uint8(-np.uint8(bit_is_set) ^ bits[i // 8]) & kBitmask[
        i % 8]


@numba.extending.register_jitable
def get_bit_bitmap_arr(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@overload(operator.getitem, no_unliteral=True)
def int_arr_getitem(A, ind):
    if not isinstance(A, IntegerArrayType):
        return
    if isinstance(ind, types.Integer):
        return lambda A, ind: A._data[ind]
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            mycdj__pisyi, kqfho__seaqw = array_getitem_bool_index(A, ind)
            return init_integer_array(mycdj__pisyi, kqfho__seaqw)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            mycdj__pisyi, kqfho__seaqw = array_getitem_int_index(A, ind)
            return init_integer_array(mycdj__pisyi, kqfho__seaqw)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            mycdj__pisyi, kqfho__seaqw = array_getitem_slice_index(A, ind)
            return init_integer_array(mycdj__pisyi, kqfho__seaqw)
        return impl_slice
    raise BodoError(
        f'getitem for IntegerArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def int_arr_setitem(A, idx, val):
    if not isinstance(A, IntegerArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    dehc__xpgh = (
        f"setitem for IntegerArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    umb__jhmoj = isinstance(val, (types.Integer, types.Boolean))
    if isinstance(idx, types.Integer):
        if umb__jhmoj:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(dehc__xpgh)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean)) or umb__jhmoj):
        raise BodoError(dehc__xpgh)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, types.Integer):

        def impl_arr_ind_mask(A, idx, val):
            array_setitem_int_index(A, idx, val)
        return impl_arr_ind_mask
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:

        def impl_bool_ind_mask(A, idx, val):
            array_setitem_bool_index(A, idx, val)
        return impl_bool_ind_mask
    if isinstance(idx, types.SliceType):

        def impl_slice_mask(A, idx, val):
            array_setitem_slice_index(A, idx, val)
        return impl_slice_mask
    raise BodoError(
        f'setitem for IntegerArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_int_arr_len(A):
    if isinstance(A, IntegerArrayType):
        return lambda A: len(A._data)


@overload_attribute(IntegerArrayType, 'shape')
def overload_int_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(IntegerArrayType, 'dtype')
def overload_int_arr_dtype(A):
    dtype_class = getattr(pd, '{}Int{}Dtype'.format('' if A.dtype.signed else
        'U', A.dtype.bitwidth))
    return lambda A: dtype_class()


@overload_attribute(IntegerArrayType, 'ndim')
def overload_int_arr_ndim(A):
    return lambda A: 1


@overload_attribute(IntegerArrayType, 'nbytes')
def int_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


@overload_method(IntegerArrayType, 'copy', no_unliteral=True)
def overload_int_arr_copy(A, dtype=None):
    if not is_overload_none(dtype):
        return lambda A, dtype=None: A.astype(dtype, copy=True)
    else:
        return lambda A, dtype=None: bodo.libs.int_arr_ext.init_integer_array(
            bodo.libs.int_arr_ext.get_int_arr_data(A).copy(), bodo.libs.
            int_arr_ext.get_int_arr_bitmap(A).copy())


@overload_method(IntegerArrayType, 'astype', no_unliteral=True)
def overload_int_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "IntegerArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if isinstance(dtype, types.NumberClass):
        dtype = dtype.dtype
    if isinstance(dtype, IntDtype) and A.dtype == dtype.dtype:
        if is_overload_false(copy):
            return lambda A, dtype, copy=True: A
        elif is_overload_true(copy):
            return lambda A, dtype, copy=True: A.copy()
        else:

            def impl(A, dtype, copy=True):
                if copy:
                    return A.copy()
                else:
                    return A
            return impl
    if isinstance(dtype, IntDtype):
        np_dtype = dtype.dtype
        return (lambda A, dtype, copy=True: bodo.libs.int_arr_ext.
            init_integer_array(bodo.libs.int_arr_ext.get_int_arr_data(A).
            astype(np_dtype), bodo.libs.int_arr_ext.get_int_arr_bitmap(A).
            copy()))
    nb_dtype = parse_dtype(dtype, 'IntegerArray.astype')
    if isinstance(nb_dtype, types.Float):

        def impl_float(A, dtype, copy=True):
            data = bodo.libs.int_arr_ext.get_int_arr_data(A)
            n = len(data)
            tqbse__uuav = np.empty(n, nb_dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                tqbse__uuav[i] = data[i]
                if bodo.libs.array_kernels.isna(A, i):
                    tqbse__uuav[i] = np.nan
            return tqbse__uuav
        return impl_float
    return lambda A, dtype, copy=True: bodo.libs.int_arr_ext.get_int_arr_data(A
        ).astype(nb_dtype)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def apply_null_mask(arr, bitmap, mask_fill, inplace):
    assert isinstance(arr, types.Array)
    if isinstance(arr.dtype, types.Integer):
        if is_overload_none(inplace):
            return (lambda arr, bitmap, mask_fill, inplace: bodo.libs.
                int_arr_ext.init_integer_array(arr, bitmap.copy()))
        else:
            return (lambda arr, bitmap, mask_fill, inplace: bodo.libs.
                int_arr_ext.init_integer_array(arr, bitmap))
    if isinstance(arr.dtype, types.Float):

        def impl(arr, bitmap, mask_fill, inplace):
            n = len(arr)
            for i in numba.parfors.parfor.internal_prange(n):
                if not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bitmap, i):
                    arr[i] = np.nan
            return arr
        return impl
    if arr.dtype == types.bool_:

        def impl_bool(arr, bitmap, mask_fill, inplace):
            n = len(arr)
            for i in numba.parfors.parfor.internal_prange(n):
                if not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bitmap, i):
                    arr[i] = mask_fill
            return arr
        return impl_bool
    return lambda arr, bitmap, mask_fill, inplace: arr


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def merge_bitmaps(B1, B2, n, inplace):
    assert B1 == types.Array(types.uint8, 1, 'C')
    assert B2 == types.Array(types.uint8, 1, 'C')
    if not is_overload_none(inplace):

        def impl_inplace(B1, B2, n, inplace):
            for i in numba.parfors.parfor.internal_prange(n):
                nwb__swx = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
                wcjy__crp = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
                gwwnv__dwlt = nwb__swx & wcjy__crp
                bodo.libs.int_arr_ext.set_bit_to_arr(B1, i, gwwnv__dwlt)
            return B1
        return impl_inplace

    def impl(B1, B2, n, inplace):
        numba.parfors.parfor.init_prange()
        qxqm__coo = n + 7 >> 3
        tqbse__uuav = np.empty(qxqm__coo, np.uint8)
        for i in numba.parfors.parfor.internal_prange(n):
            nwb__swx = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
            wcjy__crp = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
            gwwnv__dwlt = nwb__swx & wcjy__crp
            bodo.libs.int_arr_ext.set_bit_to_arr(tqbse__uuav, i, gwwnv__dwlt)
        return tqbse__uuav
    return impl


ufunc_aliases = {'subtract': 'sub', 'multiply': 'mul', 'floor_divide':
    'floordiv', 'true_divide': 'truediv', 'power': 'pow', 'remainder':
    'mod', 'divide': 'div', 'equal': 'eq', 'not_equal': 'ne', 'less': 'lt',
    'less_equal': 'le', 'greater': 'gt', 'greater_equal': 'ge'}


def create_op_overload(op, n_inputs):
    if n_inputs == 1:

        def overload_int_arr_op_nin_1(A):
            if isinstance(A, IntegerArrayType):
                return get_nullable_array_unary_impl(op, A)
        return overload_int_arr_op_nin_1
    elif n_inputs == 2:

        def overload_series_op_nin_2(lhs, rhs):
            if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
                IntegerArrayType):
                return get_nullable_array_binary_impl(op, lhs, rhs)
        return overload_series_op_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for llpl__jgn in numba.np.ufunc_db.get_ufuncs():
        idd__gqdro = create_op_overload(llpl__jgn, llpl__jgn.nin)
        overload(llpl__jgn, no_unliteral=True)(idd__gqdro)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        idd__gqdro = create_op_overload(op, 2)
        overload(op)(idd__gqdro)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        idd__gqdro = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(idd__gqdro)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        idd__gqdro = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(idd__gqdro)


_install_unary_ops()


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data_tup(arrs):
    xnlmh__mqvbi = len(arrs.types)
    rnme__ftqz = 'def f(arrs):\n'
    tnunc__gdeax = ', '.join('arrs[{}]._data'.format(i) for i in range(
        xnlmh__mqvbi))
    rnme__ftqz += '  return ({}{})\n'.format(tnunc__gdeax, ',' if 
        xnlmh__mqvbi == 1 else '')
    edwtx__sso = {}
    exec(rnme__ftqz, {}, edwtx__sso)
    impl = edwtx__sso['f']
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def concat_bitmap_tup(arrs):
    xnlmh__mqvbi = len(arrs.types)
    ajwka__iww = '+'.join('len(arrs[{}]._data)'.format(i) for i in range(
        xnlmh__mqvbi))
    rnme__ftqz = 'def f(arrs):\n'
    rnme__ftqz += '  n = {}\n'.format(ajwka__iww)
    rnme__ftqz += '  n_bytes = (n + 7) >> 3\n'
    rnme__ftqz += '  new_mask = np.empty(n_bytes, np.uint8)\n'
    rnme__ftqz += '  curr_bit = 0\n'
    for i in range(xnlmh__mqvbi):
        rnme__ftqz += '  old_mask = arrs[{}]._null_bitmap\n'.format(i)
        rnme__ftqz += '  for j in range(len(arrs[{}])):\n'.format(i)
        rnme__ftqz += (
            '    bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        rnme__ftqz += (
            '    bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        rnme__ftqz += '    curr_bit += 1\n'
    rnme__ftqz += '  return new_mask\n'
    edwtx__sso = {}
    exec(rnme__ftqz, {'np': np, 'bodo': bodo}, edwtx__sso)
    impl = edwtx__sso['f']
    return impl


@overload_method(IntegerArrayType, 'sum', no_unliteral=True)
def overload_int_arr_sum(A, skipna=True, min_count=0):
    higm__gfndh = dict(skipna=skipna, min_count=min_count)
    ytgs__hyz = dict(skipna=True, min_count=0)
    check_unsupported_args('IntegerArray.sum', higm__gfndh, ytgs__hyz)

    def impl(A, skipna=True, min_count=0):
        numba.parfors.parfor.init_prange()
        s = 0
        for i in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, i):
                val = A[i]
            s += val
        return s
    return impl


@overload_method(IntegerArrayType, 'unique', no_unliteral=True)
def overload_unique(A):
    dtype = A.dtype

    def impl_int_arr(A):
        data = []
        llxa__rirdl = []
        sdc__rfiq = False
        s = set()
        for i in range(len(A)):
            val = A[i]
            if bodo.libs.array_kernels.isna(A, i):
                if not sdc__rfiq:
                    data.append(dtype(1))
                    llxa__rirdl.append(False)
                    sdc__rfiq = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                llxa__rirdl.append(True)
        mycdj__pisyi = np.array(data)
        n = len(mycdj__pisyi)
        qxqm__coo = n + 7 >> 3
        kqfho__seaqw = np.empty(qxqm__coo, np.uint8)
        for xojt__yial in range(n):
            set_bit_to_arr(kqfho__seaqw, xojt__yial, llxa__rirdl[xojt__yial])
        return init_integer_array(mycdj__pisyi, kqfho__seaqw)
    return impl_int_arr


def get_nullable_array_unary_impl(op, A):
    buhe__szuvp = numba.core.registry.cpu_target.typing_context
    xkr__sye = buhe__szuvp.resolve_function_type(op, (types.Array(A.dtype, 
        1, 'C'),), {}).return_type
    xkr__sye = to_nullable_type(xkr__sye)

    def impl(A):
        n = len(A)
        ugqf__luwkh = bodo.utils.utils.alloc_type(n, xkr__sye, None)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(ugqf__luwkh, i)
                continue
            ugqf__luwkh[i] = op(A[i])
        return ugqf__luwkh
    return impl


def get_nullable_array_binary_impl(op, lhs, rhs):
    inplace = (op in numba.core.typing.npydecl.
        NumpyRulesInplaceArrayOperator._op_map.keys())
    eqrvu__gnz = isinstance(lhs, (types.Number, types.Boolean))
    ijk__wnmc = isinstance(rhs, (types.Number, types.Boolean))
    yro__hoz = types.Array(getattr(lhs, 'dtype', lhs), 1, 'C')
    zsw__vzsg = types.Array(getattr(rhs, 'dtype', rhs), 1, 'C')
    buhe__szuvp = numba.core.registry.cpu_target.typing_context
    xkr__sye = buhe__szuvp.resolve_function_type(op, (yro__hoz, zsw__vzsg), {}
        ).return_type
    xkr__sye = to_nullable_type(xkr__sye)
    if op in (operator.truediv, operator.itruediv):
        op = np.true_divide
    elif op in (operator.floordiv, operator.ifloordiv):
        op = np.floor_divide
    jtqwh__umvd = 'lhs' if eqrvu__gnz else 'lhs[i]'
    fraqy__uzj = 'rhs' if ijk__wnmc else 'rhs[i]'
    sys__exh = ('False' if eqrvu__gnz else
        'bodo.libs.array_kernels.isna(lhs, i)')
    hchx__ljx = ('False' if ijk__wnmc else
        'bodo.libs.array_kernels.isna(rhs, i)')
    rnme__ftqz = 'def impl(lhs, rhs):\n'
    rnme__ftqz += '  n = len({})\n'.format('lhs' if not eqrvu__gnz else 'rhs')
    if inplace:
        rnme__ftqz += '  out_arr = {}\n'.format('lhs' if not eqrvu__gnz else
            'rhs')
    else:
        rnme__ftqz += (
            '  out_arr = bodo.utils.utils.alloc_type(n, ret_dtype, None)\n')
    rnme__ftqz += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    rnme__ftqz += '    if ({}\n'.format(sys__exh)
    rnme__ftqz += '        or {}):\n'.format(hchx__ljx)
    rnme__ftqz += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    rnme__ftqz += '      continue\n'
    rnme__ftqz += (
        '    out_arr[i] = bodo.utils.conversion.unbox_if_timestamp(op({}, {}))\n'
        .format(jtqwh__umvd, fraqy__uzj))
    rnme__ftqz += '  return out_arr\n'
    edwtx__sso = {}
    exec(rnme__ftqz, {'bodo': bodo, 'numba': numba, 'np': np, 'ret_dtype':
        xkr__sye, 'op': op}, edwtx__sso)
    impl = edwtx__sso['impl']
    return impl


def get_int_array_op_pd_td(op):

    def impl(lhs, rhs):
        eqrvu__gnz = lhs in [pd_timedelta_type]
        ijk__wnmc = rhs in [pd_timedelta_type]
        if eqrvu__gnz:

            def impl(lhs, rhs):
                n = len(rhs)
                ugqf__luwkh = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(ugqf__luwkh, i)
                        continue
                    ugqf__luwkh[i] = bodo.utils.conversion.unbox_if_timestamp(
                        op(lhs, rhs[i]))
                return ugqf__luwkh
            return impl
        elif ijk__wnmc:

            def impl(lhs, rhs):
                n = len(lhs)
                ugqf__luwkh = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(ugqf__luwkh, i)
                        continue
                    ugqf__luwkh[i] = bodo.utils.conversion.unbox_if_timestamp(
                        op(lhs[i], rhs))
                return ugqf__luwkh
            return impl
    return impl
