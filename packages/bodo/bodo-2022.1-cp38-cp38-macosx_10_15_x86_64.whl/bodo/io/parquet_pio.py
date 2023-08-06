import os
import warnings
from collections import defaultdict
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pyarrow
import pyarrow.dataset as ds
from numba.core import ir, types
from numba.core.ir_utils import compile_to_numba_ir, get_definition, guard, mk_unique_var, next_label, replace_arg_nodes
from numba.extending import NativeValue, intrinsic, models, overload, register_model, unbox
from pyarrow import null
import bodo
import bodo.ir.parquet_ext
import bodo.utils.tracing as tracing
from bodo.hiframes.datetime_date_ext import datetime_date_array_type, datetime_date_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.table import TableType
from bodo.io.fs_io import get_hdfs_fs, get_s3_fs_from_path, get_s3_subtree_fs
from bodo.libs.array import cpp_table_to_py_table, delete_table, info_from_table, info_to_array, table_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.distributed_api import get_end, get_start
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.transforms import distributed_pass
from bodo.utils.transform import get_const_value
from bodo.utils.typing import BodoError, BodoWarning, FileInfo, get_overload_const_str, get_overload_constant_dict
from bodo.utils.utils import check_and_propagate_cpp_exception, numba_to_c_type, sanitize_varname
use_nullable_int_arr = True
from urllib.parse import urlparse
import bodo.io.pa_parquet


class ParquetPredicateType(types.Type):

    def __init__(self):
        super(ParquetPredicateType, self).__init__(name=
            'ParquetPredicateType()')


parquet_predicate_type = ParquetPredicateType()
types.parquet_predicate_type = parquet_predicate_type
register_model(ParquetPredicateType)(models.OpaqueModel)


@unbox(ParquetPredicateType)
def unbox_parquet_predicate_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


class ReadParquetFilepathType(types.Opaque):

    def __init__(self):
        super(ReadParquetFilepathType, self).__init__(name=
            'ReadParquetFilepathType')


read_parquet_fpath_type = ReadParquetFilepathType()
types.read_parquet_fpath_type = read_parquet_fpath_type
register_model(ReadParquetFilepathType)(models.OpaqueModel)


@unbox(ReadParquetFilepathType)
def unbox_read_parquet_fpath_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


class StorageOptionsDictType(types.Opaque):

    def __init__(self):
        super(StorageOptionsDictType, self).__init__(name=
            'StorageOptionsDictType')


storage_options_dict_type = StorageOptionsDictType()
types.storage_options_dict_type = storage_options_dict_type
register_model(StorageOptionsDictType)(models.OpaqueModel)


@unbox(StorageOptionsDictType)
def unbox_storage_options_dict_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


class ParquetFileInfo(FileInfo):

    def __init__(self, columns, storage_options=None):
        self.columns = columns
        self.storage_options = storage_options
        super().__init__()

    def _get_schema(self, fname):
        try:
            return parquet_file_schema(fname, selected_columns=self.columns,
                storage_options=self.storage_options)
        except OSError as zcsg__hjcg:
            if 'non-file path' in str(zcsg__hjcg):
                raise FileNotFoundError(str(zcsg__hjcg))
            raise


class ParquetHandler:

    def __init__(self, func_ir, typingctx, args, _locals):
        self.func_ir = func_ir
        self.typingctx = typingctx
        self.args = args
        self.locals = _locals

    def gen_parquet_read(self, file_name, lhs, columns, storage_options=None):
        xtn__npy = lhs.scope
        wja__gfw = lhs.loc
        syxey__jpyk = None
        if lhs.name in self.locals:
            syxey__jpyk = self.locals[lhs.name]
            self.locals.pop(lhs.name)
        rztu__wvys = {}
        if lhs.name + ':convert' in self.locals:
            rztu__wvys = self.locals[lhs.name + ':convert']
            self.locals.pop(lhs.name + ':convert')
        if syxey__jpyk is None:
            jcpxd__rdakp = (
                'Parquet schema not available. Either path argument should be constant for Bodo to look at the file at compile time or schema should be provided. For more information, see: https://docs.bodo.ai/latest/source/programming_with_bodo/file_io.html#non-constant-filepaths'
                )
            miu__zmmks = get_const_value(file_name, self.func_ir,
                jcpxd__rdakp, arg_types=self.args, file_info=
                ParquetFileInfo(columns, storage_options=storage_options))
            eos__cgjw = False
            jjf__vonng = guard(get_definition, self.func_ir, file_name)
            if isinstance(jjf__vonng, ir.Arg):
                typ = self.args[jjf__vonng.index]
                if isinstance(typ, types.FilenameType):
                    (col_names, uxsx__evxt, zgl__syg, col_indices,
                        partition_names) = typ.schema
                    eos__cgjw = True
            if not eos__cgjw:
                (col_names, uxsx__evxt, zgl__syg, col_indices, partition_names
                    ) = (parquet_file_schema(miu__zmmks, columns,
                    storage_options=storage_options))
        else:
            ulbj__nyxre = list(syxey__jpyk.keys())
            hxni__lyuyn = [oxp__zhr for oxp__zhr in syxey__jpyk.values()]
            zgl__syg = 'index' if 'index' in ulbj__nyxre else None
            if columns is None:
                selected_columns = ulbj__nyxre
            else:
                selected_columns = columns
            col_indices = [ulbj__nyxre.index(c) for c in selected_columns]
            uxsx__evxt = [hxni__lyuyn[ulbj__nyxre.index(c)] for c in
                selected_columns]
            col_names = selected_columns
            zgl__syg = zgl__syg if zgl__syg in col_names else None
            partition_names = []
        euezo__lakzm = None if isinstance(zgl__syg, dict
            ) or zgl__syg is None else zgl__syg
        index_column_index = None
        index_column_type = types.none
        if euezo__lakzm:
            gzrc__usje = col_names.index(euezo__lakzm)
            col_indices = col_indices.copy()
            uxsx__evxt = uxsx__evxt.copy()
            index_column_index = col_indices.pop(gzrc__usje)
            index_column_type = uxsx__evxt.pop(gzrc__usje)
        for ltpbh__eqlw, c in enumerate(col_names):
            if c in rztu__wvys:
                uxsx__evxt[ltpbh__eqlw] = rztu__wvys[c]
        clcg__ytfkx = [ir.Var(xtn__npy, mk_unique_var('pq_table'), wja__gfw
            ), ir.Var(xtn__npy, mk_unique_var('pq_index'), wja__gfw)]
        dffzp__rvlf = [bodo.ir.parquet_ext.ParquetReader(file_name, lhs.
            name, col_names, col_indices, uxsx__evxt, clcg__ytfkx, wja__gfw,
            partition_names, storage_options, index_column_index,
            index_column_type)]
        return (col_names, clcg__ytfkx, zgl__syg, dffzp__rvlf, uxsx__evxt,
            index_column_type)


