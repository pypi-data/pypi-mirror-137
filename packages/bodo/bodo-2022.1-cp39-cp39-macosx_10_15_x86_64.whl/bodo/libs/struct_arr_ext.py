"""Array implementation for structs of values.
Corresponds to Spark's StructType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Struct arrays: https://arrow.apache.org/docs/format/Columnar.html

The values are stored in contiguous data arrays; one array per field. For example:
A:             ["AA", "B", "C"]
B:             [1, 2, 4]
"""
import operator
import llvmlite.binding as ll
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import NativeValue, box, intrinsic, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
from numba.typed.typedobjectutils import _cast
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs import array_ext
from bodo.utils.cg_helpers import gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit, to_arr_obj_if_list_obj
from bodo.utils.typing import BodoError, dtype_to_array_type, get_overload_const_int, get_overload_const_str, is_list_like_index_type, is_overload_constant_int, is_overload_constant_str, is_overload_none
ll.add_symbol('struct_array_from_sequence', array_ext.
    struct_array_from_sequence)
ll.add_symbol('np_array_from_struct_array', array_ext.
    np_array_from_struct_array)


class StructArrayType(types.ArrayCompatible):

    def __init__(self, data, names=None):
        assert isinstance(data, tuple) and len(data) > 0 and all(bodo.utils
            .utils.is_array_typ(wkgsd__yqt, False) for wkgsd__yqt in data)
        if names is not None:
            assert isinstance(names, tuple) and all(isinstance(wkgsd__yqt,
                str) for wkgsd__yqt in names) and len(names) == len(data)
        else:
            names = tuple('f{}'.format(i) for i in range(len(data)))
        self.data = data
        self.names = names
        super(StructArrayType, self).__init__(name=
            'StructArrayType({}, {})'.format(data, names))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return StructType(tuple(bte__apzjb.dtype for bte__apzjb in self.
            data), self.names)

    @classmethod
    def from_dict(cls, d):
        assert isinstance(d, dict)
        names = tuple(str(wkgsd__yqt) for wkgsd__yqt in d.keys())
        data = tuple(dtype_to_array_type(bte__apzjb) for bte__apzjb in d.
            values())
        return StructArrayType(data, names)

    def copy(self):
        return StructArrayType(self.data, self.names)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class StructArrayPayloadType(types.Type):

    def __init__(self, data):
        assert isinstance(data, tuple) and all(bodo.utils.utils.
            is_array_typ(wkgsd__yqt, False) for wkgsd__yqt in data)
        self.data = data
        super(StructArrayPayloadType, self).__init__(name=
            'StructArrayPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructArrayPayloadType)
class StructArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        egc__ggmlg = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, egc__ggmlg)


@register_model(StructArrayType)
class StructArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructArrayPayloadType(fe_type.data)
        egc__ggmlg = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, egc__ggmlg)


def define_struct_arr_dtor(context, builder, struct_arr_type, payload_type):
    jbc__pzv = builder.module
    qcojh__dtjoa = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    pfju__nxg = cgutils.get_or_insert_function(jbc__pzv, qcojh__dtjoa, name
        ='.dtor.struct_arr.{}.{}.'.format(struct_arr_type.data,
        struct_arr_type.names))
    if not pfju__nxg.is_declaration:
        return pfju__nxg
    pfju__nxg.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(pfju__nxg.append_basic_block())
    fksmf__mdy = pfju__nxg.args[0]
    ezp__kpaf = context.get_value_type(payload_type).as_pointer()
    qjr__tduy = builder.bitcast(fksmf__mdy, ezp__kpaf)
    mvfc__dhrv = context.make_helper(builder, payload_type, ref=qjr__tduy)
    context.nrt.decref(builder, types.BaseTuple.from_types(struct_arr_type.
        data), mvfc__dhrv.data)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        mvfc__dhrv.null_bitmap)
    builder.ret_void()
    return pfju__nxg


