"""
Indexing support for pd.DataFrame type.
"""
import operator
import numpy as np
import pandas as pd
from numba.core import cgutils, types
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported
from bodo.utils.transform import gen_const_tup
from bodo.utils.typing import BodoError, get_overload_const_int, get_overload_const_list, get_overload_const_str, is_immutable_array, is_list_like_index_type, is_overload_constant_int, is_overload_constant_list, is_overload_constant_str, raise_bodo_error


@infer_global(operator.getitem)
class DataFrameGetItemTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        check_runtime_cols_unsupported(args[0], 'DataFrame getitem (df[])')
        if isinstance(args[0], DataFrameType):
            return self.typecheck_df_getitem(args)
        elif isinstance(args[0], DataFrameLocType):
            return self.typecheck_loc_getitem(args)
        else:
            return

    def typecheck_loc_getitem(self, args):
        I = args[0]
        idx = args[1]
        df = I.df_type
        if isinstance(df.columns[0], tuple):
            raise_bodo_error(
                'DataFrame.loc[] getitem (location-based indexing) with multi-indexed columns not supported yet'
                )
        if is_list_like_index_type(idx) and idx.dtype == types.bool_:
            lwzul__posq = idx
            pnww__ylq = df.data
            cpjia__tsb = df.columns
            mrm__prez = self.replace_range_with_numeric_idx_if_needed(df,
                lwzul__posq)
            qyvod__pouk = DataFrameType(pnww__ylq, mrm__prez, cpjia__tsb)
            return qyvod__pouk(*args)
        if isinstance(idx, types.BaseTuple) and len(idx) == 2:
            ytmz__xxn = idx.types[0]
            aztsi__sbc = idx.types[1]
            if isinstance(ytmz__xxn, types.Integer):
                if not isinstance(df.index, bodo.hiframes.pd_index_ext.
                    RangeIndexType):
                    raise_bodo_error(
                        'Dataframe.loc[int, col_ind] getitem only supported for dataframes with RangeIndexes'
                        )
                if is_overload_constant_str(aztsi__sbc):
                    bkfx__uaml = get_overload_const_str(aztsi__sbc)
                    if bkfx__uaml not in df.columns:
                        raise_bodo_error(
                            'dataframe {} does not include column {}'.
                            format(df, bkfx__uaml))
                    ryb__gthw = df.columns.index(bkfx__uaml)
                    return df.data[ryb__gthw].dtype(*args)
                if isinstance(aztsi__sbc, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
                        )
                else:
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
                        )
            if is_list_like_index_type(ytmz__xxn
                ) and ytmz__xxn.dtype == types.bool_ or isinstance(ytmz__xxn,
                types.SliceType):
                mrm__prez = self.replace_range_with_numeric_idx_if_needed(df,
                    ytmz__xxn)
                if is_overload_constant_str(aztsi__sbc):
                    zbks__wtmny = get_overload_const_str(aztsi__sbc)
                    if zbks__wtmny not in df.columns:
                        raise_bodo_error(
                            f'dataframe {df} does not include column {zbks__wtmny}'
                            )
                    ryb__gthw = df.columns.index(zbks__wtmny)
                    ttcz__whcp = df.data[ryb__gthw]
                    wbwl__wztg = ttcz__whcp.dtype
                    goh__ciuo = types.literal(df.columns[ryb__gthw])
                    qyvod__pouk = bodo.SeriesType(wbwl__wztg, ttcz__whcp,
                        mrm__prez, goh__ciuo)
                    return qyvod__pouk(*args)
                if isinstance(aztsi__sbc, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
                        )
                elif is_overload_constant_list(aztsi__sbc):
                    bpty__qksi = get_overload_const_list(aztsi__sbc)
                    bso__nixyc = types.unliteral(aztsi__sbc)
                    if bso__nixyc.dtype == types.bool_:
                        if len(df.columns) != len(bpty__qksi):
                            raise_bodo_error(
                                f'dataframe {df} has {len(df.columns)} columns, but boolean array used with DataFrame.loc[] {bpty__qksi} has {len(bpty__qksi)} values'
                                )
                        pdgct__zxnmd = []
                        pnop__nms = []
                        for mam__uuf in range(len(bpty__qksi)):
                            if bpty__qksi[mam__uuf]:
                                pdgct__zxnmd.append(df.columns[mam__uuf])
                                pnop__nms.append(df.data[mam__uuf])
                        eod__zedwl = tuple()
                        qyvod__pouk = DataFrameType(tuple(pnop__nms),
                            mrm__prez, tuple(pdgct__zxnmd))
                        return qyvod__pouk(*args)
                    elif bso__nixyc.dtype == bodo.string_type:
                        eod__zedwl, pnop__nms = self.get_kept_cols_and_data(df,
                            bpty__qksi)
                        qyvod__pouk = DataFrameType(pnop__nms, mrm__prez,
                            eod__zedwl)
                        return qyvod__pouk(*args)
        raise_bodo_error(
            f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet. If you are trying to select a subset of the columns by passing a list of column names, that list must be a compile time constant. See https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
            )

    def typecheck_df_getitem(self, args):
        df = args[0]
        ind = args[1]
        if is_overload_constant_str(ind) or is_overload_constant_int(ind):
            ind_val = get_overload_const_str(ind) if is_overload_constant_str(
                ind) else get_overload_const_int(ind)
            if isinstance(df.columns[0], tuple):
                pdgct__zxnmd = []
                pnop__nms = []
                for mam__uuf, qsk__ufv in enumerate(df.columns):
                    if qsk__ufv[0] != ind_val:
                        continue
                    pdgct__zxnmd.append(qsk__ufv[1] if len(qsk__ufv) == 2 else
                        qsk__ufv[1:])
                    pnop__nms.append(df.data[mam__uuf])
                ttcz__whcp = tuple(pnop__nms)
                efa__wvpll = df.index
                lxbj__uclaw = tuple(pdgct__zxnmd)
                qyvod__pouk = DataFrameType(ttcz__whcp, efa__wvpll, lxbj__uclaw
                    )
                return qyvod__pouk(*args)
            else:
                if ind_val not in df.columns:
                    raise_bodo_error('dataframe {} does not include column {}'
                        .format(df, ind_val))
                ryb__gthw = df.columns.index(ind_val)
                ttcz__whcp = df.data[ryb__gthw]
                wbwl__wztg = ttcz__whcp.dtype
                efa__wvpll = df.index
                goh__ciuo = types.literal(df.columns[ryb__gthw])
                qyvod__pouk = bodo.SeriesType(wbwl__wztg, ttcz__whcp,
                    efa__wvpll, goh__ciuo)
                return qyvod__pouk(*args)
        if isinstance(ind, types.Integer) or isinstance(ind, types.UnicodeType
            ):
            raise_bodo_error(
                'df[] getitem selecting a subset of columns requires providing constant column names. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html'
                )
        if is_list_like_index_type(ind
            ) and ind.dtype == types.bool_ or isinstance(ind, types.SliceType):
            ttcz__whcp = df.data
            efa__wvpll = self.replace_range_with_numeric_idx_if_needed(df, ind)
            lxbj__uclaw = df.columns
            qyvod__pouk = DataFrameType(ttcz__whcp, efa__wvpll, lxbj__uclaw,
                is_table_format=df.is_table_format)
            return qyvod__pouk(*args)
        elif is_overload_constant_list(ind):
            xjgys__xvdn = get_overload_const_list(ind)
            lxbj__uclaw, ttcz__whcp = self.get_kept_cols_and_data(df,
                xjgys__xvdn)
            efa__wvpll = df.index
            qyvod__pouk = DataFrameType(ttcz__whcp, efa__wvpll, lxbj__uclaw)
            return qyvod__pouk(*args)
        raise_bodo_error(
            f'df[] getitem using {ind} not supported. If you are trying to select a subset of the columns, you must provide the column names you are selecting as a constant. See https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html'
            )

    def get_kept_cols_and_data(self, df, cols_to_keep_list):
        for ytzn__ixye in cols_to_keep_list:
            if ytzn__ixye not in df.columns:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(ytzn__ixye, df.columns))
        lxbj__uclaw = tuple(cols_to_keep_list)
        ttcz__whcp = tuple(df.data[df.columns.index(ktkf__hzokt)] for
            ktkf__hzokt in lxbj__uclaw)
        return lxbj__uclaw, ttcz__whcp

    def replace_range_with_numeric_idx_if_needed(self, df, ind):
        mrm__prez = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64,
            df.index.name_typ) if not isinstance(ind, types.SliceType
            ) and isinstance(df.index, bodo.hiframes.pd_index_ext.
            RangeIndexType) else df.index
        return mrm__prez