def determine_filter_cast(pq_node, typemap, filter_val):
    fksrl__eulg = filter_val[0]
    iehv__lwow = pq_node.original_out_types[pq_node.original_df_colnames.
        index(fksrl__eulg)]
    yryl__pxyk = bodo.utils.typing.element_type(iehv__lwow)
    if fksrl__eulg in pq_node.partition_names:
        if yryl__pxyk == types.unicode_type:
            vdzgx__ntzsb = '.cast(pyarrow.string(), safe=False)'
        elif isinstance(yryl__pxyk, types.Integer):
            vdzgx__ntzsb = f'.cast(pyarrow.{yryl__pxyk.name}(), safe=False)'
        else:
            vdzgx__ntzsb = ''
    else:
        vdzgx__ntzsb = ''
    fmdti__zac = typemap[filter_val[2].name]
    if not bodo.utils.typing.is_common_scalar_dtype([yryl__pxyk, fmdti__zac]):
        if not bodo.utils.typing.is_safe_arrow_cast(yryl__pxyk, fmdti__zac):
            raise BodoError(
                f'Unsupport Arrow cast from {yryl__pxyk} to {fmdti__zac} in filter pushdown. Please try a comparison that avoids casting the column.'
                )
        if yryl__pxyk == types.unicode_type:
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif yryl__pxyk in (bodo.datetime64ns, bodo.pd_timestamp_type):
            return vdzgx__ntzsb, ".cast(pyarrow.timestamp('ns'), safe=False)"
    return vdzgx__ntzsb, ''