def construct_struct_array(context, builder, struct_arr_type, n_structs,
    n_elems, c=None):
    payload_type = StructArrayPayloadType(struct_arr_type.data)
    pmfo__gtge = context.get_value_type(payload_type)
    mkgkn__mwfd = context.get_abi_sizeof(pmfo__gtge)
    edl__sbkv = define_struct_arr_dtor(context, builder, struct_arr_type,
        payload_type)
    xnvmr__olta = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, mkgkn__mwfd), edl__sbkv)
    ruq__dqb = context.nrt.meminfo_data(builder, xnvmr__olta)
    oeggo__epwp = builder.bitcast(ruq__dqb, pmfo__gtge.as_pointer())
    mvfc__dhrv = cgutils.create_struct_proxy(payload_type)(context, builder)
    eug__npjld = []
    lsll__xvpz = 0
    for arr_typ in struct_arr_type.data:
        ytvuj__saos = bodo.utils.transform.get_type_alloc_counts(arr_typ.dtype)
        smd__muqtw = cgutils.pack_array(builder, [n_structs] + [builder.
            extract_value(n_elems, i) for i in range(lsll__xvpz, lsll__xvpz +
            ytvuj__saos)])
        arr = gen_allocate_array(context, builder, arr_typ, smd__muqtw, c)
        eug__npjld.append(arr)
        lsll__xvpz += ytvuj__saos
    mvfc__dhrv.data = cgutils.pack_array(builder, eug__npjld
        ) if types.is_homogeneous(*struct_arr_type.data
        ) else cgutils.pack_struct(builder, eug__npjld)
    eegy__ykcr = builder.udiv(builder.add(n_structs, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    gqr__bqk = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [eegy__ykcr])
    null_bitmap_ptr = gqr__bqk.data
    mvfc__dhrv.null_bitmap = gqr__bqk._getvalue()
    builder.store(mvfc__dhrv._getvalue(), oeggo__epwp)
    return xnvmr__olta, mvfc__dhrv.data, null_bitmap_ptr


def _get_C_API_ptrs(c, data_tup, data_typ, names):
    pekfb__zzmwh = []
    assert len(data_typ) > 0
    for i, arr_typ in enumerate(data_typ):
        nit__slvzk = c.builder.extract_value(data_tup, i)
        arr = c.context.make_array(arr_typ)(c.context, c.builder, value=
            nit__slvzk)
        pekfb__zzmwh.append(arr.data)
    klt__vum = cgutils.pack_array(c.builder, pekfb__zzmwh
        ) if types.is_homogeneous(*data_typ) else cgutils.pack_struct(c.
        builder, pekfb__zzmwh)
    ryugg__pct = cgutils.alloca_once_value(c.builder, klt__vum)
    aine__obl = [c.context.get_constant(types.int32, bodo.utils.utils.
        numba_to_c_type(wkgsd__yqt.dtype)) for wkgsd__yqt in data_typ]
    kvqo__zgjcd = cgutils.alloca_once_value(c.builder, cgutils.pack_array(c
        .builder, aine__obl))
    zlz__sau = cgutils.pack_array(c.builder, [c.context.insert_const_string
        (c.builder.module, wkgsd__yqt) for wkgsd__yqt in names])
    bwlf__hewt = cgutils.alloca_once_value(c.builder, zlz__sau)
    return ryugg__pct, kvqo__zgjcd, bwlf__hewt


@unbox(StructArrayType)
def unbox_struct_array(typ, val, c, is_tuple_array=False):
    from bodo.libs.tuple_arr_ext import TupleArrayType
    n_structs = bodo.utils.utils.object_length(c, val)
    inr__gzpm = all(isinstance(bte__apzjb, types.Array) and bte__apzjb.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for bte__apzjb in typ.data)
    if inr__gzpm:
        n_elems = cgutils.pack_array(c.builder, [], lir.IntType(64))
    else:
        dxn__jem = get_array_elem_counts(c, c.builder, c.context, val, 
            TupleArrayType(typ.data) if is_tuple_array else typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            dxn__jem, i) for i in range(1, dxn__jem.type.count)], lir.
            IntType(64))
    xnvmr__olta, data_tup, null_bitmap_ptr = construct_struct_array(c.
        context, c.builder, typ, n_structs, n_elems, c)
    if inr__gzpm:
        ryugg__pct, kvqo__zgjcd, bwlf__hewt = _get_C_API_ptrs(c, data_tup,
            typ.data, typ.names)
        qcojh__dtjoa = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1)])
        pfju__nxg = cgutils.get_or_insert_function(c.builder.module,
            qcojh__dtjoa, name='struct_array_from_sequence')
        c.builder.call(pfju__nxg, [val, c.context.get_constant(types.int32,
            len(typ.data)), c.builder.bitcast(ryugg__pct, lir.IntType(8).
            as_pointer()), null_bitmap_ptr, c.builder.bitcast(kvqo__zgjcd,
            lir.IntType(8).as_pointer()), c.builder.bitcast(bwlf__hewt, lir
            .IntType(8).as_pointer()), c.context.get_constant(types.bool_,
            is_tuple_array)])
    else:
        _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
            null_bitmap_ptr, is_tuple_array)
    wsb__vmts = c.context.make_helper(c.builder, typ)
    wsb__vmts.meminfo = xnvmr__olta
    ojwl__wsirh = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(wsb__vmts._getvalue(), is_error=ojwl__wsirh)