DataFrameGetItemTemplate._no_unliteral = True


@lower_builtin(operator.getitem, DataFrameType, types.Any)
def getitem_df_lower(context, builder, sig, args):
    impl = df_getitem_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def df_getitem_overload(df, ind):
    if not isinstance(df, DataFrameType):
        return
    if is_overload_constant_str(ind) or is_overload_constant_int(ind):
        ind_val = get_overload_const_str(ind) if is_overload_constant_str(ind
            ) else get_overload_const_int(ind)
        if isinstance(df.columns[0], tuple):
            pdgct__zxnmd = []
            pnop__nms = []
            for mam__uuf, qsk__ufv in enumerate(df.columns):
                if qsk__ufv[0] != ind_val:
                    continue
                pdgct__zxnmd.append(qsk__ufv[1] if len(qsk__ufv) == 2 else
                    qsk__ufv[1:])
                pnop__nms.append(
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'
                    .format(mam__uuf))
            wcbyd__vgdz = 'def impl(df, ind):\n'
            liar__yolf = (
                'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
            return bodo.hiframes.dataframe_impl._gen_init_df(wcbyd__vgdz,
                pdgct__zxnmd, ', '.join(pnop__nms), liar__yolf)
        if ind_val not in df.columns:
            raise_bodo_error('dataframe {} does not include column {}'.
                format(df, ind_val))
        col_no = df.columns.index(ind_val)
        return lambda df, ind: bodo.hiframes.pd_series_ext.init_series(bodo
            .hiframes.pd_dataframe_ext.get_dataframe_data(df, col_no), bodo
            .hiframes.pd_dataframe_ext.get_dataframe_index(df), ind_val)
    if is_overload_constant_list(ind):
        xjgys__xvdn = get_overload_const_list(ind)
        for ytzn__ixye in xjgys__xvdn:
            if ytzn__ixye not in df.columns:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(ytzn__ixye, df.columns))
        pnop__nms = ', '.join(
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}).copy()'
            .format(df.columns.index(ytzn__ixye)) for ytzn__ixye in xjgys__xvdn
            )
        wcbyd__vgdz = 'def impl(df, ind):\n'
        liar__yolf = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
        return bodo.hiframes.dataframe_impl._gen_init_df(wcbyd__vgdz,
            xjgys__xvdn, pnop__nms, liar__yolf)
    if is_list_like_index_type(ind) and ind.dtype == types.bool_ or isinstance(
        ind, types.SliceType):
        wcbyd__vgdz = 'def impl(df, ind):\n'
        if not isinstance(ind, types.SliceType):
            wcbyd__vgdz += (
                '  ind = bodo.utils.conversion.coerce_to_ndarray(ind)\n')
        liar__yolf = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[ind]')
        if df.is_table_format:
            pnop__nms = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[ind]')
        else:
            pnop__nms = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(ytzn__ixye)})[ind]'
                 for ytzn__ixye in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(wcbyd__vgdz, df.
            columns, pnop__nms, liar__yolf, out_df_type=df)
    raise_bodo_error('df[] getitem using {} not supported'.format(ind))