def pq_distributed_run(pq_node, array_dists, typemap, calltypes, typingctx,
    targetctx, meta_head_only_info=None):
    xmgl__gcjxd = len(pq_node.out_vars)
    extra_args = ''
    dnf_filter_str = 'None'
    expr_filter_str = 'None'
    cfa__huc, thlvu__dqfvq = bodo.ir.connector.generate_filter_map(pq_node.
        filters)
    if cfa__huc:
        ldy__smpi = []
        cfvpl__iik = []
        uxfwi__sjvyr = False
        aoxn__yzgcp = None
        for uxid__grojz in pq_node.filters:
            wja__gmne = []
            kiyjn__myy = []
            amwkb__rtrt = set()
            for rlg__hfyfl in uxid__grojz:
                if isinstance(rlg__hfyfl[2], ir.Var):
                    lxvzk__yyl, lbq__lby = determine_filter_cast(pq_node,
                        typemap, rlg__hfyfl)
                    kiyjn__myy.append(
                        f"(ds.field('{rlg__hfyfl[0]}'){lxvzk__yyl} {rlg__hfyfl[1]} ds.scalar({cfa__huc[rlg__hfyfl[2].name]}){lbq__lby})"
                        )
                else:
                    assert rlg__hfyfl[2
                        ] == 'NULL', 'unsupport constant used in filter pushdown'
                    if rlg__hfyfl[1] == 'is not':
                        lvfz__dpudo = '~'
                    else:
                        lvfz__dpudo = ''
                    kiyjn__myy.append(
                        f"({lvfz__dpudo}ds.field('{rlg__hfyfl[0]}').is_null())"
                        )
                if rlg__hfyfl[0] in pq_node.partition_names and isinstance(
                    rlg__hfyfl[2], ir.Var):
                    hqj__csydt = (
                        f"('{rlg__hfyfl[0]}', '{rlg__hfyfl[1]}', {cfa__huc[rlg__hfyfl[2].name]})"
                        )
                    wja__gmne.append(hqj__csydt)
                    amwkb__rtrt.add(hqj__csydt)
                else:
                    uxfwi__sjvyr = True
            if aoxn__yzgcp is None:
                aoxn__yzgcp = amwkb__rtrt
            else:
                aoxn__yzgcp.intersection_update(amwkb__rtrt)
            rdck__masuv = ', '.join(wja__gmne)
            wvs__wvfig = ' & '.join(kiyjn__myy)
            if rdck__masuv:
                ldy__smpi.append(f'[{rdck__masuv}]')
            cfvpl__iik.append(f'({wvs__wvfig})')
        xlyr__fvgp = ', '.join(ldy__smpi)
        yrv__ifa = ' | '.join(cfvpl__iik)
        if uxfwi__sjvyr:
            if aoxn__yzgcp:
                yuxfk__gwy = sorted(aoxn__yzgcp)
                dnf_filter_str = f"[[{', '.join(yuxfk__gwy)}]]"
        elif xlyr__fvgp:
            dnf_filter_str = f'[{xlyr__fvgp}]'
        expr_filter_str = f'({yrv__ifa})'
        extra_args = ', '.join(cfa__huc.values())
    nqf__lrs = ', '.join(f'out{ltpbh__eqlw}' for ltpbh__eqlw in range(
        xmgl__gcjxd))
    wazdp__wjd = f'def pq_impl(fname, {extra_args}):\n'
    wazdp__wjd += (
        f'    (total_rows, {nqf__lrs},) = _pq_reader_py(fname, {extra_args})\n'
        )
    eyqy__ojypo = {}
    exec(wazdp__wjd, {}, eyqy__ojypo)
    ztwjp__qdt = eyqy__ojypo['pq_impl']
    parallel = False
    if array_dists is not None:
        obups__fjd = pq_node.out_vars[0].name
        parallel = array_dists[obups__fjd] in (distributed_pass.
            Distribution.OneD, distributed_pass.Distribution.OneD_Var)
        wygjk__tsk = pq_node.out_vars[1].name
        assert typemap[wygjk__tsk
            ] == types.none or not parallel or array_dists[wygjk__tsk] in (
            distributed_pass.Distribution.OneD, distributed_pass.
            Distribution.OneD_Var
            ), 'pq data/index parallelization does not match'
    nqh__svg = _gen_pq_reader_py(pq_node.df_colnames, pq_node.col_indices,
        pq_node.type_usecol_offset, pq_node.out_types, pq_node.
        storage_options, pq_node.partition_names, dnf_filter_str,
        expr_filter_str, extra_args, parallel, meta_head_only_info, pq_node
        .index_column_index, pq_node.index_column_type)
    dofrj__rrt = typemap[pq_node.file_name.name]
    jdnpz__wjfp = (dofrj__rrt,) + tuple(typemap[rlg__hfyfl.name] for
        rlg__hfyfl in thlvu__dqfvq)
    hdzx__wvx = compile_to_numba_ir(ztwjp__qdt, {'_pq_reader_py': nqh__svg},
        typingctx=typingctx, targetctx=targetctx, arg_typs=jdnpz__wjfp,
        typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(hdzx__wvx, [pq_node.file_name] + thlvu__dqfvq)
    dffzp__rvlf = hdzx__wvx.body[:-3]
    if meta_head_only_info:
        dffzp__rvlf[-1 - xmgl__gcjxd].target = meta_head_only_info[1]
    dffzp__rvlf[-2].target = pq_node.out_vars[0]
    dffzp__rvlf[-1].target = pq_node.out_vars[1]
    return dffzp__rvlf


distributed_pass.distributed_run_extensions[bodo.ir.parquet_ext.ParquetReader
    ] = pq_distributed_run


def get_filters_pyobject(dnf_filter_str, expr_filter_str, vars):
    pass


@overload(get_filters_pyobject, no_unliteral=True)
def overload_get_filters_pyobject(dnf_filter_str, expr_filter_str, var_tup):
    jzh__hvvvj = get_overload_const_str(dnf_filter_str)
    qqzqh__wnl = get_overload_const_str(expr_filter_str)
    eog__ajdyc = ', '.join(f'f{ltpbh__eqlw}' for ltpbh__eqlw in range(len(
        var_tup)))
    wazdp__wjd = 'def impl(dnf_filter_str, expr_filter_str, var_tup):\n'
    if len(var_tup):
        wazdp__wjd += f'  {eog__ajdyc}, = var_tup\n'
    wazdp__wjd += """  with numba.objmode(dnf_filters_py='parquet_predicate_type', expr_filters_py='parquet_predicate_type'):
"""
    wazdp__wjd += f'    dnf_filters_py = {jzh__hvvvj}\n'
    wazdp__wjd += f'    expr_filters_py = {qqzqh__wnl}\n'
    wazdp__wjd += '  return (dnf_filters_py, expr_filters_py)\n'
    eyqy__ojypo = {}
    exec(wazdp__wjd, globals(), eyqy__ojypo)
    return eyqy__ojypo['impl']


@numba.njit
def get_fname_pyobject(fname):
    with numba.objmode(fname_py='read_parquet_fpath_type'):
        fname_py = fname
    return fname_py


def get_storage_options_pyobject(storage_options):
    pass


@overload(get_storage_options_pyobject, no_unliteral=True)
def overload_get_storage_options_pyobject(storage_options):
    ctxgi__tnxue = get_overload_constant_dict(storage_options)
    wazdp__wjd = 'def impl(storage_options):\n'
    wazdp__wjd += (
        "  with numba.objmode(storage_options_py='storage_options_dict_type'):\n"
        )
    wazdp__wjd += f'    storage_options_py = {str(ctxgi__tnxue)}\n'
    wazdp__wjd += '  return storage_options_py\n'
    eyqy__ojypo = {}
    exec(wazdp__wjd, globals(), eyqy__ojypo)
    return eyqy__ojypo['impl']


def _gen_pq_reader_py(col_names, col_indices, type_usecol_offset, out_types,
    storage_options, partition_names, dnf_filter_str, expr_filter_str,
    extra_args, is_parallel, meta_head_only_info, index_column_index,
    index_column_type):
    lhdx__xce = next_label()
    wqbc__bkvg = ',' if extra_args else ''
    wazdp__wjd = f'def pq_reader_py(fname,{extra_args}):\n'
    wazdp__wjd += (
        f"    ev = bodo.utils.tracing.Event('read_parquet', {is_parallel})\n")
    wazdp__wjd += "    ev.add_attribute('fname', fname)\n"
    wazdp__wjd += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={is_parallel})
"""
    wazdp__wjd += f"""    dnf_filters, expr_filters = get_filters_pyobject("{dnf_filter_str}", "{expr_filter_str}", ({extra_args}{wqbc__bkvg}))
