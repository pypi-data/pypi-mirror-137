"""
Support for Series.dt attributes and methods
"""
import datetime
import operator
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import intrinsic, make_attribute_wrapper, models, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, raise_bodo_error
dt64_dtype = np.dtype('datetime64[ns]')
timedelta64_dtype = np.dtype('timedelta64[ns]')


class SeriesDatetimePropertiesType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        derjn__jyo = 'SeriesDatetimePropertiesType({})'.format(stype)
        super(SeriesDatetimePropertiesType, self).__init__(derjn__jyo)


@register_model(SeriesDatetimePropertiesType)
class SeriesDtModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ldyj__rfhdq = [('obj', fe_type.stype)]
        super(SeriesDtModel, self).__init__(dmm, fe_type, ldyj__rfhdq)


make_attribute_wrapper(SeriesDatetimePropertiesType, 'obj', '_obj')


@intrinsic
def init_series_dt_properties(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        bypr__ntvoa, = args
        nbzb__shtd = signature.return_type
        lqbi__fevx = cgutils.create_struct_proxy(nbzb__shtd)(context, builder)
        lqbi__fevx.obj = bypr__ntvoa
        context.nrt.incref(builder, signature.args[0], bypr__ntvoa)
        return lqbi__fevx._getvalue()
    return SeriesDatetimePropertiesType(obj)(obj), codegen


@overload_attribute(SeriesType, 'dt')
def overload_series_dt(s):
    if not (bodo.hiframes.pd_series_ext.is_dt64_series_typ(s) or bodo.
        hiframes.pd_series_ext.is_timedelta64_series_typ(s)):
        raise_bodo_error('Can only use .dt accessor with datetimelike values.')
    return lambda s: bodo.hiframes.series_dt_impl.init_series_dt_properties(s)


def create_date_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPDatetime('ns'):
            return
        qkvk__lyxd = 'def impl(S_dt):\n'
        qkvk__lyxd += '    S = S_dt._obj\n'
        qkvk__lyxd += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        qkvk__lyxd += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        qkvk__lyxd += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        qkvk__lyxd += '    numba.parfors.parfor.init_prange()\n'
        qkvk__lyxd += '    n = len(arr)\n'
        if field in ('is_leap_year', 'is_month_start', 'is_month_end',
            'is_quarter_start', 'is_quarter_end', 'is_year_start',
            'is_year_end'):
            qkvk__lyxd += '    out_arr = np.empty(n, np.bool_)\n'
        else:
            qkvk__lyxd += (
                '    out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n'
                )
        qkvk__lyxd += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        qkvk__lyxd += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        qkvk__lyxd += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
        qkvk__lyxd += '            continue\n'
        qkvk__lyxd += (
            '        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arr[i])\n'
            )
        if field in ('year', 'month', 'day'):
            qkvk__lyxd += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            if field in ('month', 'day'):
                qkvk__lyxd += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            qkvk__lyxd += '        out_arr[i] = {}\n'.format(field)
        elif field in ('dayofyear', 'day_of_year', 'dayofweek',
            'day_of_week', 'weekday'):
            szagm__dboj = {'dayofyear': 'get_day_of_year', 'day_of_year':
                'get_day_of_year', 'dayofweek': 'get_day_of_week',
                'day_of_week': 'get_day_of_week', 'weekday': 'get_day_of_week'}
            qkvk__lyxd += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            qkvk__lyxd += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            qkvk__lyxd += (
                """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month, day)
"""
                .format(szagm__dboj[field]))
        elif field == 'is_leap_year':
            qkvk__lyxd += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            qkvk__lyxd += """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(year)
"""
        elif field in ('daysinmonth', 'days_in_month'):
            szagm__dboj = {'days_in_month': 'get_days_in_month',
                'daysinmonth': 'get_days_in_month'}
            qkvk__lyxd += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            qkvk__lyxd += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            qkvk__lyxd += (
                '        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month)\n'
                .format(szagm__dboj[field]))
        else:
            qkvk__lyxd += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
            qkvk__lyxd += '        out_arr[i] = ts.' + field + '\n'
        qkvk__lyxd += (
            '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        tqkb__kucf = {}
        exec(qkvk__lyxd, {'bodo': bodo, 'numba': numba, 'np': np}, tqkb__kucf)
        impl = tqkb__kucf['impl']
        return impl
    return overload_field


def _install_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        eahu__zzjo = create_date_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(eahu__zzjo)


_install_date_fields()


def create_date_method_overload(method):
    gtbz__mfsc = method in ['day_name', 'month_name']
    if gtbz__mfsc:
        qkvk__lyxd = 'def overload_method(S_dt, locale=None):\n'
        qkvk__lyxd += '    unsupported_args = dict(locale=locale)\n'
        qkvk__lyxd += '    arg_defaults = dict(locale=None)\n'
        qkvk__lyxd += '    bodo.utils.typing.check_unsupported_args(\n'
        qkvk__lyxd += f"        'Series.dt.{method}',\n"
        qkvk__lyxd += '        unsupported_args,\n'
        qkvk__lyxd += '        arg_defaults,\n'
        qkvk__lyxd += "        package_name='pandas',\n"
        qkvk__lyxd += "        module_name='Series',\n"
        qkvk__lyxd += '    )\n'
    else:
        qkvk__lyxd = 'def overload_method(S_dt):\n'
    qkvk__lyxd += '    if not S_dt.stype.dtype == bodo.datetime64ns:\n'
    qkvk__lyxd += '        return\n'
    if gtbz__mfsc:
        qkvk__lyxd += '    def impl(S_dt, locale=None):\n'
    else:
        qkvk__lyxd += '    def impl(S_dt):\n'
    qkvk__lyxd += '        S = S_dt._obj\n'
    qkvk__lyxd += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    qkvk__lyxd += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    qkvk__lyxd += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    qkvk__lyxd += '        numba.parfors.parfor.init_prange()\n'
    qkvk__lyxd += '        n = len(arr)\n'
    if gtbz__mfsc:
        qkvk__lyxd += """        out_arr = bodo.utils.utils.alloc_type(n, bodo.string_array_type, (-1,))
"""
    else:
        qkvk__lyxd += (
            "        out_arr = np.empty(n, np.dtype('datetime64[ns]'))\n")
    qkvk__lyxd += '        for i in numba.parfors.parfor.internal_prange(n):\n'
    qkvk__lyxd += '            if bodo.libs.array_kernels.isna(arr, i):\n'
    qkvk__lyxd += '                bodo.libs.array_kernels.setna(out_arr, i)\n'
    qkvk__lyxd += '                continue\n'
    qkvk__lyxd += """            ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(arr[i])
"""
    qkvk__lyxd += f'            method_val = ts.{method}()\n'
    if gtbz__mfsc:
        qkvk__lyxd += '            out_arr[i] = method_val\n'
    else:
        qkvk__lyxd += """            out_arr[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(method_val.value)
"""
    qkvk__lyxd += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    qkvk__lyxd += '    return impl\n'
    tqkb__kucf = {}
    exec(qkvk__lyxd, {'bodo': bodo, 'numba': numba, 'np': np}, tqkb__kucf)
    overload_method = tqkb__kucf['overload_method']
    return overload_method


def _install_date_methods():
    for method in bodo.hiframes.pd_timestamp_ext.date_methods:
        eahu__zzjo = create_date_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            eahu__zzjo)


_install_date_methods()


@overload_attribute(SeriesDatetimePropertiesType, 'date')
def series_dt_date_overload(S_dt):
    if not S_dt.stype.dtype == types.NPDatetime('ns'):
        return

    def impl(S_dt):
        vnh__dho = S_dt._obj
        pjms__fvfan = bodo.hiframes.pd_series_ext.get_series_data(vnh__dho)
        erv__wkjf = bodo.hiframes.pd_series_ext.get_series_index(vnh__dho)
        derjn__jyo = bodo.hiframes.pd_series_ext.get_series_name(vnh__dho)
        numba.parfors.parfor.init_prange()
        cuxb__acep = len(pjms__fvfan)
        xviz__mwp = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
            cuxb__acep)
        for jbu__wwbje in numba.parfors.parfor.internal_prange(cuxb__acep):
            guqj__fwayp = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                pjms__fvfan[jbu__wwbje])
            wqyh__ccyam = (bodo.hiframes.pd_timestamp_ext.
                convert_datetime64_to_timestamp(guqj__fwayp))
            xviz__mwp[jbu__wwbje] = datetime.date(wqyh__ccyam.year,
                wqyh__ccyam.month, wqyh__ccyam.day)
        return bodo.hiframes.pd_series_ext.init_series(xviz__mwp, erv__wkjf,
            derjn__jyo)
    return impl


