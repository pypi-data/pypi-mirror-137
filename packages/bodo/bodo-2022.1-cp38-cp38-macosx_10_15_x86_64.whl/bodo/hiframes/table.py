"""Table data type for storing dataframe column arrays. Supports storing many columns
(e.g. >10k) efficiently.
"""
import operator
from collections import defaultdict
import numba
import numpy as np
import pandas as pd
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.cpython.listobj import ListInstance
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, register_model, typeof_impl, unbox
from numba.np.arrayobj import _getitem_array_single_int
from numba.parfors.array_analysis import ArrayAnalysis
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.typing import BodoError, get_overload_const_int, is_list_like_index_type, is_overload_constant_int


class Table:

    def __init__(self, arrs, usecols=None, num_arrs=-1):
        if usecols is not None:
            assert num_arrs != -1, 'num_arrs must be provided if usecols is not None'
            anzoe__vcc = 0
            kzoj__nrjs = []
            for i in range(usecols[-1] + 1):
                if i == usecols[anzoe__vcc]:
                    kzoj__nrjs.append(arrs[anzoe__vcc])
                    anzoe__vcc += 1
                else:
                    kzoj__nrjs.append(None)
            for zasd__iak in range(usecols[-1] + 1, num_arrs):
                kzoj__nrjs.append(None)
            self.arrays = kzoj__nrjs
        else:
            self.arrays = arrs
        self.block_0 = arrs

    def __eq__(self, other):
        return isinstance(other, Table) and other.arrays == self.arrays

    def __str__(self) ->str:
        return str(self.arrays)

    def to_pandas(self, index=None):
        ogf__kphz = len(self.arrays)
        kdxvj__dbfac = dict(zip(range(ogf__kphz), self.arrays))
        dhol__nuq = pd.DataFrame(kdxvj__dbfac, index)
        return dhol__nuq


