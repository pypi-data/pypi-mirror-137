"""CSR Matrix data type implementation for scipy.sparse.csr_matrix
"""
import operator
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
import bodo
from bodo.utils.typing import BodoError


class CSRMatrixType(types.ArrayCompatible):
    ndim = 2

    def __init__(self, dtype, idx_dtype):
        self.dtype = dtype
        self.idx_dtype = idx_dtype
        super(CSRMatrixType, self).__init__(name=
            f'CSRMatrixType({dtype}, {idx_dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    def copy(self):
        return CSRMatrixType(self.dtype, self.idx_dtype)


@register_model(CSRMatrixType)
class CSRMatrixModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        itcsy__qhjf = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'indices', types.Array(fe_type.idx_dtype, 1, 'C')), ('indptr',
            types.Array(fe_type.idx_dtype, 1, 'C')), ('shape', types.
            UniTuple(types.int64, 2))]
        models.StructModel.__init__(self, dmm, fe_type, itcsy__qhjf)


make_attribute_wrapper(CSRMatrixType, 'data', 'data')
make_attribute_wrapper(CSRMatrixType, 'indices', 'indices')
make_attribute_wrapper(CSRMatrixType, 'indptr', 'indptr')
make_attribute_wrapper(CSRMatrixType, 'shape', 'shape')


@intrinsic
def init_csr_matrix(typingctx, data_t, indices_t, indptr_t, shape_t=None):
    assert isinstance(data_t, types.Array)
    assert isinstance(indices_t, types.Array) and isinstance(indices_t.
        dtype, types.Integer)
    assert indices_t == indptr_t

    def codegen(context, builder, signature, args):
        vqq__sxrw, rdwc__jsijt, hoqt__etcc, crkki__kmkhd = args
        cihd__uidjb = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        cihd__uidjb.data = vqq__sxrw
        cihd__uidjb.indices = rdwc__jsijt
        cihd__uidjb.indptr = hoqt__etcc
        cihd__uidjb.shape = crkki__kmkhd
        context.nrt.incref(builder, signature.args[0], vqq__sxrw)
        context.nrt.incref(builder, signature.args[1], rdwc__jsijt)
        context.nrt.incref(builder, signature.args[2], hoqt__etcc)
        return cihd__uidjb._getvalue()
    uzsae__ncu = CSRMatrixType(data_t.dtype, indices_t.dtype)
    jhvm__kwv = uzsae__ncu(data_t, indices_t, indptr_t, types.UniTuple(
        types.int64, 2))
    return jhvm__kwv, codegen


if bodo.utils.utils.has_scipy():
    import scipy.sparse

    @typeof_impl.register(scipy.sparse.csr_matrix)
    def _typeof_csr_matrix(val, c):
        dtype = numba.from_dtype(val.dtype)
        idx_dtype = numba.from_dtype(val.indices.dtype)
        return CSRMatrixType(dtype, idx_dtype)


@unbox(CSRMatrixType)
def unbox_csr_matrix(typ, val, c):
    cihd__uidjb = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    jmoif__tkode = c.pyapi.object_getattr_string(val, 'data')
    sxmgu__flp = c.pyapi.object_getattr_string(val, 'indices')
    notgv__wlu = c.pyapi.object_getattr_string(val, 'indptr')
    xssc__ljf = c.pyapi.object_getattr_string(val, 'shape')
    cihd__uidjb.data = c.pyapi.to_native_value(types.Array(typ.dtype, 1,
        'C'), jmoif__tkode).value
    cihd__uidjb.indices = c.pyapi.to_native_value(types.Array(typ.idx_dtype,
        1, 'C'), sxmgu__flp).value
    cihd__uidjb.indptr = c.pyapi.to_native_value(types.Array(typ.idx_dtype,
        1, 'C'), notgv__wlu).value
    cihd__uidjb.shape = c.pyapi.to_native_value(types.UniTuple(types.int64,
        2), xssc__ljf).value
    c.pyapi.decref(jmoif__tkode)
    c.pyapi.decref(sxmgu__flp)
    c.pyapi.decref(notgv__wlu)
    c.pyapi.decref(xssc__ljf)
    oliif__yyy = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cihd__uidjb._getvalue(), is_error=oliif__yyy)