@overload(operator.setitem, no_unliteral=True)
def df_setitem_overload(df, idx, val):
    check_runtime_cols_unsupported(df, 'DataFrame setitem (df[])')
    if not isinstance(df, DataFrameType):
        return
    raise_bodo_error('DataFrame setitem: transform necessary')


class DataFrameILocType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        ktkf__hzokt = 'DataFrameILocType({})'.format(df_type)
        super(DataFrameILocType, self).__init__(ktkf__hzokt)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameILocType)
class DataFrameILocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nire__pwcf = [('obj', fe_type.df_type)]
        super(DataFrameILocModel, self).__init__(dmm, fe_type, nire__pwcf)


make_attribute_wrapper(DataFrameILocType, 'obj', '_obj')


@intrinsic
def init_dataframe_iloc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        pypo__pnhcv, = args
        mim__frvq = signature.return_type
        pduwr__lepxn = cgutils.create_struct_proxy(mim__frvq)(context, builder)
        pduwr__lepxn.obj = pypo__pnhcv
        context.nrt.incref(builder, signature.args[0], pypo__pnhcv)
        return pduwr__lepxn._getvalue()
    return DataFrameILocType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'iloc')
def overload_dataframe_iloc(df):
    check_runtime_cols_unsupported(df, 'DataFrame.iloc')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_iloc(df)