"""
    wazdp__wjd += '    fname_py = get_fname_pyobject(fname)\n'
    storage_options['bodo_dummy'] = 'dummy'
    wazdp__wjd += (
        f'    storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    yhrea__ylmkl = -1
    if meta_head_only_info and meta_head_only_info[0] is not None:
        yhrea__ylmkl = meta_head_only_info[0]
    hgc__woi = not type_usecol_offset
    kba__ghsxo = [sanitize_varname(c) for c in col_names]
    partition_names = [sanitize_varname(c) for c in partition_names]
    ackae__xqtu = []
    jipzx__hdg = set()
    for ltpbh__eqlw in type_usecol_offset:
        if kba__ghsxo[ltpbh__eqlw] not in partition_names:
            ackae__xqtu.append(col_indices[ltpbh__eqlw])
        else:
            jipzx__hdg.add(col_indices[ltpbh__eqlw])
    if index_column_index is not None:
        ackae__xqtu.append(index_column_index)
    ackae__xqtu = sorted(ackae__xqtu)

    def is_nullable(typ):
        return bodo.utils.utils.is_array_typ(typ, False) and not isinstance(typ
            , types.Array)
    cbocz__vuxer = [(int(is_nullable(out_types[col_indices.index(lcbb__mxb)
        ])) if lcbb__mxb != index_column_index else int(is_nullable(
        index_column_type))) for lcbb__mxb in ackae__xqtu]
    vaie__tqt = []
    cpg__idegr = []
    cmrbe__sjpq = []
    for ltpbh__eqlw, fvjyu__sdjd in enumerate(partition_names):
        try:
            juiw__udh = kba__ghsxo.index(fvjyu__sdjd)
            if col_indices[juiw__udh] not in jipzx__hdg:
                continue
        except ValueError as iutzk__hohni:
            continue
        vaie__tqt.append(fvjyu__sdjd)
        cpg__idegr.append(ltpbh__eqlw)
        nocd__jhwy = out_types[juiw__udh].dtype
        wwtp__fqgg = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            nocd__jhwy)
        cmrbe__sjpq.append(numba_to_c_type(wwtp__fqgg))
    wazdp__wjd += f'    total_rows_np = np.array([0], dtype=np.int64)\n'
    if len(cpg__idegr) > 0:
        wazdp__wjd += f"""    out_table = pq_read(fname_py, {is_parallel}, unicode_to_utf8(bucket_region), dnf_filters, expr_filters, storage_options_py, {yhrea__ylmkl}, selected_cols_arr_{lhdx__xce}.ctypes, {len(ackae__xqtu)}, nullable_cols_arr_{lhdx__xce}.ctypes, np.array({cpg__idegr}, dtype=np.int32).ctypes, np.array({cmrbe__sjpq}, dtype=np.int32).ctypes, {len(cpg__idegr)}, total_rows_np.ctypes)
"""
    else:
        wazdp__wjd += f"""    out_table = pq_read(fname_py, {is_parallel}, unicode_to_utf8(bucket_region), dnf_filters, expr_filters, storage_options_py, {yhrea__ylmkl}, selected_cols_arr_{lhdx__xce}.ctypes, {len(ackae__xqtu)}, nullable_cols_arr_{lhdx__xce}.ctypes, 0, 0, 0, total_rows_np.ctypes)
"""
    wazdp__wjd += '    check_and_propagate_cpp_exception()\n'
    zji__ylwzs = 'None'
    msps__add = index_column_type
    zsh__lfm = TableType(tuple(out_types))
    if hgc__woi:
        zsh__lfm = types.none
    if index_column_index is not None:
        xnfrs__isnl = ackae__xqtu.index(index_column_index)
        zji__ylwzs = (
            f'info_to_array(info_from_table(out_table, {xnfrs__isnl}), index_arr_type)'
            )
    wazdp__wjd += f'    index_arr = {zji__ylwzs}\n'
    if hgc__woi:
        upkrb__alxz = None
    else:
        upkrb__alxz = []
        icqt__npyb = 0
        for ltpbh__eqlw, rxma__nqlib in enumerate(col_indices):
            if icqt__npyb < len(type_usecol_offset
                ) and ltpbh__eqlw == type_usecol_offset[icqt__npyb]:
                jowxe__dznz = col_indices[ltpbh__eqlw]
                if jowxe__dznz in jipzx__hdg:
                    jsns__atvpf = kba__ghsxo[ltpbh__eqlw]
                    upkrb__alxz.append(len(ackae__xqtu) + vaie__tqt.index(
                        jsns__atvpf))
                else:
                    upkrb__alxz.append(ackae__xqtu.index(rxma__nqlib))
                icqt__npyb += 1
            else:
                upkrb__alxz.append(-1)
        upkrb__alxz = np.array(upkrb__alxz, dtype=np.int64)
    if hgc__woi:
        wazdp__wjd += '    T = None\n'
    else:
        wazdp__wjd += f"""    T = cpp_table_to_py_table(out_table, table_idx_{lhdx__xce}, py_table_type_{lhdx__xce})