def _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    gofds__fgmzg = context.insert_const_string(builder.module, 'pandas')
    fxpl__bllll = c.pyapi.import_module_noblock(gofds__fgmzg)
    repng__wzl = c.pyapi.object_getattr_string(fxpl__bllll, 'NA')
    with cgutils.for_range(builder, n_structs) as loop:
        dlduu__hjjio = loop.index
        mrpaj__hubfh = seq_getitem(builder, context, val, dlduu__hjjio)
        set_bitmap_bit(builder, null_bitmap_ptr, dlduu__hjjio, 0)
        for adl__guws in range(len(typ.data)):
            arr_typ = typ.data[adl__guws]
            data_arr = builder.extract_value(data_tup, adl__guws)

            def set_na(data_arr, i):
                bodo.libs.array_kernels.setna(data_arr, i)
            sig = types.none(arr_typ, types.int64)
            taz__noczq, dld__ylw = c.pyapi.call_jit_code(set_na, sig, [
                data_arr, dlduu__hjjio])
        yolq__zuxij = is_na_value(builder, context, mrpaj__hubfh, repng__wzl)
        fxibu__ekh = builder.icmp_unsigned('!=', yolq__zuxij, lir.Constant(
            yolq__zuxij.type, 1))
        with builder.if_then(fxibu__ekh):
            set_bitmap_bit(builder, null_bitmap_ptr, dlduu__hjjio, 1)
            for adl__guws in range(len(typ.data)):
                arr_typ = typ.data[adl__guws]
                if is_tuple_array:
                    mny__gqq = c.pyapi.tuple_getitem(mrpaj__hubfh, adl__guws)
                else:
                    mny__gqq = c.pyapi.dict_getitem_string(mrpaj__hubfh,
                        typ.names[adl__guws])
                yolq__zuxij = is_na_value(builder, context, mny__gqq,
                    repng__wzl)
                fxibu__ekh = builder.icmp_unsigned('!=', yolq__zuxij, lir.
                    Constant(yolq__zuxij.type, 1))
                with builder.if_then(fxibu__ekh):
                    mny__gqq = to_arr_obj_if_list_obj(c, context, builder,
                        mny__gqq, arr_typ.dtype)
                    field_val = c.pyapi.to_native_value(arr_typ.dtype, mny__gqq
                        ).value
                    data_arr = builder.extract_value(data_tup, adl__guws)

                    def set_data(data_arr, i, field_val):
                        data_arr[i] = field_val
                    sig = types.none(arr_typ, types.int64, arr_typ.dtype)
                    taz__noczq, dld__ylw = c.pyapi.call_jit_code(set_data,
                        sig, [data_arr, dlduu__hjjio, field_val])
                    c.context.nrt.decref(builder, arr_typ.dtype, field_val)
        c.pyapi.decref(mrpaj__hubfh)
    c.pyapi.decref(fxpl__bllll)
    c.pyapi.decref(repng__wzl)


def _get_struct_arr_payload(context, builder, arr_typ, arr):
    wsb__vmts = context.make_helper(builder, arr_typ, arr)
    payload_type = StructArrayPayloadType(arr_typ.data)
    ruq__dqb = context.nrt.meminfo_data(builder, wsb__vmts.meminfo)
    oeggo__epwp = builder.bitcast(ruq__dqb, context.get_value_type(
        payload_type).as_pointer())
    mvfc__dhrv = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(oeggo__epwp))
    return mvfc__dhrv


