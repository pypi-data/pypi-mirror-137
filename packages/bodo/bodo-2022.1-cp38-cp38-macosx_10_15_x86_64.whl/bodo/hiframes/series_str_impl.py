"""
Support for Series.str methods
"""
import operator
import re
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_index_ext import StringIndexType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.split_impl import get_split_view_data_ptr, get_split_view_index, string_array_split_view_type
from bodo.libs.array import get_search_regex
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.str_arr_ext import get_utf8_size, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import str_findall_count
from bodo.utils.typing import BodoError, create_unsupported_overload, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_const_str_len, is_list_like_index_type, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_list, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true, raise_bodo_error


class SeriesStrMethodType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        boazj__oguly = 'SeriesStrMethodType({})'.format(stype)
        super(SeriesStrMethodType, self).__init__(boazj__oguly)


@register_model(SeriesStrMethodType)
class SeriesStrModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        zcfvg__doaeu = [('obj', fe_type.stype)]
        super(SeriesStrModel, self).__init__(dmm, fe_type, zcfvg__doaeu)


make_attribute_wrapper(SeriesStrMethodType, 'obj', '_obj')


@intrinsic
def init_series_str_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        xfyik__gkxzn, = args
        yfmal__weh = signature.return_type
        mmf__jpz = cgutils.create_struct_proxy(yfmal__weh)(context, builder)
        mmf__jpz.obj = xfyik__gkxzn
        context.nrt.incref(builder, signature.args[0], xfyik__gkxzn)
        return mmf__jpz._getvalue()
    return SeriesStrMethodType(obj)(obj), codegen


def str_arg_check(func_name, arg_name, arg):
    if not isinstance(arg, types.UnicodeType) and not is_overload_constant_str(
        arg):
        raise_bodo_error(
            "Series.str.{}(): parameter '{}' expected a string object, not {}"
            .format(func_name, arg_name, arg))


def int_arg_check(func_name, arg_name, arg):
    if not isinstance(arg, types.Integer) and not is_overload_constant_int(arg
        ):
        raise BodoError(
            "Series.str.{}(): parameter '{}' expected an int object, not {}"
            .format(func_name, arg_name, arg))


def not_supported_arg_check(func_name, arg_name, arg, defval):
    if arg_name == 'na':
        if not isinstance(arg, types.Omitted) and (not isinstance(arg,
            float) or not np.isnan(arg)):
            raise BodoError(
                "Series.str.{}(): parameter '{}' is not supported, default: np.nan"
                .format(func_name, arg_name))
    elif not isinstance(arg, types.Omitted) and arg != defval:
        raise BodoError(
            "Series.str.{}(): parameter '{}' is not supported, default: {}"
            .format(func_name, arg_name, defval))


def common_validate_padding(func_name, width, fillchar):
    if is_overload_constant_str(fillchar):
        if get_overload_const_str_len(fillchar) != 1:
            raise BodoError(
                'Series.str.{}(): fillchar must be a character, not str'.
                format(func_name))
    elif not isinstance(fillchar, types.UnicodeType):
        raise BodoError('Series.str.{}(): fillchar must be a character, not {}'
            .format(func_name, fillchar))
    int_arg_check(func_name, 'width', width)


@overload_attribute(SeriesType, 'str')
def overload_series_str(S):
    if not isinstance(S, SeriesType) or not (S.data in (string_array_type,
        string_array_split_view_type) or isinstance(S.data, ArrayItemArrayType)
        ):
        raise_bodo_error(
            'Series.str: input should be a series of string or arrays')
    return lambda S: bodo.hiframes.series_str_impl.init_series_str_method(S)


@overload_method(SeriesStrMethodType, 'len', inline='always', no_unliteral=True
    )
def overload_str_method_len(S_str):

    def impl(S_str):
        S = S_str._obj
        wgulj__tdb = bodo.hiframes.pd_series_ext.get_series_data(S)
        rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
        boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(wgulj__tdb)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(wgulj__tdb, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = len(wgulj__tdb[i])
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            rlcoy__kvykc, boazj__oguly)
    return impl


@overload_method(SeriesStrMethodType, 'split', inline='always',
    no_unliteral=True)
def overload_str_method_split(S_str, pat=None, n=-1, expand=False):
    if not is_overload_none(pat):
        str_arg_check('split', 'pat', pat)
    int_arg_check('split', 'n', n)
    not_supported_arg_check('split', 'expand', expand, False)
    if is_overload_constant_str(pat) and len(get_overload_const_str(pat)
        ) == 1 and get_overload_const_str(pat).isascii(
        ) and is_overload_constant_int(n) and get_overload_const_int(n) == -1:

        def _str_split_view_impl(S_str, pat=None, n=-1, expand=False):
            S = S_str._obj
            wgulj__tdb = bodo.hiframes.pd_series_ext.get_series_data(S)
            rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
            boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.hiframes.split_impl.compute_split_view(wgulj__tdb,
                pat)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rlcoy__kvykc, boazj__oguly)
        return _str_split_view_impl

    def _str_split_impl(S_str, pat=None, n=-1, expand=False):
        S = S_str._obj
        wgulj__tdb = bodo.hiframes.pd_series_ext.get_series_data(S)
        rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
        boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.str_ext.str_split(wgulj__tdb, pat, n)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            rlcoy__kvykc, boazj__oguly)
    return _str_split_impl


