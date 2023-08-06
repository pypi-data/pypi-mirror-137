import operator
import llvmlite.binding as ll
import numba
import numba.core.typing.typeof
import numpy as np
from llvmlite import ir as lir
from llvmlite.llvmpy.core import Type as LLType
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, impl_ret_new_ref
from numba.extending import box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, register_model
import bodo
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import offset_type
from bodo.libs.str_arr_ext import _get_str_binary_arr_payload, _memcpy, char_arr_type, get_data_ptr, null_bitmap_arr_type, offset_arr_type, string_array_type
ll.add_symbol('array_setitem', hstr_ext.array_setitem)
ll.add_symbol('array_getptr1', hstr_ext.array_getptr1)
ll.add_symbol('dtor_str_arr_split_view', hstr_ext.dtor_str_arr_split_view)
ll.add_symbol('str_arr_split_view_impl', hstr_ext.str_arr_split_view_impl)
ll.add_symbol('str_arr_split_view_alloc', hstr_ext.str_arr_split_view_alloc)
char_typ = types.uint8
data_ctypes_type = types.ArrayCTypes(types.Array(char_typ, 1, 'C'))
offset_ctypes_type = types.ArrayCTypes(types.Array(offset_type, 1, 'C'))


class StringArraySplitViewType(types.ArrayCompatible):

    def __init__(self):
        super(StringArraySplitViewType, self).__init__(name=
            'StringArraySplitViewType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_array_type

    def copy(self):
        return StringArraySplitViewType()


string_array_split_view_type = StringArraySplitViewType()


class StringArraySplitViewPayloadType(types.Type):

    def __init__(self):
        super(StringArraySplitViewPayloadType, self).__init__(name=
            'StringArraySplitViewPayloadType()')


str_arr_split_view_payload_type = StringArraySplitViewPayloadType()


@register_model(StringArraySplitViewPayloadType)
class StringArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        icni__bixe = [('index_offsets', types.CPointer(offset_type)), (
            'data_offsets', types.CPointer(offset_type)), ('null_bitmap',
            types.CPointer(char_typ))]
        models.StructModel.__init__(self, dmm, fe_type, icni__bixe)


str_arr_model_members = [('num_items', types.uint64), ('index_offsets',
    types.CPointer(offset_type)), ('data_offsets', types.CPointer(
    offset_type)), ('data', data_ctypes_type), ('null_bitmap', types.
    CPointer(char_typ)), ('meminfo', types.MemInfoPointer(
    str_arr_split_view_payload_type))]


@register_model(StringArraySplitViewType)
class StringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        models.StructModel.__init__(self, dmm, fe_type, str_arr_model_members)


make_attribute_wrapper(StringArraySplitViewType, 'num_items', '_num_items')
make_attribute_wrapper(StringArraySplitViewType, 'index_offsets',
    '_index_offsets')
make_attribute_wrapper(StringArraySplitViewType, 'data_offsets',
    '_data_offsets')
make_attribute_wrapper(StringArraySplitViewType, 'data', '_data')
make_attribute_wrapper(StringArraySplitViewType, 'null_bitmap', '_null_bitmap')


def construct_str_arr_split_view(context, builder):
    vzj__hhqw = context.get_value_type(str_arr_split_view_payload_type)
    ntau__cyuo = context.get_abi_sizeof(vzj__hhqw)
    tcwxq__jeg = context.get_value_type(types.voidptr)
    fpt__yzpcp = context.get_value_type(types.uintp)
    hfy__fovm = lir.FunctionType(lir.VoidType(), [tcwxq__jeg, fpt__yzpcp,
        tcwxq__jeg])
    fbx__tgar = cgutils.get_or_insert_function(builder.module, hfy__fovm,
        name='dtor_str_arr_split_view')
    ddllk__mis = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, ntau__cyuo), fbx__tgar)
    nmkju__cmc = context.nrt.meminfo_data(builder, ddllk__mis)
    oau__sdeij = builder.bitcast(nmkju__cmc, vzj__hhqw.as_pointer())
    return ddllk__mis, oau__sdeij


