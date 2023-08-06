"""Support for Pandas Groupby operations
"""
import operator
from enum import Enum
import numba
import numpy as np
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.core.registry import CPUDispatcher
from numba.core.typing.templates import AbstractTemplate, bound_function, infer_global, signature
from numba.extending import infer, infer_getattr, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import NumericIndexType, RangeIndexType
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_table, delete_table_decref_arrays, get_groupby_labels, get_shuffle_info, info_from_table, info_to_array, reverse_shuffle_table, shuffle_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.decimal_arr_ext import Decimal128Type
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.transform import gen_const_tup, get_call_expr_arg, get_const_func_output_type
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, dtype_to_array_type, get_index_data_arr_types, get_index_name_types, get_literal_value, get_overload_const_bool, get_overload_const_func, get_overload_const_list, get_overload_const_str, get_overload_constant_dict, get_udf_error_msg, get_udf_out_arr_type, is_dtype_nullable, is_literal_type, is_overload_constant_bool, is_overload_constant_dict, is_overload_constant_list, is_overload_constant_str, is_overload_none, is_overload_true, list_cumulative, raise_bodo_error, raise_const_error
from bodo.utils.utils import dt_err, is_expr


class DataFrameGroupByType(types.Type):

    def __init__(self, df_type, keys, selection, as_index, dropna=True,
        explicit_select=False, series_select=False):
        self.df_type = df_type
        self.keys = keys
        self.selection = selection
        self.as_index = as_index
        self.dropna = dropna
        self.explicit_select = explicit_select
        self.series_select = series_select
        super(DataFrameGroupByType, self).__init__(name=
            f'DataFrameGroupBy({df_type}, {keys}, {selection}, {as_index}, {dropna}, {explicit_select}, {series_select})'
            )

    def copy(self):
        return DataFrameGroupByType(self.df_type, self.keys, self.selection,
            self.as_index, self.dropna, self.explicit_select, self.
            series_select)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(DataFrameGroupByType)
class GroupbyModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wkdi__agc = [('obj', fe_type.df_type)]
        super(GroupbyModel, self).__init__(dmm, fe_type, wkdi__agc)


make_attribute_wrapper(DataFrameGroupByType, 'obj', 'obj')


def validate_udf(func_name, func):
    if not isinstance(func, (types.functions.MakeFunctionLiteral, bodo.
        utils.typing.FunctionLiteral, types.Dispatcher, CPUDispatcher)):
        raise_const_error(
            f"Groupby.{func_name}: 'func' must be user defined function")


@intrinsic
def init_groupby(typingctx, obj_type, by_type, as_index_type=None,
    dropna_type=None):

    def codegen(context, builder, signature, args):
        rrz__nnksp = args[0]
        wrypa__tuix = signature.return_type
        aszib__kgt = cgutils.create_struct_proxy(wrypa__tuix)(context, builder)
        aszib__kgt.obj = rrz__nnksp
        context.nrt.incref(builder, signature.args[0], rrz__nnksp)
        return aszib__kgt._getvalue()
    if is_overload_constant_list(by_type):
        keys = tuple(get_overload_const_list(by_type))
    elif is_literal_type(by_type):
        keys = get_literal_value(by_type),
    else:
        assert False, 'Reached unreachable code in init_groupby; there is an validate_groupby_spec'
    selection = list(obj_type.columns)
    for ouq__iro in keys:
        selection.remove(ouq__iro)
    if is_overload_constant_bool(as_index_type):
        as_index = is_overload_true(as_index_type)
    else:
        as_index = True
    if is_overload_constant_bool(dropna_type):
        dropna = is_overload_true(dropna_type)
    else:
        dropna = True
    wrypa__tuix = DataFrameGroupByType(obj_type, keys, tuple(selection),
        as_index, dropna, False)
    return wrypa__tuix(obj_type, by_type, as_index_type, dropna_type), codegen


@lower_builtin('groupby.count', types.VarArg(types.Any))
@lower_builtin('groupby.size', types.VarArg(types.Any))
@lower_builtin('groupby.apply', types.VarArg(types.Any))
@lower_builtin('groupby.agg', types.VarArg(types.Any))
def lower_groupby_count_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


@infer
class StaticGetItemDataFrameGroupBy(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        grpby, zdgow__dzvi = args
        if isinstance(grpby, DataFrameGroupByType):
            series_select = False
            if isinstance(zdgow__dzvi, (tuple, list)):
                if len(set(zdgow__dzvi).difference(set(grpby.df_type.columns))
                    ) > 0:
                    raise_const_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(set(zdgow__dzvi).difference(set(grpby.
                        df_type.columns))))
                selection = zdgow__dzvi
            else:
                if zdgow__dzvi not in grpby.df_type.columns:
                    raise_const_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(zdgow__dzvi))
                selection = zdgow__dzvi,
                series_select = True
            vvwx__grbfi = DataFrameGroupByType(grpby.df_type, grpby.keys,
                selection, grpby.as_index, grpby.dropna, True, series_select)
            return signature(vvwx__grbfi, *args)


@infer_global(operator.getitem)
class GetItemDataFrameGroupBy(AbstractTemplate):

    def generic(self, args, kws):
        grpby, zdgow__dzvi = args
        if isinstance(grpby, DataFrameGroupByType) and is_literal_type(
            zdgow__dzvi):
            vvwx__grbfi = StaticGetItemDataFrameGroupBy.generic(self, (
                grpby, get_literal_value(zdgow__dzvi)), {}).return_type
            return signature(vvwx__grbfi, *args)


GetItemDataFrameGroupBy.prefer_literal = True


