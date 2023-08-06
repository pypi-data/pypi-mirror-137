from collections import defaultdict
import numba
import numpy as np
import pandas as pd
from mpi4py import MPI
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, replace_arg_nodes
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.table import Table, TableType
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, string_array_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.table_column_del_pass import get_live_column_nums_block, ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import BodoError
from bodo.utils.utils import check_java_installation
from bodo.utils.utils import sanitize_varname


class CsvReader(ir.Stmt):

    def __init__(self, file_name, df_out, sep, df_colnames, out_vars,
        out_types, usecols, loc, header, compression, nrows, skiprows,
        chunksize, is_skiprows_list, low_memory, index_column_index=None,
        index_column_typ=types.none):
        self.connector_typ = 'csv'
        self.file_name = file_name
        self.df_out = df_out
        self.sep = sep
        self.df_colnames = df_colnames
        self.out_vars = out_vars
        self.out_types = out_types
        self.usecols = usecols
        self.loc = loc
        self.skiprows = skiprows
        self.nrows = nrows
        self.header = header
        self.compression = compression
        self.chunksize = chunksize
        self.is_skiprows_list = is_skiprows_list
        self.pd_low_memory = low_memory
        self.index_column_index = index_column_index
        self.index_column_typ = index_column_typ
        self.type_usecol_offset = list(range(len(usecols)))

    def __repr__(self):
        return (
            '{} = ReadCsv(file={}, col_names={}, types={}, vars={}, nrows={}, skiprows={}, chunksize={}, is_skiprows_list={}, pd_low_memory={}, index_column_index={}, index_colum_typ = {}, type_usecol_offsets={})'
            .format(self.df_out, self.file_name, self.df_colnames, self.
            out_types, self.out_vars, self.nrows, self.skiprows, self.
            chunksize, self.is_skiprows_list, self.pd_low_memory, self.
            index_column_index, self.index_column_typ, self.type_usecol_offset)
            )


def check_node_typing(node, typemap):
    fdobl__ipei = typemap[node.file_name.name]
    if types.unliteral(fdobl__ipei) != types.unicode_type:
        raise BodoError(
            f"pd.read_csv(): 'filepath_or_buffer' must be a string. Found type: {fdobl__ipei}."
            , node.file_name.loc)
    if not isinstance(node.skiprows, ir.Const):
        lqdrm__ecz = typemap[node.skiprows.name]
        if isinstance(lqdrm__ecz, types.Dispatcher):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' callable not supported yet.",
                node.file_name.loc)
        elif not isinstance(lqdrm__ecz, types.Integer) and not (isinstance(
            lqdrm__ecz, (types.List, types.Tuple)) and isinstance(
            lqdrm__ecz.dtype, types.Integer)) and not isinstance(lqdrm__ecz,
            (types.LiteralList, bodo.utils.typing.ListLiteral)):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' must be an integer or list of integers. Found type {lqdrm__ecz}."
                , loc=node.skiprows.loc)
        elif isinstance(lqdrm__ecz, (types.List, types.Tuple)):
            node.is_skiprows_list = True
    if not isinstance(node.nrows, ir.Const):
        hryhj__hphq = typemap[node.nrows.name]
        if not isinstance(hryhj__hphq, types.Integer):
            raise BodoError(
                f"pd.read_csv(): 'nrows' must be an integer. Found type {hryhj__hphq}."
                , loc=node.nrows.loc)


import llvmlite.binding as ll
from bodo.io import csv_cpp
ll.add_symbol('csv_file_chunk_reader', csv_cpp.csv_file_chunk_reader)
csv_file_chunk_reader = types.ExternalFunction('csv_file_chunk_reader',
    bodo.ir.connector.stream_reader_type(types.voidptr, types.bool_, types.
    voidptr, types.int64, types.bool_, types.voidptr, types.voidptr, types.
    int64, types.bool_, types.int64, types.bool_))


