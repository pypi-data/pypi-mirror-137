"""Nullable boolean array that stores data in Numpy format (1 byte per value)
but nulls are stored in bit arrays (1 bit per value) similar to Arrow's nulls.
Pandas converts boolean array to object when NAs are introduced.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import NativeValue, box, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs import hstr_ext
from bodo.libs.str_arr_ext import string_array_type
from bodo.utils.typing import is_list_like_index_type
ll.add_symbol('is_bool_array', hstr_ext.is_bool_array)
ll.add_symbol('is_pd_boolean_array', hstr_ext.is_pd_boolean_array)
ll.add_symbol('unbox_bool_array_obj', hstr_ext.unbox_bool_array_obj)
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, is_iterable_type, is_overload_false, is_overload_true, parse_dtype, raise_bodo_error


class BooleanArrayType(types.ArrayCompatible):

    def __init__(self):
        super(BooleanArrayType, self).__init__(name='BooleanArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.bool_

    def copy(self):
        return BooleanArrayType()


boolean_array = BooleanArrayType()


@typeof_impl.register(pd.arrays.BooleanArray)
def typeof_boolean_array(val, c):
    return boolean_array


data_type = types.Array(types.bool_, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(BooleanArrayType)
class BooleanArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ptvh__jpv = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, ptvh__jpv)


make_attribute_wrapper(BooleanArrayType, 'data', '_data')
make_attribute_wrapper(BooleanArrayType, 'null_bitmap', '_null_bitmap')


class BooleanDtype(types.Number):

    def __init__(self):
        self.dtype = types.bool_
        super(BooleanDtype, self).__init__('BooleanDtype')


boolean_dtype = BooleanDtype()
register_model(BooleanDtype)(models.OpaqueModel)


@box(BooleanDtype)
def box_boolean_dtype(typ, val, c):
    xpq__xladg = c.context.insert_const_string(c.builder.module, 'pandas')
    sulx__lwkw = c.pyapi.import_module_noblock(xpq__xladg)
    rxf__chgyv = c.pyapi.call_method(sulx__lwkw, 'BooleanDtype', ())
    c.pyapi.decref(sulx__lwkw)
    return rxf__chgyv


@unbox(BooleanDtype)
def unbox_boolean_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.BooleanDtype)(lambda a, b: boolean_dtype)
type_callable(pd.BooleanDtype)(lambda c: lambda : boolean_dtype)
lower_builtin(pd.BooleanDtype)(lambda c, b, s, a: c.get_dummy_value())


@numba.njit
def gen_full_bitmap(n):
    uayjs__seej = n + 7 >> 3
    return np.full(uayjs__seej, 255, np.uint8)


def call_func_in_unbox(func, args, arg_typs, c):
    zmgqr__zbl = c.context.typing_context.resolve_value_type(func)
    mmjn__ndva = zmgqr__zbl.get_call_type(c.context.typing_context,
        arg_typs, {})
    hsym__kvvu = c.context.get_function(zmgqr__zbl, mmjn__ndva)
    nsvk__ohhf = c.context.call_conv.get_function_type(mmjn__ndva.
        return_type, mmjn__ndva.args)
    mpy__kerv = c.builder.module
    lbdey__xxc = lir.Function(mpy__kerv, nsvk__ohhf, name=mpy__kerv.
        get_unique_name('.func_conv'))
    lbdey__xxc.linkage = 'internal'
    ifw__qpojg = lir.IRBuilder(lbdey__xxc.append_basic_block())
    mps__mzm = c.context.call_conv.decode_arguments(ifw__qpojg, mmjn__ndva.
        args, lbdey__xxc)
    tkjx__yacw = hsym__kvvu(ifw__qpojg, mps__mzm)
    c.context.call_conv.return_value(ifw__qpojg, tkjx__yacw)
    bizz__ttlz, mct__jov = c.context.call_conv.call_function(c.builder,
        lbdey__xxc, mmjn__ndva.return_type, mmjn__ndva.args, args)
    return mct__jov


@unbox(BooleanArrayType)
def unbox_bool_array(typ, obj, c):
    ecg__nedu = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(ecg__nedu)
    c.pyapi.decref(ecg__nedu)
    nsvk__ohhf = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    oap__whgf = cgutils.get_or_insert_function(c.builder.module, nsvk__ohhf,
        name='is_bool_array')
    nsvk__ohhf = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    lbdey__xxc = cgutils.get_or_insert_function(c.builder.module,
        nsvk__ohhf, name='is_pd_boolean_array')
    szaj__ppkco = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    loljm__kzjoi = c.builder.call(lbdey__xxc, [obj])
    gwhlq__sgvd = c.builder.icmp_unsigned('!=', loljm__kzjoi, loljm__kzjoi.
        type(0))
    with c.builder.if_else(gwhlq__sgvd) as (pd_then, pd_otherwise):
        with pd_then:
            fmul__dhhuk = c.pyapi.object_getattr_string(obj, '_data')
            szaj__ppkco.data = c.pyapi.to_native_value(types.Array(types.
                bool_, 1, 'C'), fmul__dhhuk).value
            yole__ietxt = c.pyapi.object_getattr_string(obj, '_mask')
            hszyq__zhh = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), yole__ietxt).value
            uayjs__seej = c.builder.udiv(c.builder.add(n, lir.Constant(lir.
                IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
            crhvj__sxe = c.context.make_array(types.Array(types.bool_, 1, 'C')
                )(c.context, c.builder, hszyq__zhh)
            pnhu__kjy = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(types.uint8, 1, 'C'), [uayjs__seej])
            nsvk__ohhf = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            lbdey__xxc = cgutils.get_or_insert_function(c.builder.module,
                nsvk__ohhf, name='mask_arr_to_bitmap')
            c.builder.call(lbdey__xxc, [pnhu__kjy.data, crhvj__sxe.data, n])
            szaj__ppkco.null_bitmap = pnhu__kjy._getvalue()
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), hszyq__zhh)
            c.pyapi.decref(fmul__dhhuk)
            c.pyapi.decref(yole__ietxt)
        with pd_otherwise:
            vlq__ric = c.builder.call(oap__whgf, [obj])
            wsr__lqgk = c.builder.icmp_unsigned('!=', vlq__ric, vlq__ric.
                type(0))
            with c.builder.if_else(wsr__lqgk) as (then, otherwise):
                with then:
                    szaj__ppkco.data = c.pyapi.to_native_value(types.Array(
                        types.bool_, 1, 'C'), obj).value
                    szaj__ppkco.null_bitmap = call_func_in_unbox(
                        gen_full_bitmap, (n,), (types.int64,), c)
                with otherwise:
                    szaj__ppkco.data = bodo.utils.utils._empty_nd_impl(c.
                        context, c.builder, types.Array(types.bool_, 1, 'C'
                        ), [n])._getvalue()
                    uayjs__seej = c.builder.udiv(c.builder.add(n, lir.
                        Constant(lir.IntType(64), 7)), lir.Constant(lir.
                        IntType(64), 8))
                    szaj__ppkco.null_bitmap = bodo.utils.utils._empty_nd_impl(c
                        .context, c.builder, types.Array(types.uint8, 1,
                        'C'), [uayjs__seej])._getvalue()
                    lrdw__puk = c.context.make_array(types.Array(types.
                        bool_, 1, 'C'))(c.context, c.builder, szaj__ppkco.data
                        ).data
                    cnfm__tlivd = c.context.make_array(types.Array(types.
                        uint8, 1, 'C'))(c.context, c.builder, szaj__ppkco.
                        null_bitmap).data
                    nsvk__ohhf = lir.FunctionType(lir.VoidType(), [lir.
                        IntType(8).as_pointer(), lir.IntType(8).as_pointer(
                        ), lir.IntType(8).as_pointer(), lir.IntType(64)])
                    lbdey__xxc = cgutils.get_or_insert_function(c.builder.
                        module, nsvk__ohhf, name='unbox_bool_array_obj')
                    c.builder.call(lbdey__xxc, [obj, lrdw__puk, cnfm__tlivd, n]
                        )
    return NativeValue(szaj__ppkco._getvalue())


@box(BooleanArrayType)
def box_bool_arr(typ, val, c):
    szaj__ppkco = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        szaj__ppkco.data, c.env_manager)
    ndisf__qod = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, szaj__ppkco.null_bitmap).data
    ecg__nedu = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(ecg__nedu)
    xpq__xladg = c.context.insert_const_string(c.builder.module, 'numpy')
    wqmuj__igit = c.pyapi.import_module_noblock(xpq__xladg)
    nou__scq = c.pyapi.object_getattr_string(wqmuj__igit, 'bool_')
    hszyq__zhh = c.pyapi.call_method(wqmuj__igit, 'empty', (ecg__nedu,
        nou__scq))
    mgpjx__nyva = c.pyapi.object_getattr_string(hszyq__zhh, 'ctypes')
    hwb__ajkmv = c.pyapi.object_getattr_string(mgpjx__nyva, 'data')
    vppuw__hocx = c.builder.inttoptr(c.pyapi.long_as_longlong(hwb__ajkmv),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as loop:
        duh__xjj = loop.index
        zvs__wnkj = c.builder.lshr(duh__xjj, lir.Constant(lir.IntType(64), 3))
        wdfg__eim = c.builder.load(cgutils.gep(c.builder, ndisf__qod,
            zvs__wnkj))
        naq__lkdau = c.builder.trunc(c.builder.and_(duh__xjj, lir.Constant(
            lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(wdfg__eim, naq__lkdau), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        hmnrv__iusw = cgutils.gep(c.builder, vppuw__hocx, duh__xjj)
        c.builder.store(val, hmnrv__iusw)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        szaj__ppkco.null_bitmap)
    xpq__xladg = c.context.insert_const_string(c.builder.module, 'pandas')
    sulx__lwkw = c.pyapi.import_module_noblock(xpq__xladg)
    wupz__neuf = c.pyapi.object_getattr_string(sulx__lwkw, 'arrays')
    rxf__chgyv = c.pyapi.call_method(wupz__neuf, 'BooleanArray', (data,
        hszyq__zhh))
    c.pyapi.decref(sulx__lwkw)
    c.pyapi.decref(ecg__nedu)
    c.pyapi.decref(wqmuj__igit)
    c.pyapi.decref(nou__scq)
    c.pyapi.decref(mgpjx__nyva)
    c.pyapi.decref(hwb__ajkmv)
    c.pyapi.decref(wupz__neuf)
    c.pyapi.decref(data)
    c.pyapi.decref(hszyq__zhh)
    return rxf__chgyv


@lower_constant(BooleanArrayType)
def lower_constant_bool_arr(context, builder, typ, pyval):
    n = len(pyval)
    ngzsl__slzc = np.empty(n, np.bool_)
    aqxh__pwog = np.empty(n + 7 >> 3, np.uint8)
    for duh__xjj, s in enumerate(pyval):
        zyfz__xafey = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(aqxh__pwog, duh__xjj, int(not
            zyfz__xafey))
        if not zyfz__xafey:
            ngzsl__slzc[duh__xjj] = s
    pqp__uebb = context.get_constant_generic(builder, data_type, ngzsl__slzc)
    saqzm__dfnwd = context.get_constant_generic(builder, nulls_type, aqxh__pwog
        )
    return lir.Constant.literal_struct([pqp__uebb, saqzm__dfnwd])


def lower_init_bool_array(context, builder, signature, args):
    pmup__axta, yav__oqtk = args
    szaj__ppkco = cgutils.create_struct_proxy(signature.return_type)(context,
        builder)
    szaj__ppkco.data = pmup__axta
    szaj__ppkco.null_bitmap = yav__oqtk
    context.nrt.incref(builder, signature.args[0], pmup__axta)
    context.nrt.incref(builder, signature.args[1], yav__oqtk)
    return szaj__ppkco._getvalue()


@intrinsic
def init_bool_array(typingctx, data, null_bitmap=None):
    assert data == types.Array(types.bool_, 1, 'C')
    assert null_bitmap == types.Array(types.uint8, 1, 'C')
    sig = boolean_array(data, null_bitmap)
    return sig, lower_init_bool_array


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_bool_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_bool_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_bool_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    dzhto__rmuw = args[0]
    if equiv_set.has_shape(dzhto__rmuw):
        return ArrayAnalysis.AnalyzeResult(shape=dzhto__rmuw, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_get_bool_arr_data = (
    get_bool_arr_data_equiv)


def init_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    dzhto__rmuw = args[0]
    if equiv_set.has_shape(dzhto__rmuw):
        return ArrayAnalysis.AnalyzeResult(shape=dzhto__rmuw, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_init_bool_array = (
    init_bool_array_equiv)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


def alias_ext_init_bool_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_bool_array',
    'bodo.libs.bool_arr_ext'] = alias_ext_init_bool_array
numba.core.ir_utils.alias_func_extensions['get_bool_arr_data',
    'bodo.libs.bool_arr_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_bool_arr_bitmap',
    'bodo.libs.bool_arr_ext'] = alias_ext_dummy_func


@numba.njit(no_cpython_wrapper=True)
def alloc_bool_array(n):
    ngzsl__slzc = np.empty(n, dtype=np.bool_)
    dme__qkd = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_bool_array(ngzsl__slzc, dme__qkd)


def alloc_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_alloc_bool_array = (
    alloc_bool_array_equiv)


@overload(operator.getitem, no_unliteral=True)
def bool_arr_getitem(A, ind):
    if A != boolean_array:
        return
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda A, ind: A._data[ind]
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            pwsa__vftjy, oeeo__gpz = array_getitem_bool_index(A, ind)
            return init_bool_array(pwsa__vftjy, oeeo__gpz)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            pwsa__vftjy, oeeo__gpz = array_getitem_int_index(A, ind)
            return init_bool_array(pwsa__vftjy, oeeo__gpz)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            pwsa__vftjy, oeeo__gpz = array_getitem_slice_index(A, ind)
            return init_bool_array(pwsa__vftjy, oeeo__gpz)
        return impl_slice
    raise BodoError(
        f'getitem for BooleanArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def bool_arr_setitem(A, idx, val):
    if A != boolean_array:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    kvjw__cmdb = (
        f"setitem for BooleanArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == types.bool_:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(kvjw__cmdb)
    if not (is_iterable_type(val) and val.dtype == types.bool_ or types.
        unliteral(val) == types.bool_):
        raise BodoError(kvjw__cmdb)
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
        f'setitem for BooleanArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_bool_arr_len(A):
    if A == boolean_array:
        return lambda A: len(A._data)


@overload_attribute(BooleanArrayType, 'shape')
def overload_bool_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(BooleanArrayType, 'dtype')
def overload_bool_arr_dtype(A):
    return lambda A: pd.BooleanDtype()


@overload_attribute(BooleanArrayType, 'ndim')
def overload_bool_arr_ndim(A):
    return lambda A: 1


@overload_attribute(BooleanArrayType, 'nbytes')
def bool_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


@overload_method(BooleanArrayType, 'copy', no_unliteral=True)
def overload_bool_arr_copy(A):
    return lambda A: bodo.libs.bool_arr_ext.init_bool_array(bodo.libs.
        bool_arr_ext.get_bool_arr_data(A).copy(), bodo.libs.bool_arr_ext.
        get_bool_arr_bitmap(A).copy())


@overload_method(BooleanArrayType, 'sum', no_unliteral=True, inline='always')
def overload_bool_sum(A):

    def impl(A):
        numba.parfors.parfor.init_prange()
        s = 0
        for duh__xjj in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, duh__xjj):
                val = A[duh__xjj]
            s += val
        return s
    return impl


@overload_method(BooleanArrayType, 'astype', no_unliteral=True)
def overload_bool_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "BooleanArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if dtype == types.bool_:
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
    nb_dtype = parse_dtype(dtype, 'BooleanArray.astype')
    if isinstance(nb_dtype, types.Float):

        def impl_float(A, dtype, copy=True):
            data = bodo.libs.bool_arr_ext.get_bool_arr_data(A)
            n = len(data)
            ccrp__gllx = np.empty(n, nb_dtype)
            for duh__xjj in numba.parfors.parfor.internal_prange(n):
                ccrp__gllx[duh__xjj] = data[duh__xjj]
                if bodo.libs.array_kernels.isna(A, duh__xjj):
                    ccrp__gllx[duh__xjj] = np.nan
            return ccrp__gllx
        return impl_float
    return (lambda A, dtype, copy=True: bodo.libs.bool_arr_ext.
        get_bool_arr_data(A).astype(nb_dtype))


@overload(str, no_unliteral=True)
def overload_str_bool(val):
    if val == types.bool_:

        def impl(val):
            if val:
                return 'True'
            return 'False'
        return impl


ufunc_aliases = {'equal': 'eq', 'not_equal': 'ne', 'less': 'lt',
    'less_equal': 'le', 'greater': 'gt', 'greater_equal': 'ge'}


def create_op_overload(op, n_inputs):
    jvbyv__ktz = op.__name__
    jvbyv__ktz = ufunc_aliases.get(jvbyv__ktz, jvbyv__ktz)
    if n_inputs == 1:

        def overload_bool_arr_op_nin_1(A):
            if isinstance(A, BooleanArrayType):
                return bodo.libs.int_arr_ext.get_nullable_array_unary_impl(op,
                    A)
        return overload_bool_arr_op_nin_1
    elif n_inputs == 2:

        def overload_bool_arr_op_nin_2(lhs, rhs):
            if lhs == boolean_array or rhs == boolean_array:
                return bodo.libs.int_arr_ext.get_nullable_array_binary_impl(op,
                    lhs, rhs)
        return overload_bool_arr_op_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for rqp__pzaja in numba.np.ufunc_db.get_ufuncs():
        ffb__kpxah = create_op_overload(rqp__pzaja, rqp__pzaja.nin)
        overload(rqp__pzaja, no_unliteral=True)(ffb__kpxah)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod, operator.or_, operator.and_]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        ffb__kpxah = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(ffb__kpxah)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        ffb__kpxah = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(ffb__kpxah)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        ffb__kpxah = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(ffb__kpxah)


_install_unary_ops()


@overload_method(BooleanArrayType, 'unique', no_unliteral=True)
def overload_unique(A):

    def impl_bool_arr(A):
        data = []
        naq__lkdau = []
        pflel__dmv = False
        ghaf__lno = False
        lice__wnsic = False
        for duh__xjj in range(len(A)):
            if bodo.libs.array_kernels.isna(A, duh__xjj):
                if not pflel__dmv:
                    data.append(False)
                    naq__lkdau.append(False)
                    pflel__dmv = True
                continue
            val = A[duh__xjj]
            if val and not ghaf__lno:
                data.append(True)
                naq__lkdau.append(True)
                ghaf__lno = True
            if not val and not lice__wnsic:
                data.append(False)
                naq__lkdau.append(True)
                lice__wnsic = True
            if pflel__dmv and ghaf__lno and lice__wnsic:
                break
        pwsa__vftjy = np.array(data)
        n = len(pwsa__vftjy)
        uayjs__seej = 1
        oeeo__gpz = np.empty(uayjs__seej, np.uint8)
        for kvbtg__ekhk in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(oeeo__gpz, kvbtg__ekhk,
                naq__lkdau[kvbtg__ekhk])
        return init_bool_array(pwsa__vftjy, oeeo__gpz)
    return impl_bool_arr


@overload(operator.getitem, no_unliteral=True)
def bool_arr_ind_getitem(A, ind):
    if ind == boolean_array and (isinstance(A, (types.Array, bodo.libs.
        int_arr_ext.IntegerArrayType)) or isinstance(A, bodo.libs.
        struct_arr_ext.StructArrayType) or isinstance(A, bodo.libs.
        array_item_arr_ext.ArrayItemArrayType) or isinstance(A, bodo.libs.
        map_arr_ext.MapArrayType) or A in (string_array_type, bodo.hiframes
        .split_impl.string_array_split_view_type, boolean_array)):
        return lambda A, ind: A[ind._data]


@lower_cast(types.Array(types.bool_, 1, 'C'), boolean_array)
def cast_np_bool_arr_to_bool_arr(context, builder, fromty, toty, val):
    func = lambda A: bodo.libs.bool_arr_ext.init_bool_array(A, np.full(len(
        A) + 7 >> 3, 255, np.uint8))
    rxf__chgyv = context.compile_internal(builder, func, toty(fromty), [val])
    return impl_ret_borrowed(context, builder, toty, rxf__chgyv)


@overload(operator.setitem, no_unliteral=True)
def overload_np_array_setitem_bool_arr(A, idx, val):
    if isinstance(A, types.Array) and idx == boolean_array:

        def impl(A, idx, val):
            A[idx._data] = val
        return impl


def create_nullable_logical_op_overload(op):
    hbgie__mth = op == operator.or_

    def bool_array_impl(val1, val2):
        if not is_valid_boolean_array_logical_op(val1, val2):
            return
        bxcy__hosbr = bodo.utils.utils.is_array_typ(val1, False)
        simac__arxn = bodo.utils.utils.is_array_typ(val2, False)
        ebhv__pvlde = 'val1' if bxcy__hosbr else 'val2'
        elxdw__eilkh = 'def impl(val1, val2):\n'
        elxdw__eilkh += f'  n = len({ebhv__pvlde})\n'
        elxdw__eilkh += (
            '  out_arr = bodo.utils.utils.alloc_type(n, bodo.boolean_array, (-1,))\n'
            )
        elxdw__eilkh += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if bxcy__hosbr:
            null1 = 'bodo.libs.array_kernels.isna(val1, i)\n'
            qne__nms = 'val1[i]'
        else:
            null1 = 'False\n'
            qne__nms = 'val1'
        if simac__arxn:
            null2 = 'bodo.libs.array_kernels.isna(val2, i)\n'
            ren__nzck = 'val2[i]'
        else:
            null2 = 'False\n'
            ren__nzck = 'val2'
        if hbgie__mth:
            elxdw__eilkh += f"""    result, isna_val = compute_or_body({null1}, {null2}, {qne__nms}, {ren__nzck})
