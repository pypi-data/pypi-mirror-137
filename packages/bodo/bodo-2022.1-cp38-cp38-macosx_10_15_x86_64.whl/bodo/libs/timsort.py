import numpy as np
import pandas as pd
import numba
from numba.extending import overload
from bodo.utils.utils import alloc_arr_tup
MIN_MERGE = 32


@numba.njit(no_cpython_wrapper=True, cache=True)
def sort(key_arrs, lo, hi, data):
    pwfe__kdn = hi - lo
    if pwfe__kdn < 2:
        return
    if pwfe__kdn < MIN_MERGE:
        qvp__kot = countRunAndMakeAscending(key_arrs, lo, hi, data)
        binarySort(key_arrs, lo, hi, lo + qvp__kot, data)
        return
    stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop = (
        init_sort_start(key_arrs, data))
    xpd__zvay = minRunLength(pwfe__kdn)
    while True:
        jqyo__njcgw = countRunAndMakeAscending(key_arrs, lo, hi, data)
        if jqyo__njcgw < xpd__zvay:
            ieuae__dvolr = pwfe__kdn if pwfe__kdn <= xpd__zvay else xpd__zvay
            binarySort(key_arrs, lo, lo + ieuae__dvolr, lo + jqyo__njcgw, data)
            jqyo__njcgw = ieuae__dvolr
        stackSize = pushRun(stackSize, runBase, runLen, lo, jqyo__njcgw)
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeCollapse(
            stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
            tmp_data, minGallop)
        lo += jqyo__njcgw
        pwfe__kdn -= jqyo__njcgw
        if pwfe__kdn == 0:
            break
    assert lo == hi
    stackSize, tmpLength, tmp, tmp_data, minGallop = mergeForceCollapse(
        stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
        tmp_data, minGallop)
    assert stackSize == 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def binarySort(key_arrs, lo, hi, start, data):
    assert lo <= start and start <= hi
    if start == lo:
        start += 1
    while start < hi:
        twpp__vffzt = getitem_arr_tup(key_arrs, start)
        ucn__wwjzh = getitem_arr_tup(data, start)
        hcfa__zdgli = lo
        lqh__phmi = start
        assert hcfa__zdgli <= lqh__phmi
        while hcfa__zdgli < lqh__phmi:
            ohs__zyg = hcfa__zdgli + lqh__phmi >> 1
            if twpp__vffzt < getitem_arr_tup(key_arrs, ohs__zyg):
                lqh__phmi = ohs__zyg
            else:
                hcfa__zdgli = ohs__zyg + 1
        assert hcfa__zdgli == lqh__phmi
        n = start - hcfa__zdgli
        copyRange_tup(key_arrs, hcfa__zdgli, key_arrs, hcfa__zdgli + 1, n)
        copyRange_tup(data, hcfa__zdgli, data, hcfa__zdgli + 1, n)
        setitem_arr_tup(key_arrs, hcfa__zdgli, twpp__vffzt)
        setitem_arr_tup(data, hcfa__zdgli, ucn__wwjzh)
        start += 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def countRunAndMakeAscending(key_arrs, lo, hi, data):
    assert lo < hi
    rkx__tior = lo + 1
    if rkx__tior == hi:
        return 1
    if getitem_arr_tup(key_arrs, rkx__tior) < getitem_arr_tup(key_arrs, lo):
        rkx__tior += 1
        while rkx__tior < hi and getitem_arr_tup(key_arrs, rkx__tior
            ) < getitem_arr_tup(key_arrs, rkx__tior - 1):
            rkx__tior += 1
        reverseRange(key_arrs, lo, rkx__tior, data)
    else:
        rkx__tior += 1
        while rkx__tior < hi and getitem_arr_tup(key_arrs, rkx__tior
            ) >= getitem_arr_tup(key_arrs, rkx__tior - 1):
            rkx__tior += 1
    return rkx__tior - lo


