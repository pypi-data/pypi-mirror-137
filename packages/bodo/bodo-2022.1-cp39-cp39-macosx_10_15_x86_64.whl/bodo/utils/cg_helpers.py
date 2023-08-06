"""helper functions for code generation with llvmlite
"""
import llvmlite.binding as ll
from llvmlite import ir as lir
from numba.core import cgutils, types
import bodo
from bodo.libs import array_ext, hdist
ll.add_symbol('array_getitem', array_ext.array_getitem)
ll.add_symbol('seq_getitem', array_ext.seq_getitem)
ll.add_symbol('list_check', array_ext.list_check)
ll.add_symbol('dict_keys', array_ext.dict_keys)
ll.add_symbol('dict_values', array_ext.dict_values)
ll.add_symbol('dict_merge_from_seq2', array_ext.dict_merge_from_seq2)
ll.add_symbol('is_na_value', array_ext.is_na_value)


def set_bitmap_bit(builder, null_bitmap_ptr, ind, val):
    tzu__khx = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    hengw__logf = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    uwui__mxnmr = builder.gep(null_bitmap_ptr, [tzu__khx], inbounds=True)
    ovryc__kowx = builder.load(uwui__mxnmr)
    reumm__cte = lir.ArrayType(lir.IntType(8), 8)
    qossw__bzxtp = cgutils.alloca_once_value(builder, lir.Constant(
        reumm__cte, (1, 2, 4, 8, 16, 32, 64, 128)))
    qbre__stog = builder.load(builder.gep(qossw__bzxtp, [lir.Constant(lir.
        IntType(64), 0), hengw__logf], inbounds=True))
    if val:
        builder.store(builder.or_(ovryc__kowx, qbre__stog), uwui__mxnmr)
    else:
        qbre__stog = builder.xor(qbre__stog, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(ovryc__kowx, qbre__stog), uwui__mxnmr)


def get_bitmap_bit(builder, null_bitmap_ptr, ind):
    tzu__khx = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    hengw__logf = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    ovryc__kowx = builder.load(builder.gep(null_bitmap_ptr, [tzu__khx],
        inbounds=True))
    reumm__cte = lir.ArrayType(lir.IntType(8), 8)
    qossw__bzxtp = cgutils.alloca_once_value(builder, lir.Constant(
        reumm__cte, (1, 2, 4, 8, 16, 32, 64, 128)))
    qbre__stog = builder.load(builder.gep(qossw__bzxtp, [lir.Constant(lir.
        IntType(64), 0), hengw__logf], inbounds=True))
    return builder.and_(ovryc__kowx, qbre__stog)


def pyarray_getitem(builder, context, arr_obj, ind):
    jdhwn__vvzg = context.get_argument_type(types.pyobject)
    xjh__cnpgf = context.get_value_type(types.intp)
    rpjp__pfbcz = lir.FunctionType(lir.IntType(8).as_pointer(), [
        jdhwn__vvzg, xjh__cnpgf])
    srus__zba = cgutils.get_or_insert_function(builder.module, rpjp__pfbcz,
        name='array_getptr1')
    yxptk__marks = lir.FunctionType(jdhwn__vvzg, [jdhwn__vvzg, lir.IntType(
        8).as_pointer()])
    iwzjj__fdj = cgutils.get_or_insert_function(builder.module,
        yxptk__marks, name='array_getitem')
    uxir__pon = builder.call(srus__zba, [arr_obj, ind])
    return builder.call(iwzjj__fdj, [arr_obj, uxir__pon])


def pyarray_setitem(builder, context, arr_obj, ind, val_obj):
    jdhwn__vvzg = context.get_argument_type(types.pyobject)
    xjh__cnpgf = context.get_value_type(types.intp)
    rpjp__pfbcz = lir.FunctionType(lir.IntType(8).as_pointer(), [
        jdhwn__vvzg, xjh__cnpgf])
    srus__zba = cgutils.get_or_insert_function(builder.module, rpjp__pfbcz,
        name='array_getptr1')
    jmuld__hyo = lir.FunctionType(lir.VoidType(), [jdhwn__vvzg, lir.IntType
        (8).as_pointer(), jdhwn__vvzg])
    tps__tcyn = cgutils.get_or_insert_function(builder.module, jmuld__hyo,
        name='array_setitem')
    uxir__pon = builder.call(srus__zba, [arr_obj, ind])
    builder.call(tps__tcyn, [arr_obj, uxir__pon, val_obj])


