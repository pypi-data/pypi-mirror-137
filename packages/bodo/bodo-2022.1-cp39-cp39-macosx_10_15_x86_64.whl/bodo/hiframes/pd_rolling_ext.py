"""typing for rolling window functions
"""
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.core.typing.templates import AbstractTemplate, AttributeTemplate, signature
from numba.extending import infer, infer_getattr, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_method, register_model
import bodo
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_type, pd_timedelta_type
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported
from bodo.hiframes.pd_groupby_ext import DataFrameGroupByType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.rolling import supported_rolling_funcs, unsupported_rolling_methods
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, get_literal_value, is_const_func_type, is_literal_type, is_overload_bool, is_overload_constant_str, is_overload_int, is_overload_none, raise_bodo_error, raise_const_error


class RollingType(types.Type):

    def __init__(self, obj_type, window_type, on, selection,
        explicit_select=False, series_select=False):
        self.obj_type = obj_type
        self.window_type = window_type
        self.on = on
        self.selection = selection
        self.explicit_select = explicit_select
        self.series_select = series_select
        super(RollingType, self).__init__(name=
            f'RollingType({obj_type}, {window_type}, {on}, {selection}, {explicit_select}, {series_select})'
            )

    def copy(self):
        return RollingType(self.obj_type, self.window_type, self.on, self.
            selection, self.explicit_select, self.series_select)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(RollingType)
class RollingModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        yuh__gxwh = [('obj', fe_type.obj_type), ('window', fe_type.
            window_type), ('min_periods', types.int64), ('center', types.bool_)
            ]
        super(RollingModel, self).__init__(dmm, fe_type, yuh__gxwh)


make_attribute_wrapper(RollingType, 'obj', 'obj')
make_attribute_wrapper(RollingType, 'window', 'window')
make_attribute_wrapper(RollingType, 'center', 'center')
make_attribute_wrapper(RollingType, 'min_periods', 'min_periods')


