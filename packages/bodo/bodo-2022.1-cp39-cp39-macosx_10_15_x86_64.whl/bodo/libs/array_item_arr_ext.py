"""Array implementation for variable-size array items.
Corresponds to Spark's ArrayType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Variable-size List: https://arrow.apache.org/docs/format/Columnar.html

The values are stored in a contingous data array, while an offsets array marks the
individual arrays. For example:
value:             [[1, 2], [3], None, [5, 4, 6], []]
data:              [1, 2, 3, 5, 4, 6]
offsets:           [0, 2, 3, 3, 6, 6]
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import NativeValue, box, intrinsic, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs import array_ext
from bodo.utils.cg_helpers import gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit, to_arr_obj_if_list_obj
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.typing import BodoError, is_iterable_type, is_list_like_index_type
ll.add_symbol('count_total_elems_list_array', array_ext.
    count_total_elems_list_array)
ll.add_symbol('array_item_array_from_sequence', array_ext.
    array_item_array_from_sequence)
ll.add_symbol('np_array_from_array_item_array', array_ext.
    np_array_from_array_item_array)
offset_type = types.uint64
np_offset_type = numba.np.numpy_support.as_dtype(offset_type)


class ArrayItemArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        assert bodo.utils.utils.is_array_typ(dtype, False)
        self.dtype = dtype
        super(ArrayItemArrayType, self).__init__(name=
            'ArrayItemArrayType({})'.format(dtype))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return ArrayItemArrayType(self.dtype)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class ArrayItemArrayPayloadType(types.Type):

    def __init__(self, array_type):
        self.array_type = array_type
        super(ArrayItemArrayPayloadType, self).__init__(name=
            'ArrayItemArrayPayloadType({})'.format(array_type))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(ArrayItemArrayPayloadType)
class ArrayItemArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        sejw__wknx = [('n_arrays', types.int64), ('data', fe_type.
            array_type.dtype), ('offsets', types.Array(offset_type, 1, 'C')
            ), ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, sejw__wknx)


@register_model(ArrayItemArrayType)
class ArrayItemArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = ArrayItemArrayPayloadType(fe_type)
        sejw__wknx = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, sejw__wknx)


def define_array_item_dtor(context, builder, array_item_type, payload_type):
    ezlo__efa = builder.module
    hvzbn__okhlj = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    fba__jaqdv = cgutils.get_or_insert_function(ezlo__efa, hvzbn__okhlj,
        name='.dtor.array_item.{}'.format(array_item_type.dtype))
    if not fba__jaqdv.is_declaration:
        return fba__jaqdv
    fba__jaqdv.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(fba__jaqdv.append_basic_block())
    rohbj__cgsx = fba__jaqdv.args[0]
    ctni__sso = context.get_value_type(payload_type).as_pointer()
    cciv__erz = builder.bitcast(rohbj__cgsx, ctni__sso)
    dde__hkzdz = context.make_helper(builder, payload_type, ref=cciv__erz)
    context.nrt.decref(builder, array_item_type.dtype, dde__hkzdz.data)
    context.nrt.decref(builder, types.Array(offset_type, 1, 'C'),
        dde__hkzdz.offsets)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        dde__hkzdz.null_bitmap)
    builder.ret_void()
    return fba__jaqdv


def construct_array_item_array(context, builder, array_item_type, n_arrays,
    n_elems, c=None):
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    gulg__hzalg = context.get_value_type(payload_type)
    rphhn__dee = context.get_abi_sizeof(gulg__hzalg)
    geb__zwwbk = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    oqcwi__hpgh = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, rphhn__dee), geb__zwwbk)
    htq__wtlof = context.nrt.meminfo_data(builder, oqcwi__hpgh)
    tuzas__njo = builder.bitcast(htq__wtlof, gulg__hzalg.as_pointer())
    dde__hkzdz = cgutils.create_struct_proxy(payload_type)(context, builder)
    dde__hkzdz.n_arrays = n_arrays
    olvp__zcm = n_elems.type.count
    qeca__qir = builder.extract_value(n_elems, 0)
    blhx__tvx = cgutils.alloca_once_value(builder, qeca__qir)
    cnv__bywr = builder.icmp_signed('==', qeca__qir, lir.Constant(qeca__qir
        .type, -1))
    with builder.if_then(cnv__bywr):
        builder.store(n_arrays, blhx__tvx)
    n_elems = cgutils.pack_array(builder, [builder.load(blhx__tvx)] + [
        builder.extract_value(n_elems, adzfl__umegz) for adzfl__umegz in
        range(1, olvp__zcm)])
    dde__hkzdz.data = gen_allocate_array(context, builder, array_item_type.
        dtype, n_elems, c)
    bqbn__xjr = builder.add(n_arrays, lir.Constant(lir.IntType(64), 1))
    soqcp__brd = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(offset_type, 1, 'C'), [bqbn__xjr])
    offsets_ptr = soqcp__brd.data
    builder.store(context.get_constant(offset_type, 0), offsets_ptr)
    builder.store(builder.trunc(builder.extract_value(n_elems, 0), lir.
        IntType(offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    dde__hkzdz.offsets = soqcp__brd._getvalue()
    ysol__xlxb = builder.udiv(builder.add(n_arrays, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    jrvcw__aiu = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [ysol__xlxb])
    null_bitmap_ptr = jrvcw__aiu.data
    dde__hkzdz.null_bitmap = jrvcw__aiu._getvalue()
    builder.store(dde__hkzdz._getvalue(), tuzas__njo)
    return oqcwi__hpgh, dde__hkzdz.data, offsets_ptr, null_bitmap_ptr


def _unbox_array_item_array_copy_data(arr_typ, arr_obj, c, data_arr,
    item_ind, n_items):
    context = c.context
    builder = c.builder
    arr_obj = to_arr_obj_if_list_obj(c, context, builder, arr_obj, arr_typ)
    arr_val = c.pyapi.to_native_value(arr_typ, arr_obj).value
    sig = types.none(arr_typ, types.int64, types.int64, arr_typ)

    def copy_data(data_arr, item_ind, n_items, arr_val):
        data_arr[item_ind:item_ind + n_items] = arr_val
    joz__emu, ymn__otboo = c.pyapi.call_jit_code(copy_data, sig, [data_arr,
        item_ind, n_items, arr_val])
    c.context.nrt.decref(builder, arr_typ, arr_val)


def _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
    offsets_ptr, null_bitmap_ptr):
    context = c.context
    builder = c.builder
    felc__ofqor = context.insert_const_string(builder.module, 'pandas')
    cnv__sfb = c.pyapi.import_module_noblock(felc__ofqor)
    nca__kwkx = c.pyapi.object_getattr_string(cnv__sfb, 'NA')
    cpwk__kfi = c.context.get_constant(offset_type, 0)
    builder.store(cpwk__kfi, offsets_ptr)
    tog__ejl = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_arrays) as loop:
        ycf__qdb = loop.index
        item_ind = builder.load(tog__ejl)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [ycf__qdb]))
        arr_obj = seq_getitem(builder, context, val, ycf__qdb)
        set_bitmap_bit(builder, null_bitmap_ptr, ycf__qdb, 0)
        vaw__dtexa = is_na_value(builder, context, arr_obj, nca__kwkx)
        ijob__xuqgh = builder.icmp_unsigned('!=', vaw__dtexa, lir.Constant(
            vaw__dtexa.type, 1))
        with builder.if_then(ijob__xuqgh):
            set_bitmap_bit(builder, null_bitmap_ptr, ycf__qdb, 1)
            n_items = bodo.utils.utils.object_length(c, arr_obj)
            _unbox_array_item_array_copy_data(typ.dtype, arr_obj, c,
                data_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), tog__ejl)
        c.pyapi.decref(arr_obj)
    builder.store(builder.trunc(builder.load(tog__ejl), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    c.pyapi.decref(cnv__sfb)
    c.pyapi.decref(nca__kwkx)


@unbox(ArrayItemArrayType)
def unbox_array_item_array(typ, val, c):
    abv__zap = isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types
        .int64, types.float64, types.bool_, datetime_date_type)
    n_arrays = bodo.utils.utils.object_length(c, val)
    if abv__zap:
        hvzbn__okhlj = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        dav__fruax = cgutils.get_or_insert_function(c.builder.module,
            hvzbn__okhlj, name='count_total_elems_list_array')
        n_elems = cgutils.pack_array(c.builder, [c.builder.call(dav__fruax,
            [val])])
    else:
        iltac__ndjpp = get_array_elem_counts(c, c.builder, c.context, val, typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            iltac__ndjpp, adzfl__umegz) for adzfl__umegz in range(1,
            iltac__ndjpp.type.count)])
    oqcwi__hpgh, data_arr, offsets_ptr, null_bitmap_ptr = (
        construct_array_item_array(c.context, c.builder, typ, n_arrays,
        n_elems, c))
    if abv__zap:
        clgpz__gwp = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        dqr__udfz = c.context.make_array(typ.dtype)(c.context, c.builder,
            data_arr).data
        hvzbn__okhlj = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(32)])
        fba__jaqdv = cgutils.get_or_insert_function(c.builder.module,
            hvzbn__okhlj, name='array_item_array_from_sequence')
        c.builder.call(fba__jaqdv, [val, c.builder.bitcast(dqr__udfz, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), clgpz__gwp)])
    else:
        _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
            offsets_ptr, null_bitmap_ptr)
    unrbm__knc = c.context.make_helper(c.builder, typ)
    unrbm__knc.meminfo = oqcwi__hpgh
    fwfyf__mes = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(unrbm__knc._getvalue(), is_error=fwfyf__mes)


def _get_array_item_arr_payload(context, builder, arr_typ, arr):
    unrbm__knc = context.make_helper(builder, arr_typ, arr)
    payload_type = ArrayItemArrayPayloadType(arr_typ)
    htq__wtlof = context.nrt.meminfo_data(builder, unrbm__knc.meminfo)
    tuzas__njo = builder.bitcast(htq__wtlof, context.get_value_type(
        payload_type).as_pointer())
    dde__hkzdz = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(tuzas__njo))
    return dde__hkzdz


def _box_array_item_array_generic(typ, c, n_arrays, data_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    felc__ofqor = context.insert_const_string(builder.module, 'numpy')
    irp__dabu = c.pyapi.import_module_noblock(felc__ofqor)
    xycsf__jened = c.pyapi.object_getattr_string(irp__dabu, 'object_')
    ald__juusj = c.pyapi.long_from_longlong(n_arrays)
    poqss__vqco = c.pyapi.call_method(irp__dabu, 'ndarray', (ald__juusj,
        xycsf__jened))
    zxu__rlbt = c.pyapi.object_getattr_string(irp__dabu, 'nan')
    tog__ejl = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType(
        64), 0))
    with cgutils.for_range(builder, n_arrays) as loop:
        ycf__qdb = loop.index
        pyarray_setitem(builder, context, poqss__vqco, ycf__qdb, zxu__rlbt)
        nhbe__dqoz = get_bitmap_bit(builder, null_bitmap_ptr, ycf__qdb)
        wgw__osdn = builder.icmp_unsigned('!=', nhbe__dqoz, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(wgw__osdn):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(ycf__qdb, lir.Constant(ycf__qdb.
                type, 1))])), builder.load(builder.gep(offsets_ptr, [
                ycf__qdb]))), lir.IntType(64))
            item_ind = builder.load(tog__ejl)
            joz__emu, moenf__cfcbo = c.pyapi.call_jit_code(lambda data_arr,
                item_ind, n_items: data_arr[item_ind:item_ind + n_items],
                typ.dtype(typ.dtype, types.int64, types.int64), [data_arr,
                item_ind, n_items])
            builder.store(builder.add(item_ind, n_items), tog__ejl)
            arr_obj = c.pyapi.from_native_value(typ.dtype, moenf__cfcbo, c.
                env_manager)
            pyarray_setitem(builder, context, poqss__vqco, ycf__qdb, arr_obj)
            c.pyapi.decref(arr_obj)
    c.pyapi.decref(irp__dabu)
    c.pyapi.decref(xycsf__jened)
    c.pyapi.decref(ald__juusj)
    c.pyapi.decref(zxu__rlbt)
    return poqss__vqco


@box(ArrayItemArrayType)
def box_array_item_arr(typ, val, c):
    dde__hkzdz = _get_array_item_arr_payload(c.context, c.builder, typ, val)
    data_arr = dde__hkzdz.data
    offsets_ptr = c.context.make_helper(c.builder, types.Array(offset_type,
        1, 'C'), dde__hkzdz.offsets).data
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), dde__hkzdz.null_bitmap).data
    if isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type):
        clgpz__gwp = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        dqr__udfz = c.context.make_helper(c.builder, typ.dtype, data_arr).data
        hvzbn__okhlj = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32)])
        vvkb__pnqh = cgutils.get_or_insert_function(c.builder.module,
            hvzbn__okhlj, name='np_array_from_array_item_array')
        arr = c.builder.call(vvkb__pnqh, [dde__hkzdz.n_arrays, c.builder.
            bitcast(dqr__udfz, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), clgpz__gwp)])
    else:
        arr = _box_array_item_array_generic(typ, c, dde__hkzdz.n_arrays,
            data_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def lower_pre_alloc_array_item_array(context, builder, sig, args):
    array_item_type = sig.return_type
    oqt__wzha, tftfe__sjg, yov__tcch = args
    deanu__oxygz = bodo.utils.transform.get_type_alloc_counts(array_item_type
        .dtype)
    shhww__kgecq = sig.args[1]
    if not isinstance(shhww__kgecq, types.UniTuple):
        tftfe__sjg = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), -1) for yov__tcch in range(deanu__oxygz)])
    elif shhww__kgecq.count < deanu__oxygz:
        tftfe__sjg = cgutils.pack_array(builder, [builder.extract_value(
            tftfe__sjg, adzfl__umegz) for adzfl__umegz in range(
            shhww__kgecq.count)] + [lir.Constant(lir.IntType(64), -1) for
            yov__tcch in range(deanu__oxygz - shhww__kgecq.count)])
    oqcwi__hpgh, yov__tcch, yov__tcch, yov__tcch = construct_array_item_array(
        context, builder, array_item_type, oqt__wzha, tftfe__sjg)
    unrbm__knc = context.make_helper(builder, array_item_type)
    unrbm__knc.meminfo = oqcwi__hpgh
    return unrbm__knc._getvalue()


@intrinsic
def pre_alloc_array_item_array(typingctx, num_arrs_typ, num_values_typ,
    dtype_typ=None):
    assert isinstance(num_arrs_typ, types.Integer)
    array_item_type = ArrayItemArrayType(dtype_typ.instance_type)
    num_values_typ = types.unliteral(num_values_typ)
    return array_item_type(types.int64, num_values_typ, dtype_typ
        ), lower_pre_alloc_array_item_array


def pre_alloc_array_item_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_libs_array_item_arr_ext_pre_alloc_array_item_array
    ) = pre_alloc_array_item_array_equiv


def init_array_item_array_codegen(context, builder, signature, args):
    n_arrays, djudi__kza, soqcp__brd, jrvcw__aiu = args
    array_item_type = signature.return_type
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    gulg__hzalg = context.get_value_type(payload_type)
    rphhn__dee = context.get_abi_sizeof(gulg__hzalg)
    geb__zwwbk = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    oqcwi__hpgh = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, rphhn__dee), geb__zwwbk)
    htq__wtlof = context.nrt.meminfo_data(builder, oqcwi__hpgh)
    tuzas__njo = builder.bitcast(htq__wtlof, gulg__hzalg.as_pointer())
    dde__hkzdz = cgutils.create_struct_proxy(payload_type)(context, builder)
    dde__hkzdz.n_arrays = n_arrays
    dde__hkzdz.data = djudi__kza
    dde__hkzdz.offsets = soqcp__brd
    dde__hkzdz.null_bitmap = jrvcw__aiu
    builder.store(dde__hkzdz._getvalue(), tuzas__njo)
    context.nrt.incref(builder, signature.args[1], djudi__kza)
    context.nrt.incref(builder, signature.args[2], soqcp__brd)
    context.nrt.incref(builder, signature.args[3], jrvcw__aiu)
    unrbm__knc = context.make_helper(builder, array_item_type)
    unrbm__knc.meminfo = oqcwi__hpgh
    return unrbm__knc._getvalue()


@intrinsic
def init_array_item_array(typingctx, n_arrays_typ, data_type, offsets_typ,
    null_bitmap_typ=None):
    assert null_bitmap_typ == types.Array(types.uint8, 1, 'C')
    gcip__aiy = ArrayItemArrayType(data_type)
    sig = gcip__aiy(types.int64, data_type, offsets_typ, null_bitmap_typ)
    return sig, init_array_item_array_codegen


@intrinsic
def get_offsets(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        dde__hkzdz = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return impl_ret_borrowed(context, builder, sig.return_type,
            dde__hkzdz.offsets)
    return types.Array(offset_type, 1, 'C')(arr_typ), codegen


@intrinsic
def get_offsets_ind(typingctx, arr_typ, ind_t=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, ind = args
        dde__hkzdz = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        dqr__udfz = context.make_array(types.Array(offset_type, 1, 'C'))(
            context, builder, dde__hkzdz.offsets).data
        soqcp__brd = builder.bitcast(dqr__udfz, lir.IntType(offset_type.
            bitwidth).as_pointer())
        return builder.load(builder.gep(soqcp__brd, [ind]))
    return offset_type(arr_typ, types.int64), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        dde__hkzdz = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return impl_ret_borrowed(context, builder, sig.return_type,
            dde__hkzdz.data)
    return arr_typ.dtype(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        dde__hkzdz = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return impl_ret_borrowed(context, builder, sig.return_type,
            dde__hkzdz.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


def alias_ext_single_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_offsets',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array
numba.core.ir_utils.alias_func_extensions['get_data',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array
numba.core.ir_utils.alias_func_extensions['get_null_bitmap',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array


@intrinsic
def get_n_arrays(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        dde__hkzdz = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return dde__hkzdz.n_arrays
    return types.int64(arr_typ), codegen


@intrinsic
def replace_data_arr(typingctx, arr_typ, data_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType
        ) and data_typ == arr_typ.dtype

    def codegen(context, builder, sig, args):
        arr, ezewv__pxdg = args
        unrbm__knc = context.make_helper(builder, arr_typ, arr)
        payload_type = ArrayItemArrayPayloadType(arr_typ)
        htq__wtlof = context.nrt.meminfo_data(builder, unrbm__knc.meminfo)
        tuzas__njo = builder.bitcast(htq__wtlof, context.get_value_type(
            payload_type).as_pointer())
        dde__hkzdz = cgutils.create_struct_proxy(payload_type)(context,
            builder, builder.load(tuzas__njo))
        context.nrt.decref(builder, data_typ, dde__hkzdz.data)
        dde__hkzdz.data = ezewv__pxdg
        context.nrt.incref(builder, data_typ, ezewv__pxdg)
        builder.store(dde__hkzdz._getvalue(), tuzas__njo)
    return types.none(arr_typ, data_typ), codegen


@numba.njit(no_cpython_wrapper=True)
def ensure_data_capacity(arr, old_size, new_size):
    djudi__kza = get_data(arr)
    ygoji__lnhi = len(djudi__kza)
    if ygoji__lnhi < new_size:
        ruzp__fdupv = max(2 * ygoji__lnhi, new_size)
        ezewv__pxdg = bodo.libs.array_kernels.resize_and_copy(djudi__kza,
            old_size, ruzp__fdupv)
        replace_data_arr(arr, ezewv__pxdg)


@numba.njit(no_cpython_wrapper=True)
def trim_excess_data(arr):
    djudi__kza = get_data(arr)
    soqcp__brd = get_offsets(arr)
    qtt__ljhg = len(djudi__kza)
    erxt__liy = soqcp__brd[-1]
    if qtt__ljhg != erxt__liy:
        ezewv__pxdg = bodo.libs.array_kernels.resize_and_copy(djudi__kza,
            erxt__liy, erxt__liy)
        replace_data_arr(arr, ezewv__pxdg)


@overload(len, no_unliteral=True)
def overload_array_item_arr_len(A):
    if isinstance(A, ArrayItemArrayType):
        return lambda A: get_n_arrays(A)


@overload_attribute(ArrayItemArrayType, 'shape')
def overload_array_item_arr_shape(A):
    return lambda A: (get_n_arrays(A),)


@overload_attribute(ArrayItemArrayType, 'dtype')
def overload_array_item_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(ArrayItemArrayType, 'ndim')
def overload_array_item_arr_ndim(A):
    return lambda A: 1


@overload_attribute(ArrayItemArrayType, 'nbytes')
def overload_array_item_arr_nbytes(A):
    return lambda A: get_data(A).nbytes + get_offsets(A
        ).nbytes + get_null_bitmap(A).nbytes


@overload(operator.getitem, no_unliteral=True)
def array_item_arr_getitem_array(arr, ind):
    if not isinstance(arr, ArrayItemArrayType):
        return
    if isinstance(ind, types.Integer):

        def array_item_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            soqcp__brd = get_offsets(arr)
            djudi__kza = get_data(arr)
            btxew__rorm = soqcp__brd[ind]
            oad__tzgw = soqcp__brd[ind + 1]
            return djudi__kza[btxew__rorm:oad__tzgw]
        return array_item_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        uza__vynob = arr.dtype

        def impl_bool(arr, ind):
            zjwl__qvjf = len(arr)
            if zjwl__qvjf != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            jrvcw__aiu = get_null_bitmap(arr)
            n_arrays = 0
            fifb__iplf = init_nested_counts(uza__vynob)
            for adzfl__umegz in range(zjwl__qvjf):
                if ind[adzfl__umegz]:
                    n_arrays += 1
                    zdzms__nvu = arr[adzfl__umegz]
                    fifb__iplf = add_nested_counts(fifb__iplf, zdzms__nvu)
            poqss__vqco = pre_alloc_array_item_array(n_arrays, fifb__iplf,
                uza__vynob)
            hgbzb__otd = get_null_bitmap(poqss__vqco)
            cgmtd__ajcd = 0
            for puded__xltqr in range(zjwl__qvjf):
                if ind[puded__xltqr]:
                    poqss__vqco[cgmtd__ajcd] = arr[puded__xltqr]
                    ijj__rtd = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        jrvcw__aiu, puded__xltqr)
                    bodo.libs.int_arr_ext.set_bit_to_arr(hgbzb__otd,
                        cgmtd__ajcd, ijj__rtd)
                    cgmtd__ajcd += 1
            return poqss__vqco
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        uza__vynob = arr.dtype

        def impl_int(arr, ind):
            jrvcw__aiu = get_null_bitmap(arr)
            zjwl__qvjf = len(ind)
            n_arrays = zjwl__qvjf
            fifb__iplf = init_nested_counts(uza__vynob)
            for ytitn__zopm in range(zjwl__qvjf):
                adzfl__umegz = ind[ytitn__zopm]
                zdzms__nvu = arr[adzfl__umegz]
                fifb__iplf = add_nested_counts(fifb__iplf, zdzms__nvu)
            poqss__vqco = pre_alloc_array_item_array(n_arrays, fifb__iplf,
                uza__vynob)
            hgbzb__otd = get_null_bitmap(poqss__vqco)
            for hhzx__atw in range(zjwl__qvjf):
                puded__xltqr = ind[hhzx__atw]
                poqss__vqco[hhzx__atw] = arr[puded__xltqr]
                ijj__rtd = bodo.libs.int_arr_ext.get_bit_bitmap_arr(jrvcw__aiu,
                    puded__xltqr)
                bodo.libs.int_arr_ext.set_bit_to_arr(hgbzb__otd, hhzx__atw,
                    ijj__rtd)
            return poqss__vqco
        return impl_int
    if isinstance(ind, types.SliceType):

        def impl_slice(arr, ind):
            zjwl__qvjf = len(arr)
            huq__npv = numba.cpython.unicode._normalize_slice(ind, zjwl__qvjf)
            vzowa__zjdgs = np.arange(huq__npv.start, huq__npv.stop,
                huq__npv.step)
            return arr[vzowa__zjdgs]
        return impl_slice


@overload(operator.setitem)
def array_item_arr_setitem(A, idx, val):
    if not isinstance(A, ArrayItemArrayType):
        return
    if isinstance(idx, types.Integer):

        def impl_scalar(A, idx, val):
            soqcp__brd = get_offsets(A)
            jrvcw__aiu = get_null_bitmap(A)
            if idx == 0:
                soqcp__brd[0] = 0
            n_items = len(val)
            dtb__tcb = soqcp__brd[idx] + n_items
            ensure_data_capacity(A, soqcp__brd[idx], dtb__tcb)
            djudi__kza = get_data(A)
            soqcp__brd[idx + 1] = soqcp__brd[idx] + n_items
            djudi__kza[soqcp__brd[idx]:soqcp__brd[idx + 1]] = val
            bodo.libs.int_arr_ext.set_bit_to_arr(jrvcw__aiu, idx, 1)
        return impl_scalar
    if isinstance(idx, types.SliceType) and A.dtype == val:

        def impl_slice_elem(A, idx, val):
            huq__npv = numba.cpython.unicode._normalize_slice(idx, len(A))
            for adzfl__umegz in range(huq__npv.start, huq__npv.stop,
                huq__npv.step):
                A[adzfl__umegz] = val
        return impl_slice_elem
    if isinstance(idx, types.SliceType) and is_iterable_type(val):

        def impl_slice(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            soqcp__brd = get_offsets(A)
            jrvcw__aiu = get_null_bitmap(A)
            undat__baqms = get_offsets(val)
            tuf__gtsm = get_data(val)
            ofx__swx = get_null_bitmap(val)
            zjwl__qvjf = len(A)
            huq__npv = numba.cpython.unicode._normalize_slice(idx, zjwl__qvjf)
            eegkl__wjdux, zjk__zqk = huq__npv.start, huq__npv.stop
            assert huq__npv.step == 1
            if eegkl__wjdux == 0:
                soqcp__brd[eegkl__wjdux] = 0
            zyyq__alrsq = soqcp__brd[eegkl__wjdux]
            dtb__tcb = zyyq__alrsq + len(tuf__gtsm)
            ensure_data_capacity(A, zyyq__alrsq, dtb__tcb)
            djudi__kza = get_data(A)
            djudi__kza[zyyq__alrsq:zyyq__alrsq + len(tuf__gtsm)] = tuf__gtsm
            soqcp__brd[eegkl__wjdux:zjk__zqk + 1] = undat__baqms + zyyq__alrsq
            ruwi__ual = 0
            for adzfl__umegz in range(eegkl__wjdux, zjk__zqk):
                ijj__rtd = bodo.libs.int_arr_ext.get_bit_bitmap_arr(ofx__swx,
                    ruwi__ual)
                bodo.libs.int_arr_ext.set_bit_to_arr(jrvcw__aiu,
                    adzfl__umegz, ijj__rtd)
                ruwi__ual += 1
        return impl_slice
    raise BodoError(
        'only setitem with scalar index is currently supported for list arrays'
        )


@overload_method(ArrayItemArrayType, 'copy', no_unliteral=True)
def overload_array_item_arr_copy(A):

    def copy_impl(A):
        return init_array_item_array(len(A), get_data(A).copy(),
            get_offsets(A).copy(), get_null_bitmap(A).copy())
    return copy_impl