class TableType(types.ArrayCompatible):

    def __init__(self, arr_types, has_runtime_cols=False):
        self.arr_types = arr_types
        self.has_runtime_cols = has_runtime_cols
        hngzg__cicml = []
        bwzp__xubn = []
        ktm__lgisj = {}
        edhi__ikf = defaultdict(int)
        oeru__piz = defaultdict(list)
        if not has_runtime_cols:
            for i, cxszg__lvwuj in enumerate(arr_types):
                if cxszg__lvwuj not in ktm__lgisj:
                    ktm__lgisj[cxszg__lvwuj] = len(ktm__lgisj)
                ykhx__rhzy = ktm__lgisj[cxszg__lvwuj]
                hngzg__cicml.append(ykhx__rhzy)
                bwzp__xubn.append(edhi__ikf[ykhx__rhzy])
                edhi__ikf[ykhx__rhzy] += 1
                oeru__piz[ykhx__rhzy].append(i)
        self.block_nums = hngzg__cicml
        self.block_offsets = bwzp__xubn
        self.type_to_blk = ktm__lgisj
        self.block_to_arr_ind = oeru__piz
        super(TableType, self).__init__(name=
            f'TableType({arr_types}, {has_runtime_cols})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    @property
    def key(self):
        return self.arr_types, self.has_runtime_cols

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(Table)
def typeof_table(val, c):
    return TableType(tuple(numba.typeof(dyg__tmtmm) for dyg__tmtmm in val.
        arrays))


@register_model(TableType)
class TableTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        if fe_type.has_runtime_cols:
            wygh__fitxw = [(f'block_{i}', types.List(cxszg__lvwuj)) for i,
                cxszg__lvwuj in enumerate(fe_type.arr_types)]
        else:
            wygh__fitxw = [(f'block_{ykhx__rhzy}', types.List(cxszg__lvwuj)
                ) for cxszg__lvwuj, ykhx__rhzy in fe_type.type_to_blk.items()]
        wygh__fitxw.append(('parent', types.pyobject))
        wygh__fitxw.append(('len', types.int64))
        super(TableTypeModel, self).__init__(dmm, fe_type, wygh__fitxw)


make_attribute_wrapper(TableType, 'block_0', 'block_0')
make_attribute_wrapper(TableType, 'len', '_len')


@unbox(TableType)
def unbox_table(typ, val, c):
    zcy__yinxe = c.pyapi.object_getattr_string(val, 'arrays')
    uxoco__prsmg = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    uxoco__prsmg.parent = cgutils.get_null_value(uxoco__prsmg.parent.type)
    wtxxk__ofz = c.pyapi.make_none()
    wur__gknd = c.context.get_constant(types.int64, 0)
    ssw__zblz = cgutils.alloca_once_value(c.builder, wur__gknd)
    for cxszg__lvwuj, ykhx__rhzy in typ.type_to_blk.items():
        csn__wje = c.context.get_constant(types.int64, len(typ.
            block_to_arr_ind[ykhx__rhzy]))
        zasd__iak, dsl__bnxtu = ListInstance.allocate_ex(c.context, c.
            builder, types.List(cxszg__lvwuj), csn__wje)
        dsl__bnxtu.size = csn__wje
        msiot__kix = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[ykhx__rhzy],
            dtype=np.int64))
        kusq__dgi = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, msiot__kix)
        with cgutils.for_range(c.builder, csn__wje) as loop:
            i = loop.index
            qkhj__mvgx = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), kusq__dgi, i)
            eui__omjrw = c.pyapi.long_from_longlong(qkhj__mvgx)
            zup__dey = c.pyapi.object_getitem(zcy__yinxe, eui__omjrw)
            kizm__edylx = c.builder.icmp_unsigned('==', zup__dey, wtxxk__ofz)
            with c.builder.if_else(kizm__edylx) as (then, orelse):
                with then:
                    qfbzu__ukla = c.context.get_constant_null(cxszg__lvwuj)
                    dsl__bnxtu.inititem(i, qfbzu__ukla, incref=False)
                with orelse:
                    hwss__imcq = c.pyapi.call_method(zup__dey, '__len__', ())
                    jvsq__hkj = c.pyapi.long_as_longlong(hwss__imcq)
                    c.builder.store(jvsq__hkj, ssw__zblz)
                    c.pyapi.decref(hwss__imcq)
                    dyg__tmtmm = c.pyapi.to_native_value(cxszg__lvwuj, zup__dey
                        ).value
                    dsl__bnxtu.inititem(i, dyg__tmtmm, incref=False)
            c.pyapi.decref(zup__dey)
            c.pyapi.decref(eui__omjrw)
        setattr(uxoco__prsmg, f'block_{ykhx__rhzy}', dsl__bnxtu.value)
    uxoco__prsmg.len = c.builder.load(ssw__zblz)
    c.pyapi.decref(zcy__yinxe)
    c.pyapi.decref(wtxxk__ofz)
    gnxhm__akpn = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(uxoco__prsmg._getvalue(), is_error=gnxhm__akpn)


