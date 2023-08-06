"""Tools for handling bodo arrays, e.g. passing to C/C++ code
"""
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.typing.templates import signature
from numba.cpython.listobj import ListInstance
from numba.extending import intrinsic, models, register_model
from numba.np.arrayobj import _getitem_array_single_int
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, get_categories_int_type
from bodo.libs import array_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayPayloadType, ArrayItemArrayType, _get_array_item_arr_payload, define_array_item_dtor, offset_type
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType, int128_type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType, _get_map_arr_data_type, init_map_arr_codegen
from bodo.libs.str_arr_ext import _get_str_binary_arr_payload, char_arr_type, null_bitmap_arr_type, offset_arr_type, string_array_type
from bodo.libs.struct_arr_ext import StructArrayPayloadType, StructArrayType, StructType, _get_struct_arr_payload, define_struct_arr_dtor
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoError, MetaType
from bodo.utils.utils import CTypeEnum, check_and_propagate_cpp_exception, numba_to_c_type
ll.add_symbol('list_string_array_to_info', array_ext.list_string_array_to_info)
ll.add_symbol('nested_array_to_info', array_ext.nested_array_to_info)
ll.add_symbol('string_array_to_info', array_ext.string_array_to_info)
ll.add_symbol('numpy_array_to_info', array_ext.numpy_array_to_info)
ll.add_symbol('categorical_array_to_info', array_ext.categorical_array_to_info)
ll.add_symbol('nullable_array_to_info', array_ext.nullable_array_to_info)
ll.add_symbol('interval_array_to_info', array_ext.interval_array_to_info)
ll.add_symbol('decimal_array_to_info', array_ext.decimal_array_to_info)
ll.add_symbol('info_to_nested_array', array_ext.info_to_nested_array)
ll.add_symbol('info_to_list_string_array', array_ext.info_to_list_string_array)
ll.add_symbol('info_to_string_array', array_ext.info_to_string_array)
ll.add_symbol('info_to_numpy_array', array_ext.info_to_numpy_array)
ll.add_symbol('info_to_nullable_array', array_ext.info_to_nullable_array)
ll.add_symbol('info_to_interval_array', array_ext.info_to_interval_array)
ll.add_symbol('alloc_numpy', array_ext.alloc_numpy)
ll.add_symbol('alloc_string_array', array_ext.alloc_string_array)
ll.add_symbol('arr_info_list_to_table', array_ext.arr_info_list_to_table)
ll.add_symbol('info_from_table', array_ext.info_from_table)
ll.add_symbol('delete_info_decref_array', array_ext.delete_info_decref_array)
ll.add_symbol('delete_table_decref_arrays', array_ext.
    delete_table_decref_arrays)
ll.add_symbol('delete_table', array_ext.delete_table)
ll.add_symbol('shuffle_table', array_ext.shuffle_table)
ll.add_symbol('get_shuffle_info', array_ext.get_shuffle_info)
ll.add_symbol('delete_shuffle_info', array_ext.delete_shuffle_info)
ll.add_symbol('reverse_shuffle_table', array_ext.reverse_shuffle_table)
ll.add_symbol('hash_join_table', array_ext.hash_join_table)
ll.add_symbol('drop_duplicates_table', array_ext.drop_duplicates_table)
ll.add_symbol('sort_values_table', array_ext.sort_values_table)
ll.add_symbol('sample_table', array_ext.sample_table)
ll.add_symbol('shuffle_renormalization', array_ext.shuffle_renormalization)
ll.add_symbol('shuffle_renormalization_group', array_ext.
    shuffle_renormalization_group)
ll.add_symbol('groupby_and_aggregate', array_ext.groupby_and_aggregate)
ll.add_symbol('pivot_groupby_and_aggregate', array_ext.
    pivot_groupby_and_aggregate)
ll.add_symbol('get_groupby_labels', array_ext.get_groupby_labels)
ll.add_symbol('array_isin', array_ext.array_isin)
ll.add_symbol('get_search_regex', array_ext.get_search_regex)
ll.add_symbol('compute_node_partition_by_hash', array_ext.
    compute_node_partition_by_hash)
ll.add_symbol('array_info_getitem', array_ext.array_info_getitem)


class ArrayInfoType(types.Type):

    def __init__(self):
        super(ArrayInfoType, self).__init__(name='ArrayInfoType()')


array_info_type = ArrayInfoType()
register_model(ArrayInfoType)(models.OpaqueModel)


class TableTypeCPP(types.Type):

    def __init__(self):
        super(TableTypeCPP, self).__init__(name='TableTypeCPP()')


table_type = TableTypeCPP()
register_model(TableTypeCPP)(models.OpaqueModel)


@intrinsic
def array_to_info(typingctx, arr_type_t=None):
    return array_info_type(arr_type_t), array_to_info_codegen