@overload(operator.getitem, no_unliteral=True)
def overload_iloc_getitem(I, idx):
    if not isinstance(I, DataFrameILocType):
        return
    df = I.df_type
    if isinstance(idx, types.Integer):
        return _gen_iloc_getitem_row_impl(df, df.columns, 'idx')
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and not isinstance(
        idx[1], types.SliceType):
        if not (is_overload_constant_list(idx.types[1]) or
            is_overload_constant_int(idx.types[1])):
            raise_bodo_error(
                'idx2 in df.iloc[idx1, idx2] should be a constant integer or constant list of integers. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
                )
        wjn__hhcl = len(df.data)
        if is_overload_constant_int(idx.types[1]):
            is_out_series = True
            utyi__yzf = get_overload_const_int(idx.types[1])
            if utyi__yzf < 0 or utyi__yzf >= wjn__hhcl:
                raise BodoError(
                    'df.iloc: column integer must refer to a valid column number'
                    )
            sgi__hycmb = [utyi__yzf]
        else:
            is_out_series = False
            sgi__hycmb = get_overload_const_list(idx.types[1])
            if any(not isinstance(ind, int) or ind < 0 or ind >= wjn__hhcl for
                ind in sgi__hycmb):
                raise BodoError(
                    'df.iloc: column list must be integers referring to a valid column number'
                    )
        col_names = tuple(pd.Series(df.columns, dtype=object)[sgi__hycmb])
        if isinstance(idx.types[0], types.Integer):
            if isinstance(idx.types[1], types.Integer):
                utyi__yzf = sgi__hycmb[0]

                def impl(I, idx):
                    df = I._obj
                    return bodo.utils.conversion.box_if_dt64(bodo.hiframes.
                        pd_dataframe_ext.get_dataframe_data(df, utyi__yzf)[
                        idx[0]])
                return impl
            return _gen_iloc_getitem_row_impl(df, col_names, 'idx[0]')
        if is_list_like_index_type(idx.types[0]) and isinstance(idx.types[0
            ].dtype, (types.Integer, types.Boolean)) or isinstance(idx.
            types[0], types.SliceType):
            return _gen_iloc_getitem_bool_slice_impl(df, col_names, idx.
                types[0], 'idx[0]', is_out_series)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, (types.
        Integer, types.Boolean)) or isinstance(idx, types.SliceType):
        return _gen_iloc_getitem_bool_slice_impl(df, df.columns, idx, 'idx',
            False)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):
        raise_bodo_error(
            'slice2 in df.iloc[slice1,slice2] should be constant. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
            )
    raise_bodo_error(f'df.iloc[] getitem using {idx} not supported')


def _gen_iloc_getitem_bool_slice_impl(df, col_names, idx_typ, idx,
    is_out_series):
    wcbyd__vgdz = 'def impl(I, idx):\n'
    wcbyd__vgdz += '  df = I._obj\n'
    if isinstance(idx_typ, types.SliceType):
        wcbyd__vgdz += f'  idx_t = {idx}\n'
    else:
        wcbyd__vgdz += (
            f'  idx_t = bodo.utils.conversion.coerce_to_ndarray({idx})\n')
    liar__yolf = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
    pnop__nms = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(ytzn__ixye)})[idx_t]'
         for ytzn__ixye in col_names)
    if is_out_series:
        wttda__qojuz = f"'{col_names[0]}'" if isinstance(col_names[0], str
            ) else f'{col_names[0]}'
        wcbyd__vgdz += f"""  return bodo.hiframes.pd_series_ext.init_series({pnop__nms}, {liar__yolf}, {wttda__qojuz})
"""
        qxs__brpmg = {}
        exec(wcbyd__vgdz, {'bodo': bodo}, qxs__brpmg)
        return qxs__brpmg['impl']
    return bodo.hiframes.dataframe_impl._gen_init_df(wcbyd__vgdz, col_names,
        pnop__nms, liar__yolf)