@box(TableType)
def box_table(typ, val, c, ensure_unboxed=None):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    uxoco__prsmg = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ.has_runtime_cols:
        ixa__jua = c.context.get_constant(types.int64, 0)
        for i, cxszg__lvwuj in enumerate(typ.arr_types):
            kzoj__nrjs = getattr(uxoco__prsmg, f'block_{i}')
            jwq__dudl = ListInstance(c.context, c.builder, types.List(
                cxszg__lvwuj), kzoj__nrjs)
            ixa__jua = c.builder.add(ixa__jua, jwq__dudl.size)
        ntk__lzw = c.pyapi.list_new(ixa__jua)
        ktbap__ptg = c.context.get_constant(types.int64, 0)
        for i, cxszg__lvwuj in enumerate(typ.arr_types):
            kzoj__nrjs = getattr(uxoco__prsmg, f'block_{i}')
            jwq__dudl = ListInstance(c.context, c.builder, types.List(
                cxszg__lvwuj), kzoj__nrjs)
            with cgutils.for_range(c.builder, jwq__dudl.size) as loop:
                i = loop.index
                dyg__tmtmm = jwq__dudl.getitem(i)
                c.context.nrt.incref(c.builder, cxszg__lvwuj, dyg__tmtmm)
                idx = c.builder.add(ktbap__ptg, i)
                c.pyapi.list_setitem(ntk__lzw, idx, c.pyapi.
                    from_native_value(cxszg__lvwuj, dyg__tmtmm, c.env_manager))
            ktbap__ptg = c.builder.add(ktbap__ptg, jwq__dudl.size)
        wjty__qap = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
        ubuo__stef = c.pyapi.call_function_objargs(wjty__qap, (ntk__lzw,))
        c.pyapi.decref(wjty__qap)
        c.pyapi.decref(ntk__lzw)
        c.context.nrt.decref(c.builder, typ, val)
        return ubuo__stef
    ntk__lzw = c.pyapi.list_new(c.context.get_constant(types.int64, len(typ
        .arr_types)))
    lhdeo__ylg = cgutils.is_not_null(c.builder, uxoco__prsmg.parent)
    if ensure_unboxed is None:
        ensure_unboxed = c.context.get_constant(types.bool_, False)
    for cxszg__lvwuj, ykhx__rhzy in typ.type_to_blk.items():
        kzoj__nrjs = getattr(uxoco__prsmg, f'block_{ykhx__rhzy}')
        jwq__dudl = ListInstance(c.context, c.builder, types.List(
            cxszg__lvwuj), kzoj__nrjs)
        msiot__kix = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[ykhx__rhzy],
            dtype=np.int64))
        kusq__dgi = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, msiot__kix)
        with cgutils.for_range(c.builder, jwq__dudl.size) as loop:
            i = loop.index
            qkhj__mvgx = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), kusq__dgi, i)
            dyg__tmtmm = jwq__dudl.getitem(i)
            jyck__gzgo = cgutils.alloca_once_value(c.builder, dyg__tmtmm)
            bmuit__gicpc = cgutils.alloca_once_value(c.builder, c.context.
                get_constant_null(cxszg__lvwuj))
            stdh__swkel = is_ll_eq(c.builder, jyck__gzgo, bmuit__gicpc)
            with c.builder.if_else(c.builder.and_(stdh__swkel, c.builder.
                not_(ensure_unboxed))) as (then, orelse):
                with then:
                    wtxxk__ofz = c.pyapi.make_none()
                    c.pyapi.list_setitem(ntk__lzw, qkhj__mvgx, wtxxk__ofz)
                with orelse:
                    zup__dey = cgutils.alloca_once(c.builder, c.context.
                        get_value_type(types.pyobject))
                    with c.builder.if_else(c.builder.and_(stdh__swkel,
                        lhdeo__ylg)) as (arr_then, arr_orelse):
                        with arr_then:
                            yuhde__hkze = get_df_obj_column_codegen(c.
                                context, c.builder, c.pyapi, uxoco__prsmg.
                                parent, qkhj__mvgx, cxszg__lvwuj)
                            c.builder.store(yuhde__hkze, zup__dey)
                        with arr_orelse:
                            c.context.nrt.incref(c.builder, cxszg__lvwuj,
                                dyg__tmtmm)
                            c.builder.store(c.pyapi.from_native_value(
                                cxszg__lvwuj, dyg__tmtmm, c.env_manager),
                                zup__dey)
                    c.pyapi.list_setitem(ntk__lzw, qkhj__mvgx, c.builder.
                        load(zup__dey))
    wjty__qap = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
    ubuo__stef = c.pyapi.call_function_objargs(wjty__qap, (ntk__lzw,))
    c.pyapi.decref(wjty__qap)
    c.pyapi.decref(ntk__lzw)
    c.context.nrt.decref(c.builder, typ, val)
    return ubuo__stef


