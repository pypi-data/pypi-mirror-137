"""Array implementation for string objects, which are usually immutable.
The characters are stored in a contingous data array, and an offsets array marks the
the individual strings. For example:
value:             ['a', 'bc', '', 'abc', None, 'bb']
data:              [a, b, c, a, b, c, b, b]
offsets:           [0, 1, 3, 3, 6, 6, 8]
"""
import glob
import operator
import llvmlite.llvmpy.core as lc
import numba
import numba.core.typing.typeof
import numpy as np
import pandas as pd
from numba.core import cgutils, types
from numba.core.imputils import RefType, impl_ret_borrowed, iternext_impl, lower_constant
from numba.core.typing.templates import signature
from numba.core.unsafe.bytes import memcpy_region
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, type_callable, typeof_impl, unbox
import bodo
from bodo.libs.array_item_arr_ext import ArrayItemArrayPayloadType, ArrayItemArrayType, _get_array_item_arr_payload, np_offset_type, offset_type
from bodo.libs.binary_arr_ext import BinaryArrayType, binary_array_type, pre_alloc_binary_array
from bodo.libs.str_ext import memcmp, string_type, unicode_to_utf8_and_len
from bodo.utils.typing import BodoError, is_list_like_index_type, is_overload_constant_int, is_overload_none, is_overload_true, parse_dtype, raise_bodo_error
use_pd_string_array = False
char_type = types.uint8
char_arr_type = types.Array(char_type, 1, 'C')
offset_arr_type = types.Array(offset_type, 1, 'C')
null_bitmap_arr_type = types.Array(types.uint8, 1, 'C')
data_ctypes_type = types.ArrayCTypes(char_arr_type)
offset_ctypes_type = types.ArrayCTypes(offset_arr_type)


class StringArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self):
        super(StringArrayType, self).__init__(name='StringArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_type

    @property
    def iterator_type(self):
        return StringArrayIterator()

    def copy(self):
        return StringArrayType()


string_array_type = StringArrayType()


@typeof_impl.register(pd.arrays.StringArray)
def typeof_string_array(val, c):
    return string_array_type


@register_model(BinaryArrayType)
@register_model(StringArrayType)
class StringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        iyedw__gthmc = ArrayItemArrayType(char_arr_type)
        cqan__rph = [('data', iyedw__gthmc)]
        models.StructModel.__init__(self, dmm, fe_type, cqan__rph)


make_attribute_wrapper(StringArrayType, 'data', '_data')
make_attribute_wrapper(BinaryArrayType, 'data', '_data')


@intrinsic
def init_str_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(char_type, 1, 'C')

    def codegen(context, builder, sig, args):
        uxe__pcxz, = args
        rdo__alub = context.make_helper(builder, string_array_type)
        rdo__alub.data = uxe__pcxz
        context.nrt.incref(builder, data_typ, uxe__pcxz)
        return rdo__alub._getvalue()
    return string_array_type(data_typ), codegen


class StringDtype(types.Number):

    def __init__(self):
        super(StringDtype, self).__init__('StringDtype')


string_dtype = StringDtype()
register_model(StringDtype)(models.OpaqueModel)


@box(StringDtype)
def box_string_dtype(typ, val, c):
    iyy__afn = c.context.insert_const_string(c.builder.module, 'pandas')
    xtcl__drgv = c.pyapi.import_module_noblock(iyy__afn)
    gzmgh__cwu = c.pyapi.call_method(xtcl__drgv, 'StringDtype', ())
    c.pyapi.decref(xtcl__drgv)
    return gzmgh__cwu


@unbox(StringDtype)
def unbox_string_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.StringDtype)(lambda a, b: string_dtype)
type_callable(pd.StringDtype)(lambda c: lambda : string_dtype)
lower_builtin(pd.StringDtype)(lambda c, b, s, a: c.get_dummy_value())


