"""
Implementation of pd.read_sql in BODO.
We piggyback on the pandas implementation. Future plan is to have a faster
version for this task.
"""
import numba
import numpy as np
import pandas as pd
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, replace_arg_nodes
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.ir.csv_ext import _get_dtype_str
from bodo.libs.array import delete_table, info_from_table, info_to_array, table_type
from bodo.libs.distributed_api import bcast, bcast_scalar
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.utils.typing import BodoError
from bodo.utils.utils import check_and_propagate_cpp_exception, sanitize_varname
MPI_ROOT = 0


class SqlReader(ir.Stmt):

    def __init__(self, sql_request, connection, df_out, df_colnames,
        out_vars, out_types, converted_colnames, db_type, loc):
        self.connector_typ = 'sql'
        self.sql_request = sql_request
        self.connection = connection
        self.df_out = df_out
        self.df_colnames = df_colnames
        self.out_vars = out_vars
        self.out_types = out_types
        self.converted_colnames = converted_colnames
        self.loc = loc
        self.limit = req_limit(sql_request)
        self.db_type = db_type
        self.filters = None

    def __repr__(self):
        return (
            '{} = ReadSql(sql_request={}, connection={}, col_names={}, types={}, vars={}, limit={})'
            .format(self.df_out, self.sql_request, self.connection, self.
            df_colnames, self.out_types, self.out_vars, self.limit))


