"""
Implement pd.DataFrame typing and data model handling.
"""
import json
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import AbstractTemplate, bound_function, infer_global, signature
from numba.cpython.listobj import ListInstance
from numba.extending import infer_getattr, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.hiframes.pd_index_ext import HeterogeneousIndexType, NumericIndexType, RangeIndexType, is_pd_index_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.hiframes.series_indexing import SeriesIlocType
from bodo.hiframes.table import Table, TableType, get_table_data, set_table_data_codegen
from bodo.io import json_cpp
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_info_decref_array, delete_table, delete_table_decref_arrays, info_from_table, info_to_array, py_table_to_cpp_table, shuffle_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.distributed_api import bcast_scalar
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import str_arr_from_sequence, string_array_type
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.conversion import index_to_array
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.transform import gen_const_tup, get_const_func_output_type, get_const_tup_vals
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, dtype_to_array_type, get_index_data_arr_types, get_literal_value, get_overload_const, get_overload_const_bool, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_udf_error_msg, get_udf_out_arr_type, is_heterogeneous_tuple_type, is_iterable_type, is_literal_type, is_overload_bool, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_str, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_tuple_like_type, raise_bodo_error, to_nullable_type
from bodo.utils.utils import is_null_pointer
_json_write = types.ExternalFunction('json_write', types.void(types.voidptr,
    types.voidptr, types.int64, types.int64, types.bool_, types.bool_,
    types.voidptr))
ll.add_symbol('json_write', json_cpp.json_write)


class DataFrameType(types.ArrayCompatible):
    ndim = 2

    def __init__(self, data=None, index=None, columns=None, dist=None,
        is_table_format=False):
        from bodo.transforms.distributed_analysis import Distribution
        self.data = data
        if index is None:
            index = RangeIndexType(types.none)
        self.index = index
        self.columns = columns
        dist = Distribution.OneD_Var if dist is None else dist
        self.dist = dist
        self.is_table_format = is_table_format
        if columns is None:
            assert is_table_format, 'Determining columns at runtime is only supported for DataFrame with table format'
            self.table_type = TableType(tuple(data[:-1]), True)
        else:
            self.table_type = TableType(data) if is_table_format else None
        super(DataFrameType, self).__init__(name=
            f'dataframe({data}, {index}, {columns}, {dist}, {is_table_format})'
            )

    def __str__(self):
        if not self.has_runtime_cols and len(self.columns) > 20:
            gbm__qmo = f'{len(self.data)} columns of types {set(self.data)}'
            ophct__okecp = (
                f"('{self.columns[0]}', '{self.columns[1]}', ..., '{self.columns[-1]}')"
                )
            return (
                f'dataframe({gbm__qmo}, {self.index}, {ophct__okecp}, {self.dist}, {self.is_table_format})'
                )
        return super().__str__()

    def copy(self, data=None, index=None, columns=None, dist=None,
        is_table_format=None):
        if data is None:
            data = self.data
        if columns is None:
            columns = self.columns
        if index is None:
            index = self.index
        if dist is None:
            dist = self.dist
        if is_table_format is None:
            is_table_format = self.is_table_format
        return DataFrameType(data, index, columns, dist, is_table_format)

    @property
    def has_runtime_cols(self):
        return self.columns is None

    @property
    def runtime_colname_typ(self):
        return self.data[-1] if self.has_runtime_cols else None

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    @property
    def key(self):
        return (self.data, self.index, self.columns, self.dist, self.
            is_table_format)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    def unify(self, typingctx, other):
        from bodo.transforms.distributed_analysis import Distribution
        if (isinstance(other, DataFrameType) and len(other.data) == len(
            self.data) and other.columns == self.columns and other.
            has_runtime_cols == self.has_runtime_cols):
            aes__bxu = (self.index if self.index == other.index else self.
                index.unify(typingctx, other.index))
            data = tuple(lxv__insej.unify(typingctx, oeuk__qit) if 
                lxv__insej != oeuk__qit else lxv__insej for lxv__insej,
                oeuk__qit in zip(self.data, other.data))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if aes__bxu is not None and None not in data:
                return DataFrameType(data, aes__bxu, self.columns, dist,
                    self.is_table_format)
        if isinstance(other, DataFrameType) and len(self.data
            ) == 0 and not self.has_runtime_cols:
            return other

    def can_convert_to(self, typingctx, other):
        from numba.core.typeconv import Conversion
        if (isinstance(other, DataFrameType) and self.data == other.data and
            self.index == other.index and self.columns == other.columns and
            self.dist != other.dist and self.has_runtime_cols == other.
            has_runtime_cols):
            return Conversion.safe

    def is_precise(self):
        return all(lxv__insej.is_precise() for lxv__insej in self.data
            ) and self.index.is_precise()

    def replace_col_type(self, col_name, new_type):
        if col_name not in self.columns:
            raise ValueError(
                f"DataFrameType.replace_col_type replaced column must be found in the DataFrameType. '{col_name}' not found in DataFrameType with columns {self.columns}"
                )
        rvvf__yqtoj = self.columns.index(col_name)
        hwz__mazq = tuple(list(self.data[:rvvf__yqtoj]) + [new_type] + list
            (self.data[rvvf__yqtoj + 1:]))
        return DataFrameType(hwz__mazq, self.index, self.columns, self.dist,
            self.is_table_format)


def check_runtime_cols_unsupported(df, func_name):
    if isinstance(df, DataFrameType) and df.has_runtime_cols:
        raise BodoError(
            f'{func_name} on DataFrames with columns determined at runtime is not yet supported. Please return the DataFrame to regular Python to update typing information.'
            )


class DataFramePayloadType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        super(DataFramePayloadType, self).__init__(name=
            f'DataFramePayloadType({df_type})')

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(DataFramePayloadType)
class DataFramePayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        data_typ = types.Tuple(fe_type.df_type.data)
        if fe_type.df_type.is_table_format:
            data_typ = types.Tuple([fe_type.df_type.table_type])
        zvs__kdpth = [('data', data_typ), ('index', fe_type.df_type.index),
            ('parent', types.pyobject)]
        if fe_type.df_type.has_runtime_cols:
            zvs__kdpth.append(('columns', fe_type.df_type.runtime_colname_typ))
        super(DataFramePayloadModel, self).__init__(dmm, fe_type, zvs__kdpth)


@register_model(DataFrameType)
class DataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = DataFramePayloadType(fe_type)
        zvs__kdpth = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(DataFrameModel, self).__init__(dmm, fe_type, zvs__kdpth)


make_attribute_wrapper(DataFrameType, 'meminfo', '_meminfo')