@intrinsic
def compute_split_view(typingctx, str_arr_typ, sep_typ=None):
    assert str_arr_typ == string_array_type and isinstance(sep_typ, types.
        StringLiteral)

    def codegen(context, builder, sig, args):
        qzexl__qqwm, eoh__ajn = args
        ddllk__mis, oau__sdeij = construct_str_arr_split_view(context, builder)
        kinw__vyqo = _get_str_binary_arr_payload(context, builder,
            qzexl__qqwm, string_array_type)
        innit__ytj = lir.FunctionType(lir.VoidType(), [oau__sdeij.type, lir
            .IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8)])
        zvfit__gcmo = cgutils.get_or_insert_function(builder.module,
            innit__ytj, name='str_arr_split_view_impl')
        sal__cdyte = context.make_helper(builder, offset_arr_type,
            kinw__vyqo.offsets).data
        rbtxp__nrgvu = context.make_helper(builder, char_arr_type,
            kinw__vyqo.data).data
        qumte__lorgp = context.make_helper(builder, null_bitmap_arr_type,
            kinw__vyqo.null_bitmap).data
        ciyoh__zxqpr = context.get_constant(types.int8, ord(sep_typ.
            literal_value))
        builder.call(zvfit__gcmo, [oau__sdeij, kinw__vyqo.n_arrays,
            sal__cdyte, rbtxp__nrgvu, qumte__lorgp, ciyoh__zxqpr])
        vlqd__nhet = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(oau__sdeij))
        tllj__fasr = context.make_helper(builder, string_array_split_view_type)
        tllj__fasr.num_items = kinw__vyqo.n_arrays
        tllj__fasr.index_offsets = vlqd__nhet.index_offsets
        tllj__fasr.data_offsets = vlqd__nhet.data_offsets
        tllj__fasr.data = context.compile_internal(builder, lambda S:
            get_data_ptr(S), data_ctypes_type(string_array_type), [qzexl__qqwm]
            )
        tllj__fasr.null_bitmap = vlqd__nhet.null_bitmap
        tllj__fasr.meminfo = ddllk__mis
        cmor__kuyro = tllj__fasr._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, cmor__kuyro)
    return string_array_split_view_type(string_array_type, sep_typ), codegen


@box(StringArraySplitViewType)
def box_str_arr_split_view(typ, val, c):
    context = c.context
    builder = c.builder
    aeb__vvs = context.make_helper(builder, string_array_split_view_type, val)
    vzue__dfu = context.insert_const_string(builder.module, 'numpy')
    ngcmg__apmxt = c.pyapi.import_module_noblock(vzue__dfu)
    dtype = c.pyapi.object_getattr_string(ngcmg__apmxt, 'object_')
    qtpt__owgkc = builder.sext(aeb__vvs.num_items, c.pyapi.longlong)
    ess__rltb = c.pyapi.long_from_longlong(qtpt__owgkc)
    oyo__nsak = c.pyapi.call_method(ngcmg__apmxt, 'ndarray', (ess__rltb, dtype)
        )
    zvkkk__xaxga = LLType.function(lir.IntType(8).as_pointer(), [c.pyapi.
        pyobj, c.pyapi.py_ssize_t])
    jcu__upo = c.pyapi._get_function(zvkkk__xaxga, name='array_getptr1')
    tabgy__lpdsv = LLType.function(lir.VoidType(), [c.pyapi.pyobj, lir.
        IntType(8).as_pointer(), c.pyapi.pyobj])
    zwh__pinxl = c.pyapi._get_function(tabgy__lpdsv, name='array_setitem')
    eaqpk__qcd = c.pyapi.object_getattr_string(ngcmg__apmxt, 'nan')
    with cgutils.for_range(builder, aeb__vvs.num_items) as loop:
        str_ind = loop.index
        shnme__ewi = builder.sext(builder.load(builder.gep(aeb__vvs.
            index_offsets, [str_ind])), lir.IntType(64))
        mcg__khx = builder.sext(builder.load(builder.gep(aeb__vvs.
            index_offsets, [builder.add(str_ind, str_ind.type(1))])), lir.
            IntType(64))
        xvdu__ygeu = builder.lshr(str_ind, lir.Constant(lir.IntType(64), 3))
        gub__okjx = builder.gep(aeb__vvs.null_bitmap, [xvdu__ygeu])
        tbhnf__yfz = builder.load(gub__okjx)
        cem__bze = builder.trunc(builder.and_(str_ind, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = builder.and_(builder.lshr(tbhnf__yfz, cem__bze), lir.Constant
            (lir.IntType(8), 1))
        oqcip__eswsv = builder.sub(mcg__khx, shnme__ewi)
        oqcip__eswsv = builder.sub(oqcip__eswsv, oqcip__eswsv.type(1))
        udgof__ubl = builder.call(jcu__upo, [oyo__nsak, str_ind])
        legkh__smdw = c.builder.icmp_unsigned('!=', val, val.type(0))
        with c.builder.if_else(legkh__smdw) as (then, otherwise):
            with then:
                xkw__izcqg = c.pyapi.list_new(oqcip__eswsv)
                with c.builder.if_then(cgutils.is_not_null(c.builder,
                    xkw__izcqg), likely=True):
                    with cgutils.for_range(c.builder, oqcip__eswsv) as loop:
                        vrlk__dnm = builder.add(shnme__ewi, loop.index)
                        data_start = builder.load(builder.gep(aeb__vvs.
                            data_offsets, [vrlk__dnm]))
                        data_start = builder.add(data_start, data_start.type(1)
                            )
                        lxje__ugf = builder.load(builder.gep(aeb__vvs.
                            data_offsets, [builder.add(vrlk__dnm, vrlk__dnm
                            .type(1))]))
                        hcij__getoz = builder.gep(builder.extract_value(
                            aeb__vvs.data, 0), [data_start])
                        heqdg__gcum = builder.sext(builder.sub(lxje__ugf,
                            data_start), lir.IntType(64))
                        hlr__jhftp = c.pyapi.string_from_string_and_size(
                            hcij__getoz, heqdg__gcum)
                        c.pyapi.list_setitem(xkw__izcqg, loop.index, hlr__jhftp
                            )
                builder.call(zwh__pinxl, [oyo__nsak, udgof__ubl, xkw__izcqg])
            with otherwise:
                builder.call(zwh__pinxl, [oyo__nsak, udgof__ubl, eaqpk__qcd])
    c.pyapi.decref(ngcmg__apmxt)
    c.pyapi.decref(dtype)
    c.pyapi.decref(eaqpk__qcd)
    return oyo__nsak


@intrinsic
def pre_alloc_str_arr_view(typingctx, num_items_t, num_offsets_t, data_t=None):
    assert num_items_t == types.intp and num_offsets_t == types.intp

    def codegen(context, builder, sig, args):
        yeqg__fiqb, ujyrz__yyef, hcij__getoz = args
        ddllk__mis, oau__sdeij = construct_str_arr_split_view(context, builder)
        innit__ytj = lir.FunctionType(lir.VoidType(), [oau__sdeij.type, lir
            .IntType(64), lir.IntType(64)])
        zvfit__gcmo = cgutils.get_or_insert_function(builder.module,
            innit__ytj, name='str_arr_split_view_alloc')
        builder.call(zvfit__gcmo, [oau__sdeij, yeqg__fiqb, ujyrz__yyef])
        vlqd__nhet = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(oau__sdeij))
        tllj__fasr = context.make_helper(builder, string_array_split_view_type)
        tllj__fasr.num_items = yeqg__fiqb
        tllj__fasr.index_offsets = vlqd__nhet.index_offsets
        tllj__fasr.data_offsets = vlqd__nhet.data_offsets
        tllj__fasr.data = hcij__getoz
        tllj__fasr.null_bitmap = vlqd__nhet.null_bitmap
        context.nrt.incref(builder, data_t, hcij__getoz)
        tllj__fasr.meminfo = ddllk__mis
        cmor__kuyro = tllj__fasr._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, cmor__kuyro)
    return string_array_split_view_type(types.intp, types.intp, data_t
        ), codegen


