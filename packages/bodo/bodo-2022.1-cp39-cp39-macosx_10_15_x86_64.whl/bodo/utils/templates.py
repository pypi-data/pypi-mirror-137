"""
Helper functions and classes to simplify Template Generation
for Bodo classes.
"""
import numba
from numba.core.typing.templates import AttributeTemplate


class OverloadedKeyAttributeTemplate(AttributeTemplate):
    _attr_set = None

    def _is_existing_attr(self, attr_name):
        if self._attr_set is None:
            who__pvat = set()
            zgkfm__tszpu = list(self.context._get_attribute_templates(self.key)
                )
            qogby__ztl = zgkfm__tszpu.index(self) + 1
            for hgqok__oufcd in range(qogby__ztl, len(zgkfm__tszpu)):
                if isinstance(zgkfm__tszpu[hgqok__oufcd], numba.core.typing
                    .templates._OverloadAttributeTemplate):
                    who__pvat.add(zgkfm__tszpu[hgqok__oufcd]._attr)
            self._attr_set = who__pvat
        return attr_name in self._attr_set