@infer_getattr
class DataFrameAttribute(OverloadedKeyAttributeTemplate):
    key = DataFrameType

    @bound_function('df.head')
    def resolve_head(self, df, args, kws):
        func_name = 'DataFrame.head'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        mce__xvhf = 'n',
        ujv__sfwfp = {'n': 5}
        xcljr__gym, pkasr__mbdy = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, mce__xvhf, ujv__sfwfp)
        buys__ivy = pkasr__mbdy[0]
        if not is_overload_int(buys__ivy):
            raise BodoError(f"{func_name}(): 'n' must be an Integer")
        gpvx__eqrgz = df.copy(is_table_format=False)
        return gpvx__eqrgz(*pkasr__mbdy).replace(pysig=xcljr__gym)

    @bound_function('df.corr')
    def resolve_corr(self, df, args, kws):
        func_name = 'DataFrame.corr'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        sho__zku = (df,) + args
        mce__xvhf = 'df', 'method', 'min_periods'
        ujv__sfwfp = {'method': 'pearson', 'min_periods': 1}
        gcnz__irch = 'method',
        xcljr__gym, pkasr__mbdy = bodo.utils.typing.fold_typing_args(func_name,
            sho__zku, kws, mce__xvhf, ujv__sfwfp, gcnz__irch)
        lbcww__rqz = pkasr__mbdy[2]
        if not is_overload_int(lbcww__rqz):
            raise BodoError(f"{func_name}(): 'min_periods' must be an Integer")
        sgl__kggk = []
        zmbe__apzz = []
        for jil__onn, gtu__hyvdd in zip(df.columns, df.data):
            if bodo.utils.typing._is_pandas_numeric_dtype(gtu__hyvdd.dtype):
                sgl__kggk.append(jil__onn)
                zmbe__apzz.append(types.Array(types.float64, 1, 'A'))
        if len(sgl__kggk) == 0:
            raise_bodo_error('DataFrame.corr(): requires non-empty dataframe')
        zmbe__apzz = tuple(zmbe__apzz)
        sgl__kggk = tuple(sgl__kggk)
        index_typ = bodo.utils.typing.type_col_to_index(sgl__kggk)
        gpvx__eqrgz = DataFrameType(zmbe__apzz, index_typ, sgl__kggk)
        return gpvx__eqrgz(*pkasr__mbdy).replace(pysig=xcljr__gym)

    @bound_function('df.pipe', no_unliteral=True)
    def resolve_pipe(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.pipe()')
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, df, args,
            kws, 'DataFrame')

    @bound_function('df.apply', no_unliteral=True)
    def resolve_apply(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.apply()')
        kws = dict(kws)
        vbqaj__vaf = args[0] if len(args) > 0 else kws.pop('func', None)
        axis = args[1] if len(args) > 1 else kws.pop('axis', types.literal(0))
        mlqci__xil = args[2] if len(args) > 2 else kws.pop('raw', types.
            literal(False))
        lrwsy__ybhrf = args[3] if len(args) > 3 else kws.pop('result_type',
            types.none)
        vqda__hmfmy = args[4] if len(args) > 4 else kws.pop('args', types.
            Tuple([]))
        nhmzs__rirc = dict(raw=mlqci__xil, result_type=lrwsy__ybhrf)
        vtyw__aeinw = dict(raw=False, result_type=None)
        check_unsupported_args('Dataframe.apply', nhmzs__rirc, vtyw__aeinw,
            package_name='pandas', module_name='DataFrame')
        tpfsn__znzy = True
        if types.unliteral(vbqaj__vaf) == types.unicode_type:
            if not is_overload_constant_str(vbqaj__vaf):
                raise BodoError(
                    f'DataFrame.apply(): string argument (for builtins) must be a compile time constant'
                    )
            tpfsn__znzy = False
        if not is_overload_constant_int(axis):
            raise BodoError(
                'Dataframe.apply(): axis argument must be a compile time constant.'
                )
        jphj__cvsoj = get_overload_const_int(axis)
        if tpfsn__znzy and jphj__cvsoj != 1:
            raise BodoError(
                'Dataframe.apply(): only axis=1 supported for user-defined functions'
                )
        elif jphj__cvsoj not in (0, 1):
            raise BodoError('Dataframe.apply(): axis must be either 0 or 1')
        julkk__slatw = []
        for arr_typ in df.data:
            ibupj__hoxg = SeriesType(arr_typ.dtype, arr_typ, df.index,
                string_type)
            klr__oyp = self.context.resolve_function_type(operator.getitem,
                (SeriesIlocType(ibupj__hoxg), types.int64), {}).return_type
            julkk__slatw.append(klr__oyp)
        mkkyv__rvb = types.none
        sdvtc__tzn = HeterogeneousIndexType(types.BaseTuple.from_types(
            tuple(types.literal(jil__onn) for jil__onn in df.columns)), None)
        pmoxw__iaj = types.BaseTuple.from_types(julkk__slatw)
        dtd__avps = df.index.dtype
        if dtd__avps == types.NPDatetime('ns'):
            dtd__avps = bodo.pd_timestamp_type
        if dtd__avps == types.NPTimedelta('ns'):
            dtd__avps = bodo.pd_timedelta_type
        if is_heterogeneous_tuple_type(pmoxw__iaj):
            inn__qifzp = HeterogeneousSeriesType(pmoxw__iaj, sdvtc__tzn,
                dtd__avps)
        else:
            inn__qifzp = SeriesType(pmoxw__iaj.dtype, pmoxw__iaj,
                sdvtc__tzn, dtd__avps)
        ayvnb__qdmrf = inn__qifzp,
        if vqda__hmfmy is not None:
            ayvnb__qdmrf += tuple(vqda__hmfmy.types)
        try:
            if not tpfsn__znzy:
                llr__xze = bodo.utils.transform.get_udf_str_return_type(df,
                    get_overload_const_str(vbqaj__vaf), self.context,
                    'DataFrame.apply', axis if jphj__cvsoj == 1 else None)
            else:
                llr__xze = get_const_func_output_type(vbqaj__vaf,
                    ayvnb__qdmrf, kws, self.context, numba.core.registry.
                    cpu_target.target_context)
        except Exception as phrh__nfumm:
            raise_bodo_error(get_udf_error_msg('DataFrame.apply()',
                phrh__nfumm))
        if tpfsn__znzy:
            if not (is_overload_constant_int(axis) and 
                get_overload_const_int(axis) == 1):
                raise BodoError(
                    'Dataframe.apply(): only user-defined functions with axis=1 supported'
                    )
            if isinstance(llr__xze, (SeriesType, HeterogeneousSeriesType)
                ) and llr__xze.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(llr__xze, HeterogeneousSeriesType):
                gjxct__snxcx, hkupf__ysca = llr__xze.const_info
                zka__njwge = tuple(dtype_to_array_type(bxqdu__pfi) for
                    bxqdu__pfi in llr__xze.data.types)
                ffrw__yprfe = DataFrameType(zka__njwge, df.index, hkupf__ysca)
            elif isinstance(llr__xze, SeriesType):
                yet__vjub, hkupf__ysca = llr__xze.const_info
                zka__njwge = tuple(dtype_to_array_type(llr__xze.dtype) for
                    gjxct__snxcx in range(yet__vjub))
                ffrw__yprfe = DataFrameType(zka__njwge, df.index, hkupf__ysca)
            else:
                llu__ybeja = get_udf_out_arr_type(llr__xze)
                ffrw__yprfe = SeriesType(llu__ybeja.dtype, llu__ybeja, df.
                    index, None)
        else:
            ffrw__yprfe = llr__xze
        vdumm__svdxi = ', '.join("{} = ''".format(lxv__insej) for
            lxv__insej in kws.keys())
        erva__nxrvs = f"""def apply_stub(func, axis=0, raw=False, result_type=None, args=(), {vdumm__svdxi}):
"""
        erva__nxrvs += '    pass\n'
        mintx__azc = {}
        exec(erva__nxrvs, {}, mintx__azc)
        erz__tkvwe = mintx__azc['apply_stub']
        xcljr__gym = numba.core.utils.pysignature(erz__tkvwe)
        rpqke__qjsf = (vbqaj__vaf, axis, mlqci__xil, lrwsy__ybhrf, vqda__hmfmy
            ) + tuple(kws.values())
        return signature(ffrw__yprfe, *rpqke__qjsf).replace(pysig=xcljr__gym)

    @bound_function('df.plot', no_unliteral=True)
    def resolve_plot(self, df, args, kws):
        func_name = 'DataFrame.plot'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        mce__xvhf = ('x', 'y', 'kind', 'figsize', 'ax', 'subplots',
            'sharex', 'sharey', 'layout', 'use_index', 'title', 'grid',
            'legend', 'style', 'logx', 'logy', 'loglog', 'xticks', 'yticks',
            'xlim', 'ylim', 'rot', 'fontsize', 'colormap', 'table', 'yerr',
            'xerr', 'secondary_y', 'sort_columns', 'xlabel', 'ylabel',
            'position', 'stacked', 'mark_right', 'include_bool', 'backend')
        ujv__sfwfp = {'x': None, 'y': None, 'kind': 'line', 'figsize': None,
            'ax': None, 'subplots': False, 'sharex': None, 'sharey': False,
            'layout': None, 'use_index': True, 'title': None, 'grid': None,
            'legend': True, 'style': None, 'logx': False, 'logy': False,
            'loglog': False, 'xticks': None, 'yticks': None, 'xlim': None,
            'ylim': None, 'rot': None, 'fontsize': None, 'colormap': None,
            'table': False, 'yerr': None, 'xerr': None, 'secondary_y': 
            False, 'sort_columns': False, 'xlabel': None, 'ylabel': None,
            'position': 0.5, 'stacked': False, 'mark_right': True,
            'include_bool': False, 'backend': None}
        gcnz__irch = ('subplots', 'sharex', 'sharey', 'layout', 'use_index',
            'grid', 'style', 'logx', 'logy', 'loglog', 'xlim', 'ylim',
            'rot', 'colormap', 'table', 'yerr', 'xerr', 'sort_columns',
            'secondary_y', 'colorbar', 'position', 'stacked', 'mark_right',
            'include_bool', 'backend')
        xcljr__gym, pkasr__mbdy = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, mce__xvhf, ujv__sfwfp, gcnz__irch)
        tylwc__fzw = pkasr__mbdy[2]
        if not is_overload_constant_str(tylwc__fzw):
            raise BodoError(
                f"{func_name}: kind must be a constant string and one of ('line', 'scatter')."
                )
        znhx__rbf = pkasr__mbdy[0]
        if not is_overload_none(znhx__rbf) and not (is_overload_int(
            znhx__rbf) or is_overload_constant_str(znhx__rbf)):
            raise BodoError(
                f'{func_name}: x must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(znhx__rbf):
            arpz__dkvob = get_overload_const_str(znhx__rbf)
            if arpz__dkvob not in df.columns:
                raise BodoError(f'{func_name}: {arpz__dkvob} column not found.'
                    )
        elif is_overload_int(znhx__rbf):
            mdv__brd = get_overload_const_int(znhx__rbf)
            if mdv__brd > len(df.columns):
                raise BodoError(
                    f'{func_name}: x: {mdv__brd} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            znhx__rbf = df.columns[znhx__rbf]
        tho__vqk = pkasr__mbdy[1]
        if not is_overload_none(tho__vqk) and not (is_overload_int(tho__vqk
            ) or is_overload_constant_str(tho__vqk)):
            raise BodoError(
                'df.plot(): y must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(tho__vqk):
            fkipe__xsa = get_overload_const_str(tho__vqk)
            if fkipe__xsa not in df.columns:
                raise BodoError(f'{func_name}: {fkipe__xsa} column not found.')
        elif is_overload_int(tho__vqk):
            uvnqf__lbwat = get_overload_const_int(tho__vqk)
            if uvnqf__lbwat > len(df.columns):
                raise BodoError(
                    f'{func_name}: y: {uvnqf__lbwat} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            tho__vqk = df.columns[tho__vqk]
        xbgem__rag = pkasr__mbdy[3]
        if not is_overload_none(xbgem__rag) and not is_tuple_like_type(
            xbgem__rag):
            raise BodoError(
                f'{func_name}: figsize must be a constant numeric tuple (width, height) or None.'
                )
        sqi__tkxu = pkasr__mbdy[10]
        if not is_overload_none(sqi__tkxu) and not is_overload_constant_str(
            sqi__tkxu):
            raise BodoError(
                f'{func_name}: title must be a constant string or None.')
        nweo__rwoou = pkasr__mbdy[12]
        if not is_overload_bool(nweo__rwoou):
            raise BodoError(f'{func_name}: legend must be a boolean type.')
        onhm__idze = pkasr__mbdy[17]
        if not is_overload_none(onhm__idze) and not is_tuple_like_type(
            onhm__idze):
            raise BodoError(
                f'{func_name}: xticks must be a constant tuple or None.')
        mam__ttzu = pkasr__mbdy[18]
        if not is_overload_none(mam__ttzu) and not is_tuple_like_type(mam__ttzu
            ):
            raise BodoError(
                f'{func_name}: yticks must be a constant tuple or None.')
        htdh__tcrx = pkasr__mbdy[22]
        if not is_overload_none(htdh__tcrx) and not is_overload_int(htdh__tcrx
            ):
            raise BodoError(
                f'{func_name}: fontsize must be an integer or None.')
        gpf__iiq = pkasr__mbdy[29]
        if not is_overload_none(gpf__iiq) and not is_overload_constant_str(
            gpf__iiq):
            raise BodoError(
                f'{func_name}: xlabel must be a constant string or None.')
        ipxlg__hjzy = pkasr__mbdy[30]
        if not is_overload_none(ipxlg__hjzy) and not is_overload_constant_str(
            ipxlg__hjzy):
            raise BodoError(
                f'{func_name}: ylabel must be a constant string or None.')
        cdu__gepko = types.List(types.mpl_line_2d_type)
        tylwc__fzw = get_overload_const_str(tylwc__fzw)
        if tylwc__fzw == 'scatter':
            if is_overload_none(znhx__rbf) and is_overload_none(tho__vqk):
                raise BodoError(
                    f'{func_name}: {tylwc__fzw} requires an x and y column.')
            elif is_overload_none(znhx__rbf):
                raise BodoError(
                    f'{func_name}: {tylwc__fzw} x column is missing.')
            elif is_overload_none(tho__vqk):
                raise BodoError(
                    f'{func_name}: {tylwc__fzw} y column is missing.')
            cdu__gepko = types.mpl_path_collection_type
        elif tylwc__fzw != 'line':
            raise BodoError(f'{func_name}: {tylwc__fzw} plot is not supported.'
                )
        return signature(cdu__gepko, *pkasr__mbdy).replace(pysig=xcljr__gym)

    def generic_resolve(self, df, attr):
        if self._is_existing_attr(attr):
            return
        check_runtime_cols_unsupported(df,
            'Acessing DataFrame columns by attribute')
        if attr in df.columns:
            lpclh__ylup = df.columns.index(attr)
            arr_typ = df.data[lpclh__ylup]
            return SeriesType(arr_typ.dtype, arr_typ, df.index, types.
                StringLiteral(attr))
        if len(df.columns) > 0 and isinstance(df.columns[0], tuple):
            jtwe__hor = []
            hwz__mazq = []
            xsv__uba = False
            for i, nmxkx__axu in enumerate(df.columns):
                if nmxkx__axu[0] != attr:
                    continue
                xsv__uba = True
                jtwe__hor.append(nmxkx__axu[1] if len(nmxkx__axu) == 2 else
                    nmxkx__axu[1:])
                hwz__mazq.append(df.data[i])
            if xsv__uba:
                return DataFrameType(tuple(hwz__mazq), df.index, tuple(
                    jtwe__hor))


DataFrameAttribute._no_unliteral = True


@overload(operator.getitem, no_unliteral=True)
def namedtuple_getitem_overload(tup, idx):
    if isinstance(tup, types.BaseNamedTuple) and is_overload_constant_str(idx):
        ephyd__ptzu = get_overload_const_str(idx)
        val_ind = tup.instance_class._fields.index(ephyd__ptzu)
        return lambda tup, idx: tup[val_ind]


def decref_df_data(context, builder, payload, df_type):
    if df_type.is_table_format:
        context.nrt.decref(builder, df_type.table_type, builder.
            extract_value(payload.data, 0))
        context.nrt.decref(builder, df_type.index, payload.index)
        if df_type.has_runtime_cols:
            context.nrt.decref(builder, df_type.data[-1], payload.columns)
        return
    for i in range(len(df_type.data)):
        iznta__uenzl = builder.extract_value(payload.data, i)
        context.nrt.decref(builder, df_type.data[i], iznta__uenzl)
    context.nrt.decref(builder, df_type.index, payload.index)


def define_df_dtor(context, builder, df_type, payload_type):
    hqipv__mjcn = builder.module
    vrh__iot = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    xnkj__irgkd = cgutils.get_or_insert_function(hqipv__mjcn, vrh__iot,
        name='.dtor.df.{}'.format(df_type))
    if not xnkj__irgkd.is_declaration:
        return xnkj__irgkd
    xnkj__irgkd.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(xnkj__irgkd.append_basic_block())
    ets__okqx = xnkj__irgkd.args[0]
    mec__lfa = context.get_value_type(payload_type).as_pointer()
    awews__nvla = builder.bitcast(ets__okqx, mec__lfa)
    payload = context.make_helper(builder, payload_type, ref=awews__nvla)
    decref_df_data(context, builder, payload, df_type)
    has_parent = cgutils.is_not_null(builder, payload.parent)
    with builder.if_then(has_parent):
        elr__tkuzd = context.get_python_api(builder)
        hbxg__xwo = elr__tkuzd.gil_ensure()
        elr__tkuzd.decref(payload.parent)
        elr__tkuzd.gil_release(hbxg__xwo)
    builder.ret_void()
    return xnkj__irgkd


def construct_dataframe(context, builder, df_type, data_tup, index_val,
    parent=None, colnames=None):
    payload_type = DataFramePayloadType(df_type)
    inv__bslu = cgutils.create_struct_proxy(payload_type)(context, builder)
    inv__bslu.data = data_tup
    inv__bslu.index = index_val
    if colnames is not None:
        assert df_type.has_runtime_cols, 'construct_dataframe can only provide colnames if columns are determined at runtime'
        inv__bslu.columns = colnames
    pdfug__dmyy = context.get_value_type(payload_type)
    kslk__dkl = context.get_abi_sizeof(pdfug__dmyy)
    dmp__tmyrv = define_df_dtor(context, builder, df_type, payload_type)
    rxn__rpf = context.nrt.meminfo_alloc_dtor(builder, context.get_constant
        (types.uintp, kslk__dkl), dmp__tmyrv)
    yhv__oekax = context.nrt.meminfo_data(builder, rxn__rpf)
    rpa__tiec = builder.bitcast(yhv__oekax, pdfug__dmyy.as_pointer())
    lpmkd__lqvq = cgutils.create_struct_proxy(df_type)(context, builder)
    lpmkd__lqvq.meminfo = rxn__rpf
    if parent is None:
        lpmkd__lqvq.parent = cgutils.get_null_value(lpmkd__lqvq.parent.type)
    else:
        lpmkd__lqvq.parent = parent
        inv__bslu.parent = parent
        has_parent = cgutils.is_not_null(builder, parent)
        with builder.if_then(has_parent):
            elr__tkuzd = context.get_python_api(builder)
            hbxg__xwo = elr__tkuzd.gil_ensure()
            elr__tkuzd.incref(parent)
            elr__tkuzd.gil_release(hbxg__xwo)
    builder.store(inv__bslu._getvalue(), rpa__tiec)
    return lpmkd__lqvq._getvalue()


@intrinsic
def init_runtime_cols_dataframe(typingctx, data_typ, index_typ,
    colnames_index_typ=None):
    assert isinstance(data_typ, types.BaseTuple) and isinstance(data_typ.
        dtype, TableType
        ) and data_typ.dtype.has_runtime_cols, 'init_runtime_cols_dataframe must be called with a table that determines columns at runtime.'
    assert bodo.hiframes.pd_index_ext.is_pd_index_type(colnames_index_typ
        ) or isinstance(colnames_index_typ, bodo.hiframes.
        pd_multi_index_ext.MultiIndexType), 'Column names must be an index'
    if isinstance(data_typ.dtype.arr_types, types.UniTuple):
        gfjw__tsnml = [data_typ.dtype.arr_types.dtype] * len(data_typ.dtype
            .arr_types)
    else:
        gfjw__tsnml = [bxqdu__pfi for bxqdu__pfi in data_typ.dtype.arr_types]
    prn__nfqfe = DataFrameType(tuple(gfjw__tsnml + [colnames_index_typ]),
        index_typ, None, is_table_format=True)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup, index, col_names = args
        parent = None
        seih__jxdtk = construct_dataframe(context, builder, df_type,
            data_tup, index, parent, col_names)
        context.nrt.incref(builder, data_typ, data_tup)
        context.nrt.incref(builder, index_typ, index)
        context.nrt.incref(builder, colnames_index_typ, col_names)
        return seih__jxdtk
    sig = signature(prn__nfqfe, data_typ, index_typ, colnames_index_typ)
    return sig, codegen


@intrinsic
def init_dataframe(typingctx, data_tup_typ, index_typ, col_names_typ=None):
    assert is_pd_index_type(index_typ) or isinstance(index_typ, MultiIndexType
        ), 'init_dataframe(): invalid index type'
    yet__vjub = len(data_tup_typ.types)
    if yet__vjub == 0:
        wcsvo__ynuzd = ()
    elif isinstance(col_names_typ, types.TypeRef):
        wcsvo__ynuzd = col_names_typ.instance_type.columns
    else:
        wcsvo__ynuzd = get_const_tup_vals(col_names_typ)
    if yet__vjub == 1 and isinstance(data_tup_typ.types[0], TableType):
        yet__vjub = len(data_tup_typ.types[0].arr_types)
    assert len(wcsvo__ynuzd
        ) == yet__vjub, 'init_dataframe(): number of column names does not match number of columns'
    is_table_format = False
    soym__dehv = data_tup_typ.types
    if yet__vjub != 0 and isinstance(data_tup_typ.types[0], TableType):
        soym__dehv = data_tup_typ.types[0].arr_types
        is_table_format = True
    prn__nfqfe = DataFrameType(soym__dehv, index_typ, wcsvo__ynuzd,
        is_table_format=is_table_format)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup = args[0]
        index_val = args[1]
        parent = None
        if is_table_format:
            muvtg__qyw = cgutils.create_struct_proxy(prn__nfqfe.table_type)(
                context, builder, builder.extract_value(data_tup, 0))
            parent = muvtg__qyw.parent
        seih__jxdtk = construct_dataframe(context, builder, df_type,
            data_tup, index_val, parent, None)
        context.nrt.incref(builder, data_tup_typ, data_tup)
        context.nrt.incref(builder, index_typ, index_val)
        return seih__jxdtk
    sig = signature(prn__nfqfe, data_tup_typ, index_typ, col_names_typ)
    return sig, codegen


@intrinsic
def has_parent(typingctx, df=None):
    check_runtime_cols_unsupported(df, 'has_parent')

    def codegen(context, builder, sig, args):
        lpmkd__lqvq = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        return cgutils.is_not_null(builder, lpmkd__lqvq.parent)
    return signature(types.bool_, df), codegen


@intrinsic
def _column_needs_unboxing(typingctx, df_typ, i_typ=None):
    check_runtime_cols_unsupported(df_typ, '_column_needs_unboxing')
    assert isinstance(df_typ, DataFrameType) and is_overload_constant_int(i_typ
        )

    def codegen(context, builder, sig, args):
        inv__bslu = get_dataframe_payload(context, builder, df_typ, args[0])
        wizuy__uqci = get_overload_const_int(i_typ)
        arr_typ = df_typ.data[wizuy__uqci]
        if df_typ.is_table_format:
            muvtg__qyw = cgutils.create_struct_proxy(df_typ.table_type)(context
                , builder, builder.extract_value(inv__bslu.data, 0))
            lzvt__vla = df_typ.table_type.type_to_blk[arr_typ]
            bff__qynpt = getattr(muvtg__qyw, f'block_{lzvt__vla}')
            vtb__kuu = ListInstance(context, builder, types.List(arr_typ),
                bff__qynpt)
            qhre__xtdes = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[wizuy__uqci])
            iznta__uenzl = vtb__kuu.getitem(qhre__xtdes)
        else:
            iznta__uenzl = builder.extract_value(inv__bslu.data, wizuy__uqci)
        wvhj__wcrl = cgutils.alloca_once_value(builder, iznta__uenzl)
        dlwa__uzebi = cgutils.alloca_once_value(builder, context.
            get_constant_null(arr_typ))
        return is_ll_eq(builder, wvhj__wcrl, dlwa__uzebi)
    return signature(types.bool_, df_typ, i_typ), codegen


def get_dataframe_payload(context, builder, df_type, value):
    rxn__rpf = cgutils.create_struct_proxy(df_type)(context, builder, value
        ).meminfo
    payload_type = DataFramePayloadType(df_type)
    payload = context.nrt.meminfo_data(builder, rxn__rpf)
    mec__lfa = context.get_value_type(payload_type).as_pointer()
    payload = builder.bitcast(payload, mec__lfa)
    return context.make_helper(builder, payload_type, ref=payload)


@intrinsic
def _get_dataframe_data(typingctx, df_typ=None):
    check_runtime_cols_unsupported(df_typ, '_get_dataframe_data')
    prn__nfqfe = types.Tuple(df_typ.data)
    if df_typ.is_table_format:
        prn__nfqfe = types.Tuple([TableType(df_typ.data)])
    sig = signature(prn__nfqfe, df_typ)

    def codegen(context, builder, signature, args):
        inv__bslu = get_dataframe_payload(context, builder, signature.args[
            0], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            inv__bslu.data)
    return sig, codegen


@intrinsic
def get_dataframe_index(typingctx, df_typ=None):
    check_runtime_cols_unsupported(df_typ, 'get_dataframe_index')

    def codegen(context, builder, signature, args):
        inv__bslu = get_dataframe_payload(context, builder, signature.args[
            0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.index, inv__bslu.
            index)
    prn__nfqfe = df_typ.index
    sig = signature(prn__nfqfe, df_typ)
    return sig, codegen


def get_dataframe_data(df, i):
    return df[i]


@infer_global(get_dataframe_data)
class GetDataFrameDataInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        if not is_overload_constant_int(args[1]):
            raise_bodo_error(
                'Selecting a DataFrame column requires a constant column label'
                )
        df = args[0]
        check_runtime_cols_unsupported(df, 'get_dataframe_data')
        i = get_overload_const_int(args[1])
        gpvx__eqrgz = df.data[i]
        return gpvx__eqrgz(*args)


GetDataFrameDataInfer.prefer_literal = True


def get_dataframe_data_impl(df, i):
    if df.is_table_format:

        def _impl(df, i):
            if has_parent(df) and _column_needs_unboxing(df, i):
                bodo.hiframes.boxing.unbox_dataframe_column(df, i)
            return get_table_data(_get_dataframe_data(df)[0], i)
        return _impl

    def _impl(df, i):
        if has_parent(df) and _column_needs_unboxing(df, i):
            bodo.hiframes.boxing.unbox_dataframe_column(df, i)
        return _get_dataframe_data(df)[i]
    return _impl


@intrinsic
def get_dataframe_table(typingctx, df_typ=None):
    assert df_typ.is_table_format, 'get_dataframe_table() expects table format'

    def codegen(context, builder, signature, args):
        inv__bslu = get_dataframe_payload(context, builder, signature.args[
            0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.table_type,
            builder.extract_value(inv__bslu.data, 0))
    return df_typ.table_type(df_typ), codegen


@lower_builtin(get_dataframe_data, DataFrameType, types.IntegerLiteral)
def lower_get_dataframe_data(context, builder, sig, args):
    impl = get_dataframe_data_impl(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_dataframe_data',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_dataframe_index',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_dataframe_table',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func


def alias_ext_init_dataframe(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 3
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_dataframe',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_init_dataframe


def init_dataframe_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 3 and not kws
    data_tup = args[0]
    index = args[1]
    pmoxw__iaj = self.typemap[data_tup.name]
    if any(is_tuple_like_type(bxqdu__pfi) for bxqdu__pfi in pmoxw__iaj.types):
        return None
    if equiv_set.has_shape(data_tup):
        rtom__unbvv = equiv_set.get_shape(data_tup)
        if len(rtom__unbvv) > 1:
            equiv_set.insert_equiv(*rtom__unbvv)
        if len(rtom__unbvv) > 0:
            sdvtc__tzn = self.typemap[index.name]
            if not isinstance(sdvtc__tzn, HeterogeneousIndexType
                ) and equiv_set.has_shape(index):
                equiv_set.insert_equiv(rtom__unbvv[0], index)
            return ArrayAnalysis.AnalyzeResult(shape=(rtom__unbvv[0], len(
                rtom__unbvv)), pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_dataframe_ext_init_dataframe
    ) = init_dataframe_equiv


def get_dataframe_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    unv__yalrz = args[0]
    vxmjb__qqfcf = self.typemap[unv__yalrz.name].data
    if any(is_tuple_like_type(bxqdu__pfi) for bxqdu__pfi in vxmjb__qqfcf):
        return None
    if equiv_set.has_shape(unv__yalrz):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            unv__yalrz)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_data
    ) = get_dataframe_data_equiv


def get_dataframe_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    unv__yalrz = args[0]
    sdvtc__tzn = self.typemap[unv__yalrz.name].index
    if isinstance(sdvtc__tzn, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(unv__yalrz):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            unv__yalrz)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_index
    ) = get_dataframe_index_equiv


def get_dataframe_table_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    unv__yalrz = args[0]
    if equiv_set.has_shape(unv__yalrz):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            unv__yalrz), pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_table
    ) = get_dataframe_table_equiv


@intrinsic
def set_dataframe_data(typingctx, df_typ, c_ind_typ, arr_typ=None):
    check_runtime_cols_unsupported(df_typ, 'set_dataframe_data')
    assert is_overload_constant_int(c_ind_typ)
    wizuy__uqci = get_overload_const_int(c_ind_typ)
    if df_typ.data[wizuy__uqci] != arr_typ:
        raise BodoError(
            'Changing dataframe column data type inplace is not supported in conditionals/loops or for dataframe arguments'
            )

    def codegen(context, builder, signature, args):
        naik__tifjm, gjxct__snxcx, xlm__cpzgm = args
        inv__bslu = get_dataframe_payload(context, builder, df_typ, naik__tifjm
            )
        if df_typ.is_table_format:
            muvtg__qyw = cgutils.create_struct_proxy(df_typ.table_type)(context
                , builder, builder.extract_value(inv__bslu.data, 0))
            lzvt__vla = df_typ.table_type.type_to_blk[arr_typ]
            bff__qynpt = getattr(muvtg__qyw, f'block_{lzvt__vla}')
            vtb__kuu = ListInstance(context, builder, types.List(arr_typ),
                bff__qynpt)
            qhre__xtdes = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[wizuy__uqci])
            vtb__kuu.setitem(qhre__xtdes, xlm__cpzgm, True)
        else:
            iznta__uenzl = builder.extract_value(inv__bslu.data, wizuy__uqci)
            context.nrt.decref(builder, df_typ.data[wizuy__uqci], iznta__uenzl)
            inv__bslu.data = builder.insert_value(inv__bslu.data,
                xlm__cpzgm, wizuy__uqci)
            context.nrt.incref(builder, arr_typ, xlm__cpzgm)
        lpmkd__lqvq = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=naik__tifjm)
        payload_type = DataFramePayloadType(df_typ)
        awews__nvla = context.nrt.meminfo_data(builder, lpmkd__lqvq.meminfo)
        mec__lfa = context.get_value_type(payload_type).as_pointer()
        awews__nvla = builder.bitcast(awews__nvla, mec__lfa)
        builder.store(inv__bslu._getvalue(), awews__nvla)
        return impl_ret_borrowed(context, builder, df_typ, naik__tifjm)
    sig = signature(df_typ, df_typ, c_ind_typ, arr_typ)
    return sig, codegen