@box(StructArrayType)
def box_struct_arr(typ, val, c, is_tuple_array=False):
    mvfc__dhrv = _get_struct_arr_payload(c.context, c.builder, typ, val)
    taz__noczq, length = c.pyapi.call_jit_code(lambda A: len(A), types.
        int64(typ), [val])
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), mvfc__dhrv.null_bitmap).data
    inr__gzpm = all(isinstance(bte__apzjb, types.Array) and bte__apzjb.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for bte__apzjb in typ.data)
    if inr__gzpm:
        ryugg__pct, kvqo__zgjcd, bwlf__hewt = _get_C_API_ptrs(c, mvfc__dhrv
            .data, typ.data, typ.names)
        qcojh__dtjoa = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        iyv__gnd = cgutils.get_or_insert_function(c.builder.module,
            qcojh__dtjoa, name='np_array_from_struct_array')
        arr = c.builder.call(iyv__gnd, [length, c.context.get_constant(
            types.int32, len(typ.data)), c.builder.bitcast(ryugg__pct, lir.
            IntType(8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(
            kvqo__zgjcd, lir.IntType(8).as_pointer()), c.builder.bitcast(
            bwlf__hewt, lir.IntType(8).as_pointer()), c.context.
            get_constant(types.bool_, is_tuple_array)])
    else:
        arr = _box_struct_array_generic(typ, c, length, mvfc__dhrv.data,
            null_bitmap_ptr, is_tuple_array)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_struct_array_generic(typ, c, length, data_arrs_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    gofds__fgmzg = context.insert_const_string(builder.module, 'numpy')
    ibkf__dhc = c.pyapi.import_module_noblock(gofds__fgmzg)
    dfzgx__qpb = c.pyapi.object_getattr_string(ibkf__dhc, 'object_')
    gbba__ammy = c.pyapi.long_from_longlong(length)
    hjmo__bhf = c.pyapi.call_method(ibkf__dhc, 'ndarray', (gbba__ammy,
        dfzgx__qpb))
    aknaf__dgwf = c.pyapi.object_getattr_string(ibkf__dhc, 'nan')
    with cgutils.for_range(builder, length) as loop:
        dlduu__hjjio = loop.index
        pyarray_setitem(builder, context, hjmo__bhf, dlduu__hjjio, aknaf__dgwf)
        ukzg__why = get_bitmap_bit(builder, null_bitmap_ptr, dlduu__hjjio)
        zjrp__nypg = builder.icmp_unsigned('!=', ukzg__why, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(zjrp__nypg):
            if is_tuple_array:
                mrpaj__hubfh = c.pyapi.tuple_new(len(typ.data))
            else:
                mrpaj__hubfh = c.pyapi.dict_new(len(typ.data))
            for i, arr_typ in enumerate(typ.data):
                if is_tuple_array:
                    c.pyapi.incref(aknaf__dgwf)
                    c.pyapi.tuple_setitem(mrpaj__hubfh, i, aknaf__dgwf)
                else:
                    c.pyapi.dict_setitem_string(mrpaj__hubfh, typ.names[i],
                        aknaf__dgwf)
                data_arr = c.builder.extract_value(data_arrs_tup, i)
                taz__noczq, lwv__kht = c.pyapi.call_jit_code(lambda
                    data_arr, ind: not bodo.libs.array_kernels.isna(
                    data_arr, ind), types.bool_(arr_typ, types.int64), [
                    data_arr, dlduu__hjjio])
                with builder.if_then(lwv__kht):
                    taz__noczq, field_val = c.pyapi.call_jit_code(lambda
                        data_arr, ind: data_arr[ind], arr_typ.dtype(arr_typ,
                        types.int64), [data_arr, dlduu__hjjio])
                    tggf__ssu = c.pyapi.from_native_value(arr_typ.dtype,
                        field_val, c.env_manager)
                    if is_tuple_array:
                        c.pyapi.tuple_setitem(mrpaj__hubfh, i, tggf__ssu)
                    else:
                        c.pyapi.dict_setitem_string(mrpaj__hubfh, typ.names
                            [i], tggf__ssu)
                        c.pyapi.decref(tggf__ssu)
            pyarray_setitem(builder, context, hjmo__bhf, dlduu__hjjio,
                mrpaj__hubfh)
            c.pyapi.decref(mrpaj__hubfh)
    c.pyapi.decref(ibkf__dhc)
    c.pyapi.decref(dfzgx__qpb)
    c.pyapi.decref(gbba__ammy)
    c.pyapi.decref(aknaf__dgwf)
    return hjmo__bhf


def _fix_nested_counts(nested_counts, struct_arr_type, nested_counts_type,
    builder):
    nzfxa__dijvb = bodo.utils.transform.get_type_alloc_counts(struct_arr_type
        ) - 1
    if nzfxa__dijvb == 0:
        return nested_counts
    if not isinstance(nested_counts_type, types.UniTuple):
        nested_counts = cgutils.pack_array(builder, [lir.Constant(lir.
            IntType(64), -1) for pps__gsm in range(nzfxa__dijvb)])
    elif nested_counts_type.count < nzfxa__dijvb:
        nested_counts = cgutils.pack_array(builder, [builder.extract_value(
            nested_counts, i) for i in range(nested_counts_type.count)] + [
            lir.Constant(lir.IntType(64), -1) for pps__gsm in range(
            nzfxa__dijvb - nested_counts_type.count)])
    return nested_counts


@intrinsic
def pre_alloc_struct_array(typingctx, num_structs_typ, nested_counts_typ,
    dtypes_typ, names_typ=None):
    assert isinstance(num_structs_typ, types.Integer) and isinstance(dtypes_typ
        , types.BaseTuple)
    if is_overload_none(names_typ):
        names = tuple(f'f{i}' for i in range(len(dtypes_typ)))
    else:
        names = tuple(get_overload_const_str(bte__apzjb) for bte__apzjb in
            names_typ.types)
    irrw__oov = tuple(bte__apzjb.instance_type for bte__apzjb in dtypes_typ
        .types)
    struct_arr_type = StructArrayType(irrw__oov, names)

    def codegen(context, builder, sig, args):
        oqhpd__opjso, nested_counts, pps__gsm, pps__gsm = args
        nested_counts_type = sig.args[1]
        nested_counts = _fix_nested_counts(nested_counts, struct_arr_type,
            nested_counts_type, builder)
        xnvmr__olta, pps__gsm, pps__gsm = construct_struct_array(context,
            builder, struct_arr_type, oqhpd__opjso, nested_counts)
        wsb__vmts = context.make_helper(builder, struct_arr_type)
        wsb__vmts.meminfo = xnvmr__olta
        return wsb__vmts._getvalue()
    return struct_arr_type(num_structs_typ, nested_counts_typ, dtypes_typ,
        names_typ), codegen


def pre_alloc_struct_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 4 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_struct_arr_ext_pre_alloc_struct_array
    ) = pre_alloc_struct_array_equiv


class StructType(types.Type):

    def __init__(self, data, names):
        assert isinstance(data, tuple) and len(data) > 0
        assert isinstance(names, tuple) and all(isinstance(wkgsd__yqt, str) for
            wkgsd__yqt in names) and len(names) == len(data)
        self.data = data
        self.names = names
        super(StructType, self).__init__(name='StructType({}, {})'.format(
            data, names))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class StructPayloadType(types.Type):

    def __init__(self, data):
        assert isinstance(data, tuple)
        self.data = data
        super(StructPayloadType, self).__init__(name=
            'StructPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructPayloadType)
class StructPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        egc__ggmlg = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.UniTuple(types.int8, len(fe_type.data)))]
        models.StructModel.__init__(self, dmm, fe_type, egc__ggmlg)


@register_model(StructType)
class StructModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructPayloadType(fe_type.data)
        egc__ggmlg = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, egc__ggmlg)


def define_struct_dtor(context, builder, struct_type, payload_type):
    jbc__pzv = builder.module
    qcojh__dtjoa = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    pfju__nxg = cgutils.get_or_insert_function(jbc__pzv, qcojh__dtjoa, name
        ='.dtor.struct.{}.{}.'.format(struct_type.data, struct_type.names))
    if not pfju__nxg.is_declaration:
        return pfju__nxg
    pfju__nxg.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(pfju__nxg.append_basic_block())
    fksmf__mdy = pfju__nxg.args[0]
    ezp__kpaf = context.get_value_type(payload_type).as_pointer()
    qjr__tduy = builder.bitcast(fksmf__mdy, ezp__kpaf)
    mvfc__dhrv = context.make_helper(builder, payload_type, ref=qjr__tduy)
    for i in range(len(struct_type.data)):
        jomh__adscp = builder.extract_value(mvfc__dhrv.null_bitmap, i)
        zjrp__nypg = builder.icmp_unsigned('==', jomh__adscp, lir.Constant(
            jomh__adscp.type, 1))
        with builder.if_then(zjrp__nypg):
            val = builder.extract_value(mvfc__dhrv.data, i)
            context.nrt.decref(builder, struct_type.data[i], val)
    builder.ret_void()
    return pfju__nxg


def _get_struct_payload(context, builder, typ, struct):
    struct = context.make_helper(builder, typ, struct)
    payload_type = StructPayloadType(typ.data)
    ruq__dqb = context.nrt.meminfo_data(builder, struct.meminfo)
    oeggo__epwp = builder.bitcast(ruq__dqb, context.get_value_type(
        payload_type).as_pointer())
    mvfc__dhrv = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(oeggo__epwp))
    return mvfc__dhrv, oeggo__epwp