def create_binary_op_overload(op):

    def overload_string_array_binary_op(lhs, rhs):
        if lhs == string_array_type and rhs == string_array_type:

            def impl_both(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pcd__gsd = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(pcd__gsd)
                for i in numba.parfors.parfor.internal_prange(pcd__gsd):
                    if bodo.libs.array_kernels.isna(lhs, i
                        ) or bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs[i], rhs[i])
                    out_arr[i] = val
                return out_arr
            return impl_both
        if lhs == string_array_type and types.unliteral(rhs) == string_type:

            def impl_left(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pcd__gsd = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(pcd__gsd)
                for i in numba.parfors.parfor.internal_prange(pcd__gsd):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs[i], rhs)
                    out_arr[i] = val
                return out_arr
            return impl_left
        if types.unliteral(lhs) == string_type and rhs == string_array_type:

            def impl_right(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pcd__gsd = len(rhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(pcd__gsd)
                for i in numba.parfors.parfor.internal_prange(pcd__gsd):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs, rhs[i])
                    out_arr[i] = val
                return out_arr
            return impl_right
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_string_array_binary_op


def overload_add_operator_string_array(lhs, rhs):
    obp__cqen = lhs == string_array_type or isinstance(lhs, types.Array
        ) and lhs.dtype == string_type
    lkp__srm = rhs == string_array_type or isinstance(rhs, types.Array
        ) and rhs.dtype == string_type
    if (lhs == string_array_type and lkp__srm or obp__cqen and rhs ==
        string_array_type):

        def impl_both(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for yyzz__yir in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, yyzz__yir
                    ) or bodo.libs.array_kernels.isna(rhs, yyzz__yir):
                    out_arr[yyzz__yir] = ''
                    bodo.libs.array_kernels.setna(out_arr, yyzz__yir)
                else:
                    out_arr[yyzz__yir] = lhs[yyzz__yir] + rhs[yyzz__yir]
            return out_arr
        return impl_both
    if lhs == string_array_type and types.unliteral(rhs) == string_type:

        def impl_left(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for yyzz__yir in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, yyzz__yir):
                    out_arr[yyzz__yir] = ''
                    bodo.libs.array_kernels.setna(out_arr, yyzz__yir)
                else:
                    out_arr[yyzz__yir] = lhs[yyzz__yir] + rhs
            return out_arr
        return impl_left
    if types.unliteral(lhs) == string_type and rhs == string_array_type:

        def impl_right(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(rhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for yyzz__yir in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(rhs, yyzz__yir):
                    out_arr[yyzz__yir] = ''
                    bodo.libs.array_kernels.setna(out_arr, yyzz__yir)
                else:
                    out_arr[yyzz__yir] = lhs + rhs[yyzz__yir]
            return out_arr
        return impl_right


def overload_mul_operator_str_arr(lhs, rhs):
    if lhs == string_array_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for yyzz__yir in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, yyzz__yir):
                    out_arr[yyzz__yir] = ''
                    bodo.libs.array_kernels.setna(out_arr, yyzz__yir)
                else:
                    out_arr[yyzz__yir] = lhs[yyzz__yir] * rhs
            return out_arr
        return impl
    if isinstance(lhs, types.Integer) and rhs == string_array_type:

        def impl(lhs, rhs):
            return rhs * lhs
        return impl


class StringArrayIterator(types.SimpleIteratorType):

    def __init__(self):
        bvm__aajwl = 'iter(String)'
        wjsk__dzc = string_type
        super(StringArrayIterator, self).__init__(bvm__aajwl, wjsk__dzc)


@register_model(StringArrayIterator)
class StrArrayIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        cqan__rph = [('index', types.EphemeralPointer(types.uintp)), (
            'array', string_array_type)]
        super(StrArrayIteratorModel, self).__init__(dmm, fe_type, cqan__rph)


lower_builtin('getiter', string_array_type)(numba.np.arrayobj.getiter_array)


@lower_builtin('iternext', StringArrayIterator)
@iternext_impl(RefType.NEW)
def iternext_str_array(context, builder, sig, args, result):
    [eeg__dce] = sig.args
    [ucdo__pcnqg] = args
    ladlb__myzxf = context.make_helper(builder, eeg__dce, value=ucdo__pcnqg)
    iwtw__suz = signature(types.intp, string_array_type)
    kxq__vzx = context.compile_internal(builder, lambda a: len(a),
        iwtw__suz, [ladlb__myzxf.array])
    dthkr__hwsc = builder.load(ladlb__myzxf.index)
    woq__egn = builder.icmp(lc.ICMP_SLT, dthkr__hwsc, kxq__vzx)
    result.set_valid(woq__egn)
    with builder.if_then(woq__egn):
        fhoe__jfjmb = signature(string_type, string_array_type, types.intp)
        value = context.compile_internal(builder, lambda a, i: a[i],
            fhoe__jfjmb, [ladlb__myzxf.array, dthkr__hwsc])
        result.yield_(value)
        ktm__kmh = cgutils.increment_index(builder, dthkr__hwsc)
        builder.store(ktm__kmh, ladlb__myzxf.index)


def _get_str_binary_arr_payload(context, builder, arr_value, arr_typ):
    assert arr_typ == string_array_type or arr_typ == binary_array_type
    rmo__ceypf = context.make_helper(builder, arr_typ, arr_value)
    iyedw__gthmc = ArrayItemArrayType(char_arr_type)
    kpuny__bzrmp = _get_array_item_arr_payload(context, builder,
        iyedw__gthmc, rmo__ceypf.data)
    return kpuny__bzrmp


@intrinsic
def num_strings(typingctx, str_arr_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        kpuny__bzrmp = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        return kpuny__bzrmp.n_arrays
    return types.int64(string_array_type), codegen


def _get_num_total_chars(builder, offsets, num_strings):
    return builder.zext(builder.load(builder.gep(offsets, [num_strings])),
        lir.IntType(64))


@intrinsic
def num_total_chars(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        kpuny__bzrmp = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        pdruj__beo = context.make_helper(builder, offset_arr_type,
            kpuny__bzrmp.offsets).data
        return _get_num_total_chars(builder, pdruj__beo, kpuny__bzrmp.n_arrays)
    return types.uint64(in_arr_typ), codegen


@intrinsic
def get_offset_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        kpuny__bzrmp = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        rycs__rjqbx = context.make_helper(builder, offset_arr_type,
            kpuny__bzrmp.offsets)
        qmz__mtih = context.make_helper(builder, offset_ctypes_type)
        qmz__mtih.data = builder.bitcast(rycs__rjqbx.data, lir.IntType(
            offset_type.bitwidth).as_pointer())
        qmz__mtih.meminfo = rycs__rjqbx.meminfo
        gzmgh__cwu = qmz__mtih._getvalue()
        return impl_ret_borrowed(context, builder, offset_ctypes_type,
            gzmgh__cwu)
    return offset_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        kpuny__bzrmp = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        uxe__pcxz = context.make_helper(builder, char_arr_type,
            kpuny__bzrmp.data)
        qmz__mtih = context.make_helper(builder, data_ctypes_type)
        qmz__mtih.data = uxe__pcxz.data
        qmz__mtih.meminfo = uxe__pcxz.meminfo
        gzmgh__cwu = qmz__mtih._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, gzmgh__cwu
            )
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr_ind(typingctx, in_arr_typ, int_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        uga__vdlbo, ind = args
        kpuny__bzrmp = _get_str_binary_arr_payload(context, builder,
            uga__vdlbo, sig.args[0])
        uxe__pcxz = context.make_helper(builder, char_arr_type,
            kpuny__bzrmp.data)
        qmz__mtih = context.make_helper(builder, data_ctypes_type)
        qmz__mtih.data = builder.gep(uxe__pcxz.data, [ind])
        qmz__mtih.meminfo = uxe__pcxz.meminfo
        gzmgh__cwu = qmz__mtih._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, gzmgh__cwu
            )
    return data_ctypes_type(in_arr_typ, types.intp), codegen


@intrinsic
def copy_single_char(typingctx, dst_ptr_t, dst_ind_t, src_ptr_t, src_ind_t=None
    ):

    def codegen(context, builder, sig, args):
        qcm__bmxe, qntpy__tksiq, zvpqb__bbnyi, nosy__nnmci = args
        uisr__hyst = builder.bitcast(builder.gep(qcm__bmxe, [qntpy__tksiq]),
            lir.IntType(8).as_pointer())
        oxts__nhb = builder.bitcast(builder.gep(zvpqb__bbnyi, [nosy__nnmci]
            ), lir.IntType(8).as_pointer())
        kfwd__djg = builder.load(oxts__nhb)
        builder.store(kfwd__djg, uisr__hyst)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@intrinsic
def get_null_bitmap_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        kpuny__bzrmp = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        lri__dmmd = context.make_helper(builder, null_bitmap_arr_type,
            kpuny__bzrmp.null_bitmap)
        qmz__mtih = context.make_helper(builder, data_ctypes_type)
        qmz__mtih.data = lri__dmmd.data
        qmz__mtih.meminfo = lri__dmmd.meminfo
        gzmgh__cwu = qmz__mtih._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, gzmgh__cwu
            )
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def getitem_str_offset(typingctx, in_arr_typ, ind_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        kpuny__bzrmp = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        pdruj__beo = context.make_helper(builder, offset_arr_type,
            kpuny__bzrmp.offsets).data
        return builder.load(builder.gep(pdruj__beo, [ind]))
    return offset_type(in_arr_typ, ind_t), codegen


@intrinsic
def setitem_str_offset(typingctx, str_arr_typ, ind_t, val_t=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind, val = args
        kpuny__bzrmp = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        offsets = context.make_helper(builder, offset_arr_type,
            kpuny__bzrmp.offsets).data
        builder.store(val, builder.gep(offsets, [ind]))
        return context.get_dummy_value()
    return types.void(string_array_type, ind_t, offset_type), codegen


@intrinsic
def getitem_str_bitmap(typingctx, in_bitmap_typ, ind_t=None):

    def codegen(context, builder, sig, args):
        vuvm__gpkw, ind = args
        if in_bitmap_typ == data_ctypes_type:
            qmz__mtih = context.make_helper(builder, data_ctypes_type,
                vuvm__gpkw)
            vuvm__gpkw = qmz__mtih.data
        return builder.load(builder.gep(vuvm__gpkw, [ind]))
    return char_type(in_bitmap_typ, ind_t), codegen


@intrinsic
def setitem_str_bitmap(typingctx, in_bitmap_typ, ind_t, val_t=None):

    def codegen(context, builder, sig, args):
        vuvm__gpkw, ind, val = args
        if in_bitmap_typ == data_ctypes_type:
            qmz__mtih = context.make_helper(builder, data_ctypes_type,
                vuvm__gpkw)
            vuvm__gpkw = qmz__mtih.data
        builder.store(val, builder.gep(vuvm__gpkw, [ind]))
        return context.get_dummy_value()
    return types.void(in_bitmap_typ, ind_t, char_type), codegen


@intrinsic
def copy_str_arr_slice(typingctx, out_str_arr_typ, in_str_arr_typ, ind_t=None):
    assert out_str_arr_typ == string_array_type and in_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr, ind = args
        lvp__gkvtl = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        ewum__rai = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        sxvec__ntlan = context.make_helper(builder, offset_arr_type,
            lvp__gkvtl.offsets).data
        sths__myd = context.make_helper(builder, offset_arr_type, ewum__rai
            .offsets).data
        lxitl__meua = context.make_helper(builder, char_arr_type,
            lvp__gkvtl.data).data
        oxwa__svdc = context.make_helper(builder, char_arr_type, ewum__rai.data
            ).data
        ettos__yhrj = context.make_helper(builder, null_bitmap_arr_type,
            lvp__gkvtl.null_bitmap).data
        svbsi__ddclw = context.make_helper(builder, null_bitmap_arr_type,
            ewum__rai.null_bitmap).data
        ucft__rxyb = builder.add(ind, context.get_constant(types.intp, 1))
        cgutils.memcpy(builder, sths__myd, sxvec__ntlan, ucft__rxyb)
        cgutils.memcpy(builder, oxwa__svdc, lxitl__meua, builder.load(
            builder.gep(sxvec__ntlan, [ind])))
        cabek__ebrwz = builder.add(ind, lir.Constant(lir.IntType(64), 7))
        mhzh__zmx = builder.lshr(cabek__ebrwz, lir.Constant(lir.IntType(64), 3)
            )
        cgutils.memcpy(builder, svbsi__ddclw, ettos__yhrj, mhzh__zmx)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type, ind_t), codegen


@intrinsic
def copy_data(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        lvp__gkvtl = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        ewum__rai = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        sxvec__ntlan = context.make_helper(builder, offset_arr_type,
            lvp__gkvtl.offsets).data
        lxitl__meua = context.make_helper(builder, char_arr_type,
            lvp__gkvtl.data).data
        oxwa__svdc = context.make_helper(builder, char_arr_type, ewum__rai.data
            ).data
        num_total_chars = _get_num_total_chars(builder, sxvec__ntlan,
            lvp__gkvtl.n_arrays)
        cgutils.memcpy(builder, oxwa__svdc, lxitl__meua, num_total_chars)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def copy_non_null_offsets(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        lvp__gkvtl = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        ewum__rai = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        sxvec__ntlan = context.make_helper(builder, offset_arr_type,
            lvp__gkvtl.offsets).data
        sths__myd = context.make_helper(builder, offset_arr_type, ewum__rai
            .offsets).data
        ettos__yhrj = context.make_helper(builder, null_bitmap_arr_type,
            lvp__gkvtl.null_bitmap).data
        pcd__gsd = lvp__gkvtl.n_arrays
        ybfw__mcavq = context.get_constant(offset_type, 0)
        qgdxt__yum = cgutils.alloca_once_value(builder, ybfw__mcavq)
        with cgutils.for_range(builder, pcd__gsd) as loop:
            hpdkf__dcu = lower_is_na(context, builder, ettos__yhrj, loop.index)
            with cgutils.if_likely(builder, builder.not_(hpdkf__dcu)):
                oibnd__bpepf = builder.load(builder.gep(sxvec__ntlan, [loop
                    .index]))
                pleup__gbzs = builder.load(qgdxt__yum)
                builder.store(oibnd__bpepf, builder.gep(sths__myd, [
                    pleup__gbzs]))
                builder.store(builder.add(pleup__gbzs, lir.Constant(context
                    .get_value_type(offset_type), 1)), qgdxt__yum)
        pleup__gbzs = builder.load(qgdxt__yum)
        oibnd__bpepf = builder.load(builder.gep(sxvec__ntlan, [pcd__gsd]))
        builder.store(oibnd__bpepf, builder.gep(sths__myd, [pleup__gbzs]))
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def str_copy(typingctx, buff_arr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        rpyzs__thtgc, ind, str, ido__cet = args
        rpyzs__thtgc = context.make_array(sig.args[0])(context, builder,
            rpyzs__thtgc)
        oehk__taad = builder.gep(rpyzs__thtgc.data, [ind])
        cgutils.raw_memcpy(builder, oehk__taad, str, ido__cet, 1)
        return context.get_dummy_value()
    return types.void(null_bitmap_arr_type, types.intp, types.voidptr,
        types.intp), codegen


@intrinsic
def str_copy_ptr(typingctx, ptr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        oehk__taad, ind, vtydc__fqufv, ido__cet = args
        oehk__taad = builder.gep(oehk__taad, [ind])
        cgutils.raw_memcpy(builder, oehk__taad, vtydc__fqufv, ido__cet, 1)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_length(A, i):
    return np.int64(getitem_str_offset(A, i + 1) - getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_ptr(A, i):
    return get_data_ptr_ind(A, getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_null_bools(str_arr):
    pcd__gsd = len(str_arr)
    ykre__udpib = np.empty(pcd__gsd, np.bool_)
    for i in range(pcd__gsd):
        ykre__udpib[i] = bodo.libs.array_kernels.isna(str_arr, i)
    return ykre__udpib


def to_list_if_immutable_arr(arr, str_null_bools=None):
    return arr


@overload(to_list_if_immutable_arr, no_unliteral=True)
def to_list_if_immutable_arr_overload(data, str_null_bools=None):
    if data in [string_array_type, binary_array_type]:

        def to_list_impl(data, str_null_bools=None):
            pcd__gsd = len(data)
            l = []
            for i in range(pcd__gsd):
                l.append(data[i])
            return l
        return to_list_impl
    if isinstance(data, types.BaseTuple):
        mzhfs__suprs = data.count
        jdvw__goxyq = ['to_list_if_immutable_arr(data[{}])'.format(i) for i in
            range(mzhfs__suprs)]
        if is_overload_true(str_null_bools):
            jdvw__goxyq += ['get_str_null_bools(data[{}])'.format(i) for i in
                range(mzhfs__suprs) if data.types[i] in [string_array_type,
                binary_array_type]]
        rebbe__zfe = 'def f(data, str_null_bools=None):\n'
        rebbe__zfe += '  return ({}{})\n'.format(', '.join(jdvw__goxyq), 
            ',' if mzhfs__suprs == 1 else '')
        toky__qtb = {}
        exec(rebbe__zfe, {'to_list_if_immutable_arr':
            to_list_if_immutable_arr, 'get_str_null_bools':
            get_str_null_bools, 'bodo': bodo}, toky__qtb)
        nzt__jasby = toky__qtb['f']
        return nzt__jasby
    return lambda data, str_null_bools=None: data


def cp_str_list_to_array(str_arr, str_list, str_null_bools=None):
    return


@overload(cp_str_list_to_array, no_unliteral=True)
def cp_str_list_to_array_overload(str_arr, list_data, str_null_bools=None):
    if str_arr == string_array_type:
        if is_overload_none(str_null_bools):

            def cp_str_list_impl(str_arr, list_data, str_null_bools=None):
                pcd__gsd = len(list_data)
                for i in range(pcd__gsd):
                    vtydc__fqufv = list_data[i]
                    str_arr[i] = vtydc__fqufv
            return cp_str_list_impl
        else:

            def cp_str_list_impl_null(str_arr, list_data, str_null_bools=None):
                pcd__gsd = len(list_data)
                for i in range(pcd__gsd):
                    vtydc__fqufv = list_data[i]
                    str_arr[i] = vtydc__fqufv
                    if str_null_bools[i]:
                        str_arr_set_na(str_arr, i)
                    else:
                        str_arr_set_not_na(str_arr, i)
            return cp_str_list_impl_null
    if isinstance(str_arr, types.BaseTuple):
        mzhfs__suprs = str_arr.count
        ooyy__fxoh = 0
        rebbe__zfe = 'def f(str_arr, list_data, str_null_bools=None):\n'
        for i in range(mzhfs__suprs):
            if is_overload_true(str_null_bools) and str_arr.types[i
                ] == string_array_type:
                rebbe__zfe += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}], list_data[{}])\n'
                    .format(i, i, mzhfs__suprs + ooyy__fxoh))
                ooyy__fxoh += 1
            else:
                rebbe__zfe += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}])\n'.
                    format(i, i))
        rebbe__zfe += '  return\n'
        toky__qtb = {}
        exec(rebbe__zfe, {'cp_str_list_to_array': cp_str_list_to_array},
            toky__qtb)
        bxuq__sff = toky__qtb['f']
        return bxuq__sff
    return lambda str_arr, list_data, str_null_bools=None: None


def str_list_to_array(str_list):
    return str_list


@overload(str_list_to_array, no_unliteral=True)
def str_list_to_array_overload(str_list):
    if isinstance(str_list, types.List) and str_list.dtype == bodo.string_type:

        def str_list_impl(str_list):
            pcd__gsd = len(str_list)
            str_arr = pre_alloc_string_array(pcd__gsd, -1)
            for i in range(pcd__gsd):
                vtydc__fqufv = str_list[i]
                str_arr[i] = vtydc__fqufv
            return str_arr
        return str_list_impl
    return lambda str_list: str_list


def get_num_total_chars(A):
    pass


@overload(get_num_total_chars)
def overload_get_num_total_chars(A):
    if isinstance(A, types.List) and A.dtype == string_type:

        def str_list_impl(A):
            pcd__gsd = len(A)
            uuc__pgl = 0
            for i in range(pcd__gsd):
                vtydc__fqufv = A[i]
                uuc__pgl += get_utf8_size(vtydc__fqufv)
            return uuc__pgl
        return str_list_impl
    assert A == string_array_type
    return lambda A: num_total_chars(A)


@overload_method(StringArrayType, 'copy', no_unliteral=True)
def str_arr_copy_overload(arr):

    def copy_impl(arr):
        pcd__gsd = len(arr)
        n_chars = num_total_chars(arr)
        jhr__zaoln = pre_alloc_string_array(pcd__gsd, np.int64(n_chars))
        copy_str_arr_slice(jhr__zaoln, arr, pcd__gsd)
        return jhr__zaoln
    return copy_impl


@overload(len, no_unliteral=True)
def str_arr_len_overload(str_arr):
    if str_arr == string_array_type:

        def str_arr_len(str_arr):
            return str_arr.size
        return str_arr_len


@overload_attribute(StringArrayType, 'size')
def str_arr_size_overload(str_arr):
    return lambda str_arr: len(str_arr._data)


@overload_attribute(StringArrayType, 'shape')
def str_arr_shape_overload(str_arr):
    return lambda str_arr: (str_arr.size,)


@overload_attribute(StringArrayType, 'nbytes')
def str_arr_nbytes_overload(str_arr):
    return lambda str_arr: str_arr._data.nbytes


@overload_method(types.Array, 'tolist', no_unliteral=True)
@overload_method(StringArrayType, 'tolist', no_unliteral=True)
def overload_to_list(arr):
    return lambda arr: list(arr)


import llvmlite.binding as ll
from llvmlite import ir as lir
from bodo.libs import array_ext, hstr_ext
ll.add_symbol('get_str_len', hstr_ext.get_str_len)
ll.add_symbol('setitem_string_array', hstr_ext.setitem_string_array)
ll.add_symbol('is_na', hstr_ext.is_na)
ll.add_symbol('string_array_from_sequence', array_ext.
    string_array_from_sequence)
ll.add_symbol('pd_array_from_string_array', hstr_ext.pd_array_from_string_array
    )
ll.add_symbol('np_array_from_string_array', hstr_ext.np_array_from_string_array
    )
ll.add_symbol('convert_len_arr_to_offset32', hstr_ext.
    convert_len_arr_to_offset32)
ll.add_symbol('convert_len_arr_to_offset', hstr_ext.convert_len_arr_to_offset)
ll.add_symbol('set_string_array_range', hstr_ext.set_string_array_range)
ll.add_symbol('str_arr_to_int64', hstr_ext.str_arr_to_int64)
ll.add_symbol('str_arr_to_float64', hstr_ext.str_arr_to_float64)
ll.add_symbol('get_utf8_size', hstr_ext.get_utf8_size)
ll.add_symbol('print_str_arr', hstr_ext.print_str_arr)
ll.add_symbol('inplace_int64_to_str', hstr_ext.inplace_int64_to_str)
inplace_int64_to_str = types.ExternalFunction('inplace_int64_to_str', types
    .void(types.voidptr, types.int64, types.int64))
convert_len_arr_to_offset32 = types.ExternalFunction(
    'convert_len_arr_to_offset32', types.void(types.voidptr, types.intp))
convert_len_arr_to_offset = types.ExternalFunction('convert_len_arr_to_offset',
    types.void(types.voidptr, types.voidptr, types.intp))
setitem_string_array = types.ExternalFunction('setitem_string_array', types
    .void(types.CPointer(offset_type), types.CPointer(char_type), types.
    uint64, types.voidptr, types.intp, offset_type, offset_type, types.intp))
_get_utf8_size = types.ExternalFunction('get_utf8_size', types.intp(types.
    voidptr, types.intp, offset_type))
_print_str_arr = types.ExternalFunction('print_str_arr', types.void(types.
    uint64, types.uint64, types.CPointer(offset_type), types.CPointer(
    char_type)))


@numba.generated_jit(nopython=True)
def empty_str_arr(in_seq):
    rebbe__zfe = 'def f(in_seq):\n'
    rebbe__zfe += '    n_strs = len(in_seq)\n'
    rebbe__zfe += '    A = pre_alloc_string_array(n_strs, -1)\n'
    rebbe__zfe += '    return A\n'
    toky__qtb = {}
    exec(rebbe__zfe, {'pre_alloc_string_array': pre_alloc_string_array},
        toky__qtb)
    sduht__vcnd = toky__qtb['f']
    return sduht__vcnd


@numba.generated_jit(nopython=True)
def str_arr_from_sequence(in_seq):
    if in_seq.dtype == bodo.bytes_type:
        qjbw__xfkq = 'pre_alloc_binary_array'
    else:
        qjbw__xfkq = 'pre_alloc_string_array'
    rebbe__zfe = 'def f(in_seq):\n'
    rebbe__zfe += '    n_strs = len(in_seq)\n'
    rebbe__zfe += f'    A = {qjbw__xfkq}(n_strs, -1)\n'
    rebbe__zfe += '    for i in range(n_strs):\n'
    rebbe__zfe += '        A[i] = in_seq[i]\n'
    rebbe__zfe += '    return A\n'
    toky__qtb = {}
    exec(rebbe__zfe, {'pre_alloc_string_array': pre_alloc_string_array,
        'pre_alloc_binary_array': pre_alloc_binary_array}, toky__qtb)
    sduht__vcnd = toky__qtb['f']
    return sduht__vcnd


@intrinsic
def set_all_offsets_to_0(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_all_offsets_to_0 requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        kpuny__bzrmp = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        jmn__sdj = builder.add(kpuny__bzrmp.n_arrays, lir.Constant(lir.
            IntType(64), 1))
        wdb__fgcya = builder.lshr(lir.Constant(lir.IntType(64), offset_type
            .bitwidth), lir.Constant(lir.IntType(64), 3))
        mhzh__zmx = builder.mul(jmn__sdj, wdb__fgcya)
        xqi__jukv = context.make_array(offset_arr_type)(context, builder,
            kpuny__bzrmp.offsets).data
        cgutils.memset(builder, xqi__jukv, mhzh__zmx, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@intrinsic
def set_bitmap_all_NA(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_bitmap_all_NA requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        kpuny__bzrmp = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        dzm__bopr = kpuny__bzrmp.n_arrays
        mhzh__zmx = builder.lshr(builder.add(dzm__bopr, lir.Constant(lir.
            IntType(64), 7)), lir.Constant(lir.IntType(64), 3))
        qosvi__mpyac = context.make_array(null_bitmap_arr_type)(context,
            builder, kpuny__bzrmp.null_bitmap).data
        cgutils.memset(builder, qosvi__mpyac, mhzh__zmx, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@numba.njit
def pre_alloc_string_array(n_strs, n_chars):
    if n_chars is None:
        n_chars = -1
    str_arr = init_str_arr(bodo.libs.array_item_arr_ext.
        pre_alloc_array_item_array(np.int64(n_strs), (np.int64(n_chars),),
        char_arr_type))
    if n_chars == 0:
        set_all_offsets_to_0(str_arr)
    return str_arr


@register_jitable
def gen_na_str_array_lens(n_strs, total_len, len_arr):
    str_arr = pre_alloc_string_array(n_strs, total_len)
    set_bitmap_all_NA(str_arr)
    offsets = bodo.libs.array_item_arr_ext.get_offsets(str_arr._data)
    liz__rirc = 0
    uctea__zrvec = len(len_arr)
    for i in range(uctea__zrvec):
        offsets[i] = liz__rirc
        liz__rirc += len_arr[i]
    offsets[uctea__zrvec] = liz__rirc
    return str_arr


kBitmask = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)


@numba.njit
def set_bit_to(bits, i, bit_is_set):
    jdjh__ldsbm = i // 8
    vjdj__jnt = getitem_str_bitmap(bits, jdjh__ldsbm)
    vjdj__jnt ^= np.uint8(-np.uint8(bit_is_set) ^ vjdj__jnt) & kBitmask[i % 8]
    setitem_str_bitmap(bits, jdjh__ldsbm, vjdj__jnt)


@numba.njit
def get_bit_bitmap(bits, i):
    return getitem_str_bitmap(bits, i >> 3) >> (i & 7) & 1


@numba.njit
def copy_nulls_range(out_str_arr, in_str_arr, out_start):
    ugq__zit = get_null_bitmap_ptr(out_str_arr)
    ewpn__axbe = get_null_bitmap_ptr(in_str_arr)
    for yyzz__yir in range(len(in_str_arr)):
        obv__gkhv = get_bit_bitmap(ewpn__axbe, yyzz__yir)
        set_bit_to(ugq__zit, out_start + yyzz__yir, obv__gkhv)


@intrinsic
def set_string_array_range(typingctx, out_typ, in_typ, curr_str_typ,
    curr_chars_typ=None):
    assert out_typ == string_array_type and in_typ == string_array_type or out_typ == binary_array_type and in_typ == binary_array_type
    assert curr_str_typ == types.intp and curr_chars_typ == types.intp

    def codegen(context, builder, sig, args):
        out_arr, uga__vdlbo, rvxu__jaewp, sopi__viir = args
        lvp__gkvtl = _get_str_binary_arr_payload(context, builder,
            uga__vdlbo, string_array_type)
        ewum__rai = _get_str_binary_arr_payload(context, builder, out_arr,
            string_array_type)
        sxvec__ntlan = context.make_helper(builder, offset_arr_type,
            lvp__gkvtl.offsets).data
        sths__myd = context.make_helper(builder, offset_arr_type, ewum__rai
            .offsets).data
        lxitl__meua = context.make_helper(builder, char_arr_type,
            lvp__gkvtl.data).data
        oxwa__svdc = context.make_helper(builder, char_arr_type, ewum__rai.data
            ).data
        num_total_chars = _get_num_total_chars(builder, sxvec__ntlan,
            lvp__gkvtl.n_arrays)
        nrmwx__nwlf = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(64), lir.IntType(64),
            lir.IntType(64)])
        xdw__butvb = cgutils.get_or_insert_function(builder.module,
            nrmwx__nwlf, name='set_string_array_range')
        builder.call(xdw__butvb, [sths__myd, oxwa__svdc, sxvec__ntlan,
            lxitl__meua, rvxu__jaewp, sopi__viir, lvp__gkvtl.n_arrays,
            num_total_chars])
        nxvty__lwqnr = context.typing_context.resolve_value_type(
            copy_nulls_range)
        fvqyl__gwh = nxvty__lwqnr.get_call_type(context.typing_context, (
            string_array_type, string_array_type, types.int64), {})
        kub__zkx = context.get_function(nxvty__lwqnr, fvqyl__gwh)
        kub__zkx(builder, (out_arr, uga__vdlbo, rvxu__jaewp))
        return context.get_dummy_value()
    sig = types.void(out_typ, in_typ, types.intp, types.intp)
    return sig, codegen


@box(BinaryArrayType)
@box(StringArrayType)
def box_str_arr(typ, val, c):
    assert typ in [binary_array_type, string_array_type]
    aygs__luq = c.context.make_helper(c.builder, typ, val)
    iyedw__gthmc = ArrayItemArrayType(char_arr_type)
    kpuny__bzrmp = _get_array_item_arr_payload(c.context, c.builder,
        iyedw__gthmc, aygs__luq.data)
    hieay__mro = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    pleh__zqnwz = 'np_array_from_string_array'
    if use_pd_string_array and typ != binary_array_type:
        pleh__zqnwz = 'pd_array_from_string_array'
    nrmwx__nwlf = lir.FunctionType(c.context.get_argument_type(types.
        pyobject), [lir.IntType(64), lir.IntType(offset_type.bitwidth).
        as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
        as_pointer(), lir.IntType(32)])
    ciw__wzve = cgutils.get_or_insert_function(c.builder.module,
        nrmwx__nwlf, name=pleh__zqnwz)
    pdruj__beo = c.context.make_array(offset_arr_type)(c.context, c.builder,
        kpuny__bzrmp.offsets).data
    mrej__zbg = c.context.make_array(char_arr_type)(c.context, c.builder,
        kpuny__bzrmp.data).data
    qosvi__mpyac = c.context.make_array(null_bitmap_arr_type)(c.context, c.
        builder, kpuny__bzrmp.null_bitmap).data
    arr = c.builder.call(ciw__wzve, [kpuny__bzrmp.n_arrays, pdruj__beo,
        mrej__zbg, qosvi__mpyac, hieay__mro])
    c.context.nrt.decref(c.builder, typ, val)
    return arr


@intrinsic
def str_arr_is_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        kpuny__bzrmp = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        qosvi__mpyac = context.make_array(null_bitmap_arr_type)(context,
            builder, kpuny__bzrmp.null_bitmap).data
        irby__hjc = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        uiuc__mdzo = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        vjdj__jnt = builder.load(builder.gep(qosvi__mpyac, [irby__hjc],
            inbounds=True))
        ckldd__kmta = lir.ArrayType(lir.IntType(8), 8)
        ufl__yval = cgutils.alloca_once_value(builder, lir.Constant(
            ckldd__kmta, (1, 2, 4, 8, 16, 32, 64, 128)))
        cfy__jvp = builder.load(builder.gep(ufl__yval, [lir.Constant(lir.
            IntType(64), 0), uiuc__mdzo], inbounds=True))
        return builder.icmp_unsigned('==', builder.and_(vjdj__jnt, cfy__jvp
            ), lir.Constant(lir.IntType(8), 0))
    return types.bool_(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        kpuny__bzrmp = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        irby__hjc = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        uiuc__mdzo = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        qosvi__mpyac = context.make_array(null_bitmap_arr_type)(context,
            builder, kpuny__bzrmp.null_bitmap).data
        offsets = context.make_helper(builder, offset_arr_type,
            kpuny__bzrmp.offsets).data
        hzuz__oqryi = builder.gep(qosvi__mpyac, [irby__hjc], inbounds=True)
        vjdj__jnt = builder.load(hzuz__oqryi)
        ckldd__kmta = lir.ArrayType(lir.IntType(8), 8)
        ufl__yval = cgutils.alloca_once_value(builder, lir.Constant(
            ckldd__kmta, (1, 2, 4, 8, 16, 32, 64, 128)))
        cfy__jvp = builder.load(builder.gep(ufl__yval, [lir.Constant(lir.
            IntType(64), 0), uiuc__mdzo], inbounds=True))
        cfy__jvp = builder.xor(cfy__jvp, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(vjdj__jnt, cfy__jvp), hzuz__oqryi)
        if str_arr_typ == string_array_type:
            dzyuk__raa = builder.add(ind, lir.Constant(lir.IntType(64), 1))
            nyf__qkxj = builder.icmp_unsigned('!=', dzyuk__raa,
                kpuny__bzrmp.n_arrays)
            with builder.if_then(nyf__qkxj):
                builder.store(builder.load(builder.gep(offsets, [ind])),
                    builder.gep(offsets, [dzyuk__raa]))
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_not_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        kpuny__bzrmp = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        irby__hjc = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        uiuc__mdzo = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        qosvi__mpyac = context.make_array(null_bitmap_arr_type)(context,
            builder, kpuny__bzrmp.null_bitmap).data
        hzuz__oqryi = builder.gep(qosvi__mpyac, [irby__hjc], inbounds=True)
        vjdj__jnt = builder.load(hzuz__oqryi)
        ckldd__kmta = lir.ArrayType(lir.IntType(8), 8)
        ufl__yval = cgutils.alloca_once_value(builder, lir.Constant(
            ckldd__kmta, (1, 2, 4, 8, 16, 32, 64, 128)))
        cfy__jvp = builder.load(builder.gep(ufl__yval, [lir.Constant(lir.
            IntType(64), 0), uiuc__mdzo], inbounds=True))
        builder.store(builder.or_(vjdj__jnt, cfy__jvp), hzuz__oqryi)
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def set_null_bits_to_value(typingctx, arr_typ, value_typ=None):
    assert (arr_typ == string_array_type or arr_typ == binary_array_type
        ) and is_overload_constant_int(value_typ)

    def codegen(context, builder, sig, args):
        in_str_arr, value = args
        kpuny__bzrmp = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        mhzh__zmx = builder.udiv(builder.add(kpuny__bzrmp.n_arrays, lir.
            Constant(lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
        qosvi__mpyac = context.make_array(null_bitmap_arr_type)(context,
            builder, kpuny__bzrmp.null_bitmap).data
        cgutils.memset(builder, qosvi__mpyac, mhzh__zmx, value)
        return context.get_dummy_value()
    return types.none(arr_typ, types.int8), codegen


def _get_str_binary_arr_data_payload_ptr(context, builder, str_arr):
    dqomq__wsrq = context.make_helper(builder, string_array_type, str_arr)
    iyedw__gthmc = ArrayItemArrayType(char_arr_type)
    diz__jmuag = context.make_helper(builder, iyedw__gthmc, dqomq__wsrq.data)
    lctvz__fnkm = ArrayItemArrayPayloadType(iyedw__gthmc)
    loy__mrolt = context.nrt.meminfo_data(builder, diz__jmuag.meminfo)
    nzb__ozhy = builder.bitcast(loy__mrolt, context.get_value_type(
        lctvz__fnkm).as_pointer())
    return nzb__ozhy


@intrinsic
def move_str_binary_arr_payload(typingctx, to_arr_typ, from_arr_typ=None):
    assert to_arr_typ == string_array_type and from_arr_typ == string_array_type or to_arr_typ == binary_array_type and from_arr_typ == binary_array_type

    def codegen(context, builder, sig, args):
        zeilp__ojfph, ttr__ryfmd = args
        qjw__vzmnk = _get_str_binary_arr_data_payload_ptr(context, builder,
            ttr__ryfmd)
        ful__ejfg = _get_str_binary_arr_data_payload_ptr(context, builder,
            zeilp__ojfph)
        taov__opic = _get_str_binary_arr_payload(context, builder,
            ttr__ryfmd, sig.args[1])
        gbnn__fqqz = _get_str_binary_arr_payload(context, builder,
            zeilp__ojfph, sig.args[0])
        context.nrt.incref(builder, char_arr_type, taov__opic.data)
        context.nrt.incref(builder, offset_arr_type, taov__opic.offsets)
        context.nrt.incref(builder, null_bitmap_arr_type, taov__opic.
            null_bitmap)
        context.nrt.decref(builder, char_arr_type, gbnn__fqqz.data)
        context.nrt.decref(builder, offset_arr_type, gbnn__fqqz.offsets)
        context.nrt.decref(builder, null_bitmap_arr_type, gbnn__fqqz.
            null_bitmap)
        builder.store(builder.load(qjw__vzmnk), ful__ejfg)
        return context.get_dummy_value()
    return types.none(to_arr_typ, from_arr_typ), codegen


dummy_use = numba.njit(lambda a: None)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_utf8_size(s):
    if isinstance(s, types.StringLiteral):
        l = len(s.literal_value.encode())
        return lambda s: l

    def impl(s):
        if s is None:
            return 0
        s = bodo.utils.indexing.unoptional(s)
        if s._is_ascii == 1:
            return len(s)
        pcd__gsd = _get_utf8_size(s._data, s._length, s._kind)
        dummy_use(s)
        return pcd__gsd
    return impl


@intrinsic
def setitem_str_arr_ptr(typingctx, str_arr_t, ind_t, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        arr, ind, oehk__taad, sqoc__ufqx = args
        kpuny__bzrmp = _get_str_binary_arr_payload(context, builder, arr,
            sig.args[0])
        offsets = context.make_helper(builder, offset_arr_type,
            kpuny__bzrmp.offsets).data
        data = context.make_helper(builder, char_arr_type, kpuny__bzrmp.data
            ).data
        nrmwx__nwlf = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64),
            lir.IntType(32), lir.IntType(32), lir.IntType(64)])
        fdha__ujus = cgutils.get_or_insert_function(builder.module,
            nrmwx__nwlf, name='setitem_string_array')
        xjkj__fmcuu = context.get_constant(types.int32, -1)
        sbey__lfd = context.get_constant(types.int32, 1)
        num_total_chars = _get_num_total_chars(builder, offsets,
            kpuny__bzrmp.n_arrays)
        builder.call(fdha__ujus, [offsets, data, num_total_chars, builder.
            extract_value(oehk__taad, 0), sqoc__ufqx, xjkj__fmcuu,
            sbey__lfd, ind])
        return context.get_dummy_value()
    return types.void(str_arr_t, ind_t, ptr_t, len_t), codegen


def lower_is_na(context, builder, bull_bitmap, ind):
    nrmwx__nwlf = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64)])
    hqb__ndf = cgutils.get_or_insert_function(builder.module, nrmwx__nwlf,
        name='is_na')
    return builder.call(hqb__ndf, [bull_bitmap, ind])


@intrinsic
def _memcpy(typingctx, dest_t, src_t, count_t, item_size_t=None):

    def codegen(context, builder, sig, args):
        uisr__hyst, oxts__nhb, mzhfs__suprs, taind__pfwn = args
        cgutils.raw_memcpy(builder, uisr__hyst, oxts__nhb, mzhfs__suprs,
            taind__pfwn)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.voidptr, types.intp, types.intp
        ), codegen


