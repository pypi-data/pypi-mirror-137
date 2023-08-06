"""
Common IR extension functions for connectors such as CSV, Parquet and JSON readers.
"""
from collections import defaultdict
import numba
from numba.core import ir, types
from numba.core.ir_utils import replace_vars_inner, visit_vars_inner
from numba.extending import box, models, register_model
from bodo.hiframes.table import TableType
from bodo.transforms.distributed_analysis import Distribution
from bodo.utils.utils import debug_prints


def connector_array_analysis(node, equiv_set, typemap, array_analysis):
    lkkwp__kev = []
    assert len(node.out_vars) > 0, 'empty {} in array analysis'.format(node
        .connector_typ)
    if node.connector_typ == 'csv' and node.chunksize is not None:
        return [], []
    fmtz__qjnl = []
    for tle__ywj in node.out_vars:
        typ = typemap[tle__ywj.name]
        if typ == types.none:
            continue
        rbhzl__jsn = array_analysis._gen_shape_call(equiv_set, tle__ywj,
            typ.ndim, None, lkkwp__kev)
        equiv_set.insert_equiv(tle__ywj, rbhzl__jsn)
        fmtz__qjnl.append(rbhzl__jsn[0])
        equiv_set.define(tle__ywj, set())
    if len(fmtz__qjnl) > 1:
        equiv_set.insert_equiv(*fmtz__qjnl)
    return [], lkkwp__kev


def connector_distributed_analysis(node, array_dists):
    from bodo.ir.sql_ext import SqlReader
    if isinstance(node, SqlReader) and node.limit is not None:
        sam__oowy = Distribution.OneD_Var
    else:
        sam__oowy = Distribution.OneD
    for wfm__zhy in node.out_vars:
        if wfm__zhy.name in array_dists:
            sam__oowy = Distribution(min(sam__oowy.value, array_dists[
                wfm__zhy.name].value))
    for wfm__zhy in node.out_vars:
        array_dists[wfm__zhy.name] = sam__oowy


def connector_typeinfer(node, typeinferer):
    if node.connector_typ == 'csv':
        if node.chunksize is not None:
            typeinferer.lock_type(node.out_vars[0].name, node.out_types[0],
                loc=node.loc)
        else:
            typeinferer.lock_type(node.out_vars[0].name, TableType(tuple(
                node.out_types)), loc=node.loc)
            typeinferer.lock_type(node.out_vars[1].name, node.
                index_column_typ, loc=node.loc)
        return
    if node.connector_typ == 'parquet':
        typeinferer.lock_type(node.out_vars[0].name, TableType(tuple(node.
            out_types)), loc=node.loc)
        typeinferer.lock_type(node.out_vars[1].name, node.index_column_type,
            loc=node.loc)
        return
    for tle__ywj, typ in zip(node.out_vars, node.out_types):
        typeinferer.lock_type(tle__ywj.name, typ, loc=node.loc)


def visit_vars_connector(node, callback, cbdata):
    if debug_prints():
        print('visiting {} vars for:'.format(node.connector_typ), node)
        print('cbdata: ', sorted(cbdata.items()))
    jwl__gjvb = []
    for tle__ywj in node.out_vars:
        jfk__uuw = visit_vars_inner(tle__ywj, callback, cbdata)
        jwl__gjvb.append(jfk__uuw)
    node.out_vars = jwl__gjvb
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = visit_vars_inner(node.file_name, callback, cbdata)
    if node.connector_typ == 'csv':
        node.nrows = visit_vars_inner(node.nrows, callback, cbdata)
        node.skiprows = visit_vars_inner(node.skiprows, callback, cbdata)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for iasig__zzhet in node.filters:
            for bps__oga in range(len(iasig__zzhet)):
                val = iasig__zzhet[bps__oga]
                iasig__zzhet[bps__oga] = val[0], val[1], visit_vars_inner(val
                    [2], callback, cbdata)


def connector_usedefs(node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    def_set.update({wfm__zhy.name for wfm__zhy in node.out_vars})
    if node.connector_typ in ('csv', 'parquet', 'json'):
        use_set.add(node.file_name.name)
    if node.connector_typ == 'csv':
        if isinstance(node.nrows, numba.core.ir.Var):
            use_set.add(node.nrows.name)
        if isinstance(node.skiprows, numba.core.ir.Var):
            use_set.add(node.skiprows.name)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for cjp__zqwt in node.filters:
            for wfm__zhy in cjp__zqwt:
                if isinstance(wfm__zhy[2], ir.Var):
                    use_set.add(wfm__zhy[2].name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


def get_copies_connector(node, typemap):
    mitha__uck = set(wfm__zhy.name for wfm__zhy in node.out_vars)
    return set(), mitha__uck


def apply_copies_connector(node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    jwl__gjvb = []
    for tle__ywj in node.out_vars:
        jfk__uuw = replace_vars_inner(tle__ywj, var_dict)
        jwl__gjvb.append(jfk__uuw)
    node.out_vars = jwl__gjvb
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = replace_vars_inner(node.file_name, var_dict)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for iasig__zzhet in node.filters:
            for bps__oga in range(len(iasig__zzhet)):
                val = iasig__zzhet[bps__oga]
                iasig__zzhet[bps__oga] = val[0], val[1], replace_vars_inner(val
                    [2], var_dict)
    if node.connector_typ == 'csv':
        node.nrows = replace_vars_inner(node.nrows, var_dict)
        node.skiprows = replace_vars_inner(node.skiprows, var_dict)


def build_connector_definitions(node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for tle__ywj in node.out_vars:
        gzgue__val = definitions[tle__ywj.name]
        if node not in gzgue__val:
            gzgue__val.append(node)
    return definitions


def generate_filter_map(filters):
    if filters:
        fojp__auwz = []
        wcwb__pnv = [wfm__zhy[2] for cjp__zqwt in filters for wfm__zhy in
            cjp__zqwt]
        qkxh__dna = set()
        for ecml__otxe in wcwb__pnv:
            if isinstance(ecml__otxe, ir.Var):
                if ecml__otxe.name not in qkxh__dna:
                    fojp__auwz.append(ecml__otxe)
                qkxh__dna.add(ecml__otxe.name)
        return {wfm__zhy.name: f'f{bps__oga}' for bps__oga, wfm__zhy in
            enumerate(fojp__auwz)}, fojp__auwz
    else:
        return {}, []


class StreamReaderType(types.Opaque):

    def __init__(self):
        super(StreamReaderType, self).__init__(name='StreamReaderType')


stream_reader_type = StreamReaderType()
register_model(StreamReaderType)(models.OpaqueModel)


@box(StreamReaderType)
def box_stream_reader(typ, val, c):
    c.pyapi.incref(val)
    return val


def trim_extra_used_columns(used_columns, num_columns):
    wnv__nufy = len(used_columns)
    for bps__oga in range(len(used_columns) - 1, -1, -1):
        if used_columns[bps__oga] < num_columns:
            break
        wnv__nufy = bps__oga
    return used_columns[:wnv__nufy]