@overload(len)
def table_len_overload(T):
    if not isinstance(T, TableType):
        return

    def impl(T):
        return T._len
    return impl


@overload_attribute(TableType, 'shape')
def table_shape_overload(T):
    if T.has_runtime_cols:

        def impl(T):
            return T._len, compute_num_runtime_columns(T)
        return impl
    ncols = len(T.arr_types)
    return lambda T: (T._len, types.int64(ncols))


@intrinsic
def compute_num_runtime_columns(typingctx, table_type):
    assert isinstance(table_type, TableType)

    def codegen(context, builder, sig, args):
        table_arg, = args
        uxoco__prsmg = cgutils.create_struct_proxy(table_type)(context,
            builder, table_arg)
        hgnwj__nip = context.get_constant(types.int64, 0)
        for i, cxszg__lvwuj in enumerate(table_type.arr_types):
            kzoj__nrjs = getattr(uxoco__prsmg, f'block_{i}')
            jwq__dudl = ListInstance(context, builder, types.List(
                cxszg__lvwuj), kzoj__nrjs)
            hgnwj__nip = builder.add(hgnwj__nip, jwq__dudl.size)
        return hgnwj__nip
    sig = types.int64(table_type)
    return sig, codegen


def get_table_data_codegen(context, builder, table_arg, col_ind, table_type):
    arr_type = table_type.arr_types[col_ind]
    uxoco__prsmg = cgutils.create_struct_proxy(table_type)(context, builder,
        table_arg)
    ykhx__rhzy = table_type.block_nums[col_ind]
    ibq__sft = table_type.block_offsets[col_ind]
    kzoj__nrjs = getattr(uxoco__prsmg, f'block_{ykhx__rhzy}')
    jwq__dudl = ListInstance(context, builder, types.List(arr_type), kzoj__nrjs
        )
    dyg__tmtmm = jwq__dudl.getitem(ibq__sft)
    return dyg__tmtmm


@intrinsic
def get_table_data(typingctx, table_type, ind_typ=None):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, zasd__iak = args
        dyg__tmtmm = get_table_data_codegen(context, builder, table_arg,
            col_ind, table_type)
        return impl_ret_borrowed(context, builder, arr_type, dyg__tmtmm)
    sig = arr_type(table_type, ind_typ)
    return sig, codegen


@intrinsic
def del_column(typingctx, table_type, ind_typ=None):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, zasd__iak = args
        uxoco__prsmg = cgutils.create_struct_proxy(table_type)(context,
            builder, table_arg)
        ykhx__rhzy = table_type.block_nums[col_ind]
        ibq__sft = table_type.block_offsets[col_ind]
        kzoj__nrjs = getattr(uxoco__prsmg, f'block_{ykhx__rhzy}')
        jwq__dudl = ListInstance(context, builder, types.List(arr_type),
            kzoj__nrjs)
        dyg__tmtmm = jwq__dudl.getitem(ibq__sft)
        context.nrt.decref(builder, arr_type, dyg__tmtmm)
        qfbzu__ukla = context.get_constant_null(arr_type)
        jwq__dudl.inititem(ibq__sft, qfbzu__ukla, incref=False)
    sig = types.void(table_type, ind_typ)
    return sig, codegen