@numba.njit
def print_str_arr(arr):
    _print_str_arr(num_strings(arr), num_total_chars(arr), get_offset_ptr(
        arr), get_data_ptr(arr))


def inplace_eq(A, i, val):
    return A[i] == val


@overload(inplace_eq)
def inplace_eq_overload(A, ind, val):

    def impl(A, ind, val):
        rjmm__xiv, kxwt__xwb = unicode_to_utf8_and_len(val)
        pfxg__xhr = getitem_str_offset(A, ind)
        xkdi__hxh = getitem_str_offset(A, ind + 1)
        yqxpm__pcthl = xkdi__hxh - pfxg__xhr
        if yqxpm__pcthl != kxwt__xwb:
            return False
        oehk__taad = get_data_ptr_ind(A, pfxg__xhr)
        return memcmp(oehk__taad, rjmm__xiv, kxwt__xwb) == 0
    return impl


def str_arr_setitem_int_to_str(A, ind, value):
    A[ind] = str(value)


@overload(str_arr_setitem_int_to_str)
def overload_str_arr_setitem_int_to_str(A, ind, val):

    def impl(A, ind, val):
        pfxg__xhr = getitem_str_offset(A, ind)
        yqxpm__pcthl = bodo.libs.str_ext.int_to_str_len(val)
        yvurw__qcpke = pfxg__xhr + yqxpm__pcthl
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            pfxg__xhr, yvurw__qcpke)
        oehk__taad = get_data_ptr_ind(A, pfxg__xhr)
        inplace_int64_to_str(oehk__taad, yqxpm__pcthl, val)
        setitem_str_offset(A, ind + 1, pfxg__xhr + yqxpm__pcthl)
        str_arr_set_not_na(A, ind)
    return impl


