from urllib.parse import parse_qsl, urlparse
import snowflake.connector
import bodo
from bodo.utils import tracing


def get_connection_params(conn_str):
    import json
    bvu__tpazc = urlparse(conn_str)
    ksow__burl = {}
    if bvu__tpazc.username:
        ksow__burl['user'] = bvu__tpazc.username
    if bvu__tpazc.password:
        ksow__burl['password'] = bvu__tpazc.password
    if bvu__tpazc.hostname:
        ksow__burl['account'] = bvu__tpazc.hostname
    if bvu__tpazc.port:
        ksow__burl['port'] = bvu__tpazc.port
    if bvu__tpazc.path:
        ybvtp__lejks = bvu__tpazc.path
        if ybvtp__lejks.startswith('/'):
            ybvtp__lejks = ybvtp__lejks[1:]
        jqojf__ddj, schema = ybvtp__lejks.split('/')
        ksow__burl['database'] = jqojf__ddj
        if schema:
            ksow__burl['schema'] = schema
    if bvu__tpazc.query:
        for bzj__scsdt, uuk__sqj in parse_qsl(bvu__tpazc.query):
            ksow__burl[bzj__scsdt] = uuk__sqj
            if bzj__scsdt == 'session_parameters':
                ksow__burl[bzj__scsdt] = json.loads(uuk__sqj)
    ksow__burl['application'] = 'bodo'
    return ksow__burl


class SnowflakeDataset(object):

    def __init__(self, batches, schema, conn):
        self.pieces = batches
        self._bodo_total_rows = 0
        for tfauc__amzg in batches:
            tfauc__amzg._bodo_num_rows = tfauc__amzg.rowcount
            self._bodo_total_rows += tfauc__amzg._bodo_num_rows
        self.schema = schema
        self.conn = conn


def get_dataset(query, conn_str):
    rxl__vmu = tracing.Event('get_snowflake_dataset')
    from mpi4py import MPI
    cgn__zabjn = MPI.COMM_WORLD
    gpqyg__spz = tracing.Event('snowflake_connect', is_parallel=False)
    pqq__yvhng = get_connection_params(conn_str)
    conn = snowflake.connector.connect(**pqq__yvhng)
    gpqyg__spz.finalize()
    if bodo.get_rank() == 0:
        ezat__robsw = conn.cursor()
        ezac__zxu = tracing.Event('get_schema', is_parallel=False)
        osbyy__ull = f'select * from ({query}) x LIMIT {100}'
        schema = ezat__robsw.execute(osbyy__ull).fetch_arrow_all().schema
        ezac__zxu.finalize()
        unrlb__oyxo = tracing.Event('execute_query', is_parallel=False)
        ezat__robsw.execute(query)
        unrlb__oyxo.finalize()
        batches = ezat__robsw.get_result_batches()
        cgn__zabjn.bcast((batches, schema))
    else:
        batches, schema = cgn__zabjn.bcast(None)
    hxtsx__tjzth = SnowflakeDataset(batches, schema, conn)
    rxl__vmu.finalize()
    return hxtsx__tjzth