def array_to_info_codegen(context, builder, sig, args):
    in_arr, = args
    arr_type = sig.args[0]
    if isinstance(arr_type, TupleArrayType):
        zfthl__jepc = context.make_helper(builder, arr_type, in_arr)
        in_arr = zfthl__jepc.data
        arr_type = StructArrayType(arr_type.data, ('dummy',) * len(arr_type
            .data))
    context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        wsqjq__eujm = context.make_helper(builder, arr_type, in_arr)
        abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        obn__sjzj = cgutils.get_or_insert_function(builder.module,
            abpxx__qvrpn, name='list_string_array_to_info')
        return builder.call(obn__sjzj, [wsqjq__eujm.meminfo])
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType, StructArrayType)
        ):

        def get_types(arr_typ):
            if isinstance(arr_typ, MapArrayType):
                return get_types(_get_map_arr_data_type(arr_typ))
            elif isinstance(arr_typ, ArrayItemArrayType):
                return [CTypeEnum.LIST.value] + get_types(arr_typ.dtype)
            elif isinstance(arr_typ, (StructType, StructArrayType)):
                beidz__xjg = [CTypeEnum.STRUCT.value, len(arr_typ.names)]
                for qixai__btzrn in arr_typ.data:
                    beidz__xjg += get_types(qixai__btzrn)
                return beidz__xjg
            elif isinstance(arr_typ, (types.Array, IntegerArrayType)
                ) or arr_typ == boolean_array:
                return get_types(arr_typ.dtype)
            elif arr_typ == string_array_type:
                return [CTypeEnum.STRING.value]
            elif arr_typ == binary_array_type:
                return [CTypeEnum.BINARY.value]
            elif isinstance(arr_typ, DecimalArrayType):
                return [CTypeEnum.Decimal.value, arr_typ.precision, arr_typ
                    .scale]
            else:
                return [numba_to_c_type(arr_typ)]

        def get_lengths(arr_typ, arr):
            zmzi__rup = context.compile_internal(builder, lambda a: len(a),
                types.intp(arr_typ), [arr])
            if isinstance(arr_typ, MapArrayType):
                zayq__wwo = context.make_helper(builder, arr_typ, value=arr)
                vxzx__onhm = get_lengths(_get_map_arr_data_type(arr_typ),
                    zayq__wwo.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                udo__hocv = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                vxzx__onhm = get_lengths(arr_typ.dtype, udo__hocv.data)
                vxzx__onhm = cgutils.pack_array(builder, [udo__hocv.
                    n_arrays] + [builder.extract_value(vxzx__onhm,
                    jlzqa__krsau) for jlzqa__krsau in range(vxzx__onhm.type
                    .count)])
            elif isinstance(arr_typ, StructArrayType):
                udo__hocv = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                vxzx__onhm = []
                for jlzqa__krsau, qixai__btzrn in enumerate(arr_typ.data):
                    fmuwu__tzbek = get_lengths(qixai__btzrn, builder.
                        extract_value(udo__hocv.data, jlzqa__krsau))
                    vxzx__onhm += [builder.extract_value(fmuwu__tzbek,
                        gkzvs__smhry) for gkzvs__smhry in range(
                        fmuwu__tzbek.type.count)]
                vxzx__onhm = cgutils.pack_array(builder, [zmzi__rup,
                    context.get_constant(types.int64, -1)] + vxzx__onhm)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType,
                types.Array)) or arr_typ in (boolean_array,
                datetime_date_array_type, string_array_type, binary_array_type
                ):
                vxzx__onhm = cgutils.pack_array(builder, [zmzi__rup])
            else:
                raise RuntimeError(
                    'array_to_info: unsupported type for subarray')
            return vxzx__onhm

        def get_buffers(arr_typ, arr):
            if isinstance(arr_typ, MapArrayType):
                zayq__wwo = context.make_helper(builder, arr_typ, value=arr)
                cxif__fnxo = get_buffers(_get_map_arr_data_type(arr_typ),
                    zayq__wwo.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                udo__hocv = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                opgj__lmq = get_buffers(arr_typ.dtype, udo__hocv.data)
                fix__kfp = context.make_array(types.Array(offset_type, 1, 'C')
                    )(context, builder, udo__hocv.offsets)
                ogw__xbyvq = builder.bitcast(fix__kfp.data, lir.IntType(8).
                    as_pointer())
                tdk__cgl = context.make_array(types.Array(types.uint8, 1, 'C')
                    )(context, builder, udo__hocv.null_bitmap)
                don__sjbc = builder.bitcast(tdk__cgl.data, lir.IntType(8).
                    as_pointer())
                cxif__fnxo = cgutils.pack_array(builder, [ogw__xbyvq,
                    don__sjbc] + [builder.extract_value(opgj__lmq,
                    jlzqa__krsau) for jlzqa__krsau in range(opgj__lmq.type.
                    count)])
            elif isinstance(arr_typ, StructArrayType):
                udo__hocv = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                opgj__lmq = []
                for jlzqa__krsau, qixai__btzrn in enumerate(arr_typ.data):
                    gdmh__gsk = get_buffers(qixai__btzrn, builder.
                        extract_value(udo__hocv.data, jlzqa__krsau))
                    opgj__lmq += [builder.extract_value(gdmh__gsk,
                        gkzvs__smhry) for gkzvs__smhry in range(gdmh__gsk.
                        type.count)]
                tdk__cgl = context.make_array(types.Array(types.uint8, 1, 'C')
                    )(context, builder, udo__hocv.null_bitmap)
                don__sjbc = builder.bitcast(tdk__cgl.data, lir.IntType(8).
                    as_pointer())
                cxif__fnxo = cgutils.pack_array(builder, [don__sjbc] +
                    opgj__lmq)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
                ) or arr_typ in (boolean_array, datetime_date_array_type):
                bdo__qvcj = arr_typ.dtype
                if isinstance(arr_typ, DecimalArrayType):
                    bdo__qvcj = int128_type
                elif arr_typ == datetime_date_array_type:
                    bdo__qvcj = types.int64
                arr = cgutils.create_struct_proxy(arr_typ)(context, builder,
                    arr)
                gpx__xhtty = context.make_array(types.Array(bdo__qvcj, 1, 'C')
                    )(context, builder, arr.data)
                tdk__cgl = context.make_array(types.Array(types.uint8, 1, 'C')
                    )(context, builder, arr.null_bitmap)
                hhf__yjz = builder.bitcast(gpx__xhtty.data, lir.IntType(8).
                    as_pointer())
                don__sjbc = builder.bitcast(tdk__cgl.data, lir.IntType(8).
                    as_pointer())
                cxif__fnxo = cgutils.pack_array(builder, [don__sjbc, hhf__yjz])
            elif arr_typ in (string_array_type, binary_array_type):
                udo__hocv = _get_str_binary_arr_payload(context, builder,
                    arr, arr_typ)
                unn__czjq = context.make_helper(builder, offset_arr_type,
                    udo__hocv.offsets).data
                ilbj__aoed = context.make_helper(builder, char_arr_type,
                    udo__hocv.data).data
                kayp__girui = context.make_helper(builder,
                    null_bitmap_arr_type, udo__hocv.null_bitmap).data
                cxif__fnxo = cgutils.pack_array(builder, [builder.bitcast(
                    unn__czjq, lir.IntType(8).as_pointer()), builder.
                    bitcast(kayp__girui, lir.IntType(8).as_pointer()),
                    builder.bitcast(ilbj__aoed, lir.IntType(8).as_pointer())])
            elif isinstance(arr_typ, types.Array):
                arr = context.make_array(arr_typ)(context, builder, arr)
                hhf__yjz = builder.bitcast(arr.data, lir.IntType(8).
                    as_pointer())
                qvs__bvvh = lir.Constant(lir.IntType(8).as_pointer(), None)
                cxif__fnxo = cgutils.pack_array(builder, [qvs__bvvh, hhf__yjz])
            else:
                raise RuntimeError(
                    'array_to_info: unsupported type for subarray ' + str(
                    arr_typ))
            return cxif__fnxo

        def get_field_names(arr_typ):
            svwn__vzv = []
            if isinstance(arr_typ, StructArrayType):
                for nrsa__wimka, sgj__pnwh in zip(arr_typ.dtype.names,
                    arr_typ.data):
                    svwn__vzv.append(nrsa__wimka)
                    svwn__vzv += get_field_names(sgj__pnwh)
            elif isinstance(arr_typ, ArrayItemArrayType):
                svwn__vzv += get_field_names(arr_typ.dtype)
            elif isinstance(arr_typ, MapArrayType):
                svwn__vzv += get_field_names(_get_map_arr_data_type(arr_typ))
            return svwn__vzv
        beidz__xjg = get_types(arr_type)
        ftsz__opph = cgutils.pack_array(builder, [context.get_constant(
            types.int32, t) for t in beidz__xjg])
        cchsr__axyto = cgutils.alloca_once_value(builder, ftsz__opph)
        vxzx__onhm = get_lengths(arr_type, in_arr)
        lengths_ptr = cgutils.alloca_once_value(builder, vxzx__onhm)
        cxif__fnxo = get_buffers(arr_type, in_arr)
        zrs__vkmwq = cgutils.alloca_once_value(builder, cxif__fnxo)
        svwn__vzv = get_field_names(arr_type)
        if len(svwn__vzv) == 0:
            svwn__vzv = ['irrelevant']
        hovu__rys = cgutils.pack_array(builder, [context.
            insert_const_string(builder.module, a) for a in svwn__vzv])
        rbk__wbx = cgutils.alloca_once_value(builder, hovu__rys)
        if isinstance(arr_type, MapArrayType):
            pzky__jtmb = _get_map_arr_data_type(arr_type)
            hxr__fmz = context.make_helper(builder, arr_type, value=in_arr)
            wog__ziyo = hxr__fmz.data
        else:
            pzky__jtmb = arr_type
            wog__ziyo = in_arr
        kgtvd__xdl = context.make_helper(builder, pzky__jtmb, wog__ziyo)
        abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(32).as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        obn__sjzj = cgutils.get_or_insert_function(builder.module,
            abpxx__qvrpn, name='nested_array_to_info')
        qkq__bdwvb = builder.call(obn__sjzj, [builder.bitcast(cchsr__axyto,
            lir.IntType(32).as_pointer()), builder.bitcast(zrs__vkmwq, lir.
            IntType(8).as_pointer().as_pointer()), builder.bitcast(
            lengths_ptr, lir.IntType(64).as_pointer()), builder.bitcast(
            rbk__wbx, lir.IntType(8).as_pointer()), kgtvd__xdl.meminfo])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return qkq__bdwvb
    if arr_type in (string_array_type, binary_array_type):
        oluo__yxid = context.make_helper(builder, arr_type, in_arr)
        jljmd__duael = ArrayItemArrayType(char_arr_type)
        wsqjq__eujm = context.make_helper(builder, jljmd__duael, oluo__yxid
            .data)
        udo__hocv = _get_str_binary_arr_payload(context, builder, in_arr,
            arr_type)
        unn__czjq = context.make_helper(builder, offset_arr_type, udo__hocv
            .offsets).data
        ilbj__aoed = context.make_helper(builder, char_arr_type, udo__hocv.data
            ).data
        kayp__girui = context.make_helper(builder, null_bitmap_arr_type,
            udo__hocv.null_bitmap).data
        luozj__xvj = builder.zext(builder.load(builder.gep(unn__czjq, [
            udo__hocv.n_arrays])), lir.IntType(64))
        sbkbf__wjkn = context.get_constant(types.int32, int(arr_type ==
            binary_array_type))
        abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32)])
        obn__sjzj = cgutils.get_or_insert_function(builder.module,
            abpxx__qvrpn, name='string_array_to_info')
        return builder.call(obn__sjzj, [udo__hocv.n_arrays, luozj__xvj,
            ilbj__aoed, unn__czjq, kayp__girui, wsqjq__eujm.meminfo,
            sbkbf__wjkn])
    xta__zxsa = False
    if isinstance(arr_type, CategoricalArrayType):
        context.nrt.decref(builder, arr_type, in_arr)
        wtvlp__ahro = context.compile_internal(builder, lambda a: len(a.
            dtype.categories), types.intp(arr_type), [in_arr])
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).codes
        rhrm__isho = get_categories_int_type(arr_type.dtype)
        arr_type = types.Array(rhrm__isho, 1, 'C')
        xta__zxsa = True
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, types.Array):
        arr = context.make_array(arr_type)(context, builder, in_arr)
        assert arr_type.ndim == 1, 'only 1D array shuffle supported'
        zmzi__rup = builder.extract_value(arr.shape, 0)
        ldwns__cis = arr_type.dtype
        iuqn__rgt = numba_to_c_type(ldwns__cis)
        ujo__zrznj = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), iuqn__rgt))
        if xta__zxsa:
            abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(64), lir.IntType(8).as_pointer()])
            obn__sjzj = cgutils.get_or_insert_function(builder.module,
                abpxx__qvrpn, name='categorical_array_to_info')
            return builder.call(obn__sjzj, [zmzi__rup, builder.bitcast(arr.
                data, lir.IntType(8).as_pointer()), builder.load(ujo__zrznj
                ), wtvlp__ahro, arr.meminfo])
        else:
            abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer()])
            obn__sjzj = cgutils.get_or_insert_function(builder.module,
                abpxx__qvrpn, name='numpy_array_to_info')
            return builder.call(obn__sjzj, [zmzi__rup, builder.bitcast(arr.
                data, lir.IntType(8).as_pointer()), builder.load(ujo__zrznj
                ), arr.meminfo])
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        ldwns__cis = arr_type.dtype
        bdo__qvcj = ldwns__cis
        if isinstance(arr_type, DecimalArrayType):
            bdo__qvcj = int128_type
        if arr_type == datetime_date_array_type:
            bdo__qvcj = types.int64
        gpx__xhtty = context.make_array(types.Array(bdo__qvcj, 1, 'C'))(context
            , builder, arr.data)
        zmzi__rup = builder.extract_value(gpx__xhtty.shape, 0)
        kcrgs__sqbhp = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, arr.null_bitmap)
        iuqn__rgt = numba_to_c_type(ldwns__cis)
        ujo__zrznj = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), iuqn__rgt))
        if isinstance(arr_type, DecimalArrayType):
            abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer
                (), lir.IntType(8).as_pointer(), lir.IntType(32), lir.
                IntType(32)])
            obn__sjzj = cgutils.get_or_insert_function(builder.module,
                abpxx__qvrpn, name='decimal_array_to_info')
            return builder.call(obn__sjzj, [zmzi__rup, builder.bitcast(
                gpx__xhtty.data, lir.IntType(8).as_pointer()), builder.load
                (ujo__zrznj), builder.bitcast(kcrgs__sqbhp.data, lir.
                IntType(8).as_pointer()), gpx__xhtty.meminfo, kcrgs__sqbhp.
                meminfo, context.get_constant(types.int32, arr_type.
                precision), context.get_constant(types.int32, arr_type.scale)])
        else:
            abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer
                (), lir.IntType(8).as_pointer()])
            obn__sjzj = cgutils.get_or_insert_function(builder.module,
                abpxx__qvrpn, name='nullable_array_to_info')
            return builder.call(obn__sjzj, [zmzi__rup, builder.bitcast(
                gpx__xhtty.data, lir.IntType(8).as_pointer()), builder.load
                (ujo__zrznj), builder.bitcast(kcrgs__sqbhp.data, lir.
                IntType(8).as_pointer()), gpx__xhtty.meminfo, kcrgs__sqbhp.
                meminfo])
    if isinstance(arr_type, IntervalArrayType):
        assert isinstance(arr_type.arr_type, types.Array
            ), 'array_to_info(): only IntervalArrayType with Numpy arrays supported'
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        ghceh__lww = context.make_array(arr_type.arr_type)(context, builder,
            arr.left)
        jah__ytn = context.make_array(arr_type.arr_type)(context, builder,
            arr.right)
        zmzi__rup = builder.extract_value(ghceh__lww.shape, 0)
        iuqn__rgt = numba_to_c_type(arr_type.arr_type.dtype)
        ujo__zrznj = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), iuqn__rgt))
        abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        obn__sjzj = cgutils.get_or_insert_function(builder.module,
            abpxx__qvrpn, name='interval_array_to_info')
        return builder.call(obn__sjzj, [zmzi__rup, builder.bitcast(
            ghceh__lww.data, lir.IntType(8).as_pointer()), builder.bitcast(
            jah__ytn.data, lir.IntType(8).as_pointer()), builder.load(
            ujo__zrznj), ghceh__lww.meminfo, jah__ytn.meminfo])
    raise BodoError(f'array_to_info(): array type {arr_type} is not supported')


