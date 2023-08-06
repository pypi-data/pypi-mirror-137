"""IR node for the parquet data access"""
import numba
from numba.core import ir, ir_utils, typeinfer, types
import bodo
import bodo.ir.connector
from bodo.hiframes.table import Table, TableType
from bodo.transforms import distributed_analysis
from bodo.transforms.table_column_del_pass import get_live_column_nums_block, ir_extension_table_column_use, remove_dead_column_extensions


class ParquetReader(ir.Stmt):

    def __init__(self, file_name, df_out, col_names, col_indices, out_types,
        out_vars, loc, partition_names, storage_options, index_column_index,
        index_column_type):
        self.connector_typ = 'parquet'
        self.file_name = file_name
        self.df_out = df_out
        self.df_colnames = col_names
        self.col_indices = col_indices
        self.out_types = out_types
        self.original_out_types = out_types
        self.original_df_colnames = col_names
        self.out_vars = out_vars
        self.loc = loc
        self.partition_names = partition_names
        self.filters = None
        self.storage_options = storage_options
        self.index_column_index = index_column_index
        self.index_column_type = index_column_type
        self.type_usecol_offset = list(range(len(col_indices)))

    def __repr__(self):
        return (
            '({}) = ReadParquet({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'
            .format(self.df_out, self.file_name.name, self.df_colnames,
            self.col_indices, self.out_types, self.original_out_types, self
            .original_df_colnames, self.out_vars, self.partition_names,
            self.filters, self.storage_options, self.index_column_index,
            self.index_column_type, self.type_usecol_offset))


def remove_dead_pq(pq_node, lives_no_aliases, lives, arg_aliases, alias_map,
    func_ir, typemap):
    zuadw__kefx = pq_node.out_vars[0].name
    ixozj__kwg = pq_node.out_vars[1].name
    if zuadw__kefx not in lives and ixozj__kwg not in lives:
        return None
    elif zuadw__kefx not in lives:
        pq_node.col_indices = []
        pq_node.df_colnames = []
        pq_node.type_usecol_offset = []
    elif ixozj__kwg not in lives:
        pq_node.index_column_index = None
        pq_node.index_column_type = types.none
    return pq_node


def pq_remove_dead_column(pq_node, column_live_map, equiv_vars, typemap):
    assert len(pq_node.out_vars) == 2, 'invalid ParquetReader node'
    hyrm__rvb = pq_node.out_vars[0].name
    assert isinstance(typemap[hyrm__rvb], TableType
        ), 'Parquet Node Table must be a TableType'
    if pq_node.col_indices:
        dusxl__tgxiv, gatl__lxhzj = get_live_column_nums_block(column_live_map,
            equiv_vars, hyrm__rvb)
        dusxl__tgxiv = bodo.ir.connector.trim_extra_used_columns(dusxl__tgxiv,
            len(pq_node.col_indices))
        if not gatl__lxhzj and not dusxl__tgxiv:
            dusxl__tgxiv = [0]
        if not gatl__lxhzj and len(dusxl__tgxiv) != len(pq_node.
            type_usecol_offset):
            pq_node.type_usecol_offset = dusxl__tgxiv
            return True
    return False


def pq_table_column_use(pq_node, block_use_map, equiv_vars, typemap):
    return


numba.parfors.array_analysis.array_analysis_extensions[ParquetReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[ParquetReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[ParquetReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[ParquetReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[ParquetReader] = remove_dead_pq
numba.core.analysis.ir_extension_usedefs[ParquetReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[ParquetReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[ParquetReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[ParquetReader
    ] = bodo.ir.connector.build_connector_definitions
remove_dead_column_extensions[ParquetReader] = pq_remove_dead_column
ir_extension_table_column_use[ParquetReader] = pq_table_column_use