@intrinsic
def inplace_set_NA_str(typingctx, ptr_typ=None):

    def codegen(context, builder, sig, args):
        oehk__taad, = args
        boi__zzhs = context.insert_const_string(builder.module, '<NA>')
        wxnwr__weffs = lir.Constant(lir.IntType(64), len('<NA>'))
        cgutils.raw_memcpy(builder, oehk__taad, boi__zzhs, wxnwr__weffs, 1)
    return types.none(types.voidptr), codegen


def str_arr_setitem_NA_str(A, ind):
    A[ind] = '<NA>'


@overload(str_arr_setitem_NA_str)
def overload_str_arr_setitem_NA_str(A, ind):
    advx__idj = len('<NA>')

    def impl(A, ind):
        pfxg__xhr = getitem_str_offset(A, ind)
        yvurw__qcpke = pfxg__xhr + advx__idj
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            pfxg__xhr, yvurw__qcpke)
        oehk__taad = get_data_ptr_ind(A, pfxg__xhr)
        inplace_set_NA_str(oehk__taad)
        setitem_str_offset(A, ind + 1, pfxg__xhr + advx__idj)
        str_arr_set_not_na(A, ind)
    return impl


@overload(operator.getitem, no_unliteral=True)
def str_arr_getitem_int(A, ind):
    if A != string_array_type:
        return
    if isinstance(ind, types.Integer):

        def str_arr_getitem_impl(A, ind):
            if ind < 0:
                ind += A.size
            pfxg__xhr = getitem_str_offset(A, ind)
            xkdi__hxh = getitem_str_offset(A, ind + 1)
            sqoc__ufqx = xkdi__hxh - pfxg__xhr
            oehk__taad = get_data_ptr_ind(A, pfxg__xhr)
            cesmb__uobaq = decode_utf8(oehk__taad, sqoc__ufqx)
            return cesmb__uobaq
        return str_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def bool_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_ndarray(ind)
            pcd__gsd = len(A)
            n_strs = 0
            n_chars = 0
            for i in range(pcd__gsd):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    n_strs += 1
                    n_chars += get_str_arr_item_length(A, i)
            out_arr = pre_alloc_string_array(n_strs, n_chars)
            rltan__tepbm = get_data_ptr(out_arr).data
            idp__jnjdg = get_data_ptr(A).data
            ooyy__fxoh = 0
            pleup__gbzs = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(pcd__gsd):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    cxd__hrv = get_str_arr_item_length(A, i)
                    if cxd__hrv == 1:
                        copy_single_char(rltan__tepbm, pleup__gbzs,
                            idp__jnjdg, getitem_str_offset(A, i))
                    else:
                        memcpy_region(rltan__tepbm, pleup__gbzs, idp__jnjdg,
                            getitem_str_offset(A, i), cxd__hrv, 1)
                    pleup__gbzs += cxd__hrv
                    setitem_str_offset(out_arr, ooyy__fxoh + 1, pleup__gbzs)
                    if str_arr_is_na(A, i):
                        str_arr_set_na(out_arr, ooyy__fxoh)
                    else:
                        str_arr_set_not_na(out_arr, ooyy__fxoh)
                    ooyy__fxoh += 1
            return out_arr
        return bool_impl
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def str_arr_arr_impl(A, ind):
            pcd__gsd = len(ind)
            out_arr = pre_alloc_string_array(pcd__gsd, -1)
            ooyy__fxoh = 0
            for i in range(pcd__gsd):
                vtydc__fqufv = A[ind[i]]
                out_arr[ooyy__fxoh] = vtydc__fqufv
                if str_arr_is_na(A, ind[i]):
                    str_arr_set_na(out_arr, ooyy__fxoh)
                ooyy__fxoh += 1
            return out_arr
        return str_arr_arr_impl
    if isinstance(ind, types.SliceType):

        def str_arr_slice_impl(A, ind):
            pcd__gsd = len(A)
            gwveq__ugav = numba.cpython.unicode._normalize_slice(ind, pcd__gsd)
            bcw__yryju = numba.cpython.unicode._slice_span(gwveq__ugav)
            if gwveq__ugav.step == 1:
                pfxg__xhr = getitem_str_offset(A, gwveq__ugav.start)
                xkdi__hxh = getitem_str_offset(A, gwveq__ugav.stop)
                n_chars = xkdi__hxh - pfxg__xhr
                jhr__zaoln = pre_alloc_string_array(bcw__yryju, np.int64(
                    n_chars))
                for i in range(bcw__yryju):
                    jhr__zaoln[i] = A[gwveq__ugav.start + i]
                    if str_arr_is_na(A, gwveq__ugav.start + i):
                        str_arr_set_na(jhr__zaoln, i)
                return jhr__zaoln
            else:
                jhr__zaoln = pre_alloc_string_array(bcw__yryju, -1)
                for i in range(bcw__yryju):
                    jhr__zaoln[i] = A[gwveq__ugav.start + i * gwveq__ugav.step]
                    if str_arr_is_na(A, gwveq__ugav.start + i * gwveq__ugav
                        .step):
                        str_arr_set_na(jhr__zaoln, i)
                return jhr__zaoln
        return str_arr_slice_impl
    raise BodoError(
        f'getitem for StringArray with indexing type {ind} not supported.')