def create_series_dt_df_output_overload(attr):

    def series_dt_df_output_overload(S_dt):
        if not (attr == 'components' and S_dt.stype.dtype == types.
            NPTimedelta('ns') or attr == 'isocalendar' and S_dt.stype.dtype ==
            types.NPDatetime('ns')):
            return
        if attr == 'components':
            lnw__ushq = ['days', 'hours', 'minutes', 'seconds',
                'milliseconds', 'microseconds', 'nanoseconds']
            fbwz__pza = 'convert_numpy_timedelta64_to_pd_timedelta'
            hback__wyxm = 'np.empty(n, np.int64)'
            hbr__cbemu = attr
        elif attr == 'isocalendar':
            lnw__ushq = ['year', 'week', 'day']
            fbwz__pza = 'convert_datetime64_to_timestamp'
            hback__wyxm = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.uint32)'
            hbr__cbemu = attr + '()'
        qkvk__lyxd = 'def impl(S_dt):\n'
        qkvk__lyxd += '    S = S_dt._obj\n'
        qkvk__lyxd += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        qkvk__lyxd += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        qkvk__lyxd += '    numba.parfors.parfor.init_prange()\n'
        qkvk__lyxd += '    n = len(arr)\n'
        for field in lnw__ushq:
            qkvk__lyxd += '    {} = {}\n'.format(field, hback__wyxm)
        qkvk__lyxd += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        qkvk__lyxd += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        for field in lnw__ushq:
            qkvk__lyxd += ('            bodo.libs.array_kernels.setna({}, i)\n'
                .format(field))
        qkvk__lyxd += '            continue\n'
        hfth__mddua = '(' + '[i], '.join(lnw__ushq) + '[i])'
        qkvk__lyxd += (
            '        {} = bodo.hiframes.pd_timestamp_ext.{}(arr[i]).{}\n'.
            format(hfth__mddua, fbwz__pza, hbr__cbemu))
        pinl__cxcs = '(' + ', '.join(lnw__ushq) + ')'
        bwdd__ckbi = "('" + "', '".join(lnw__ushq) + "')"
        qkvk__lyxd += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, index, {})\n'
            .format(pinl__cxcs, bwdd__ckbi))
        tqkb__kucf = {}
        exec(qkvk__lyxd, {'bodo': bodo, 'numba': numba, 'np': np}, tqkb__kucf)
        impl = tqkb__kucf['impl']
        return impl
    return series_dt_df_output_overload


