import numba
import numpy as np
import pandas as pd
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, replace_arg_nodes
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.utils.utils import check_java_installation
from bodo.utils.utils import sanitize_varname


class JsonReader(ir.Stmt):

    def __init__(self, df_out, loc, out_vars, out_types, file_name,
        df_colnames, orient, convert_dates, precise_float, lines, compression):
        self.connector_typ = 'json'
        self.df_out = df_out
        self.loc = loc
        self.out_vars = out_vars
        self.out_types = out_types
        self.file_name = file_name
        self.df_colnames = df_colnames
        self.orient = orient
        self.convert_dates = convert_dates
        self.precise_float = precise_float
        self.lines = lines
        self.compression = compression

    def __repr__(self):
        return ('{} = ReadJson(file={}, col_names={}, types={}, vars={})'.
            format(self.df_out, self.file_name, self.df_colnames, self.
            out_types, self.out_vars))


import llvmlite.binding as ll
from bodo.io import json_cpp
ll.add_symbol('json_file_chunk_reader', json_cpp.json_file_chunk_reader)
json_file_chunk_reader = types.ExternalFunction('json_file_chunk_reader',
    bodo.ir.connector.stream_reader_type(types.voidptr, types.bool_, types.
    bool_, types.int64, types.voidptr, types.voidptr))


def remove_dead_json(json_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    klrk__fjag = []
    fzxr__ipa = []
    gxjs__biyz = []
    for dwkhl__txjub, xija__yjx in enumerate(json_node.out_vars):
        if xija__yjx.name in lives:
            klrk__fjag.append(json_node.df_colnames[dwkhl__txjub])
            fzxr__ipa.append(json_node.out_vars[dwkhl__txjub])
            gxjs__biyz.append(json_node.out_types[dwkhl__txjub])
    json_node.df_colnames = klrk__fjag
    json_node.out_vars = fzxr__ipa
    json_node.out_types = gxjs__biyz
    if len(json_node.out_vars) == 0:
        return None
    return json_node


def json_distributed_run(json_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    parallel = False
    if array_dists is not None:
        parallel = True
        for koj__gityv in json_node.out_vars:
            if array_dists[koj__gityv.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                koj__gityv.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    ythlt__hphfa = len(json_node.out_vars)
    qehzi__oxaay = ', '.join('arr' + str(dwkhl__txjub) for dwkhl__txjub in
        range(ythlt__hphfa))
    fncvg__jqz = 'def json_impl(fname):\n'
    fncvg__jqz += '    ({},) = _json_reader_py(fname)\n'.format(qehzi__oxaay)
    gir__wjnif = {}
    exec(fncvg__jqz, {}, gir__wjnif)
    wbb__lszvw = gir__wjnif['json_impl']
    htyue__bvp = _gen_json_reader_py(json_node.df_colnames, json_node.
        out_types, typingctx, targetctx, parallel, json_node.orient,
        json_node.convert_dates, json_node.precise_float, json_node.lines,
        json_node.compression)
    uaobi__afmz = compile_to_numba_ir(wbb__lszvw, {'_json_reader_py':
        htyue__bvp}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type,), typemap=typemap, calltypes=calltypes).blocks.popitem()[1
        ]
    replace_arg_nodes(uaobi__afmz, [json_node.file_name])
    araxv__csoof = uaobi__afmz.body[:-3]
    for dwkhl__txjub in range(len(json_node.out_vars)):
        araxv__csoof[-len(json_node.out_vars) + dwkhl__txjub
            ].target = json_node.out_vars[dwkhl__txjub]
    return araxv__csoof


numba.parfors.array_analysis.array_analysis_extensions[JsonReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[JsonReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[JsonReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[JsonReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[JsonReader] = remove_dead_json
numba.core.analysis.ir_extension_usedefs[JsonReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[JsonReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[JsonReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[JsonReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[JsonReader] = json_distributed_run
compiled_funcs = []


def _gen_json_reader_py(col_names, col_typs, typingctx, targetctx, parallel,
    orient, convert_dates, precise_float, lines, compression):
    cpg__rtjaq = [sanitize_varname(etg__ryy) for etg__ryy in col_names]
    hnhpd__pyr = ', '.join(str(dwkhl__txjub) for dwkhl__txjub, mmm__alde in
        enumerate(col_typs) if mmm__alde.dtype == types.NPDatetime('ns'))
    eyo__xiqu = ', '.join(["{}='{}'".format(cep__mmw, bodo.ir.csv_ext.
        _get_dtype_str(mmm__alde)) for cep__mmw, mmm__alde in zip(
        cpg__rtjaq, col_typs)])
    ffej__rhcj = ', '.join(["'{}':{}".format(oank__ubfe, bodo.ir.csv_ext.
        _get_pd_dtype_str(mmm__alde)) for oank__ubfe, mmm__alde in zip(
        col_names, col_typs)])
    if compression is None:
        compression = 'uncompressed'
    fncvg__jqz = 'def json_reader_py(fname):\n'
    fncvg__jqz += '  check_java_installation(fname)\n'
    fncvg__jqz += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    fncvg__jqz += (
        '  f_reader = bodo.ir.json_ext.json_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    fncvg__jqz += (
        """    {}, {}, -1, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region) )
"""
        .format(lines, parallel, compression))
    fncvg__jqz += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    fncvg__jqz += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    fncvg__jqz += "      raise FileNotFoundError('File does not exist')\n"
    fncvg__jqz += '  with objmode({}):\n'.format(eyo__xiqu)
    fncvg__jqz += "    df = pd.read_json(f_reader, orient='{}',\n".format(
        orient)
    fncvg__jqz += '       convert_dates = {}, \n'.format(convert_dates)
    fncvg__jqz += '       precise_float={}, \n'.format(precise_float)
    fncvg__jqz += '       lines={}, \n'.format(lines)
    fncvg__jqz += '       dtype={{{}}},\n'.format(ffej__rhcj)
    fncvg__jqz += '       )\n'
    for cep__mmw, oank__ubfe in zip(cpg__rtjaq, col_names):
        fncvg__jqz += '    if len(df) > 0:\n'
        fncvg__jqz += "        {} = df['{}'].values\n".format(cep__mmw,
            oank__ubfe)
        fncvg__jqz += '    else:\n'
        fncvg__jqz += '        {} = np.array([])\n'.format(cep__mmw)
    fncvg__jqz += '  return ({},)\n'.format(', '.join(jqxua__vsg for
        jqxua__vsg in cpg__rtjaq))
    eayn__tbu = globals()
    gir__wjnif = {}
    exec(fncvg__jqz, eayn__tbu, gir__wjnif)
    htyue__bvp = gir__wjnif['json_reader_py']
    vlo__svb = numba.njit(htyue__bvp)
    compiled_funcs.append(vlo__svb)
    return vlo__svb