@overload_method(SeriesStrMethodType, 'get', no_unliteral=True)
def overload_str_method_get(S_str, i):
    oeyp__xnsx = S_str.stype.data
    if (oeyp__xnsx != string_array_split_view_type and oeyp__xnsx !=
        string_array_type) and not isinstance(oeyp__xnsx, ArrayItemArrayType):
        raise_bodo_error(
            'Series.str.get(): only supports input type of Series(array(item)) and Series(str)'
            )
    int_arg_check('get', 'i', i)
    if isinstance(oeyp__xnsx, ArrayItemArrayType):

        def _str_get_array_impl(S_str, i):
            S = S_str._obj
            wgulj__tdb = bodo.hiframes.pd_series_ext.get_series_data(S)
            rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
            boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.array_kernels.get(wgulj__tdb, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rlcoy__kvykc, boazj__oguly)
        return _str_get_array_impl
    if oeyp__xnsx == string_array_split_view_type:

        def _str_get_split_impl(S_str, i):
            S = S_str._obj
            wgulj__tdb = bodo.hiframes.pd_series_ext.get_series_data(S)
            rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
            boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            n = len(wgulj__tdb)
            iqwb__pbwbn = 0
            for tmb__uqf in numba.parfors.parfor.internal_prange(n):
                bwss__khykw, bwss__khykw, yon__rvzzb = get_split_view_index(
                    wgulj__tdb, tmb__uqf, i)
                iqwb__pbwbn += yon__rvzzb
            numba.parfors.parfor.init_prange()
            out_arr = pre_alloc_string_array(n, iqwb__pbwbn)
            for uciw__xmtg in numba.parfors.parfor.internal_prange(n):
                edz__cpv, bsmgs__dhm, yon__rvzzb = get_split_view_index(
                    wgulj__tdb, uciw__xmtg, i)
                if edz__cpv == 0:
                    bodo.libs.array_kernels.setna(out_arr, uciw__xmtg)
                    xzwrt__wbgm = get_split_view_data_ptr(wgulj__tdb, 0)
                else:
                    bodo.libs.str_arr_ext.str_arr_set_not_na(out_arr,
                        uciw__xmtg)
                    xzwrt__wbgm = get_split_view_data_ptr(wgulj__tdb,
                        bsmgs__dhm)
                bodo.libs.str_arr_ext.setitem_str_arr_ptr(out_arr,
                    uciw__xmtg, xzwrt__wbgm, yon__rvzzb)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rlcoy__kvykc, boazj__oguly)
        return _str_get_split_impl

    def _str_get_impl(S_str, i):
        S = S_str._obj
        wgulj__tdb = bodo.hiframes.pd_series_ext.get_series_data(S)
        rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
        boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(wgulj__tdb)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(n, -1)
        for uciw__xmtg in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(wgulj__tdb, uciw__xmtg) or not len(
                wgulj__tdb[uciw__xmtg]) > i >= -len(wgulj__tdb[uciw__xmtg]):
                out_arr[uciw__xmtg] = ''
                bodo.libs.array_kernels.setna(out_arr, uciw__xmtg)
            else:
                out_arr[uciw__xmtg] = wgulj__tdb[uciw__xmtg][i]
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            rlcoy__kvykc, boazj__oguly)
    return _str_get_impl


@overload_method(SeriesStrMethodType, 'join', inline='always', no_unliteral
    =True)
def overload_str_method_join(S_str, sep):
    oeyp__xnsx = S_str.stype.data
    if (oeyp__xnsx != string_array_split_view_type and oeyp__xnsx !=
        ArrayItemArrayType(string_array_type) and oeyp__xnsx !=
        string_array_type):
        raise_bodo_error(
            'Series.str.join(): only supports input type of Series(list(str)) and Series(str)'
            )
    str_arg_check('join', 'sep', sep)

    def impl(S_str, sep):
        S = S_str._obj
        dluj__fpxx = bodo.hiframes.pd_series_ext.get_series_data(S)
        boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
        rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        n = len(dluj__fpxx)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
        for uciw__xmtg in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(dluj__fpxx, uciw__xmtg):
                out_arr[uciw__xmtg] = ''
                bodo.libs.array_kernels.setna(out_arr, uciw__xmtg)
            else:
                pww__cibq = dluj__fpxx[uciw__xmtg]
                out_arr[uciw__xmtg] = sep.join(pww__cibq)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            rlcoy__kvykc, boazj__oguly)
    return impl


@overload_method(SeriesStrMethodType, 'replace', inline='always',
    no_unliteral=True)
def overload_str_method_replace(S_str, pat, repl, n=-1, case=None, flags=0,
    regex=True):
    not_supported_arg_check('replace', 'n', n, -1)
    not_supported_arg_check('replace', 'case', case, None)
    str_arg_check('replace', 'pat', pat)
    str_arg_check('replace', 'repl', repl)
    int_arg_check('replace', 'flags', flags)
    if is_overload_true(regex):

        def _str_replace_regex_impl(S_str, pat, repl, n=-1, case=None,
            flags=0, regex=True):
            S = S_str._obj
            wgulj__tdb = bodo.hiframes.pd_series_ext.get_series_data(S)
            rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
            boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            bfmwi__qnp = re.compile(pat, flags)
            rdb__sxmxt = len(wgulj__tdb)
            out_arr = pre_alloc_string_array(rdb__sxmxt, -1)
            for uciw__xmtg in numba.parfors.parfor.internal_prange(rdb__sxmxt):
                if bodo.libs.array_kernels.isna(wgulj__tdb, uciw__xmtg):
                    out_arr[uciw__xmtg] = ''
                    bodo.libs.array_kernels.setna(out_arr, uciw__xmtg)
                    continue
                out_arr[uciw__xmtg] = bfmwi__qnp.sub(repl, wgulj__tdb[
                    uciw__xmtg])
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rlcoy__kvykc, boazj__oguly)
        return _str_replace_regex_impl
    if not is_overload_false(regex):
        raise BodoError('Series.str.replace(): regex argument should be bool')

    def _str_replace_noregex_impl(S_str, pat, repl, n=-1, case=None, flags=
        0, regex=True):
        S = S_str._obj
        wgulj__tdb = bodo.hiframes.pd_series_ext.get_series_data(S)
        rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
        boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        rdb__sxmxt = len(wgulj__tdb)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(rdb__sxmxt, -1)
        for uciw__xmtg in numba.parfors.parfor.internal_prange(rdb__sxmxt):
            if bodo.libs.array_kernels.isna(wgulj__tdb, uciw__xmtg):
                out_arr[uciw__xmtg] = ''
                bodo.libs.array_kernels.setna(out_arr, uciw__xmtg)
                continue
            out_arr[uciw__xmtg] = wgulj__tdb[uciw__xmtg].replace(pat, repl)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            rlcoy__kvykc, boazj__oguly)
    return _str_replace_noregex_impl


