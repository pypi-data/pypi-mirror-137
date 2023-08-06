"""
Class information for DataFrame iterators returned by pd.read_csv. This is used
to handle situations in which pd.read_csv is used to return chunks with separate
read calls instead of just a single read.
"""
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir_utils, types
from numba.core.imputils import RefType, impl_ret_borrowed, iternext_impl
from numba.core.typing.templates import signature
from numba.extending import intrinsic, lower_builtin, models, register_model
import bodo
import bodo.ir.connector
import bodo.ir.csv_ext
from bodo import objmode
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.table import Table, TableType
from bodo.io import csv_cpp
from bodo.ir.csv_ext import _gen_read_csv_objmode, astype
from bodo.utils.utils import check_java_installation
from bodo.utils.utils import sanitize_varname
ll.add_symbol('update_csv_reader', csv_cpp.update_csv_reader)
ll.add_symbol('initialize_csv_reader', csv_cpp.initialize_csv_reader)


class CSVIteratorType(types.SimpleIteratorType):

    def __init__(self, df_type, out_colnames, out_types, usecols, sep,
        index_ind, index_arr_typ, index_name):
        assert isinstance(df_type, DataFrameType
            ), 'CSVIterator must return a DataFrame'
        leza__sgob = (
            f'CSVIteratorType({df_type}, {out_colnames}, {out_types}, {usecols}, {sep}, {index_ind}, {index_arr_typ}, {index_name})'
            )
        super(types.SimpleIteratorType, self).__init__(leza__sgob)
        self._yield_type = df_type
        self._out_colnames = out_colnames
        self._out_types = out_types
        self._usecols = usecols
        self._sep = sep
        self._index_ind = index_ind
        self._index_arr_typ = index_arr_typ
        self._index_name = index_name

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(CSVIteratorType)
class CSVIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        hnnkh__xtif = [('csv_reader', bodo.ir.connector.stream_reader_type),
            ('index', types.EphemeralPointer(types.uintp))]
        super(CSVIteratorModel, self).__init__(dmm, fe_type, hnnkh__xtif)


@lower_builtin('getiter', CSVIteratorType)
def getiter_csv_iterator(context, builder, sig, args):
    kvxsz__xkbdt = cgutils.create_struct_proxy(sig.args[0])(context,
        builder, value=args[0])
    bac__jibe = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer()])
    vdj__vakh = cgutils.get_or_insert_function(builder.module, bac__jibe,
        name='initialize_csv_reader')
    builder.call(vdj__vakh, [kvxsz__xkbdt.csv_reader])
    builder.store(context.get_constant(types.uint64, 0), kvxsz__xkbdt.index)
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', CSVIteratorType)
@iternext_impl(RefType.NEW)
def iternext_csv_iterator(context, builder, sig, args, result):
    [poadu__xlhyp] = sig.args
    [vgnb__ter] = args
    kvxsz__xkbdt = cgutils.create_struct_proxy(poadu__xlhyp)(context,
        builder, value=vgnb__ter)
    bac__jibe = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer()])
    vdj__vakh = cgutils.get_or_insert_function(builder.module, bac__jibe,
        name='update_csv_reader')
    mmhg__lsf = builder.call(vdj__vakh, [kvxsz__xkbdt.csv_reader])
    result.set_valid(mmhg__lsf)
    with builder.if_then(mmhg__lsf):
        pbrs__rreo = builder.load(kvxsz__xkbdt.index)
        hfumv__lrwml = types.Tuple([sig.return_type.first_type, types.int64])
        xfqq__hnvqg = gen_read_csv_objmode(sig.args[0])
        aysgq__qur = signature(hfumv__lrwml, bodo.ir.connector.
            stream_reader_type, types.int64)
        zrk__aaccb = context.compile_internal(builder, xfqq__hnvqg,
            aysgq__qur, [kvxsz__xkbdt.csv_reader, pbrs__rreo])
        jfyi__ibf, onxfu__wjf = cgutils.unpack_tuple(builder, zrk__aaccb)
        nzy__mpi = builder.add(pbrs__rreo, onxfu__wjf, flags=['nsw'])
        builder.store(nzy__mpi, kvxsz__xkbdt.index)
        result.yield_(jfyi__ibf)