def set_table_data_codegen(context, builder, in_table_type, in_table,
    out_table_type, arr_type, arr_arg, col_ind, is_new_col):
    in_table = cgutils.create_struct_proxy(in_table_type)(context, builder,
        in_table)
    out_table = cgutils.create_struct_proxy(out_table_type)(context, builder)
    out_table.len = in_table.len
    out_table.parent = in_table.parent
    wur__gknd = context.get_constant(types.int64, 0)
    qmov__fwzdi = context.get_constant(types.int64, 1)
    rtz__gqher = arr_type not in in_table_type.type_to_blk
    for cxszg__lvwuj, ykhx__rhzy in out_table_type.type_to_blk.items():
        if cxszg__lvwuj in in_table_type.type_to_blk:
            pdl__snzz = in_table_type.type_to_blk[cxszg__lvwuj]
            dsl__bnxtu = ListInstance(context, builder, types.List(
                cxszg__lvwuj), getattr(in_table, f'block_{pdl__snzz}'))
            context.nrt.incref(builder, types.List(cxszg__lvwuj),
                dsl__bnxtu.value)
            setattr(out_table, f'block_{ykhx__rhzy}', dsl__bnxtu.value)
    if rtz__gqher:
        zasd__iak, dsl__bnxtu = ListInstance.allocate_ex(context, builder,
            types.List(arr_type), qmov__fwzdi)
        dsl__bnxtu.size = qmov__fwzdi
        dsl__bnxtu.inititem(wur__gknd, arr_arg, incref=True)
        ykhx__rhzy = out_table_type.type_to_blk[arr_type]
        setattr(out_table, f'block_{ykhx__rhzy}', dsl__bnxtu.value)
        if not is_new_col:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
    else:
        ykhx__rhzy = out_table_type.type_to_blk[arr_type]
        dsl__bnxtu = ListInstance(context, builder, types.List(arr_type),
            getattr(out_table, f'block_{ykhx__rhzy}'))
        if is_new_col:
            n = dsl__bnxtu.size
            axlm__gzqu = builder.add(n, qmov__fwzdi)
            dsl__bnxtu.resize(axlm__gzqu)
            dsl__bnxtu.inititem(n, arr_arg, incref=True)
        elif arr_type == in_table_type.arr_types[col_ind]:
            fbdtq__iveh = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            dsl__bnxtu.setitem(fbdtq__iveh, arr_arg, True)
        else:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
            fbdtq__iveh = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            n = dsl__bnxtu.size
            axlm__gzqu = builder.add(n, qmov__fwzdi)
            dsl__bnxtu.resize(axlm__gzqu)
            context.nrt.incref(builder, arr_type, dsl__bnxtu.getitem(
                fbdtq__iveh))
            dsl__bnxtu.move(builder.add(fbdtq__iveh, qmov__fwzdi),
                fbdtq__iveh, builder.sub(n, fbdtq__iveh))
            dsl__bnxtu.setitem(fbdtq__iveh, arr_arg, incref=True)
    return out_table._getvalue()


def _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
    context, builder):
    pcuez__ykqy = in_table_type.arr_types[col_ind]
    if pcuez__ykqy in out_table_type.type_to_blk:
        ykhx__rhzy = out_table_type.type_to_blk[pcuez__ykqy]
        snx__wwa = getattr(out_table, f'block_{ykhx__rhzy}')
        eganz__vrpqd = types.List(pcuez__ykqy)
        fbdtq__iveh = context.get_constant(types.int64, in_table_type.
            block_offsets[col_ind])
        ojqer__qubx = eganz__vrpqd.dtype(eganz__vrpqd, types.intp)
        kczrz__flz = context.compile_internal(builder, lambda lst, i: lst.
            pop(i), ojqer__qubx, (snx__wwa, fbdtq__iveh))
        context.nrt.decref(builder, pcuez__ykqy, kczrz__flz)


@intrinsic
def set_table_data(typingctx, table_type, ind_type, arr_type=None):
    assert isinstance(table_type, TableType), 'invalid input to set_table_data'
    assert is_overload_constant_int(ind_type
        ), 'set_table_data expects const index'
    col_ind = get_overload_const_int(ind_type)
    is_new_col = col_ind == len(table_type.arr_types)
    iftf__gsy = list(table_type.arr_types)
    if is_new_col:
        iftf__gsy.append(arr_type)
    else:
        iftf__gsy[col_ind] = arr_type
    out_table_type = TableType(tuple(iftf__gsy))

    def codegen(context, builder, sig, args):
        table_arg, zasd__iak, gnhie__dcr = args
        out_table = set_table_data_codegen(context, builder, table_type,
            table_arg, out_table_type, arr_type, gnhie__dcr, col_ind,
            is_new_col)
        return out_table
    return out_table_type(table_type, ind_type, arr_type), codegen


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_table_data',
    'bodo.hiframes.table'] = alias_ext_dummy_func