"""
    wazdp__wjd += '    delete_table(out_table)\n'
    wazdp__wjd += f'    total_rows = total_rows_np[0]\n'
    wazdp__wjd += f'    ev.finalize()\n'
    wazdp__wjd += '    return (total_rows, T, index_arr)\n'
    eyqy__ojypo = {}
    ziay__jete = {f'py_table_type_{lhdx__xce}': zsh__lfm,
        f'table_idx_{lhdx__xce}': upkrb__alxz,
        f'selected_cols_arr_{lhdx__xce}': np.array(ackae__xqtu, np.int32),
        f'nullable_cols_arr_{lhdx__xce}': np.array(cbocz__vuxer, np.int32),
        'index_arr_type': msps__add, 'cpp_table_to_py_table':
        cpp_table_to_py_table, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'delete_table': delete_table,
        'check_and_propagate_cpp_exception':
        check_and_propagate_cpp_exception, 'pq_read': _pq_read,
        'unicode_to_utf8': unicode_to_utf8, 'get_filters_pyobject':
        get_filters_pyobject, 'get_storage_options_pyobject':
        get_storage_options_pyobject, 'get_fname_pyobject':
        get_fname_pyobject, 'np': np, 'pd': pd, 'bodo': bodo}
    exec(wazdp__wjd, ziay__jete, eyqy__ojypo)
    nqh__svg = eyqy__ojypo['pq_reader_py']
    bqel__xoce = numba.njit(nqh__svg, no_cpython_wrapper=True)
    return bqel__xoce


def _get_numba_typ_from_pa_typ(pa_typ, is_index, nullable_from_metadata,
    category_info):
    import pyarrow as pa
    if isinstance(pa_typ.type, pa.ListType):
        return ArrayItemArrayType(_get_numba_typ_from_pa_typ(pa_typ.type.
            value_field, is_index, nullable_from_metadata, category_info))
    if isinstance(pa_typ.type, pa.StructType):
        eln__kwoe = []
        ebv__dwt = []
        for iinxt__gmcz in pa_typ.flatten():
            ebv__dwt.append(iinxt__gmcz.name.split('.')[-1])
            eln__kwoe.append(_get_numba_typ_from_pa_typ(iinxt__gmcz,
                is_index, nullable_from_metadata, category_info))
        return StructArrayType(tuple(eln__kwoe), tuple(ebv__dwt))
    if isinstance(pa_typ.type, pa.Decimal128Type):
        return DecimalArrayType(pa_typ.type.precision, pa_typ.type.scale)
    cvzv__mlhrv = {pa.bool_(): types.bool_, pa.int8(): types.int8, pa.int16
        (): types.int16, pa.int32(): types.int32, pa.int64(): types.int64,
        pa.uint8(): types.uint8, pa.uint16(): types.uint16, pa.uint32():
        types.uint32, pa.uint64(): types.uint64, pa.float32(): types.
        float32, pa.float64(): types.float64, pa.string(): string_type, pa.
        binary(): bytes_type, pa.date32(): datetime_date_type, pa.date64():
        types.NPDatetime('ns'), pa.timestamp('ns'): types.NPDatetime('ns'),
        pa.timestamp('us'): types.NPDatetime('ns'), pa.timestamp('ms'):
        types.NPDatetime('ns'), pa.timestamp('s'): types.NPDatetime('ns'),
        null(): string_type}
    if isinstance(pa_typ.type, pa.DictionaryType):
        if pa_typ.type.value_type != pa.string():
            raise BodoError(
                f'Parquet Categorical data type should be string, not {pa_typ.type.value_type}'
                )
        ivmq__cjyjm = cvzv__mlhrv[pa_typ.type.index_type]
        tgt__kdk = PDCategoricalDtype(category_info[pa_typ.name], bodo.
            string_type, pa_typ.type.ordered, int_type=ivmq__cjyjm)
        return CategoricalArrayType(tgt__kdk)
    if pa_typ.type not in cvzv__mlhrv:
        raise BodoError('Arrow data type {} not supported yet'.format(
            pa_typ.type))
    xch__ltnyf = cvzv__mlhrv[pa_typ.type]
    if xch__ltnyf == datetime_date_type:
        return datetime_date_array_type
    if xch__ltnyf == bytes_type:
        return binary_array_type
    yujmy__lwmnx = (string_array_type if xch__ltnyf == string_type else
        types.Array(xch__ltnyf, 1, 'C'))
    if xch__ltnyf == types.bool_:
        yujmy__lwmnx = boolean_array
    if nullable_from_metadata is not None:
        jdl__nxe = nullable_from_metadata
    else:
        jdl__nxe = use_nullable_int_arr
    if jdl__nxe and not is_index and isinstance(xch__ltnyf, types.Integer
        ) and pa_typ.nullable:
        yujmy__lwmnx = IntegerArrayType(xch__ltnyf)
    return yujmy__lwmnx


def is_filter_pushdown_disabled_fpath(fpath):
    return fpath.startswith('gs://') or fpath.startswith('gcs://'
        ) or fpath.startswith('hdfs://') or fpath.startswith('abfs://'
        ) or fpath.startswith('abfss://')


def get_parquet_dataset(fpath, get_row_counts=True, dnf_filters=None,
    expr_filters=None, storage_options=None, read_categories=False,
    is_parallel=False):
    if get_row_counts:
        yimek__eyoy = tracing.Event('get_parquet_dataset')
    import time
    import pyarrow as pa
    import pyarrow.parquet as pq
    from mpi4py import MPI
    rinu__regfr = MPI.COMM_WORLD
    if isinstance(fpath, list):
        zfcu__snjjv = urlparse(fpath[0])
        mvi__ile = zfcu__snjjv.scheme
        jlw__dbolp = zfcu__snjjv.netloc
        for ltpbh__eqlw in range(len(fpath)):
            pkr__yhg = fpath[ltpbh__eqlw]
            ejqy__vns = urlparse(pkr__yhg)
            if ejqy__vns.scheme != mvi__ile:
                raise BodoError(
                    'All parquet files must use the same filesystem protocol')
            if ejqy__vns.netloc != jlw__dbolp:
                raise BodoError(
                    'All parquet files must be in the same S3 bucket')
            fpath[ltpbh__eqlw] = pkr__yhg.rstrip('/')
    else:
        zfcu__snjjv = urlparse(fpath)
        mvi__ile = zfcu__snjjv.scheme
        fpath = fpath.rstrip('/')
    if mvi__ile in {'gcs', 'gs'}:
        try:
            import gcsfs
        except ImportError as iutzk__hohni:
            bsbre__luruj = """Couldn't import gcsfs, which is required for Google cloud access. gcsfs can be installed by calling 'conda install -c conda-forge gcsfs'.
"""
            raise BodoError(bsbre__luruj)
    if mvi__ile == 'http':
        try:
            import fsspec
        except ImportError as iutzk__hohni:
            bsbre__luruj = """Couldn't import fsspec, which is required for http access. fsspec can be installed by calling 'conda install -c conda-forge fsspec'.