def _install_df_output_overload():
    baa__zwg = [('components', overload_attribute), ('isocalendar',
        overload_method)]
    for attr, vng__rfbf in baa__zwg:
        eahu__zzjo = create_series_dt_df_output_overload(attr)
        vng__rfbf(SeriesDatetimePropertiesType, attr, inline='always')(
            eahu__zzjo)


_install_df_output_overload()


def create_timedelta_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        qkvk__lyxd = 'def impl(S_dt):\n'
        qkvk__lyxd += '    S = S_dt._obj\n'
        qkvk__lyxd += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        qkvk__lyxd += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        qkvk__lyxd += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        qkvk__lyxd += '    numba.parfors.parfor.init_prange()\n'
        qkvk__lyxd += '    n = len(A)\n'
        qkvk__lyxd += (
            '    B = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
        qkvk__lyxd += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        qkvk__lyxd += '        if bodo.libs.array_kernels.isna(A, i):\n'
        qkvk__lyxd += '            bodo.libs.array_kernels.setna(B, i)\n'
        qkvk__lyxd += '            continue\n'
        qkvk__lyxd += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if field == 'nanoseconds':
            qkvk__lyxd += '        B[i] = td64 % 1000\n'
        elif field == 'microseconds':
            qkvk__lyxd += '        B[i] = td64 // 1000 % 1000000\n'
        elif field == 'seconds':
            qkvk__lyxd += (
                '        B[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
        elif field == 'days':
            qkvk__lyxd += (
                '        B[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
        else:
            assert False, 'invalid timedelta field'
        qkvk__lyxd += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        tqkb__kucf = {}
        exec(qkvk__lyxd, {'numba': numba, 'np': np, 'bodo': bodo}, tqkb__kucf)
        impl = tqkb__kucf['impl']
        return impl
    return overload_field


def create_timedelta_method_overload(method):

    def overload_method(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        qkvk__lyxd = 'def impl(S_dt):\n'
        qkvk__lyxd += '    S = S_dt._obj\n'
        qkvk__lyxd += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        qkvk__lyxd += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        qkvk__lyxd += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        qkvk__lyxd += '    numba.parfors.parfor.init_prange()\n'
        qkvk__lyxd += '    n = len(A)\n'
        if method == 'total_seconds':
            qkvk__lyxd += '    B = np.empty(n, np.float64)\n'
        else:
            qkvk__lyxd += """    B = bodo.hiframes.datetime_timedelta_ext.alloc_datetime_timedelta_array(n)
"""
        qkvk__lyxd += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        qkvk__lyxd += '        if bodo.libs.array_kernels.isna(A, i):\n'
        qkvk__lyxd += '            bodo.libs.array_kernels.setna(B, i)\n'
        qkvk__lyxd += '            continue\n'
        qkvk__lyxd += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if method == 'total_seconds':
            qkvk__lyxd += '        B[i] = td64 / (1000.0 * 1000000.0)\n'
        elif method == 'to_pytimedelta':
            qkvk__lyxd += (
                '        B[i] = datetime.timedelta(microseconds=td64 // 1000)\n'
                )
        else:
            assert False, 'invalid timedelta method'
        if method == 'total_seconds':
            qkvk__lyxd += (
                '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
                )
        else:
            qkvk__lyxd += '    return B\n'
        tqkb__kucf = {}
        exec(qkvk__lyxd, {'numba': numba, 'np': np, 'bodo': bodo,
            'datetime': datetime}, tqkb__kucf)
        impl = tqkb__kucf['impl']
        return impl
    return overload_method


def _install_S_dt_timedelta_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        eahu__zzjo = create_timedelta_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(eahu__zzjo)


_install_S_dt_timedelta_fields()


def _install_S_dt_timedelta_methods():
    for method in bodo.hiframes.pd_timestamp_ext.timedelta_methods:
        eahu__zzjo = create_timedelta_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            eahu__zzjo)


_install_S_dt_timedelta_methods()


@overload_method(SeriesDatetimePropertiesType, 'strftime', inline='always',
    no_unliteral=True)
def dt_strftime(S_dt, date_format):
    if S_dt.stype.dtype != types.NPDatetime('ns'):
        return
    if types.unliteral(date_format) != types.unicode_type:
        raise BodoError(
            "Series.str.strftime(): 'date_format' argument must be a string")

    def impl(S_dt, date_format):
        vnh__dho = S_dt._obj
        ikgm__klg = bodo.hiframes.pd_series_ext.get_series_data(vnh__dho)
        erv__wkjf = bodo.hiframes.pd_series_ext.get_series_index(vnh__dho)
        derjn__jyo = bodo.hiframes.pd_series_ext.get_series_name(vnh__dho)
        numba.parfors.parfor.init_prange()
        cuxb__acep = len(ikgm__klg)
        szzx__rgli = bodo.libs.str_arr_ext.pre_alloc_string_array(cuxb__acep,
            -1)
        for wel__fvbs in numba.parfors.parfor.internal_prange(cuxb__acep):
            if bodo.libs.array_kernels.isna(ikgm__klg, wel__fvbs):
                bodo.libs.array_kernels.setna(szzx__rgli, wel__fvbs)
                continue
            szzx__rgli[wel__fvbs
                ] = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(
                ikgm__klg[wel__fvbs]).strftime(date_format)
        return bodo.hiframes.pd_series_ext.init_series(szzx__rgli,
            erv__wkjf, derjn__jyo)
    return impl


def create_timedelta_freq_overload(method):

    def freq_overload(S_dt, freq, ambiguous='raise', nonexistent='raise'):
        if S_dt.stype.dtype != types.NPTimedelta('ns'
            ) and S_dt.stype.dtype != types.NPDatetime('ns'):
            return
        iiia__gkn = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        htlr__dud = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Series.dt.{method}', iiia__gkn, htlr__dud,
            package_name='pandas', module_name='Series')
        qkvk__lyxd = (
            "def impl(S_dt, freq, ambiguous='raise', nonexistent='raise'):\n")
        qkvk__lyxd += '    S = S_dt._obj\n'
        qkvk__lyxd += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        qkvk__lyxd += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        qkvk__lyxd += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        qkvk__lyxd += '    numba.parfors.parfor.init_prange()\n'
        qkvk__lyxd += '    n = len(A)\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            qkvk__lyxd += "    B = np.empty(n, np.dtype('timedelta64[ns]'))\n"
        else:
            qkvk__lyxd += "    B = np.empty(n, np.dtype('datetime64[ns]'))\n"
        qkvk__lyxd += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        qkvk__lyxd += '        if bodo.libs.array_kernels.isna(A, i):\n'
        qkvk__lyxd += '            bodo.libs.array_kernels.setna(B, i)\n'
        qkvk__lyxd += '            continue\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            uvc__hcnot = (
                'bodo.hiframes.pd_timestamp_ext.convert_numpy_timedelta64_to_pd_timedelta'
                )
            mzn__zhv = 'bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64'
        else:
            uvc__hcnot = (
                'bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp'
                )
            mzn__zhv = 'bodo.hiframes.pd_timestamp_ext.integer_to_dt64'
        qkvk__lyxd += '        B[i] = {}({}(A[i]).{}(freq).value)\n'.format(
            mzn__zhv, uvc__hcnot, method)
        qkvk__lyxd += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        tqkb__kucf = {}
        exec(qkvk__lyxd, {'numba': numba, 'np': np, 'bodo': bodo}, tqkb__kucf)
        impl = tqkb__kucf['impl']
        return impl
    return freq_overload


def _install_S_dt_timedelta_freq_methods():
    eezw__prbrf = ['ceil', 'floor', 'round']
    for method in eezw__prbrf:
        eahu__zzjo = create_timedelta_freq_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            eahu__zzjo)