@intrinsic
def get_c_arr_ptr(typingctx, c_arr, ind_t=None):
    assert isinstance(c_arr, (types.CPointer, types.ArrayCTypes))

    def codegen(context, builder, sig, args):
        jlmfb__mjt, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            jlmfb__mjt = builder.extract_value(jlmfb__mjt, 0)
        return builder.bitcast(builder.gep(jlmfb__mjt, [ind]), lir.IntType(
            8).as_pointer())
    return types.voidptr(c_arr, ind_t), codegen


@intrinsic
def getitem_c_arr(typingctx, c_arr, ind_t=None):

    def codegen(context, builder, sig, args):
        jlmfb__mjt, ind = args
        return builder.load(builder.gep(jlmfb__mjt, [ind]))
    return c_arr.dtype(c_arr, ind_t), codegen


@intrinsic
def setitem_c_arr(typingctx, c_arr, ind_t, item_t=None):

    def codegen(context, builder, sig, args):
        jlmfb__mjt, ind, jbsgd__kcie = args
        gztl__aapb = builder.gep(jlmfb__mjt, [ind])
        builder.store(jbsgd__kcie, gztl__aapb)
    return types.void(c_arr, ind_t, c_arr.dtype), codegen


@intrinsic
def get_array_ctypes_ptr(typingctx, arr_ctypes_t, ind_t=None):

    def codegen(context, builder, sig, args):
        iach__usw, ind = args
        syve__etjy = context.make_helper(builder, arr_ctypes_t, iach__usw)
        lhici__jsy = context.make_helper(builder, arr_ctypes_t)
        lhici__jsy.data = builder.gep(syve__etjy.data, [ind])
        lhici__jsy.meminfo = syve__etjy.meminfo
        idog__djkm = lhici__jsy._getvalue()
        return impl_ret_borrowed(context, builder, arr_ctypes_t, idog__djkm)
    return arr_ctypes_t(arr_ctypes_t, ind_t), codegen


