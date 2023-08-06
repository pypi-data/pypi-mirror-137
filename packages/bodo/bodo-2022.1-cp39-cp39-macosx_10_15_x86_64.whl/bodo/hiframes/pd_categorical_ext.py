import enum
import operator
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.utils.typing import NOT_CONSTANT, BodoError, MetaType, check_unsupported_args, dtype_to_array_type, get_literal_value, get_overload_const, get_overload_const_bool, is_common_scalar_dtype, is_iterable_type, is_list_like_index_type, is_literal_type, is_overload_constant_bool, is_overload_none, is_overload_true, is_scalar_type, raise_bodo_error


class PDCategoricalDtype(types.Opaque):

    def __init__(self, categories, elem_type, ordered, data=None, int_type=None
        ):
        self.categories = categories
        self.elem_type = elem_type
        self.ordered = ordered
        self.data = _get_cat_index_type(elem_type) if data is None else data
        self.int_type = int_type
        mhc__ddy = (
            f'PDCategoricalDtype({self.categories}, {self.elem_type}, {self.ordered}, {self.data}, {self.int_type})'
            )
        super(PDCategoricalDtype, self).__init__(name=mhc__ddy)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.CategoricalDtype)
def _typeof_pd_cat_dtype(val, c):
    oomn__tykam = tuple(val.categories.values)
    elem_type = None if len(oomn__tykam) == 0 else bodo.typeof(val.
        categories.values).dtype
    int_type = getattr(val, '_int_type', None)
    return PDCategoricalDtype(oomn__tykam, elem_type, val.ordered, bodo.
        typeof(val.categories), int_type)


def _get_cat_index_type(elem_type):
    elem_type = bodo.string_type if elem_type is None else elem_type
    return bodo.utils.typing.get_index_type_from_dtype(elem_type)


@lower_constant(PDCategoricalDtype)
def lower_constant_categorical_type(context, builder, typ, pyval):
    categories = context.get_constant_generic(builder, bodo.typeof(pyval.
        categories), pyval.categories)
    ordered = context.get_constant(types.bool_, pyval.ordered)
    return lir.Constant.literal_struct([categories, ordered])