@unbox(StructType)
def unbox_struct(typ, val, c):
    context = c.context
    builder = c.builder
    gofds__fgmzg = context.insert_const_string(builder.module, 'pandas')
    fxpl__bllll = c.pyapi.import_module_noblock(gofds__fgmzg)
    repng__wzl = c.pyapi.object_getattr_string(fxpl__bllll, 'NA')
    uyy__iyg = []
    nulls = []
    for i, bte__apzjb in enumerate(typ.data):
        tggf__ssu = c.pyapi.dict_getitem_string(val, typ.names[i])
        xwbp__qxfxc = cgutils.alloca_once_value(c.builder, context.
            get_constant(types.uint8, 0))
        njuoh__kag = cgutils.alloca_once_value(c.builder, cgutils.
            get_null_value(context.get_value_type(bte__apzjb)))
        yolq__zuxij = is_na_value(builder, context, tggf__ssu, repng__wzl)
        zjrp__nypg = builder.icmp_unsigned('!=', yolq__zuxij, lir.Constant(
            yolq__zuxij.type, 1))
        with builder.if_then(zjrp__nypg):
            builder.store(context.get_constant(types.uint8, 1), xwbp__qxfxc)
            field_val = c.pyapi.to_native_value(bte__apzjb, tggf__ssu).value
            builder.store(field_val, njuoh__kag)
        uyy__iyg.append(builder.load(njuoh__kag))
        nulls.append(builder.load(xwbp__qxfxc))
    c.pyapi.decref(fxpl__bllll)
    c.pyapi.decref(repng__wzl)
    xnvmr__olta = construct_struct(context, builder, typ, uyy__iyg, nulls)
    struct = context.make_helper(builder, typ)
    struct.meminfo = xnvmr__olta
    ojwl__wsirh = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(struct._getvalue(), is_error=ojwl__wsirh)


@box(StructType)
def box_struct(typ, val, c):
    vnu__iqow = c.pyapi.dict_new(len(typ.data))
    mvfc__dhrv, pps__gsm = _get_struct_payload(c.context, c.builder, typ, val)
    assert len(typ.data) > 0
    for i, val_typ in enumerate(typ.data):
        c.pyapi.dict_setitem_string(vnu__iqow, typ.names[i], c.pyapi.
            borrow_none())
        jomh__adscp = c.builder.extract_value(mvfc__dhrv.null_bitmap, i)
        zjrp__nypg = c.builder.icmp_unsigned('==', jomh__adscp, lir.
            Constant(jomh__adscp.type, 1))
        with c.builder.if_then(zjrp__nypg):
            tkou__pinf = c.builder.extract_value(mvfc__dhrv.data, i)
            c.context.nrt.incref(c.builder, val_typ, tkou__pinf)
            mny__gqq = c.pyapi.from_native_value(val_typ, tkou__pinf, c.
                env_manager)
            c.pyapi.dict_setitem_string(vnu__iqow, typ.names[i], mny__gqq)
            c.pyapi.decref(mny__gqq)
    c.context.nrt.decref(c.builder, typ, val)
    return vnu__iqow


@intrinsic
def init_struct(typingctx, data_typ, names_typ=None):
    names = tuple(get_overload_const_str(bte__apzjb) for bte__apzjb in
        names_typ.types)
    struct_type = StructType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, jag__wmo = args
        payload_type = StructPayloadType(struct_type.data)
        pmfo__gtge = context.get_value_type(payload_type)
        mkgkn__mwfd = context.get_abi_sizeof(pmfo__gtge)
        edl__sbkv = define_struct_dtor(context, builder, struct_type,
            payload_type)
        xnvmr__olta = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, mkgkn__mwfd), edl__sbkv)
        ruq__dqb = context.nrt.meminfo_data(builder, xnvmr__olta)
        oeggo__epwp = builder.bitcast(ruq__dqb, pmfo__gtge.as_pointer())
        mvfc__dhrv = cgutils.create_struct_proxy(payload_type)(context, builder
            )
        mvfc__dhrv.data = data
        mvfc__dhrv.null_bitmap = cgutils.pack_array(builder, [context.
            get_constant(types.uint8, 1) for pps__gsm in range(len(data_typ
            .types))])
        builder.store(mvfc__dhrv._getvalue(), oeggo__epwp)
        context.nrt.incref(builder, data_typ, data)
        struct = context.make_helper(builder, struct_type)
        struct.meminfo = xnvmr__olta
        return struct._getvalue()
    return struct_type(data_typ, names_typ), codegen