@numba.njit
def series_contains_regex(S, pat, case, flags, na, regex):
    with numba.objmode(out_arr=bodo.boolean_array):
        out_arr = S.array._str_contains(pat, case, flags, na, regex)
    return out_arr


def is_regex_unsupported(pat):
    kbr__gsc = ['(?a', '(?i', '(?L', '(?m', '(?s', '(?u', '(?x', '(?#']
    if is_overload_constant_str(pat):
        if isinstance(pat, types.StringLiteral):
            pat = pat.literal_value
        return any([(xsu__hbiwd in pat) for xsu__hbiwd in kbr__gsc])
    else:
        return True


@overload_method(SeriesStrMethodType, 'contains', no_unliteral=True)
def overload_str_method_contains(S_str, pat, case=True, flags=0, na=np.nan,
    regex=True):
    not_supported_arg_check('contains', 'na', na, np.nan)
    str_arg_check('contains', 'pat', pat)
    int_arg_check('contains', 'flags', flags)
    if not is_overload_constant_bool(regex):
        raise BodoError(
            "Series.str.contains(): 'regex' argument should be a constant boolean"
            )
    if not is_overload_constant_bool(case):
        raise BodoError(
            "Series.str.contains(): 'case' argument should be a constant boolean"
            )
    eein__efb = re.IGNORECASE.value
    lopbu__oxoh = 'def impl(\n'
    lopbu__oxoh += (
        '    S_str, pat, case=True, flags=0, na=np.nan, regex=True\n')
    lopbu__oxoh += '):\n'
    lopbu__oxoh += '  S = S_str._obj\n'
    lopbu__oxoh += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    lopbu__oxoh += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    lopbu__oxoh += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    lopbu__oxoh += '  l = len(arr)\n'
    lopbu__oxoh += '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    if is_overload_true(regex):
        if is_regex_unsupported(pat) or flags:
            lopbu__oxoh += """  out_arr = bodo.hiframes.series_str_impl.series_contains_regex(S, pat, case, flags, na, regex)
"""
        else:
            lopbu__oxoh += """  get_search_regex(arr, case, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    else:
        lopbu__oxoh += '  numba.parfors.parfor.init_prange()\n'
        if is_overload_false(case):
            lopbu__oxoh += '  upper_pat = pat.upper()\n'
        lopbu__oxoh += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        lopbu__oxoh += '      if bodo.libs.array_kernels.isna(arr, i):\n'
        lopbu__oxoh += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        lopbu__oxoh += '      else: \n'
        if is_overload_true(case):
            lopbu__oxoh += '          out_arr[i] = pat in arr[i]\n'
        else:
            lopbu__oxoh += (
                '          out_arr[i] = upper_pat in arr[i].upper()\n')
    lopbu__oxoh += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    zou__lpygg = {}
    exec(lopbu__oxoh, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': eein__efb, 'get_search_regex':
        get_search_regex}, zou__lpygg)
    impl = zou__lpygg['impl']
    return impl


@overload_method(SeriesStrMethodType, 'count', inline='always',
    no_unliteral=True)
def overload_str_method_count(S_str, pat, flags=0):
    str_arg_check('count', 'pat', pat)
    int_arg_check('count', 'flags', flags)

    def impl(S_str, pat, flags=0):
        S = S_str._obj
        dluj__fpxx = bodo.hiframes.pd_series_ext.get_series_data(S)
        boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
        rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
        bfmwi__qnp = re.compile(pat, flags)
        numba.parfors.parfor.init_prange()
        rdb__sxmxt = len(dluj__fpxx)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(rdb__sxmxt, np.int64)
        for i in numba.parfors.parfor.internal_prange(rdb__sxmxt):
            if bodo.libs.array_kernels.isna(dluj__fpxx, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = str_findall_count(bfmwi__qnp, dluj__fpxx[i])
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            rlcoy__kvykc, boazj__oguly)
    return impl


@overload_method(SeriesStrMethodType, 'find', inline='always', no_unliteral
    =True)
def overload_str_method_find(S_str, sub, start=0, end=None):
    str_arg_check('find', 'sub', sub)
    int_arg_check('find', 'start', start)
    if not is_overload_none(end):
        int_arg_check('find', 'end', end)

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        dluj__fpxx = bodo.hiframes.pd_series_ext.get_series_data(S)
        boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
        rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        rdb__sxmxt = len(dluj__fpxx)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(rdb__sxmxt, np.int64)
        for i in numba.parfors.parfor.internal_prange(rdb__sxmxt):
            if bodo.libs.array_kernels.isna(dluj__fpxx, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = dluj__fpxx[i].find(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            rlcoy__kvykc, boazj__oguly)
    return impl


@overload_method(SeriesStrMethodType, 'rfind', inline='always',
    no_unliteral=True)
def overload_str_method_rfind(S_str, sub, start=0, end=None):
    str_arg_check('rfind', 'sub', sub)
    if start != 0:
        int_arg_check('rfind', 'start', start)
    if not is_overload_none(end):
        int_arg_check('rfind', 'end', end)

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        dluj__fpxx = bodo.hiframes.pd_series_ext.get_series_data(S)
        boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
        rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        rdb__sxmxt = len(dluj__fpxx)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(rdb__sxmxt, np.int64)
        for i in numba.parfors.parfor.internal_prange(rdb__sxmxt):
            if bodo.libs.array_kernels.isna(dluj__fpxx, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = dluj__fpxx[i].rfind(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            rlcoy__kvykc, boazj__oguly)
    return impl


@overload_method(SeriesStrMethodType, 'center', inline='always',
    no_unliteral=True)
def overload_str_method_center(S_str, width, fillchar=' '):
    common_validate_padding('center', width, fillchar)

    def impl(S_str, width, fillchar=' '):
        S = S_str._obj
        dluj__fpxx = bodo.hiframes.pd_series_ext.get_series_data(S)
        boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
        rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        rdb__sxmxt = len(dluj__fpxx)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(rdb__sxmxt, -1)
        for uciw__xmtg in numba.parfors.parfor.internal_prange(rdb__sxmxt):
            if bodo.libs.array_kernels.isna(dluj__fpxx, uciw__xmtg):
                out_arr[uciw__xmtg] = ''
                bodo.libs.array_kernels.setna(out_arr, uciw__xmtg)
            else:
                out_arr[uciw__xmtg] = dluj__fpxx[uciw__xmtg].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            rlcoy__kvykc, boazj__oguly)
    return impl


@overload_method(SeriesStrMethodType, 'slice_replace', inline='always',
    no_unliteral=True)
def overload_str_method_slice_replace(S_str, start=0, stop=None, repl=''):
    int_arg_check('slice_replace', 'start', start)
    if not is_overload_none(stop):
        int_arg_check('slice_replace', 'stop', stop)
    str_arg_check('slice_replace', 'repl', repl)

    def impl(S_str, start=0, stop=None, repl=''):
        S = S_str._obj
        dluj__fpxx = bodo.hiframes.pd_series_ext.get_series_data(S)
        boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
        rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        rdb__sxmxt = len(dluj__fpxx)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(rdb__sxmxt, -1)
        for uciw__xmtg in numba.parfors.parfor.internal_prange(rdb__sxmxt):
            if bodo.libs.array_kernels.isna(dluj__fpxx, uciw__xmtg):
                bodo.libs.array_kernels.setna(out_arr, uciw__xmtg)
            else:
                if stop is not None:
                    nlm__hqh = dluj__fpxx[uciw__xmtg][stop:]
                else:
                    nlm__hqh = ''
                out_arr[uciw__xmtg] = dluj__fpxx[uciw__xmtg][:start
                    ] + repl + nlm__hqh
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            rlcoy__kvykc, boazj__oguly)
    return impl


@overload_method(SeriesStrMethodType, 'repeat', inline='always',
    no_unliteral=True)
def overload_str_method_repeat(S_str, repeats):
    if isinstance(repeats, types.Integer) or is_overload_constant_int(repeats):

        def impl(S_str, repeats):
            S = S_str._obj
            dluj__fpxx = bodo.hiframes.pd_series_ext.get_series_data(S)
            boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
            rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
            numba.parfors.parfor.init_prange()
            rdb__sxmxt = len(dluj__fpxx)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(rdb__sxmxt,
                -1)
            for uciw__xmtg in numba.parfors.parfor.internal_prange(rdb__sxmxt):
                if bodo.libs.array_kernels.isna(dluj__fpxx, uciw__xmtg):
                    bodo.libs.array_kernels.setna(out_arr, uciw__xmtg)
                else:
                    out_arr[uciw__xmtg] = dluj__fpxx[uciw__xmtg] * repeats
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rlcoy__kvykc, boazj__oguly)
        return impl
    elif is_overload_constant_list(repeats):
        uow__eczdl = get_overload_const_list(repeats)
        jbjfp__evx = all([isinstance(vtwzk__jruwu, int) for vtwzk__jruwu in
            uow__eczdl])
    elif is_list_like_index_type(repeats) and isinstance(repeats.dtype,
        types.Integer):
        jbjfp__evx = True
    else:
        jbjfp__evx = False
    if jbjfp__evx:

        def impl(S_str, repeats):
            S = S_str._obj
            dluj__fpxx = bodo.hiframes.pd_series_ext.get_series_data(S)
            boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
            rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
            ddo__nojgq = bodo.utils.conversion.coerce_to_array(repeats)
            numba.parfors.parfor.init_prange()
            rdb__sxmxt = len(dluj__fpxx)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(rdb__sxmxt,
                -1)
            for uciw__xmtg in numba.parfors.parfor.internal_prange(rdb__sxmxt):
                if bodo.libs.array_kernels.isna(dluj__fpxx, uciw__xmtg):
                    bodo.libs.array_kernels.setna(out_arr, uciw__xmtg)
                else:
                    out_arr[uciw__xmtg] = dluj__fpxx[uciw__xmtg] * ddo__nojgq[
                        uciw__xmtg]
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rlcoy__kvykc, boazj__oguly)
        return impl
    else:
        raise BodoError(
            'Series.str.repeat(): repeats argument must either be an integer or a sequence of integers'
            )


@overload_method(SeriesStrMethodType, 'ljust', inline='always',
    no_unliteral=True)
def overload_str_method_ljust(S_str, width, fillchar=' '):
    common_validate_padding('ljust', width, fillchar)

    def impl(S_str, width, fillchar=' '):
        S = S_str._obj
        dluj__fpxx = bodo.hiframes.pd_series_ext.get_series_data(S)
        boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
        rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        rdb__sxmxt = len(dluj__fpxx)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(rdb__sxmxt, -1)
        for uciw__xmtg in numba.parfors.parfor.internal_prange(rdb__sxmxt):
            if bodo.libs.array_kernels.isna(dluj__fpxx, uciw__xmtg):
                out_arr[uciw__xmtg] = ''
                bodo.libs.array_kernels.setna(out_arr, uciw__xmtg)
            else:
                out_arr[uciw__xmtg] = dluj__fpxx[uciw__xmtg].ljust(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            rlcoy__kvykc, boazj__oguly)
    return impl


@overload_method(SeriesStrMethodType, 'rjust', inline='always',
    no_unliteral=True)
def overload_str_method_rjust(S_str, width, fillchar=' '):
    common_validate_padding('rjust', width, fillchar)

    def impl(S_str, width, fillchar=' '):
        S = S_str._obj
        dluj__fpxx = bodo.hiframes.pd_series_ext.get_series_data(S)
        boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
        rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        rdb__sxmxt = len(dluj__fpxx)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(rdb__sxmxt, -1)
        for uciw__xmtg in numba.parfors.parfor.internal_prange(rdb__sxmxt):
            if bodo.libs.array_kernels.isna(dluj__fpxx, uciw__xmtg):
                out_arr[uciw__xmtg] = ''
                bodo.libs.array_kernels.setna(out_arr, uciw__xmtg)
            else:
                out_arr[uciw__xmtg] = dluj__fpxx[uciw__xmtg].rjust(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            rlcoy__kvykc, boazj__oguly)
    return impl


@overload_method(SeriesStrMethodType, 'pad', no_unliteral=True)
def overload_str_method_pad(S_str, width, side='left', fillchar=' '):
    common_validate_padding('pad', width, fillchar)
    if is_overload_constant_str(side):
        if get_overload_const_str(side) not in ['left', 'right', 'both']:
            raise BodoError('Series.str.pad(): Invalid Side')
    else:
        raise BodoError('Series.str.pad(): Invalid Side')

    def impl(S_str, width, side='left', fillchar=' '):
        S = S_str._obj
        dluj__fpxx = bodo.hiframes.pd_series_ext.get_series_data(S)
        boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
        rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        rdb__sxmxt = len(dluj__fpxx)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(rdb__sxmxt, -1)
        for uciw__xmtg in numba.parfors.parfor.internal_prange(rdb__sxmxt):
            if bodo.libs.array_kernels.isna(dluj__fpxx, uciw__xmtg):
                out_arr[uciw__xmtg] = ''
                bodo.libs.array_kernels.setna(out_arr, uciw__xmtg)
            elif side == 'left':
                out_arr[uciw__xmtg] = dluj__fpxx[uciw__xmtg].rjust(width,
                    fillchar)
            elif side == 'right':
                out_arr[uciw__xmtg] = dluj__fpxx[uciw__xmtg].ljust(width,
                    fillchar)
            elif side == 'both':
                out_arr[uciw__xmtg] = dluj__fpxx[uciw__xmtg].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            rlcoy__kvykc, boazj__oguly)
    return impl


@overload_method(SeriesStrMethodType, 'zfill', inline='always',
    no_unliteral=True)
def overload_str_method_zfill(S_str, width):
    int_arg_check('zfill', 'width', width)

    def impl(S_str, width):
        S = S_str._obj
        dluj__fpxx = bodo.hiframes.pd_series_ext.get_series_data(S)
        boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
        rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        rdb__sxmxt = len(dluj__fpxx)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(rdb__sxmxt, -1)
        for uciw__xmtg in numba.parfors.parfor.internal_prange(rdb__sxmxt):
            if bodo.libs.array_kernels.isna(dluj__fpxx, uciw__xmtg):
                out_arr[uciw__xmtg] = ''
                bodo.libs.array_kernels.setna(out_arr, uciw__xmtg)
            else:
                out_arr[uciw__xmtg] = dluj__fpxx[uciw__xmtg].zfill(width)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            rlcoy__kvykc, boazj__oguly)
    return impl


@overload_method(SeriesStrMethodType, 'slice', no_unliteral=True)
def overload_str_method_slice(S_str, start=None, stop=None, step=None):
    if not is_overload_none(start):
        int_arg_check('slice', 'start', start)
    if not is_overload_none(stop):
        int_arg_check('slice', 'stop', stop)
    if not is_overload_none(step):
        int_arg_check('slice', 'step', step)

    def impl(S_str, start=None, stop=None, step=None):
        S = S_str._obj
        dluj__fpxx = bodo.hiframes.pd_series_ext.get_series_data(S)
        boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
        rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        rdb__sxmxt = len(dluj__fpxx)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(rdb__sxmxt, -1)
        for uciw__xmtg in numba.parfors.parfor.internal_prange(rdb__sxmxt):
            if bodo.libs.array_kernels.isna(dluj__fpxx, uciw__xmtg):
                out_arr[uciw__xmtg] = ''
                bodo.libs.array_kernels.setna(out_arr, uciw__xmtg)
            else:
                out_arr[uciw__xmtg] = dluj__fpxx[uciw__xmtg][start:stop:step]
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            rlcoy__kvykc, boazj__oguly)
    return impl


@overload_method(SeriesStrMethodType, 'startswith', inline='always',
    no_unliteral=True)
def overload_str_method_startswith(S_str, pat, na=np.nan):
    not_supported_arg_check('startswith', 'na', na, np.nan)
    str_arg_check('startswith', 'pat', pat)

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        dluj__fpxx = bodo.hiframes.pd_series_ext.get_series_data(S)
        boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
        rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        rdb__sxmxt = len(dluj__fpxx)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(rdb__sxmxt)
        for i in numba.parfors.parfor.internal_prange(rdb__sxmxt):
            if bodo.libs.array_kernels.isna(dluj__fpxx, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = dluj__fpxx[i].startswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            rlcoy__kvykc, boazj__oguly)
    return impl


@overload_method(SeriesStrMethodType, 'endswith', inline='always',
    no_unliteral=True)
def overload_str_method_endswith(S_str, pat, na=np.nan):
    not_supported_arg_check('endswith', 'na', na, np.nan)
    str_arg_check('endswith', 'pat', pat)

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        dluj__fpxx = bodo.hiframes.pd_series_ext.get_series_data(S)
        boazj__oguly = bodo.hiframes.pd_series_ext.get_series_name(S)
        rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        rdb__sxmxt = len(dluj__fpxx)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(rdb__sxmxt)
        for i in numba.parfors.parfor.internal_prange(rdb__sxmxt):
            if bodo.libs.array_kernels.isna(dluj__fpxx, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = dluj__fpxx[i].endswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            rlcoy__kvykc, boazj__oguly)
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_str_method_getitem(S_str, ind):
    if not isinstance(S_str, SeriesStrMethodType):
        return
    if not isinstance(types.unliteral(ind), (types.SliceType, types.Integer)):
        raise BodoError(
            'index input to Series.str[] should be a slice or an integer')
    if isinstance(ind, types.SliceType):
        return lambda S_str, ind: S_str.slice(ind.start, ind.stop, ind.step)
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda S_str, ind: S_str.get(ind)


@overload_method(SeriesStrMethodType, 'extract', inline='always',
    no_unliteral=True)
def overload_str_method_extract(S_str, pat, flags=0, expand=True):
    if not is_overload_constant_bool(expand):
        raise BodoError(
            "Series.str.extract(): 'expand' argument should be a constant bool"
            )
    qvz__oqe, regex = _get_column_names_from_regex(pat, flags, 'extract')
    stdlq__wkyn = len(qvz__oqe)
    lopbu__oxoh = 'def impl(S_str, pat, flags=0, expand=True):\n'
    lopbu__oxoh += '  regex = re.compile(pat, flags=flags)\n'
    lopbu__oxoh += '  S = S_str._obj\n'
    lopbu__oxoh += (
        '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    lopbu__oxoh += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    lopbu__oxoh += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    lopbu__oxoh += '  numba.parfors.parfor.init_prange()\n'
    lopbu__oxoh += '  n = len(str_arr)\n'
    for i in range(stdlq__wkyn):
        lopbu__oxoh += (
            '  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)\n'
            .format(i))
    lopbu__oxoh += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    lopbu__oxoh += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
    for i in range(stdlq__wkyn):
        lopbu__oxoh += "          out_arr_{}[j] = ''\n".format(i)
        lopbu__oxoh += (
            '          bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
            format(i))
    lopbu__oxoh += '      else:\n'
    lopbu__oxoh += '          m = regex.search(str_arr[j])\n'
    lopbu__oxoh += '          if m:\n'
    lopbu__oxoh += '            g = m.groups()\n'
    for i in range(stdlq__wkyn):
        lopbu__oxoh += '            out_arr_{0}[j] = g[{0}]\n'.format(i)
    lopbu__oxoh += '          else:\n'
    for i in range(stdlq__wkyn):
        lopbu__oxoh += "            out_arr_{}[j] = ''\n".format(i)
        lopbu__oxoh += (
            '            bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
            format(i))
    if is_overload_false(expand) and regex.groups == 1:
        boazj__oguly = "'{}'".format(list(regex.groupindex.keys()).pop()
            ) if len(regex.groupindex.keys()) > 0 else 'name'
        lopbu__oxoh += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr_0, index, {})\n'
            .format(boazj__oguly))
        zou__lpygg = {}
        exec(lopbu__oxoh, {'re': re, 'bodo': bodo, 'numba': numba,
            'get_utf8_size': get_utf8_size}, zou__lpygg)
        impl = zou__lpygg['impl']
        return impl
    zqe__yxeyc = ', '.join('out_arr_{}'.format(i) for i in range(stdlq__wkyn))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(lopbu__oxoh, qvz__oqe,
        zqe__yxeyc, 'index', extra_globals={'get_utf8_size': get_utf8_size,
        're': re})
    return impl


@overload_method(SeriesStrMethodType, 'extractall', inline='always',
    no_unliteral=True)
def overload_str_method_extractall(S_str, pat, flags=0):
    qvz__oqe, bwss__khykw = _get_column_names_from_regex(pat, flags,
        'extractall')
    stdlq__wkyn = len(qvz__oqe)
    giy__jcud = isinstance(S_str.stype.index, StringIndexType)
    lopbu__oxoh = 'def impl(S_str, pat, flags=0):\n'
    lopbu__oxoh += '  regex = re.compile(pat, flags=flags)\n'
    lopbu__oxoh += '  S = S_str._obj\n'
    lopbu__oxoh += (
        '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    lopbu__oxoh += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    lopbu__oxoh += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    lopbu__oxoh += (
        '  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    lopbu__oxoh += (
        '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n')
    lopbu__oxoh += '  numba.parfors.parfor.init_prange()\n'
    lopbu__oxoh += '  n = len(str_arr)\n'
    lopbu__oxoh += '  out_n_l = [0]\n'
    for i in range(stdlq__wkyn):
        lopbu__oxoh += '  num_chars_{} = 0\n'.format(i)
    if giy__jcud:
        lopbu__oxoh += '  index_num_chars = 0\n'
    lopbu__oxoh += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    if giy__jcud:
        lopbu__oxoh += '      index_num_chars += get_utf8_size(index_arr[i])\n'
    lopbu__oxoh += '      if bodo.libs.array_kernels.isna(str_arr, i):\n'
    lopbu__oxoh += '          continue\n'
    lopbu__oxoh += '      m = regex.findall(str_arr[i])\n'
    lopbu__oxoh += '      out_n_l[0] += len(m)\n'
    for i in range(stdlq__wkyn):
        lopbu__oxoh += '      l_{} = 0\n'.format(i)
    lopbu__oxoh += '      for s in m:\n'
    for i in range(stdlq__wkyn):
        lopbu__oxoh += '        l_{} += get_utf8_size(s{})\n'.format(i, 
            '[{}]'.format(i) if stdlq__wkyn > 1 else '')
    for i in range(stdlq__wkyn):
        lopbu__oxoh += '      num_chars_{0} += l_{0}\n'.format(i)
    lopbu__oxoh += (
        '  out_n = bodo.libs.distributed_api.local_alloc_size(out_n_l[0], str_arr)\n'
        )
    for i in range(stdlq__wkyn):
        lopbu__oxoh += (
            """  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, num_chars_{0})