@overload_method(DataFrameType, 'rolling', inline='always', no_unliteral=True)
def df_rolling_overload(df, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    check_runtime_cols_unsupported(df, 'DataFrame.rolling()')
    rgv__gftnd = dict(win_type=win_type, axis=axis, closed=closed)
    rcq__pbino = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('DataFrame.rolling', rgv__gftnd, rcq__pbino,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(df, window, min_periods, center, on)

    def impl(df, window, min_periods=None, center=False, win_type=None, on=
        None, axis=0, closed=None):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(df, window,
            min_periods, center, on)
    return impl


@overload_method(SeriesType, 'rolling', inline='always', no_unliteral=True)
def overload_series_rolling(S, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    rgv__gftnd = dict(win_type=win_type, axis=axis, closed=closed)
    rcq__pbino = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('Series.rolling', rgv__gftnd, rcq__pbino,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(S, window, min_periods, center, on)

    def impl(S, window, min_periods=None, center=False, win_type=None, on=
        None, axis=0, closed=None):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(S, window,
            min_periods, center, on)
    return impl


@intrinsic
def init_rolling(typingctx, obj_type, window_type, min_periods_type,
    center_type, on_type=None):

    def codegen(context, builder, signature, args):
        ahlu__epe, ncb__ehswm, hgjs__naqb, dcsn__frb, efgr__jkg = args
        ylq__wcdm = signature.return_type
        cbbsh__aln = cgutils.create_struct_proxy(ylq__wcdm)(context, builder)
        cbbsh__aln.obj = ahlu__epe
        cbbsh__aln.window = ncb__ehswm
        cbbsh__aln.min_periods = hgjs__naqb
        cbbsh__aln.center = dcsn__frb
        context.nrt.incref(builder, signature.args[0], ahlu__epe)
        context.nrt.incref(builder, signature.args[1], ncb__ehswm)
        context.nrt.incref(builder, signature.args[2], hgjs__naqb)
        context.nrt.incref(builder, signature.args[3], dcsn__frb)
        return cbbsh__aln._getvalue()
    on = get_literal_value(on_type)
    if isinstance(obj_type, SeriesType):
        selection = None
    elif isinstance(obj_type, DataFrameType):
        selection = obj_type.columns
    else:
        assert isinstance(obj_type, DataFrameGroupByType
            ), f'invalid obj type for rolling: {obj_type}'
        selection = obj_type.selection
    ylq__wcdm = RollingType(obj_type, window_type, on, selection, False)
    return ylq__wcdm(obj_type, window_type, min_periods_type, center_type,
        on_type), codegen


def _handle_default_min_periods(min_periods, window):
    return min_periods


@overload(_handle_default_min_periods)
def overload_handle_default_min_periods(min_periods, window):
    if is_overload_none(min_periods):
        if isinstance(window, types.Integer):
            return lambda min_periods, window: window
        else:
            return lambda min_periods, window: 1
    else:
        return lambda min_periods, window: min_periods


def _gen_df_rolling_out_data(rolling):
    kse__kfcv = not isinstance(rolling.window_type, types.Integer)
    isov__ofvxj = 'variable' if kse__kfcv else 'fixed'
    jfo__wwoy = 'None'
    if kse__kfcv:
        jfo__wwoy = ('bodo.utils.conversion.index_to_array(index)' if 
            rolling.on is None else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rolling.obj_type.columns.index(rolling.on)})'
            )
    ozp__oro = []
    jvzc__yco = 'on_arr, ' if kse__kfcv else ''
    if isinstance(rolling.obj_type, SeriesType):
        return (
            f'bodo.hiframes.rolling.rolling_{isov__ofvxj}(bodo.hiframes.pd_series_ext.get_series_data(df), {jvzc__yco}index_arr, window, minp, center, func, raw)'
            , jfo__wwoy, rolling.selection)
    assert isinstance(rolling.obj_type, DataFrameType
        ), 'expected df in rolling obj'
    zigwt__jgdn = rolling.obj_type.data
    out_cols = []
    for jpeqx__wqws in rolling.selection:
        rrzl__nkpdw = rolling.obj_type.columns.index(jpeqx__wqws)
        if jpeqx__wqws == rolling.on:
            if len(rolling.selection) == 2 and rolling.series_select:
                continue
            wsw__plj = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rrzl__nkpdw})'
                )
            out_cols.append(jpeqx__wqws)
        else:
            if not isinstance(zigwt__jgdn[rrzl__nkpdw].dtype, (types.
                Boolean, types.Number)):
                continue
            wsw__plj = (
                f'bodo.hiframes.rolling.rolling_{isov__ofvxj}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rrzl__nkpdw}), {jvzc__yco}index_arr, window, minp, center, func, raw)'
                )
            out_cols.append(jpeqx__wqws)
        ozp__oro.append(wsw__plj)
    return ', '.join(ozp__oro), jfo__wwoy, tuple(out_cols)


@overload_method(RollingType, 'apply', inline='always', no_unliteral=True)
def overload_rolling_apply(rolling, func, raw=False, engine=None,
    engine_kwargs=None, args=None, kwargs=None):
    rgv__gftnd = dict(engine=engine, engine_kwargs=engine_kwargs, args=args,
        kwargs=kwargs)
    rcq__pbino = dict(engine=None, engine_kwargs=None, args=None, kwargs=None)
    check_unsupported_args('Rolling.apply', rgv__gftnd, rcq__pbino,
        package_name='pandas', module_name='Window')
    if not is_const_func_type(func):
        raise BodoError(
            f"Rolling.apply(): 'func' parameter must be a function, not {func} (builtin functions not supported yet)."
            )
    if not is_overload_bool(raw):
        raise BodoError(
            f"Rolling.apply(): 'raw' parameter must be bool, not {raw}.")
    return _gen_rolling_impl(rolling, 'apply')


@overload_method(DataFrameGroupByType, 'rolling', inline='always',
    no_unliteral=True)