@intrinsic
def set_df_index(typingctx, df_t, index_t=None):
    check_runtime_cols_unsupported(df_t, 'set_df_index')

    def codegen(context, builder, signature, args):
        sjjw__gxat = args[0]
        index_val = args[1]
        df_typ = signature.args[0]
        ynf__tqf = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=sjjw__gxat)
        iqmmg__okhtj = get_dataframe_payload(context, builder, df_typ,
            sjjw__gxat)
        lpmkd__lqvq = construct_dataframe(context, builder, signature.
            return_type, iqmmg__okhtj.data, index_val, ynf__tqf.parent, None)
        context.nrt.incref(builder, index_t, index_val)
        context.nrt.incref(builder, types.Tuple(df_t.data), iqmmg__okhtj.data)
        return lpmkd__lqvq
    prn__nfqfe = DataFrameType(df_t.data, index_t, df_t.columns, df_t.dist,
        df_t.is_table_format)
    sig = signature(prn__nfqfe, df_t, index_t)
    return sig, codegen


@intrinsic
def set_df_column_with_reflect(typingctx, df_type, cname_type, arr_type=None):
    check_runtime_cols_unsupported(df_type, 'set_df_column_with_reflect')
    assert is_literal_type(cname_type), 'constant column name expected'
    col_name = get_literal_value(cname_type)
    yet__vjub = len(df_type.columns)
    edp__fdcc = yet__vjub
    avxw__ctv = df_type.data
    wcsvo__ynuzd = df_type.columns
    index_typ = df_type.index
    dqtim__wmec = col_name not in df_type.columns
    wizuy__uqci = yet__vjub
    if dqtim__wmec:
        avxw__ctv += arr_type,
        wcsvo__ynuzd += col_name,
        edp__fdcc += 1
    else:
        wizuy__uqci = df_type.columns.index(col_name)
        avxw__ctv = tuple(arr_type if i == wizuy__uqci else avxw__ctv[i] for
            i in range(yet__vjub))

    def codegen(context, builder, signature, args):
        naik__tifjm, gjxct__snxcx, xlm__cpzgm = args
        in_dataframe_payload = get_dataframe_payload(context, builder,
            df_type, naik__tifjm)
        albpu__olgf = cgutils.create_struct_proxy(df_type)(context, builder,
            value=naik__tifjm)
        if df_type.is_table_format:
            ivvf__jeipj = df_type.table_type
            duol__xeei = builder.extract_value(in_dataframe_payload.data, 0)
            jai__vyhx = TableType(avxw__ctv)
            tvavt__cpnym = set_table_data_codegen(context, builder,
                ivvf__jeipj, duol__xeei, jai__vyhx, arr_type, xlm__cpzgm,
                wizuy__uqci, dqtim__wmec)
            data_tup = context.make_tuple(builder, types.Tuple([jai__vyhx]),
                [tvavt__cpnym])
        else:
            soym__dehv = [(builder.extract_value(in_dataframe_payload.data,
                i) if i != wizuy__uqci else xlm__cpzgm) for i in range(
                yet__vjub)]
            if dqtim__wmec:
                soym__dehv.append(xlm__cpzgm)
            for unv__yalrz, reiex__nlm in zip(soym__dehv, avxw__ctv):
                context.nrt.incref(builder, reiex__nlm, unv__yalrz)
            data_tup = context.make_tuple(builder, types.Tuple(avxw__ctv),
                soym__dehv)
        index_val = in_dataframe_payload.index
        context.nrt.incref(builder, index_typ, index_val)
        uzh__kjo = construct_dataframe(context, builder, signature.
            return_type, data_tup, index_val, albpu__olgf.parent, None)
        if not dqtim__wmec and arr_type == df_type.data[wizuy__uqci]:
            decref_df_data(context, builder, in_dataframe_payload, df_type)
            payload_type = DataFramePayloadType(df_type)
            awews__nvla = context.nrt.meminfo_data(builder, albpu__olgf.meminfo
                )
            mec__lfa = context.get_value_type(payload_type).as_pointer()
            awews__nvla = builder.bitcast(awews__nvla, mec__lfa)
            jex__gxtdk = get_dataframe_payload(context, builder, df_type,
                uzh__kjo)
            builder.store(jex__gxtdk._getvalue(), awews__nvla)
            context.nrt.incref(builder, index_typ, index_val)
            if df_type.is_table_format:
                context.nrt.incref(builder, jai__vyhx, builder.
                    extract_value(data_tup, 0))
            else:
                for unv__yalrz, reiex__nlm in zip(soym__dehv, avxw__ctv):
                    context.nrt.incref(builder, reiex__nlm, unv__yalrz)
        has_parent = cgutils.is_not_null(builder, albpu__olgf.parent)
        with builder.if_then(has_parent):
            elr__tkuzd = context.get_python_api(builder)
            hbxg__xwo = elr__tkuzd.gil_ensure()
            yoip__iwnt = context.get_env_manager(builder)
            context.nrt.incref(builder, arr_type, xlm__cpzgm)
            jil__onn = numba.core.pythonapi._BoxContext(context, builder,
                elr__tkuzd, yoip__iwnt)
            qboqh__rdui = jil__onn.pyapi.from_native_value(arr_type,
                xlm__cpzgm, jil__onn.env_manager)
            if isinstance(col_name, str):
                xnkr__hgk = context.insert_const_string(builder.module,
                    col_name)
                ybgg__blcs = elr__tkuzd.string_from_string(xnkr__hgk)
            else:
                assert isinstance(col_name, int)
                ybgg__blcs = elr__tkuzd.long_from_longlong(context.
                    get_constant(types.intp, col_name))
            elr__tkuzd.object_setitem(albpu__olgf.parent, ybgg__blcs,
                qboqh__rdui)
            elr__tkuzd.decref(qboqh__rdui)
            elr__tkuzd.decref(ybgg__blcs)
            elr__tkuzd.gil_release(hbxg__xwo)
        return uzh__kjo
    prn__nfqfe = DataFrameType(avxw__ctv, index_typ, wcsvo__ynuzd, df_type.
        dist, df_type.is_table_format)
    sig = signature(prn__nfqfe, df_type, cname_type, arr_type)
    return sig, codegen