dummy_use = numba.njit(lambda a: None)


@overload(operator.setitem)
def str_arr_setitem(A, idx, val):
    if A != string_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    celwx__baii = (
        f'StringArray setitem with index {idx} and value {val} not supported yet.'
        )
    if isinstance(idx, types.Integer):
        if val != string_type:
            raise BodoError(celwx__baii)
        leoj__vlkc = 4

        def impl_scalar(A, idx, val):
            wrfb__ewwa = (val._length if val._is_ascii else leoj__vlkc *
                val._length)
            uxe__pcxz = A._data
            pfxg__xhr = np.int64(getitem_str_offset(A, idx))
            yvurw__qcpke = pfxg__xhr + wrfb__ewwa
            bodo.libs.array_item_arr_ext.ensure_data_capacity(uxe__pcxz,
                pfxg__xhr, yvurw__qcpke)
            setitem_string_array(get_offset_ptr(A), get_data_ptr(A),
                yvurw__qcpke, val._data, val._length, val._kind, val.
                _is_ascii, idx)
            str_arr_set_not_na(A, idx)
            dummy_use(A)
            dummy_use(val)
        return impl_scalar
    if isinstance(idx, types.SliceType):
        if val == string_array_type:

            def impl_slice(A, idx, val):
                gwveq__ugav = numba.cpython.unicode._normalize_slice(idx,
                    len(A))
                myh__fexc = gwveq__ugav.start
                uxe__pcxz = A._data
                pfxg__xhr = np.int64(getitem_str_offset(A, myh__fexc))
                yvurw__qcpke = pfxg__xhr + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(uxe__pcxz,
                    pfxg__xhr, yvurw__qcpke)
                set_string_array_range(A, val, myh__fexc, pfxg__xhr)
                yju__sst = 0
                for i in range(gwveq__ugav.start, gwveq__ugav.stop,
                    gwveq__ugav.step):
                    if str_arr_is_na(val, yju__sst):
                        str_arr_set_na(A, i)
                    else:
                        str_arr_set_not_na(A, i)
                    yju__sst += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == string_type:

            def impl_slice_list(A, idx, val):
                lhfg__jqou = str_list_to_array(val)
                A[idx] = lhfg__jqou
            return impl_slice_list
        elif val == string_type:

            def impl_slice(A, idx, val):
                gwveq__ugav = numba.cpython.unicode._normalize_slice(idx,
                    len(A))
                for i in range(gwveq__ugav.start, gwveq__ugav.stop,
                    gwveq__ugav.step):
                    A[i] = val
            return impl_slice
        else:
            raise BodoError(celwx__baii)
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if val == string_type:

            def impl_bool_scalar(A, idx, val):
                pcd__gsd = len(A)
                idx = bodo.utils.conversion.coerce_to_ndarray(idx)
                out_arr = pre_alloc_string_array(pcd__gsd, -1)
                for i in numba.parfors.parfor.internal_prange(pcd__gsd):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        out_arr[i] = val
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        out_arr[i] = A[i]
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_scalar
        elif val == string_array_type or isinstance(val, types.Array
            ) and isinstance(val.dtype, types.UnicodeCharSeq):

            def impl_bool_arr(A, idx, val):
                pcd__gsd = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx,
                    use_nullable_array=True)
                out_arr = pre_alloc_string_array(pcd__gsd, -1)
                bjned__leib = 0
                for i in numba.parfors.parfor.internal_prange(pcd__gsd):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        if bodo.libs.array_kernels.isna(val, bjned__leib):
                            out_arr[i] = ''
                            str_arr_set_na(out_arr, bjned__leib)
                        else:
                            out_arr[i] = str(val[bjned__leib])
                        bjned__leib += 1
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        out_arr[i] = A[i]
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_arr
        else:
            raise BodoError(celwx__baii)
    raise BodoError(celwx__baii)