def _lower_info_to_array_numpy(arr_type, context, builder, in_info):
    assert arr_type.ndim == 1, 'only 1D array supported'
    arr = context.make_array(arr_type)(context, builder)
    rhnss__ltct = cgutils.alloca_once(builder, lir.IntType(64))
    hhf__yjz = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    zkr__uthj = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    abpxx__qvrpn = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    obn__sjzj = cgutils.get_or_insert_function(builder.module, abpxx__qvrpn,
        name='info_to_numpy_array')
    builder.call(obn__sjzj, [in_info, rhnss__ltct, hhf__yjz, zkr__uthj])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    vqnfx__vvp = context.get_value_type(types.intp)
    wbq__vuolm = cgutils.pack_array(builder, [builder.load(rhnss__ltct)],
        ty=vqnfx__vvp)
    qgfca__rztj = context.get_constant(types.intp, context.get_abi_sizeof(
        context.get_data_type(arr_type.dtype)))
    ohj__amrh = cgutils.pack_array(builder, [qgfca__rztj], ty=vqnfx__vvp)
    ilbj__aoed = builder.bitcast(builder.load(hhf__yjz), context.
        get_data_type(arr_type.dtype).as_pointer())
    numba.np.arrayobj.populate_array(arr, data=ilbj__aoed, shape=wbq__vuolm,
        strides=ohj__amrh, itemsize=qgfca__rztj, meminfo=builder.load(
        zkr__uthj))
    return arr._getvalue()


def _lower_info_to_array_list_string_array(arr_type, context, builder, in_info
    ):
    zed__wizxj = context.make_helper(builder, arr_type)
    abpxx__qvrpn = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    obn__sjzj = cgutils.get_or_insert_function(builder.module, abpxx__qvrpn,
        name='info_to_list_string_array')
    builder.call(obn__sjzj, [in_info, zed__wizxj._get_ptr_by_name('meminfo')])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    return zed__wizxj._getvalue()