def get_table_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    sxktb__uio = args[0]
    if equiv_set.has_shape(sxktb__uio):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            sxktb__uio)[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_get_table_data = (
    get_table_data_equiv)


@lower_constant(TableType)
def lower_constant_table(context, builder, table_type, pyval):
    uxoco__prsmg = cgutils.create_struct_proxy(table_type)(context, builder)
    uxoco__prsmg.parent = cgutils.get_null_value(uxoco__prsmg.parent.type)
    for cxszg__lvwuj, ykhx__rhzy in table_type.type_to_blk.items():
        aha__gkqk = len(table_type.block_to_arr_ind[ykhx__rhzy])
        csn__wje = context.get_constant(types.int64, aha__gkqk)
        zasd__iak, dsl__bnxtu = ListInstance.allocate_ex(context, builder,
            types.List(cxszg__lvwuj), csn__wje)
        dsl__bnxtu.size = csn__wje
        for i in range(aha__gkqk):
            qkhj__mvgx = table_type.block_to_arr_ind[ykhx__rhzy][i]
            dyg__tmtmm = context.get_constant_generic(builder, table_type.
                arr_types[qkhj__mvgx], pyval.arrays[qkhj__mvgx])
            hjpac__ookml = context.get_constant(types.int64, i)
            dsl__bnxtu.inititem(hjpac__ookml, dyg__tmtmm, incref=False)
        setattr(uxoco__prsmg, f'block_{ykhx__rhzy}', dsl__bnxtu.value)
    return uxoco__prsmg._getvalue()


@intrinsic
def init_table(typingctx, table_type=None):
    assert isinstance(table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        uxoco__prsmg = cgutils.create_struct_proxy(table_type)(context, builder
            )
        for cxszg__lvwuj, ykhx__rhzy in table_type.type_to_blk.items():
            zwu__jcej = context.get_constant_null(types.List(cxszg__lvwuj))
            setattr(uxoco__prsmg, f'block_{ykhx__rhzy}', zwu__jcej)
        return uxoco__prsmg._getvalue()
    sig = table_type(table_type)
    return sig, codegen


@intrinsic
def get_table_block(typingctx, table_type, blk_type=None):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_int(blk_type)
    ykhx__rhzy = get_overload_const_int(blk_type)
    arr_type = None
    for cxszg__lvwuj, wxin__hiv in table_type.type_to_blk.items():
        if wxin__hiv == ykhx__rhzy:
            arr_type = cxszg__lvwuj
            break
    assert arr_type is not None, 'invalid table type block'
    epir__yvwzr = types.List(arr_type)

    def codegen(context, builder, sig, args):
        uxoco__prsmg = cgutils.create_struct_proxy(table_type)(context,
            builder, args[0])
        kzoj__nrjs = getattr(uxoco__prsmg, f'block_{ykhx__rhzy}')
        return impl_ret_borrowed(context, builder, epir__yvwzr, kzoj__nrjs)
    sig = epir__yvwzr(table_type, blk_type)
    return sig, codegen


@intrinsic
def ensure_column_unboxed(typingctx, table_type, arr_list_t, ind_t,
    arr_ind_t=None):
    assert isinstance(table_type, TableType), 'table type expected'
    sig = types.none(table_type, arr_list_t, ind_t, arr_ind_t)
    return sig, ensure_column_unboxed_codegen


def ensure_column_unboxed_codegen(context, builder, sig, args):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    table_arg, zod__qyhgx, tzd__pkoye, esdq__ycsus = args
    apub__suei = context.get_python_api(builder)
    uxoco__prsmg = cgutils.create_struct_proxy(sig.args[0])(context,
        builder, table_arg)
    lhdeo__ylg = cgutils.is_not_null(builder, uxoco__prsmg.parent)
    jwq__dudl = ListInstance(context, builder, sig.args[1], zod__qyhgx)
    xrohw__vned = jwq__dudl.getitem(tzd__pkoye)
    jyck__gzgo = cgutils.alloca_once_value(builder, xrohw__vned)
    bmuit__gicpc = cgutils.alloca_once_value(builder, context.
        get_constant_null(sig.args[1].dtype))
    stdh__swkel = is_ll_eq(builder, jyck__gzgo, bmuit__gicpc)
    with builder.if_then(stdh__swkel):
        with builder.if_else(lhdeo__ylg) as (then, orelse):
            with then:
                zup__dey = get_df_obj_column_codegen(context, builder,
                    apub__suei, uxoco__prsmg.parent, esdq__ycsus, sig.args[
                    1].dtype)
                dyg__tmtmm = apub__suei.to_native_value(sig.args[1].dtype,
                    zup__dey).value
                jwq__dudl.inititem(tzd__pkoye, dyg__tmtmm, incref=False)
                apub__suei.decref(zup__dey)
            with orelse:
                context.call_conv.return_user_exc(builder, BodoError, (
                    'unexpected null table column',))


@intrinsic
def set_table_block(typingctx, table_type, arr_list_type, blk_type=None):
    assert isinstance(table_type, TableType), 'table type expected'
    assert isinstance(arr_list_type, types.List), 'list type expected'
    assert is_overload_constant_int(blk_type), 'blk should be const int'
    ykhx__rhzy = get_overload_const_int(blk_type)

    def codegen(context, builder, sig, args):
        table_arg, lhxk__hguk, zasd__iak = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        setattr(in_table, f'block_{ykhx__rhzy}', lhxk__hguk)
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, arr_list_type, blk_type)
    return sig, codegen


@intrinsic
def set_table_len(typingctx, table_type, l_type=None):
    assert isinstance(table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        table_arg, vyfv__kpmxy = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        in_table.len = vyfv__kpmxy
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, l_type)
    return sig, codegen


@intrinsic
def alloc_list_like(typingctx, list_type=None):
    assert isinstance(list_type, types.List), 'list type expected'

    def codegen(context, builder, sig, args):
        bykog__bpxy = ListInstance(context, builder, list_type, args[0])
        tyugh__zxzts = bykog__bpxy.size
        zasd__iak, dsl__bnxtu = ListInstance.allocate_ex(context, builder,
            list_type, tyugh__zxzts)
        dsl__bnxtu.size = tyugh__zxzts
        return dsl__bnxtu.value
    sig = list_type(list_type)
    return sig, codegen


def _get_idx_length(idx):
    pass


@overload(_get_idx_length)
def overload_get_idx_length(idx, n):
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        return lambda idx, n: idx.sum()
    assert isinstance(idx, types.SliceType), 'slice index expected'

    def impl(idx, n):
        suig__bmvjt = numba.cpython.unicode._normalize_slice(idx, n)
        return numba.cpython.unicode._slice_span(suig__bmvjt)
    return impl


def gen_table_filter(T, used_cols=None):
    from bodo.utils.conversion import ensure_contig_if_np
    hncb__nmeev = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, '_get_idx_length':
        _get_idx_length, 'ensure_contig_if_np': ensure_contig_if_np}
    if used_cols is not None:
        hncb__nmeev['used_cols'] = np.array(used_cols, dtype=np.int64)
    jxg__shbv = 'def impl(T, idx):\n'
    jxg__shbv += f'  T2 = init_table(T)\n'
    jxg__shbv += f'  l = 0\n'
    if used_cols is not None and len(used_cols) == 0:
        jxg__shbv += f'  l = _get_idx_length(idx, len(T))\n'
        jxg__shbv += f'  T2 = set_table_len(T2, l)\n'
        jxg__shbv += f'  return T2\n'
        cka__rteq = {}
        exec(jxg__shbv, hncb__nmeev, cka__rteq)
        return cka__rteq['impl']
    if used_cols is not None:
        jxg__shbv += f'  used_set = set(used_cols)\n'
    for ykhx__rhzy in T.type_to_blk.values():
        hncb__nmeev[f'arr_inds_{ykhx__rhzy}'] = np.array(T.block_to_arr_ind
            [ykhx__rhzy], dtype=np.int64)
        jxg__shbv += (
            f'  arr_list_{ykhx__rhzy} = get_table_block(T, {ykhx__rhzy})\n')
        jxg__shbv += (
            f'  out_arr_list_{ykhx__rhzy} = alloc_list_like(arr_list_{ykhx__rhzy})\n'
            )
        jxg__shbv += f'  for i in range(len(arr_list_{ykhx__rhzy})):\n'
        jxg__shbv += f'    arr_ind_{ykhx__rhzy} = arr_inds_{ykhx__rhzy}[i]\n'
        if used_cols is not None:
            jxg__shbv += (
                f'    if arr_ind_{ykhx__rhzy} not in used_set: continue\n')
        jxg__shbv += f"""    ensure_column_unboxed(T, arr_list_{ykhx__rhzy}, i, arr_ind_{ykhx__rhzy})
"""
        jxg__shbv += f"""    out_arr_{ykhx__rhzy} = ensure_contig_if_np(arr_list_{ykhx__rhzy}[i][idx])
"""
        jxg__shbv += f'    l = len(out_arr_{ykhx__rhzy})\n'
        jxg__shbv += (
            f'    out_arr_list_{ykhx__rhzy}[i] = out_arr_{ykhx__rhzy}\n')
        jxg__shbv += (
            f'  T2 = set_table_block(T2, out_arr_list_{ykhx__rhzy}, {ykhx__rhzy})\n'
            )
    jxg__shbv += f'  T2 = set_table_len(T2, l)\n'
    jxg__shbv += f'  return T2\n'
    cka__rteq = {}
    exec(jxg__shbv, hncb__nmeev, cka__rteq)
    return cka__rteq['impl']