@register_model(PDCategoricalDtype)
class PDCategoricalDtypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        gcfli__xgh = [('categories', fe_type.data), ('ordered', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, gcfli__xgh)


make_attribute_wrapper(PDCategoricalDtype, 'categories', 'categories')
make_attribute_wrapper(PDCategoricalDtype, 'ordered', 'ordered')


@intrinsic
def init_cat_dtype(typingctx, categories_typ, ordered_typ, int_type,
    cat_vals_typ=None):
    assert bodo.hiframes.pd_index_ext.is_index_type(categories_typ
        ), 'init_cat_dtype requires index type for categories'
    assert is_overload_constant_bool(ordered_typ
        ), 'init_cat_dtype requires constant ordered flag'
    pne__ftkku = None if is_overload_none(int_type) else int_type.dtype
    assert is_overload_none(cat_vals_typ) or isinstance(cat_vals_typ, types
        .TypeRef), 'init_cat_dtype requires constant category values'
    zkeog__idfsy = None if is_overload_none(cat_vals_typ
        ) else cat_vals_typ.instance_type.meta

    def codegen(context, builder, sig, args):
        categories, ordered, meucs__ocf, meucs__ocf = args
        cat_dtype = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        cat_dtype.categories = categories
        context.nrt.incref(builder, sig.args[0], categories)
        context.nrt.incref(builder, sig.args[1], ordered)
        cat_dtype.ordered = ordered
        return cat_dtype._getvalue()
    qvo__hxyz = PDCategoricalDtype(zkeog__idfsy, categories_typ.dtype,
        is_overload_true(ordered_typ), categories_typ, pne__ftkku)
    return qvo__hxyz(categories_typ, ordered_typ, int_type, cat_vals_typ
        ), codegen


@unbox(PDCategoricalDtype)
def unbox_cat_dtype(typ, obj, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    hhs__ecy = c.pyapi.object_getattr_string(obj, 'ordered')
    cat_dtype.ordered = c.pyapi.to_native_value(types.bool_, hhs__ecy).value
    c.pyapi.decref(hhs__ecy)
    pqlin__ebxw = c.pyapi.object_getattr_string(obj, 'categories')
    cat_dtype.categories = c.pyapi.to_native_value(typ.data, pqlin__ebxw).value
    c.pyapi.decref(pqlin__ebxw)
    hhkuz__nhcw = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cat_dtype._getvalue(), is_error=hhkuz__nhcw)


@box(PDCategoricalDtype)
def box_cat_dtype(typ, val, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    hhs__ecy = c.pyapi.from_native_value(types.bool_, cat_dtype.ordered, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.data, cat_dtype.categories)
    rbr__srnux = c.pyapi.from_native_value(typ.data, cat_dtype.categories,
        c.env_manager)
    dbv__txvya = c.context.insert_const_string(c.builder.module, 'pandas')
    gng__fhbm = c.pyapi.import_module_noblock(dbv__txvya)
    zvni__isir = c.pyapi.call_method(gng__fhbm, 'CategoricalDtype', (
        rbr__srnux, hhs__ecy))
    c.pyapi.decref(hhs__ecy)
    c.pyapi.decref(rbr__srnux)
    c.pyapi.decref(gng__fhbm)
    c.context.nrt.decref(c.builder, typ, val)
    return zvni__isir


@overload_attribute(PDCategoricalDtype, 'nbytes')
def pd_categorical_nbytes_overload(A):
    return lambda A: A.categories.nbytes + bodo.io.np_io.get_dtype_size(types
        .bool_)


class CategoricalArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        self.dtype = dtype
        super(CategoricalArrayType, self).__init__(name=
            'CategoricalArrayType({})'.format(dtype))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return CategoricalArrayType(self.dtype)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.Categorical)
def _typeof_pd_cat(val, c):
    return CategoricalArrayType(bodo.typeof(val.dtype))


@register_model(CategoricalArrayType)
class CategoricalArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        rixkk__tkosw = get_categories_int_type(fe_type.dtype)
        gcfli__xgh = [('dtype', fe_type.dtype), ('codes', types.Array(
            rixkk__tkosw, 1, 'C'))]
        super(CategoricalArrayModel, self).__init__(dmm, fe_type, gcfli__xgh)


make_attribute_wrapper(CategoricalArrayType, 'codes', 'codes')
make_attribute_wrapper(CategoricalArrayType, 'dtype', 'dtype')


@unbox(CategoricalArrayType)
def unbox_categorical_array(typ, val, c):
    tjwnr__zgu = c.pyapi.object_getattr_string(val, 'codes')
    dtype = get_categories_int_type(typ.dtype)
    codes = c.pyapi.to_native_value(types.Array(dtype, 1, 'C'), tjwnr__zgu
        ).value
    c.pyapi.decref(tjwnr__zgu)
    zvni__isir = c.pyapi.object_getattr_string(val, 'dtype')
    baju__qbc = c.pyapi.to_native_value(typ.dtype, zvni__isir).value
    c.pyapi.decref(zvni__isir)
    huf__hpdv = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    huf__hpdv.codes = codes
    huf__hpdv.dtype = baju__qbc
    return NativeValue(huf__hpdv._getvalue())


@lower_constant(CategoricalArrayType)
def lower_constant_categorical_array(context, builder, typ, pyval):
    zed__nvbo = get_categories_int_type(typ.dtype)
    qis__rff = context.get_constant_generic(builder, types.Array(zed__nvbo,
        1, 'C'), pyval.codes)
    cat_dtype = context.get_constant_generic(builder, typ.dtype, pyval.dtype)
    return lir.Constant.literal_struct([cat_dtype, qis__rff])


def get_categories_int_type(cat_dtype):
    dtype = types.int64
    if cat_dtype.int_type is not None:
        return cat_dtype.int_type
    if cat_dtype.categories is None:
        return types.int64
    amgg__buwy = len(cat_dtype.categories)
    if amgg__buwy < np.iinfo(np.int8).max:
        dtype = types.int8
    elif amgg__buwy < np.iinfo(np.int16).max:
        dtype = types.int16
    elif amgg__buwy < np.iinfo(np.int32).max:
        dtype = types.int32
    return dtype


@box(CategoricalArrayType)
def box_categorical_array(typ, val, c):
    dtype = typ.dtype
    dbv__txvya = c.context.insert_const_string(c.builder.module, 'pandas')
    gng__fhbm = c.pyapi.import_module_noblock(dbv__txvya)
    rixkk__tkosw = get_categories_int_type(dtype)
    owmqc__rozfi = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    dkie__lyxev = types.Array(rixkk__tkosw, 1, 'C')
    c.context.nrt.incref(c.builder, dkie__lyxev, owmqc__rozfi.codes)
    tjwnr__zgu = c.pyapi.from_native_value(dkie__lyxev, owmqc__rozfi.codes,
        c.env_manager)
    c.context.nrt.incref(c.builder, dtype, owmqc__rozfi.dtype)
    zvni__isir = c.pyapi.from_native_value(dtype, owmqc__rozfi.dtype, c.
        env_manager)
    mhuvh__hheh = c.pyapi.borrow_none()
    kqq__epcw = c.pyapi.object_getattr_string(gng__fhbm, 'Categorical')
    nkhj__ztuce = c.pyapi.call_method(kqq__epcw, 'from_codes', (tjwnr__zgu,
        mhuvh__hheh, mhuvh__hheh, zvni__isir))
    c.pyapi.decref(kqq__epcw)
    c.pyapi.decref(tjwnr__zgu)
    c.pyapi.decref(zvni__isir)
    c.pyapi.decref(gng__fhbm)
    c.context.nrt.decref(c.builder, typ, val)
    return nkhj__ztuce


def _to_readonly(t):
    from bodo.hiframes.pd_index_ext import DatetimeIndexType, NumericIndexType, TimedeltaIndexType
    if isinstance(t, types.Array):
        return types.Array(t.dtype, t.ndim, 'C', True)
    if isinstance(t, NumericIndexType):
        return NumericIndexType(t.dtype, t.name_typ, _to_readonly(t.data))
    if isinstance(t, (DatetimeIndexType, TimedeltaIndexType)):
        return t.__class__(t.name_typ, _to_readonly(t.data))
    return t


@lower_cast(CategoricalArrayType, CategoricalArrayType)
def cast_cat_arr(context, builder, fromty, toty, val):
    vtni__fwoz = toty.dtype
    tnx__srf = PDCategoricalDtype(vtni__fwoz.categories, vtni__fwoz.
        elem_type, vtni__fwoz.ordered, _to_readonly(vtni__fwoz.data),
        vtni__fwoz.int_type)
    if tnx__srf == fromty.dtype:
        return val
    raise BodoError(f'Cannot cast from {fromty} to {toty}')


def create_cmp_op_overload(op):

    def overload_cat_arr_cmp(A, other):
        if not isinstance(A, CategoricalArrayType):
            return
        if A.dtype.categories and is_literal_type(other) and types.unliteral(
            other) == A.dtype.elem_type:
            val = get_literal_value(other)
            xgddc__jzok = list(A.dtype.categories).index(val
                ) if val in A.dtype.categories else -2

            def impl_lit(A, other):
                djzr__youcs = op(bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(A), xgddc__jzok)
                return djzr__youcs
            return impl_lit

        def impl(A, other):
            xgddc__jzok = get_code_for_value(A.dtype, other)
            djzr__youcs = op(bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A), xgddc__jzok)
            return djzr__youcs
        return impl
    return overload_cat_arr_cmp