def nested_to_array(context, builder, arr_typ, lengths_ptr, array_infos_ptr,
    lengths_pos, infos_pos):
    uslez__mvas = context.get_data_type(array_info_type)
    if isinstance(arr_typ, ArrayItemArrayType):
        orc__kfafi = lengths_pos
        hxgw__ban = infos_pos
        cchsb__bsj, lengths_pos, infos_pos = nested_to_array(context,
            builder, arr_typ.dtype, lengths_ptr, array_infos_ptr, 
            lengths_pos + 1, infos_pos + 2)
        cctv__ruim = ArrayItemArrayPayloadType(arr_typ)
        nkot__bfjz = context.get_data_type(cctv__ruim)
        znaqc__omaqw = context.get_abi_sizeof(nkot__bfjz)
        jsyr__equmw = define_array_item_dtor(context, builder, arr_typ,
            cctv__ruim)
        racy__xkxc = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, znaqc__omaqw), jsyr__equmw)
        cmfx__uuvi = context.nrt.meminfo_data(builder, racy__xkxc)
        khlyq__ulxmz = builder.bitcast(cmfx__uuvi, nkot__bfjz.as_pointer())
        udo__hocv = cgutils.create_struct_proxy(cctv__ruim)(context, builder)
        udo__hocv.n_arrays = builder.extract_value(builder.load(lengths_ptr
            ), orc__kfafi)
        udo__hocv.data = cchsb__bsj
        bpxb__vpy = builder.load(array_infos_ptr)
        wicz__mgc = builder.bitcast(builder.extract_value(bpxb__vpy,
            hxgw__ban), uslez__mvas)
        udo__hocv.offsets = _lower_info_to_array_numpy(types.Array(
            offset_type, 1, 'C'), context, builder, wicz__mgc)
        tlqri__qdqj = builder.bitcast(builder.extract_value(bpxb__vpy, 
            hxgw__ban + 1), uslez__mvas)
        udo__hocv.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, tlqri__qdqj)
        builder.store(udo__hocv._getvalue(), khlyq__ulxmz)
        wsqjq__eujm = context.make_helper(builder, arr_typ)
        wsqjq__eujm.meminfo = racy__xkxc
        return wsqjq__eujm._getvalue(), lengths_pos, infos_pos
    elif isinstance(arr_typ, StructArrayType):
        wpo__ret = []
        hxgw__ban = infos_pos
        lengths_pos += 1
        infos_pos += 1
        for fml__giopn in arr_typ.data:
            cchsb__bsj, lengths_pos, infos_pos = nested_to_array(context,
                builder, fml__giopn, lengths_ptr, array_infos_ptr,
                lengths_pos, infos_pos)
            wpo__ret.append(cchsb__bsj)
        cctv__ruim = StructArrayPayloadType(arr_typ.data)
        nkot__bfjz = context.get_value_type(cctv__ruim)
        znaqc__omaqw = context.get_abi_sizeof(nkot__bfjz)
        jsyr__equmw = define_struct_arr_dtor(context, builder, arr_typ,
            cctv__ruim)
        racy__xkxc = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, znaqc__omaqw), jsyr__equmw)
        cmfx__uuvi = context.nrt.meminfo_data(builder, racy__xkxc)
        khlyq__ulxmz = builder.bitcast(cmfx__uuvi, nkot__bfjz.as_pointer())
        udo__hocv = cgutils.create_struct_proxy(cctv__ruim)(context, builder)
        udo__hocv.data = cgutils.pack_array(builder, wpo__ret
            ) if types.is_homogeneous(*arr_typ.data) else cgutils.pack_struct(
            builder, wpo__ret)
        bpxb__vpy = builder.load(array_infos_ptr)
        tlqri__qdqj = builder.bitcast(builder.extract_value(bpxb__vpy,
            hxgw__ban), uslez__mvas)
        udo__hocv.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, tlqri__qdqj)
        builder.store(udo__hocv._getvalue(), khlyq__ulxmz)
        vagf__zezs = context.make_helper(builder, arr_typ)
        vagf__zezs.meminfo = racy__xkxc
        return vagf__zezs._getvalue(), lengths_pos, infos_pos
    elif arr_typ in (string_array_type, binary_array_type):
        bpxb__vpy = builder.load(array_infos_ptr)
        mtiz__udfpg = builder.bitcast(builder.extract_value(bpxb__vpy,
            infos_pos), uslez__mvas)
        oluo__yxid = context.make_helper(builder, arr_typ)
        jljmd__duael = ArrayItemArrayType(char_arr_type)
        wsqjq__eujm = context.make_helper(builder, jljmd__duael)
        abpxx__qvrpn = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        obn__sjzj = cgutils.get_or_insert_function(builder.module,
            abpxx__qvrpn, name='info_to_string_array')
        builder.call(obn__sjzj, [mtiz__udfpg, wsqjq__eujm._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        oluo__yxid.data = wsqjq__eujm._getvalue()
        return oluo__yxid._getvalue(), lengths_pos + 1, infos_pos + 1
    elif isinstance(arr_typ, types.Array):
        bpxb__vpy = builder.load(array_infos_ptr)
        fxfa__sihhx = builder.bitcast(builder.extract_value(bpxb__vpy, 
            infos_pos + 1), uslez__mvas)
        return _lower_info_to_array_numpy(arr_typ, context, builder,
            fxfa__sihhx), lengths_pos + 1, infos_pos + 2
    elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
        ) or arr_typ in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_typ)(context, builder)
        bdo__qvcj = arr_typ.dtype
        if isinstance(arr_typ, DecimalArrayType):
            bdo__qvcj = int128_type
        elif arr_typ == datetime_date_array_type:
            bdo__qvcj = types.int64
        bpxb__vpy = builder.load(array_infos_ptr)
        tlqri__qdqj = builder.bitcast(builder.extract_value(bpxb__vpy,
            infos_pos), uslez__mvas)
        arr.null_bitmap = _lower_info_to_array_numpy(types.Array(types.
            uint8, 1, 'C'), context, builder, tlqri__qdqj)
        fxfa__sihhx = builder.bitcast(builder.extract_value(bpxb__vpy, 
            infos_pos + 1), uslez__mvas)
        arr.data = _lower_info_to_array_numpy(types.Array(bdo__qvcj, 1, 'C'
            ), context, builder, fxfa__sihhx)
        return arr._getvalue(), lengths_pos + 1, infos_pos + 2