"""
        else:
            elxdw__eilkh += f"""    result, isna_val = compute_and_body({null1}, {null2}, {qne__nms}, {ren__nzck})
"""
        elxdw__eilkh += '    out_arr[i] = result\n'
        elxdw__eilkh += '    if isna_val:\n'
        elxdw__eilkh += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        elxdw__eilkh += '      continue\n'
        elxdw__eilkh += '  return out_arr\n'
        tasp__nuc = {}
        exec(elxdw__eilkh, {'bodo': bodo, 'numba': numba,
            'compute_and_body': compute_and_body, 'compute_or_body':
            compute_or_body}, tasp__nuc)
        impl = tasp__nuc['impl']
        return impl
    return bool_array_impl


def compute_or_body(null1, null2, val1, val2):
    pass


@overload(compute_or_body)
def overload_compute_or_body(null1, null2, val1, val2):

    def impl(null1, null2, val1, val2):
        if null1 and null2:
            return False, True
        elif null1:
            return val2, val2 == False
        elif null2:
            return val1, val1 == False
        else:
            return val1 | val2, False
    return impl


def compute_and_body(null1, null2, val1, val2):
    pass


@overload(compute_and_body)
def overload_compute_and_body(null1, null2, val1, val2):

    def impl(null1, null2, val1, val2):
        if null1 and null2:
            return False, True
        elif null1:
            return val2, val2 == True
        elif null2:
            return val1, val1 == True
        else:
            return val1 & val2, False
    return impl


def create_boolean_array_logical_lower_impl(op):

    def logical_lower_impl(context, builder, sig, args):
        impl = create_nullable_logical_op_overload(op)(*sig.args)
        return context.compile_internal(builder, impl, sig, args)
    return logical_lower_impl


class BooleanArrayLogicalOperatorTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        if not is_valid_boolean_array_logical_op(args[0], args[1]):
            return
        cybx__xjyxr = boolean_array
        return cybx__xjyxr(*args)


def is_valid_boolean_array_logical_op(typ1, typ2):
    uez__npler = (typ1 == bodo.boolean_array or typ2 == bodo.boolean_array
        ) and (bodo.utils.utils.is_array_typ(typ1, False) and typ1.dtype ==
        types.bool_ or typ1 == types.bool_) and (bodo.utils.utils.
        is_array_typ(typ2, False) and typ2.dtype == types.bool_ or typ2 ==
        types.bool_)
    return uez__npler


def _install_nullable_logical_lowering():
    for op in (operator.and_, operator.or_):
        gftxt__geh = create_boolean_array_logical_lower_impl(op)
        infer_global(op)(BooleanArrayLogicalOperatorTemplate)
        for typ1, typ2 in [(boolean_array, boolean_array), (boolean_array,
            types.bool_), (boolean_array, types.Array(types.bool_, 1, 'C'))]:
            lower_builtin(op, typ1, typ2)(gftxt__geh)
            if typ1 != typ2:
                lower_builtin(op, typ2, typ1)(gftxt__geh)


_install_nullable_logical_lowering()