def seq_getitem(builder, context, obj, ind):
    jdhwn__vvzg = context.get_argument_type(types.pyobject)
    xjh__cnpgf = context.get_value_type(types.intp)
    zwrrm__eumg = lir.FunctionType(jdhwn__vvzg, [jdhwn__vvzg, xjh__cnpgf])
    pdj__itf = cgutils.get_or_insert_function(builder.module, zwrrm__eumg,
        name='seq_getitem')
    return builder.call(pdj__itf, [obj, ind])


def is_na_value(builder, context, val, C_NA):
    jdhwn__vvzg = context.get_argument_type(types.pyobject)
    swq__yit = lir.FunctionType(lir.IntType(32), [jdhwn__vvzg, jdhwn__vvzg])
    tqe__bze = cgutils.get_or_insert_function(builder.module, swq__yit,
        name='is_na_value')
    return builder.call(tqe__bze, [val, C_NA])


def list_check(builder, context, obj):
    jdhwn__vvzg = context.get_argument_type(types.pyobject)
    csgv__vtak = context.get_value_type(types.int32)
    smqzl__ftvqt = lir.FunctionType(csgv__vtak, [jdhwn__vvzg])
    jhbbs__xcw = cgutils.get_or_insert_function(builder.module,
        smqzl__ftvqt, name='list_check')
    return builder.call(jhbbs__xcw, [obj])


def dict_keys(builder, context, obj):
    jdhwn__vvzg = context.get_argument_type(types.pyobject)
    smqzl__ftvqt = lir.FunctionType(jdhwn__vvzg, [jdhwn__vvzg])
    jhbbs__xcw = cgutils.get_or_insert_function(builder.module,
        smqzl__ftvqt, name='dict_keys')
    return builder.call(jhbbs__xcw, [obj])


def dict_values(builder, context, obj):
    jdhwn__vvzg = context.get_argument_type(types.pyobject)
    smqzl__ftvqt = lir.FunctionType(jdhwn__vvzg, [jdhwn__vvzg])
    jhbbs__xcw = cgutils.get_or_insert_function(builder.module,
        smqzl__ftvqt, name='dict_values')
    return builder.call(jhbbs__xcw, [obj])


def dict_merge_from_seq2(builder, context, dict_obj, seq2_obj):
    jdhwn__vvzg = context.get_argument_type(types.pyobject)
    smqzl__ftvqt = lir.FunctionType(lir.VoidType(), [jdhwn__vvzg, jdhwn__vvzg])
    jhbbs__xcw = cgutils.get_or_insert_function(builder.module,
        smqzl__ftvqt, name='dict_merge_from_seq2')
    builder.call(jhbbs__xcw, [dict_obj, seq2_obj])


def to_arr_obj_if_list_obj(c, context, builder, val, typ):
    if not (isinstance(typ, types.List) or bodo.utils.utils.is_array_typ(
        typ, False)):
        return val
    bdd__toso = cgutils.alloca_once_value(builder, val)
    doyd__gcdao = list_check(builder, context, val)
    oazm__knnc = builder.icmp_unsigned('!=', doyd__gcdao, lir.Constant(
        doyd__gcdao.type, 0))
    with builder.if_then(oazm__knnc):
        akdq__vkay = context.insert_const_string(builder.module, 'numpy')
        xtb__hny = c.pyapi.import_module_noblock(akdq__vkay)
        ydtca__hef = 'object_'
        if isinstance(typ, types.Array) or isinstance(typ.dtype, types.Float):
            ydtca__hef = str(typ.dtype)
        unct__vbwx = c.pyapi.object_getattr_string(xtb__hny, ydtca__hef)
        bbnns__dxth = builder.load(bdd__toso)
        dbxr__gny = c.pyapi.call_method(xtb__hny, 'asarray', (bbnns__dxth,
            unct__vbwx))
        builder.store(dbxr__gny, bdd__toso)
        c.pyapi.decref(xtb__hny)
        c.pyapi.decref(unct__vbwx)
    val = builder.load(bdd__toso)
    return val