@intrinsic
def info_to_array(typingctx, info_type, array_type):
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    assert info_type == array_info_type

    def codegen(context, builder, sig, args):
        in_info, egk__kdwu = args
        if isinstance(arr_type, ArrayItemArrayType
            ) and arr_type.dtype == string_array_type:
            return _lower_info_to_array_list_string_array(arr_type, context,
                builder, in_info)
        if isinstance(arr_type, (MapArrayType, ArrayItemArrayType,
            StructArrayType, TupleArrayType)):

            def get_num_arrays(arr_typ):
                if isinstance(arr_typ, ArrayItemArrayType):
                    return 1 + get_num_arrays(arr_typ.dtype)
                elif isinstance(arr_typ, StructArrayType):
                    return 1 + sum([get_num_arrays(fml__giopn) for
                        fml__giopn in arr_typ.data])
                else:
                    return 1

            def get_num_infos(arr_typ):
                if isinstance(arr_typ, ArrayItemArrayType):
                    return 2 + get_num_infos(arr_typ.dtype)
                elif isinstance(arr_typ, StructArrayType):
                    return 1 + sum([get_num_infos(fml__giopn) for
                        fml__giopn in arr_typ.data])
                elif arr_typ in (string_array_type, binary_array_type):
                    return 1
                else:
                    return 2
            if isinstance(arr_type, TupleArrayType):
                abr__wfb = StructArrayType(arr_type.data, ('dummy',) * len(
                    arr_type.data))
            elif isinstance(arr_type, MapArrayType):
                abr__wfb = _get_map_arr_data_type(arr_type)
            else:
                abr__wfb = arr_type
            hojcc__xvca = get_num_arrays(abr__wfb)
            vxzx__onhm = cgutils.pack_array(builder, [lir.Constant(lir.
                IntType(64), 0) for egk__kdwu in range(hojcc__xvca)])
            lengths_ptr = cgutils.alloca_once_value(builder, vxzx__onhm)
            qvs__bvvh = lir.Constant(lir.IntType(8).as_pointer(), None)
            zqkd__cqowi = cgutils.pack_array(builder, [qvs__bvvh for
                egk__kdwu in range(get_num_infos(abr__wfb))])
            array_infos_ptr = cgutils.alloca_once_value(builder, zqkd__cqowi)
            abpxx__qvrpn = lir.FunctionType(lir.VoidType(), [lir.IntType(8)
                .as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8)
                .as_pointer().as_pointer()])
            obn__sjzj = cgutils.get_or_insert_function(builder.module,
                abpxx__qvrpn, name='info_to_nested_array')
            builder.call(obn__sjzj, [in_info, builder.bitcast(lengths_ptr,
                lir.IntType(64).as_pointer()), builder.bitcast(
                array_infos_ptr, lir.IntType(8).as_pointer().as_pointer())])
            context.compile_internal(builder, lambda :
                check_and_propagate_cpp_exception(), types.none(), [])
            arr, egk__kdwu, egk__kdwu = nested_to_array(context, builder,
                abr__wfb, lengths_ptr, array_infos_ptr, 0, 0)
            if isinstance(arr_type, TupleArrayType):
                zfthl__jepc = context.make_helper(builder, arr_type)
                zfthl__jepc.data = arr
                context.nrt.incref(builder, abr__wfb, arr)
                arr = zfthl__jepc._getvalue()
            elif isinstance(arr_type, MapArrayType):
                sig = signature(arr_type, abr__wfb)
                arr = init_map_arr_codegen(context, builder, sig, (arr,))
            return arr
        if arr_type in (string_array_type, binary_array_type):
            oluo__yxid = context.make_helper(builder, arr_type)
            jljmd__duael = ArrayItemArrayType(char_arr_type)
            wsqjq__eujm = context.make_helper(builder, jljmd__duael)
            abpxx__qvrpn = lir.FunctionType(lir.VoidType(), [lir.IntType(8)
                .as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
            obn__sjzj = cgutils.get_or_insert_function(builder.module,
                abpxx__qvrpn, name='info_to_string_array')
            builder.call(obn__sjzj, [in_info, wsqjq__eujm._get_ptr_by_name(
                'meminfo')])
            context.compile_internal(builder, lambda :
                check_and_propagate_cpp_exception(), types.none(), [])
            oluo__yxid.data = wsqjq__eujm._getvalue()
            return oluo__yxid._getvalue()
        if isinstance(arr_type, CategoricalArrayType):
            out_arr = cgutils.create_struct_proxy(arr_type)(context, builder)
            rhrm__isho = get_categories_int_type(arr_type.dtype)
            rlpt__upun = types.Array(rhrm__isho, 1, 'C')
            out_arr.codes = _lower_info_to_array_numpy(rlpt__upun, context,
                builder, in_info)
            if isinstance(array_type, types.TypeRef):
                assert arr_type.dtype.categories is not None, 'info_to_array: unknown categories'
                is_ordered = arr_type.dtype.ordered
                fxfo__ugjf = pd.CategoricalDtype(arr_type.dtype.categories,
                    is_ordered).categories.values
                new_cats_tup = MetaType(tuple(fxfo__ugjf))
                int_type = arr_type.dtype.int_type
                vjhf__gnl = bodo.typeof(fxfo__ugjf)
                glc__rwf = context.get_constant_generic(builder, vjhf__gnl,
                    fxfo__ugjf)
                ldwns__cis = context.compile_internal(builder, lambda c_arr:
                    bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo.
                    utils.conversion.index_from_array(c_arr), is_ordered,
                    int_type, new_cats_tup), arr_type.dtype(vjhf__gnl), [
                    glc__rwf])
            else:
                ldwns__cis = cgutils.create_struct_proxy(arr_type)(context,
                    builder, args[1]).dtype
                context.nrt.incref(builder, arr_type.dtype, ldwns__cis)
            out_arr.dtype = ldwns__cis
            return out_arr._getvalue()
        if isinstance(arr_type, types.Array):
            return _lower_info_to_array_numpy(arr_type, context, builder,
                in_info)
        if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
            ) or arr_type in (boolean_array, datetime_date_array_type):
            arr = cgutils.create_struct_proxy(arr_type)(context, builder)
            bdo__qvcj = arr_type.dtype
            if isinstance(arr_type, DecimalArrayType):
                bdo__qvcj = int128_type
            elif arr_type == datetime_date_array_type:
                bdo__qvcj = types.int64
            lnp__jncy = types.Array(bdo__qvcj, 1, 'C')
            gpx__xhtty = context.make_array(lnp__jncy)(context, builder)
            hjef__lhsql = types.Array(types.uint8, 1, 'C')
            lkymb__jeif = context.make_array(hjef__lhsql)(context, builder)
            rhnss__ltct = cgutils.alloca_once(builder, lir.IntType(64))
            ctr__vjczt = cgutils.alloca_once(builder, lir.IntType(64))
            hhf__yjz = cgutils.alloca_once(builder, lir.IntType(8).as_pointer()
                )
            hksz__iqeq = cgutils.alloca_once(builder, lir.IntType(8).
                as_pointer())
            zkr__uthj = cgutils.alloca_once(builder, lir.IntType(8).
                as_pointer())
            hznqq__mfix = cgutils.alloca_once(builder, lir.IntType(8).
                as_pointer())
            abpxx__qvrpn = lir.FunctionType(lir.VoidType(), [lir.IntType(8)
                .as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64
                ).as_pointer(), lir.IntType(8).as_pointer().as_pointer(),
                lir.IntType(8).as_pointer().as_pointer(), lir.IntType(8).
                as_pointer().as_pointer(), lir.IntType(8).as_pointer().
                as_pointer()])
            obn__sjzj = cgutils.get_or_insert_function(builder.module,
                abpxx__qvrpn, name='info_to_nullable_array')
            builder.call(obn__sjzj, [in_info, rhnss__ltct, ctr__vjczt,
                hhf__yjz, hksz__iqeq, zkr__uthj, hznqq__mfix])
            context.compile_internal(builder, lambda :
                check_and_propagate_cpp_exception(), types.none(), [])
            vqnfx__vvp = context.get_value_type(types.intp)
            wbq__vuolm = cgutils.pack_array(builder, [builder.load(
                rhnss__ltct)], ty=vqnfx__vvp)
            qgfca__rztj = context.get_constant(types.intp, context.
                get_abi_sizeof(context.get_data_type(bdo__qvcj)))
            ohj__amrh = cgutils.pack_array(builder, [qgfca__rztj], ty=
                vqnfx__vvp)
            ilbj__aoed = builder.bitcast(builder.load(hhf__yjz), context.
                get_data_type(bdo__qvcj).as_pointer())
            numba.np.arrayobj.populate_array(gpx__xhtty, data=ilbj__aoed,
                shape=wbq__vuolm, strides=ohj__amrh, itemsize=qgfca__rztj,
                meminfo=builder.load(zkr__uthj))
            arr.data = gpx__xhtty._getvalue()
            wbq__vuolm = cgutils.pack_array(builder, [builder.load(
                ctr__vjczt)], ty=vqnfx__vvp)
            qgfca__rztj = context.get_constant(types.intp, context.
                get_abi_sizeof(context.get_data_type(types.uint8)))
            ohj__amrh = cgutils.pack_array(builder, [qgfca__rztj], ty=
                vqnfx__vvp)
            ilbj__aoed = builder.bitcast(builder.load(hksz__iqeq), context.
                get_data_type(types.uint8).as_pointer())
            numba.np.arrayobj.populate_array(lkymb__jeif, data=ilbj__aoed,
                shape=wbq__vuolm, strides=ohj__amrh, itemsize=qgfca__rztj,
                meminfo=builder.load(hznqq__mfix))
            arr.null_bitmap = lkymb__jeif._getvalue()
            return arr._getvalue()
        if isinstance(arr_type, IntervalArrayType):
            arr = cgutils.create_struct_proxy(arr_type)(context, builder)
            ghceh__lww = context.make_array(arr_type.arr_type)(context, builder
                )
            jah__ytn = context.make_array(arr_type.arr_type)(context, builder)
            rhnss__ltct = cgutils.alloca_once(builder, lir.IntType(64))
            ssyfb__utyg = cgutils.alloca_once(builder, lir.IntType(8).
                as_pointer())
            zyn__pvncm = cgutils.alloca_once(builder, lir.IntType(8).
                as_pointer())
            gty__qjsdh = cgutils.alloca_once(builder, lir.IntType(8).
                as_pointer())
            lan__gioe = cgutils.alloca_once(builder, lir.IntType(8).
                as_pointer())
            abpxx__qvrpn = lir.FunctionType(lir.VoidType(), [lir.IntType(8)
                .as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8)
                .as_pointer().as_pointer(), lir.IntType(8).as_pointer().
                as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir
                .IntType(8).as_pointer().as_pointer()])
            obn__sjzj = cgutils.get_or_insert_function(builder.module,
                abpxx__qvrpn, name='info_to_interval_array')
            builder.call(obn__sjzj, [in_info, rhnss__ltct, ssyfb__utyg,
                zyn__pvncm, gty__qjsdh, lan__gioe])
            context.compile_internal(builder, lambda :
                check_and_propagate_cpp_exception(), types.none(), [])
            vqnfx__vvp = context.get_value_type(types.intp)
            wbq__vuolm = cgutils.pack_array(builder, [builder.load(
                rhnss__ltct)], ty=vqnfx__vvp)
            qgfca__rztj = context.get_constant(types.intp, context.
                get_abi_sizeof(context.get_data_type(arr_type.arr_type.dtype)))
            ohj__amrh = cgutils.pack_array(builder, [qgfca__rztj], ty=
                vqnfx__vvp)
            bfb__konj = builder.bitcast(builder.load(ssyfb__utyg), context.
                get_data_type(arr_type.arr_type.dtype).as_pointer())
            numba.np.arrayobj.populate_array(ghceh__lww, data=bfb__konj,
                shape=wbq__vuolm, strides=ohj__amrh, itemsize=qgfca__rztj,
                meminfo=builder.load(gty__qjsdh))
            arr.left = ghceh__lww._getvalue()
            ioie__hprgb = builder.bitcast(builder.load(zyn__pvncm), context
                .get_data_type(arr_type.arr_type.dtype).as_pointer())
            numba.np.arrayobj.populate_array(jah__ytn, data=ioie__hprgb,
                shape=wbq__vuolm, strides=ohj__amrh, itemsize=qgfca__rztj,
                meminfo=builder.load(lan__gioe))
            arr.right = jah__ytn._getvalue()
            return arr._getvalue()
        raise BodoError(
            f'info_to_array(): array type {arr_type} is not supported')
    return arr_type(info_type, array_type), codegen