@numba.njit(no_cpython_wrapper=True, cache=True)
def reverseRange(key_arrs, lo, hi, data):
    hi -= 1
    while lo < hi:
        swap_arrs(key_arrs, lo, hi)
        swap_arrs(data, lo, hi)
        lo += 1
        hi -= 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def minRunLength(n):
    assert n >= 0
    qeyvi__loeef = 0
    while n >= MIN_MERGE:
        qeyvi__loeef |= n & 1
        n >>= 1
    return n + qeyvi__loeef


MIN_GALLOP = 7
INITIAL_TMP_STORAGE_LENGTH = 256


@numba.njit(no_cpython_wrapper=True, cache=True)
def init_sort_start(key_arrs, data):
    minGallop = MIN_GALLOP
    gmv__htoz = len(key_arrs[0])
    tmpLength = (gmv__htoz >> 1 if gmv__htoz < 2 *
        INITIAL_TMP_STORAGE_LENGTH else INITIAL_TMP_STORAGE_LENGTH)
    tmp = alloc_arr_tup(tmpLength, key_arrs)
    tmp_data = alloc_arr_tup(tmpLength, data)
    stackSize = 0
    tqdy__xsfw = (5 if gmv__htoz < 120 else 10 if gmv__htoz < 1542 else 19 if
        gmv__htoz < 119151 else 40)
    runBase = np.empty(tqdy__xsfw, np.int64)
    runLen = np.empty(tqdy__xsfw, np.int64)
    return stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def pushRun(stackSize, runBase, runLen, runBase_val, runLen_val):
    runBase[stackSize] = runBase_val
    runLen[stackSize] = runLen_val
    stackSize += 1
    return stackSize


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeCollapse(stackSize, runBase, runLen, key_arrs, data, tmpLength,
    tmp, tmp_data, minGallop):
    while stackSize > 1:
        n = stackSize - 2
        if n >= 1 and runLen[n - 1] <= runLen[n] + runLen[n + 1
            ] or n >= 2 and runLen[n - 2] <= runLen[n] + runLen[n - 1]:
            if runLen[n - 1] < runLen[n + 1]:
                n -= 1
        elif runLen[n] > runLen[n + 1]:
            break
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeAt(stackSize,
            runBase, runLen, key_arrs, data, tmpLength, tmp, tmp_data,
            minGallop, n)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeForceCollapse(stackSize, runBase, runLen, key_arrs, data,
    tmpLength, tmp, tmp_data, minGallop):
    while stackSize > 1:
        n = stackSize - 2
        if n > 0 and runLen[n - 1] < runLen[n + 1]:
            n -= 1
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeAt(stackSize,
            runBase, runLen, key_arrs, data, tmpLength, tmp, tmp_data,
            minGallop, n)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeAt(stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
    tmp_data, minGallop, i):
    assert stackSize >= 2
    assert i >= 0
    assert i == stackSize - 2 or i == stackSize - 3
    base1 = runBase[i]
    len1 = runLen[i]
    base2 = runBase[i + 1]
    len2 = runLen[i + 1]
    assert len1 > 0 and len2 > 0
    assert base1 + len1 == base2
    runLen[i] = len1 + len2
    if i == stackSize - 3:
        runBase[i + 1] = runBase[i + 2]
        runLen[i + 1] = runLen[i + 2]
    stackSize -= 1
    jvmqi__cihw = gallopRight(getitem_arr_tup(key_arrs, base2), key_arrs,
        base1, len1, 0)
    assert jvmqi__cihw >= 0
    base1 += jvmqi__cihw
    len1 -= jvmqi__cihw
    if len1 == 0:
        return stackSize, tmpLength, tmp, tmp_data, minGallop
    len2 = gallopLeft(getitem_arr_tup(key_arrs, base1 + len1 - 1), key_arrs,
        base2, len2, len2 - 1)
    assert len2 >= 0
    if len2 == 0:
        return stackSize, tmpLength, tmp, tmp_data, minGallop
    if len1 <= len2:
        tmpLength, tmp, tmp_data = ensureCapacity(tmpLength, tmp, tmp_data,
            key_arrs, data, len1)
        minGallop = mergeLo(key_arrs, data, tmp, tmp_data, minGallop, base1,
            len1, base2, len2)
    else:
        tmpLength, tmp, tmp_data = ensureCapacity(tmpLength, tmp, tmp_data,
            key_arrs, data, len2)
        minGallop = mergeHi(key_arrs, data, tmp, tmp_data, minGallop, base1,
            len1, base2, len2)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopLeft(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    cgut__ena = 0
    pxyz__eduwc = 1
    if key > getitem_arr_tup(arr, base + hint):
        ort__nvd = _len - hint
        while pxyz__eduwc < ort__nvd and key > getitem_arr_tup(arr, base +
            hint + pxyz__eduwc):
            cgut__ena = pxyz__eduwc
            pxyz__eduwc = (pxyz__eduwc << 1) + 1
            if pxyz__eduwc <= 0:
                pxyz__eduwc = ort__nvd
        if pxyz__eduwc > ort__nvd:
            pxyz__eduwc = ort__nvd
        cgut__ena += hint
        pxyz__eduwc += hint
    else:
        ort__nvd = hint + 1
        while pxyz__eduwc < ort__nvd and key <= getitem_arr_tup(arr, base +
            hint - pxyz__eduwc):
            cgut__ena = pxyz__eduwc
            pxyz__eduwc = (pxyz__eduwc << 1) + 1
            if pxyz__eduwc <= 0:
                pxyz__eduwc = ort__nvd
        if pxyz__eduwc > ort__nvd:
            pxyz__eduwc = ort__nvd
        tmp = cgut__ena
        cgut__ena = hint - pxyz__eduwc
        pxyz__eduwc = hint - tmp
    assert -1 <= cgut__ena and cgut__ena < pxyz__eduwc and pxyz__eduwc <= _len
    cgut__ena += 1
    while cgut__ena < pxyz__eduwc:
        ymcld__jvcji = cgut__ena + (pxyz__eduwc - cgut__ena >> 1)
        if key > getitem_arr_tup(arr, base + ymcld__jvcji):
            cgut__ena = ymcld__jvcji + 1
        else:
            pxyz__eduwc = ymcld__jvcji
    assert cgut__ena == pxyz__eduwc
    return pxyz__eduwc


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopRight(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    pxyz__eduwc = 1
    cgut__ena = 0
    if key < getitem_arr_tup(arr, base + hint):
        ort__nvd = hint + 1
        while pxyz__eduwc < ort__nvd and key < getitem_arr_tup(arr, base +
            hint - pxyz__eduwc):
            cgut__ena = pxyz__eduwc
            pxyz__eduwc = (pxyz__eduwc << 1) + 1
            if pxyz__eduwc <= 0:
                pxyz__eduwc = ort__nvd
        if pxyz__eduwc > ort__nvd:
            pxyz__eduwc = ort__nvd
        tmp = cgut__ena
        cgut__ena = hint - pxyz__eduwc
        pxyz__eduwc = hint - tmp
    else:
        ort__nvd = _len - hint
        while pxyz__eduwc < ort__nvd and key >= getitem_arr_tup(arr, base +
            hint + pxyz__eduwc):
            cgut__ena = pxyz__eduwc
            pxyz__eduwc = (pxyz__eduwc << 1) + 1
            if pxyz__eduwc <= 0:
                pxyz__eduwc = ort__nvd
        if pxyz__eduwc > ort__nvd:
            pxyz__eduwc = ort__nvd
        cgut__ena += hint
        pxyz__eduwc += hint
    assert -1 <= cgut__ena and cgut__ena < pxyz__eduwc and pxyz__eduwc <= _len
    cgut__ena += 1
    while cgut__ena < pxyz__eduwc:
        ymcld__jvcji = cgut__ena + (pxyz__eduwc - cgut__ena >> 1)
        if key < getitem_arr_tup(arr, base + ymcld__jvcji):
            pxyz__eduwc = ymcld__jvcji
        else:
            cgut__ena = ymcld__jvcji + 1
    assert cgut__ena == pxyz__eduwc
    return pxyz__eduwc


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeLo(key_arrs, data, tmp, tmp_data, minGallop, base1, len1, base2, len2
    ):
    assert len1 > 0 and len2 > 0 and base1 + len1 == base2
    arr = key_arrs
    arr_data = data
    copyRange_tup(arr, base1, tmp, 0, len1)
    copyRange_tup(arr_data, base1, tmp_data, 0, len1)
    cursor1 = 0
    cursor2 = base2
    dest = base1
    setitem_arr_tup(arr, dest, getitem_arr_tup(arr, cursor2))
    copyElement_tup(arr_data, cursor2, arr_data, dest)
    cursor2 += 1
    dest += 1
    len2 -= 1
    if len2 == 0:
        copyRange_tup(tmp, cursor1, arr, dest, len1)
        copyRange_tup(tmp_data, cursor1, arr_data, dest, len1)
        return minGallop
    if len1 == 1:
        copyRange_tup(arr, cursor2, arr, dest, len2)
        copyRange_tup(arr_data, cursor2, arr_data, dest, len2)
        copyElement_tup(tmp, cursor1, arr, dest + len2)
        copyElement_tup(tmp_data, cursor1, arr_data, dest + len2)
        return minGallop
    len1, len2, cursor1, cursor2, dest, minGallop = mergeLo_inner(key_arrs,
        data, tmp_data, len1, len2, tmp, cursor1, cursor2, dest, minGallop)
    minGallop = 1 if minGallop < 1 else minGallop
    if len1 == 1:
        assert len2 > 0
        copyRange_tup(arr, cursor2, arr, dest, len2)
        copyRange_tup(arr_data, cursor2, arr_data, dest, len2)
        copyElement_tup(tmp, cursor1, arr, dest + len2)
        copyElement_tup(tmp_data, cursor1, arr_data, dest + len2)
    elif len1 == 0:
        raise ValueError('Comparison method violates its general contract!')
    else:
        assert len2 == 0
        assert len1 > 1
        copyRange_tup(tmp, cursor1, arr, dest, len1)
        copyRange_tup(tmp_data, cursor1, arr_data, dest, len1)
    return minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeLo_inner(arr, arr_data, tmp_data, len1, len2, tmp, cursor1,
    cursor2, dest, minGallop):
    while True:
        gje__zkywb = 0
        sko__wsai = 0
        while True:
            assert len1 > 1 and len2 > 0
            if getitem_arr_tup(arr, cursor2) < getitem_arr_tup(tmp, cursor1):
                copyElement_tup(arr, cursor2, arr, dest)
                copyElement_tup(arr_data, cursor2, arr_data, dest)
                cursor2 += 1
                dest += 1
                sko__wsai += 1
                gje__zkywb = 0
                len2 -= 1
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor1, arr, dest)
                copyElement_tup(tmp_data, cursor1, arr_data, dest)
                cursor1 += 1
                dest += 1
                gje__zkywb += 1
                sko__wsai = 0
                len1 -= 1
                if len1 == 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            if not gje__zkywb | sko__wsai < minGallop:
                break
        while True:
            assert len1 > 1 and len2 > 0
            gje__zkywb = gallopRight(getitem_arr_tup(arr, cursor2), tmp,
                cursor1, len1, 0)
            if gje__zkywb != 0:
                copyRange_tup(tmp, cursor1, arr, dest, gje__zkywb)
                copyRange_tup(tmp_data, cursor1, arr_data, dest, gje__zkywb)
                dest += gje__zkywb
                cursor1 += gje__zkywb
                len1 -= gje__zkywb
                if len1 <= 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor2, arr, dest)
            copyElement_tup(arr_data, cursor2, arr_data, dest)
            cursor2 += 1
            dest += 1
            len2 -= 1
            if len2 == 0:
                return len1, len2, cursor1, cursor2, dest, minGallop
            sko__wsai = gallopLeft(getitem_arr_tup(tmp, cursor1), arr,
                cursor2, len2, 0)
            if sko__wsai != 0:
                copyRange_tup(arr, cursor2, arr, dest, sko__wsai)
                copyRange_tup(arr_data, cursor2, arr_data, dest, sko__wsai)
                dest += sko__wsai
                cursor2 += sko__wsai
                len2 -= sko__wsai
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor1, arr, dest)
            copyElement_tup(tmp_data, cursor1, arr_data, dest)
            cursor1 += 1
            dest += 1
            len1 -= 1
            if len1 == 1:
                return len1, len2, cursor1, cursor2, dest, minGallop
            minGallop -= 1
            if not gje__zkywb >= MIN_GALLOP | sko__wsai >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeHi(key_arrs, data, tmp, tmp_data, minGallop, base1, len1, base2, len2
    ):
    assert len1 > 0 and len2 > 0 and base1 + len1 == base2
    arr = key_arrs
    arr_data = data
    copyRange_tup(arr, base2, tmp, 0, len2)
    copyRange_tup(arr_data, base2, tmp_data, 0, len2)
    cursor1 = base1 + len1 - 1
    cursor2 = len2 - 1
    dest = base2 + len2 - 1
    copyElement_tup(arr, cursor1, arr, dest)
    copyElement_tup(arr_data, cursor1, arr_data, dest)
    cursor1 -= 1
    dest -= 1
    len1 -= 1
    if len1 == 0:
        copyRange_tup(tmp, 0, arr, dest - (len2 - 1), len2)
        copyRange_tup(tmp_data, 0, arr_data, dest - (len2 - 1), len2)
        return minGallop
    if len2 == 1:
        dest -= len1
        cursor1 -= len1
        copyRange_tup(arr, cursor1 + 1, arr, dest + 1, len1)
        copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1, len1)
        copyElement_tup(tmp, cursor2, arr, dest)
        copyElement_tup(tmp_data, cursor2, arr_data, dest)
        return minGallop
    len1, len2, tmp, cursor1, cursor2, dest, minGallop = mergeHi_inner(key_arrs
        , data, tmp_data, base1, len1, len2, tmp, cursor1, cursor2, dest,
        minGallop)
    minGallop = 1 if minGallop < 1 else minGallop
    if len2 == 1:
        assert len1 > 0
        dest -= len1
        cursor1 -= len1
        copyRange_tup(arr, cursor1 + 1, arr, dest + 1, len1)
        copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1, len1)
        copyElement_tup(tmp, cursor2, arr, dest)
        copyElement_tup(tmp_data, cursor2, arr_data, dest)
    elif len2 == 0:
        raise ValueError('Comparison method violates its general contract!')
    else:
        assert len1 == 0
        assert len2 > 0
        copyRange_tup(tmp, 0, arr, dest - (len2 - 1), len2)
        copyRange_tup(tmp_data, 0, arr_data, dest - (len2 - 1), len2)
    return minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeHi_inner(arr, arr_data, tmp_data, base1, len1, len2, tmp, cursor1,
    cursor2, dest, minGallop):
    while True:
        gje__zkywb = 0
        sko__wsai = 0
        while True:
            assert len1 > 0 and len2 > 1
            if getitem_arr_tup(tmp, cursor2) < getitem_arr_tup(arr, cursor1):
                copyElement_tup(arr, cursor1, arr, dest)
                copyElement_tup(arr_data, cursor1, arr_data, dest)
                cursor1 -= 1
                dest -= 1
                gje__zkywb += 1
                sko__wsai = 0
                len1 -= 1
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor2, arr, dest)
                copyElement_tup(tmp_data, cursor2, arr_data, dest)
                cursor2 -= 1
                dest -= 1
                sko__wsai += 1
                gje__zkywb = 0
                len2 -= 1
                if len2 == 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            if not gje__zkywb | sko__wsai < minGallop:
                break
        while True:
            assert len1 > 0 and len2 > 1
            gje__zkywb = len1 - gallopRight(getitem_arr_tup(tmp, cursor2),
                arr, base1, len1, len1 - 1)
            if gje__zkywb != 0:
                dest -= gje__zkywb
                cursor1 -= gje__zkywb
                len1 -= gje__zkywb
                copyRange_tup(arr, cursor1 + 1, arr, dest + 1, gje__zkywb)
                copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1,
                    gje__zkywb)
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor2, arr, dest)
            copyElement_tup(tmp_data, cursor2, arr_data, dest)
            cursor2 -= 1
            dest -= 1
            len2 -= 1
            if len2 == 1:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            sko__wsai = len2 - gallopLeft(getitem_arr_tup(arr, cursor1),
                tmp, 0, len2, len2 - 1)
            if sko__wsai != 0:
                dest -= sko__wsai
                cursor2 -= sko__wsai
                len2 -= sko__wsai
                copyRange_tup(tmp, cursor2 + 1, arr, dest + 1, sko__wsai)
                copyRange_tup(tmp_data, cursor2 + 1, arr_data, dest + 1,
                    sko__wsai)
                if len2 <= 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor1, arr, dest)
            copyElement_tup(arr_data, cursor1, arr_data, dest)
            cursor1 -= 1
            dest -= 1
            len1 -= 1
            if len1 == 0:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            minGallop -= 1
            if not gje__zkywb >= MIN_GALLOP | sko__wsai >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, tmp, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def ensureCapacity(tmpLength, tmp, tmp_data, key_arrs, data, minCapacity):
    trnv__yolf = len(key_arrs[0])
    if tmpLength < minCapacity:
        xnk__ovsre = minCapacity
        xnk__ovsre |= xnk__ovsre >> 1
        xnk__ovsre |= xnk__ovsre >> 2
        xnk__ovsre |= xnk__ovsre >> 4
        xnk__ovsre |= xnk__ovsre >> 8
        xnk__ovsre |= xnk__ovsre >> 16
        xnk__ovsre += 1
        if xnk__ovsre < 0:
            xnk__ovsre = minCapacity
        else:
            xnk__ovsre = min(xnk__ovsre, trnv__yolf >> 1)
        tmp = alloc_arr_tup(xnk__ovsre, key_arrs)
        tmp_data = alloc_arr_tup(xnk__ovsre, data)
        tmpLength = xnk__ovsre
    return tmpLength, tmp, tmp_data