def _gen_iloc_getitem_row_impl(df, col_names, idx):
    wcbyd__vgdz = 'def impl(I, idx):\n'
    wcbyd__vgdz += '  df = I._obj\n'
    nfpb__uqwd = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(ytzn__ixye)})[{idx}]'
         for ytzn__ixye in col_names)
    wcbyd__vgdz += f"""  row_idx = bodo.hiframes.pd_index_ext.init_heter_index({gen_const_tup(col_names)}, None)
"""
    wcbyd__vgdz += f"""  return bodo.hiframes.pd_series_ext.init_series(({nfpb__uqwd},), row_idx, None)
"""
    qxs__brpmg = {}
    exec(wcbyd__vgdz, {'bodo': bodo}, qxs__brpmg)
    impl = qxs__brpmg['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def df_iloc_setitem_overload(df, idx, val):
    if not isinstance(df, DataFrameILocType):
        return
    raise_bodo_error(
        f'DataFrame.iloc setitem unsupported for dataframe {df.df_type}, index {idx}, value {val}'
        )


class DataFrameLocType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        ktkf__hzokt = 'DataFrameLocType({})'.format(df_type)
        super(DataFrameLocType, self).__init__(ktkf__hzokt)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameLocType)
class DataFrameLocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nire__pwcf = [('obj', fe_type.df_type)]
        super(DataFrameLocModel, self).__init__(dmm, fe_type, nire__pwcf)


make_attribute_wrapper(DataFrameLocType, 'obj', '_obj')


@intrinsic
def init_dataframe_loc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        pypo__pnhcv, = args
        fzbb__yof = signature.return_type
        bka__amajp = cgutils.create_struct_proxy(fzbb__yof)(context, builder)
        bka__amajp.obj = pypo__pnhcv
        context.nrt.incref(builder, signature.args[0], pypo__pnhcv)
        return bka__amajp._getvalue()
    return DataFrameLocType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'loc')
def overload_dataframe_loc(df):
    check_runtime_cols_unsupported(df, 'DataFrame.loc')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_loc(df)


@lower_builtin(operator.getitem, DataFrameLocType, types.Any)
def loc_getitem_lower(context, builder, sig, args):
    impl = overload_loc_getitem(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def overload_loc_getitem(I, idx):
    if not isinstance(I, DataFrameLocType):
        return
    df = I.df_type
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        wcbyd__vgdz = 'def impl(I, idx):\n'
        wcbyd__vgdz += '  df = I._obj\n'
        wcbyd__vgdz += (
            '  idx_t = bodo.utils.conversion.coerce_to_ndarray(idx)\n')
        liar__yolf = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
        pnop__nms = ', '.join(
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[idx_t]'
            .format(df.columns.index(ytzn__ixye)) for ytzn__ixye in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(wcbyd__vgdz, df.
            columns, pnop__nms, liar__yolf)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        bgg__krx = idx.types[1]
        if is_overload_constant_str(bgg__krx):
            ednnf__tqlpz = get_overload_const_str(bgg__krx)
            utyi__yzf = df.columns.index(ednnf__tqlpz)

            def impl_col_name(I, idx):
                df = I._obj
                liar__yolf = (bodo.hiframes.pd_dataframe_ext.
                    get_dataframe_index(df))
                thdta__jnw = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
                    df, utyi__yzf)
                return bodo.hiframes.pd_series_ext.init_series(thdta__jnw,
                    liar__yolf, ednnf__tqlpz).loc[idx[0]]
            return impl_col_name
        if is_overload_constant_list(bgg__krx):
            col_idx_list = get_overload_const_list(bgg__krx)
            if len(col_idx_list) > 0 and not isinstance(col_idx_list[0], (
                bool, np.bool_)) and not all(ytzn__ixye in df.columns for
                ytzn__ixye in col_idx_list):
                raise_bodo_error(
                    f'DataFrame.loc[]: invalid column list {col_idx_list}; not all in dataframe columns {df.columns}'
                    )
            return gen_df_loc_col_select_impl(df, col_idx_list)
    raise_bodo_error(
        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
        )


def gen_df_loc_col_select_impl(df, col_idx_list):
    if len(col_idx_list) > 0 and isinstance(col_idx_list[0], (bool, np.bool_)):
        col_idx_list = list(pd.Series(df.columns, dtype=object)[col_idx_list])
    pnop__nms = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[idx[0]]'
        .format(df.columns.index(ytzn__ixye)) for ytzn__ixye in col_idx_list)
    liar__yolf = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx[0]]')
    wcbyd__vgdz = 'def impl(I, idx):\n'
    wcbyd__vgdz += '  df = I._obj\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(wcbyd__vgdz,
        col_idx_list, pnop__nms, liar__yolf)