def remove_dead_csv(csv_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if csv_node.chunksize is not None:
        lbyng__twc = csv_node.out_vars[0]
        if lbyng__twc.name not in lives:
            return None
    else:
        drubj__ofw = csv_node.out_vars[0]
        edm__wrec = csv_node.out_vars[1]
        if drubj__ofw.name not in lives and edm__wrec.name not in lives:
            return None
        elif edm__wrec.name not in lives:
            csv_node.index_column_index = None
            csv_node.index_column_typ = types.none
        elif drubj__ofw.name not in lives:
            csv_node.usecols = []
            csv_node.out_types = []
            csv_node.type_usecol_offset = []
    return csv_node


def csv_distributed_run(csv_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    parallel = False
    lqdrm__ecz = types.int64 if isinstance(csv_node.skiprows, ir.Const
        ) else types.unliteral(typemap[csv_node.skiprows.name])
    if csv_node.chunksize is not None:
        if array_dists is not None:
            dgxl__suj = csv_node.out_vars[0].name
            parallel = array_dists[dgxl__suj] in (distributed_pass.
                Distribution.OneD, distributed_pass.Distribution.OneD_Var)
        djzt__shjn = 'def csv_iterator_impl(fname, nrows, skiprows):\n'
        djzt__shjn += (
            f'    reader = _csv_reader_init(fname, nrows, skiprows)\n')
        djzt__shjn += (
            f'    iterator = init_csv_iterator(reader, csv_iterator_type)\n')
        gzn__zwsxr = {}
        from bodo.io.csv_iterator_ext import init_csv_iterator
        exec(djzt__shjn, {}, gzn__zwsxr)
        gyda__cuk = gzn__zwsxr['csv_iterator_impl']
        pykdv__exdh = 'def csv_reader_init(fname, nrows, skiprows):\n'
        pykdv__exdh += _gen_csv_file_reader_init(parallel, csv_node.header,
            csv_node.compression, csv_node.chunksize, csv_node.
            is_skiprows_list, csv_node.pd_low_memory)
        pykdv__exdh += '  return f_reader\n'
        exec(pykdv__exdh, globals(), gzn__zwsxr)
        wdkms__usgj = gzn__zwsxr['csv_reader_init']
        bftb__frzms = numba.njit(wdkms__usgj)
        compiled_funcs.append(bftb__frzms)
        psxg__nzotq = compile_to_numba_ir(gyda__cuk, {'_csv_reader_init':
            bftb__frzms, 'init_csv_iterator': init_csv_iterator,
            'csv_iterator_type': typemap[csv_node.out_vars[0].name]},
            typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
            types.int64, lqdrm__ecz), typemap=typemap, calltypes=calltypes
            ).blocks.popitem()[1]
        replace_arg_nodes(psxg__nzotq, [csv_node.file_name, csv_node.nrows,
            csv_node.skiprows])
        dxr__ssq = psxg__nzotq.body[:-3]
        dxr__ssq[-1].target = csv_node.out_vars[0]
        return dxr__ssq
    if array_dists is not None:
        czggz__xoial = csv_node.out_vars[0].name
        parallel = array_dists[czggz__xoial] in (distributed_pass.
            Distribution.OneD, distributed_pass.Distribution.OneD_Var)
        pfqkn__pesnq = csv_node.out_vars[1].name
        assert typemap[pfqkn__pesnq
            ] == types.none or not parallel or array_dists[pfqkn__pesnq] in (
            distributed_pass.Distribution.OneD, distributed_pass.
            Distribution.OneD_Var
            ), 'pq data/index parallelization does not match'
    djzt__shjn = 'def csv_impl(fname, nrows, skiprows):\n'
    djzt__shjn += (
        f'    (table_val, idx_col) = _csv_reader_py(fname, nrows, skiprows)\n')
    gzn__zwsxr = {}
    exec(djzt__shjn, {}, gzn__zwsxr)
    tvylk__savr = gzn__zwsxr['csv_impl']
    lyk__bml = csv_node.usecols
    if lyk__bml:
        lyk__bml = [csv_node.usecols[duxnx__xabze] for duxnx__xabze in
            csv_node.type_usecol_offset]
    pkozu__jmh = _gen_csv_reader_py(csv_node.df_colnames, csv_node.
        out_types, lyk__bml, csv_node.type_usecol_offset, csv_node.sep,
        parallel, csv_node.header, csv_node.compression, csv_node.
        is_skiprows_list, csv_node.pd_low_memory, idx_col_index=csv_node.
        index_column_index, idx_col_typ=csv_node.index_column_typ)
    psxg__nzotq = compile_to_numba_ir(tvylk__savr, {'_csv_reader_py':
        pkozu__jmh}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type, types.int64, lqdrm__ecz), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(psxg__nzotq, [csv_node.file_name, csv_node.nrows,
        csv_node.skiprows, csv_node.is_skiprows_list])
    dxr__ssq = psxg__nzotq.body[:-3]
    dxr__ssq[-1].target = csv_node.out_vars[1]
    dxr__ssq[-2].target = csv_node.out_vars[0]
    if csv_node.index_column_index is None:
        dxr__ssq.pop(-1)
    elif not lyk__bml:
        dxr__ssq.pop(-2)
    return dxr__ssq


def csv_remove_dead_column(csv_node, column_live_map, equiv_vars, typemap):
    if csv_node.chunksize is not None:
        return False
    assert len(csv_node.out_vars) == 2, 'invalid CsvReader node'
    abu__atku = csv_node.out_vars[0].name
    if isinstance(typemap[abu__atku], TableType) and csv_node.usecols:
        sycsu__tigps, hqpx__nkmg = get_live_column_nums_block(column_live_map,
            equiv_vars, abu__atku)
        sycsu__tigps = bodo.ir.connector.trim_extra_used_columns(sycsu__tigps,
            len(csv_node.usecols))
        if not hqpx__nkmg and not sycsu__tigps:
            sycsu__tigps = [0]
        if not hqpx__nkmg and len(sycsu__tigps) != len(csv_node.
            type_usecol_offset):
            csv_node.type_usecol_offset = sycsu__tigps
            return True
    return False


def csv_table_column_use(csv_node, block_use_map, equiv_vars, typemap):
    return


numba.parfors.array_analysis.array_analysis_extensions[CsvReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[CsvReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[CsvReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[CsvReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[CsvReader] = remove_dead_csv
numba.core.analysis.ir_extension_usedefs[CsvReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[CsvReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[CsvReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[CsvReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[CsvReader] = csv_distributed_run
remove_dead_column_extensions[CsvReader] = csv_remove_dead_column
ir_extension_table_column_use[CsvReader] = csv_table_column_use


def _get_dtype_str(t):
    lha__yjd = t.dtype
    if isinstance(lha__yjd, PDCategoricalDtype):
        neqo__rfjct = CategoricalArrayType(lha__yjd)
        kebh__wbzb = 'CategoricalArrayType' + str(ir_utils.next_label())
        setattr(types, kebh__wbzb, neqo__rfjct)
        return kebh__wbzb
    if lha__yjd == types.NPDatetime('ns'):
        lha__yjd = 'NPDatetime("ns")'
    if t == string_array_type:
        types.string_array_type = string_array_type
        return 'string_array_type'
    if isinstance(t, IntegerArrayType):
        qei__yivk = 'int_arr_{}'.format(lha__yjd)
        setattr(types, qei__yivk, t)
        return qei__yivk
    if t == boolean_array:
        types.boolean_array = boolean_array
        return 'boolean_array'
    if lha__yjd == types.bool_:
        lha__yjd = 'bool_'
    if lha__yjd == datetime_date_type:
        return 'datetime_date_array_type'
    if isinstance(t, ArrayItemArrayType) and isinstance(lha__yjd, (
        StringArrayType, ArrayItemArrayType)):
        qgoky__nwlfu = f'ArrayItemArrayType{str(ir_utils.next_label())}'
        setattr(types, qgoky__nwlfu, t)
        return qgoky__nwlfu
    return '{}[::1]'.format(lha__yjd)


def _get_pd_dtype_str(t):
    lha__yjd = t.dtype
    if isinstance(lha__yjd, PDCategoricalDtype):
        return 'pd.CategoricalDtype({})'.format(lha__yjd.categories)
    if lha__yjd == types.NPDatetime('ns'):
        return 'str'
    if t == string_array_type:
        return 'str'
    if isinstance(t, IntegerArrayType):
        return '"{}Int{}"'.format('' if lha__yjd.signed else 'U', lha__yjd.
            bitwidth)
    if t == boolean_array:
        return 'np.bool_'
    if isinstance(t, ArrayItemArrayType) and isinstance(lha__yjd, (
        StringArrayType, ArrayItemArrayType)):
        return 'object'
    return 'np.{}'.format(lha__yjd)


compiled_funcs = []


@numba.njit
def check_nrows_skiprows_value(nrows, skiprows):
    if nrows < -1:
        raise ValueError('pd.read_csv: nrows must be integer >= 0.')
    if skiprows[0] < 0:
        raise ValueError('pd.read_csv: skiprows must be integer >= 0.')


def astype(df, typemap, parallel):
    zbimo__gxf = ''
    from collections import defaultdict
    zwi__ghp = defaultdict(list)
    for emb__zqady, fwws__puaul in typemap.items():
        zwi__ghp[fwws__puaul].append(emb__zqady)
    mgc__ngirq = df.columns.to_list()
    etrc__prsma = []
    for fwws__puaul, ncofc__ctwcm in zwi__ghp.items():
        try:
            etrc__prsma.append(df.loc[:, (ncofc__ctwcm)].astype(fwws__puaul,
                copy=False))
            df = df.drop(ncofc__ctwcm, axis=1)
        except (ValueError, TypeError) as bdod__ssvzv:
            zbimo__gxf = (
                f"Caught the runtime error '{bdod__ssvzv}' on columns {ncofc__ctwcm}. Consider setting the 'dtype' argument in 'read_csv' or investigate if the data is corrupted."
                )
            break
    dcsqr__gnhb = bool(zbimo__gxf)
    if parallel:
        xjbx__vqlk = MPI.COMM_WORLD
        dcsqr__gnhb = xjbx__vqlk.allreduce(dcsqr__gnhb, op=MPI.LOR)
    if dcsqr__gnhb:
        rrb__tefvl = 'pd.read_csv(): Bodo could not infer dtypes correctly.'
        if zbimo__gxf:
            raise TypeError(f'{rrb__tefvl}\n{zbimo__gxf}')
        else:
            raise TypeError(
                f'{rrb__tefvl}\nPlease refer to errors on other ranks.')
    df = pd.concat(etrc__prsma + [df], axis=1)
    zduuk__wjdh = df.loc[:, (mgc__ngirq)]
    return zduuk__wjdh


def _gen_csv_file_reader_init(parallel, header, compression, chunksize,
    is_skiprows_list, pd_low_memory):
    poyou__rhx = header == 0
    if compression is None:
        compression = 'uncompressed'
    if is_skiprows_list:
        djzt__shjn = '  skiprows = sorted(set(skiprows))\n'
    else:
        djzt__shjn = '  skiprows = [skiprows]\n'
    djzt__shjn += '  skiprows_list_len = len(skiprows)\n'
    djzt__shjn += '  check_nrows_skiprows_value(nrows, skiprows)\n'
    djzt__shjn += '  check_java_installation(fname)\n'
    djzt__shjn += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    djzt__shjn += (
        '  f_reader = bodo.ir.csv_ext.csv_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    djzt__shjn += (
        """    {}, bodo.utils.conversion.coerce_to_ndarray(skiprows, scalar_to_arr_len=1).ctypes, nrows, {}, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), {}, {}, skiprows_list_len, {})
"""
        .format(parallel, poyou__rhx, compression, chunksize,
        is_skiprows_list, pd_low_memory))
    djzt__shjn += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    djzt__shjn += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    djzt__shjn += "      raise FileNotFoundError('File does not exist')\n"
    return djzt__shjn


def _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs, usecols,
    type_usecol_offset, sep, call_id, glbs, parallel,
    check_parallel_runtime, idx_col_index, idx_col_typ):
    icd__iwipw = [str(xuv__qjgce) for duxnx__xabze, xuv__qjgce in enumerate
        (usecols) if col_typs[type_usecol_offset[duxnx__xabze]].dtype ==
        types.NPDatetime('ns')]
    if idx_col_typ == types.NPDatetime('ns'):
        assert not idx_col_index is None
        icd__iwipw.append(str(idx_col_index))
    ipq__vtiir = ', '.join(icd__iwipw)
    dcuzs__smj = _gen_parallel_flag_name(sanitized_cnames)
    qyhn__mwqs = f"{dcuzs__smj}='bool_'" if check_parallel_runtime else ''
    wqqow__igxo = [_get_pd_dtype_str(col_typs[type_usecol_offset[
        duxnx__xabze]]) for duxnx__xabze in range(len(usecols))]
    aex__bno = None if idx_col_index is None else _get_pd_dtype_str(idx_col_typ
        )
    tjozu__qeq = [xuv__qjgce for duxnx__xabze, xuv__qjgce in enumerate(
        usecols) if wqqow__igxo[duxnx__xabze] == 'str']
    if idx_col_index is not None and aex__bno == 'str':
        tjozu__qeq.append(idx_col_index)
    poeb__etbk = np.array(tjozu__qeq, dtype=np.int64)
    glbs[f'str_col_nums_{call_id}'] = poeb__etbk
    djzt__shjn = f'  str_col_nums_{call_id}_2 = str_col_nums_{call_id}\n'
    werj__rdxc = np.array(usecols + ([idx_col_index] if idx_col_index is not
        None else []))
    glbs[f'usecols_arr_{call_id}'] = werj__rdxc
    djzt__shjn += f'  usecols_arr_{call_id}_2 = usecols_arr_{call_id}\n'
    ehb__rmdir = np.array(type_usecol_offset, dtype=np.int64)
    if usecols:
        glbs[f'type_usecols_offsets_arr_{call_id}'] = ehb__rmdir
        djzt__shjn += f"""  type_usecols_offsets_arr_{call_id}_2 = type_usecols_offsets_arr_{call_id}
"""
    cqajr__yow = defaultdict(list)
    for duxnx__xabze, xuv__qjgce in enumerate(usecols):
        if wqqow__igxo[duxnx__xabze] == 'str':
            continue
        cqajr__yow[wqqow__igxo[duxnx__xabze]].append(xuv__qjgce)
    if idx_col_index is not None and aex__bno != 'str':
        cqajr__yow[aex__bno].append(idx_col_index)
    for duxnx__xabze, osfd__zqdo in enumerate(cqajr__yow.values()):
        glbs[f't_arr_{duxnx__xabze}_{call_id}'] = np.asarray(osfd__zqdo)
        djzt__shjn += (
            f'  t_arr_{duxnx__xabze}_{call_id}_2 = t_arr_{duxnx__xabze}_{call_id}\n'
            )
    if idx_col_index != None:
        djzt__shjn += f"""  with objmode(T=table_type_{call_id}, idx_arr=idx_array_typ, {qyhn__mwqs}):
"""
    else:
        djzt__shjn += (
            f'  with objmode(T=table_type_{call_id}, {qyhn__mwqs}):\n')
    djzt__shjn += f'    typemap = {{}}\n'
    for duxnx__xabze, vga__jiiea in enumerate(cqajr__yow.keys()):
        djzt__shjn += f"""    typemap.update({{i:{vga__jiiea} for i in t_arr_{duxnx__xabze}_{call_id}_2}})
"""
    djzt__shjn += '    if f_reader.get_chunk_size() == 0:\n'
    djzt__shjn += (
        f'      df = pd.DataFrame(columns=usecols_arr_{call_id}_2, dtype=str)\n'
        )
    djzt__shjn += '    else:\n'
    djzt__shjn += '      df = pd.read_csv(f_reader,\n'
    djzt__shjn += '        header=None,\n'
    djzt__shjn += '        parse_dates=[{}],\n'.format(ipq__vtiir)
    djzt__shjn += (
        f'        dtype={{i:str for i in str_col_nums_{call_id}_2}},\n')
    djzt__shjn += (
        f'        usecols=usecols_arr_{call_id}_2, sep={sep!r}, low_memory=False)\n'
        )
    if check_parallel_runtime:
        djzt__shjn += f'    {dcuzs__smj} = f_reader.is_parallel()\n'
    else:
        djzt__shjn += f'    {dcuzs__smj} = {parallel}\n'
    djzt__shjn += f'    df = astype(df, typemap, {dcuzs__smj})\n'
    if idx_col_index != None:
        rjt__tbnlj = sorted(werj__rdxc).index(idx_col_index)
        djzt__shjn += f'    idx_arr = df.iloc[:, {rjt__tbnlj}].values\n'
        djzt__shjn += (
            f'    df.drop(columns=df.columns[{rjt__tbnlj}], inplace=True)\n')
    if len(usecols) == 0:
        djzt__shjn += f'    T = None\n'
    else:
        djzt__shjn += f'    arrs = []\n'
        djzt__shjn += f'    for i in range(df.shape[1]):\n'
        djzt__shjn += f'      arrs.append(df.iloc[:, i].values)\n'
        djzt__shjn += f"""    T = Table(arrs, type_usecols_offsets_arr_{call_id}_2, {len(col_names)})
"""
    return djzt__shjn


def _gen_parallel_flag_name(sanitized_cnames):
    dcuzs__smj = '_parallel_value'
    while dcuzs__smj in sanitized_cnames:
        dcuzs__smj = '_' + dcuzs__smj
    return dcuzs__smj


def _gen_csv_reader_py(col_names, col_typs, usecols, type_usecol_offset,
    sep, parallel, header, compression, is_skiprows_list, pd_low_memory,
    idx_col_index=None, idx_col_typ=types.none):
    sanitized_cnames = [sanitize_varname(oib__qrgd) for oib__qrgd in col_names]
    djzt__shjn = 'def csv_reader_py(fname, nrows, skiprows):\n'
    djzt__shjn += _gen_csv_file_reader_init(parallel, header, compression, 
        -1, is_skiprows_list, pd_low_memory)
    call_id = ir_utils.next_label()
    xpg__btgj = globals()
    if idx_col_typ != types.none:
        xpg__btgj[f'idx_array_typ'] = idx_col_typ
    if len(usecols) == 0:
        xpg__btgj[f'table_type_{call_id}'] = types.none
    else:
        xpg__btgj[f'table_type_{call_id}'] = TableType(tuple(col_typs))
    djzt__shjn += _gen_read_csv_objmode(col_names, sanitized_cnames,
        col_typs, usecols, type_usecol_offset, sep, call_id, xpg__btgj,
        parallel=parallel, check_parallel_runtime=False, idx_col_index=
        idx_col_index, idx_col_typ=idx_col_typ)
    if idx_col_index != None:
        djzt__shjn += '  return (T, idx_arr)\n'
    else:
        djzt__shjn += '  return (T, None)\n'
    gzn__zwsxr = {}
    exec(djzt__shjn, xpg__btgj, gzn__zwsxr)
    pkozu__jmh = gzn__zwsxr['csv_reader_py']
    bftb__frzms = numba.njit(pkozu__jmh)
    compiled_funcs.append(bftb__frzms)
    return bftb__frzms