@intrinsic
def test_alloc_np(typingctx, len_typ, arr_type):
    array_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type

    def codegen(context, builder, sig, args):
        zmzi__rup, egk__kdwu = args
        iuqn__rgt = numba_to_c_type(array_type.dtype)
        ujo__zrznj = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), iuqn__rgt))
        abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(32)])
        obn__sjzj = cgutils.get_or_insert_function(builder.module,
            abpxx__qvrpn, name='alloc_numpy')
        return builder.call(obn__sjzj, [zmzi__rup, builder.load(ujo__zrznj)])
    return array_info_type(len_typ, arr_type), codegen


@intrinsic
def test_alloc_string(typingctx, len_typ, n_chars_typ):

    def codegen(context, builder, sig, args):
        zmzi__rup, wtldn__zpiv = args
        abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64)])
        obn__sjzj = cgutils.get_or_insert_function(builder.module,
            abpxx__qvrpn, name='alloc_string_array')
        return builder.call(obn__sjzj, [zmzi__rup, wtldn__zpiv])
    return array_info_type(len_typ, n_chars_typ), codegen


@intrinsic
def arr_info_list_to_table(typingctx, list_arr_info_typ=None):
    assert list_arr_info_typ == types.List(array_info_type)
    return table_type(list_arr_info_typ), arr_info_list_to_table_codegen


def arr_info_list_to_table_codegen(context, builder, sig, args):
    pgfw__dhw, = args
    odfr__zidl = numba.cpython.listobj.ListInstance(context, builder, sig.
        args[0], pgfw__dhw)
    abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
        IntType(8).as_pointer().as_pointer(), lir.IntType(64)])
    obn__sjzj = cgutils.get_or_insert_function(builder.module, abpxx__qvrpn,
        name='arr_info_list_to_table')
    return builder.call(obn__sjzj, [odfr__zidl.data, odfr__zidl.size])


@intrinsic
def info_from_table(typingctx, table_t, ind_t):

    def codegen(context, builder, sig, args):
        abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        obn__sjzj = cgutils.get_or_insert_function(builder.module,
            abpxx__qvrpn, name='info_from_table')
        return builder.call(obn__sjzj, args)
    return array_info_type(table_t, ind_t), codegen


@intrinsic
def cpp_table_to_py_table(typingctx, cpp_table_t, table_idx_arr_t,
    py_table_type_t):
    assert cpp_table_t == table_type, 'invalid cpp table type'
    assert isinstance(table_idx_arr_t, types.Array
        ) and table_idx_arr_t.dtype == types.int64, 'invalid table index array'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    kvi__vumo = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        tiis__iymk, nxcgr__gujwm, egk__kdwu = args
        abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        obn__sjzj = cgutils.get_or_insert_function(builder.module,
            abpxx__qvrpn, name='info_from_table')
        ptuma__jkcra = cgutils.create_struct_proxy(kvi__vumo)(context, builder)
        ptuma__jkcra.parent = cgutils.get_null_value(ptuma__jkcra.parent.type)
        wxsr__sui = context.make_array(table_idx_arr_t)(context, builder,
            nxcgr__gujwm)
        bwom__aaay = context.get_constant(types.int64, -1)
        igd__mczqh = context.get_constant(types.int64, 0)
        aqw__zxlkr = cgutils.alloca_once_value(builder, igd__mczqh)
        for t, duaz__pgjea in kvi__vumo.type_to_blk.items():
            uesw__oeux = context.get_constant(types.int64, len(kvi__vumo.
                block_to_arr_ind[duaz__pgjea]))
            egk__kdwu, htb__daw = ListInstance.allocate_ex(context, builder,
                types.List(t), uesw__oeux)
            htb__daw.size = uesw__oeux
            jsth__pwzac = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(kvi__vumo.block_to_arr_ind[
                duaz__pgjea], dtype=np.int64))
            gtsop__bcqeu = context.make_array(types.Array(types.int64, 1, 'C')
                )(context, builder, jsth__pwzac)
            with cgutils.for_range(builder, uesw__oeux) as loop:
                jlzqa__krsau = loop.index
                fpb__ltgux = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    gtsop__bcqeu, jlzqa__krsau)
                wtiho__yoe = _getitem_array_single_int(context, builder,
                    types.int64, table_idx_arr_t, wxsr__sui, fpb__ltgux)
                smqd__okdk = builder.icmp_unsigned('!=', wtiho__yoe, bwom__aaay
                    )
                with builder.if_else(smqd__okdk) as (then, orelse):
                    with then:
                        ade__pqwxr = builder.call(obn__sjzj, [tiis__iymk,
                            wtiho__yoe])
                        arr = context.compile_internal(builder, lambda info:
                            info_to_array(info, t), t(array_info_type), [
                            ade__pqwxr])
                        htb__daw.inititem(jlzqa__krsau, arr, incref=False)
                        zmzi__rup = context.compile_internal(builder, lambda
                            arr: len(arr), types.int64(t), [arr])
                        builder.store(zmzi__rup, aqw__zxlkr)
                    with orelse:
                        kjib__udq = context.get_constant_null(t)
                        htb__daw.inititem(jlzqa__krsau, kjib__udq, incref=False
                            )
            setattr(ptuma__jkcra, f'block_{duaz__pgjea}', htb__daw.value)
        ptuma__jkcra.len = builder.load(aqw__zxlkr)
        return ptuma__jkcra._getvalue()
    return kvi__vumo(cpp_table_t, table_idx_arr_t, py_table_type_t), codegen