def _install_cmp_ops():
    for op in [operator.eq, operator.ne]:
        kfv__wkuob = create_cmp_op_overload(op)
        overload(op, inline='always', no_unliteral=True)(kfv__wkuob)


_install_cmp_ops()


@register_jitable
def get_code_for_value(cat_dtype, val):
    owmqc__rozfi = cat_dtype.categories
    n = len(owmqc__rozfi)
    for cafvc__ktw in range(n):
        if owmqc__rozfi[cafvc__ktw] == val:
            return cafvc__ktw
    return -2


@overload_method(CategoricalArrayType, 'astype', inline='always',
    no_unliteral=True)
def overload_cat_arr_astype(A, dtype, copy=True, _bodo_nan_to_str=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "CategoricalArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    achu__wqyl = bodo.utils.typing.parse_dtype(dtype, 'CategoricalArray.astype'
        )
    if achu__wqyl != A.dtype.elem_type and achu__wqyl != types.unicode_type:
        raise BodoError(
            f'Converting categorical array {A} to dtype {dtype} not supported yet'
            )
    if achu__wqyl == types.unicode_type:

        def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
            codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(
                A)
            categories = A.dtype.categories
            n = len(codes)
            djzr__youcs = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
            for cafvc__ktw in numba.parfors.parfor.internal_prange(n):
                dvq__jofvh = codes[cafvc__ktw]
                if dvq__jofvh == -1:
                    if _bodo_nan_to_str:
                        bodo.libs.str_arr_ext.str_arr_setitem_NA_str(
                            djzr__youcs, cafvc__ktw)
                    else:
                        bodo.libs.array_kernels.setna(djzr__youcs, cafvc__ktw)
                    continue
                djzr__youcs[cafvc__ktw] = str(bodo.utils.conversion.
                    unbox_if_timestamp(categories[dvq__jofvh]))
            return djzr__youcs
        return impl
    dkie__lyxev = dtype_to_array_type(achu__wqyl)

    def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
        codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(A)
        categories = A.dtype.categories
        n = len(codes)
        djzr__youcs = bodo.utils.utils.alloc_type(n, dkie__lyxev, (-1,))
        for cafvc__ktw in numba.parfors.parfor.internal_prange(n):
            dvq__jofvh = codes[cafvc__ktw]
            if dvq__jofvh == -1:
                bodo.libs.array_kernels.setna(djzr__youcs, cafvc__ktw)
                continue
            djzr__youcs[cafvc__ktw] = bodo.utils.conversion.unbox_if_timestamp(
                categories[dvq__jofvh])
        return djzr__youcs
    return impl