@lower_constant(DataFrameType)
def lower_constant_dataframe(context, builder, df_type, pyval):
    check_runtime_cols_unsupported(df_type, 'lowering a constant DataFrame')
    yet__vjub = len(pyval.columns)
    soym__dehv = tuple(pyval.iloc[:, (i)].values for i in range(yet__vjub))
    if df_type.is_table_format:
        muvtg__qyw = context.get_constant_generic(builder, df_type.
            table_type, Table(soym__dehv))
        data_tup = lir.Constant.literal_struct([muvtg__qyw])
    else:
        data_tup = lir.Constant.literal_struct([context.
            get_constant_generic(builder, df_type.data[i], nmxkx__axu) for 
            i, nmxkx__axu in enumerate(soym__dehv)])
    index_val = context.get_constant_generic(builder, df_type.index, pyval.
        index)
    ilo__snw = context.get_constant_null(types.pyobject)
    payload = lir.Constant.literal_struct([data_tup, index_val, ilo__snw])
    payload = cgutils.global_constant(builder, '.const.payload', payload
        ).bitcast(cgutils.voidptr_t)
    gfnsf__ubyfw = context.get_constant(types.int64, -1)
    afbs__pro = context.get_constant_null(types.voidptr)
    rxn__rpf = lir.Constant.literal_struct([gfnsf__ubyfw, afbs__pro,
        afbs__pro, payload, gfnsf__ubyfw])
    rxn__rpf = cgutils.global_constant(builder, '.const.meminfo', rxn__rpf
        ).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([rxn__rpf, ilo__snw])


@lower_cast(DataFrameType, DataFrameType)
def cast_df_to_df(context, builder, fromty, toty, val):
    if (fromty.data == toty.data and fromty.index == toty.index and fromty.
        columns == toty.columns and fromty.is_table_format == toty.
        is_table_format and fromty.dist != toty.dist and fromty.
        has_runtime_cols == toty.has_runtime_cols):
        return val
    if not fromty.has_runtime_cols and not toty.has_runtime_cols and len(fromty
        .data) == 0 and len(toty.columns):
        return _cast_empty_df(context, builder, toty)
    if (fromty.data != toty.data or fromty.has_runtime_cols != toty.
        has_runtime_cols):
        raise BodoError(f'Invalid dataframe cast from {fromty} to {toty}')
    in_dataframe_payload = get_dataframe_payload(context, builder, fromty, val)
    if isinstance(fromty.index, RangeIndexType) and isinstance(toty.index,
        NumericIndexType):
        aes__bxu = context.cast(builder, in_dataframe_payload.index, fromty
            .index, toty.index)
    else:
        aes__bxu = in_dataframe_payload.index
        context.nrt.incref(builder, fromty.index, aes__bxu)
    if fromty.is_table_format == toty.is_table_format:
        hwz__mazq = in_dataframe_payload.data
        if fromty.is_table_format:
            context.nrt.incref(builder, types.Tuple([fromty.table_type]),
                hwz__mazq)
        else:
            context.nrt.incref(builder, types.BaseTuple.from_types(fromty.
                data), hwz__mazq)
    elif toty.is_table_format:
        hwz__mazq = _cast_df_data_to_table_format(context, builder, fromty,
            toty, in_dataframe_payload)
    else:
        hwz__mazq = _cast_df_data_to_tuple_format(context, builder, fromty,
            toty, in_dataframe_payload)
    return construct_dataframe(context, builder, toty, hwz__mazq, aes__bxu,
        in_dataframe_payload.parent, None)


def _cast_empty_df(context, builder, toty):
    evkwg__joe = {}
    if isinstance(toty.index, RangeIndexType):
        index = 'bodo.hiframes.pd_index_ext.init_range_index(0, 0, 1, None)'
    else:
        yankb__egin = get_index_data_arr_types(toty.index)[0]
        rktr__xcqz = bodo.utils.transform.get_type_alloc_counts(yankb__egin
            ) - 1
        corks__arsq = ', '.join('0' for gjxct__snxcx in range(rktr__xcqz))
        index = (
            'bodo.utils.conversion.index_from_array(bodo.utils.utils.alloc_type(0, index_arr_type, ({}{})))'
            .format(corks__arsq, ', ' if rktr__xcqz == 1 else ''))
        evkwg__joe['index_arr_type'] = yankb__egin
    xlyp__six = []
    for i, arr_typ in enumerate(toty.data):
        rktr__xcqz = bodo.utils.transform.get_type_alloc_counts(arr_typ) - 1
        corks__arsq = ', '.join('0' for gjxct__snxcx in range(rktr__xcqz))
        azyqi__bzb = ('bodo.utils.utils.alloc_type(0, arr_type{}, ({}{}))'.
            format(i, corks__arsq, ', ' if rktr__xcqz == 1 else ''))
        xlyp__six.append(azyqi__bzb)
        evkwg__joe[f'arr_type{i}'] = arr_typ
    xlyp__six = ', '.join(xlyp__six)
    erva__nxrvs = 'def impl():\n'
    agbn__fntky = bodo.hiframes.dataframe_impl._gen_init_df(erva__nxrvs,
        toty.columns, xlyp__six, index, evkwg__joe)
    df = context.compile_internal(builder, agbn__fntky, toty(), [])
    return df


def _cast_df_data_to_table_format(context, builder, fromty, toty,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame to table format')
    bxdlg__jvkt = toty.table_type
    muvtg__qyw = cgutils.create_struct_proxy(bxdlg__jvkt)(context, builder)
    muvtg__qyw.parent = in_dataframe_payload.parent
    for bxqdu__pfi, lzvt__vla in bxdlg__jvkt.type_to_blk.items():
        fkk__wyupd = context.get_constant(types.int64, len(bxdlg__jvkt.
            block_to_arr_ind[lzvt__vla]))
        gjxct__snxcx, piydt__xaii = ListInstance.allocate_ex(context,
            builder, types.List(bxqdu__pfi), fkk__wyupd)
        piydt__xaii.size = fkk__wyupd
        setattr(muvtg__qyw, f'block_{lzvt__vla}', piydt__xaii.value)
    for i, bxqdu__pfi in enumerate(fromty.data):
        iznta__uenzl = builder.extract_value(in_dataframe_payload.data, i)
        lzvt__vla = bxdlg__jvkt.type_to_blk[bxqdu__pfi]
        bff__qynpt = getattr(muvtg__qyw, f'block_{lzvt__vla}')
        vtb__kuu = ListInstance(context, builder, types.List(bxqdu__pfi),
            bff__qynpt)
        qhre__xtdes = context.get_constant(types.int64, bxdlg__jvkt.
            block_offsets[i])
        vtb__kuu.setitem(qhre__xtdes, iznta__uenzl, True)
    data_tup = context.make_tuple(builder, types.Tuple([bxdlg__jvkt]), [
        muvtg__qyw._getvalue()])
    return data_tup


def _cast_df_data_to_tuple_format(context, builder, fromty, toty,
    in_dataframe_payload):
    check_runtime_cols_unsupported(fromty,
        'casting table format to traditional DataFrame')
    bxdlg__jvkt = fromty.table_type
    muvtg__qyw = cgutils.create_struct_proxy(bxdlg__jvkt)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    soym__dehv = []
    for i, bxqdu__pfi in enumerate(toty.data):
        lzvt__vla = bxdlg__jvkt.type_to_blk[bxqdu__pfi]
        bff__qynpt = getattr(muvtg__qyw, f'block_{lzvt__vla}')
        vtb__kuu = ListInstance(context, builder, types.List(bxqdu__pfi),
            bff__qynpt)
        qhre__xtdes = context.get_constant(types.int64, bxdlg__jvkt.
            block_offsets[i])
        iznta__uenzl = vtb__kuu.getitem(qhre__xtdes)
        context.nrt.incref(builder, bxqdu__pfi, iznta__uenzl)
        soym__dehv.append(iznta__uenzl)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), soym__dehv)
    return data_tup


@overload(pd.DataFrame, inline='always', no_unliteral=True)
def pd_dataframe_overload(data=None, index=None, columns=None, dtype=None,
    copy=False):
    if not is_overload_constant_bool(copy):
        raise BodoError(
            "pd.DataFrame(): 'copy' argument should be a constant boolean")
    copy = get_overload_const(copy)
    blcv__sinvd, xlyp__six, index_arg = _get_df_args(data, index, columns,
        dtype, copy)
    tski__cgiu = gen_const_tup(blcv__sinvd)
    erva__nxrvs = (
        'def _init_df(data=None, index=None, columns=None, dtype=None, copy=False):\n'
        )
    erva__nxrvs += (
        '  return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, {}, {})\n'
        .format(xlyp__six, index_arg, tski__cgiu))
    mintx__azc = {}
    exec(erva__nxrvs, {'bodo': bodo, 'np': np}, mintx__azc)
    rgzqc__igp = mintx__azc['_init_df']
    return rgzqc__igp


def _get_df_args(data, index, columns, dtype, copy):
    tatl__xpa = ''
    if not is_overload_none(dtype):
        tatl__xpa = '.astype(dtype)'
    index_is_none = is_overload_none(index)
    index_arg = 'bodo.utils.conversion.convert_to_index(index)'
    if isinstance(data, types.BaseTuple):
        if not data.types[0] == types.StringLiteral('__bodo_tup'):
            raise BodoError('pd.DataFrame tuple input data not supported yet')
        assert len(data.types) % 2 == 1, 'invalid const dict tuple structure'
        yet__vjub = (len(data.types) - 1) // 2
        ahuz__uuj = [bxqdu__pfi.literal_value for bxqdu__pfi in data.types[
            1:yet__vjub + 1]]
        data_val_types = dict(zip(ahuz__uuj, data.types[yet__vjub + 1:]))
        soym__dehv = ['data[{}]'.format(i) for i in range(yet__vjub + 1, 2 *
            yet__vjub + 1)]
        data_dict = dict(zip(ahuz__uuj, soym__dehv))
        if is_overload_none(index):
            for i, bxqdu__pfi in enumerate(data.types[yet__vjub + 1:]):
                if isinstance(bxqdu__pfi, SeriesType):
                    index_arg = (
                        'bodo.hiframes.pd_series_ext.get_series_index(data[{}])'
                        .format(yet__vjub + 1 + i))
                    index_is_none = False
                    break
    elif is_overload_none(data):
        data_dict = {}
        data_val_types = {}
    else:
        if not (isinstance(data, types.Array) and data.ndim == 2):
            raise BodoError(
                'pd.DataFrame() only supports constant dictionary and array input'
                )
        if is_overload_none(columns):
            raise BodoError(
                "pd.DataFrame() 'columns' argument is required when an array is passed as data"
                )
        fxi__vuwuo = '.copy()' if copy else ''
        vwak__ecm = get_overload_const_list(columns)
        yet__vjub = len(vwak__ecm)
        data_val_types = {jil__onn: data.copy(ndim=1) for jil__onn in vwak__ecm
            }
        soym__dehv = ['data[:,{}]{}'.format(i, fxi__vuwuo) for i in range(
            yet__vjub)]
        data_dict = dict(zip(vwak__ecm, soym__dehv))
    if is_overload_none(columns):
        col_names = data_dict.keys()
    else:
        col_names = get_overload_const_list(columns)
    df_len = _get_df_len_from_info(data_dict, data_val_types, col_names,
        index_is_none, index_arg)
    _fill_null_arrays(data_dict, col_names, df_len, dtype)
    if index_is_none:
        if is_overload_none(data):
            index_arg = (
                'bodo.hiframes.pd_index_ext.init_binary_str_index(bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0))'
                )
        else:
            index_arg = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, {}, 1, None)'
                .format(df_len))
    xlyp__six = '({},)'.format(', '.join(
        'bodo.utils.conversion.coerce_to_array({}, True, scalar_to_arr_len={}){}'
        .format(data_dict[jil__onn], df_len, tatl__xpa) for jil__onn in
        col_names))
    if len(col_names) == 0:
        xlyp__six = '()'
    return col_names, xlyp__six, index_arg