@intrinsic
def py_table_to_cpp_table(typingctx, py_table_t, py_table_type_t):
    assert isinstance(py_table_t, bodo.hiframes.table.TableType
        ), 'invalid py table type'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    kvi__vumo = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        faam__vvfhb, egk__kdwu = args
        lnrx__mospp = lir.Constant(lir.IntType(64), len(kvi__vumo.arr_types))
        egk__kdwu, qrhcm__fwg = ListInstance.allocate_ex(context, builder,
            types.List(array_info_type), lnrx__mospp)
        qrhcm__fwg.size = lnrx__mospp
        zlvei__hlcw = cgutils.create_struct_proxy(kvi__vumo)(context,
            builder, faam__vvfhb)
        for t, duaz__pgjea in kvi__vumo.type_to_blk.items():
            uesw__oeux = context.get_constant(types.int64, len(kvi__vumo.
                block_to_arr_ind[duaz__pgjea]))
            uzrb__uqbmj = getattr(zlvei__hlcw, f'block_{duaz__pgjea}')
            aqs__hzmcx = ListInstance(context, builder, types.List(t),
                uzrb__uqbmj)
            jsth__pwzac = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(kvi__vumo.block_to_arr_ind[
                duaz__pgjea], dtype=np.int64))
            gtsop__bcqeu = context.make_array(types.Array(types.int64, 1, 'C')
                )(context, builder, jsth__pwzac)
            with cgutils.for_range(builder, uesw__oeux) as loop:
                jlzqa__krsau = loop.index
                fpb__ltgux = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    gtsop__bcqeu, jlzqa__krsau)
                lbof__gimna = signature(types.none, kvi__vumo, types.List(t
                    ), types.int64, types.int64)
                xehw__wiudh = (faam__vvfhb, uzrb__uqbmj, jlzqa__krsau,
                    fpb__ltgux)
                bodo.hiframes.table.ensure_column_unboxed_codegen(context,
                    builder, lbof__gimna, xehw__wiudh)
                arr = aqs__hzmcx.getitem(jlzqa__krsau)
                sdkq__bcd = signature(array_info_type, t)
                ijhp__vvtv = arr,
                gtfdd__klw = array_to_info_codegen(context, builder,
                    sdkq__bcd, ijhp__vvtv)
                qrhcm__fwg.inititem(fpb__ltgux, gtfdd__klw, incref=False)
        czus__udwn = qrhcm__fwg.value
        nbke__cphvq = signature(table_type, types.List(array_info_type))
        ayr__zwssx = czus__udwn,
        tiis__iymk = arr_info_list_to_table_codegen(context, builder,
            nbke__cphvq, ayr__zwssx)
        context.nrt.decref(builder, types.List(array_info_type), czus__udwn)
        return tiis__iymk
    return table_type(kvi__vumo, py_table_type_t), codegen


delete_info_decref_array = types.ExternalFunction('delete_info_decref_array',
    types.void(array_info_type))
delete_table_decref_arrays = types.ExternalFunction(
    'delete_table_decref_arrays', types.void(table_type))


@intrinsic
def delete_table(typingctx, table_t=None):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        abpxx__qvrpn = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        obn__sjzj = cgutils.get_or_insert_function(builder.module,
            abpxx__qvrpn, name='delete_table')
        builder.call(obn__sjzj, args)
    return types.void(table_t), codegen