"""
            .format(i))
    if giy__jcud:
        lopbu__oxoh += """  out_ind_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, index_num_chars)
"""
    else:
        lopbu__oxoh += '  out_ind_arr = np.empty(out_n, index_arr.dtype)\n'
    lopbu__oxoh += '  out_match_arr = np.empty(out_n, np.int64)\n'
    lopbu__oxoh += '  out_ind = 0\n'
    lopbu__oxoh += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    lopbu__oxoh += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
    lopbu__oxoh += '          continue\n'
    lopbu__oxoh += '      m = regex.findall(str_arr[j])\n'
    lopbu__oxoh += '      for k, s in enumerate(m):\n'
    for i in range(stdlq__wkyn):
        lopbu__oxoh += (
            """        bodo.libs.distributed_api.set_arr_local(out_arr_{}, out_ind, s{})
"""
            .format(i, '[{}]'.format(i) if stdlq__wkyn > 1 else ''))
    lopbu__oxoh += """        bodo.libs.distributed_api.set_arr_local(out_ind_arr, out_ind, index_arr[j])
"""
    lopbu__oxoh += (
        '        bodo.libs.distributed_api.set_arr_local(out_match_arr, out_ind, k)\n'
        )
    lopbu__oxoh += '        out_ind += 1\n'
    lopbu__oxoh += (
        '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n')
    lopbu__oxoh += "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n"
    zqe__yxeyc = ', '.join('out_arr_{}'.format(i) for i in range(stdlq__wkyn))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(lopbu__oxoh, qvz__oqe,
        zqe__yxeyc, 'out_index', extra_globals={'get_utf8_size':
        get_utf8_size, 're': re})
    return impl


def _get_column_names_from_regex(pat, flags, func_name):
    if not is_overload_constant_str(pat):
        raise BodoError(
            "Series.str.{}(): 'pat' argument should be a constant string".
            format(func_name))
    if not is_overload_constant_int(flags):
        raise BodoError(
            "Series.str.{}(): 'flags' argument should be a constant int".
            format(func_name))
    pat = get_overload_const_str(pat)
    flags = get_overload_const_int(flags)
    regex = re.compile(pat, flags=flags)
    if regex.groups == 0:
        raise BodoError(
            'Series.str.{}(): pattern {} contains no capture groups'.format
            (func_name, pat))
    umoad__ihnyx = dict(zip(regex.groupindex.values(), regex.groupindex.keys())
        )
    qvz__oqe = [umoad__ihnyx.get(1 + i, i) for i in range(regex.groups)]
    return qvz__oqe, regex


def create_str2str_methods_overload(func_name):
    if func_name in ['lstrip', 'rstrip', 'strip']:
        lopbu__oxoh = 'def f(S_str, to_strip=None):\n'
    else:
        lopbu__oxoh = 'def f(S_str):\n'
    lopbu__oxoh += '    S = S_str._obj\n'
    lopbu__oxoh += (
        '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    lopbu__oxoh += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    lopbu__oxoh += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    lopbu__oxoh += '    numba.parfors.parfor.init_prange()\n'
    lopbu__oxoh += '    n = len(str_arr)\n'
    if func_name in ('capitalize', 'lower', 'swapcase', 'title', 'upper'):
        lopbu__oxoh += '    num_chars = num_total_chars(str_arr)\n'
    else:
        lopbu__oxoh += '    num_chars = -1\n'
    lopbu__oxoh += (
        '    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, num_chars)\n'
        )
    lopbu__oxoh += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    lopbu__oxoh += '        if bodo.libs.array_kernels.isna(str_arr, j):\n'
    lopbu__oxoh += '            out_arr[j] = ""\n'
    lopbu__oxoh += '            bodo.libs.array_kernels.setna(out_arr, j)\n'
    lopbu__oxoh += '        else:\n'
    if func_name in ['lstrip', 'rstrip', 'strip']:
        lopbu__oxoh += ('            out_arr[j] = str_arr[j].{}(to_strip)\n'
            .format(func_name))
    else:
        lopbu__oxoh += '            out_arr[j] = str_arr[j].{}()\n'.format(
            func_name)
    lopbu__oxoh += (
        '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    zou__lpygg = {}
    exec(lopbu__oxoh, {'bodo': bodo, 'numba': numba, 'num_total_chars':
        bodo.libs.str_arr_ext.num_total_chars, 'get_utf8_size': bodo.libs.
        str_arr_ext.get_utf8_size}, zou__lpygg)
    tgdfx__opm = zou__lpygg['f']
    if func_name in ['lstrip', 'rstrip', 'strip']:

        def overload_strip_method(S_str, to_strip=None):
            if not is_overload_none(to_strip):
                str_arg_check(func_name, 'to_strip', to_strip)
            return tgdfx__opm
        return overload_strip_method
    else:

        def overload_str2str_methods(S_str):
            return tgdfx__opm
        return overload_str2str_methods


def create_str2bool_methods_overload(func_name):

    def overload_str2bool_methods(S_str):
        lopbu__oxoh = 'def f(S_str):\n'
        lopbu__oxoh += '    S = S_str._obj\n'
        lopbu__oxoh += (
            '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        lopbu__oxoh += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        lopbu__oxoh += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        lopbu__oxoh += '    numba.parfors.parfor.init_prange()\n'
        lopbu__oxoh += '    l = len(str_arr)\n'
        lopbu__oxoh += (
            '    out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n')
        lopbu__oxoh += (
            '    for i in numba.parfors.parfor.internal_prange(l):\n')
        lopbu__oxoh += '        if bodo.libs.array_kernels.isna(str_arr, i):\n'
        lopbu__oxoh += (
            '            bodo.libs.array_kernels.setna(out_arr, i)\n')
        lopbu__oxoh += '        else:\n'
        lopbu__oxoh += ('            out_arr[i] = np.bool_(str_arr[i].{}())\n'
            .format(func_name))
        lopbu__oxoh += '    return bodo.hiframes.pd_series_ext.init_series(\n'
        lopbu__oxoh += '      out_arr,index, name)\n'
        zou__lpygg = {}
        exec(lopbu__oxoh, {'bodo': bodo, 'numba': numba, 'np': np}, zou__lpygg)
        tgdfx__opm = zou__lpygg['f']
        return tgdfx__opm
    return overload_str2bool_methods


def _install_str2str_methods():
    for jwp__pceoa in bodo.hiframes.pd_series_ext.str2str_methods:
        abd__qiez = create_str2str_methods_overload(jwp__pceoa)
        overload_method(SeriesStrMethodType, jwp__pceoa, inline='always',
            no_unliteral=True)(abd__qiez)


def _install_str2bool_methods():
    for jwp__pceoa in bodo.hiframes.pd_series_ext.str2bool_methods:
        abd__qiez = create_str2bool_methods_overload(jwp__pceoa)
        overload_method(SeriesStrMethodType, jwp__pceoa, inline='always',
            no_unliteral=True)(abd__qiez)


_install_str2str_methods()
_install_str2bool_methods()


@overload_attribute(SeriesType, 'cat')
def overload_series_cat(s):
    if not isinstance(s.dtype, bodo.hiframes.pd_categorical_ext.
        PDCategoricalDtype):
        raise BodoError('Can only use .cat accessor with categorical values.')
    return lambda s: bodo.hiframes.series_str_impl.init_series_cat_method(s)


class SeriesCatMethodType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        boazj__oguly = 'SeriesCatMethodType({})'.format(stype)
        super(SeriesCatMethodType, self).__init__(boazj__oguly)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SeriesCatMethodType)
class SeriesCatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        zcfvg__doaeu = [('obj', fe_type.stype)]
        super(SeriesCatModel, self).__init__(dmm, fe_type, zcfvg__doaeu)


make_attribute_wrapper(SeriesCatMethodType, 'obj', '_obj')


@intrinsic
def init_series_cat_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        xfyik__gkxzn, = args
        kmtw__kof = signature.return_type
        asc__yvu = cgutils.create_struct_proxy(kmtw__kof)(context, builder)
        asc__yvu.obj = xfyik__gkxzn
        context.nrt.incref(builder, signature.args[0], xfyik__gkxzn)
        return asc__yvu._getvalue()
    return SeriesCatMethodType(obj)(obj), codegen


@overload_attribute(SeriesCatMethodType, 'codes')
def series_cat_codes_overload(S_dt):

    def impl(S_dt):
        S = S_dt._obj
        wgulj__tdb = bodo.hiframes.pd_series_ext.get_series_data(S)
        rlcoy__kvykc = bodo.hiframes.pd_series_ext.get_series_index(S)
        boazj__oguly = None
        return bodo.hiframes.pd_series_ext.init_series(bodo.hiframes.
            pd_categorical_ext.get_categorical_arr_codes(wgulj__tdb),
            rlcoy__kvykc, boazj__oguly)
    return impl


unsupported_cat_attrs = {'categories', 'ordered'}
unsupported_cat_methods = {'rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered'}


def _install_catseries_unsupported():
    for pnl__rgf in unsupported_cat_attrs:
        bytin__plhll = 'Series.cat.' + pnl__rgf
        overload_attribute(SeriesCatMethodType, pnl__rgf)(
            create_unsupported_overload(bytin__plhll))
    for twlml__kfgj in unsupported_cat_methods:
        bytin__plhll = 'Series.cat.' + twlml__kfgj
        overload_method(SeriesCatMethodType, twlml__kfgj)(
            create_unsupported_overload(bytin__plhll))


_install_catseries_unsupported()
unsupported_str_methods = {'casefold', 'cat', 'decode', 'encode', 'findall',
    'fullmatch', 'index', 'match', 'normalize', 'partition', 'rindex',
    'rpartition', 'slice_replace', 'rsplit', 'translate', 'wrap', 'get_dummies'
    }


def _install_strseries_unsupported():
    for twlml__kfgj in unsupported_str_methods:
        bytin__plhll = 'Series.str.' + twlml__kfgj
        overload_method(SeriesStrMethodType, twlml__kfgj)(
            create_unsupported_overload(bytin__plhll))


_install_strseries_unsupported()