def _get_df_len_from_info(data_dict, data_val_types, col_names,
    index_is_none, index_arg):
    df_len = '0'
    for jil__onn in col_names:
        if jil__onn in data_dict and is_iterable_type(data_val_types[jil__onn]
            ):
            df_len = 'len({})'.format(data_dict[jil__onn])
            break
    if df_len == '0' and not index_is_none:
        df_len = f'len({index_arg})'
    return df_len


def _fill_null_arrays(data_dict, col_names, df_len, dtype):
    if all(jil__onn in data_dict for jil__onn in col_names):
        return
    if is_overload_none(dtype):
        dtype = 'bodo.string_array_type'
    else:
        dtype = 'bodo.utils.conversion.array_type_from_dtype(dtype)'
    esazl__wous = 'bodo.libs.array_kernels.gen_na_array({}, {})'.format(df_len,
        dtype)
    for jil__onn in col_names:
        if jil__onn not in data_dict:
            data_dict[jil__onn] = esazl__wous


@overload(len)
def df_len_overload(df):
    if not isinstance(df, DataFrameType):
        return
    if df.has_runtime_cols:

        def impl(df):
            bxqdu__pfi = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            return len(bxqdu__pfi)
        return impl
    if len(df.columns) == 0:
        return lambda df: 0

    def impl(df):
        if is_null_pointer(df._meminfo):
            return 0
        return len(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, 0))
    return impl


@infer_global(operator.getitem)
class GetItemTuple(AbstractTemplate):
    key = operator.getitem

    def generic(self, args, kws):
        tup, idx = args
        if not isinstance(tup, types.BaseTuple) or not isinstance(idx,
            types.IntegerLiteral):
            return
        ojul__lhn = idx.literal_value
        if isinstance(ojul__lhn, int):
            gpvx__eqrgz = tup.types[ojul__lhn]
        elif isinstance(ojul__lhn, slice):
            gpvx__eqrgz = types.BaseTuple.from_types(tup.types[ojul__lhn])
        return signature(gpvx__eqrgz, *args)


GetItemTuple.prefer_literal = True


@lower_builtin(operator.getitem, types.BaseTuple, types.IntegerLiteral)
@lower_builtin(operator.getitem, types.BaseTuple, types.SliceLiteral)
def getitem_tuple_lower(context, builder, sig, args):
    imeaj__jcrvm, idx = sig.args
    idx = idx.literal_value
    tup, gjxct__snxcx = args
    if isinstance(idx, int):
        if idx < 0:
            idx += len(imeaj__jcrvm)
        if not 0 <= idx < len(imeaj__jcrvm):
            raise IndexError('cannot index at %d in %s' % (idx, imeaj__jcrvm))
        vzkbh__nwnn = builder.extract_value(tup, idx)
    elif isinstance(idx, slice):
        ioh__kprtw = cgutils.unpack_tuple(builder, tup)[idx]
        vzkbh__nwnn = context.make_tuple(builder, sig.return_type, ioh__kprtw)
    else:
        raise NotImplementedError('unexpected index %r for %s' % (idx, sig.
            args[0]))
    return impl_ret_borrowed(context, builder, sig.return_type, vzkbh__nwnn)


def join_dummy(left_df, right_df, left_on, right_on, how, suffix_x,
    suffix_y, is_join, indicator, _bodo_na_equal, gen_cond):
    return left_df


@infer_global(join_dummy)
class JoinTyper(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        from bodo.utils.typing import is_overload_str
        assert not kws
        (left_df, right_df, left_on, right_on, zvs__osx, suffix_x, suffix_y,
            is_join, indicator, _bodo_na_equal, bghfq__prh) = args
        left_on = get_overload_const_list(left_on)
        right_on = get_overload_const_list(right_on)
        pkg__aeq = set(left_on) & set(right_on)
        ggjr__rmc = set(left_df.columns) & set(right_df.columns)
        fvzyd__gguw = ggjr__rmc - pkg__aeq
        tru__xuuer = '$_bodo_index_' in left_on
        nyk__kun = '$_bodo_index_' in right_on
        how = get_overload_const_str(zvs__osx)
        eutj__kkc = how in {'left', 'outer'}
        yaq__nzexa = how in {'right', 'outer'}
        columns = []
        data = []
        if tru__xuuer and not nyk__kun and not is_join.literal_value:
            gzny__vvy = right_on[0]
            if gzny__vvy in left_df.columns:
                columns.append(gzny__vvy)
                data.append(right_df.data[right_df.columns.index(gzny__vvy)])
        if nyk__kun and not tru__xuuer and not is_join.literal_value:
            tdte__deya = left_on[0]
            if tdte__deya in right_df.columns:
                columns.append(tdte__deya)
                data.append(left_df.data[left_df.columns.index(tdte__deya)])
        for sjle__onpa, ezfw__ydec in zip(left_df.data, left_df.columns):
            columns.append(str(ezfw__ydec) + suffix_x.literal_value if 
                ezfw__ydec in fvzyd__gguw else ezfw__ydec)
            if ezfw__ydec in pkg__aeq:
                data.append(sjle__onpa)
            else:
                data.append(to_nullable_type(sjle__onpa) if yaq__nzexa else
                    sjle__onpa)
        for sjle__onpa, ezfw__ydec in zip(right_df.data, right_df.columns):
            if ezfw__ydec not in pkg__aeq:
                columns.append(str(ezfw__ydec) + suffix_y.literal_value if 
                    ezfw__ydec in fvzyd__gguw else ezfw__ydec)
                data.append(to_nullable_type(sjle__onpa) if eutj__kkc else
                    sjle__onpa)
        cyd__bnw = get_overload_const_bool(indicator)
        if cyd__bnw:
            columns.append('_merge')
            data.append(bodo.CategoricalArrayType(bodo.PDCategoricalDtype((
                'left_only', 'right_only', 'both'), bodo.string_type, False)))
        index_typ = RangeIndexType(types.none)
        if tru__xuuer and nyk__kun and not is_overload_str(how, 'asof'):
            index_typ = left_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        elif tru__xuuer and not nyk__kun:
            index_typ = right_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        elif nyk__kun and not tru__xuuer:
            index_typ = left_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        tsx__jmii = DataFrameType(tuple(data), index_typ, tuple(columns))
        return signature(tsx__jmii, *args)


JoinTyper._no_unliteral = True


@lower_builtin(join_dummy, types.VarArg(types.Any))
def lower_join_dummy(context, builder, sig, args):
    lpmkd__lqvq = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return lpmkd__lqvq._getvalue()


@overload(pd.concat, inline='always', no_unliteral=True)
def concat_overload(objs, axis=0, join='outer', join_axes=None,
    ignore_index=False, keys=None, levels=None, names=None,
    verify_integrity=False, sort=None, copy=True):
    if not is_overload_constant_int(axis):
        raise BodoError("pd.concat(): 'axis' should be a constant integer")
    if not is_overload_constant_bool(ignore_index):
        raise BodoError(
            "pd.concat(): 'ignore_index' should be a constant boolean")
    axis = get_overload_const_int(axis)
    ignore_index = is_overload_true(ignore_index)
    nhmzs__rirc = dict(join=join, join_axes=join_axes, keys=keys, levels=
        levels, names=names, verify_integrity=verify_integrity, sort=sort,
        copy=copy)
    ujv__sfwfp = dict(join='outer', join_axes=None, keys=None, levels=None,
        names=None, verify_integrity=False, sort=None, copy=True)
    check_unsupported_args('pandas.concat', nhmzs__rirc, ujv__sfwfp,
        package_name='pandas', module_name='General')
    erva__nxrvs = """def impl(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):
"""
    if axis == 1:
        if not isinstance(objs, types.BaseTuple):
            raise_bodo_error(
                'Only tuple argument for pd.concat(axis=1) expected')
        index = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(objs[0]), 1, None)'
            )
        gfaw__tli = 0
        xlyp__six = []
        names = []
        for i, lgmm__hlvr in enumerate(objs.types):
            assert isinstance(lgmm__hlvr, (SeriesType, DataFrameType))
            check_runtime_cols_unsupported(lgmm__hlvr, 'pd.concat()')
            if isinstance(lgmm__hlvr, SeriesType):
                names.append(str(gfaw__tli))
                gfaw__tli += 1
                xlyp__six.append(
                    'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'
                    .format(i))
            else:
                names.extend(lgmm__hlvr.columns)
                for wzhzw__xkvg in range(len(lgmm__hlvr.data)):
                    xlyp__six.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, wzhzw__xkvg))
        return bodo.hiframes.dataframe_impl._gen_init_df(erva__nxrvs, names,
            ', '.join(xlyp__six), index)
    assert axis == 0
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        DataFrameType):
        assert all(isinstance(bxqdu__pfi, DataFrameType) for bxqdu__pfi in
            objs.types)
        uoqrh__fly = []
        for df in objs.types:
            check_runtime_cols_unsupported(df, 'pd.concat()')
            uoqrh__fly.extend(df.columns)
        uoqrh__fly = list(dict.fromkeys(uoqrh__fly).keys())
        gfjw__tsnml = {}
        for gfaw__tli, jil__onn in enumerate(uoqrh__fly):
            for df in objs.types:
                if jil__onn in df.columns:
                    gfjw__tsnml['arr_typ{}'.format(gfaw__tli)] = df.data[df
                        .columns.index(jil__onn)]
                    break
        assert len(gfjw__tsnml) == len(uoqrh__fly)
        yewuo__enb = []
        for gfaw__tli, jil__onn in enumerate(uoqrh__fly):
            args = []
            for i, df in enumerate(objs.types):
                if jil__onn in df.columns:
                    wizuy__uqci = df.columns.index(jil__onn)
                    args.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, wizuy__uqci))
                else:
                    args.append(
                        'bodo.libs.array_kernels.gen_na_array(len(objs[{}]), arr_typ{})'
                        .format(i, gfaw__tli))
            erva__nxrvs += ('  A{} = bodo.libs.array_kernels.concat(({},))\n'
                .format(gfaw__tli, ', '.join(args)))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(A0), 1, None)'
                )
        else:
            index = (
                """bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)) if len(objs[i].
                columns) > 0)))
        return bodo.hiframes.dataframe_impl._gen_init_df(erva__nxrvs,
            uoqrh__fly, ', '.join('A{}'.format(i) for i in range(len(
            uoqrh__fly))), index, gfjw__tsnml)
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        SeriesType):
        assert all(isinstance(bxqdu__pfi, SeriesType) for bxqdu__pfi in
            objs.types)
        erva__nxrvs += ('  out_arr = bodo.libs.array_kernels.concat(({},))\n'
            .format(', '.join(
            'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'.format(
            i) for i in range(len(objs.types)))))
        if ignore_index:
            erva__nxrvs += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            erva__nxrvs += (
                """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)))))
        erva__nxrvs += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        mintx__azc = {}
        exec(erva__nxrvs, {'bodo': bodo, 'np': np, 'numba': numba}, mintx__azc)
        return mintx__azc['impl']
    if isinstance(objs, types.List) and isinstance(objs.dtype, DataFrameType):
        check_runtime_cols_unsupported(objs.dtype, 'pd.concat()')
        df_type = objs.dtype
        for gfaw__tli, jil__onn in enumerate(df_type.columns):
            erva__nxrvs += '  arrs{} = []\n'.format(gfaw__tli)
            erva__nxrvs += '  for i in range(len(objs)):\n'
            erva__nxrvs += '    df = objs[i]\n'
            erva__nxrvs += (
                """    arrs{0}.append(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0}))
"""
                .format(gfaw__tli))
            erva__nxrvs += (
                '  out_arr{0} = bodo.libs.array_kernels.concat(arrs{0})\n'.
                format(gfaw__tli))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr0), 1, None)'
                )
        else:
            erva__nxrvs += '  arrs_index = []\n'
            erva__nxrvs += '  for i in range(len(objs)):\n'
            erva__nxrvs += '    df = objs[i]\n'
            erva__nxrvs += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
            if objs.dtype.index.name_typ == types.none:
                name = None
            else:
                name = objs.dtype.index.name_typ.literal_value
            index = f"""bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index), {name!r})
"""
        return bodo.hiframes.dataframe_impl._gen_init_df(erva__nxrvs,
            df_type.columns, ', '.join('out_arr{}'.format(i) for i in range
            (len(df_type.columns))), index)
    if isinstance(objs, types.List) and isinstance(objs.dtype, SeriesType):
        erva__nxrvs += '  arrs = []\n'
        erva__nxrvs += '  for i in range(len(objs)):\n'
        erva__nxrvs += (
            '    arrs.append(bodo.hiframes.pd_series_ext.get_series_data(objs[i]))\n'
            )
        erva__nxrvs += '  out_arr = bodo.libs.array_kernels.concat(arrs)\n'
        if ignore_index:
            erva__nxrvs += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            erva__nxrvs += '  arrs_index = []\n'
            erva__nxrvs += '  for i in range(len(objs)):\n'
            erva__nxrvs += '    S = objs[i]\n'
            erva__nxrvs += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S)))
