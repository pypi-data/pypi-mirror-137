"""
Analysis and transformation for HDF5 support.
"""
import types as pytypes
import numba
from numba.core import ir, types
from numba.core.ir_utils import compile_to_numba_ir, find_callname, find_const, get_definition, guard, replace_arg_nodes, require
import bodo
import bodo.io
from bodo.utils.transform import get_const_value_inner


class H5_IO:

    def __init__(self, func_ir, _locals, flags, arg_types):
        self.func_ir = func_ir
        self.locals = _locals
        self.flags = flags
        self.arg_types = arg_types

    def handle_possible_h5_read(self, assign, lhs, rhs):
        txhr__znd = self._get_h5_type(lhs, rhs)
        if txhr__znd is not None:
            ovn__yll = str(txhr__znd.dtype)
            ixzhv__reyx = 'def _h5_read_impl(dset, index):\n'
            ixzhv__reyx += (
                "  arr = bodo.io.h5_api.h5_read_dummy(dset, {}, '{}', index)\n"
                .format(txhr__znd.ndim, ovn__yll))
            uvfi__mmtcz = {}
            exec(ixzhv__reyx, {}, uvfi__mmtcz)
            udhwa__xse = uvfi__mmtcz['_h5_read_impl']
            iti__bagz = compile_to_numba_ir(udhwa__xse, {'bodo': bodo}
                ).blocks.popitem()[1]
            kjada__nhohd = rhs.index if rhs.op == 'getitem' else rhs.index_var
            replace_arg_nodes(iti__bagz, [rhs.value, kjada__nhohd])
            yjjp__troa = iti__bagz.body[:-3]
            yjjp__troa[-1].target = assign.target
            return yjjp__troa
        return None

    def _get_h5_type(self, lhs, rhs):
        txhr__znd = self._get_h5_type_locals(lhs)
        if txhr__znd is not None:
            return txhr__znd
        return guard(self._infer_h5_typ, rhs)

    def _infer_h5_typ(self, rhs):
        require(rhs.op in ('getitem', 'static_getitem'))
        kjada__nhohd = rhs.index if rhs.op == 'getitem' else rhs.index_var
        tod__syor = guard(find_const, self.func_ir, kjada__nhohd)
        require(not isinstance(tod__syor, str))
        val_def = rhs
        obj_name_list = []
        while True:
            val_def = get_definition(self.func_ir, val_def.value)
            require(isinstance(val_def, ir.Expr))
            if val_def.op == 'call':
                return self._get_h5_type_file(val_def, obj_name_list)
            require(val_def.op in ('getitem', 'static_getitem'))
            twu__miyeg = (val_def.index if val_def.op == 'getitem' else
                val_def.index_var)
            jmju__yzrw = get_const_value_inner(self.func_ir, twu__miyeg,
                arg_types=self.arg_types)
            obj_name_list.append(jmju__yzrw)

    def _get_h5_type_file(self, val_def, obj_name_list):
        require(len(obj_name_list) > 0)
        require(find_callname(self.func_ir, val_def) == ('File', 'h5py'))
        require(len(val_def.args) > 0)
        mivf__ydp = get_const_value_inner(self.func_ir, val_def.args[0],
            arg_types=self.arg_types)
        obj_name_list.reverse()
        import h5py
        pbgr__bcsbf = h5py.File(mivf__ydp, 'r')
        lzptm__lqw = pbgr__bcsbf
        for jmju__yzrw in obj_name_list:
            lzptm__lqw = lzptm__lqw[jmju__yzrw]
        require(isinstance(lzptm__lqw, h5py.Dataset))
        aza__rpws = len(lzptm__lqw.shape)
        zcr__lirl = numba.np.numpy_support.from_dtype(lzptm__lqw.dtype)
        pbgr__bcsbf.close()
        return types.Array(zcr__lirl, aza__rpws, 'C')

    def _get_h5_type_locals(self, varname):
        ohq__fjk = self.locals.pop(varname, None)
        if ohq__fjk is None and varname is not None:
            ohq__fjk = self.flags.h5_types.get(varname, None)
        return ohq__fjk