@overload(pd.api.types.CategoricalDtype, no_unliteral=True)
def cat_overload_dummy(val_list):
    return lambda val_list: 1


@intrinsic
def init_categorical_array(typingctx, codes, cat_dtype=None):
    assert isinstance(codes, types.Array) and isinstance(codes.dtype, types
        .Integer)

    def codegen(context, builder, signature, args):
        dil__buz, baju__qbc = args
        owmqc__rozfi = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        owmqc__rozfi.codes = dil__buz
        owmqc__rozfi.dtype = baju__qbc
        context.nrt.incref(builder, signature.args[0], dil__buz)
        context.nrt.incref(builder, signature.args[1], baju__qbc)
        return owmqc__rozfi._getvalue()
    beq__wemnl = CategoricalArrayType(cat_dtype)
    sig = beq__wemnl(codes, cat_dtype)
    return sig, codegen


def init_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    oyo__ejfnw = args[0]
    if equiv_set.has_shape(oyo__ejfnw):
        return ArrayAnalysis.AnalyzeResult(shape=oyo__ejfnw, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_init_categorical_array
    ) = init_categorical_array_equiv


def alloc_categorical_array(n, cat_dtype):
    pass


@overload(alloc_categorical_array, no_unliteral=True)
def _alloc_categorical_array(n, cat_dtype):
    rixkk__tkosw = get_categories_int_type(cat_dtype)

    def impl(n, cat_dtype):
        codes = np.empty(n, rixkk__tkosw)
        return init_categorical_array(codes, cat_dtype)
    return impl


def alloc_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_alloc_categorical_array
    ) = alloc_categorical_array_equiv


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_categorical_arr_codes(A):
    return lambda A: A.codes


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_categorical_array',
    'bodo.hiframes.pd_categorical_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_categorical_arr_codes',
    'bodo.hiframes.pd_categorical_ext'] = alias_ext_dummy_func


@overload_method(CategoricalArrayType, 'copy', no_unliteral=True)
def cat_arr_copy_overload(arr):
    return lambda arr: init_categorical_array(arr.codes.copy(), arr.dtype)


def build_replace_dicts(to_replace, value, categories):
    return dict(), np.empty(len(categories) + 1), 0


@overload(build_replace_dicts, no_unliteral=True)
def _build_replace_dicts(to_replace, value, categories):
    if isinstance(to_replace, types.Number) or to_replace == bodo.string_type:

        def impl(to_replace, value, categories):
            return build_replace_dicts([to_replace], value, categories)
        return impl
    else:

        def impl(to_replace, value, categories):
            n = len(categories)
            lmw__ezif = {}
            qis__rff = np.empty(n + 1, np.int64)
            fcil__jgdal = {}
            hss__ksd = []
            mevt__mld = {}
            for cafvc__ktw in range(n):
                mevt__mld[categories[cafvc__ktw]] = cafvc__ktw
            for khml__redgb in to_replace:
                if khml__redgb != value:
                    if khml__redgb in mevt__mld:
                        if value in mevt__mld:
                            lmw__ezif[khml__redgb] = khml__redgb
                            vxb__fzkyn = mevt__mld[khml__redgb]
                            fcil__jgdal[vxb__fzkyn] = mevt__mld[value]
                            hss__ksd.append(vxb__fzkyn)
                        else:
                            lmw__ezif[khml__redgb] = value
                            mevt__mld[value] = mevt__mld[khml__redgb]
            jwlzc__kbet = np.sort(np.array(hss__ksd))
            unkun__crtvi = 0
            jqlf__nnad = []
            for ody__wowz in range(-1, n):
                while unkun__crtvi < len(jwlzc__kbet
                    ) and ody__wowz > jwlzc__kbet[unkun__crtvi]:
                    unkun__crtvi += 1
                jqlf__nnad.append(unkun__crtvi)
            for jte__ttki in range(-1, n):
                ayowb__kqoqr = jte__ttki
                if jte__ttki in fcil__jgdal:
                    ayowb__kqoqr = fcil__jgdal[jte__ttki]
                qis__rff[jte__ttki + 1] = ayowb__kqoqr - jqlf__nnad[
                    ayowb__kqoqr + 1]
            return lmw__ezif, qis__rff, len(jwlzc__kbet)
        return impl