"""
            erva__nxrvs += """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index))
"""
        erva__nxrvs += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        mintx__azc = {}
        exec(erva__nxrvs, {'bodo': bodo, 'np': np, 'numba': numba}, mintx__azc)
        return mintx__azc['impl']
    raise BodoError('pd.concat(): input type {} not supported yet'.format(objs)
        )


def sort_values_dummy(df, by, ascending, inplace, na_position):
    return df.sort_values(by, ascending=ascending, inplace=inplace,
        na_position=na_position)


@infer_global(sort_values_dummy)
class SortDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df, by, ascending, inplace, na_position = args
        index = df.index
        if isinstance(index, bodo.hiframes.pd_index_ext.RangeIndexType):
            index = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64)
        prn__nfqfe = df.copy(index=index, is_table_format=False)
        return signature(prn__nfqfe, *args)


SortDummyTyper._no_unliteral = True


@lower_builtin(sort_values_dummy, types.VarArg(types.Any))
def lower_sort_values_dummy(context, builder, sig, args):
    if sig.return_type == types.none:
        return
    dmfmq__eesy = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return dmfmq__eesy._getvalue()


@overload_method(DataFrameType, 'itertuples', inline='always', no_unliteral
    =True)
def itertuples_overload(df, index=True, name='Pandas'):
    check_runtime_cols_unsupported(df, 'DataFrame.itertuples()')
    nhmzs__rirc = dict(index=index, name=name)
    ujv__sfwfp = dict(index=True, name='Pandas')
    check_unsupported_args('DataFrame.itertuples', nhmzs__rirc, ujv__sfwfp,
        package_name='pandas', module_name='DataFrame')

    def _impl(df, index=True, name='Pandas'):
        return bodo.hiframes.pd_dataframe_ext.itertuples_dummy(df)
    return _impl


def itertuples_dummy(df):
    return df


@infer_global(itertuples_dummy)
class ItertuplesDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df, = args
        assert 'Index' not in df.columns
        columns = ('Index',) + df.columns
        gfjw__tsnml = (types.Array(types.int64, 1, 'C'),) + df.data
        jpdsu__iwkou = bodo.hiframes.dataframe_impl.DataFrameTupleIterator(
            columns, gfjw__tsnml)
        return signature(jpdsu__iwkou, *args)


@lower_builtin(itertuples_dummy, types.VarArg(types.Any))
def lower_itertuples_dummy(context, builder, sig, args):
    dmfmq__eesy = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return dmfmq__eesy._getvalue()


def query_dummy(df, expr):
    return df.eval(expr)


@infer_global(query_dummy)
class QueryDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(SeriesType(types.bool_, index=RangeIndexType(types
            .none)), *args)


@lower_builtin(query_dummy, types.VarArg(types.Any))
def lower_query_dummy(context, builder, sig, args):
    dmfmq__eesy = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return dmfmq__eesy._getvalue()


def val_isin_dummy(S, vals):
    return S in vals


def val_notin_dummy(S, vals):
    return S not in vals


@infer_global(val_isin_dummy)
@infer_global(val_notin_dummy)
class ValIsinTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(SeriesType(types.bool_, index=args[0].index), *args)


@lower_builtin(val_isin_dummy, types.VarArg(types.Any))
@lower_builtin(val_notin_dummy, types.VarArg(types.Any))
def lower_val_isin_dummy(context, builder, sig, args):
    dmfmq__eesy = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return dmfmq__eesy._getvalue()


@numba.generated_jit(nopython=True)
def pivot_impl(index_tup, columns_tup, values_tup, pivot_values, index_name,
    columns_name, value_names, check_duplicates=True, parallel=False):
    if not is_overload_constant_bool(check_duplicates):
        raise BodoError(
            'pivot_impl(): check_duplicates must be a constant boolean')
    teuji__boz = get_overload_const_bool(check_duplicates)
    nibjc__flwke = not is_overload_none(value_names)
    pls__xgj = isinstance(values_tup, types.UniTuple)
    if pls__xgj:
        siyo__zuvpu = [to_nullable_type(values_tup.dtype)]
    else:
        siyo__zuvpu = [to_nullable_type(reiex__nlm) for reiex__nlm in
            values_tup]
    erva__nxrvs = 'def impl(\n'
    erva__nxrvs += """    index_tup, columns_tup, values_tup, pivot_values, index_name, columns_name, value_names, check_duplicates=True, parallel=False
"""
    erva__nxrvs += '):\n'
    erva__nxrvs += '    if parallel:\n'
    bcdy__toaal = ', '.join([f'array_to_info(index_tup[{i}])' for i in
        range(len(index_tup))] + [f'array_to_info(columns_tup[{i}])' for i in
        range(len(columns_tup))] + [f'array_to_info(values_tup[{i}])' for i in
        range(len(values_tup))])
    erva__nxrvs += f'        info_list = [{bcdy__toaal}]\n'
    erva__nxrvs += '        cpp_table = arr_info_list_to_table(info_list)\n'
    erva__nxrvs += (
        '        out_cpp_table = shuffle_table(cpp_table, 1, parallel, 0)\n')
    nnfw__yln = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i}), index_tup[{i}])'
         for i in range(len(index_tup))])
    wjjnh__gzdx = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup)}), columns_tup[{i}])'
         for i in range(len(columns_tup))])
    vpsrp__gcdfw = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup) + len(columns_tup)}), values_tup[{i}])'
         for i in range(len(values_tup))])
    erva__nxrvs += f'        index_tup = ({nnfw__yln},)\n'
    erva__nxrvs += f'        columns_tup = ({wjjnh__gzdx},)\n'
    erva__nxrvs += f'        values_tup = ({vpsrp__gcdfw},)\n'
    erva__nxrvs += '        delete_table(cpp_table)\n'
    erva__nxrvs += '        delete_table(out_cpp_table)\n'
    erva__nxrvs += '    index_arr = index_tup[0]\n'
    erva__nxrvs += '    columns_arr = columns_tup[0]\n'
    if pls__xgj:
        erva__nxrvs += '    values_arrs = [arr for arr in values_tup]\n'
    erva__nxrvs += """    unique_index_arr, row_vector = bodo.libs.array_ops.array_unique_vector_map(
"""
    erva__nxrvs += '        index_arr\n'
    erva__nxrvs += '    )\n'
    erva__nxrvs += '    n_rows = len(unique_index_arr)\n'
    erva__nxrvs += '    num_values_arrays = len(values_tup)\n'
    erva__nxrvs += '    n_unique_pivots = len(pivot_values)\n'
    if pls__xgj:
        erva__nxrvs += '    n_cols = num_values_arrays * n_unique_pivots\n'
    else:
        erva__nxrvs += '    n_cols = n_unique_pivots\n'
    erva__nxrvs += '    col_map = {}\n'
    erva__nxrvs += '    for i in range(n_unique_pivots):\n'
    erva__nxrvs += (
        '        if bodo.libs.array_kernels.isna(pivot_values, i):\n')
    erva__nxrvs += '            raise ValueError(\n'
    erva__nxrvs += """                "DataFrame.pivot(): NA values in 'columns' array not supported\"
"""
    erva__nxrvs += '            )\n'
    erva__nxrvs += '        col_map[pivot_values[i]] = i\n'
    euep__ujpg = False
    for i, hjkq__dign in enumerate(siyo__zuvpu):
        if hjkq__dign == bodo.string_array_type:
            euep__ujpg = True
            erva__nxrvs += f"""    len_arrs_{i} = [np.zeros(n_rows, np.int64) for _ in range(n_cols)]
"""
            erva__nxrvs += f'    total_lens_{i} = np.zeros(n_cols, np.int64)\n'
    if euep__ujpg:
        if teuji__boz:
            erva__nxrvs += '    nbytes = (n_rows + 7) >> 3\n'
            erva__nxrvs += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
        erva__nxrvs += '    for i in range(len(columns_arr)):\n'
        erva__nxrvs += '        col_name = columns_arr[i]\n'
        erva__nxrvs += '        pivot_idx = col_map[col_name]\n'
        erva__nxrvs += '        row_idx = row_vector[i]\n'
        if teuji__boz:
            erva__nxrvs += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
            erva__nxrvs += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
            erva__nxrvs += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
            erva__nxrvs += '        else:\n'
            erva__nxrvs += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
        if pls__xgj:
            erva__nxrvs += '        for j in range(num_values_arrays):\n'
            erva__nxrvs += (
                '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
            erva__nxrvs += '            len_arr = len_arrs_0[col_idx]\n'
            erva__nxrvs += '            values_arr = values_arrs[j]\n'
            erva__nxrvs += (
                '            if not bodo.libs.array_kernels.isna(values_arr, i):\n'
                )
            erva__nxrvs += (
                '                len_arr[row_idx] = len(values_arr[i])\n')
            erva__nxrvs += (
                '                total_lens_0[col_idx] += len(values_arr[i])\n'
                )
        else:
            for i, hjkq__dign in enumerate(siyo__zuvpu):
                if hjkq__dign == bodo.string_array_type:
                    erva__nxrvs += f"""        if not bodo.libs.array_kernels.isna(values_tup[{i}], i):
"""
                    erva__nxrvs += f"""            len_arrs_{i}[pivot_idx][row_idx] = len(values_tup[{i}][i])
"""
                    erva__nxrvs += f"""            total_lens_{i}[pivot_idx] += len(values_tup[{i}][i])
"""
    for i, hjkq__dign in enumerate(siyo__zuvpu):
        if hjkq__dign == bodo.string_array_type:
            erva__nxrvs += f'    data_arrs_{i} = [\n'
            erva__nxrvs += (
                '        bodo.libs.str_arr_ext.gen_na_str_array_lens(\n')
            erva__nxrvs += (
                f'            n_rows, total_lens_{i}[i], len_arrs_{i}[i]\n')
            erva__nxrvs += '        )\n'
            erva__nxrvs += '        for i in range(n_cols)\n'
            erva__nxrvs += '    ]\n'
        else:
            erva__nxrvs += f'    data_arrs_{i} = [\n'
            erva__nxrvs += f"""        bodo.libs.array_kernels.gen_na_array(n_rows, data_arr_typ_{i})
"""
            erva__nxrvs += '        for _ in range(n_cols)\n'
            erva__nxrvs += '    ]\n'
    if not euep__ujpg and teuji__boz:
        erva__nxrvs += '    nbytes = (n_rows + 7) >> 3\n'
        erva__nxrvs += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
    erva__nxrvs += '    for i in range(len(columns_arr)):\n'
    erva__nxrvs += '        col_name = columns_arr[i]\n'
    erva__nxrvs += '        pivot_idx = col_map[col_name]\n'
    erva__nxrvs += '        row_idx = row_vector[i]\n'
    if not euep__ujpg and teuji__boz:
        erva__nxrvs += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
        erva__nxrvs += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
        erva__nxrvs += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
        erva__nxrvs += '        else:\n'
        erva__nxrvs += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
    if pls__xgj:
        erva__nxrvs += '        for j in range(num_values_arrays):\n'
        erva__nxrvs += (
            '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
        erva__nxrvs += '            col_arr = data_arrs_0[col_idx]\n'
        erva__nxrvs += '            values_arr = values_arrs[j]\n'
        erva__nxrvs += (
            '            if bodo.libs.array_kernels.isna(values_arr, i):\n')
        erva__nxrvs += (
            '                bodo.libs.array_kernels.setna(col_arr, row_idx)\n'
            )
        erva__nxrvs += '            else:\n'
        erva__nxrvs += '                col_arr[row_idx] = values_arr[i]\n'
    else:
        for i, hjkq__dign in enumerate(siyo__zuvpu):
            erva__nxrvs += f'        col_arr_{i} = data_arrs_{i}[pivot_idx]\n'
            erva__nxrvs += (
                f'        if bodo.libs.array_kernels.isna(values_tup[{i}], i):\n'
                )
            erva__nxrvs += (
                f'            bodo.libs.array_kernels.setna(col_arr_{i}, row_idx)\n'
                )
            erva__nxrvs += f'        else:\n'
            erva__nxrvs += (
                f'            col_arr_{i}[row_idx] = values_tup[{i}][i]\n')
    erva__nxrvs += """    index = bodo.utils.conversion.index_from_array(unique_index_arr, index_name)
"""
    if nibjc__flwke:
        erva__nxrvs += '    num_rows = len(value_names) * len(pivot_values)\n'
        if value_names == bodo.string_array_type:
            erva__nxrvs += '    total_chars = 0\n'
            erva__nxrvs += '    for i in range(len(value_names)):\n'
            erva__nxrvs += '        total_chars += len(value_names[i])\n'
            erva__nxrvs += """    new_value_names = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(pivot_values))
"""
        else:
            erva__nxrvs += """    new_value_names = bodo.utils.utils.alloc_type(num_rows, value_names, (-1,))
"""
        if pivot_values == bodo.string_array_type:
            erva__nxrvs += '    total_chars = 0\n'
            erva__nxrvs += '    for i in range(len(pivot_values)):\n'
            erva__nxrvs += '        total_chars += len(pivot_values[i])\n'
            erva__nxrvs += """    new_pivot_values = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(value_names))
"""
        else:
            erva__nxrvs += """    new_pivot_values = bodo.utils.utils.alloc_type(num_rows, pivot_values, (-1,))