@intrinsic
def get_struct_data(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        mvfc__dhrv, pps__gsm = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            mvfc__dhrv.data)
    return types.BaseTuple.from_types(struct_typ.data)(struct_typ), codegen


@intrinsic
def get_struct_null_bitmap(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        mvfc__dhrv, pps__gsm = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            mvfc__dhrv.null_bitmap)
    xdiic__bjk = types.UniTuple(types.int8, len(struct_typ.data))
    return xdiic__bjk(struct_typ), codegen


@intrinsic
def set_struct_data(typingctx, struct_typ, field_ind_typ, val_typ=None):
    assert isinstance(struct_typ, StructType) and is_overload_constant_int(
        field_ind_typ)
    field_ind = get_overload_const_int(field_ind_typ)

    def codegen(context, builder, sig, args):
        struct, pps__gsm, val = args
        mvfc__dhrv, oeggo__epwp = _get_struct_payload(context, builder,
            struct_typ, struct)
        zsaoa__koa = mvfc__dhrv.data
        kdj__vkvog = builder.insert_value(zsaoa__koa, val, field_ind)
        dncr__casai = types.BaseTuple.from_types(struct_typ.data)
        context.nrt.decref(builder, dncr__casai, zsaoa__koa)
        context.nrt.incref(builder, dncr__casai, kdj__vkvog)
        mvfc__dhrv.data = kdj__vkvog
        builder.store(mvfc__dhrv._getvalue(), oeggo__epwp)
        return context.get_dummy_value()
    return types.none(struct_typ, field_ind_typ, val_typ), codegen


def _get_struct_field_ind(struct, ind, op):
    if not is_overload_constant_str(ind):
        raise BodoError(
            'structs (from struct array) only support constant strings for {}, not {}'
            .format(op, ind))
    zkbfy__cwm = get_overload_const_str(ind)
    if zkbfy__cwm not in struct.names:
        raise BodoError('Field {} does not exist in struct {}'.format(
            zkbfy__cwm, struct))
    return struct.names.index(zkbfy__cwm)


def is_field_value_null(s, field_name):
    pass


@overload(is_field_value_null, no_unliteral=True)
def overload_is_field_value_null(s, field_name):
    field_ind = _get_struct_field_ind(s, field_name, 'element access (getitem)'
        )
    return lambda s, field_name: get_struct_null_bitmap(s)[field_ind] == 0


@overload(operator.getitem, no_unliteral=True)
def struct_getitem(struct, ind):
    if not isinstance(struct, StructType):
        return
    field_ind = _get_struct_field_ind(struct, ind, 'element access (getitem)')
    return lambda struct, ind: get_struct_data(struct)[field_ind]


@overload(operator.setitem, no_unliteral=True)
def struct_setitem(struct, ind, val):
    if not isinstance(struct, StructType):
        return
    field_ind = _get_struct_field_ind(struct, ind, 'item assignment (setitem)')
    field_typ = struct.data[field_ind]
    return lambda struct, ind, val: set_struct_data(struct, field_ind,
        _cast(val, field_typ))


@overload(len, no_unliteral=True)
def overload_struct_arr_len(struct):
    if isinstance(struct, StructType):
        num_fields = len(struct.data)
        return lambda struct: num_fields


def construct_struct(context, builder, struct_type, values, nulls):
    payload_type = StructPayloadType(struct_type.data)
    pmfo__gtge = context.get_value_type(payload_type)
    mkgkn__mwfd = context.get_abi_sizeof(pmfo__gtge)
    edl__sbkv = define_struct_dtor(context, builder, struct_type, payload_type)
    xnvmr__olta = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, mkgkn__mwfd), edl__sbkv)
    ruq__dqb = context.nrt.meminfo_data(builder, xnvmr__olta)
    oeggo__epwp = builder.bitcast(ruq__dqb, pmfo__gtge.as_pointer())
    mvfc__dhrv = cgutils.create_struct_proxy(payload_type)(context, builder)
    mvfc__dhrv.data = cgutils.pack_array(builder, values
        ) if types.is_homogeneous(*struct_type.data) else cgutils.pack_struct(
        builder, values)
    mvfc__dhrv.null_bitmap = cgutils.pack_array(builder, nulls)
    builder.store(mvfc__dhrv._getvalue(), oeggo__epwp)
    return xnvmr__olta