def swap_arrs(data, lo, hi):
    for arr in data:
        xekid__agucc = arr[lo]
        arr[lo] = arr[hi]
        arr[hi] = xekid__agucc


@overload(swap_arrs, no_unliteral=True)
def swap_arrs_overload(arr_tup, lo, hi):
    rwc__gjkvk = arr_tup.count
    rcvhv__tho = 'def f(arr_tup, lo, hi):\n'
    for i in range(rwc__gjkvk):
        rcvhv__tho += '  tmp_v_{} = arr_tup[{}][lo]\n'.format(i, i)
        rcvhv__tho += '  arr_tup[{}][lo] = arr_tup[{}][hi]\n'.format(i, i)
        rcvhv__tho += '  arr_tup[{}][hi] = tmp_v_{}\n'.format(i, i)
    rcvhv__tho += '  return\n'
    zejc__cuku = {}
    exec(rcvhv__tho, {}, zejc__cuku)
    kfmkw__jmnm = zejc__cuku['f']
    return kfmkw__jmnm


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyRange(src_arr, src_pos, dst_arr, dst_pos, n):
    dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


def copyRange_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


@overload(copyRange_tup, no_unliteral=True)
def copyRange_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    rwc__gjkvk = src_arr_tup.count
    assert rwc__gjkvk == dst_arr_tup.count
    rcvhv__tho = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):\n'
    for i in range(rwc__gjkvk):
        rcvhv__tho += (
            '  copyRange(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos, n)\n'
            .format(i, i))
    rcvhv__tho += '  return\n'
    zejc__cuku = {}
    exec(rcvhv__tho, {'copyRange': copyRange}, zejc__cuku)
    gmwb__qcxn = zejc__cuku['f']
    return gmwb__qcxn


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyElement(src_arr, src_pos, dst_arr, dst_pos):
    dst_arr[dst_pos] = src_arr[src_pos]