"""
        erva__nxrvs += '    for i in range(len(value_names)):\n'
        erva__nxrvs += '        for j in range(len(pivot_values)):\n'
        erva__nxrvs += """            new_value_names[(i * len(pivot_values)) + j] = value_names[i]
"""
        erva__nxrvs += """            new_pivot_values[(i * len(pivot_values)) + j] = pivot_values[j]
"""
        erva__nxrvs += """    column_index = bodo.hiframes.pd_multi_index_ext.init_multi_index((new_value_names, new_pivot_values), (None, columns_name), None)
"""
    else:
        erva__nxrvs += """    column_index =  bodo.utils.conversion.index_from_array(pivot_values, columns_name)
"""
    yelhz__fuhg = ', '.join(f'data_arrs_{i}' for i in range(len(siyo__zuvpu)))
    erva__nxrvs += f"""    table = bodo.hiframes.table.init_runtime_table_from_lists(({yelhz__fuhg},), n_rows)
"""
    erva__nxrvs += (
        '    return bodo.hiframes.pd_dataframe_ext.init_runtime_cols_dataframe(\n'
        )
    erva__nxrvs += '        (table,), index, column_index\n'
    erva__nxrvs += '    )\n'
    mintx__azc = {}
    bgx__gztj = {f'data_arr_typ_{i}': hjkq__dign for i, hjkq__dign in
        enumerate(siyo__zuvpu)}
    zaf__qaphe = {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'info_from_table': info_from_table, **bgx__gztj}
    exec(erva__nxrvs, zaf__qaphe, mintx__azc)
    impl = mintx__azc['impl']
    return impl


def gen_pandas_parquet_metadata(df, write_non_range_index_to_metadata,
    write_rangeindex_to_metadata, partition_cols=None):
    tgycc__bedc = {}
    tgycc__bedc['columns'] = []
    if partition_cols is None:
        partition_cols = []
    for col_name, kvlg__rsnvu in zip(df.columns, df.data):
        if col_name in partition_cols:
            continue
        if isinstance(kvlg__rsnvu, types.Array
            ) or kvlg__rsnvu == boolean_array:
            ssj__cpqhi = szim__kkyb = kvlg__rsnvu.dtype.name
            if szim__kkyb.startswith('datetime'):
                ssj__cpqhi = 'datetime'
        elif kvlg__rsnvu == string_array_type:
            ssj__cpqhi = 'unicode'
            szim__kkyb = 'object'
        elif kvlg__rsnvu == binary_array_type:
            ssj__cpqhi = 'bytes'
            szim__kkyb = 'object'
        elif isinstance(kvlg__rsnvu, DecimalArrayType):
            ssj__cpqhi = szim__kkyb = 'object'
        elif isinstance(kvlg__rsnvu, IntegerArrayType):
            tlb__gsacg = kvlg__rsnvu.dtype.name
            if tlb__gsacg.startswith('int'):
                ssj__cpqhi = 'Int' + tlb__gsacg[3:]
            elif tlb__gsacg.startswith('uint'):
                ssj__cpqhi = 'UInt' + tlb__gsacg[4:]
            else:
                raise BodoError(
                    'to_parquet(): unknown dtype in nullable Integer column {} {}'
                    .format(col_name, kvlg__rsnvu))
            szim__kkyb = kvlg__rsnvu.dtype.name
        elif kvlg__rsnvu == datetime_date_array_type:
            ssj__cpqhi = 'datetime'
            szim__kkyb = 'object'
        elif isinstance(kvlg__rsnvu, (StructArrayType, ArrayItemArrayType)):
            ssj__cpqhi = 'object'
            szim__kkyb = 'object'
        else:
            raise BodoError(
                'to_parquet(): unsupported column type for metadata generation : {} {}'
                .format(col_name, kvlg__rsnvu))
        hml__owob = {'name': col_name, 'field_name': col_name,
            'pandas_type': ssj__cpqhi, 'numpy_type': szim__kkyb, 'metadata':
            None}
        tgycc__bedc['columns'].append(hml__owob)
    if write_non_range_index_to_metadata:
        if isinstance(df.index, MultiIndexType):
            raise BodoError('to_parquet: MultiIndex not supported yet')
        if 'none' in df.index.name:
            cfafq__ehe = '__index_level_0__'
            yhgvj__xlkza = None
        else:
            cfafq__ehe = '%s'
            yhgvj__xlkza = '%s'
        tgycc__bedc['index_columns'] = [cfafq__ehe]
        tgycc__bedc['columns'].append({'name': yhgvj__xlkza, 'field_name':
            cfafq__ehe, 'pandas_type': df.index.pandas_type_name,
            'numpy_type': df.index.numpy_type_name, 'metadata': None})
    elif write_rangeindex_to_metadata:
        tgycc__bedc['index_columns'] = [{'kind': 'range', 'name': '%s',
            'start': '%d', 'stop': '%d', 'step': '%d'}]
    else:
        tgycc__bedc['index_columns'] = []
    tgycc__bedc['pandas_version'] = pd.__version__
    return tgycc__bedc


@overload_method(DataFrameType, 'to_parquet', no_unliteral=True)
def to_parquet_overload(df, fname, engine='auto', compression='snappy',
    index=None, partition_cols=None, storage_options=None, _is_parallel=False):
    check_runtime_cols_unsupported(df, 'DataFrame.to_parquet()')
    check_unsupported_args('DataFrame.to_parquet', {'storage_options':
        storage_options}, {'storage_options': None}, package_name='pandas',
        module_name='IO')
    if not is_overload_none(engine) and get_overload_const_str(engine) not in (
        'auto', 'pyarrow'):
        raise BodoError('DataFrame.to_parquet(): only pyarrow engine supported'
            )
    if not is_overload_none(compression) and get_overload_const_str(compression
        ) not in {'snappy', 'gzip', 'brotli'}:
        raise BodoError('to_parquet(): Unsupported compression: ' + str(
            get_overload_const_str(compression)))
    if not is_overload_none(partition_cols):
        partition_cols = get_overload_const_list(partition_cols)
        uksb__qem = []
        for ydgd__ddsg in partition_cols:
            try:
                idx = df.columns.index(ydgd__ddsg)
            except ValueError as rcd__ubs:
                raise BodoError(
                    f'Partition column {ydgd__ddsg} is not in dataframe')
            uksb__qem.append(idx)
    else:
        partition_cols = None
    if not is_overload_none(index) and not is_overload_constant_bool(index):
        raise BodoError('to_parquet(): index must be a constant bool or None')
    from bodo.io.parquet_pio import parquet_write_table_cpp, parquet_write_table_partitioned_cpp
    lwl__jxpya = isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType
        )
    itoqm__gzs = df.index is not None and (is_overload_true(_is_parallel) or
        not is_overload_true(_is_parallel) and not lwl__jxpya)
    write_non_range_index_to_metadata = is_overload_true(index
        ) or is_overload_none(index) and (not lwl__jxpya or
        is_overload_true(_is_parallel))
    write_rangeindex_to_metadata = is_overload_none(index
        ) and lwl__jxpya and not is_overload_true(_is_parallel)
    nysrn__jpy = json.dumps(gen_pandas_parquet_metadata(df,
        write_non_range_index_to_metadata, write_rangeindex_to_metadata,
        partition_cols=partition_cols))
    if not is_overload_true(_is_parallel) and lwl__jxpya:
        nysrn__jpy = nysrn__jpy.replace('"%d"', '%d')
        if df.index.name == 'RangeIndexType(none)':
            nysrn__jpy = nysrn__jpy.replace('"%s"', '%s')
    xlyp__six = ', '.join(
        'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
        .format(i) for i in range(len(df.columns)))
    erva__nxrvs = """def df_to_parquet(df, fname, engine='auto', compression='snappy', index=None, partition_cols=None, storage_options=None, _is_parallel=False):
"""
    if df.is_table_format:
        erva__nxrvs += (
            '    table = py_table_to_cpp_table(get_dataframe_table(df), py_table_typ)\n'
            )
    else:
        erva__nxrvs += '    info_list = [{}]\n'.format(xlyp__six)
        erva__nxrvs += '    table = arr_info_list_to_table(info_list)\n'
    erva__nxrvs += '    col_names = array_to_info(col_names_arr)\n'
    if is_overload_true(index) or is_overload_none(index) and itoqm__gzs:
        erva__nxrvs += """    index_col = array_to_info(index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
        rcrvk__voih = True
    else:
        erva__nxrvs += '    index_col = array_to_info(np.empty(0))\n'
        rcrvk__voih = False
    erva__nxrvs += '    metadata = """' + nysrn__jpy + '"""\n'
    erva__nxrvs += '    if compression is None:\n'
    erva__nxrvs += "        compression = 'none'\n"
    erva__nxrvs += '    if df.index.name is not None:\n'
    erva__nxrvs += '        name_ptr = df.index.name\n'
    erva__nxrvs += '    else:\n'
    erva__nxrvs += "        name_ptr = 'null'\n"
    erva__nxrvs += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel=_is_parallel)
"""
    tzro__bkgji = None
    if partition_cols:
        tzro__bkgji = pd.array([col_name for col_name in df.columns if 
            col_name not in partition_cols])
        lojz__trusp = ', '.join(
            f'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype.categories.values)'
             for i in range(len(df.columns)) if isinstance(df.data[i],
            CategoricalArrayType) and i in uksb__qem)
        if lojz__trusp:
            erva__nxrvs += '    cat_info_list = [{}]\n'.format(lojz__trusp)
            erva__nxrvs += (
                '    cat_table = arr_info_list_to_table(cat_info_list)\n')
        else:
            erva__nxrvs += '    cat_table = table\n'
        erva__nxrvs += (
            '    col_names_no_partitions = array_to_info(col_names_no_parts_arr)\n'
            )
        erva__nxrvs += (
            f'    part_cols_idxs = np.array({uksb__qem}, dtype=np.int32)\n')
        erva__nxrvs += (
            '    parquet_write_table_partitioned_cpp(unicode_to_utf8(fname),\n'
            )
        erva__nxrvs += """                            table, col_names, col_names_no_partitions, cat_table,