@lower_builtin('static_getitem', DataFrameGroupByType, types.Any)
@lower_builtin(operator.getitem, DataFrameGroupByType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


def get_groupby_output_dtype(arr_type, func_name, index_type=None):
    eceb__tqqv = arr_type == ArrayItemArrayType(string_array_type)
    syj__rhs = arr_type.dtype
    if isinstance(syj__rhs, bodo.hiframes.datetime_timedelta_ext.
        DatetimeTimeDeltaType):
        raise BodoError(
            f"""column type of {syj__rhs} is not supported in groupby built-in function {func_name}.
{dt_err}"""
            )
    if func_name == 'median' and not isinstance(syj__rhs, (Decimal128Type,
        types.Float, types.Integer)):
        return (None,
            'For median, only column of integer, float or Decimal type are allowed'
            )
    if func_name in ('first', 'last', 'sum', 'prod', 'min', 'max', 'count',
        'nunique', 'head') and isinstance(arr_type, (TupleArrayType,
        ArrayItemArrayType)):
        return (None,
            f'column type of list/tuple of {syj__rhs} is not supported in groupby built-in function {func_name}'
            )
    if func_name in {'median', 'mean', 'var', 'std'} and isinstance(syj__rhs,
        (Decimal128Type, types.Integer, types.Float)):
        return dtype_to_array_type(types.float64), 'ok'
    if not isinstance(syj__rhs, (types.Integer, types.Float, types.Boolean)):
        if eceb__tqqv or syj__rhs == types.unicode_type:
            if func_name not in {'count', 'nunique', 'min', 'max', 'sum',
                'first', 'last', 'head'}:
                return (None,
                    f'column type of strings or list of strings is not supported in groupby built-in function {func_name}'
                    )
        else:
            if isinstance(syj__rhs, bodo.PDCategoricalDtype):
                if func_name in ('min', 'max') and not syj__rhs.ordered:
                    return (None,
                        f'categorical column must be ordered in groupby built-in function {func_name}'
                        )
            if func_name not in {'count', 'nunique', 'min', 'max', 'first',
                'last', 'head'}:
                return (None,
                    f'column type of {syj__rhs} is not supported in groupby built-in function {func_name}'
                    )
    if isinstance(syj__rhs, types.Boolean) and func_name in {'cumsum',
        'sum', 'mean', 'std', 'var'}:
        return (None,
            f'groupby built-in functions {func_name} does not support boolean column'
            )
    if func_name in {'idxmin', 'idxmax'}:
        return dtype_to_array_type(get_index_data_arr_types(index_type)[0].
            dtype), 'ok'
    if func_name in {'count', 'nunique'}:
        return dtype_to_array_type(types.int64), 'ok'
    else:
        return arr_type, 'ok'


def get_pivot_output_dtype(arr_type, func_name, index_type=None):
    syj__rhs = arr_type.dtype
    if func_name in {'count'}:
        return IntDtype(types.int64)
    if func_name in {'sum', 'prod', 'min', 'max'}:
        if func_name in {'sum', 'prod'} and not isinstance(syj__rhs, (types
            .Integer, types.Float)):
            raise BodoError(
                'pivot_table(): sum and prod operations require integer or float input'
                )
        if isinstance(syj__rhs, types.Integer):
            return IntDtype(syj__rhs)
        return syj__rhs
    if func_name in {'mean', 'var', 'std'}:
        return types.float64
    raise BodoError('invalid pivot operation')


def check_args_kwargs(func_name, len_args, args, kws):
    if len(kws) > 0:
        gebf__tza = list(kws.keys())[0]
        raise BodoError(
            f"Groupby.{func_name}() got an unexpected keyword argument '{gebf__tza}'."
            )
    elif len(args) > len_args:
        raise BodoError(
            f'Groupby.{func_name}() takes {len_args + 1} positional argument but {len(args)} were given.'
            )


class ColumnType(Enum):
    KeyColumn = 0
    NumericalColumn = 1
    NonNumericalColumn = 2


def get_keys_not_as_index(grp, out_columns, out_data, out_column_type,
    multi_level_names=False):
    for ouq__iro in grp.keys:
        if multi_level_names:
            cxxvl__trn = ouq__iro, ''
        else:
            cxxvl__trn = ouq__iro
        pja__nfhhr = grp.df_type.columns.index(ouq__iro)
        data = grp.df_type.data[pja__nfhhr]
        out_columns.append(cxxvl__trn)
        out_data.append(data)
        out_column_type.append(ColumnType.KeyColumn.value)


def get_agg_typ(grp, args, func_name, typing_context, target_context, func=
    None, kws=None):
    index = RangeIndexType(types.none)
    out_data = []
    out_columns = []
    out_column_type = []
    if func_name == 'head':
        grp.dropna = False
        grp.as_index = True
    if not grp.as_index:
        get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
    elif func_name == 'head':
        if grp.df_type.index == index:
            index = NumericIndexType(types.int64, types.none)
        else:
            index = grp.df_type.index
    elif len(grp.keys) > 1:
        zbncg__xut = tuple(grp.df_type.columns.index(grp.keys[edccw__dmt]) for
            edccw__dmt in range(len(grp.keys)))
        mli__gdgqk = tuple(grp.df_type.data[pja__nfhhr] for pja__nfhhr in
            zbncg__xut)
        index = MultiIndexType(mli__gdgqk, tuple(types.StringLiteral(
            ouq__iro) for ouq__iro in grp.keys))
    else:
        pja__nfhhr = grp.df_type.columns.index(grp.keys[0])
        index = bodo.hiframes.pd_index_ext.array_type_to_index(grp.df_type.
            data[pja__nfhhr], types.StringLiteral(grp.keys[0]))
    bldx__yjref = {}
    dzd__wtnlq = []
    if func_name in ('size', 'count'):
        kws = dict(kws) if kws else {}
        check_args_kwargs(func_name, 0, args, kws)
    if func_name == 'size':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('size')
        bldx__yjref[None, 'size'] = 'size'
    else:
        columns = (grp.selection if func_name != 'head' or grp.
            explicit_select else grp.df_type.columns)
        for oaprd__tnvmf in columns:
            pja__nfhhr = grp.df_type.columns.index(oaprd__tnvmf)
            data = grp.df_type.data[pja__nfhhr]
            ivnr__skdky = ColumnType.NonNumericalColumn.value
            if isinstance(data, (types.Array, IntegerArrayType)
                ) and isinstance(data.dtype, (types.Integer, types.Float)):
                ivnr__skdky = ColumnType.NumericalColumn.value
            if func_name == 'agg':
                try:
                    sqp__ywl = SeriesType(data.dtype, data, None, string_type)
                    ooem__uab = get_const_func_output_type(func, (sqp__ywl,
                        ), {}, typing_context, target_context)
                    if ooem__uab != ArrayItemArrayType(string_array_type):
                        ooem__uab = dtype_to_array_type(ooem__uab)
                    err_msg = 'ok'
                except:
                    raise_bodo_error(
                        'Groupy.agg()/Groupy.aggregate(): column {col} of type {type} is unsupported/not a valid input type for user defined function'
                        .format(col=oaprd__tnvmf, type=data.dtype))
            else:
                if func_name in ('first', 'last', 'min', 'max'):
                    kws = dict(kws) if kws else {}
                    pkba__fwq = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', False)
                    znp__lpl = args[1] if len(args) > 1 else kws.pop(
                        'min_count', -1)
                    uqxh__xsxjp = dict(numeric_only=pkba__fwq, min_count=
                        znp__lpl)
                    fspif__apndu = dict(numeric_only=False, min_count=-1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        uqxh__xsxjp, fspif__apndu, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('sum', 'prod'):
                    kws = dict(kws) if kws else {}
                    pkba__fwq = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    znp__lpl = args[1] if len(args) > 1 else kws.pop(
                        'min_count', 0)
                    uqxh__xsxjp = dict(numeric_only=pkba__fwq, min_count=
                        znp__lpl)
                    fspif__apndu = dict(numeric_only=True, min_count=0)
                    check_unsupported_args(f'Groupby.{func_name}',
                        uqxh__xsxjp, fspif__apndu, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('mean', 'median'):
                    kws = dict(kws) if kws else {}
                    pkba__fwq = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    uqxh__xsxjp = dict(numeric_only=pkba__fwq)
                    fspif__apndu = dict(numeric_only=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        uqxh__xsxjp, fspif__apndu, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('idxmin', 'idxmax'):
                    kws = dict(kws) if kws else {}
                    hny__bisb = args[0] if len(args) > 0 else kws.pop('axis', 0
                        )
                    yuayg__txrk = args[1] if len(args) > 1 else kws.pop(
                        'skipna', True)
                    uqxh__xsxjp = dict(axis=hny__bisb, skipna=yuayg__txrk)
                    fspif__apndu = dict(axis=0, skipna=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        uqxh__xsxjp, fspif__apndu, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('var', 'std'):
                    kws = dict(kws) if kws else {}
                    wburz__vkr = args[0] if len(args) > 0 else kws.pop('ddof',
                        1)
                    uqxh__xsxjp = dict(ddof=wburz__vkr)
                    fspif__apndu = dict(ddof=1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        uqxh__xsxjp, fspif__apndu, package_name='pandas',
                        module_name='GroupBy')
                elif func_name == 'nunique':
                    kws = dict(kws) if kws else {}
                    dropna = args[0] if len(args) > 0 else kws.pop('dropna', 1)
                    check_args_kwargs(func_name, 1, args, kws)
                elif func_name == 'head':
                    if len(args) == 0:
                        kws.pop('n', None)
                ooem__uab, err_msg = get_groupby_output_dtype(data,
                    func_name, grp.df_type.index)
            if err_msg == 'ok':
                qkvmh__jbla = ooem__uab
                out_data.append(qkvmh__jbla)
                out_columns.append(oaprd__tnvmf)
                if func_name == 'agg':
                    shns__lgt = bodo.ir.aggregate._get_udf_name(bodo.ir.
                        aggregate._get_const_agg_func(func, None))
                    bldx__yjref[oaprd__tnvmf, shns__lgt] = oaprd__tnvmf
                else:
                    bldx__yjref[oaprd__tnvmf, func_name] = oaprd__tnvmf
                out_column_type.append(ivnr__skdky)
            else:
                dzd__wtnlq.append(err_msg)
    if func_name == 'sum':
        mjlv__qdcsq = any([(iaqt__vuzv == ColumnType.NumericalColumn.value) for
            iaqt__vuzv in out_column_type])
        if mjlv__qdcsq:
            out_data = [iaqt__vuzv for iaqt__vuzv, boa__vmgb in zip(
                out_data, out_column_type) if boa__vmgb != ColumnType.
                NonNumericalColumn.value]
            out_columns = [iaqt__vuzv for iaqt__vuzv, boa__vmgb in zip(
                out_columns, out_column_type) if boa__vmgb != ColumnType.
                NonNumericalColumn.value]
            bldx__yjref = {}
            for oaprd__tnvmf in out_columns:
                if grp.as_index is False and oaprd__tnvmf in grp.keys:
                    continue
                bldx__yjref[oaprd__tnvmf, func_name] = oaprd__tnvmf
    lsv__mxiko = len(dzd__wtnlq)
    if len(out_data) == 0:
        if lsv__mxiko == 0:
            raise BodoError('No columns in output.')
        else:
            raise BodoError(
                'No columns in output. {} column{} dropped for following reasons: {}'
                .format(lsv__mxiko, ' was' if lsv__mxiko == 1 else 's were',
                ','.join(dzd__wtnlq)))
    wlj__ace = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if (len(grp.selection) == 1 and grp.series_select and grp.as_index or 
        func_name == 'size' and grp.as_index):
        if isinstance(out_data[0], IntegerArrayType):
            gmfdt__hmg = IntDtype(out_data[0].dtype)
        else:
            gmfdt__hmg = out_data[0].dtype
        imcz__ijfzx = (types.none if func_name == 'size' else types.
            StringLiteral(grp.selection[0]))
        wlj__ace = SeriesType(gmfdt__hmg, index=index, name_typ=imcz__ijfzx)
    return signature(wlj__ace, *args), bldx__yjref


def get_agg_funcname_and_outtyp(grp, col, f_val, typing_context, target_context
    ):
    puie__ohwqw = True
    if isinstance(f_val, str):
        puie__ohwqw = False
        uzgs__vnu = f_val
    elif is_overload_constant_str(f_val):
        puie__ohwqw = False
        uzgs__vnu = get_overload_const_str(f_val)
    elif bodo.utils.typing.is_builtin_function(f_val):
        puie__ohwqw = False
        uzgs__vnu = bodo.utils.typing.get_builtin_function_name(f_val)
    if not puie__ohwqw:
        if uzgs__vnu not in bodo.ir.aggregate.supported_agg_funcs[:-1]:
            raise BodoError(f'unsupported aggregate function {uzgs__vnu}')
        vvwx__grbfi = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(vvwx__grbfi, (), uzgs__vnu, typing_context,
            target_context)[0].return_type
    else:
        if is_expr(f_val, 'make_function'):
            bgwe__nji = types.functions.MakeFunctionLiteral(f_val)
        else:
            bgwe__nji = f_val
        validate_udf('agg', bgwe__nji)
        func = get_overload_const_func(bgwe__nji, None)
        bect__vxuqs = func.code if hasattr(func, 'code') else func.__code__
        uzgs__vnu = bect__vxuqs.co_name
        vvwx__grbfi = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(vvwx__grbfi, (), 'agg', typing_context,
            target_context, bgwe__nji)[0].return_type
    return uzgs__vnu, out_tp


def resolve_agg(grp, args, kws, typing_context, target_context):
    func = get_call_expr_arg('agg', args, dict(kws), 0, 'func', default=
        types.none)
    wem__qsdy = kws and all(isinstance(bbmah__xajal, types.Tuple) and len(
        bbmah__xajal) == 2 for bbmah__xajal in kws.values())
    if is_overload_none(func) and not wem__qsdy:
        raise_bodo_error("Groupby.agg()/aggregate(): Must provide 'func'")
    if len(args) > 1 or kws and not wem__qsdy:
        raise_bodo_error(
            'Groupby.agg()/aggregate(): passing extra arguments to functions not supported yet.'
            )
    ove__bdtpo = False

    def _append_out_type(grp, out_data, out_tp):
        if grp.as_index is False:
            out_data.append(out_tp.data[len(grp.keys)])
        else:
            out_data.append(out_tp.data)
    if wem__qsdy or is_overload_constant_dict(func):
        if wem__qsdy:
            roy__fetur = [get_literal_value(wkzf__bvrb) for wkzf__bvrb,
                iifjf__rca in kws.values()]
            npaq__tphxp = [get_literal_value(gfhv__nmuu) for iifjf__rca,
                gfhv__nmuu in kws.values()]
        else:
            ivccu__gji = get_overload_constant_dict(func)
            roy__fetur = tuple(ivccu__gji.keys())
            npaq__tphxp = tuple(ivccu__gji.values())
        if 'head' in npaq__tphxp:
            raise BodoError(
                'Groupby.agg()/aggregate(): head cannot be mixed with other groupby operations.'
                )
        if any(oaprd__tnvmf not in grp.selection and oaprd__tnvmf not in
            grp.keys for oaprd__tnvmf in roy__fetur):
            raise_const_error(
                f'Selected column names {roy__fetur} not all available in dataframe column names {grp.selection}'
                )
        multi_level_names = any(isinstance(f_val, (tuple, list)) for f_val in
            npaq__tphxp)
        if wem__qsdy and multi_level_names:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): cannot pass multiple functions in a single pd.NamedAgg()'
                )
        bldx__yjref = {}
        out_columns = []
        out_data = []
        out_column_type = []
        zdkro__ysp = []
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data,
                out_column_type, multi_level_names=multi_level_names)
        for jlai__csl, f_val in zip(roy__fetur, npaq__tphxp):
            if isinstance(f_val, (tuple, list)):
                lgi__dtg = 0
                for bgwe__nji in f_val:
                    uzgs__vnu, out_tp = get_agg_funcname_and_outtyp(grp,
                        jlai__csl, bgwe__nji, typing_context, target_context)
                    ove__bdtpo = uzgs__vnu in list_cumulative
                    if uzgs__vnu == '<lambda>' and len(f_val) > 1:
                        uzgs__vnu = '<lambda_' + str(lgi__dtg) + '>'
                        lgi__dtg += 1
                    out_columns.append((jlai__csl, uzgs__vnu))
                    bldx__yjref[jlai__csl, uzgs__vnu] = jlai__csl, uzgs__vnu
                    _append_out_type(grp, out_data, out_tp)
            else:
                uzgs__vnu, out_tp = get_agg_funcname_and_outtyp(grp,
                    jlai__csl, f_val, typing_context, target_context)
                ove__bdtpo = uzgs__vnu in list_cumulative
                if multi_level_names:
                    out_columns.append((jlai__csl, uzgs__vnu))
                    bldx__yjref[jlai__csl, uzgs__vnu] = jlai__csl, uzgs__vnu
                elif not wem__qsdy:
                    out_columns.append(jlai__csl)
                    bldx__yjref[jlai__csl, uzgs__vnu] = jlai__csl
                elif wem__qsdy:
                    zdkro__ysp.append(uzgs__vnu)
                _append_out_type(grp, out_data, out_tp)
        if wem__qsdy:
            for edccw__dmt, arcb__wcya in enumerate(kws.keys()):
                out_columns.append(arcb__wcya)
                bldx__yjref[roy__fetur[edccw__dmt], zdkro__ysp[edccw__dmt]
                    ] = arcb__wcya
        if ove__bdtpo:
            index = grp.df_type.index
        else:
            index = out_tp.index
        wlj__ace = DataFrameType(tuple(out_data), index, tuple(out_columns))
        return signature(wlj__ace, *args), bldx__yjref
    if isinstance(func, types.BaseTuple) and not isinstance(func, types.
        LiteralStrKeyDict):
        if not (len(grp.selection) == 1 and grp.explicit_select):
            raise_bodo_error(
                'Groupby.agg()/aggregate(): must select exactly one column when more than one functions supplied'
                )
        assert len(func) > 0
        out_data = []
        out_columns = []
        out_column_type = []
        lgi__dtg = 0
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
        bldx__yjref = {}
        dui__meakn = grp.selection[0]
        for f_val in func.types:
            uzgs__vnu, out_tp = get_agg_funcname_and_outtyp(grp, dui__meakn,
                f_val, typing_context, target_context)
            ove__bdtpo = uzgs__vnu in list_cumulative
            if uzgs__vnu == '<lambda>':
                uzgs__vnu = '<lambda_' + str(lgi__dtg) + '>'
                lgi__dtg += 1
            out_columns.append(uzgs__vnu)
            bldx__yjref[dui__meakn, uzgs__vnu] = uzgs__vnu
            _append_out_type(grp, out_data, out_tp)
        if ove__bdtpo:
            index = grp.df_type.index
        else:
            index = out_tp.index
        wlj__ace = DataFrameType(tuple(out_data), index, tuple(out_columns))
        return signature(wlj__ace, *args), bldx__yjref
    uzgs__vnu = ''
    if types.unliteral(func) == types.unicode_type:
        uzgs__vnu = get_overload_const_str(func)
    if bodo.utils.typing.is_builtin_function(func):
        uzgs__vnu = bodo.utils.typing.get_builtin_function_name(func)
    if uzgs__vnu:
        args = args[1:]
        kws.pop('func', None)
        return get_agg_typ(grp, args, uzgs__vnu, typing_context, kws)
    validate_udf('agg', func)
    return get_agg_typ(grp, args, 'agg', typing_context, target_context, func)


def resolve_transformative(grp, args, kws, msg, name_operation):
    index = grp.df_type.index
    out_columns = []
    out_data = []
    if name_operation in list_cumulative:
        kws = dict(kws) if kws else {}
        hny__bisb = args[0] if len(args) > 0 else kws.pop('axis', 0)
        pkba__fwq = args[1] if len(args) > 1 else kws.pop('numeric_only', False
            )
        yuayg__txrk = args[2] if len(args) > 2 else kws.pop('skipna', 1)
        uqxh__xsxjp = dict(axis=hny__bisb, numeric_only=pkba__fwq)
        fspif__apndu = dict(axis=0, numeric_only=False)
        check_unsupported_args(f'Groupby.{name_operation}', uqxh__xsxjp,
            fspif__apndu, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 3, args, kws)
    elif name_operation == 'shift':
        ybg__ngn = args[0] if len(args) > 0 else kws.pop('periods', 1)
        bfo__kqnw = args[1] if len(args) > 1 else kws.pop('freq', None)
        hny__bisb = args[2] if len(args) > 2 else kws.pop('axis', 0)
        naxxa__uamdi = args[3] if len(args) > 3 else kws.pop('fill_value', None
            )
        uqxh__xsxjp = dict(freq=bfo__kqnw, axis=hny__bisb, fill_value=
            naxxa__uamdi)
        fspif__apndu = dict(freq=None, axis=0, fill_value=None)
        check_unsupported_args(f'Groupby.{name_operation}', uqxh__xsxjp,
            fspif__apndu, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 4, args, kws)
    elif name_operation == 'transform':
        kws = dict(kws)
        gfr__itp = args[0] if len(args) > 0 else kws.pop('func', None)
        vvgl__ruvsg = kws.pop('engine', None)
        wski__baeep = kws.pop('engine_kwargs', None)
        uqxh__xsxjp = dict(engine=vvgl__ruvsg, engine_kwargs=wski__baeep)
        fspif__apndu = dict(engine=None, engine_kwargs=None)
        check_unsupported_args(f'Groupby.transform', uqxh__xsxjp,
            fspif__apndu, package_name='pandas', module_name='GroupBy')
    bldx__yjref = {}
    for oaprd__tnvmf in grp.selection:
        out_columns.append(oaprd__tnvmf)
        bldx__yjref[oaprd__tnvmf, name_operation] = oaprd__tnvmf
        pja__nfhhr = grp.df_type.columns.index(oaprd__tnvmf)
        data = grp.df_type.data[pja__nfhhr]
        if name_operation == 'cumprod':
            if not isinstance(data.dtype, (types.Integer, types.Float)):
                raise BodoError(msg)
        if name_operation == 'cumsum':
            if data.dtype != types.unicode_type and data != ArrayItemArrayType(
                string_array_type) and not isinstance(data.dtype, (types.
                Integer, types.Float)):
                raise BodoError(msg)
        if name_operation in ('cummin', 'cummax'):
            if not isinstance(data.dtype, types.Integer
                ) and not is_dtype_nullable(data.dtype):
                raise BodoError(msg)
        if name_operation == 'shift':
            if isinstance(data, (TupleArrayType, ArrayItemArrayType)):
                raise BodoError(msg)
            if isinstance(data.dtype, bodo.hiframes.datetime_timedelta_ext.
                DatetimeTimeDeltaType):
                raise BodoError(
                    f"""column type of {data.dtype} is not supported in groupby built-in function shift.
{dt_err}"""
                    )
        if name_operation == 'transform':
            ooem__uab, err_msg = get_groupby_output_dtype(data,
                get_literal_value(gfr__itp), grp.df_type.index)
            if err_msg == 'ok':
                data = ooem__uab
            else:
                raise BodoError(
                    f'column type of {data.dtype} is not supported by {args[0]} yet.\n'
                    )
        out_data.append(data)
    if len(out_data) == 0:
        raise BodoError('No columns in output.')
    wlj__ace = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if len(grp.selection) == 1 and grp.series_select and grp.as_index:
        wlj__ace = SeriesType(out_data[0].dtype, data=out_data[0], index=
            index, name_typ=types.StringLiteral(grp.selection[0]))
    return signature(wlj__ace, *args), bldx__yjref


def resolve_gb(grp, args, kws, func_name, typing_context, target_context,
    err_msg=''):
    if func_name in set(list_cumulative) | {'shift', 'transform'}:
        return resolve_transformative(grp, args, kws, err_msg, func_name)
    elif func_name in {'agg', 'aggregate'}:
        return resolve_agg(grp, args, kws, typing_context, target_context)
    else:
        return get_agg_typ(grp, args, func_name, typing_context,
            target_context, kws=kws)


@infer_getattr
class DataframeGroupByAttribute(OverloadedKeyAttributeTemplate):
    key = DataFrameGroupByType
    _attr_set = None

    @bound_function('groupby.agg', no_unliteral=True)
    def resolve_agg(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'agg', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.aggregate', no_unliteral=True)
    def resolve_aggregate(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'agg', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.sum', no_unliteral=True)
    def resolve_sum(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'sum', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.count', no_unliteral=True)
    def resolve_count(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'count', self.context, numba.core
            .registry.cpu_target.target_context)[0]

    @bound_function('groupby.nunique', no_unliteral=True)
    def resolve_nunique(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'nunique', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.median', no_unliteral=True)
    def resolve_median(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'median', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.mean', no_unliteral=True)
    def resolve_mean(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'mean', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.min', no_unliteral=True)
    def resolve_min(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'min', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.max', no_unliteral=True)
    def resolve_max(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'max', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.prod', no_unliteral=True)
    def resolve_prod(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'prod', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.var', no_unliteral=True)
    def resolve_var(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'var', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.std', no_unliteral=True)
    def resolve_std(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'std', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.first', no_unliteral=True)
    def resolve_first(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'first', self.context, numba.core
            .registry.cpu_target.target_context)[0]

    @bound_function('groupby.last', no_unliteral=True)
    def resolve_last(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'last', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.idxmin', no_unliteral=True)
    def resolve_idxmin(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'idxmin', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.idxmax', no_unliteral=True)
    def resolve_idxmax(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'idxmax', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.size', no_unliteral=True)
    def resolve_size(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'size', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.cumsum', no_unliteral=True)
    def resolve_cumsum(self, grp, args, kws):
        msg = (
            'Groupby.cumsum() only supports columns of types integer, float, string or liststring'
            )
        return resolve_gb(grp, args, kws, 'cumsum', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cumprod', no_unliteral=True)
    def resolve_cumprod(self, grp, args, kws):
        msg = (
            'Groupby.cumprod() only supports columns of types integer and float'
            )
        return resolve_gb(grp, args, kws, 'cumprod', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cummin', no_unliteral=True)
    def resolve_cummin(self, grp, args, kws):
        msg = (
            'Groupby.cummin() only supports columns of types integer, float, string, liststring, date, datetime or timedelta'
            )
        return resolve_gb(grp, args, kws, 'cummin', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cummax', no_unliteral=True)
    def resolve_cummax(self, grp, args, kws):
        msg = (
            'Groupby.cummax() only supports columns of types integer, float, string, liststring, date, datetime or timedelta'
            )
        return resolve_gb(grp, args, kws, 'cummax', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.shift', no_unliteral=True)
    def resolve_shift(self, grp, args, kws):
        msg = (
            'Column type of list/tuple is not supported in groupby built-in function shift'
            )
        return resolve_gb(grp, args, kws, 'shift', self.context, numba.core
            .registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.pipe', no_unliteral=True)
    def resolve_pipe(self, grp, args, kws):
        return resolve_obj_pipe(self, grp, args, kws, 'GroupBy')

    @bound_function('groupby.transform', no_unliteral=True)
    def resolve_transform(self, grp, args, kws):
        msg = (
            'Groupby.transform() only supports sum, count, min, max, mean, and std operations'
            )
        return resolve_gb(grp, args, kws, 'transform', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.head', no_unliteral=True)
    def resolve_head(self, grp, args, kws):
        msg = 'Unsupported Gropupby head operation.\n'
        return resolve_gb(grp, args, kws, 'head', self.context, numba.core.
            registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.apply', no_unliteral=True)
    def resolve_apply(self, grp, args, kws):
        kws = dict(kws)
        func = args[0] if len(args) > 0 else kws.pop('func', None)
        f_args = tuple(args[1:]) if len(args) > 0 else ()
        awh__txxm = _get_groupby_apply_udf_out_type(func, grp, f_args, kws,
            self.context, numba.core.registry.cpu_target.target_context)
        uccez__mcq = isinstance(awh__txxm, (SeriesType,
            HeterogeneousSeriesType)
            ) and awh__txxm.const_info is not None or not isinstance(awh__txxm,
            (SeriesType, DataFrameType))
        if uccez__mcq:
            out_data = []
            out_columns = []
            out_column_type = []
            if not grp.as_index:
                get_keys_not_as_index(grp, out_columns, out_data,
                    out_column_type)
                efl__dbt = NumericIndexType(types.int64, types.none)
            elif len(grp.keys) > 1:
                zbncg__xut = tuple(grp.df_type.columns.index(grp.keys[
                    edccw__dmt]) for edccw__dmt in range(len(grp.keys)))
                mli__gdgqk = tuple(grp.df_type.data[pja__nfhhr] for
                    pja__nfhhr in zbncg__xut)
                efl__dbt = MultiIndexType(mli__gdgqk, tuple(types.literal(
                    ouq__iro) for ouq__iro in grp.keys))
            else:
                pja__nfhhr = grp.df_type.columns.index(grp.keys[0])
                efl__dbt = bodo.hiframes.pd_index_ext.array_type_to_index(grp
                    .df_type.data[pja__nfhhr], types.literal(grp.keys[0]))
            out_data = tuple(out_data)
            out_columns = tuple(out_columns)
        else:
            weg__zimuj = tuple(grp.df_type.data[grp.df_type.columns.index(
                oaprd__tnvmf)] for oaprd__tnvmf in grp.keys)
            lyak__mbhvs = tuple(types.literal(bbmah__xajal) for
                bbmah__xajal in grp.keys) + get_index_name_types(awh__txxm.
                index)
            if not grp.as_index:
                weg__zimuj = types.Array(types.int64, 1, 'C'),
                lyak__mbhvs = (types.none,) + get_index_name_types(awh__txxm
                    .index)
            efl__dbt = MultiIndexType(weg__zimuj + get_index_data_arr_types
                (awh__txxm.index), lyak__mbhvs)
        if uccez__mcq:
            if isinstance(awh__txxm, HeterogeneousSeriesType):
                iifjf__rca, bdgvg__jzq = awh__txxm.const_info
                pns__jlz = tuple(dtype_to_array_type(cjtfj__ylqc) for
                    cjtfj__ylqc in awh__txxm.data.types)
                pisr__fcm = DataFrameType(out_data + pns__jlz, efl__dbt, 
                    out_columns + bdgvg__jzq)
            elif isinstance(awh__txxm, SeriesType):
                vsaw__ftzsa, bdgvg__jzq = awh__txxm.const_info
                pns__jlz = tuple(dtype_to_array_type(awh__txxm.dtype) for
                    iifjf__rca in range(vsaw__ftzsa))
                pisr__fcm = DataFrameType(out_data + pns__jlz, efl__dbt, 
                    out_columns + bdgvg__jzq)
            else:
                oug__acbc = get_udf_out_arr_type(awh__txxm)
                if not grp.as_index:
                    pisr__fcm = DataFrameType(out_data + (oug__acbc,),
                        efl__dbt, out_columns + ('',))
                else:
                    pisr__fcm = SeriesType(oug__acbc.dtype, oug__acbc,
                        efl__dbt, None)
        elif isinstance(awh__txxm, SeriesType):
            pisr__fcm = SeriesType(awh__txxm.dtype, awh__txxm.data,
                efl__dbt, awh__txxm.name_typ)
        else:
            pisr__fcm = DataFrameType(awh__txxm.data, efl__dbt, awh__txxm.
                columns)
        njipn__kygv = gen_apply_pysig(len(f_args), kws.keys())
        nqmkk__wno = (func, *f_args) + tuple(kws.values())
        return signature(pisr__fcm, *nqmkk__wno).replace(pysig=njipn__kygv)

    def generic_resolve(self, grpby, attr):
        if self._is_existing_attr(attr):
            return
        if attr not in grpby.df_type.columns:
            raise_const_error(
                f'groupby: invalid attribute {attr} (column not found in dataframe or unsupported function)'
                )
        return DataFrameGroupByType(grpby.df_type, grpby.keys, (attr,),
            grpby.as_index, grpby.dropna, True, True)


def _get_groupby_apply_udf_out_type(func, grp, f_args, kws, typing_context,
    target_context):
    kezv__etbg = grp.df_type
    if grp.explicit_select:
        if len(grp.selection) == 1:
            jlai__csl = grp.selection[0]
            oug__acbc = kezv__etbg.data[kezv__etbg.columns.index(jlai__csl)]
            ljfkp__rqmr = SeriesType(oug__acbc.dtype, oug__acbc, kezv__etbg
                .index, types.literal(jlai__csl))
        else:
            hasfw__wumx = tuple(kezv__etbg.data[kezv__etbg.columns.index(
                oaprd__tnvmf)] for oaprd__tnvmf in grp.selection)
            ljfkp__rqmr = DataFrameType(hasfw__wumx, kezv__etbg.index,
                tuple(grp.selection))
    else:
        ljfkp__rqmr = kezv__etbg
    urcy__rvawt = ljfkp__rqmr,
    urcy__rvawt += tuple(f_args)
    try:
        awh__txxm = get_const_func_output_type(func, urcy__rvawt, kws,
            typing_context, target_context)
    except Exception as lbhw__stqr:
        raise_bodo_error(get_udf_error_msg('GroupBy.apply()', lbhw__stqr),
            getattr(lbhw__stqr, 'loc', None))
    return awh__txxm


def resolve_obj_pipe(self, grp, args, kws, obj_name):
    kws = dict(kws)
    func = args[0] if len(args) > 0 else kws.pop('func', None)
    f_args = tuple(args[1:]) if len(args) > 0 else ()
    urcy__rvawt = (grp,) + f_args
    try:
        awh__txxm = get_const_func_output_type(func, urcy__rvawt, kws, self
            .context, numba.core.registry.cpu_target.target_context, False)
    except Exception as lbhw__stqr:
        raise_bodo_error(get_udf_error_msg(f'{obj_name}.pipe()', lbhw__stqr
            ), getattr(lbhw__stqr, 'loc', None))
    njipn__kygv = gen_apply_pysig(len(f_args), kws.keys())
    nqmkk__wno = (func, *f_args) + tuple(kws.values())
    return signature(awh__txxm, *nqmkk__wno).replace(pysig=njipn__kygv)


def gen_apply_pysig(n_args, kws):
    ppyx__xgkwq = ', '.join(f'arg{edccw__dmt}' for edccw__dmt in range(n_args))
    ppyx__xgkwq = ppyx__xgkwq + ', ' if ppyx__xgkwq else ''
    eih__pjgf = ', '.join(f"{yih__yullt} = ''" for yih__yullt in kws)
    ccn__ztp = f'def apply_stub(func, {ppyx__xgkwq}{eih__pjgf}):\n'
    ccn__ztp += '    pass\n'
    gof__nkb = {}
    exec(ccn__ztp, {}, gof__nkb)
    ksba__xgomh = gof__nkb['apply_stub']
    return numba.core.utils.pysignature(ksba__xgomh)


def pivot_table_dummy(df, values, index, columns, aggfunc, _pivot_values):
    return 0


@infer_global(pivot_table_dummy)
class PivotTableTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df, values, index, columns, aggfunc, _pivot_values = args
        if not (is_overload_constant_str(values) and
            is_overload_constant_str(index) and is_overload_constant_str(
            columns)):
            raise BodoError(
                "pivot_table() only support string constants for 'values', 'index' and 'columns' arguments"
                )
        values = values.literal_value
        index = index.literal_value
        columns = columns.literal_value
        data = df.data[df.columns.index(values)]
        ooem__uab = get_pivot_output_dtype(data, aggfunc.literal_value)
        euuot__lcjw = dtype_to_array_type(ooem__uab)
        if is_overload_none(_pivot_values):
            raise_bodo_error(
                'Dataframe.pivot_table() requires explicit annotation to determine output columns. For more information, see: https://docs.bodo.ai/latest/source/programming_with_bodo/pandas.html'
                )
        yha__jlnl = _pivot_values.meta
        qzg__yaval = len(yha__jlnl)
        pja__nfhhr = df.columns.index(index)
        jwgt__yiv = bodo.hiframes.pd_index_ext.array_type_to_index(df.data[
            pja__nfhhr], types.StringLiteral(index))
        kjw__sockg = DataFrameType((euuot__lcjw,) * qzg__yaval, jwgt__yiv,
            tuple(yha__jlnl))
        return signature(kjw__sockg, *args)


PivotTableTyper._no_unliteral = True


@lower_builtin(pivot_table_dummy, types.VarArg(types.Any))
def lower_pivot_table_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def crosstab_dummy(index, columns, _pivot_values):
    return 0


@infer_global(crosstab_dummy)
class CrossTabTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        index, columns, _pivot_values = args
        euuot__lcjw = types.Array(types.int64, 1, 'C')
        yha__jlnl = _pivot_values.meta
        qzg__yaval = len(yha__jlnl)
        jwgt__yiv = bodo.hiframes.pd_index_ext.array_type_to_index(index.
            data, types.StringLiteral('index'))
        kjw__sockg = DataFrameType((euuot__lcjw,) * qzg__yaval, jwgt__yiv,
            tuple(yha__jlnl))
        return signature(kjw__sockg, *args)


CrossTabTyper._no_unliteral = True


@lower_builtin(crosstab_dummy, types.VarArg(types.Any))
def lower_crosstab_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def get_group_indices(keys, dropna, _is_parallel):
    return np.arange(len(keys))


@overload(get_group_indices)
def get_group_indices_overload(keys, dropna, _is_parallel):
    ccn__ztp = 'def impl(keys, dropna, _is_parallel):\n'
    ccn__ztp += (
        "    ev = bodo.utils.tracing.Event('get_group_indices', _is_parallel)\n"
        )
    ccn__ztp += '    info_list = [{}]\n'.format(', '.join(
        f'array_to_info(keys[{edccw__dmt}])' for edccw__dmt in range(len(
        keys.types))))
    ccn__ztp += '    table = arr_info_list_to_table(info_list)\n'
    ccn__ztp += '    group_labels = np.empty(len(keys[0]), np.int64)\n'
    ccn__ztp += '    sort_idx = np.empty(len(keys[0]), np.int64)\n'
    ccn__ztp += """    ngroups = get_groupby_labels(table, group_labels.ctypes, sort_idx.ctypes, dropna, _is_parallel)
"""
    ccn__ztp += '    delete_table_decref_arrays(table)\n'
    ccn__ztp += '    ev.finalize()\n'
    ccn__ztp += '    return sort_idx, group_labels, ngroups\n'
    gof__nkb = {}
    exec(ccn__ztp, {'bodo': bodo, 'np': np, 'get_groupby_labels':
        get_groupby_labels, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, gof__nkb)
    xdy__kkr = gof__nkb['impl']
    return xdy__kkr


@numba.njit(no_cpython_wrapper=True)
def generate_slices(labels, ngroups):
    wtb__putkv = len(labels)
    bcx__ecmx = np.zeros(ngroups, dtype=np.int64)
    dedj__ohhji = np.zeros(ngroups, dtype=np.int64)
    jubt__xghy = 0
    nqpeq__lnr = 0
    for edccw__dmt in range(wtb__putkv):
        cga__qyw = labels[edccw__dmt]
        if cga__qyw < 0:
            jubt__xghy += 1
        else:
            nqpeq__lnr += 1
            if edccw__dmt == wtb__putkv - 1 or cga__qyw != labels[
                edccw__dmt + 1]:
                bcx__ecmx[cga__qyw] = jubt__xghy
                dedj__ohhji[cga__qyw] = jubt__xghy + nqpeq__lnr
                jubt__xghy += nqpeq__lnr
                nqpeq__lnr = 0
    return bcx__ecmx, dedj__ohhji


def shuffle_dataframe(df, keys, _is_parallel):
    return df, keys, _is_parallel


@overload(shuffle_dataframe)
def overload_shuffle_dataframe(df, keys, _is_parallel):
    vsaw__ftzsa = len(df.columns)
    ymgj__hcftv = len(keys.types)
    abzxr__txv = ', '.join('data_{}'.format(edccw__dmt) for edccw__dmt in
        range(vsaw__ftzsa))
    ccn__ztp = 'def impl(df, keys, _is_parallel):\n'
    for edccw__dmt in range(vsaw__ftzsa):
        ccn__ztp += f"""  in_arr{edccw__dmt} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {edccw__dmt})
"""
    ccn__ztp += f"""  in_index_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
    ccn__ztp += '  info_list = [{}, {}, {}]\n'.format(', '.join(
        f'array_to_info(keys[{edccw__dmt}])' for edccw__dmt in range(
        ymgj__hcftv)), ', '.join(f'array_to_info(in_arr{edccw__dmt})' for
        edccw__dmt in range(vsaw__ftzsa)), 'array_to_info(in_index_arr)')
    ccn__ztp += '  table = arr_info_list_to_table(info_list)\n'
    ccn__ztp += (
        f'  out_table = shuffle_table(table, {ymgj__hcftv}, _is_parallel, 1)\n'
        )
    for edccw__dmt in range(ymgj__hcftv):
        ccn__ztp += f"""  out_key{edccw__dmt} = info_to_array(info_from_table(out_table, {edccw__dmt}), keys[{edccw__dmt}])
"""
    for edccw__dmt in range(vsaw__ftzsa):
        ccn__ztp += f"""  out_arr{edccw__dmt} = info_to_array(info_from_table(out_table, {edccw__dmt + ymgj__hcftv}), in_arr{edccw__dmt})
"""
    ccn__ztp += f"""  out_arr_index = info_to_array(info_from_table(out_table, {ymgj__hcftv + vsaw__ftzsa}), in_index_arr)
"""
    ccn__ztp += '  shuffle_info = get_shuffle_info(out_table)\n'
    ccn__ztp += '  delete_table(out_table)\n'
    ccn__ztp += '  delete_table(table)\n'
    out_data = ', '.join(f'out_arr{edccw__dmt}' for edccw__dmt in range(
        vsaw__ftzsa))
    ccn__ztp += (
        '  out_index = bodo.utils.conversion.index_from_array(out_arr_index)\n'
        )
    ccn__ztp += f"""  out_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(({out_data},), out_index, {gen_const_tup(df.columns)})
"""
    ccn__ztp += '  return out_df, ({},), shuffle_info\n'.format(', '.join(
        f'out_key{edccw__dmt}' for edccw__dmt in range(ymgj__hcftv)))
    gof__nkb = {}
    exec(ccn__ztp, {'bodo': bodo, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_from_table': info_from_table, 'info_to_array':
        info_to_array, 'delete_table': delete_table, 'get_shuffle_info':
        get_shuffle_info}, gof__nkb)
    xdy__kkr = gof__nkb['impl']
    return xdy__kkr


def reverse_shuffle(data, shuffle_info):
    return data


@overload(reverse_shuffle)
def overload_reverse_shuffle(data, shuffle_info):
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        unf__vqou = len(data.array_types)
        ccn__ztp = 'def impl(data, shuffle_info):\n'
        ccn__ztp += '  info_list = [{}]\n'.format(', '.join(
            f'array_to_info(data._data[{edccw__dmt}])' for edccw__dmt in
            range(unf__vqou)))
        ccn__ztp += '  table = arr_info_list_to_table(info_list)\n'
        ccn__ztp += (
            '  out_table = reverse_shuffle_table(table, shuffle_info)\n')
        for edccw__dmt in range(unf__vqou):
            ccn__ztp += f"""  out_arr{edccw__dmt} = info_to_array(info_from_table(out_table, {edccw__dmt}), data._data[{edccw__dmt}])
"""
        ccn__ztp += '  delete_table(out_table)\n'
        ccn__ztp += '  delete_table(table)\n'
        ccn__ztp += (
            '  return init_multi_index(({},), data._names, data._name)\n'.
            format(', '.join(f'out_arr{edccw__dmt}' for edccw__dmt in range
            (unf__vqou))))
        gof__nkb = {}
        exec(ccn__ztp, {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'reverse_shuffle_table': reverse_shuffle_table,
            'info_from_table': info_from_table, 'info_to_array':
            info_to_array, 'delete_table': delete_table, 'init_multi_index':
            bodo.hiframes.pd_multi_index_ext.init_multi_index}, gof__nkb)
        xdy__kkr = gof__nkb['impl']
        return xdy__kkr
    if bodo.hiframes.pd_index_ext.is_index_type(data):

        def impl_index(data, shuffle_info):
            ytwdy__ylk = bodo.utils.conversion.index_to_array(data)
            qkvmh__jbla = reverse_shuffle(ytwdy__ylk, shuffle_info)
            return bodo.utils.conversion.index_from_array(qkvmh__jbla)
        return impl_index

    def impl_arr(data, shuffle_info):
        csaph__qth = [array_to_info(data)]
        cokns__ifl = arr_info_list_to_table(csaph__qth)
        fntl__ciup = reverse_shuffle_table(cokns__ifl, shuffle_info)
        qkvmh__jbla = info_to_array(info_from_table(fntl__ciup, 0), data)
        delete_table(fntl__ciup)
        delete_table(cokns__ifl)
        return qkvmh__jbla
    return impl_arr


@overload_method(DataFrameGroupByType, 'value_counts', inline='always',
    no_unliteral=True)
def groupby_value_counts(grp, normalize=False, sort=True, ascending=False,
    bins=None, dropna=True):
    uqxh__xsxjp = dict(normalize=normalize, sort=sort, bins=bins, dropna=dropna
        )
    fspif__apndu = dict(normalize=False, sort=True, bins=None, dropna=True)
    check_unsupported_args('Groupby.value_counts', uqxh__xsxjp,
        fspif__apndu, package_name='pandas', module_name='GroupBy')
    if len(grp.selection) > 1 or not grp.as_index:
        raise BodoError(
            "'DataFrameGroupBy' object has no attribute 'value_counts'")
    if not is_overload_constant_bool(ascending):
        raise BodoError(
            'Groupby.value_counts() ascending must be a constant boolean')
    azmf__adqcj = get_overload_const_bool(ascending)
    qqehu__zyfj = grp.selection[0]
    ccn__ztp = f"""def impl(grp, normalize=False, sort=True, ascending=False, bins=None, dropna=True):
"""
    atrw__qqdo = (
        f"lambda S: S.value_counts(ascending={azmf__adqcj}, _index_name='{qqehu__zyfj}')"
        )
    ccn__ztp += f'    return grp.apply({atrw__qqdo})\n'
    gof__nkb = {}
    exec(ccn__ztp, {'bodo': bodo}, gof__nkb)
    xdy__kkr = gof__nkb['impl']
    return xdy__kkr


groupby_unsupported_attr = {'groups', 'indices'}
groupby_unsupported = {'__iter__', 'get_group', 'all', 'any', 'bfill',
    'backfill', 'cumcount', 'cummax', 'cummin', 'cumprod', 'ffill',
    'ngroup', 'nth', 'ohlc', 'pad', 'rank', 'pct_change', 'sem', 'tail',
    'corr', 'cov', 'describe', 'diff', 'fillna', 'filter', 'hist', 'mad',
    'plot', 'quantile', 'resample', 'sample', 'skew', 'take', 'tshift'}
series_only_unsupported_attrs = {'is_monotonic_increasing',
    'is_monotonic_decreasing'}
series_only_unsupported = {'nlargest', 'nsmallest', 'unique'}
dataframe_only_unsupported = {'corrwith', 'boxplot'}


def _install_groupy_unsupported():
    for vdsj__lcj in groupby_unsupported_attr:
        overload_attribute(DataFrameGroupByType, vdsj__lcj, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{vdsj__lcj}'))
    for vdsj__lcj in groupby_unsupported:
        overload_method(DataFrameGroupByType, vdsj__lcj, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{vdsj__lcj}'))
    for vdsj__lcj in series_only_unsupported_attrs:
        overload_attribute(DataFrameGroupByType, vdsj__lcj, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{vdsj__lcj}'))
    for vdsj__lcj in series_only_unsupported:
        overload_method(DataFrameGroupByType, vdsj__lcj, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{vdsj__lcj}'))
    for vdsj__lcj in dataframe_only_unsupported:
        overload_method(DataFrameGroupByType, vdsj__lcj, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{vdsj__lcj}'))


_install_groupy_unsupported()