def copyElement_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos] = src_arr[src_pos]


@overload(copyElement_tup, no_unliteral=True)
def copyElement_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    rwc__gjkvk = src_arr_tup.count
    assert rwc__gjkvk == dst_arr_tup.count
    rcvhv__tho = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos):\n'
    for i in range(rwc__gjkvk):
        rcvhv__tho += (
            '  copyElement(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos)\n'
            .format(i, i))
    rcvhv__tho += '  return\n'
    zejc__cuku = {}
    exec(rcvhv__tho, {'copyElement': copyElement}, zejc__cuku)
    gmwb__qcxn = zejc__cuku['f']
    return gmwb__qcxn


def getitem_arr_tup(arr_tup, ind):
    ndmbo__jbocx = [arr[ind] for arr in arr_tup]
    return tuple(ndmbo__jbocx)


@overload(getitem_arr_tup, no_unliteral=True)
def getitem_arr_tup_overload(arr_tup, ind):
    rwc__gjkvk = arr_tup.count
    rcvhv__tho = 'def f(arr_tup, ind):\n'
    rcvhv__tho += '  return ({}{})\n'.format(','.join(['arr_tup[{}][ind]'.
        format(i) for i in range(rwc__gjkvk)]), ',' if rwc__gjkvk == 1 else '')
    zejc__cuku = {}
    exec(rcvhv__tho, {}, zejc__cuku)
    ptw__wpk = zejc__cuku['f']
    return ptw__wpk