def get_array_elem_counts(c, builder, context, arr_obj, typ):
    from bodo.libs.array_item_arr_ext import ArrayItemArrayType
    from bodo.libs.map_arr_ext import MapArrayType
    from bodo.libs.str_arr_ext import get_utf8_size, string_array_type
    from bodo.libs.struct_arr_ext import StructArrayType, StructType
    from bodo.libs.tuple_arr_ext import TupleArrayType
    if typ == bodo.string_type:
        coqqr__vncg = c.pyapi.to_native_value(bodo.string_type, arr_obj).value
        tjz__tcmq, rzzrn__mphq = c.pyapi.call_jit_code(lambda a:
            get_utf8_size(a), types.int64(bodo.string_type), [coqqr__vncg])
        context.nrt.decref(builder, typ, coqqr__vncg)
        return cgutils.pack_array(builder, [rzzrn__mphq])
    if isinstance(typ, (StructType, types.BaseTuple)):
        akdq__vkay = context.insert_const_string(builder.module, 'pandas')
        qmby__nlpl = c.pyapi.import_module_noblock(akdq__vkay)
        C_NA = c.pyapi.object_getattr_string(qmby__nlpl, 'NA')
        actw__exi = bodo.utils.transform.get_type_alloc_counts(typ)
        idkl__swhb = context.make_tuple(builder, types.Tuple(actw__exi * [
            types.int64]), actw__exi * [context.get_constant(types.int64, 0)])
        nkvww__dpxm = cgutils.alloca_once_value(builder, idkl__swhb)
        jpq__vpl = 0
        kdgx__vdvn = typ.data if isinstance(typ, StructType) else typ.types
        for ixkif__dvp, t in enumerate(kdgx__vdvn):
            wmc__ent = bodo.utils.transform.get_type_alloc_counts(t)
            if wmc__ent == 0:
                continue
            if isinstance(typ, StructType):
                val_obj = c.pyapi.dict_getitem_string(arr_obj, typ.names[
                    ixkif__dvp])
            else:
                val_obj = c.pyapi.tuple_getitem(arr_obj, ixkif__dvp)
            tlahc__rek = is_na_value(builder, context, val_obj, C_NA)
            ftybk__casih = builder.icmp_unsigned('!=', tlahc__rek, lir.
                Constant(tlahc__rek.type, 1))
            with builder.if_then(ftybk__casih):
                idkl__swhb = builder.load(nkvww__dpxm)
                ydqb__ahcni = get_array_elem_counts(c, builder, context,
                    val_obj, t)
                for ixkif__dvp in range(wmc__ent):
                    edrw__wnuak = builder.extract_value(idkl__swhb, 
                        jpq__vpl + ixkif__dvp)
                    xrhv__jmv = builder.extract_value(ydqb__ahcni, ixkif__dvp)
                    idkl__swhb = builder.insert_value(idkl__swhb, builder.
                        add(edrw__wnuak, xrhv__jmv), jpq__vpl + ixkif__dvp)
                builder.store(idkl__swhb, nkvww__dpxm)
            jpq__vpl += wmc__ent
        c.pyapi.decref(qmby__nlpl)
        c.pyapi.decref(C_NA)
        return builder.load(nkvww__dpxm)
    if not bodo.utils.utils.is_array_typ(typ, False):
        return cgutils.pack_array(builder, [], lir.IntType(64))
    n = bodo.utils.utils.object_length(c, arr_obj)
    if not (isinstance(typ, (ArrayItemArrayType, StructArrayType,
        TupleArrayType, MapArrayType)) or typ == string_array_type):
        return cgutils.pack_array(builder, [n])
    akdq__vkay = context.insert_const_string(builder.module, 'pandas')
    qmby__nlpl = c.pyapi.import_module_noblock(akdq__vkay)
    C_NA = c.pyapi.object_getattr_string(qmby__nlpl, 'NA')
    actw__exi = bodo.utils.transform.get_type_alloc_counts(typ)
    idkl__swhb = context.make_tuple(builder, types.Tuple(actw__exi * [types
        .int64]), [n] + (actw__exi - 1) * [context.get_constant(types.int64,
        0)])
    nkvww__dpxm = cgutils.alloca_once_value(builder, idkl__swhb)
    with cgutils.for_range(builder, n) as loop:
        iqkbk__trl = loop.index
        ffhi__hwwct = seq_getitem(builder, context, arr_obj, iqkbk__trl)
        tlahc__rek = is_na_value(builder, context, ffhi__hwwct, C_NA)
        ftybk__casih = builder.icmp_unsigned('!=', tlahc__rek, lir.Constant
            (tlahc__rek.type, 1))
        with builder.if_then(ftybk__casih):
            if isinstance(typ, ArrayItemArrayType) or typ == string_array_type:
                idkl__swhb = builder.load(nkvww__dpxm)
                ydqb__ahcni = get_array_elem_counts(c, builder, context,
                    ffhi__hwwct, typ.dtype)
                for ixkif__dvp in range(actw__exi - 1):
                    edrw__wnuak = builder.extract_value(idkl__swhb, 
                        ixkif__dvp + 1)
                    xrhv__jmv = builder.extract_value(ydqb__ahcni, ixkif__dvp)
                    idkl__swhb = builder.insert_value(idkl__swhb, builder.
                        add(edrw__wnuak, xrhv__jmv), ixkif__dvp + 1)
                builder.store(idkl__swhb, nkvww__dpxm)
            elif isinstance(typ, (StructArrayType, TupleArrayType)):
                jpq__vpl = 1
                for ixkif__dvp, t in enumerate(typ.data):
                    wmc__ent = bodo.utils.transform.get_type_alloc_counts(t
                        .dtype)
                    if wmc__ent == 0:
                        continue
                    if isinstance(typ, TupleArrayType):
                        val_obj = c.pyapi.tuple_getitem(ffhi__hwwct, ixkif__dvp
                            )
                    else:
                        val_obj = c.pyapi.dict_getitem_string(ffhi__hwwct,
                            typ.names[ixkif__dvp])
                    tlahc__rek = is_na_value(builder, context, val_obj, C_NA)
                    ftybk__casih = builder.icmp_unsigned('!=', tlahc__rek,
                        lir.Constant(tlahc__rek.type, 1))
                    with builder.if_then(ftybk__casih):
                        idkl__swhb = builder.load(nkvww__dpxm)
                        ydqb__ahcni = get_array_elem_counts(c, builder,
                            context, val_obj, t.dtype)
                        for ixkif__dvp in range(wmc__ent):
                            edrw__wnuak = builder.extract_value(idkl__swhb,
                                jpq__vpl + ixkif__dvp)
                            xrhv__jmv = builder.extract_value(ydqb__ahcni,
                                ixkif__dvp)
                            idkl__swhb = builder.insert_value(idkl__swhb,
                                builder.add(edrw__wnuak, xrhv__jmv), 
                                jpq__vpl + ixkif__dvp)
                        builder.store(idkl__swhb, nkvww__dpxm)
                    jpq__vpl += wmc__ent
            else:
                assert isinstance(typ, MapArrayType), typ
                idkl__swhb = builder.load(nkvww__dpxm)
                cgk__rgm = dict_keys(builder, context, ffhi__hwwct)
                zpe__ibgx = dict_values(builder, context, ffhi__hwwct)
                rwzw__oykru = get_array_elem_counts(c, builder, context,
                    cgk__rgm, typ.key_arr_type)
                avr__lkboi = bodo.utils.transform.get_type_alloc_counts(typ
                    .key_arr_type)
                for ixkif__dvp in range(1, avr__lkboi + 1):
                    edrw__wnuak = builder.extract_value(idkl__swhb, ixkif__dvp)
                    xrhv__jmv = builder.extract_value(rwzw__oykru, 
                        ixkif__dvp - 1)
                    idkl__swhb = builder.insert_value(idkl__swhb, builder.
                        add(edrw__wnuak, xrhv__jmv), ixkif__dvp)
                vjv__sggys = get_array_elem_counts(c, builder, context,
                    zpe__ibgx, typ.value_arr_type)
                for ixkif__dvp in range(avr__lkboi + 1, actw__exi):
                    edrw__wnuak = builder.extract_value(idkl__swhb, ixkif__dvp)
                    xrhv__jmv = builder.extract_value(vjv__sggys, 
                        ixkif__dvp - avr__lkboi)
                    idkl__swhb = builder.insert_value(idkl__swhb, builder.
                        add(edrw__wnuak, xrhv__jmv), ixkif__dvp)
                builder.store(idkl__swhb, nkvww__dpxm)
                c.pyapi.decref(cgk__rgm)
                c.pyapi.decref(zpe__ibgx)
        c.pyapi.decref(ffhi__hwwct)
    c.pyapi.decref(qmby__nlpl)
    c.pyapi.decref(C_NA)
    return builder.load(nkvww__dpxm)