@numba.njit
def python_build_replace_dicts(to_replace, value, categories):
    return build_replace_dicts(to_replace, value, categories)


@register_jitable
def reassign_codes(new_codes_arr, old_codes_arr, codes_map_arr):
    for cafvc__ktw in range(len(new_codes_arr)):
        new_codes_arr[cafvc__ktw] = codes_map_arr[old_codes_arr[cafvc__ktw] + 1
            ]


@overload_method(CategoricalArrayType, 'replace', inline='always',
    no_unliteral=True)
def overload_replace(arr, to_replace, value):

    def impl(arr, to_replace, value):
        return bodo.hiframes.pd_categorical_ext.cat_replace(arr, to_replace,
            value)
    return impl


def cat_replace(arr, to_replace, value):
    return


@overload(cat_replace, no_unliteral=True)
def cat_replace_overload(arr, to_replace, value):
    cebh__lxrd = arr.dtype.ordered
    xfvbe__afa = arr.dtype.elem_type
    chokz__gpre = get_overload_const(to_replace)
    dmqbe__biss = get_overload_const(value)
    if (arr.dtype.categories is not None and chokz__gpre is not
        NOT_CONSTANT and dmqbe__biss is not NOT_CONSTANT):
        fwc__zgph, codes_map_arr, meucs__ocf = python_build_replace_dicts(
            chokz__gpre, dmqbe__biss, arr.dtype.categories)
        if len(fwc__zgph) == 0:
            return lambda arr, to_replace, value: arr.copy()
        urt__irhcj = []
        for jpga__aaiax in arr.dtype.categories:
            if jpga__aaiax in fwc__zgph:
                mjcep__rrrnb = fwc__zgph[jpga__aaiax]
                if mjcep__rrrnb != jpga__aaiax:
                    urt__irhcj.append(mjcep__rrrnb)
            else:
                urt__irhcj.append(jpga__aaiax)
        rkvqy__kia = pd.CategoricalDtype(urt__irhcj, cebh__lxrd
            ).categories.values
        uaps__wwqs = MetaType(tuple(rkvqy__kia))

        def impl_dtype(arr, to_replace, value):
            owfdb__klfm = init_cat_dtype(bodo.utils.conversion.
                index_from_array(rkvqy__kia), cebh__lxrd, None, uaps__wwqs)
            owmqc__rozfi = alloc_categorical_array(len(arr.codes), owfdb__klfm)
            reassign_codes(owmqc__rozfi.codes, arr.codes, codes_map_arr)
            return owmqc__rozfi
        return impl_dtype
    xfvbe__afa = arr.dtype.elem_type
    if xfvbe__afa == types.unicode_type:

        def impl_str(arr, to_replace, value):
            categories = arr.dtype.categories
            lmw__ezif, codes_map_arr, yawsj__ferfb = build_replace_dicts(
                to_replace, value, categories.values)
            if len(lmw__ezif) == 0:
                return init_categorical_array(arr.codes.copy().astype(np.
                    int64), init_cat_dtype(categories.copy(), cebh__lxrd,
                    None, None))
            n = len(categories)
            rkvqy__kia = bodo.libs.str_arr_ext.pre_alloc_string_array(n -
                yawsj__ferfb, -1)
            hej__ayquu = 0
            for ody__wowz in range(n):
                jmpj__uda = categories[ody__wowz]
                if jmpj__uda in lmw__ezif:
                    pmzt__knp = lmw__ezif[jmpj__uda]
                    if pmzt__knp != jmpj__uda:
                        rkvqy__kia[hej__ayquu] = pmzt__knp
                        hej__ayquu += 1
                else:
                    rkvqy__kia[hej__ayquu] = jmpj__uda
                    hej__ayquu += 1
            owmqc__rozfi = alloc_categorical_array(len(arr.codes),
                init_cat_dtype(bodo.utils.conversion.index_from_array(
                rkvqy__kia), cebh__lxrd, None, None))
            reassign_codes(owmqc__rozfi.codes, arr.codes, codes_map_arr)
            return owmqc__rozfi
        return impl_str
    lfms__nrzpo = dtype_to_array_type(xfvbe__afa)

    def impl(arr, to_replace, value):
        categories = arr.dtype.categories
        lmw__ezif, codes_map_arr, yawsj__ferfb = build_replace_dicts(to_replace
            , value, categories.values)
        if len(lmw__ezif) == 0:
            return init_categorical_array(arr.codes.copy().astype(np.int64),
                init_cat_dtype(categories.copy(), cebh__lxrd, None, None))
        n = len(categories)
        rkvqy__kia = bodo.utils.utils.alloc_type(n - yawsj__ferfb,
            lfms__nrzpo, None)
        hej__ayquu = 0
        for cafvc__ktw in range(n):
            jmpj__uda = categories[cafvc__ktw]
            if jmpj__uda in lmw__ezif:
                pmzt__knp = lmw__ezif[jmpj__uda]
                if pmzt__knp != jmpj__uda:
                    rkvqy__kia[hej__ayquu] = pmzt__knp
                    hej__ayquu += 1
            else:
                rkvqy__kia[hej__ayquu] = jmpj__uda
                hej__ayquu += 1
        owmqc__rozfi = alloc_categorical_array(len(arr.codes),
            init_cat_dtype(bodo.utils.conversion.index_from_array(
            rkvqy__kia), cebh__lxrd, None, None))
        reassign_codes(owmqc__rozfi.codes, arr.codes, codes_map_arr)
        return owmqc__rozfi
    return impl