def remove_dead_sql(sql_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    niazl__lqj = []
    vupo__nex = []
    swsh__olw = []
    for todi__ftgb, kejq__kdbv in enumerate(sql_node.out_vars):
        if kejq__kdbv.name in lives:
            niazl__lqj.append(sql_node.df_colnames[todi__ftgb])
            vupo__nex.append(sql_node.out_vars[todi__ftgb])
            swsh__olw.append(sql_node.out_types[todi__ftgb])
    sql_node.df_colnames = niazl__lqj
    sql_node.out_vars = vupo__nex
    sql_node.out_types = swsh__olw
    if len(sql_node.out_vars) == 0:
        return None
    return sql_node


def sql_distributed_run(sql_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    parallel = False
    if array_dists is not None:
        parallel = True
        for zjb__kwsf in sql_node.out_vars:
            if array_dists[zjb__kwsf.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                zjb__kwsf.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    bhh__bam = len(sql_node.out_vars)
    tyqb__oud = ', '.join('arr' + str(todi__ftgb) for todi__ftgb in range(
        bhh__bam))
    ofw__jqmrc, nxxix__xvow = bodo.ir.connector.generate_filter_map(sql_node
        .filters)
    ppe__azfjz = ', '.join(ofw__jqmrc.values())
    qhk__uqajb = f'def sql_impl(sql_request, conn, {ppe__azfjz}):\n'
    if sql_node.filters:
        dsowh__kgh = []
        for aqzfb__qxli in sql_node.filters:
            isy__gxfj = [' '.join(['(', idau__pxdc[0], idau__pxdc[1], '{' +
                ofw__jqmrc[idau__pxdc[2].name] + '}' if isinstance(
                idau__pxdc[2], ir.Var) else idau__pxdc[2], ')']) for
                idau__pxdc in aqzfb__qxli]
            dsowh__kgh.append(' ( ' + ' AND '.join(isy__gxfj) + ' ) ')
        qqasa__epe = ' WHERE ' + ' OR '.join(dsowh__kgh)
        for todi__ftgb, qgtb__lfb in enumerate(ofw__jqmrc.values()):
            qhk__uqajb += f'    {qgtb__lfb} = get_sql_literal({qgtb__lfb})\n'
        qhk__uqajb += f'    sql_request = f"{{sql_request}} {qqasa__epe}"\n'
    qhk__uqajb += '    ({},) = _sql_reader_py(sql_request, conn)\n'.format(
        tyqb__oud)
    retu__bbn = {}
    exec(qhk__uqajb, {}, retu__bbn)
    oxrh__atbuk = retu__bbn['sql_impl']
    pkd__ncx = _gen_sql_reader_py(sql_node.df_colnames, sql_node.out_types,
        typingctx, targetctx, sql_node.db_type, sql_node.limit, parallel)
    njf__dayho = compile_to_numba_ir(oxrh__atbuk, {'_sql_reader_py':
        pkd__ncx, 'bcast_scalar': bcast_scalar, 'bcast': bcast,
        'get_sql_literal': _get_snowflake_sql_literal}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(string_type, string_type) + tuple(
        typemap[zjb__kwsf.name] for zjb__kwsf in nxxix__xvow), typemap=
        typemap, calltypes=calltypes).blocks.popitem()[1]
    if sql_node.db_type == 'snowflake':
        mfkq__cvyk = [(gpqag__lgmdv.upper() if gpqag__lgmdv in sql_node.
            converted_colnames else gpqag__lgmdv) for gpqag__lgmdv in
            sql_node.df_colnames]
        xteud__dbrqq = ', '.join([f'"{gpqag__lgmdv}"' for gpqag__lgmdv in
            mfkq__cvyk])
    else:
        xteud__dbrqq = ', '.join(sql_node.df_colnames)
    ihzzc__ykvze = ('SELECT ' + xteud__dbrqq + ' FROM (' + sql_node.
        sql_request + ') as TEMP')
    replace_arg_nodes(njf__dayho, [ir.Const(ihzzc__ykvze, sql_node.loc), ir
        .Const(sql_node.connection, sql_node.loc)] + nxxix__xvow)
    hlmoa__hwug = njf__dayho.body[:-3]
    for todi__ftgb in range(len(sql_node.out_vars)):
        hlmoa__hwug[-len(sql_node.out_vars) + todi__ftgb
            ].target = sql_node.out_vars[todi__ftgb]
    return hlmoa__hwug


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal(filter_value):
    mwnuf__swyt = types.unliteral(filter_value)
    if mwnuf__swyt == types.unicode_type:
        return lambda filter_value: f'$${filter_value}$$'
    elif isinstance(mwnuf__swyt, (types.Integer, types.Float)
        ) or filter_value == types.bool_:
        return lambda filter_value: str(filter_value)
    elif mwnuf__swyt == bodo.pd_timestamp_type:

        def impl(filter_value):
            ntewl__zev = filter_value.nanosecond
            slkz__pdug = ''
            if ntewl__zev < 10:
                slkz__pdug = '00'
            elif ntewl__zev < 100:
                slkz__pdug = '0'
            return (
                f"timestamp '{filter_value.strftime('%Y-%m-%d %H:%M:%S.%f')}{slkz__pdug}{ntewl__zev}'"
                )
        return impl
    elif mwnuf__swyt == bodo.datetime_date_type:
        return (lambda filter_value:
            f"date '{filter_value.strftime('%Y-%m-%d')}'")
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported type {mwnuf__swyt} used in filter pushdown.'
            )


numba.parfors.array_analysis.array_analysis_extensions[SqlReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[SqlReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[SqlReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[SqlReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[SqlReader] = remove_dead_sql
numba.core.analysis.ir_extension_usedefs[SqlReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[SqlReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[SqlReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[SqlReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[SqlReader] = sql_distributed_run
compiled_funcs = []


@numba.njit
def sqlalchemy_check():
    with numba.objmode():
        sqlalchemy_check_()


def sqlalchemy_check_():
    try:
        import sqlalchemy
    except ImportError as nsvsu__qavzr:
        gbvc__owdou = (
            "Using URI string without sqlalchemy installed. sqlalchemy can be installed by calling 'conda install -c conda-forge sqlalchemy'."
            )
        raise BodoError(gbvc__owdou)


def req_limit(sql_request):
    import re
    cdv__qions = re.compile('LIMIT\\s+(\\d+)\\s*$', re.IGNORECASE)
    bvlj__tiei = cdv__qions.search(sql_request)
    if bvlj__tiei:
        return int(bvlj__tiei.group(1))
    else:
        return None


def _gen_sql_reader_py(col_names, col_typs, typingctx, targetctx, db_type,
    limit, parallel):
    vnz__psyiq = [sanitize_varname(bgxp__uflby) for bgxp__uflby in col_names]
    umdt__ndt = ["{}='{}'".format(bsouy__sapra, _get_dtype_str(htgr__qppok)
        ) for bsouy__sapra, htgr__qppok in zip(vnz__psyiq, col_typs)]
    if bodo.sql_access_method == 'multiple_access_by_block':
        qhk__uqajb = 'def sql_reader_py(sql_request,conn):\n'
        qhk__uqajb += '  sqlalchemy_check()\n'
        qhk__uqajb += '  rank = bodo.libs.distributed_api.get_rank()\n'
        qhk__uqajb += '  n_pes = bodo.libs.distributed_api.get_size()\n'
        qhk__uqajb += '  with objmode({}):\n'.format(', '.join(umdt__ndt))
        qhk__uqajb += '    list_df_block = []\n'
        qhk__uqajb += '    block_size = 50000\n'
        qhk__uqajb += '    iter = 0\n'
        qhk__uqajb += '    while(True):\n'
        qhk__uqajb += '      offset = (iter * n_pes + rank) * block_size\n'
        qhk__uqajb += """      sql_cons = 'select * from (' + sql_request + ') x LIMIT ' + str(block_size) + ' OFFSET ' + str(offset)
"""
        qhk__uqajb += '      df_block = pd.read_sql(sql_cons, conn)\n'
        qhk__uqajb += '      if df_block.size == 0:\n'
        qhk__uqajb += '        break\n'
        qhk__uqajb += '      list_df_block.append(df_block)\n'
        qhk__uqajb += '      iter += 1\n'
        qhk__uqajb += '    df_ret = pd.concat(list_df_block)\n'
        for bsouy__sapra, mlkmh__yqwn in zip(vnz__psyiq, col_names):
            qhk__uqajb += "    {} = df_ret['{}'].values\n".format(bsouy__sapra,
                mlkmh__yqwn)
        qhk__uqajb += '  return ({},)\n'.format(', '.join(sbzj__rikc for
            sbzj__rikc in vnz__psyiq))
    if bodo.sql_access_method == 'multiple_access_nb_row_first':
        qhk__uqajb = 'def sql_reader_py(sql_request, conn):\n'
        if db_type == 'snowflake':
            jsqsf__izr = {}
            for todi__ftgb, kkxv__xgdse in enumerate(col_typs):
                jsqsf__izr[f'col_{todi__ftgb}_type'] = kkxv__xgdse
            qhk__uqajb += (
                f"  ev = bodo.utils.tracing.Event('read_snowflake', {parallel})\n"
                )

            def is_nullable(typ):
                return bodo.utils.utils.is_array_typ(typ, False
                    ) and not isinstance(typ, types.Array)
            sjoz__lrpp = [int(is_nullable(kkxv__xgdse)) for kkxv__xgdse in
                col_typs]
            qhk__uqajb += f"""  out_table = snowflake_read(unicode_to_utf8(sql_request), unicode_to_utf8(conn), {parallel}, {len(col_names)}, np.array({sjoz__lrpp}, dtype=np.int32).ctypes)
"""
            qhk__uqajb += '  check_and_propagate_cpp_exception()\n'
            for todi__ftgb, hezes__vxi in enumerate(vnz__psyiq):
                qhk__uqajb += f"""  {hezes__vxi} = info_to_array(info_from_table(out_table, {todi__ftgb}), col_{todi__ftgb}_type)
"""
            qhk__uqajb += '  delete_table(out_table)\n'
            qhk__uqajb += f'  ev.finalize()\n'
        else:
            qhk__uqajb += '  sqlalchemy_check()\n'
            if parallel:
                qhk__uqajb += '  rank = bodo.libs.distributed_api.get_rank()\n'
                if limit is not None:
                    qhk__uqajb += f'  nb_row = {limit}\n'
                else:
                    qhk__uqajb += '  with objmode(nb_row="int64"):\n'
                    qhk__uqajb += f'     if rank == {MPI_ROOT}:\n'
                    qhk__uqajb += """         sql_cons = 'select count(*) from (' + sql_request + ') x'
"""
                    qhk__uqajb += (
                        '         frame = pd.read_sql(sql_cons, conn)\n')
                    qhk__uqajb += '         nb_row = frame.iat[0,0]\n'
                    qhk__uqajb += '     else:\n'
                    qhk__uqajb += '         nb_row = 0\n'
                    qhk__uqajb += '  nb_row = bcast_scalar(nb_row)\n'
                qhk__uqajb += '  with objmode({}):\n'.format(', '.join(
                    umdt__ndt))
                qhk__uqajb += """    offset, limit = bodo.libs.distributed_api.get_start_count(nb_row)
"""
                qhk__uqajb += f"""    sql_cons = 'select {', '.join(col_names)} from (' + sql_request + ') x LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
"""
                qhk__uqajb += '    df_ret = pd.read_sql(sql_cons, conn)\n'
            else:
                qhk__uqajb += '  with objmode({}):\n'.format(', '.join(
                    umdt__ndt))
                qhk__uqajb += '    df_ret = pd.read_sql(sql_request, conn)\n'
            for bsouy__sapra, mlkmh__yqwn in zip(vnz__psyiq, col_names):
                qhk__uqajb += "    {} = df_ret['{}'].values\n".format(
                    bsouy__sapra, mlkmh__yqwn)
        qhk__uqajb += '  return ({},)\n'.format(', '.join(sbzj__rikc for
            sbzj__rikc in vnz__psyiq))
    gcjmx__yxsis = {'bodo': bodo}
    if db_type == 'snowflake':
        gcjmx__yxsis.update(jsqsf__izr)
        gcjmx__yxsis.update({'np': np, 'unicode_to_utf8': unicode_to_utf8,
            'check_and_propagate_cpp_exception':
            check_and_propagate_cpp_exception, 'snowflake_read':
            _snowflake_read, 'info_to_array': info_to_array,
            'info_from_table': info_from_table, 'delete_table': delete_table})
    else:
        gcjmx__yxsis.update({'sqlalchemy_check': sqlalchemy_check, 'pd': pd,
            'objmode': objmode, 'bcast_scalar': bcast_scalar})
    retu__bbn = {}
    exec(qhk__uqajb, gcjmx__yxsis, retu__bbn)
    pkd__ncx = retu__bbn['sql_reader_py']
    udwy__rlji = numba.njit(pkd__ncx)
    compiled_funcs.append(udwy__rlji)
    return udwy__rlji


_snowflake_read = types.ExternalFunction('snowflake_read', table_type(types
    .voidptr, types.voidptr, types.boolean, types.int64, types.voidptr))
import llvmlite.binding as ll
from bodo.io import arrow_cpp
ll.add_symbol('snowflake_read', arrow_cpp.snowflake_read)