def gen_allocate_array(context, builder, arr_type, n_elems, c=None):
    zhkb__oetbk = n_elems.type.count
    assert zhkb__oetbk >= 1
    ujo__ptx = builder.extract_value(n_elems, 0)
    if zhkb__oetbk != 1:
        bjib__tbjnm = cgutils.pack_array(builder, [builder.extract_value(
            n_elems, ixkif__dvp) for ixkif__dvp in range(1, zhkb__oetbk)])
        mwpro__qfo = types.Tuple([types.int64] * (zhkb__oetbk - 1))
    else:
        bjib__tbjnm = context.get_dummy_value()
        mwpro__qfo = types.none
    dgfg__zgif = types.TypeRef(arr_type)
    sba__vtocz = arr_type(types.int64, dgfg__zgif, mwpro__qfo)
    args = [ujo__ptx, context.get_dummy_value(), bjib__tbjnm]
    eryto__jqq = lambda n, t, s: bodo.utils.utils.alloc_type(n, t, s)
    if c:
        tjz__tcmq, cqn__pkaz = c.pyapi.call_jit_code(eryto__jqq, sba__vtocz,
            args)
    else:
        cqn__pkaz = context.compile_internal(builder, eryto__jqq,
            sba__vtocz, args)
    return cqn__pkaz