def setitem_arr_tup(arr_tup, ind, val_tup):
    for arr, hhal__zzbh in zip(arr_tup, val_tup):
        arr[ind] = hhal__zzbh


@overload(setitem_arr_tup, no_unliteral=True)
def setitem_arr_tup_overload(arr_tup, ind, val_tup):
    rwc__gjkvk = arr_tup.count
    rcvhv__tho = 'def f(arr_tup, ind, val_tup):\n'
    for i in range(rwc__gjkvk):
        if isinstance(val_tup, numba.core.types.BaseTuple):
            rcvhv__tho += '  arr_tup[{}][ind] = val_tup[{}]\n'.format(i, i)
        else:
            assert arr_tup.count == 1
            rcvhv__tho += '  arr_tup[{}][ind] = val_tup\n'.format(i)
    rcvhv__tho += '  return\n'
    zejc__cuku = {}
    exec(rcvhv__tho, {}, zejc__cuku)
    ptw__wpk = zejc__cuku['f']
    return ptw__wpk


def test():
    import time
    pse__ntqf = time.time()
    zvhm__htdwb = np.ones(3)
    data = np.arange(3), np.ones(3)
    sort((zvhm__htdwb,), 0, 3, data)
    print('compile time', time.time() - pse__ntqf)
    n = 210000
    np.random.seed(2)
    data = np.arange(n), np.random.ranf(n)
    kwhf__sud = np.random.ranf(n)
    cxkl__tavd = pd.DataFrame({'A': kwhf__sud, 'B': data[0], 'C': data[1]})
    pse__ntqf = time.time()
    amrxg__dlhqj = cxkl__tavd.sort_values('A', inplace=False)
    ubv__mfs = time.time()
    sort((kwhf__sud,), 0, n, data)
    print('Bodo', time.time() - ubv__mfs, 'Numpy', ubv__mfs - pse__ntqf)
    np.testing.assert_almost_equal(data[0], amrxg__dlhqj.B.values)
    np.testing.assert_almost_equal(data[1], amrxg__dlhqj.C.values)


if __name__ == '__main__':
    test()