def groupby_rolling_overload(grp, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None, method='single'):
    rgv__gftnd = dict(win_type=win_type, axis=axis, closed=closed, method=
        method)
    rcq__pbino = dict(win_type=None, axis=0, closed=None, method='single')
    check_unsupported_args('GroupBy.rolling', rgv__gftnd, rcq__pbino,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(grp, window, min_periods, center, on)

    def _impl(grp, window, min_periods=None, center=False, win_type=None,
        on=None, axis=0, closed=None, method='single'):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(grp, window,
            min_periods, center, on)
    return _impl


def _gen_rolling_impl(rolling, fname, other=None):
    if isinstance(rolling.obj_type, DataFrameGroupByType):
        aio__hhoh = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
        iatyd__kqo = f"'{rolling.on}'" if isinstance(rolling.on, str
            ) else f'{rolling.on}'
        selection = ''
        if rolling.explicit_select:
            selection = '[{}]'.format(', '.join(f"'{eib__soz}'" if
                isinstance(eib__soz, str) else f'{eib__soz}' for eib__soz in
                rolling.selection if eib__soz != rolling.on))
        cqat__bru = pexgh__ddhyh = ''
        if fname == 'apply':
            cqat__bru = 'func, raw, args, kwargs'
            pexgh__ddhyh = 'func, raw, None, None, args, kwargs'
        if fname == 'corr':
            cqat__bru = pexgh__ddhyh = 'other, pairwise'
        if fname == 'cov':
            cqat__bru = pexgh__ddhyh = 'other, pairwise, ddof'
        wmazm__hqm = (
            f'lambda df, window, minp, center, {cqat__bru}: bodo.hiframes.pd_rolling_ext.init_rolling(df, window, minp, center, {iatyd__kqo}){selection}.{fname}({pexgh__ddhyh})'
            )
        aio__hhoh += f"""  return rolling.obj.apply({wmazm__hqm}, rolling.window, rolling.min_periods, rolling.center, {cqat__bru})
"""
        pjfok__rtj = {}
        exec(aio__hhoh, {'bodo': bodo}, pjfok__rtj)
        impl = pjfok__rtj['impl']
        return impl
    leuxe__xus = isinstance(rolling.obj_type, SeriesType)
    if fname in ('corr', 'cov'):
        out_cols = None if leuxe__xus else _get_corr_cov_out_cols(rolling,
            other, fname)
        df_cols = None if leuxe__xus else rolling.obj_type.columns
        other_cols = None if leuxe__xus else other.columns
        ozp__oro, jfo__wwoy = _gen_corr_cov_out_data(out_cols, df_cols,
            other_cols, rolling.window_type, fname)
    else:
        ozp__oro, jfo__wwoy, out_cols = _gen_df_rolling_out_data(rolling)
    knnfp__bkpvm = leuxe__xus or len(rolling.selection) == (1 if rolling.on is
        None else 2) and rolling.series_select
    cdjx__endvc = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
    cdjx__endvc += '  df = rolling.obj\n'
    cdjx__endvc += '  index = {}\n'.format(
        'bodo.hiframes.pd_series_ext.get_series_index(df)' if leuxe__xus else
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
    uycja__iwz = 'None'
    if leuxe__xus:
        uycja__iwz = 'bodo.hiframes.pd_series_ext.get_series_name(df)'
    elif knnfp__bkpvm:
        jpeqx__wqws = (set(out_cols) - set([rolling.on])).pop()
        uycja__iwz = f"'{jpeqx__wqws}'" if isinstance(jpeqx__wqws, str
            ) else str(jpeqx__wqws)
    cdjx__endvc += f'  name = {uycja__iwz}\n'
    cdjx__endvc += '  window = rolling.window\n'
    cdjx__endvc += '  center = rolling.center\n'
    cdjx__endvc += '  minp = rolling.min_periods\n'
    cdjx__endvc += f'  on_arr = {jfo__wwoy}\n'
    if fname == 'apply':
        cdjx__endvc += (
            f'  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    else:
        cdjx__endvc += f"  func = '{fname}'\n"
        cdjx__endvc += f'  index_arr = None\n'
        cdjx__endvc += f'  raw = False\n'
    if knnfp__bkpvm:
        cdjx__endvc += (
            f'  return bodo.hiframes.pd_series_ext.init_series({ozp__oro}, index, name)'
            )
        pjfok__rtj = {}
        nqaj__omyad = {'bodo': bodo}
        exec(cdjx__endvc, nqaj__omyad, pjfok__rtj)
        impl = pjfok__rtj['impl']
        return impl
    return bodo.hiframes.dataframe_impl._gen_init_df(cdjx__endvc, out_cols,
        ozp__oro)


def _get_rolling_func_args(fname):
    if fname == 'apply':
        return (
            'func, raw=False, engine=None, engine_kwargs=None, args=None, kwargs=None\n'
            )
    elif fname == 'corr':
        return 'other=None, pairwise=None, ddof=1\n'
    elif fname == 'cov':
        return 'other=None, pairwise=None, ddof=1\n'
    return ''


def create_rolling_overload(fname):

    def overload_rolling_func(rolling):
        return _gen_rolling_impl(rolling, fname)
    return overload_rolling_func


def _install_rolling_methods():
    for fname in supported_rolling_funcs:
        if fname in ('apply', 'corr', 'cov'):
            continue
        iqrq__yuf = create_rolling_overload(fname)
        overload_method(RollingType, fname, inline='always', no_unliteral=True
            )(iqrq__yuf)


def _install_rolling_unsupported_methods():
    for fname in unsupported_rolling_methods:
        overload_method(RollingType, fname, no_unliteral=True)(
            create_unsupported_overload(
            f'pandas.core.window.rolling.Rolling.{fname}()'))


_install_rolling_methods()
_install_rolling_unsupported_methods()


def _get_corr_cov_out_cols(rolling, other, func_name):
    if not isinstance(other, DataFrameType):
        raise_bodo_error(
            f"DataFrame.rolling.{func_name}(): requires providing a DataFrame for 'other'"
            )
    rmapd__qocs = rolling.selection
    if rolling.on is not None:
        raise BodoError(
            f'variable window rolling {func_name} not supported yet.')
    out_cols = tuple(sorted(set(rmapd__qocs) | set(other.columns), key=lambda
        k: str(k)))
    return out_cols


def _gen_corr_cov_out_data(out_cols, df_cols, other_cols, window_type,
    func_name):
    kse__kfcv = not isinstance(window_type, types.Integer)
    jfo__wwoy = 'None'
    if kse__kfcv:
        jfo__wwoy = 'bodo.utils.conversion.index_to_array(index)'
    jvzc__yco = 'on_arr, ' if kse__kfcv else ''
    ozp__oro = []
    if out_cols is None:
        return (
            f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_series_ext.get_series_data(df), bodo.hiframes.pd_series_ext.get_series_data(other), {jvzc__yco}window, minp, center)'
            , jfo__wwoy)
    for jpeqx__wqws in out_cols:
        if jpeqx__wqws in df_cols and jpeqx__wqws in other_cols:
            kuffj__bainn = df_cols.index(jpeqx__wqws)
            lkd__can = other_cols.index(jpeqx__wqws)
            wsw__plj = (
                f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {kuffj__bainn}), bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {lkd__can}), {jvzc__yco}window, minp, center)'
                )
        else:
            wsw__plj = 'np.full(len(df), np.nan)'
        ozp__oro.append(wsw__plj)
    return ', '.join(ozp__oro), jfo__wwoy