@overload(operator.getitem, no_unliteral=True)
def table_getitem(T, idx):
    if not isinstance(T, TableType):
        return
    return gen_table_filter(T)


@intrinsic
def init_runtime_table_from_lists(typingctx, arr_list_tup_typ, nrows_typ=None):
    assert isinstance(arr_list_tup_typ, types.BaseTuple
        ), 'init_runtime_table_from_lists requires a tuple of list of arrays'
    if isinstance(arr_list_tup_typ, types.UniTuple):
        if arr_list_tup_typ.dtype.dtype == types.undefined:
            return
        rja__sicwa = [arr_list_tup_typ.dtype.dtype] * len(arr_list_tup_typ)
    else:
        rja__sicwa = []
        for typ in arr_list_tup_typ:
            if typ.dtype == types.undefined:
                return
            rja__sicwa.append(typ.dtype)
    assert isinstance(nrows_typ, types.Integer
        ), 'init_runtime_table_from_lists requires an integer length'

    def codegen(context, builder, sig, args):
        wwhjr__jmx, juthg__sdcv = args
        uxoco__prsmg = cgutils.create_struct_proxy(table_type)(context, builder
            )
        uxoco__prsmg.len = juthg__sdcv
        svixi__zjmap = cgutils.unpack_tuple(builder, wwhjr__jmx)
        for i, kzoj__nrjs in enumerate(svixi__zjmap):
            setattr(uxoco__prsmg, f'block_{i}', kzoj__nrjs)
            context.nrt.incref(builder, types.List(rja__sicwa[i]), kzoj__nrjs)
        return uxoco__prsmg._getvalue()
    table_type = TableType(tuple(rja__sicwa), True)
    sig = table_type(arr_list_tup_typ, nrows_typ)
    return sig, codegen