@box(CSRMatrixType)
def box_csr_matrix(typ, val, c):
    xftw__cibuj = c.context.insert_const_string(c.builder.module,
        'scipy.sparse')
    nsoj__ikjos = c.pyapi.import_module_noblock(xftw__cibuj)
    cihd__uidjb = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Array(typ.dtype, 1, 'C'),
        cihd__uidjb.data)
    jmoif__tkode = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        cihd__uidjb.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        cihd__uidjb.indices)
    sxmgu__flp = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1,
        'C'), cihd__uidjb.indices, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        cihd__uidjb.indptr)
    notgv__wlu = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1,
        'C'), cihd__uidjb.indptr, c.env_manager)
    xssc__ljf = c.pyapi.from_native_value(types.UniTuple(types.int64, 2),
        cihd__uidjb.shape, c.env_manager)
    mvfr__lvit = c.pyapi.tuple_pack([jmoif__tkode, sxmgu__flp, notgv__wlu])
    crtp__alxx = c.pyapi.call_method(nsoj__ikjos, 'csr_matrix', (mvfr__lvit,
        xssc__ljf))
    c.pyapi.decref(mvfr__lvit)
    c.pyapi.decref(jmoif__tkode)
    c.pyapi.decref(sxmgu__flp)
    c.pyapi.decref(notgv__wlu)
    c.pyapi.decref(xssc__ljf)
    c.pyapi.decref(nsoj__ikjos)
    c.context.nrt.decref(c.builder, typ, val)
    return crtp__alxx


@overload(len, no_unliteral=True)
def overload_csr_matrix_len(A):
    if isinstance(A, CSRMatrixType):
        return lambda A: A.shape[0]


@overload_attribute(CSRMatrixType, 'ndim')
def overload_csr_matrix_ndim(A):
    return lambda A: 2


@overload_method(CSRMatrixType, 'copy', no_unliteral=True)
def overload_csr_matrix_copy(A):

    def copy_impl(A):
        return init_csr_matrix(A.data.copy(), A.indices.copy(), A.indptr.
            copy(), A.shape)
    return copy_impl


@overload(operator.getitem, no_unliteral=True)
def csr_matrix_getitem(A, idx):
    if not isinstance(A, CSRMatrixType):
        return
    loq__ixfik = A.dtype
    fggs__bom = A.idx_dtype
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):

        def impl(A, idx):
            gwwf__jrax, wzvz__kfyqd = A.shape
            dga__pvsea = numba.cpython.unicode._normalize_slice(idx[0],
                gwwf__jrax)
            vec__cpeau = numba.cpython.unicode._normalize_slice(idx[1],
                wzvz__kfyqd)
            if dga__pvsea.step != 1 or vec__cpeau.step != 1:
                raise ValueError(
                    'CSR matrix slice getitem only supports step=1 currently')
            ptu__bee = dga__pvsea.start
            kdoz__pzw = dga__pvsea.stop
            dui__przbz = vec__cpeau.start
            orecz__hoye = vec__cpeau.stop
            pzh__hwl = A.indptr
            viott__hyqif = A.indices
            tfzu__lwqp = A.data
            xgi__yxxi = kdoz__pzw - ptu__bee
            rnfw__ach = orecz__hoye - dui__przbz
            vam__kux = 0
            dwo__xkfnr = 0
            for auupm__lpkb in range(xgi__yxxi):
                pbrg__sfbe = pzh__hwl[ptu__bee + auupm__lpkb]
                radr__qdmlf = pzh__hwl[ptu__bee + auupm__lpkb + 1]
                for csfld__flps in range(pbrg__sfbe, radr__qdmlf):
                    if viott__hyqif[csfld__flps
                        ] >= dui__przbz and viott__hyqif[csfld__flps
                        ] < orecz__hoye:
                        vam__kux += 1
            rbtbo__xgogi = np.empty(xgi__yxxi + 1, fggs__bom)
            xxgx__bexgv = np.empty(vam__kux, fggs__bom)
            uslhe__bofj = np.empty(vam__kux, loq__ixfik)
            rbtbo__xgogi[0] = 0
            for auupm__lpkb in range(xgi__yxxi):
                pbrg__sfbe = pzh__hwl[ptu__bee + auupm__lpkb]
                radr__qdmlf = pzh__hwl[ptu__bee + auupm__lpkb + 1]
                for csfld__flps in range(pbrg__sfbe, radr__qdmlf):
                    if viott__hyqif[csfld__flps
                        ] >= dui__przbz and viott__hyqif[csfld__flps
                        ] < orecz__hoye:
                        xxgx__bexgv[dwo__xkfnr] = viott__hyqif[csfld__flps
                            ] - dui__przbz
                        uslhe__bofj[dwo__xkfnr] = tfzu__lwqp[csfld__flps]
                        dwo__xkfnr += 1
                rbtbo__xgogi[auupm__lpkb + 1] = dwo__xkfnr
            return init_csr_matrix(uslhe__bofj, xxgx__bexgv, rbtbo__xgogi,
                (xgi__yxxi, rnfw__ach))
        return impl
    raise BodoError(
        f'getitem for CSR matrix with index type {idx} not supported yet.')