_install_S_dt_timedelta_freq_methods()


def create_bin_op_overload(op):

    def overload_series_dt_binop(lhs, rhs):
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs):
            iwhy__esgy = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                knl__hpp = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                erv__wkjf = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                derjn__jyo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                tqdh__ouuhm = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                cuxb__acep = len(knl__hpp)
                vnh__dho = np.empty(cuxb__acep, timedelta64_dtype)
                czbv__usvv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    iwhy__esgy)
                for jbu__wwbje in numba.parfors.parfor.internal_prange(
                    cuxb__acep):
                    gxvso__feuf = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(knl__hpp[jbu__wwbje]))
                    rti__hwha = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        tqdh__ouuhm[jbu__wwbje])
                    if gxvso__feuf == czbv__usvv or rti__hwha == czbv__usvv:
                        rakcm__ovciz = czbv__usvv
                    else:
                        rakcm__ovciz = op(gxvso__feuf, rti__hwha)
                    vnh__dho[jbu__wwbje
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        rakcm__ovciz)
                return bodo.hiframes.pd_series_ext.init_series(vnh__dho,
                    erv__wkjf, derjn__jyo)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs):
            iwhy__esgy = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pjms__fvfan = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                erv__wkjf = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                derjn__jyo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                tqdh__ouuhm = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                cuxb__acep = len(pjms__fvfan)
                vnh__dho = np.empty(cuxb__acep, dt64_dtype)
                czbv__usvv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    iwhy__esgy)
                for jbu__wwbje in numba.parfors.parfor.internal_prange(
                    cuxb__acep):
                    hdih__zepc = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(pjms__fvfan[jbu__wwbje]))
                    iqtc__xbdra = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(tqdh__ouuhm[jbu__wwbje]))
                    if hdih__zepc == czbv__usvv or iqtc__xbdra == czbv__usvv:
                        rakcm__ovciz = czbv__usvv
                    else:
                        rakcm__ovciz = op(hdih__zepc, iqtc__xbdra)
                    vnh__dho[jbu__wwbje
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        rakcm__ovciz)
                return bodo.hiframes.pd_series_ext.init_series(vnh__dho,
                    erv__wkjf, derjn__jyo)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs):
            iwhy__esgy = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pjms__fvfan = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                erv__wkjf = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                derjn__jyo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                tqdh__ouuhm = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                cuxb__acep = len(pjms__fvfan)
                vnh__dho = np.empty(cuxb__acep, dt64_dtype)
                czbv__usvv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    iwhy__esgy)
                for jbu__wwbje in numba.parfors.parfor.internal_prange(
                    cuxb__acep):
                    hdih__zepc = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(pjms__fvfan[jbu__wwbje]))
                    iqtc__xbdra = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(tqdh__ouuhm[jbu__wwbje]))
                    if hdih__zepc == czbv__usvv or iqtc__xbdra == czbv__usvv:
                        rakcm__ovciz = czbv__usvv
                    else:
                        rakcm__ovciz = op(hdih__zepc, iqtc__xbdra)
                    vnh__dho[jbu__wwbje
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        rakcm__ovciz)
                return bodo.hiframes.pd_series_ext.init_series(vnh__dho,
                    erv__wkjf, derjn__jyo)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            iwhy__esgy = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pjms__fvfan = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                erv__wkjf = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                derjn__jyo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                cuxb__acep = len(pjms__fvfan)
                vnh__dho = np.empty(cuxb__acep, timedelta64_dtype)
                czbv__usvv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    iwhy__esgy)
                vacs__fiel = rhs.value
                for jbu__wwbje in numba.parfors.parfor.internal_prange(
                    cuxb__acep):
                    hdih__zepc = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(pjms__fvfan[jbu__wwbje]))
                    if hdih__zepc == czbv__usvv or vacs__fiel == czbv__usvv:
                        rakcm__ovciz = czbv__usvv
                    else:
                        rakcm__ovciz = op(hdih__zepc, vacs__fiel)
                    vnh__dho[jbu__wwbje
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        rakcm__ovciz)
                return bodo.hiframes.pd_series_ext.init_series(vnh__dho,
                    erv__wkjf, derjn__jyo)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            iwhy__esgy = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pjms__fvfan = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                erv__wkjf = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                derjn__jyo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                cuxb__acep = len(pjms__fvfan)
                vnh__dho = np.empty(cuxb__acep, timedelta64_dtype)
                czbv__usvv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    iwhy__esgy)
                vacs__fiel = lhs.value
                for jbu__wwbje in numba.parfors.parfor.internal_prange(
                    cuxb__acep):
                    hdih__zepc = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(pjms__fvfan[jbu__wwbje]))
                    if vacs__fiel == czbv__usvv or hdih__zepc == czbv__usvv:
                        rakcm__ovciz = czbv__usvv
                    else:
                        rakcm__ovciz = op(vacs__fiel, hdih__zepc)
                    vnh__dho[jbu__wwbje
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        rakcm__ovciz)
                return bodo.hiframes.pd_series_ext.init_series(vnh__dho,
                    erv__wkjf, derjn__jyo)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            iwhy__esgy = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pjms__fvfan = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                erv__wkjf = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                derjn__jyo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                cuxb__acep = len(pjms__fvfan)
                vnh__dho = np.empty(cuxb__acep, dt64_dtype)
                czbv__usvv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    iwhy__esgy)
                ayss__hsdg = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                iqtc__xbdra = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ayss__hsdg))
                for jbu__wwbje in numba.parfors.parfor.internal_prange(
                    cuxb__acep):
                    hdih__zepc = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(pjms__fvfan[jbu__wwbje]))
                    if hdih__zepc == czbv__usvv or iqtc__xbdra == czbv__usvv:
                        rakcm__ovciz = czbv__usvv
                    else:
                        rakcm__ovciz = op(hdih__zepc, iqtc__xbdra)
                    vnh__dho[jbu__wwbje
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        rakcm__ovciz)
                return bodo.hiframes.pd_series_ext.init_series(vnh__dho,
                    erv__wkjf, derjn__jyo)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            iwhy__esgy = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pjms__fvfan = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                erv__wkjf = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                derjn__jyo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                cuxb__acep = len(pjms__fvfan)
                vnh__dho = np.empty(cuxb__acep, dt64_dtype)
                czbv__usvv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    iwhy__esgy)
                ayss__hsdg = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                iqtc__xbdra = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ayss__hsdg))
                for jbu__wwbje in numba.parfors.parfor.internal_prange(
                    cuxb__acep):
                    hdih__zepc = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(pjms__fvfan[jbu__wwbje]))
                    if hdih__zepc == czbv__usvv or iqtc__xbdra == czbv__usvv:
                        rakcm__ovciz = czbv__usvv
                    else:
                        rakcm__ovciz = op(hdih__zepc, iqtc__xbdra)
                    vnh__dho[jbu__wwbje
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        rakcm__ovciz)
                return bodo.hiframes.pd_series_ext.init_series(vnh__dho,
                    erv__wkjf, derjn__jyo)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            iwhy__esgy = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pjms__fvfan = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                erv__wkjf = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                derjn__jyo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                cuxb__acep = len(pjms__fvfan)
                vnh__dho = np.empty(cuxb__acep, timedelta64_dtype)
                czbv__usvv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    iwhy__esgy)
                guqj__fwayp = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(rhs))
                hdih__zepc = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    guqj__fwayp)
                for jbu__wwbje in numba.parfors.parfor.internal_prange(
                    cuxb__acep):
                    yvw__enlk = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        pjms__fvfan[jbu__wwbje])
                    if yvw__enlk == czbv__usvv or hdih__zepc == czbv__usvv:
                        rakcm__ovciz = czbv__usvv
                    else:
                        rakcm__ovciz = op(yvw__enlk, hdih__zepc)
                    vnh__dho[jbu__wwbje
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        rakcm__ovciz)
                return bodo.hiframes.pd_series_ext.init_series(vnh__dho,
                    erv__wkjf, derjn__jyo)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            iwhy__esgy = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pjms__fvfan = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                erv__wkjf = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                derjn__jyo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                cuxb__acep = len(pjms__fvfan)
                vnh__dho = np.empty(cuxb__acep, timedelta64_dtype)
                czbv__usvv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    iwhy__esgy)
                guqj__fwayp = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(lhs))
                hdih__zepc = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    guqj__fwayp)
                for jbu__wwbje in numba.parfors.parfor.internal_prange(
                    cuxb__acep):
                    yvw__enlk = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        pjms__fvfan[jbu__wwbje])
                    if hdih__zepc == czbv__usvv or yvw__enlk == czbv__usvv:
                        rakcm__ovciz = czbv__usvv
                    else:
                        rakcm__ovciz = op(hdih__zepc, yvw__enlk)
                    vnh__dho[jbu__wwbje
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        rakcm__ovciz)
                return bodo.hiframes.pd_series_ext.init_series(vnh__dho,
                    erv__wkjf, derjn__jyo)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            iwhy__esgy = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pjms__fvfan = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                erv__wkjf = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                derjn__jyo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                cuxb__acep = len(pjms__fvfan)
                vnh__dho = np.empty(cuxb__acep, timedelta64_dtype)
                czbv__usvv = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(iwhy__esgy))
                ayss__hsdg = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                iqtc__xbdra = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ayss__hsdg))
                for jbu__wwbje in numba.parfors.parfor.internal_prange(
                    cuxb__acep):
                    qxi__uitt = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(pjms__fvfan[jbu__wwbje]))
                    if iqtc__xbdra == czbv__usvv or qxi__uitt == czbv__usvv:
                        rakcm__ovciz = czbv__usvv
                    else:
                        rakcm__ovciz = op(qxi__uitt, iqtc__xbdra)
                    vnh__dho[jbu__wwbje
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        rakcm__ovciz)
                return bodo.hiframes.pd_series_ext.init_series(vnh__dho,
                    erv__wkjf, derjn__jyo)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            iwhy__esgy = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pjms__fvfan = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                erv__wkjf = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                derjn__jyo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                cuxb__acep = len(pjms__fvfan)
                vnh__dho = np.empty(cuxb__acep, timedelta64_dtype)
                czbv__usvv = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(iwhy__esgy))
                ayss__hsdg = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                iqtc__xbdra = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ayss__hsdg))
                for jbu__wwbje in numba.parfors.parfor.internal_prange(
                    cuxb__acep):
                    qxi__uitt = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(pjms__fvfan[jbu__wwbje]))
                    if iqtc__xbdra == czbv__usvv or qxi__uitt == czbv__usvv:
                        rakcm__ovciz = czbv__usvv
                    else:
                        rakcm__ovciz = op(iqtc__xbdra, qxi__uitt)
                    vnh__dho[jbu__wwbje
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        rakcm__ovciz)
                return bodo.hiframes.pd_series_ext.init_series(vnh__dho,
                    erv__wkjf, derjn__jyo)
            return impl
        raise BodoError(f'{op} not supported for data types {lhs} and {rhs}.')
    return overload_series_dt_binop