def is_ll_eq(builder, val1, val2):
    tdyd__iimzx = val1.type.pointee
    ncgmm__wtgpc = val2.type.pointee
    assert tdyd__iimzx == ncgmm__wtgpc, 'invalid llvm value comparison'
    if isinstance(tdyd__iimzx, (lir.BaseStructType, lir.ArrayType)):
        n_elems = len(tdyd__iimzx.elements) if isinstance(tdyd__iimzx, lir.
            BaseStructType) else tdyd__iimzx.count
        htw__tfzz = lir.Constant(lir.IntType(1), 1)
        for ixkif__dvp in range(n_elems):
            xfbyv__czqf = lir.IntType(32)(0)
            wytxr__fnp = lir.IntType(32)(ixkif__dvp)
            cucu__hojc = builder.gep(val1, [xfbyv__czqf, wytxr__fnp],
                inbounds=True)
            eqzss__mrky = builder.gep(val2, [xfbyv__czqf, wytxr__fnp],
                inbounds=True)
            htw__tfzz = builder.and_(htw__tfzz, is_ll_eq(builder,
                cucu__hojc, eqzss__mrky))
        return htw__tfzz
    ixy__hdnss = builder.load(val1)
    sgi__mxn = builder.load(val2)
    if ixy__hdnss.type in (lir.FloatType(), lir.DoubleType()):
        ahl__asetn = 32 if ixy__hdnss.type == lir.FloatType() else 64
        ixy__hdnss = builder.bitcast(ixy__hdnss, lir.IntType(ahl__asetn))
        sgi__mxn = builder.bitcast(sgi__mxn, lir.IntType(ahl__asetn))
    return builder.icmp_unsigned('==', ixy__hdnss, sgi__mxn)