@overload(operator.setitem, no_unliteral=True)
def df_loc_setitem_overload(df, idx, val):
    if not isinstance(df, DataFrameLocType):
        return
    raise_bodo_error(
        f'DataFrame.loc setitem unsupported for dataframe {df.df_type}, index {idx}, value {val}'
        )


class DataFrameIatType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        ktkf__hzokt = 'DataFrameIatType({})'.format(df_type)
        super(DataFrameIatType, self).__init__(ktkf__hzokt)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameIatType)
class DataFrameIatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nire__pwcf = [('obj', fe_type.df_type)]
        super(DataFrameIatModel, self).__init__(dmm, fe_type, nire__pwcf)


make_attribute_wrapper(DataFrameIatType, 'obj', '_obj')


@intrinsic
def init_dataframe_iat(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        pypo__pnhcv, = args
        jahwv__swwon = signature.return_type
        yui__sikia = cgutils.create_struct_proxy(jahwv__swwon)(context, builder
            )
        yui__sikia.obj = pypo__pnhcv
        context.nrt.incref(builder, signature.args[0], pypo__pnhcv)
        return yui__sikia._getvalue()
    return DataFrameIatType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'iat')
def overload_dataframe_iat(df):
    check_runtime_cols_unsupported(df, 'DataFrame.iat')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_iat(df)


@overload(operator.getitem, no_unliteral=True)
def overload_iat_getitem(I, idx):
    if not isinstance(I, DataFrameIatType):
        return
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        if not isinstance(idx.types[0], types.Integer):
            raise BodoError(
                'DataFrame.iat: iAt based indexing can only have integer indexers'
                )
        if not is_overload_constant_int(idx.types[1]):
            raise_bodo_error(
                'DataFrame.iat getitem: column index must be a constant integer. For more informaton, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
                )
        utyi__yzf = get_overload_const_int(idx.types[1])

        def impl_col_ind(I, idx):
            df = I._obj
            thdta__jnw = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                utyi__yzf)
            return thdta__jnw[idx[0]]
        return impl_col_ind
    raise BodoError('df.iat[] getitem using {} not supported'.format(idx))


@overload(operator.setitem, no_unliteral=True)
def overload_iat_setitem(I, idx, val):
    if not isinstance(I, DataFrameIatType):
        return
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        if not isinstance(idx.types[0], types.Integer):
            raise BodoError(
                'DataFrame.iat: iAt based indexing can only have integer indexers'
                )
        if not is_overload_constant_int(idx.types[1]):
            raise_bodo_error(
                'DataFrame.iat setitem: column index must be a constant integer. For more informaton, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html'
                )
        utyi__yzf = get_overload_const_int(idx.types[1])
        if is_immutable_array(I.df_type.data[utyi__yzf]):
            raise BodoError(
                f'DataFrame setitem not supported for column with immutable array type {I.df_type.data}'
                )

        def impl_col_ind(I, idx, val):
            df = I._obj
            thdta__jnw = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                utyi__yzf)
            thdta__jnw[idx[0]] = bodo.utils.conversion.unbox_if_timestamp(val)
        return impl_col_ind
    raise BodoError('df.iat[] setitem using {} not supported'.format(idx))


@lower_cast(DataFrameIatType, DataFrameIatType)
@lower_cast(DataFrameILocType, DataFrameILocType)
@lower_cast(DataFrameLocType, DataFrameLocType)
def cast_series_iat(context, builder, fromty, toty, val):
    yui__sikia = cgutils.create_struct_proxy(fromty)(context, builder, val)
    bavy__jer = context.cast(builder, yui__sikia.obj, fromty.df_type, toty.
        df_type)
    serom__oor = cgutils.create_struct_proxy(toty)(context, builder)
    serom__oor.obj = bavy__jer
    return serom__oor._getvalue()