@intrinsic
def struct_array_get_struct(typingctx, struct_arr_typ, ind_typ=None):
    assert isinstance(struct_arr_typ, StructArrayType) and isinstance(ind_typ,
        types.Integer)
    tbd__otuzi = tuple(d.dtype for d in struct_arr_typ.data)
    vmhx__lizck = StructType(tbd__otuzi, struct_arr_typ.names)

    def codegen(context, builder, sig, args):
        gdoyi__xnsu, ind = args
        mvfc__dhrv = _get_struct_arr_payload(context, builder,
            struct_arr_typ, gdoyi__xnsu)
        uyy__iyg = []
        ihpux__urhe = []
        for i, arr_typ in enumerate(struct_arr_typ.data):
            nit__slvzk = builder.extract_value(mvfc__dhrv.data, i)
            hhllp__mgmo = context.compile_internal(builder, lambda arr, ind:
                np.uint8(0) if bodo.libs.array_kernels.isna(arr, ind) else
                np.uint8(1), types.uint8(arr_typ, types.int64), [nit__slvzk,
                ind])
            ihpux__urhe.append(hhllp__mgmo)
            qgsu__fancv = cgutils.alloca_once_value(builder, context.
                get_constant_null(arr_typ.dtype))
            zjrp__nypg = builder.icmp_unsigned('==', hhllp__mgmo, lir.
                Constant(hhllp__mgmo.type, 1))
            with builder.if_then(zjrp__nypg):
                hsoz__wez = context.compile_internal(builder, lambda arr,
                    ind: arr[ind], arr_typ.dtype(arr_typ, types.int64), [
                    nit__slvzk, ind])
                builder.store(hsoz__wez, qgsu__fancv)
            uyy__iyg.append(builder.load(qgsu__fancv))
        if isinstance(vmhx__lizck, types.DictType):
            cgfaa__djk = [context.insert_const_string(builder.module,
                wvwd__whlu) for wvwd__whlu in struct_arr_typ.names]
            jcvx__tts = cgutils.pack_array(builder, uyy__iyg)
            wngz__vnc = cgutils.pack_array(builder, cgfaa__djk)

            def impl(names, vals):
                d = {}
                for i, wvwd__whlu in enumerate(names):
                    d[wvwd__whlu] = vals[i]
                return d
            sbzm__toqmk = context.compile_internal(builder, impl,
                vmhx__lizck(types.Tuple(tuple(types.StringLiteral(
                wvwd__whlu) for wvwd__whlu in struct_arr_typ.names)), types
                .Tuple(tbd__otuzi)), [wngz__vnc, jcvx__tts])
            context.nrt.decref(builder, types.BaseTuple.from_types(
                tbd__otuzi), jcvx__tts)
            return sbzm__toqmk
        xnvmr__olta = construct_struct(context, builder, vmhx__lizck,
            uyy__iyg, ihpux__urhe)
        struct = context.make_helper(builder, vmhx__lizck)
        struct.meminfo = xnvmr__olta
        return struct._getvalue()
    return vmhx__lizck(struct_arr_typ, ind_typ), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        mvfc__dhrv = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            mvfc__dhrv.data)
    return types.BaseTuple.from_types(arr_typ.data)(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        mvfc__dhrv = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            mvfc__dhrv.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


@intrinsic
def init_struct_arr(typingctx, data_typ, null_bitmap_typ, names_typ=None):
    names = tuple(get_overload_const_str(bte__apzjb) for bte__apzjb in
        names_typ.types)
    struct_arr_type = StructArrayType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, gqr__bqk, jag__wmo = args
        payload_type = StructArrayPayloadType(struct_arr_type.data)
        pmfo__gtge = context.get_value_type(payload_type)
        mkgkn__mwfd = context.get_abi_sizeof(pmfo__gtge)
        edl__sbkv = define_struct_arr_dtor(context, builder,
            struct_arr_type, payload_type)
        xnvmr__olta = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, mkgkn__mwfd), edl__sbkv)
        ruq__dqb = context.nrt.meminfo_data(builder, xnvmr__olta)
        oeggo__epwp = builder.bitcast(ruq__dqb, pmfo__gtge.as_pointer())
        mvfc__dhrv = cgutils.create_struct_proxy(payload_type)(context, builder
            )
        mvfc__dhrv.data = data
        mvfc__dhrv.null_bitmap = gqr__bqk
        builder.store(mvfc__dhrv._getvalue(), oeggo__epwp)
        context.nrt.incref(builder, data_typ, data)
        context.nrt.incref(builder, null_bitmap_typ, gqr__bqk)
        wsb__vmts = context.make_helper(builder, struct_arr_type)
        wsb__vmts.meminfo = xnvmr__olta
        return wsb__vmts._getvalue()
    return struct_arr_type(data_typ, null_bitmap_typ, names_typ), codegen