@overload(len, no_unliteral=True)
def overload_cat_arr_len(A):
    if isinstance(A, CategoricalArrayType):
        return lambda A: len(A.codes)


@overload_attribute(CategoricalArrayType, 'shape')
def overload_cat_arr_shape(A):
    return lambda A: (len(A.codes),)


@overload_attribute(CategoricalArrayType, 'ndim')
def overload_cat_arr_ndim(A):
    return lambda A: 1


@overload_attribute(CategoricalArrayType, 'nbytes')
def cat_arr_nbytes_overload(A):
    return lambda A: A.codes.nbytes + A.dtype.nbytes


@register_jitable
def get_label_dict_from_categories(vals):
    kdol__zmxjm = dict()
    eys__fmsn = 0
    for cafvc__ktw in range(len(vals)):
        val = vals[cafvc__ktw]
        if val in kdol__zmxjm:
            continue
        kdol__zmxjm[val] = eys__fmsn
        eys__fmsn += 1
    return kdol__zmxjm


@register_jitable
def get_label_dict_from_categories_no_duplicates(vals):
    kdol__zmxjm = dict()
    for cafvc__ktw in range(len(vals)):
        val = vals[cafvc__ktw]
        kdol__zmxjm[val] = cafvc__ktw
    return kdol__zmxjm