@intrinsic
def shuffle_table(typingctx, table_t, n_keys_t, _is_parallel, keep_comm_info_t
    ):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(32)])
        obn__sjzj = cgutils.get_or_insert_function(builder.module,
            abpxx__qvrpn, name='shuffle_table')
        qkq__bdwvb = builder.call(obn__sjzj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return qkq__bdwvb
    return table_type(table_t, types.int64, types.boolean, types.int32
        ), codegen


class ShuffleInfoType(types.Type):

    def __init__(self):
        super(ShuffleInfoType, self).__init__(name='ShuffleInfoType()')


shuffle_info_type = ShuffleInfoType()
register_model(ShuffleInfoType)(models.OpaqueModel)
get_shuffle_info = types.ExternalFunction('get_shuffle_info',
    shuffle_info_type(table_type))
delete_shuffle_info = types.ExternalFunction('delete_shuffle_info', types.
    void(shuffle_info_type))
reverse_shuffle_table = types.ExternalFunction('reverse_shuffle_table',
    table_type(table_type, shuffle_info_type))


@intrinsic
def hash_join_table(typingctx, left_table_t, right_table_t, left_parallel_t,
    right_parallel_t, n_keys_t, n_data_left_t, n_data_right_t, same_vect_t,
    same_need_typechange_t, is_left_t, is_right_t, is_join_t,
    optional_col_t, indicator, _bodo_na_equal, cond_func, left_col_nums,
    left_col_nums_len, right_col_nums, right_col_nums_len):
    assert left_table_t == table_type
    assert right_table_t == table_type

    def codegen(context, builder, sig, args):
        abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(64), lir.IntType(64),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(1), lir.IntType(1), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(8).as_pointer(), lir.IntType(64)])
        obn__sjzj = cgutils.get_or_insert_function(builder.module,
            abpxx__qvrpn, name='hash_join_table')
        qkq__bdwvb = builder.call(obn__sjzj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return qkq__bdwvb
    return table_type(left_table_t, right_table_t, types.boolean, types.
        boolean, types.int64, types.int64, types.int64, types.voidptr,
        types.voidptr, types.boolean, types.boolean, types.boolean, types.
        boolean, types.boolean, types.boolean, types.voidptr, types.voidptr,
        types.int64, types.voidptr, types.int64), codegen


@intrinsic
def compute_node_partition_by_hash(typingctx, table_t, n_keys_t, n_pes_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(64)])
        obn__sjzj = cgutils.get_or_insert_function(builder.module,
            abpxx__qvrpn, name='compute_node_partition_by_hash')
        qkq__bdwvb = builder.call(obn__sjzj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return qkq__bdwvb
    return table_type(table_t, types.int64, types.int64), codegen


@intrinsic
def sort_values_table(typingctx, table_t, n_keys_t, vect_ascending_t,
    na_position_b_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        obn__sjzj = cgutils.get_or_insert_function(builder.module,
            abpxx__qvrpn, name='sort_values_table')
        qkq__bdwvb = builder.call(obn__sjzj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return qkq__bdwvb
    return table_type(table_t, types.int64, types.voidptr, types.voidptr,
        types.boolean), codegen


@intrinsic
def sample_table(typingctx, table_t, n_keys_t, frac_t, replace_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.DoubleType(), lir
            .IntType(1), lir.IntType(1)])
        obn__sjzj = cgutils.get_or_insert_function(builder.module,
            abpxx__qvrpn, name='sample_table')
        qkq__bdwvb = builder.call(obn__sjzj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return qkq__bdwvb
    return table_type(table_t, types.int64, types.float64, types.boolean,
        types.boolean), codegen


@intrinsic
def shuffle_renormalization(typingctx, table_t, random_t, random_seed_t,
    is_parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1)])
        obn__sjzj = cgutils.get_or_insert_function(builder.module,
            abpxx__qvrpn, name='shuffle_renormalization')
        qkq__bdwvb = builder.call(obn__sjzj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return qkq__bdwvb
    return table_type(table_t, types.int32, types.int64, types.boolean
        ), codegen


@intrinsic
def shuffle_renormalization_group(typingctx, table_t, random_t,
    random_seed_t, is_parallel_t, num_ranks_t, ranks_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1), lir.IntType(64), lir.IntType(8).as_pointer()])
        obn__sjzj = cgutils.get_or_insert_function(builder.module,
            abpxx__qvrpn, name='shuffle_renormalization_group')
        qkq__bdwvb = builder.call(obn__sjzj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return qkq__bdwvb
    return table_type(table_t, types.int32, types.int64, types.boolean,
        types.int64, types.voidptr), codegen


@intrinsic
def drop_duplicates_table(typingctx, table_t, parallel_t, nkey_t, keep_t,
    dropna):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(64), lir.IntType(1)])
        obn__sjzj = cgutils.get_or_insert_function(builder.module,
            abpxx__qvrpn, name='drop_duplicates_table')
        qkq__bdwvb = builder.call(obn__sjzj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return qkq__bdwvb
    return table_type(table_t, types.boolean, types.int64, types.int64,
        types.boolean), codegen


@intrinsic
def pivot_groupby_and_aggregate(typingctx, table_t, n_keys_t,
    dispatch_table_t, dispatch_info_t, input_has_index, ftypes,
    func_offsets, udf_n_redvars, is_parallel, is_crosstab, skipdropna_t,
    return_keys, return_index, update_cb, combine_cb, eval_cb,
    udf_table_dummy_t):
    assert table_t == table_type
    assert dispatch_table_t == table_type
    assert dispatch_info_t == table_type
    assert udf_table_dummy_t == table_type

    def codegen(context, builder, sig, args):
        abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        obn__sjzj = cgutils.get_or_insert_function(builder.module,
            abpxx__qvrpn, name='pivot_groupby_and_aggregate')
        qkq__bdwvb = builder.call(obn__sjzj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return qkq__bdwvb
    return table_type(table_t, types.int64, table_t, table_t, types.boolean,
        types.voidptr, types.voidptr, types.voidptr, types.boolean, types.
        boolean, types.boolean, types.boolean, types.boolean, types.voidptr,
        types.voidptr, types.voidptr, table_t), codegen


@intrinsic
def groupby_and_aggregate(typingctx, table_t, n_keys_t, input_has_index,
    ftypes, func_offsets, udf_n_redvars, is_parallel, skipdropna_t,
    shift_periods_t, transform_func, head_n, return_keys, return_index,
    dropna, update_cb, combine_cb, eval_cb, general_udfs_cb, udf_table_dummy_t
    ):
    assert table_t == table_type
    assert udf_table_dummy_t == table_type

    def codegen(context, builder, sig, args):
        abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(64), lir.IntType(64), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(8).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        obn__sjzj = cgutils.get_or_insert_function(builder.module,
            abpxx__qvrpn, name='groupby_and_aggregate')
        qkq__bdwvb = builder.call(obn__sjzj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return qkq__bdwvb
    return table_type(table_t, types.int64, types.boolean, types.voidptr,
        types.voidptr, types.voidptr, types.boolean, types.boolean, types.
        int64, types.int64, types.int64, types.boolean, types.boolean,
        types.boolean, types.voidptr, types.voidptr, types.voidptr, types.
        voidptr, table_t), codegen


get_groupby_labels = types.ExternalFunction('get_groupby_labels', types.
    int64(table_type, types.voidptr, types.voidptr, types.boolean, types.bool_)
    )
_array_isin = types.ExternalFunction('array_isin', types.void(
    array_info_type, array_info_type, array_info_type, types.bool_))


@numba.njit
def array_isin(out_arr, in_arr, in_values, is_parallel):
    vmuu__vrk = array_to_info(in_arr)
    jujt__vjk = array_to_info(in_values)
    wftk__jalf = array_to_info(out_arr)
    ewhb__rvi = arr_info_list_to_table([vmuu__vrk, jujt__vjk, wftk__jalf])
    _array_isin(wftk__jalf, vmuu__vrk, jujt__vjk, is_parallel)
    check_and_propagate_cpp_exception()
    delete_table(ewhb__rvi)


_get_search_regex = types.ExternalFunction('get_search_regex', types.void(
    array_info_type, types.bool_, types.voidptr, array_info_type))


@numba.njit
def get_search_regex(in_arr, case, pat, out_arr):
    vmuu__vrk = array_to_info(in_arr)
    wftk__jalf = array_to_info(out_arr)
    _get_search_regex(vmuu__vrk, case, pat, wftk__jalf)
    check_and_propagate_cpp_exception()


def _gen_row_access_intrinsic(col_dtype, c_ind):
    from llvmlite import ir as lir
    if isinstance(col_dtype, types.Number) or col_dtype in [bodo.
        datetime_date_type, bodo.datetime64ns, bodo.timedelta64ns, types.bool_
        ]:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                ptuma__jkcra, ldgyf__afdk = args
                ptuma__jkcra = builder.bitcast(ptuma__jkcra, lir.IntType(8)
                    .as_pointer().as_pointer())
                blvzg__dfjrk = lir.Constant(lir.IntType(64), c_ind)
                rci__lumfx = builder.load(builder.gep(ptuma__jkcra, [
                    blvzg__dfjrk]))
                rci__lumfx = builder.bitcast(rci__lumfx, context.
                    get_data_type(col_dtype).as_pointer())
                return builder.load(builder.gep(rci__lumfx, [ldgyf__afdk]))
            return col_dtype(types.voidptr, types.int64), codegen
        return getitem_func
    if col_dtype == types.unicode_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                ptuma__jkcra, ldgyf__afdk = args
                abpxx__qvrpn = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64), lir.IntType(64).as_pointer()])
                ciuf__htns = cgutils.get_or_insert_function(builder.module,
                    abpxx__qvrpn, name='array_info_getitem')
                blvzg__dfjrk = lir.Constant(lir.IntType(64), c_ind)
                pbc__vnxm = cgutils.alloca_once(builder, lir.IntType(64))
                args = ptuma__jkcra, blvzg__dfjrk, ldgyf__afdk, pbc__vnxm
                hhf__yjz = builder.call(ciuf__htns, args)
                return context.make_tuple(builder, sig.return_type, [
                    hhf__yjz, builder.load(pbc__vnxm)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    raise BodoError(
        f"General Join Conditions with '{col_dtype}' column data type not supported"
        )


def _gen_row_na_check_intrinsic(col_array_dtype, c_ind):
    if isinstance(col_array_dtype, bodo.libs.int_arr_ext.IntegerArrayType
        ) or col_array_dtype in [bodo.libs.bool_arr_ext.boolean_array, bodo
        .libs.str_arr_ext.string_array_type] or isinstance(col_array_dtype,
        types.Array) and col_array_dtype.dtype == bodo.datetime_date_type:

        @intrinsic
        def checkna_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                efyqg__pxjm, ldgyf__afdk = args
                efyqg__pxjm = builder.bitcast(efyqg__pxjm, lir.IntType(8).
                    as_pointer().as_pointer())
                blvzg__dfjrk = lir.Constant(lir.IntType(64), c_ind)
                rci__lumfx = builder.load(builder.gep(efyqg__pxjm, [
                    blvzg__dfjrk]))
                kayp__girui = builder.bitcast(rci__lumfx, context.
                    get_data_type(types.bool_).as_pointer())
                ebz__whq = bodo.utils.cg_helpers.get_bitmap_bit(builder,
                    kayp__girui, ldgyf__afdk)
                wzwdy__vklze = builder.icmp_unsigned('!=', ebz__whq, lir.
                    Constant(lir.IntType(8), 0))
                return builder.sext(wzwdy__vklze, lir.IntType(8))
            return types.int8(types.voidptr, types.int64), codegen
        return checkna_func
    elif isinstance(col_array_dtype, types.Array):
        col_dtype = col_array_dtype.dtype
        if col_dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    ptuma__jkcra, ldgyf__afdk = args
                    ptuma__jkcra = builder.bitcast(ptuma__jkcra, lir.
                        IntType(8).as_pointer().as_pointer())
                    blvzg__dfjrk = lir.Constant(lir.IntType(64), c_ind)
                    rci__lumfx = builder.load(builder.gep(ptuma__jkcra, [
                        blvzg__dfjrk]))
                    rci__lumfx = builder.bitcast(rci__lumfx, context.
                        get_data_type(col_dtype).as_pointer())
                    oosri__jeu = builder.load(builder.gep(rci__lumfx, [
                        ldgyf__afdk]))
                    wzwdy__vklze = builder.icmp_unsigned('!=', oosri__jeu,
                        lir.Constant(lir.IntType(64), pd._libs.iNaT))
                    return builder.sext(wzwdy__vklze, lir.IntType(8))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
        elif isinstance(col_dtype, types.Float):

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    ptuma__jkcra, ldgyf__afdk = args
                    ptuma__jkcra = builder.bitcast(ptuma__jkcra, lir.
                        IntType(8).as_pointer().as_pointer())
                    blvzg__dfjrk = lir.Constant(lir.IntType(64), c_ind)
                    rci__lumfx = builder.load(builder.gep(ptuma__jkcra, [
                        blvzg__dfjrk]))
                    rci__lumfx = builder.bitcast(rci__lumfx, context.
                        get_data_type(col_dtype).as_pointer())
                    oosri__jeu = builder.load(builder.gep(rci__lumfx, [
                        ldgyf__afdk]))
                    zihij__rxxpf = signature(types.bool_, col_dtype)
                    ebz__whq = numba.np.npyfuncs.np_real_isnan_impl(context,
                        builder, zihij__rxxpf, (oosri__jeu,))
                    return builder.not_(builder.sext(ebz__whq, lir.IntType(8)))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
    raise BodoError(
        f"General Join Conditions with '{col_array_dtype}' column type not supported"
        )