@overload_attribute(StringArrayType, 'dtype')
def overload_str_arr_dtype(A):
    return lambda A: pd.StringDtype()


@overload_attribute(StringArrayType, 'ndim')
def overload_str_arr_ndim(A):
    return lambda A: 1


@overload_method(StringArrayType, 'astype', no_unliteral=True)
def overload_str_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "StringArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if isinstance(dtype, types.Function) and dtype.key[0] == str:
        return lambda A, dtype, copy=True: A
    bxz__ihq = parse_dtype(dtype, 'StringArray.astype')
    if not isinstance(bxz__ihq, (types.Float, types.Integer)):
        raise BodoError('invalid dtype in StringArray.astype()')
    if isinstance(bxz__ihq, types.Float):

        def impl_float(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            pcd__gsd = len(A)
            velkb__drgvy = np.empty(pcd__gsd, bxz__ihq)
            for i in numba.parfors.parfor.internal_prange(pcd__gsd):
                if bodo.libs.array_kernels.isna(A, i):
                    velkb__drgvy[i] = np.nan
                else:
                    velkb__drgvy[i] = float(A[i])
            return velkb__drgvy
        return impl_float
    else:

        def impl_int(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            pcd__gsd = len(A)
            velkb__drgvy = np.empty(pcd__gsd, bxz__ihq)
            for i in numba.parfors.parfor.internal_prange(pcd__gsd):
                velkb__drgvy[i] = int(A[i])
            return velkb__drgvy
        return impl_int


@intrinsic
def decode_utf8(typingctx, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        oehk__taad, sqoc__ufqx = args
        duzhb__huf = context.get_python_api(builder)
        qlc__zwp = duzhb__huf.string_from_string_and_size(oehk__taad,
            sqoc__ufqx)
        pmzyp__vve = duzhb__huf.to_native_value(string_type, qlc__zwp).value
        sjoc__zaf = cgutils.create_struct_proxy(string_type)(context,
            builder, pmzyp__vve)
        sjoc__zaf.hash = sjoc__zaf.hash.type(-1)
        duzhb__huf.decref(qlc__zwp)
        return sjoc__zaf._getvalue()
    return string_type(types.voidptr, types.intp), codegen


def get_arr_data_ptr(arr, ind):
    return arr


@overload(get_arr_data_ptr, no_unliteral=True)
def overload_get_arr_data_ptr(arr, ind):
    assert isinstance(types.unliteral(ind), types.Integer)
    if isinstance(arr, bodo.libs.int_arr_ext.IntegerArrayType):

        def impl_int(arr, ind):
            return bodo.hiframes.split_impl.get_c_arr_ptr(arr._data.ctypes, ind
                )
        return impl_int
    assert isinstance(arr, types.Array)

    def impl_np(arr, ind):
        return bodo.hiframes.split_impl.get_c_arr_ptr(arr.ctypes, ind)
    return impl_np


def set_to_numeric_out_na_err(out_arr, out_ind, err_code):
    pass


@overload(set_to_numeric_out_na_err)
def set_to_numeric_out_na_err_overload(out_arr, out_ind, err_code):
    if isinstance(out_arr, bodo.libs.int_arr_ext.IntegerArrayType):

        def impl_int(out_arr, out_ind, err_code):
            bodo.libs.int_arr_ext.set_bit_to_arr(out_arr._null_bitmap,
                out_ind, 0 if err_code == -1 else 1)
        return impl_int
    assert isinstance(out_arr, types.Array)
    if isinstance(out_arr.dtype, types.Float):

        def impl_np(out_arr, out_ind, err_code):
            if err_code == -1:
                out_arr[out_ind] = np.nan
        return impl_np
    return lambda out_arr, out_ind, err_code: None


@numba.njit(no_cpython_wrapper=True)
def str_arr_item_to_numeric(out_arr, out_ind, str_arr, ind):
    err_code = _str_arr_item_to_numeric(get_arr_data_ptr(out_arr, out_ind),
        str_arr, ind, out_arr.dtype)
    set_to_numeric_out_na_err(out_arr, out_ind, err_code)


@intrinsic
def _str_arr_item_to_numeric(typingctx, out_ptr_t, str_arr_t, ind_t,
    out_dtype_t=None):
    assert str_arr_t == string_array_type
    assert ind_t == types.int64

    def codegen(context, builder, sig, args):
        ppu__eaza, arr, ind, lyhv__ekis = args
        kpuny__bzrmp = _get_str_binary_arr_payload(context, builder, arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type,
            kpuny__bzrmp.offsets).data
        data = context.make_helper(builder, char_arr_type, kpuny__bzrmp.data
            ).data
        nrmwx__nwlf = lir.FunctionType(lir.IntType(32), [ppu__eaza.type,
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        kzhd__ckvim = 'str_arr_to_int64'
        if sig.args[3].dtype == types.float64:
            kzhd__ckvim = 'str_arr_to_float64'
        else:
            assert sig.args[3].dtype == types.int64
        odgg__nmzz = cgutils.get_or_insert_function(builder.module,
            nrmwx__nwlf, kzhd__ckvim)
        return builder.call(odgg__nmzz, [ppu__eaza, offsets, data, ind])
    return types.int32(out_ptr_t, string_array_type, types.int64, out_dtype_t
        ), codegen


@unbox(BinaryArrayType)
@unbox(StringArrayType)
def unbox_str_series(typ, val, c):
    hieay__mro = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    nrmwx__nwlf = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
        IntType(8).as_pointer(), lir.IntType(32)])
    jgh__scp = cgutils.get_or_insert_function(c.builder.module, nrmwx__nwlf,
        name='string_array_from_sequence')
    epcp__jqwji = c.builder.call(jgh__scp, [val, hieay__mro])
    iyedw__gthmc = ArrayItemArrayType(char_arr_type)
    diz__jmuag = c.context.make_helper(c.builder, iyedw__gthmc)
    diz__jmuag.meminfo = epcp__jqwji
    dqomq__wsrq = c.context.make_helper(c.builder, typ)
    uxe__pcxz = diz__jmuag._getvalue()
    dqomq__wsrq.data = uxe__pcxz
    ukh__jdlz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(dqomq__wsrq._getvalue(), is_error=ukh__jdlz)


@lower_constant(BinaryArrayType)
@lower_constant(StringArrayType)
def lower_constant_str_arr(context, builder, typ, pyval):
    pcd__gsd = len(pyval)
    pleup__gbzs = 0
    skj__slbb = np.empty(pcd__gsd + 1, np_offset_type)
    pypr__cty = []
    vis__byhlz = np.empty(pcd__gsd + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        skj__slbb[i] = pleup__gbzs
        jqrjy__gaqz = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(vis__byhlz, i, int(not
            jqrjy__gaqz))
        if jqrjy__gaqz:
            continue
        tkjx__qfaj = list(s.encode()) if isinstance(s, str) else list(s)
        pypr__cty.extend(tkjx__qfaj)
        pleup__gbzs += len(tkjx__qfaj)
    skj__slbb[pcd__gsd] = pleup__gbzs
    rxkl__alxr = np.array(pypr__cty, np.uint8)
    qzqb__uuxq = context.get_constant(types.int64, pcd__gsd)
    cdsxy__htg = context.get_constant_generic(builder, char_arr_type,
        rxkl__alxr)
    mzee__qqfcp = context.get_constant_generic(builder, offset_arr_type,
        skj__slbb)
    hbeo__gmwbe = context.get_constant_generic(builder,
        null_bitmap_arr_type, vis__byhlz)
    kpuny__bzrmp = lir.Constant.literal_struct([qzqb__uuxq, cdsxy__htg,
        mzee__qqfcp, hbeo__gmwbe])
    kpuny__bzrmp = cgutils.global_constant(builder, '.const.payload',
        kpuny__bzrmp).bitcast(cgutils.voidptr_t)
    jhr__kbrk = context.get_constant(types.int64, -1)
    eip__pulen = context.get_constant_null(types.voidptr)
    behua__xhcbs = lir.Constant.literal_struct([jhr__kbrk, eip__pulen,
        eip__pulen, kpuny__bzrmp, jhr__kbrk])
    behua__xhcbs = cgutils.global_constant(builder, '.const.meminfo',
        behua__xhcbs).bitcast(cgutils.voidptr_t)
    uxe__pcxz = lir.Constant.literal_struct([behua__xhcbs])
    dqomq__wsrq = lir.Constant.literal_struct([uxe__pcxz])
    return dqomq__wsrq


def pre_alloc_str_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


from numba.parfors.array_analysis import ArrayAnalysis
(ArrayAnalysis._analyze_op_call_bodo_libs_str_arr_ext_pre_alloc_string_array
    ) = pre_alloc_str_arr_equiv


@overload(glob.glob, no_unliteral=True)
def overload_glob_glob(pathname, recursive=False):

    def _glob_glob_impl(pathname, recursive=False):
        with numba.objmode(l='list_str_type'):
            l = glob.glob(pathname, recursive=recursive)
        return l
    return _glob_glob_impl