@intrinsic
def init_csv_iterator(typingctx, csv_reader, csv_iterator_typeref):

    def codegen(context, builder, signature, args):
        txsp__mdbf = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        txsp__mdbf.csv_reader = args[0]
        cixbb__pnnm = context.get_constant(types.uintp, 0)
        txsp__mdbf.index = cgutils.alloca_once_value(builder, cixbb__pnnm)
        return txsp__mdbf._getvalue()
    assert isinstance(csv_iterator_typeref, types.TypeRef
        ), 'Initializing a csv iterator requires a typeref'
    mci__jzwl = csv_iterator_typeref.instance_type
    sig = signature(mci__jzwl, csv_reader, csv_iterator_typeref)
    return sig, codegen


def gen_read_csv_objmode(csv_iterator_type):
    ipbtl__feogl = 'def read_csv_objmode(f_reader):\n'
    dqg__qvbf = [sanitize_varname(rakj__qkb) for rakj__qkb in
        csv_iterator_type._out_colnames]
    sjly__qvo = ir_utils.next_label()
    caimo__ayvb = globals()
    out_types = csv_iterator_type._out_types
    caimo__ayvb[f'table_type_{sjly__qvo}'] = TableType(tuple(out_types))
    caimo__ayvb[f'idx_array_typ'] = csv_iterator_type._index_arr_typ
    cxyds__xwc = list(range(len(csv_iterator_type._usecols)))
    ipbtl__feogl += _gen_read_csv_objmode(csv_iterator_type._out_colnames,
        dqg__qvbf, out_types, csv_iterator_type._usecols, cxyds__xwc,
        csv_iterator_type._sep, sjly__qvo, caimo__ayvb, parallel=False,
        check_parallel_runtime=True, idx_col_index=csv_iterator_type.
        _index_ind, idx_col_typ=csv_iterator_type._index_arr_typ)
    ycfyj__uvtcl = bodo.ir.csv_ext._gen_parallel_flag_name(dqg__qvbf)
    tfi__flv = ['T'] + (['idx_arr'] if csv_iterator_type._index_ind is not
        None else []) + [ycfyj__uvtcl]
    ipbtl__feogl += f"  return {', '.join(tfi__flv)}"
    caimo__ayvb = globals()
    oicj__fkvsx = {}
    exec(ipbtl__feogl, caimo__ayvb, oicj__fkvsx)
    sfhoa__xofmn = oicj__fkvsx['read_csv_objmode']
    avvo__toq = numba.njit(sfhoa__xofmn)
    bodo.ir.csv_ext.compiled_funcs.append(avvo__toq)
    nafl__zvmc = 'def read_func(reader, local_start):\n'
    nafl__zvmc += f"  {', '.join(tfi__flv)} = objmode_func(reader)\n"
    index_ind = csv_iterator_type._index_ind
    if index_ind is None:
        nafl__zvmc += f'  local_len = len(T)\n'
        nafl__zvmc += '  total_size = local_len\n'
        nafl__zvmc += f'  if ({ycfyj__uvtcl}):\n'
        nafl__zvmc += """    local_start = local_start + bodo.libs.distributed_api.dist_exscan(local_len, _op)
"""
        nafl__zvmc += (
            '    total_size = bodo.libs.distributed_api.dist_reduce(local_len, _op)\n'
            )
        uklbv__bnue = (
            f'bodo.hiframes.pd_index_ext.init_range_index(local_start, local_start + local_len, 1, None)'
            )
    else:
        nafl__zvmc += '  total_size = 0\n'
        uklbv__bnue = (
            f'bodo.utils.conversion.convert_to_index({tfi__flv[1]}, {csv_iterator_type._index_name!r})'
            )
    nafl__zvmc += f"""  return (bodo.hiframes.pd_dataframe_ext.init_dataframe(({tfi__flv[0]},), {uklbv__bnue}, out_df_typ), total_size)
"""
    exec(nafl__zvmc, {'bodo': bodo, 'objmode_func': avvo__toq, '_op': np.
        int32(bodo.libs.distributed_api.Reduce_Type.Sum.value),
        'out_df_typ': csv_iterator_type.yield_type}, oicj__fkvsx)
    return oicj__fkvsx['read_func']