def create_cmp_op_overload(op):

    def overload_series_dt64_cmp(lhs, rhs):
        if op == operator.ne:
            vvy__nfi = True
        else:
            vvy__nfi = False
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            iwhy__esgy = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pjms__fvfan = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                erv__wkjf = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                derjn__jyo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                cuxb__acep = len(pjms__fvfan)
                xviz__mwp = bodo.libs.bool_arr_ext.alloc_bool_array(cuxb__acep)
                czbv__usvv = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(iwhy__esgy))
                rcff__rpu = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                abx__wpmjk = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(rcff__rpu))
                for jbu__wwbje in numba.parfors.parfor.internal_prange(
                    cuxb__acep):
                    akwcs__obzbw = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(pjms__fvfan[jbu__wwbje]))
                    if akwcs__obzbw == czbv__usvv or abx__wpmjk == czbv__usvv:
                        rakcm__ovciz = vvy__nfi
                    else:
                        rakcm__ovciz = op(akwcs__obzbw, abx__wpmjk)
                    xviz__mwp[jbu__wwbje] = rakcm__ovciz
                return bodo.hiframes.pd_series_ext.init_series(xviz__mwp,
                    erv__wkjf, derjn__jyo)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            iwhy__esgy = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pjms__fvfan = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                erv__wkjf = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                derjn__jyo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                cuxb__acep = len(pjms__fvfan)
                xviz__mwp = bodo.libs.bool_arr_ext.alloc_bool_array(cuxb__acep)
                czbv__usvv = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(iwhy__esgy))
                tha__dlzo = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                akwcs__obzbw = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(tha__dlzo))
                for jbu__wwbje in numba.parfors.parfor.internal_prange(
                    cuxb__acep):
                    abx__wpmjk = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(pjms__fvfan[jbu__wwbje]))
                    if akwcs__obzbw == czbv__usvv or abx__wpmjk == czbv__usvv:
                        rakcm__ovciz = vvy__nfi
                    else:
                        rakcm__ovciz = op(akwcs__obzbw, abx__wpmjk)
                    xviz__mwp[jbu__wwbje] = rakcm__ovciz
                return bodo.hiframes.pd_series_ext.init_series(xviz__mwp,
                    erv__wkjf, derjn__jyo)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            iwhy__esgy = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pjms__fvfan = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                erv__wkjf = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                derjn__jyo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                cuxb__acep = len(pjms__fvfan)
                xviz__mwp = bodo.libs.bool_arr_ext.alloc_bool_array(cuxb__acep)
                czbv__usvv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    iwhy__esgy)
                for jbu__wwbje in numba.parfors.parfor.internal_prange(
                    cuxb__acep):
                    akwcs__obzbw = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(pjms__fvfan[jbu__wwbje]))
                    if akwcs__obzbw == czbv__usvv or rhs.value == czbv__usvv:
                        rakcm__ovciz = vvy__nfi
                    else:
                        rakcm__ovciz = op(akwcs__obzbw, rhs.value)
                    xviz__mwp[jbu__wwbje] = rakcm__ovciz
                return bodo.hiframes.pd_series_ext.init_series(xviz__mwp,
                    erv__wkjf, derjn__jyo)
            return impl
        if (lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type and
            bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs)):
            iwhy__esgy = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pjms__fvfan = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                erv__wkjf = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                derjn__jyo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                cuxb__acep = len(pjms__fvfan)
                xviz__mwp = bodo.libs.bool_arr_ext.alloc_bool_array(cuxb__acep)
                czbv__usvv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    iwhy__esgy)
                for jbu__wwbje in numba.parfors.parfor.internal_prange(
                    cuxb__acep):
                    abx__wpmjk = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(pjms__fvfan[jbu__wwbje]))
                    if abx__wpmjk == czbv__usvv or lhs.value == czbv__usvv:
                        rakcm__ovciz = vvy__nfi
                    else:
                        rakcm__ovciz = op(lhs.value, abx__wpmjk)
                    xviz__mwp[jbu__wwbje] = rakcm__ovciz
                return bodo.hiframes.pd_series_ext.init_series(xviz__mwp,
                    erv__wkjf, derjn__jyo)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (rhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(rhs)):
            iwhy__esgy = lhs.dtype('NaT')

            def impl(lhs, rhs):
                pjms__fvfan = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                erv__wkjf = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                derjn__jyo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                cuxb__acep = len(pjms__fvfan)
                xviz__mwp = bodo.libs.bool_arr_ext.alloc_bool_array(cuxb__acep)
                czbv__usvv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    iwhy__esgy)
                nme__ramr = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    rhs)
                saa__rotm = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    nme__ramr)
                for jbu__wwbje in numba.parfors.parfor.internal_prange(
                    cuxb__acep):
                    akwcs__obzbw = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(pjms__fvfan[jbu__wwbje]))
                    if akwcs__obzbw == czbv__usvv or saa__rotm == czbv__usvv:
                        rakcm__ovciz = vvy__nfi
                    else:
                        rakcm__ovciz = op(akwcs__obzbw, saa__rotm)
                    xviz__mwp[jbu__wwbje] = rakcm__ovciz
                return bodo.hiframes.pd_series_ext.init_series(xviz__mwp,
                    erv__wkjf, derjn__jyo)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (lhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(lhs)):
            iwhy__esgy = rhs.dtype('NaT')

            def impl(lhs, rhs):
                pjms__fvfan = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                erv__wkjf = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                derjn__jyo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                numba.parfors.parfor.init_prange()
                cuxb__acep = len(pjms__fvfan)
                xviz__mwp = bodo.libs.bool_arr_ext.alloc_bool_array(cuxb__acep)
                czbv__usvv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    iwhy__esgy)
                nme__ramr = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    lhs)
                saa__rotm = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    nme__ramr)
                for jbu__wwbje in numba.parfors.parfor.internal_prange(
                    cuxb__acep):
                    guqj__fwayp = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(pjms__fvfan[jbu__wwbje]))
                    if guqj__fwayp == czbv__usvv or saa__rotm == czbv__usvv:
                        rakcm__ovciz = vvy__nfi
                    else:
                        rakcm__ovciz = op(saa__rotm, guqj__fwayp)
                    xviz__mwp[jbu__wwbje] = rakcm__ovciz
                return bodo.hiframes.pd_series_ext.init_series(xviz__mwp,
                    erv__wkjf, derjn__jyo)
            return impl
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_series_dt64_cmp


series_dt_unsupported_methods = {'to_period', 'to_pydatetime',
    'tz_localize', 'tz_convert', 'asfreq', 'to_timestamp'}
series_dt_unsupported_attrs = {'time', 'timetz', 'tz', 'freq', 'qyear',
    'start_time', 'end_time'}


def _install_series_dt_unsupported():
    for zeig__dsg in series_dt_unsupported_attrs:
        rfd__wgpp = 'Series.dt.' + zeig__dsg
        overload_attribute(SeriesDatetimePropertiesType, zeig__dsg)(
            create_unsupported_overload(rfd__wgpp))
    for azwk__sza in series_dt_unsupported_methods:
        rfd__wgpp = 'Series.dt.' + azwk__sza
        overload_method(SeriesDatetimePropertiesType, azwk__sza,
            no_unliteral=True)(create_unsupported_overload(rfd__wgpp))


_install_series_dt_unsupported()