"""
    ogj__hsg = []

    def getfs(parallel=False):
        if len(ogj__hsg) == 1:
            return ogj__hsg[0]
        if mvi__ile == 's3':
            ogj__hsg.append(get_s3_fs_from_path(fpath, parallel=parallel,
                storage_options=storage_options) if not isinstance(fpath,
                list) else get_s3_fs_from_path(fpath[0], parallel=parallel,
                storage_options=storage_options))
        elif mvi__ile in {'gcs', 'gs'}:
            lriva__ksvks = gcsfs.GCSFileSystem(token=None)
            ogj__hsg.append(lriva__ksvks)
        elif mvi__ile == 'http':
            ogj__hsg.append(fsspec.filesystem('http'))
        elif mvi__ile in {'hdfs', 'abfs', 'abfss'}:
            ogj__hsg.append(get_hdfs_fs(fpath) if not isinstance(fpath,
                list) else get_hdfs_fs(fpath[0]))
        else:
            ogj__hsg.append(None)
        return ogj__hsg[0]
    jafcu__yhhzc = False
    if get_row_counts:
        sycoo__mbec = getfs(parallel=True)
        jafcu__yhhzc = bodo.parquet_validate_schema
    if bodo.get_rank() == 0:
        tvp__cbp = 1
        mcnx__axa = os.cpu_count()
        if mcnx__axa is not None and mcnx__axa > 1:
            tvp__cbp = mcnx__axa // 2
        try:
            if get_row_counts:
                wcer__awbah = tracing.Event('pq.ParquetDataset',
                    is_parallel=False)
                if tracing.is_tracing():
                    wcer__awbah.add_attribute('dnf_filter', str(dnf_filters))
            gbl__gnevw = pa.io_thread_count()
            pa.set_io_thread_count(tvp__cbp)
            rfqr__rtwvp = pq.ParquetDataset(fpath, filesystem=getfs(),
                filters=None, use_legacy_dataset=True, validate_schema=
                False, metadata_nthreads=tvp__cbp)
            pa.set_io_thread_count(gbl__gnevw)
            ochz__leuwm = bodo.io.pa_parquet.get_dataset_schema(rfqr__rtwvp)
            if dnf_filters:
                if get_row_counts:
                    wcer__awbah.add_attribute('num_pieces_before_filter',
                        len(rfqr__rtwvp.pieces))
                xqci__tdwzb = time.time()
                rfqr__rtwvp._filter(dnf_filters)
                if get_row_counts:
                    wcer__awbah.add_attribute('dnf_filter_time', time.time(
                        ) - xqci__tdwzb)
                    wcer__awbah.add_attribute('num_pieces_after_filter',
                        len(rfqr__rtwvp.pieces))
            if get_row_counts:
                wcer__awbah.finalize()
            rfqr__rtwvp._metadata.fs = None
        except Exception as zcsg__hjcg:
            rinu__regfr.bcast(zcsg__hjcg)
            raise BodoError(
                f'error from pyarrow: {type(zcsg__hjcg).__name__}: {str(zcsg__hjcg)}\n'
                )
        if get_row_counts:
            ypa__ihko = tracing.Event('bcast dataset')
        rinu__regfr.bcast(rfqr__rtwvp)
        rinu__regfr.bcast(ochz__leuwm)
    else:
        if get_row_counts:
            ypa__ihko = tracing.Event('bcast dataset')
        rfqr__rtwvp = rinu__regfr.bcast(None)
        if isinstance(rfqr__rtwvp, Exception):
            mjw__yzk = rfqr__rtwvp
            raise BodoError(
                f'error from pyarrow: {type(mjw__yzk).__name__}: {str(mjw__yzk)}\n'
                )
        ochz__leuwm = rinu__regfr.bcast(None)
    if get_row_counts:
        ypa__ihko.finalize()
    rfqr__rtwvp._bodo_total_rows = 0
    if get_row_counts or jafcu__yhhzc:
        if get_row_counts and tracing.is_tracing():
            orm__awf = tracing.Event('get_row_counts')
            orm__awf.add_attribute('g_num_pieces', len(rfqr__rtwvp.pieces))
            orm__awf.add_attribute('g_expr_filters', str(expr_filters))
        kimtx__okf = 0.0
        num_pieces = len(rfqr__rtwvp.pieces)
        start = get_start(num_pieces, bodo.get_size(), bodo.get_rank())
        fdkp__gkccl = get_end(num_pieces, bodo.get_size(), bodo.get_rank())
        zjft__cve = 0
        tezc__zkfbg = 0
        gdu__digv = True
        rfqr__rtwvp._metadata.fs = getfs()
        if expr_filters is not None:
            import random
            random.seed(37)
            jmhsq__aeiua = random.sample(rfqr__rtwvp.pieces, k=len(
                rfqr__rtwvp.pieces))
        else:
            jmhsq__aeiua = rfqr__rtwvp.pieces
        for fuvp__mehpa in jmhsq__aeiua:
            fuvp__mehpa._bodo_num_rows = 0
        if mvi__ile in {'gcs', 'gs', 'hdfs', 'abfs', 'abfss'}:
            for fuvp__mehpa in jmhsq__aeiua[start:fdkp__gkccl]:
                xac__wyf = fuvp__mehpa.get_metadata()
                if get_row_counts:
                    if expr_filters is not None:
                        pa.set_io_thread_count(2)
                        pa.set_cpu_count(2)
                        xqci__tdwzb = time.time()
                        dfyem__zcsqt = ds.dataset(fuvp__mehpa.path,
                            partitioning=ds.partitioning(flavor='hive')
                            ).scanner(filter=expr_filters, use_threads=True,
                            use_async=True).count_rows()
                        kimtx__okf += time.time() - xqci__tdwzb
                    else:
                        dfyem__zcsqt = xac__wyf.num_rows
                    fuvp__mehpa._bodo_num_rows = dfyem__zcsqt
                    zjft__cve += dfyem__zcsqt
                    tezc__zkfbg += xac__wyf.num_row_groups
                if jafcu__yhhzc:
                    boe__fwo = xac__wyf.schema.to_arrow_schema()
                    if ochz__leuwm != boe__fwo:
                        print(
                            'Schema in {!s} was different. \n{!s}\n\nvs\n\n{!s}'
                            .format(fuvp__mehpa, boe__fwo, ochz__leuwm))
                        gdu__digv = False
                        break
        else:
            fpaths = [fuvp__mehpa.path for fuvp__mehpa in jmhsq__aeiua[
                start:fdkp__gkccl]]
            if mvi__ile == 's3':
                jlw__dbolp = zfcu__snjjv.netloc
                lvfz__dpudo = 's3://' + jlw__dbolp + '/'
                fpaths = [pkr__yhg[len(lvfz__dpudo):] for pkr__yhg in fpaths]
                cea__ciak = get_s3_subtree_fs(jlw__dbolp, region=getfs().
                    region, storage_options=storage_options)
            else:
                cea__ciak = None
            pa.set_io_thread_count(4)
            pa.set_cpu_count(4)
            fcqn__jrxg = ds.dataset(fpaths, filesystem=cea__ciak,
                partitioning=ds.partitioning(flavor='hive'))
            for yylqh__fbkt, xwmj__xahdj in zip(jmhsq__aeiua[start:
                fdkp__gkccl], fcqn__jrxg.get_fragments()):
                xqci__tdwzb = time.time()
                dfyem__zcsqt = xwmj__xahdj.scanner(schema=fcqn__jrxg.schema,
                    filter=expr_filters, use_threads=True, use_async=True
                    ).count_rows()
                kimtx__okf += time.time() - xqci__tdwzb
                yylqh__fbkt._bodo_num_rows = dfyem__zcsqt
                zjft__cve += dfyem__zcsqt
                tezc__zkfbg += xwmj__xahdj.num_row_groups
                if jafcu__yhhzc:
                    boe__fwo = xwmj__xahdj.metadata.schema.to_arrow_schema()
                    if ochz__leuwm != boe__fwo:
                        print(
                            'Schema in {!s} was different. \n{!s}\n\nvs\n\n{!s}'
                            .format(yylqh__fbkt, boe__fwo, ochz__leuwm))
                        gdu__digv = False
                        break
        if jafcu__yhhzc:
            gdu__digv = rinu__regfr.allreduce(gdu__digv, op=MPI.LAND)
            if not gdu__digv:
                raise BodoError("Schema in parquet files don't match")
        if get_row_counts:
            rfqr__rtwvp._bodo_total_rows = rinu__regfr.allreduce(zjft__cve,
                op=MPI.SUM)
            ejh__wsqqg = rinu__regfr.allreduce(tezc__zkfbg, op=MPI.SUM)
            xbqcv__syupd = np.array([fuvp__mehpa._bodo_num_rows for
                fuvp__mehpa in rfqr__rtwvp.pieces])
            xbqcv__syupd = rinu__regfr.allreduce(xbqcv__syupd, op=MPI.SUM)
            for fuvp__mehpa, nmxk__iksp in zip(rfqr__rtwvp.pieces, xbqcv__syupd
                ):
                fuvp__mehpa._bodo_num_rows = nmxk__iksp
            if is_parallel and bodo.get_rank(
                ) == 0 and ejh__wsqqg < bodo.get_size():
                warnings.warn(BodoWarning(
                    f"""Total number of row groups in parquet dataset {fpath} ({ejh__wsqqg}) is too small for effective IO parallelization.