"""
        erva__nxrvs += (
            '                            part_cols_idxs.ctypes, len(part_cols_idxs),\n'
            )
        erva__nxrvs += (
            '                            unicode_to_utf8(compression),\n')
        erva__nxrvs += '                            _is_parallel,\n'
        erva__nxrvs += (
            '                            unicode_to_utf8(bucket_region))\n')
        erva__nxrvs += '    delete_table_decref_arrays(table)\n'
        erva__nxrvs += '    delete_info_decref_array(index_col)\n'
        erva__nxrvs += (
            '    delete_info_decref_array(col_names_no_partitions)\n')
        erva__nxrvs += '    delete_info_decref_array(col_names)\n'
        if lojz__trusp:
            erva__nxrvs += '    delete_table_decref_arrays(cat_table)\n'
    elif write_rangeindex_to_metadata:
        erva__nxrvs += '    parquet_write_table_cpp(unicode_to_utf8(fname),\n'
        erva__nxrvs += (
            '                            table, col_names, index_col,\n')
        erva__nxrvs += '                            ' + str(rcrvk__voih
            ) + ',\n'
        erva__nxrvs += (
            '                            unicode_to_utf8(metadata),\n')
        erva__nxrvs += (
            '                            unicode_to_utf8(compression),\n')
        erva__nxrvs += (
            '                            _is_parallel, 1, df.index.start,\n')
        erva__nxrvs += (
            '                            df.index.stop, df.index.step,\n')
        erva__nxrvs += (
            '                            unicode_to_utf8(name_ptr),\n')
        erva__nxrvs += (
            '                            unicode_to_utf8(bucket_region))\n')
        erva__nxrvs += '    delete_table_decref_arrays(table)\n'
        erva__nxrvs += '    delete_info_decref_array(index_col)\n'
        erva__nxrvs += '    delete_info_decref_array(col_names)\n'
    else:
        erva__nxrvs += '    parquet_write_table_cpp(unicode_to_utf8(fname),\n'
        erva__nxrvs += (
            '                            table, col_names, index_col,\n')
        erva__nxrvs += '                            ' + str(rcrvk__voih
            ) + ',\n'
        erva__nxrvs += (
            '                            unicode_to_utf8(metadata),\n')
        erva__nxrvs += (
            '                            unicode_to_utf8(compression),\n')
        erva__nxrvs += (
            '                            _is_parallel, 0, 0, 0, 0,\n')
        erva__nxrvs += (
            '                            unicode_to_utf8(name_ptr),\n')
        erva__nxrvs += (
            '                            unicode_to_utf8(bucket_region))\n')
        erva__nxrvs += '    delete_table_decref_arrays(table)\n'
        erva__nxrvs += '    delete_info_decref_array(index_col)\n'
        erva__nxrvs += '    delete_info_decref_array(col_names)\n'
    mintx__azc = {}
    exec(erva__nxrvs, {'np': np, 'bodo': bodo, 'unicode_to_utf8':
        unicode_to_utf8, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'str_arr_from_sequence': str_arr_from_sequence,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'parquet_write_table_partitioned_cpp':
        parquet_write_table_partitioned_cpp, 'index_to_array':
        index_to_array, 'delete_info_decref_array':
        delete_info_decref_array, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'col_names_arr': pd.array(df.columns),
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'get_dataframe_table': get_dataframe_table,
        'col_names_no_parts_arr': tzro__bkgji}, mintx__azc)
    xykn__fupr = mintx__azc['df_to_parquet']
    return xykn__fupr


def to_sql_exception_guard(df, name, con, schema=None, if_exists='fail',
    index=True, index_label=None, chunksize=None, dtype=None, method=None):
    rwp__kbkow = 'all_ok'
    try:
        df.to_sql(name, con, schema, if_exists, index, index_label,
            chunksize, dtype, method)
    except ValueError as phrh__nfumm:
        rwp__kbkow = phrh__nfumm.args[0]
    return rwp__kbkow


@numba.njit
def to_sql_exception_guard_encaps(df, name, con, schema=None, if_exists=
    'fail', index=True, index_label=None, chunksize=None, dtype=None,
    method=None):
    with numba.objmode(out='unicode_type'):
        out = to_sql_exception_guard(df, name, con, schema, if_exists,
            index, index_label, chunksize, dtype, method)
    return out


@overload_method(DataFrameType, 'to_sql')
def to_sql_overload(df, name, con, schema=None, if_exists='fail', index=
    True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_parallel=False):
    check_runtime_cols_unsupported(df, 'DataFrame.to_sql()')
    nhmzs__rirc = dict(chunksize=chunksize)
    ujv__sfwfp = dict(chunksize=None)
    check_unsupported_args('to_sql', nhmzs__rirc, ujv__sfwfp, package_name=
        'pandas', module_name='IO')

    def _impl(df, name, con, schema=None, if_exists='fail', index=True,
        index_label=None, chunksize=None, dtype=None, method=None,
        _is_parallel=False):
        iej__gsu = bodo.libs.distributed_api.get_rank()
        rwp__kbkow = 'unset'
        if iej__gsu != 0:
            if_exists = 'append'
            rwp__kbkow = bcast_scalar(rwp__kbkow)
        if iej__gsu == 0 or _is_parallel and rwp__kbkow == 'all_ok':
            rwp__kbkow = to_sql_exception_guard_encaps(df, name, con,
                schema, if_exists, index, index_label, chunksize, dtype, method
                )
        if iej__gsu == 0:
            rwp__kbkow = bcast_scalar(rwp__kbkow)
        if rwp__kbkow != 'all_ok':
            print('err_msg=', rwp__kbkow)
            raise ValueError('error in to_sql() operation')
    return _impl


@overload_method(DataFrameType, 'to_csv', no_unliteral=True)
def to_csv_overload(df, path_or_buf=None, sep=',', na_rep='', float_format=
    None, columns=None, header=True, index=True, index_label=None, mode='w',
    encoding=None, compression=None, quoting=None, quotechar='"',
    line_terminator=None, chunksize=None, date_format=None, doublequote=
    True, escapechar=None, decimal='.', errors='strict', storage_options=None):
    check_runtime_cols_unsupported(df, 'DataFrame.to_csv()')
    check_unsupported_args('DataFrame.to_csv', {'encoding': encoding,
        'mode': mode, 'errors': errors, 'storage_options': storage_options},
        {'encoding': None, 'mode': 'w', 'errors': 'strict',
        'storage_options': None}, package_name='pandas', module_name='IO')
    if not (is_overload_none(path_or_buf) or is_overload_constant_str(
        path_or_buf) or path_or_buf == string_type):
        raise BodoError(
            "DataFrame.to_csv(): 'path_or_buf' argument should be None or string"
            )
    if not is_overload_none(compression):
        raise BodoError(
            "DataFrame.to_csv(): 'compression' argument supports only None, which is the default in JIT code."
            )
    if is_overload_constant_str(path_or_buf):
        aklbc__mwvbl = get_overload_const_str(path_or_buf)
        if aklbc__mwvbl.endswith(('.gz', '.bz2', '.zip', '.xz')):
            import warnings
            from bodo.utils.typing import BodoWarning
            warnings.warn(BodoWarning(
                "DataFrame.to_csv(): 'compression' argument defaults to None in JIT code, which is the only supported value."
                ))
    if isinstance(columns, types.List):
        raise BodoError(
            "DataFrame.to_csv(): 'columns' argument must not be list type. Please convert to tuple type."
            )
    if is_overload_none(path_or_buf):

        def _impl(df, path_or_buf=None, sep=',', na_rep='', float_format=
            None, columns=None, header=True, index=True, index_label=None,
            mode='w', encoding=None, compression=None, quoting=None,
            quotechar='"', line_terminator=None, chunksize=None,
            date_format=None, doublequote=True, escapechar=None, decimal=
            '.', errors='strict', storage_options=None):
            with numba.objmode(D='unicode_type'):
                D = df.to_csv(path_or_buf, sep, na_rep, float_format,
                    columns, header, index, index_label, mode, encoding,
                    compression, quoting, quotechar, line_terminator,
                    chunksize, date_format, doublequote, escapechar,
                    decimal, errors, storage_options)
            return D
        return _impl

    def _impl(df, path_or_buf=None, sep=',', na_rep='', float_format=None,
        columns=None, header=True, index=True, index_label=None, mode='w',
        encoding=None, compression=None, quoting=None, quotechar='"',
        line_terminator=None, chunksize=None, date_format=None, doublequote
        =True, escapechar=None, decimal='.', errors='strict',
        storage_options=None):
        with numba.objmode(D='unicode_type'):
            D = df.to_csv(None, sep, na_rep, float_format, columns, header,
                index, index_label, mode, encoding, compression, quoting,
                quotechar, line_terminator, chunksize, date_format,
                doublequote, escapechar, decimal, errors, storage_options)
        bodo.io.fs_io.csv_write(path_or_buf, D)
    return _impl


@overload_method(DataFrameType, 'to_json', no_unliteral=True)
def to_json_overload(df, path_or_buf=None, orient='columns', date_format=
    None, double_precision=10, force_ascii=True, date_unit='ms',
    default_handler=None, lines=False, compression='infer', index=True,
    indent=None, storage_options=None):
    check_runtime_cols_unsupported(df, 'DataFrame.to_json()')
    check_unsupported_args('DataFrame.to_json', {'storage_options':
        storage_options}, {'storage_options': None}, package_name='pandas',
        module_name='IO')
    if path_or_buf is None or path_or_buf == types.none:

        def _impl(df, path_or_buf=None, orient='columns', date_format=None,
            double_precision=10, force_ascii=True, date_unit='ms',
            default_handler=None, lines=False, compression='infer', index=
            True, indent=None, storage_options=None):
            with numba.objmode(D='unicode_type'):
                D = df.to_json(path_or_buf, orient, date_format,
                    double_precision, force_ascii, date_unit,
                    default_handler, lines, compression, index, indent,
                    storage_options)
            return D
        return _impl

    def _impl(df, path_or_buf=None, orient='columns', date_format=None,
        double_precision=10, force_ascii=True, date_unit='ms',
        default_handler=None, lines=False, compression='infer', index=True,
        indent=None, storage_options=None):
        with numba.objmode(D='unicode_type'):
            D = df.to_json(None, orient, date_format, double_precision,
                force_ascii, date_unit, default_handler, lines, compression,
                index, indent, storage_options)
        haqq__yejvk = bodo.io.fs_io.get_s3_bucket_region_njit(path_or_buf,
            parallel=False)
        if lines and orient == 'records':
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, True,
                unicode_to_utf8(haqq__yejvk))
            bodo.utils.utils.check_and_propagate_cpp_exception()
        else:
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, False,
                unicode_to_utf8(haqq__yejvk))
            bodo.utils.utils.check_and_propagate_cpp_exception()
    return _impl


@overload(pd.get_dummies, inline='always', no_unliteral=True)
def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=
    None, sparse=False, drop_first=False, dtype=None):
    wtk__xmo = {'prefix': prefix, 'prefix_sep': prefix_sep, 'dummy_na':
        dummy_na, 'columns': columns, 'sparse': sparse, 'drop_first':
        drop_first, 'dtype': dtype}
    bbhm__rvef = {'prefix': None, 'prefix_sep': '_', 'dummy_na': False,
        'columns': None, 'sparse': False, 'drop_first': False, 'dtype': None}
    check_unsupported_args('pandas.get_dummies', wtk__xmo, bbhm__rvef,
        package_name='pandas', module_name='General')
    if not categorical_can_construct_dataframe(data):
        raise BodoError(
            'pandas.get_dummies() only support categorical data types with explicitly known categories'
            )
    erva__nxrvs = """def impl(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None,):
"""
    if isinstance(data, SeriesType):
        awf__vsiij = data.data.dtype.categories
        erva__nxrvs += (
            '  data_values = bodo.hiframes.pd_series_ext.get_series_data(data)\n'
            )
    else:
        awf__vsiij = data.dtype.categories
        erva__nxrvs += '  data_values = data\n'
    yet__vjub = len(awf__vsiij)
    erva__nxrvs += """  codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(data_values)
"""
    erva__nxrvs += '  numba.parfors.parfor.init_prange()\n'
    erva__nxrvs += '  n = len(data_values)\n'
    for i in range(yet__vjub):
        erva__nxrvs += '  data_arr_{} = np.empty(n, np.uint8)\n'.format(i)
    erva__nxrvs += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    erva__nxrvs += '      if bodo.libs.array_kernels.isna(data_values, i):\n'
    for wzhzw__xkvg in range(yet__vjub):
        erva__nxrvs += '          data_arr_{}[i] = 0\n'.format(wzhzw__xkvg)
    erva__nxrvs += '      else:\n'
    for jnz__ewa in range(yet__vjub):
        erva__nxrvs += '          data_arr_{0}[i] = codes[i] == {0}\n'.format(
            jnz__ewa)
    xlyp__six = ', '.join(f'data_arr_{i}' for i in range(yet__vjub))
    index = 'bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)'
    if isinstance(awf__vsiij[0], np.datetime64):
        awf__vsiij = tuple(pd.Timestamp(jil__onn) for jil__onn in awf__vsiij)
    return bodo.hiframes.dataframe_impl._gen_init_df(erva__nxrvs,
        awf__vsiij, xlyp__six, index)


def categorical_can_construct_dataframe(val):
    if isinstance(val, CategoricalArrayType):
        return val.dtype.categories is not None
    elif isinstance(val, SeriesType) and isinstance(val.data,
        CategoricalArrayType):
        return val.data.dtype.categories is not None
    return False


def handle_inplace_df_type_change(inplace, _bodo_transformed, func_name):
    if is_overload_false(_bodo_transformed
        ) and bodo.transforms.typing_pass.in_partial_typing and (
        is_overload_true(inplace) or not is_overload_constant_bool(inplace)):
        bodo.transforms.typing_pass.typing_transform_required = True
        raise Exception('DataFrame.{}(): transform necessary for inplace'.
            format(func_name))


pd_unsupported = (pd.read_pickle, pd.read_table, pd.read_fwf, pd.
    read_clipboard, pd.ExcelFile, pd.read_html, pd.read_xml, pd.read_hdf,
    pd.read_feather, pd.read_orc, pd.read_sas, pd.read_spss, pd.
    read_sql_table, pd.read_sql_query, pd.read_gbq, pd.read_stata, pd.
    ExcelWriter, pd.json_normalize, pd.melt, pd.pivot, pd.pivot_table, pd.
    merge_ordered, pd.factorize, pd.unique, pd.wide_to_long, pd.bdate_range,
    pd.period_range, pd.infer_freq, pd.interval_range, pd.eval, pd.test, pd
    .Grouper)
pd_util_unsupported = pd.util.hash_array, pd.util.hash_pandas_object
dataframe_unsupported = ['set_flags', 'convert_dtypes', 'bool', '__iter__',
    'items', 'iteritems', 'keys', 'iterrows', 'lookup', 'pop', 'xs', 'get',
    'where', 'mask', 'add', 'sub', 'mul', 'div', 'truediv', 'floordiv',
    'mod', 'pow', 'dot', 'radd', 'rsub', 'rmul', 'rdiv', 'rtruediv',
    'rfloordiv', 'rmod', 'rpow', 'lt', 'gt', 'le', 'ge', 'ne', 'eq',
    'combine', 'combine_first', 'subtract', 'divide', 'multiply',
    'applymap', 'agg', 'aggregate', 'transform', 'expanding', 'ewm', 'all',
    'any', 'clip', 'corrwith', 'cummax', 'cummin', 'eval', 'kurt',
    'kurtosis', 'mad', 'mode', 'rank', 'round', 'sem', 'skew',
    'value_counts', 'add_prefix', 'add_suffix', 'align', 'at_time',
    'between_time', 'equals', 'reindex', 'reindex_like', 'rename_axis',
    'set_axis', 'truncate', 'backfill', 'bfill', 'ffill', 'interpolate',
    'pad', 'droplevel', 'reorder_levels', 'nlargest', 'nsmallest',
    'swaplevel', 'stack', 'unstack', 'swapaxes', 'melt', 'explode',
    'squeeze', 'to_xarray', 'T', 'transpose', 'compare', 'update', 'asfreq',
    'asof', 'slice_shift', 'tshift', 'first_valid_index',
    'last_valid_index', 'resample', 'to_period', 'to_timestamp',
    'tz_convert', 'tz_localize', 'boxplot', 'hist', 'from_dict',
    'from_records', 'to_pickle', 'to_hdf', 'to_dict', 'to_excel', 'to_html',
    'to_feather', 'to_latex', 'to_stata', 'to_gbq', 'to_records',
    'to_clipboard', 'to_markdown', 'to_xml']
dataframe_unsupported_attrs = ['at', 'attrs', 'axes', 'flags', 'style',
    'sparse']


def _install_pd_unsupported(mod_name, pd_unsupported):
    for gkmq__gas in pd_unsupported:
        fname = mod_name + '.' + gkmq__gas.__name__
        overload(gkmq__gas, no_unliteral=True)(create_unsupported_overload(
            fname))


def _install_dataframe_unsupported():
    for gycrb__mwpiz in dataframe_unsupported_attrs:
        qyr__bqk = 'DataFrame.' + gycrb__mwpiz
        overload_attribute(DataFrameType, gycrb__mwpiz)(
            create_unsupported_overload(qyr__bqk))
    for fname in dataframe_unsupported:
        qyr__bqk = 'DataFrame.' + fname + '()'
        overload_method(DataFrameType, fname)(create_unsupported_overload(
            qyr__bqk))


_install_pd_unsupported('pandas', pd_unsupported)
_install_pd_unsupported('pandas.util', pd_util_unsupported)
_install_dataframe_unsupported()