@overload_method(RollingType, 'corr', inline='always', no_unliteral=True)
def overload_rolling_corr(rolling, other=None, pairwise=None, ddof=1):
    teylc__cill = {'pairwise': pairwise, 'ddof': ddof}
    ahr__ieh = {'pairwise': None, 'ddof': 1}
    check_unsupported_args('pandas.core.window.rolling.Rolling.corr',
        teylc__cill, ahr__ieh, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'corr', other)


@overload_method(RollingType, 'cov', inline='always', no_unliteral=True)
def overload_rolling_cov(rolling, other=None, pairwise=None, ddof=1):
    teylc__cill = {'ddof': ddof, 'pairwise': pairwise}
    ahr__ieh = {'ddof': 1, 'pairwise': None}
    check_unsupported_args('pandas.core.window.rolling.Rolling.cov',
        teylc__cill, ahr__ieh, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'cov', other)


@infer
class GetItemDataFrameRolling2(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        rolling, yqf__uyefn = args
        if isinstance(rolling, RollingType):
            rmapd__qocs = rolling.obj_type.selection if isinstance(rolling.
                obj_type, DataFrameGroupByType) else rolling.obj_type.columns
            series_select = False
            if isinstance(yqf__uyefn, (tuple, list)):
                if len(set(yqf__uyefn).difference(set(rmapd__qocs))) > 0:
                    raise_const_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(set(yqf__uyefn).difference(set(rmapd__qocs))))
                selection = list(yqf__uyefn)
            else:
                if yqf__uyefn not in rmapd__qocs:
                    raise_const_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(yqf__uyefn))
                selection = [yqf__uyefn]
                series_select = True
            if rolling.on is not None:
                selection.append(rolling.on)
            syewo__nub = RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, tuple(selection), True, series_select)
            return signature(syewo__nub, *args)