@overload(operator.getitem, no_unliteral=True)
def struct_arr_getitem(arr, ind):
    if not isinstance(arr, StructArrayType):
        return
    if isinstance(ind, types.Integer):

        def struct_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            return struct_array_get_struct(arr, ind)
        return struct_arr_getitem_impl
    yfavs__kuv = len(arr.data)
    dujz__oqalj = 'def impl(arr, ind):\n'
    dujz__oqalj += '  data = get_data(arr)\n'
    dujz__oqalj += '  null_bitmap = get_null_bitmap(arr)\n'
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        dujz__oqalj += """  out_null_bitmap = get_new_null_mask_bool_index(null_bitmap, ind, len(data[0]))
"""
    elif is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        dujz__oqalj += """  out_null_bitmap = get_new_null_mask_int_index(null_bitmap, ind, len(data[0]))
"""
    elif isinstance(ind, types.SliceType):
        dujz__oqalj += """  out_null_bitmap = get_new_null_mask_slice_index(null_bitmap, ind, len(data[0]))
"""
    else:
        raise BodoError('invalid index {} in struct array indexing'.format(ind)
            )
    dujz__oqalj += ('  return init_struct_arr(({},), out_null_bitmap, ({},))\n'
        .format(', '.join('ensure_contig_if_np(data[{}][ind])'.format(i) for
        i in range(yfavs__kuv)), ', '.join("'{}'".format(wvwd__whlu) for
        wvwd__whlu in arr.names)))
    uqr__bub = {}
    exec(dujz__oqalj, {'init_struct_arr': init_struct_arr, 'get_data':
        get_data, 'get_null_bitmap': get_null_bitmap, 'ensure_contig_if_np':
        bodo.utils.conversion.ensure_contig_if_np,
        'get_new_null_mask_bool_index': bodo.utils.indexing.
        get_new_null_mask_bool_index, 'get_new_null_mask_int_index': bodo.
        utils.indexing.get_new_null_mask_int_index,
        'get_new_null_mask_slice_index': bodo.utils.indexing.
        get_new_null_mask_slice_index}, uqr__bub)
    impl = uqr__bub['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def struct_arr_setitem(arr, ind, val):
    if not isinstance(arr, StructArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if isinstance(ind, types.Integer):
        yfavs__kuv = len(arr.data)
        dujz__oqalj = 'def impl(arr, ind, val):\n'
        dujz__oqalj += '  data = get_data(arr)\n'
        dujz__oqalj += '  null_bitmap = get_null_bitmap(arr)\n'
        dujz__oqalj += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for i in range(yfavs__kuv):
            if isinstance(val, StructType):
                dujz__oqalj += "  if is_field_value_null(val, '{}'):\n".format(
                    arr.names[i])
                dujz__oqalj += (
                    '    bodo.libs.array_kernels.setna(data[{}], ind)\n'.
                    format(i))
                dujz__oqalj += '  else:\n'
                dujz__oqalj += "    data[{}][ind] = val['{}']\n".format(i,
                    arr.names[i])
            else:
                dujz__oqalj += "  data[{}][ind] = val['{}']\n".format(i,
                    arr.names[i])
        uqr__bub = {}
        exec(dujz__oqalj, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'is_field_value_null':
            is_field_value_null}, uqr__bub)
        impl = uqr__bub['impl']
        return impl
    if isinstance(ind, types.SliceType):
        yfavs__kuv = len(arr.data)
        dujz__oqalj = 'def impl(arr, ind, val):\n'
        dujz__oqalj += '  data = get_data(arr)\n'
        dujz__oqalj += '  null_bitmap = get_null_bitmap(arr)\n'
        dujz__oqalj += '  val_data = get_data(val)\n'
        dujz__oqalj += '  val_null_bitmap = get_null_bitmap(val)\n'
        dujz__oqalj += """  setitem_slice_index_null_bits(null_bitmap, val_null_bitmap, ind, len(arr))
"""
        for i in range(yfavs__kuv):
            dujz__oqalj += '  data[{0}][ind] = val_data[{0}]\n'.format(i)
        uqr__bub = {}
        exec(dujz__oqalj, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'setitem_slice_index_null_bits':
            bodo.utils.indexing.setitem_slice_index_null_bits}, uqr__bub)
        impl = uqr__bub['impl']
        return impl
    raise BodoError(
        'only setitem with scalar/slice index is currently supported for struct arrays'
        )


@overload(len, no_unliteral=True)
def overload_struct_arr_len(A):
    if isinstance(A, StructArrayType):
        return lambda A: len(get_data(A)[0])


@overload_attribute(StructArrayType, 'shape')
def overload_struct_arr_shape(A):
    return lambda A: (len(get_data(A)[0]),)


@overload_attribute(StructArrayType, 'dtype')
def overload_struct_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(StructArrayType, 'ndim')
def overload_struct_arr_ndim(A):
    return lambda A: 1


@overload_attribute(StructArrayType, 'nbytes')
def overload_struct_arr_nbytes(A):
    dujz__oqalj = 'def impl(A):\n'
    dujz__oqalj += '  total_nbytes = 0\n'
    dujz__oqalj += '  data = get_data(A)\n'
    for i in range(len(A.data)):
        dujz__oqalj += f'  total_nbytes += data[{i}].nbytes\n'
    dujz__oqalj += '  total_nbytes += get_null_bitmap(A).nbytes\n'
    dujz__oqalj += '  return total_nbytes\n'
    uqr__bub = {}
    exec(dujz__oqalj, {'get_data': get_data, 'get_null_bitmap':
        get_null_bitmap}, uqr__bub)
    impl = uqr__bub['impl']
    return impl


@overload_method(StructArrayType, 'copy', no_unliteral=True)
def overload_struct_arr_copy(A):
    names = A.names

    def copy_impl(A):
        data = get_data(A)
        gqr__bqk = get_null_bitmap(A)
        gtrpm__elsmc = bodo.ir.join.copy_arr_tup(data)
        isy__srqfv = gqr__bqk.copy()
        return init_struct_arr(gtrpm__elsmc, isy__srqfv, names)
    return copy_impl