@numba.njit(no_cpython_wrapper=True)
def get_split_view_index(arr, item_ind, str_ind):
    phsjh__dugbk = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr.
        _null_bitmap, item_ind)
    if not phsjh__dugbk:
        return 0, 0, 0
    vrlk__dnm = getitem_c_arr(arr._index_offsets, item_ind)
    evd__khwm = getitem_c_arr(arr._index_offsets, item_ind + 1) - 1
    tajhi__srxpm = evd__khwm - vrlk__dnm
    if str_ind >= tajhi__srxpm:
        return 0, 0, 0
    data_start = getitem_c_arr(arr._data_offsets, vrlk__dnm + str_ind)
    data_start += 1
    if vrlk__dnm + str_ind == 0:
        data_start = 0
    lxje__ugf = getitem_c_arr(arr._data_offsets, vrlk__dnm + str_ind + 1)
    mhs__xga = lxje__ugf - data_start
    return 1, data_start, mhs__xga


@numba.njit(no_cpython_wrapper=True)
def get_split_view_data_ptr(arr, data_start):
    return get_array_ctypes_ptr(arr._data, data_start)


@overload(len, no_unliteral=True)
def str_arr_split_view_len_overload(arr):
    if arr == string_array_split_view_type:
        return lambda arr: np.int64(arr._num_items)


@overload_attribute(StringArraySplitViewType, 'shape')
def overload_split_view_arr_shape(A):
    return lambda A: (np.int64(A._num_items),)


@overload(operator.getitem, no_unliteral=True)
def str_arr_split_view_getitem_overload(A, ind):
    if A != string_array_split_view_type:
        return
    if A == string_array_split_view_type and isinstance(ind, types.Integer):
        ultil__tyc = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def _impl(A, ind):
            vrlk__dnm = getitem_c_arr(A._index_offsets, ind)
            evd__khwm = getitem_c_arr(A._index_offsets, ind + 1)
            masn__cknjf = evd__khwm - vrlk__dnm - 1
            qzexl__qqwm = bodo.libs.str_arr_ext.pre_alloc_string_array(
                masn__cknjf, -1)
            for tovq__ldq in range(masn__cknjf):
                data_start = getitem_c_arr(A._data_offsets, vrlk__dnm +
                    tovq__ldq)
                data_start += 1
                if vrlk__dnm + tovq__ldq == 0:
                    data_start = 0
                lxje__ugf = getitem_c_arr(A._data_offsets, vrlk__dnm +
                    tovq__ldq + 1)
                mhs__xga = lxje__ugf - data_start
                gztl__aapb = get_array_ctypes_ptr(A._data, data_start)
                liabg__mfeb = bodo.libs.str_arr_ext.decode_utf8(gztl__aapb,
                    mhs__xga)
                qzexl__qqwm[tovq__ldq] = liabg__mfeb
            return qzexl__qqwm
        return _impl
    if A == string_array_split_view_type and ind == types.Array(types.bool_,
        1, 'C'):
        vgmam__gdjrb = offset_type.bitwidth // 8

        def _impl(A, ind):
            masn__cknjf = len(A)
            if masn__cknjf != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            yeqg__fiqb = 0
            ujyrz__yyef = 0
            for tovq__ldq in range(masn__cknjf):
                if ind[tovq__ldq]:
                    yeqg__fiqb += 1
                    vrlk__dnm = getitem_c_arr(A._index_offsets, tovq__ldq)
                    evd__khwm = getitem_c_arr(A._index_offsets, tovq__ldq + 1)
                    ujyrz__yyef += evd__khwm - vrlk__dnm
            oyo__nsak = pre_alloc_str_arr_view(yeqg__fiqb, ujyrz__yyef, A._data
                )
            item_ind = 0
            pzhhi__ekkip = 0
            for tovq__ldq in range(masn__cknjf):
                if ind[tovq__ldq]:
                    vrlk__dnm = getitem_c_arr(A._index_offsets, tovq__ldq)
                    evd__khwm = getitem_c_arr(A._index_offsets, tovq__ldq + 1)
                    zrimb__ofqqz = evd__khwm - vrlk__dnm
                    setitem_c_arr(oyo__nsak._index_offsets, item_ind,
                        pzhhi__ekkip)
                    gztl__aapb = get_c_arr_ptr(A._data_offsets, vrlk__dnm)
                    vhff__korm = get_c_arr_ptr(oyo__nsak._data_offsets,
                        pzhhi__ekkip)
                    _memcpy(vhff__korm, gztl__aapb, zrimb__ofqqz, vgmam__gdjrb)
                    phsjh__dugbk = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, tovq__ldq)
                    bodo.libs.int_arr_ext.set_bit_to_arr(oyo__nsak.
                        _null_bitmap, item_ind, phsjh__dugbk)
                    item_ind += 1
                    pzhhi__ekkip += zrimb__ofqqz
            setitem_c_arr(oyo__nsak._index_offsets, item_ind, pzhhi__ekkip)
            return oyo__nsak
        return _impl