@lower_builtin('static_getitem', RollingType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@infer_getattr
class RollingAttribute(AttributeTemplate):
    key = RollingType

    def generic_resolve(self, rolling, attr):
        rmapd__qocs = ()
        if isinstance(rolling.obj_type, DataFrameGroupByType):
            rmapd__qocs = rolling.obj_type.selection
        if isinstance(rolling.obj_type, DataFrameType):
            rmapd__qocs = rolling.obj_type.columns
        if attr in rmapd__qocs:
            return RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, (attr,) if rolling.on is None else (attr,
                rolling.on), True, True)


def _validate_rolling_args(obj, window, min_periods, center, on):
    assert isinstance(obj, (SeriesType, DataFrameType, DataFrameGroupByType)
        ), 'invalid rolling obj'
    func_name = 'Series' if isinstance(obj, SeriesType
        ) else 'DataFrame' if isinstance(obj, DataFrameType
        ) else 'DataFrameGroupBy'
    if not (is_overload_int(window) or is_overload_constant_str(window) or 
        window == bodo.string_type or window in (pd_timedelta_type,
        datetime_timedelta_type)):
        raise BodoError(
            f"{func_name}.rolling(): 'window' should be int or time offset (str, pd.Timedelta, datetime.timedelta), not {window}"
            )
    if not is_overload_bool(center):
        raise BodoError(
            f'{func_name}.rolling(): center must be a boolean, not {center}')
    if not (is_overload_none(min_periods) or isinstance(min_periods, types.
        Integer)):
        raise BodoError(
            f'{func_name}.rolling(): min_periods must be an integer, not {min_periods}'
            )
    if isinstance(obj, SeriesType) and not is_overload_none(on):
        raise BodoError(
            f"{func_name}.rolling(): 'on' not supported for Series yet (can use a DataFrame instead)."
            )
    jdh__muha = obj.columns if isinstance(obj, DataFrameType
        ) else obj.df_type.columns if isinstance(obj, DataFrameGroupByType
        ) else []
    zigwt__jgdn = [obj.data] if isinstance(obj, SeriesType
        ) else obj.data if isinstance(obj, DataFrameType) else obj.df_type.data
    if not is_overload_none(on) and (not is_literal_type(on) or 
        get_literal_value(on) not in jdh__muha):
        raise BodoError(
            f"{func_name}.rolling(): 'on' should be a constant column name.")
    if not is_overload_none(on):
        shjnj__fcg = zigwt__jgdn[jdh__muha.index(get_literal_value(on))]
        if not isinstance(shjnj__fcg, types.Array
            ) or shjnj__fcg.dtype != bodo.datetime64ns:
            raise BodoError(
                f"{func_name}.rolling(): 'on' column should have datetime64 data."
                )
    if not any(isinstance(cmnfe__hubv.dtype, (types.Boolean, types.Number)) for
        cmnfe__hubv in zigwt__jgdn):
        raise BodoError(f'{func_name}.rolling(): No numeric types to aggregate'
            )
