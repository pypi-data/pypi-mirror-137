"""Array implementation for map values.
Corresponds to Spark's MapType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Map arrays: https://github.com/apache/arrow/blob/master/format/Schema.fbs

The implementation uses an array(struct) array underneath similar to Spark and Arrow.
For example: [{1: 2.1, 3: 1.1}, {5: -1.0}]
[[{"key": 1, "value" 2.1}, {"key": 3, "value": 1.1}], [{"key": 5, "value": -1.0}]]
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, _get_array_item_arr_payload, offset_type
from bodo.libs.struct_arr_ext import StructArrayType, _get_struct_arr_payload
from bodo.utils.cg_helpers import dict_keys, dict_merge_from_seq2, dict_values, gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit
from bodo.utils.typing import BodoError
from bodo.libs import array_ext, hdist
ll.add_symbol('count_total_elems_list_array', array_ext.
    count_total_elems_list_array)
ll.add_symbol('map_array_from_sequence', array_ext.map_array_from_sequence)
ll.add_symbol('np_array_from_map_array', array_ext.np_array_from_map_array)


class MapArrayType(types.ArrayCompatible):

    def __init__(self, key_arr_type, value_arr_type):
        self.key_arr_type = key_arr_type
        self.value_arr_type = value_arr_type
        super(MapArrayType, self).__init__(name='MapArrayType({}, {})'.
            format(key_arr_type, value_arr_type))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.DictType(self.key_arr_type.dtype, self.value_arr_type.
            dtype)

    def copy(self):
        return MapArrayType(self.key_arr_type, self.value_arr_type)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


def _get_map_arr_data_type(map_type):
    lsvq__ykx = StructArrayType((map_type.key_arr_type, map_type.
        value_arr_type), ('key', 'value'))
    return ArrayItemArrayType(lsvq__ykx)


@register_model(MapArrayType)
class MapArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        uif__drmx = _get_map_arr_data_type(fe_type)
        fgjit__xuz = [('data', uif__drmx)]
        models.StructModel.__init__(self, dmm, fe_type, fgjit__xuz)


make_attribute_wrapper(MapArrayType, 'data', '_data')


@unbox(MapArrayType)
def unbox_map_array(typ, val, c):
    n_maps = bodo.utils.utils.object_length(c, val)
    olr__gxyi = all(isinstance(gmd__vpvj, types.Array) and gmd__vpvj.dtype in
        (types.int64, types.float64, types.bool_, datetime_date_type) for
        gmd__vpvj in (typ.key_arr_type, typ.value_arr_type))
    if olr__gxyi:
        hcbe__eeux = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        ayfi__lhz = cgutils.get_or_insert_function(c.builder.module,
            hcbe__eeux, name='count_total_elems_list_array')
        nvjq__ccqmh = cgutils.pack_array(c.builder, [n_maps, c.builder.call
            (ayfi__lhz, [val])])
    else:
        nvjq__ccqmh = get_array_elem_counts(c, c.builder, c.context, val, typ)
    uif__drmx = _get_map_arr_data_type(typ)
    data_arr = gen_allocate_array(c.context, c.builder, uif__drmx,
        nvjq__ccqmh, c)
    tbihw__exa = _get_array_item_arr_payload(c.context, c.builder,
        uif__drmx, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, tbihw__exa.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, tbihw__exa.offsets).data
    stvwk__hptgn = _get_struct_arr_payload(c.context, c.builder, uif__drmx.
        dtype, tbihw__exa.data)
    key_arr = c.builder.extract_value(stvwk__hptgn.data, 0)
    value_arr = c.builder.extract_value(stvwk__hptgn.data, 1)
    sig = types.none(types.Array(types.uint8, 1, 'C'))
    vqhd__lvefb, hddyn__xxrzc = c.pyapi.call_jit_code(lambda A: A.fill(255),
        sig, [stvwk__hptgn.null_bitmap])
    if olr__gxyi:
        jkhph__gqlk = c.context.make_array(uif__drmx.dtype.data[0])(c.
            context, c.builder, key_arr).data
        tmse__ldex = c.context.make_array(uif__drmx.dtype.data[1])(c.
            context, c.builder, value_arr).data
        hcbe__eeux = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
        vnxc__klm = cgutils.get_or_insert_function(c.builder.module,
            hcbe__eeux, name='map_array_from_sequence')
        rgat__fqzl = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        zndlw__tjuxg = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.
            dtype)
        c.builder.call(vnxc__klm, [val, c.builder.bitcast(jkhph__gqlk, lir.
            IntType(8).as_pointer()), c.builder.bitcast(tmse__ldex, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), rgat__fqzl), lir.Constant(lir.IntType
            (32), zndlw__tjuxg)])
    else:
        _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
            offsets_ptr, null_bitmap_ptr)
    qqbc__ajf = c.context.make_helper(c.builder, typ)
    qqbc__ajf.data = data_arr
    yimv__chej = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(qqbc__ajf._getvalue(), is_error=yimv__chej)


def _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
    offsets_ptr, null_bitmap_ptr):
    from bodo.libs.array_item_arr_ext import _unbox_array_item_array_copy_data
    context = c.context
    builder = c.builder
    surm__pdi = context.insert_const_string(builder.module, 'pandas')
    fmjm__ptn = c.pyapi.import_module_noblock(surm__pdi)
    qkxs__vhhjp = c.pyapi.object_getattr_string(fmjm__ptn, 'NA')
    hfnz__czvx = c.context.get_constant(offset_type, 0)
    builder.store(hfnz__czvx, offsets_ptr)
    uhvbd__hjn = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_maps) as loop:
        iwfk__tlqjo = loop.index
        item_ind = builder.load(uhvbd__hjn)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [iwfk__tlqjo]))
        hlram__brl = seq_getitem(builder, context, val, iwfk__tlqjo)
        set_bitmap_bit(builder, null_bitmap_ptr, iwfk__tlqjo, 0)
        vrin__gsg = is_na_value(builder, context, hlram__brl, qkxs__vhhjp)
        cpjwj__bovbq = builder.icmp_unsigned('!=', vrin__gsg, lir.Constant(
            vrin__gsg.type, 1))
        with builder.if_then(cpjwj__bovbq):
            set_bitmap_bit(builder, null_bitmap_ptr, iwfk__tlqjo, 1)
            xcfv__khzhj = dict_keys(builder, context, hlram__brl)
            qlqn__ati = dict_values(builder, context, hlram__brl)
            n_items = bodo.utils.utils.object_length(c, xcfv__khzhj)
            _unbox_array_item_array_copy_data(typ.key_arr_type, xcfv__khzhj,
                c, key_arr, item_ind, n_items)
            _unbox_array_item_array_copy_data(typ.value_arr_type, qlqn__ati,
                c, value_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), uhvbd__hjn)
            c.pyapi.decref(xcfv__khzhj)
            c.pyapi.decref(qlqn__ati)
        c.pyapi.decref(hlram__brl)
    builder.store(builder.trunc(builder.load(uhvbd__hjn), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_maps]))
    c.pyapi.decref(fmjm__ptn)
    c.pyapi.decref(qkxs__vhhjp)


@box(MapArrayType)
def box_map_arr(typ, val, c):
    qqbc__ajf = c.context.make_helper(c.builder, typ, val)
    data_arr = qqbc__ajf.data
    uif__drmx = _get_map_arr_data_type(typ)
    tbihw__exa = _get_array_item_arr_payload(c.context, c.builder,
        uif__drmx, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, tbihw__exa.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, tbihw__exa.offsets).data
    stvwk__hptgn = _get_struct_arr_payload(c.context, c.builder, uif__drmx.
        dtype, tbihw__exa.data)
    key_arr = c.builder.extract_value(stvwk__hptgn.data, 0)
    value_arr = c.builder.extract_value(stvwk__hptgn.data, 1)
    if all(isinstance(gmd__vpvj, types.Array) and gmd__vpvj.dtype in (types
        .int64, types.float64, types.bool_, datetime_date_type) for
        gmd__vpvj in (typ.key_arr_type, typ.value_arr_type)):
        jkhph__gqlk = c.context.make_array(uif__drmx.dtype.data[0])(c.
            context, c.builder, key_arr).data
        tmse__ldex = c.context.make_array(uif__drmx.dtype.data[1])(c.
            context, c.builder, value_arr).data
        hcbe__eeux = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(offset_type.bitwidth).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(32)])
        bix__njos = cgutils.get_or_insert_function(c.builder.module,
            hcbe__eeux, name='np_array_from_map_array')
        rgat__fqzl = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        zndlw__tjuxg = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.
            dtype)
        arr = c.builder.call(bix__njos, [tbihw__exa.n_arrays, c.builder.
            bitcast(jkhph__gqlk, lir.IntType(8).as_pointer()), c.builder.
            bitcast(tmse__ldex, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), rgat__fqzl), lir
            .Constant(lir.IntType(32), zndlw__tjuxg)])
    else:
        arr = _box_map_array_generic(typ, c, tbihw__exa.n_arrays, key_arr,
            value_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_map_array_generic(typ, c, n_maps, key_arr, value_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    surm__pdi = context.insert_const_string(builder.module, 'numpy')
    mbwbq__bmsvr = c.pyapi.import_module_noblock(surm__pdi)
    vrw__xcs = c.pyapi.object_getattr_string(mbwbq__bmsvr, 'object_')
    zen__osxj = c.pyapi.long_from_longlong(n_maps)
    sgp__fztk = c.pyapi.call_method(mbwbq__bmsvr, 'ndarray', (zen__osxj,
        vrw__xcs))
    txvaj__kgqzg = c.pyapi.object_getattr_string(mbwbq__bmsvr, 'nan')
    izs__jldwy = c.pyapi.unserialize(c.pyapi.serialize_object(zip))
    uhvbd__hjn = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_maps) as loop:
        kstj__poz = loop.index
        pyarray_setitem(builder, context, sgp__fztk, kstj__poz, txvaj__kgqzg)
        kxlab__zazd = get_bitmap_bit(builder, null_bitmap_ptr, kstj__poz)
        vaw__xnk = builder.icmp_unsigned('!=', kxlab__zazd, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(vaw__xnk):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(kstj__poz, lir.Constant(kstj__poz
                .type, 1))])), builder.load(builder.gep(offsets_ptr, [
                kstj__poz]))), lir.IntType(64))
            item_ind = builder.load(uhvbd__hjn)
            hlram__brl = c.pyapi.dict_new()
            slyx__cyy = lambda data_arr, item_ind, n_items: data_arr[item_ind
                :item_ind + n_items]
            vqhd__lvefb, ebu__xexjw = c.pyapi.call_jit_code(slyx__cyy, typ.
                key_arr_type(typ.key_arr_type, types.int64, types.int64), [
                key_arr, item_ind, n_items])
            vqhd__lvefb, wlzuz__tmg = c.pyapi.call_jit_code(slyx__cyy, typ.
                value_arr_type(typ.value_arr_type, types.int64, types.int64
                ), [value_arr, item_ind, n_items])
            vjnk__egig = c.pyapi.from_native_value(typ.key_arr_type,
                ebu__xexjw, c.env_manager)
            zxu__zerm = c.pyapi.from_native_value(typ.value_arr_type,
                wlzuz__tmg, c.env_manager)
            ipgou__cppu = c.pyapi.call_function_objargs(izs__jldwy, (
                vjnk__egig, zxu__zerm))
            dict_merge_from_seq2(builder, context, hlram__brl, ipgou__cppu)
            builder.store(builder.add(item_ind, n_items), uhvbd__hjn)
            pyarray_setitem(builder, context, sgp__fztk, kstj__poz, hlram__brl)
            c.pyapi.decref(ipgou__cppu)
            c.pyapi.decref(vjnk__egig)
            c.pyapi.decref(zxu__zerm)
            c.pyapi.decref(hlram__brl)
    c.pyapi.decref(izs__jldwy)
    c.pyapi.decref(mbwbq__bmsvr)
    c.pyapi.decref(vrw__xcs)
    c.pyapi.decref(zen__osxj)
    c.pyapi.decref(txvaj__kgqzg)
    return sgp__fztk


def init_map_arr_codegen(context, builder, sig, args):
    data_arr, = args
    qqbc__ajf = context.make_helper(builder, sig.return_type)
    qqbc__ajf.data = data_arr
    context.nrt.incref(builder, sig.args[0], data_arr)
    return qqbc__ajf._getvalue()


@intrinsic
def init_map_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType) and isinstance(data_typ
        .dtype, StructArrayType)
    rvtzp__mee = MapArrayType(data_typ.dtype.data[0], data_typ.dtype.data[1])
    return rvtzp__mee(data_typ), init_map_arr_codegen


def alias_ext_init_map_arr(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_map_arr',
    'bodo.libs.map_arr_ext'] = alias_ext_init_map_arr


@numba.njit
def pre_alloc_map_array(num_maps, nested_counts, struct_typ):
    hspa__trjab = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        num_maps, nested_counts, struct_typ)
    return init_map_arr(hspa__trjab)


def pre_alloc_map_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_map_arr_ext_pre_alloc_map_array
    ) = pre_alloc_map_array_equiv


@overload(len, no_unliteral=True)
def overload_map_arr_len(A):
    if isinstance(A, MapArrayType):
        return lambda A: len(A._data)


@overload_attribute(MapArrayType, 'shape')
def overload_map_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(MapArrayType, 'dtype')
def overload_map_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(MapArrayType, 'ndim')
def overload_map_arr_ndim(A):
    return lambda A: 1


@overload_attribute(MapArrayType, 'nbytes')
def overload_map_arr_nbytes(A):
    return lambda A: A._data.nbytes


@overload_method(MapArrayType, 'copy')
def overload_map_arr_copy(A):
    return lambda A: init_map_arr(A._data.copy())


@overload(operator.setitem, no_unliteral=True)
def map_arr_setitem(arr, ind, val):
    if not isinstance(arr, MapArrayType):
        return
    fwonh__ndijg = arr.key_arr_type, arr.value_arr_type
    if isinstance(ind, types.Integer):

        def map_arr_setitem_impl(arr, ind, val):
            bxjp__jom = val.keys()
            iafo__yffy = bodo.libs.struct_arr_ext.pre_alloc_struct_array(len
                (val), (-1,), fwonh__ndijg, ('key', 'value'))
            for vsvw__qndt, xxh__istv in enumerate(bxjp__jom):
                iafo__yffy[vsvw__qndt] = bodo.libs.struct_arr_ext.init_struct((
                    xxh__istv, val[xxh__istv]), ('key', 'value'))
            arr._data[ind] = iafo__yffy
        return map_arr_setitem_impl
    raise BodoError(
        'operator.setitem with MapArrays is only supported with an integer index.'
        )


@overload(operator.getitem, no_unliteral=True)
def map_arr_getitem(arr, ind):
    if not isinstance(arr, MapArrayType):
        return
    if isinstance(ind, types.Integer):

        def map_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            kmymm__ttdh = dict()
            cje__mpv = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            iafo__yffy = bodo.libs.array_item_arr_ext.get_data(arr._data)
            dba__vsolz, kbbu__ajvln = bodo.libs.struct_arr_ext.get_data(
                iafo__yffy)
            ncu__wsqy = cje__mpv[ind]
            cmlme__ukua = cje__mpv[ind + 1]
            for vsvw__qndt in range(ncu__wsqy, cmlme__ukua):
                kmymm__ttdh[dba__vsolz[vsvw__qndt]] = kbbu__ajvln[vsvw__qndt]
            return kmymm__ttdh
        return map_arr_getitem_impl
    raise BodoError(
        'operator.getitem with MapArrays is only supported with an integer index.'
        )