@overload(pd.Categorical, no_unliteral=True)
def pd_categorical_overload(values, categories=None, ordered=None, dtype=
    None, fastpath=False):
    sks__toxk = dict(fastpath=fastpath)
    yimxe__zxc = dict(fastpath=False)
    check_unsupported_args('pd.Categorical', sks__toxk, yimxe__zxc)
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):

        def impl_dtype(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, dtype)
        return impl_dtype
    if not is_overload_none(categories):
        gusg__truj = get_overload_const(categories)
        if gusg__truj is not NOT_CONSTANT and get_overload_const(ordered
            ) is not NOT_CONSTANT:
            if is_overload_none(ordered):
                csdi__ujcr = False
            else:
                csdi__ujcr = get_overload_const_bool(ordered)
            ntqgu__zmz = pd.CategoricalDtype(gusg__truj, csdi__ujcr
                ).categories.values
            zjnfl__filgt = MetaType(tuple(ntqgu__zmz))

            def impl_cats_const(values, categories=None, ordered=None,
                dtype=None, fastpath=False):
                data = bodo.utils.conversion.coerce_to_array(values)
                owfdb__klfm = init_cat_dtype(bodo.utils.conversion.
                    index_from_array(ntqgu__zmz), csdi__ujcr, None,
                    zjnfl__filgt)
                return bodo.utils.conversion.fix_arr_dtype(data, owfdb__klfm)
            return impl_cats_const

        def impl_cats(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            ordered = bodo.utils.conversion.false_if_none(ordered)
            data = bodo.utils.conversion.coerce_to_array(values)
            oomn__tykam = bodo.utils.conversion.convert_to_index(categories)
            cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(
                oomn__tykam, ordered, None, None)
            return bodo.utils.conversion.fix_arr_dtype(data, cat_dtype)
        return impl_cats
    elif is_overload_none(ordered):

        def impl_auto(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, 'category')
        return impl_auto
    raise BodoError(
        f'pd.Categorical(): argument combination not supported yet: {values}, {categories}, {ordered}, {dtype}'
        )


@overload(operator.getitem, no_unliteral=True)
def categorical_array_getitem(arr, ind):
    if not isinstance(arr, CategoricalArrayType):
        return
    if isinstance(ind, types.Integer):

        def categorical_getitem_impl(arr, ind):
            ktcmj__nibnw = arr.codes[ind]
            return arr.dtype.categories[max(ktcmj__nibnw, 0)]
        return categorical_getitem_impl
    if is_list_like_index_type(ind) or isinstance(ind, types.SliceType):

        def impl_bool(arr, ind):
            return init_categorical_array(arr.codes[ind], arr.dtype)
        return impl_bool
    raise BodoError(
        f'getitem for CategoricalArrayType with indexing type {ind} not supported.'
        )


class CategoricalMatchingValues(enum.Enum):
    DIFFERENT_TYPES = -1
    DONT_MATCH = 0
    MAY_MATCH = 1
    DO_MATCH = 2


def categorical_arrs_match(arr1, arr2):
    if not (isinstance(arr1, CategoricalArrayType) and isinstance(arr2,
        CategoricalArrayType)):
        return CategoricalMatchingValues.DIFFERENT_TYPES
    if arr1.dtype.categories is None or arr2.dtype.categories is None:
        return CategoricalMatchingValues.MAY_MATCH
    return (CategoricalMatchingValues.DO_MATCH if arr1.dtype.categories ==
        arr2.dtype.categories and arr1.dtype.ordered == arr2.dtype.ordered else
        CategoricalMatchingValues.DONT_MATCH)


@register_jitable
def cat_dtype_equal(dtype1, dtype2):
    if dtype1.ordered != dtype2.ordered or len(dtype1.categories) != len(dtype2
        .categories):
        return False
    arr1 = dtype1.categories.values
    arr2 = dtype2.categories.values
    for cafvc__ktw in range(len(arr1)):
        if arr1[cafvc__ktw] != arr2[cafvc__ktw]:
            return False
    return True


@overload(operator.setitem, no_unliteral=True)
def categorical_array_setitem(arr, ind, val):
    if not isinstance(arr, CategoricalArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    llelp__djbwj = is_scalar_type(val) and is_common_scalar_dtype([types.
        unliteral(val), arr.dtype.elem_type]) and not (isinstance(arr.dtype
        .elem_type, types.Integer) and isinstance(val, types.Float))
    hnc__rdcfu = not isinstance(val, CategoricalArrayType
        ) and is_iterable_type(val) and is_common_scalar_dtype([val.dtype,
        arr.dtype.elem_type]) and not (isinstance(arr.dtype.elem_type,
        types.Integer) and isinstance(val.dtype, types.Float))
    pby__phog = categorical_arrs_match(arr, val)
    fagjx__gny = (
        f"setitem for CategoricalArrayType of dtype {arr.dtype} with indexing type {ind} received an incorrect 'value' type {val}."
        )
    mzi__kyc = (
        'Cannot set a Categorical with another, without identical categories')
    if isinstance(ind, types.Integer):
        if not llelp__djbwj:
            raise BodoError(fagjx__gny)

        def impl_scalar(arr, ind, val):
            if val not in arr.dtype.categories:
                raise ValueError(
                    'Cannot setitem on a Categorical with a new category, set the categories first'
                    )
            ktcmj__nibnw = arr.dtype.categories.get_loc(val)
            arr.codes[ind] = ktcmj__nibnw
        return impl_scalar
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if not (llelp__djbwj or hnc__rdcfu or pby__phog !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(fagjx__gny)
        if pby__phog == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(mzi__kyc)
        if llelp__djbwj:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                zeqrp__vzdj = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for ody__wowz in range(n):
                    arr.codes[ind[ody__wowz]] = zeqrp__vzdj
            return impl_scalar
        if pby__phog == CategoricalMatchingValues.DO_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                n = len(val.codes)
                for cafvc__ktw in range(n):
                    arr.codes[ind[cafvc__ktw]] = val.codes[cafvc__ktw]
            return impl_arr_ind_mask
        if pby__phog == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(mzi__kyc)
                n = len(val.codes)
                for cafvc__ktw in range(n):
                    arr.codes[ind[cafvc__ktw]] = val.codes[cafvc__ktw]
            return impl_arr_ind_mask
        if hnc__rdcfu:

            def impl_arr_ind_mask_cat_values(arr, ind, val):
                n = len(val)
                categories = arr.dtype.categories
                for ody__wowz in range(n):
                    jkv__nwok = bodo.utils.conversion.unbox_if_timestamp(val
                        [ody__wowz])
                    if jkv__nwok not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    ktcmj__nibnw = categories.get_loc(jkv__nwok)
                    arr.codes[ind[ody__wowz]] = ktcmj__nibnw
            return impl_arr_ind_mask_cat_values
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if not (llelp__djbwj or hnc__rdcfu or pby__phog !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(fagjx__gny)
        if pby__phog == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(mzi__kyc)
        if llelp__djbwj:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                zeqrp__vzdj = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for ody__wowz in range(n):
                    if ind[ody__wowz]:
                        arr.codes[ody__wowz] = zeqrp__vzdj
            return impl_scalar
        if pby__phog == CategoricalMatchingValues.DO_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                n = len(ind)
                red__joic = 0
                for cafvc__ktw in range(n):
                    if ind[cafvc__ktw]:
                        arr.codes[cafvc__ktw] = val.codes[red__joic]
                        red__joic += 1
            return impl_bool_ind_mask
        if pby__phog == CategoricalMatchingValues.MAY_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(mzi__kyc)
                n = len(ind)
                red__joic = 0
                for cafvc__ktw in range(n):
                    if ind[cafvc__ktw]:
                        arr.codes[cafvc__ktw] = val.codes[red__joic]
                        red__joic += 1
            return impl_bool_ind_mask
        if hnc__rdcfu:

            def impl_bool_ind_mask_cat_values(arr, ind, val):
                n = len(ind)
                red__joic = 0
                categories = arr.dtype.categories
                for ody__wowz in range(n):
                    if ind[ody__wowz]:
                        jkv__nwok = bodo.utils.conversion.unbox_if_timestamp(
                            val[red__joic])
                        if jkv__nwok not in categories:
                            raise ValueError(
                                'Cannot setitem on a Categorical with a new category, set the categories first'
                                )
                        ktcmj__nibnw = categories.get_loc(jkv__nwok)
                        arr.codes[ody__wowz] = ktcmj__nibnw
                        red__joic += 1
            return impl_bool_ind_mask_cat_values
    if isinstance(ind, types.SliceType):
        if not (llelp__djbwj or hnc__rdcfu or pby__phog !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(fagjx__gny)
        if pby__phog == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(mzi__kyc)
        if llelp__djbwj:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                zeqrp__vzdj = arr.dtype.categories.get_loc(val)
                rrv__rpae = numba.cpython.unicode._normalize_slice(ind, len
                    (arr))
                for ody__wowz in range(rrv__rpae.start, rrv__rpae.stop,
                    rrv__rpae.step):
                    arr.codes[ody__wowz] = zeqrp__vzdj
            return impl_scalar
        if pby__phog == CategoricalMatchingValues.DO_MATCH:

            def impl_arr(arr, ind, val):
                arr.codes[ind] = val.codes
            return impl_arr
        if pby__phog == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(mzi__kyc)
                arr.codes[ind] = val.codes
            return impl_arr
        if hnc__rdcfu:

            def impl_slice_cat_values(arr, ind, val):
                categories = arr.dtype.categories
                rrv__rpae = numba.cpython.unicode._normalize_slice(ind, len
                    (arr))
                red__joic = 0
                for ody__wowz in range(rrv__rpae.start, rrv__rpae.stop,
                    rrv__rpae.step):
                    jkv__nwok = bodo.utils.conversion.unbox_if_timestamp(val
                        [red__joic])
                    if jkv__nwok not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    ktcmj__nibnw = categories.get_loc(jkv__nwok)
                    arr.codes[ody__wowz] = ktcmj__nibnw
                    red__joic += 1
            return impl_slice_cat_values
    raise BodoError(
        f'setitem for CategoricalArrayType with indexing type {ind} not supported.'
        )
