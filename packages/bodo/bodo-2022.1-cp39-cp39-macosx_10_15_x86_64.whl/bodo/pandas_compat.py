import hashlib
import inspect
import pandas as pd
_check_pandas_change = False


def _set_noconvert_columns(self):
    assert self.orig_names is not None
    wpzg__vem = {nhg__jzk: uzcuc__wegk for uzcuc__wegk, nhg__jzk in
        enumerate(self.orig_names)}
    sryz__cpxp = [wpzg__vem[nhg__jzk] for nhg__jzk in self.names]
    eppme__fsfbv = self._set_noconvert_dtype_columns(sryz__cpxp, self.names)
    for outa__wxb in eppme__fsfbv:
        self._reader.set_noconvert(outa__wxb)


if _check_pandas_change:
    lines = inspect.getsource(pd.io.parsers.c_parser_wrapper.CParserWrapper
        ._set_noconvert_columns)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'afc2d738f194e3976cf05d61cb16dc4224b0139451f08a1cf49c578af6f975d3':
        warnings.warn(
            'pd.io.parsers.c_parser_wrapper.CParserWrapper._set_noconvert_columns has changed'
            )
pd.io.parsers.c_parser_wrapper.CParserWrapper._set_noconvert_columns = (
    _set_noconvert_columns)