For best performance the number of row groups should be greater than the number of workers ({bodo.get_size()})
"""
                    ))
            if tracing.is_tracing():
                orm__awf.add_attribute('g_total_num_row_groups', ejh__wsqqg)
                if expr_filters is not None:
                    orm__awf.add_attribute('total_scan_time', kimtx__okf)
                pfhah__yoa = np.array([fuvp__mehpa._bodo_num_rows for
                    fuvp__mehpa in rfqr__rtwvp.pieces])
                ubvoq__yvg = np.percentile(pfhah__yoa, [25, 50, 75])
                orm__awf.add_attribute('g_row_counts_min', pfhah__yoa.min())
                orm__awf.add_attribute('g_row_counts_Q1', ubvoq__yvg[0])
                orm__awf.add_attribute('g_row_counts_median', ubvoq__yvg[1])
                orm__awf.add_attribute('g_row_counts_Q3', ubvoq__yvg[2])
                orm__awf.add_attribute('g_row_counts_max', pfhah__yoa.max())
                orm__awf.add_attribute('g_row_counts_mean', pfhah__yoa.mean())
                orm__awf.add_attribute('g_row_counts_std', pfhah__yoa.std())
                orm__awf.add_attribute('g_row_counts_sum', pfhah__yoa.sum())
                orm__awf.finalize()
    rfqr__rtwvp._prefix = ''
    if mvi__ile == 'hdfs':
        lvfz__dpudo = f'{mvi__ile}://{zfcu__snjjv.netloc}'
        if len(rfqr__rtwvp.pieces) > 0:
            yylqh__fbkt = rfqr__rtwvp.pieces[0]
            if not yylqh__fbkt.path.startswith(lvfz__dpudo):
                rfqr__rtwvp._prefix = lvfz__dpudo
    if read_categories:
        _add_categories_to_pq_dataset(rfqr__rtwvp)
    if get_row_counts:
        yimek__eyoy.finalize()
    return rfqr__rtwvp


def get_scanner_batches(fpaths, expr_filters, selected_fields,
    avg_num_pieces, is_parallel, storage_options, region):
    import pyarrow as pa
    mcnx__axa = os.cpu_count()
    if mcnx__axa is None or mcnx__axa == 0:
        mcnx__axa = 2
    pqiuj__xbhl = min(4, mcnx__axa)
    iilj__oqdnc = min(16, mcnx__axa)
    if is_parallel and len(fpaths) > iilj__oqdnc and len(fpaths
        ) / avg_num_pieces >= 2.0:
        pa.set_io_thread_count(iilj__oqdnc)
        pa.set_cpu_count(iilj__oqdnc)
    else:
        pa.set_io_thread_count(pqiuj__xbhl)
        pa.set_cpu_count(pqiuj__xbhl)
    if fpaths[0].startswith('s3://'):
        jlw__dbolp = urlparse(fpaths[0]).netloc
        lvfz__dpudo = 's3://' + jlw__dbolp + '/'
        fpaths = [pkr__yhg[len(lvfz__dpudo):] for pkr__yhg in fpaths]
        cea__ciak = get_s3_subtree_fs(jlw__dbolp, region=region,
            storage_options=storage_options)
    else:
        cea__ciak = None
    rfqr__rtwvp = ds.dataset(fpaths, filesystem=cea__ciak, partitioning=ds.
        partitioning(flavor='hive'))
    col_names = rfqr__rtwvp.schema.names
    ognlb__tqxg = [col_names[hyyr__nrfu] for hyyr__nrfu in selected_fields]
    return rfqr__rtwvp.scanner(columns=ognlb__tqxg, filter=expr_filters,
        use_threads=True, use_async=True).to_reader()


def _add_categories_to_pq_dataset(pq_dataset):
    import pyarrow as pa
    from mpi4py import MPI
    if len(pq_dataset.pieces) < 1:
        raise BodoError(
            'No pieces found in Parquet dataset. Cannot get read categorical values'
            )
    qqax__aefxz = pq_dataset.schema.to_arrow_schema()
    kmyve__ahtkr = [c for c in qqax__aefxz.names if isinstance(qqax__aefxz.
        field(c).type, pa.DictionaryType)]
    if len(kmyve__ahtkr) == 0:
        pq_dataset._category_info = {}
        return
    rinu__regfr = MPI.COMM_WORLD
    if bodo.get_rank() == 0:
        try:
            mjn__zztqg = pq_dataset.pieces[0].open()
            gvzeb__wzyc = mjn__zztqg.read_row_group(0, kmyve__ahtkr)
            category_info = {c: tuple(gvzeb__wzyc.column(c).chunk(0).
                dictionary.to_pylist()) for c in kmyve__ahtkr}
            del mjn__zztqg, gvzeb__wzyc
        except Exception as zcsg__hjcg:
            rinu__regfr.bcast(zcsg__hjcg)
            raise zcsg__hjcg
        rinu__regfr.bcast(category_info)
    else:
        category_info = rinu__regfr.bcast(None)
        if isinstance(category_info, Exception):
            mjw__yzk = category_info
            raise mjw__yzk
    pq_dataset._category_info = category_info


def get_pandas_metadata(schema, num_pieces):
    zgl__syg = None
    nullable_from_metadata = defaultdict(lambda : None)
    jxgb__kthwu = b'pandas'
    if schema.metadata is not None and jxgb__kthwu in schema.metadata:
        import json
        fldpl__swtt = json.loads(schema.metadata[jxgb__kthwu].decode('utf8'))
        vlr__ufttb = len(fldpl__swtt['index_columns'])
        if vlr__ufttb > 1:
            raise BodoError('read_parquet: MultiIndex not supported yet')
        zgl__syg = fldpl__swtt['index_columns'][0] if vlr__ufttb else None
        if not isinstance(zgl__syg, str) and (not isinstance(zgl__syg, dict
            ) or num_pieces != 1):
            zgl__syg = None
        for epx__adsc in fldpl__swtt['columns']:
            geqcl__ektyo = epx__adsc['name']
            if epx__adsc['pandas_type'].startswith('int'
                ) and geqcl__ektyo is not None:
                if epx__adsc['numpy_type'].startswith('Int'):
                    nullable_from_metadata[geqcl__ektyo] = True
                else:
                    nullable_from_metadata[geqcl__ektyo] = False
    return zgl__syg, nullable_from_metadata


def parquet_file_schema(file_name, selected_columns, storage_options=None):
    col_names = []
    uxsx__evxt = []
    pq_dataset = get_parquet_dataset(file_name, get_row_counts=False,
        storage_options=storage_options, read_categories=True)
    partition_names = [] if pq_dataset.partitions is None else [pq_dataset.
        partitions.levels[ltpbh__eqlw].name for ltpbh__eqlw in range(len(
        pq_dataset.partitions.partition_names))]
    qqax__aefxz = pq_dataset.schema.to_arrow_schema()
    num_pieces = len(pq_dataset.pieces)
    col_names = qqax__aefxz.names
    zgl__syg, nullable_from_metadata = get_pandas_metadata(qqax__aefxz,
        num_pieces)
    hxni__lyuyn = [_get_numba_typ_from_pa_typ(qqax__aefxz.field(c), c ==
        zgl__syg, nullable_from_metadata[c], pq_dataset._category_info) for
        c in col_names]
    if partition_names:
        col_names += partition_names
        hxni__lyuyn += [_get_partition_cat_dtype(pq_dataset.partitions.
            levels[ltpbh__eqlw]) for ltpbh__eqlw in range(len(partition_names))
            ]
    if selected_columns is None:
        selected_columns = col_names
    for c in selected_columns:
        if c not in col_names:
            raise BodoError('Selected column {} not in Parquet file schema'
                .format(c))
    if zgl__syg and not isinstance(zgl__syg, dict
        ) and zgl__syg not in selected_columns:
        selected_columns.append(zgl__syg)
    col_indices = [col_names.index(c) for c in selected_columns]
    uxsx__evxt = [hxni__lyuyn[col_names.index(c)] for c in selected_columns]
    col_names = selected_columns
    return col_names, uxsx__evxt, zgl__syg, col_indices, partition_names


def _get_partition_cat_dtype(part_set):
    nmqhg__urh = part_set.dictionary.to_pandas()
    tag__vkcgc = bodo.typeof(nmqhg__urh).dtype
    tgt__kdk = PDCategoricalDtype(tuple(nmqhg__urh), tag__vkcgc, False)
    return CategoricalArrayType(tgt__kdk)


_pq_read = types.ExternalFunction('pq_read', table_type(
    read_parquet_fpath_type, types.boolean, types.voidptr,
    parquet_predicate_type, parquet_predicate_type,
    storage_options_dict_type, types.int64, types.voidptr, types.int32,
    types.voidptr, types.voidptr, types.voidptr, types.int32, types.voidptr))
from llvmlite import ir as lir
from numba.core import cgutils
if bodo.utils.utils.has_pyarrow():
    from bodo.io import arrow_cpp
    ll.add_symbol('pq_read', arrow_cpp.pq_read)
    ll.add_symbol('pq_write', arrow_cpp.pq_write)
    ll.add_symbol('pq_write_partitioned', arrow_cpp.pq_write_partitioned)


@intrinsic
def parquet_write_table_cpp(typingctx, filename_t, table_t, col_names_t,
    index_t, write_index, metadata_t, compression_t, is_parallel_t,
    write_range_index, start, stop, step, name, bucket_region):

    def codegen(context, builder, sig, args):
        mbpl__ojtn = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(32), lir.IntType(32),
            lir.IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer()])
        ojcs__vcae = cgutils.get_or_insert_function(builder.module,
            mbpl__ojtn, name='pq_write')
        builder.call(ojcs__vcae, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, table_t, col_names_t, index_t, types.
        boolean, types.voidptr, types.voidptr, types.boolean, types.boolean,
        types.int32, types.int32, types.int32, types.voidptr, types.voidptr
        ), codegen


@intrinsic
def parquet_write_table_partitioned_cpp(typingctx, filename_t, data_table_t,
    col_names_t, col_names_no_partitions_t, cat_table_t, part_col_idxs_t,
    num_part_col_t, compression_t, is_parallel_t, bucket_region):

    def codegen(context, builder, sig, args):
        mbpl__ojtn = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer()])
        ojcs__vcae = cgutils.get_or_insert_function(builder.module,
            mbpl__ojtn, name='pq_write_partitioned')
        builder.call(ojcs__vcae, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, data_table_t, col_names_t,
        col_names_no_partitions_t, cat_table_t, types.voidptr, types.int32,
        types.voidptr, types.boolean, types.voidptr), codegen
