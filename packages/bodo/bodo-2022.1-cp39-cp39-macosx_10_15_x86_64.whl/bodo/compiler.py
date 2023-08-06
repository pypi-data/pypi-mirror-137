"""
Defines Bodo's compiler pipeline.
"""
import os
import warnings
from collections import namedtuple
import numba
from numba.core import ir, ir_utils
from numba.core.compiler import DefaultPassBuilder
from numba.core.compiler_machinery import AnalysisPass, FunctionPass, register_pass
from numba.core.inline_closurecall import inline_closure_call
from numba.core.ir_utils import build_definitions, find_callname, get_definition, guard
from numba.core.registry import CPUDispatcher
from numba.core.typed_passes import DumpParforDiagnostics, InlineOverloads, IRLegalization, NopythonTypeInference, ParforPass, PreParforPass
from numba.core.untyped_passes import MakeFunctionToJitFunction, ReconstructSSA, WithLifting
import bodo
import bodo.libs
import bodo.libs.array_kernels
import bodo.libs.int_arr_ext
import bodo.libs.re_ext
import bodo.libs.spark_extra
import bodo.transforms
import bodo.transforms.series_pass
import bodo.transforms.untyped_pass
from bodo.transforms.series_pass import SeriesPass
from bodo.transforms.table_column_del_pass import TableColumnDelPass
from bodo.transforms.typing_pass import BodoTypeInference
from bodo.transforms.untyped_pass import UntypedPass
from bodo.utils.utils import is_assign, is_call_assign, is_expr
_is_sklearn_supported_version = False
_max_sklearn_version = 0, 24, 2
_max_sklearn_ver_str = '.'.join(str(x) for x in _max_sklearn_version)
try:
    import re
    import sklearn
    import bodo.libs.sklearn_ext
    regex = re.compile('(\\d+)\\.(\\d+)\\..*(\\d+)')
    sklearn_version = sklearn.__version__
    m = regex.match(sklearn_version)
    if m:
        ver = tuple(map(int, m.groups()))
        if ver <= _max_sklearn_version:
            _is_sklearn_supported_version = True
except ImportError as joyba__cgtw:
    pass
_matplotlib_installed = False
try:
    import matplotlib
    import bodo.libs.matplotlib_ext
    _matplotlib_installed = True
except ImportError as joyba__cgtw:
    pass
_pyspark_installed = False
try:
    import pyspark
    import pyspark.sql.functions
    import bodo.libs.pyspark_ext
    bodo.utils.transform.no_side_effect_call_tuples.update({('col', pyspark
        .sql.functions), (pyspark.sql.functions.col,), ('sum', pyspark.sql.
        functions), (pyspark.sql.functions.sum,)})
    _pyspark_installed = True
except ImportError as joyba__cgtw:
    pass
import bodo.hiframes.dataframe_indexing
import bodo.hiframes.datetime_datetime_ext
import bodo.hiframes.datetime_timedelta_ext
try:
    import xgboost
    import bodo.libs.xgb_ext
except ImportError as joyba__cgtw:
    pass
import bodo.io
import bodo.utils
import bodo.utils.typing
if bodo.utils.utils.has_supported_h5py():
    from bodo.io import h5
numba.core.config.DISABLE_PERFORMANCE_WARNINGS = 1
from numba.core.errors import NumbaExperimentalFeatureWarning, NumbaPendingDeprecationWarning
warnings.simplefilter('ignore', category=NumbaExperimentalFeatureWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)
inline_all_calls = False


class BodoCompiler(numba.core.compiler.CompilerBase):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=True,
            inline_calls_pass=inline_all_calls)

    def _create_bodo_pipeline(self, distributed=True, inline_calls_pass=
        False, udf_pipeline=False):
        yku__akcl = 'bodo' if distributed else 'bodo_seq'
        yku__akcl = yku__akcl + '_inline' if inline_calls_pass else yku__akcl
        pm = DefaultPassBuilder.define_nopython_pipeline(self.state, yku__akcl)
        if inline_calls_pass:
            pm.add_pass_after(InlinePass, WithLifting)
        if udf_pipeline:
            pm.add_pass_after(ConvertCallsUDFPass, WithLifting)
        add_pass_before(pm, BodoUntypedPass, ReconstructSSA)
        replace_pass(pm, BodoTypeInference, NopythonTypeInference)
        remove_pass(pm, MakeFunctionToJitFunction)
        add_pass_before(pm, BodoSeriesPass, PreParforPass)
        if distributed:
            pm.add_pass_after(BodoDistributedPass, ParforPass)
        else:
            pm.add_pass_after(LowerParforSeq, ParforPass)
            pm.add_pass_after(LowerBodoIRExtSeq, LowerParforSeq)
        add_pass_before(pm, BodoTableColumnDelPass, IRLegalization)
        pm.add_pass_after(BodoDumpDistDiagnosticsPass, DumpParforDiagnostics)
        pm.finalize()
        return [pm]


def add_pass_before(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for qge__qxc, (x, vggcn__dzg) in enumerate(pm.passes):
        if x == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.insert(qge__qxc, (pass_cls, str(pass_cls)))
    pm._finalized = False


def replace_pass(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for qge__qxc, (x, vggcn__dzg) in enumerate(pm.passes):
        if x == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes[qge__qxc] = pass_cls, str(pass_cls)
    pm._finalized = False


def remove_pass(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for qge__qxc, (x, vggcn__dzg) in enumerate(pm.passes):
        if x == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.pop(qge__qxc)
    pm._finalized = False


@register_pass(mutates_CFG=True, analysis_only=False)
class InlinePass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        inline_calls(state.func_ir, state.locals)
        state.func_ir.blocks = ir_utils.simplify_CFG(state.func_ir.blocks)
        return True


def _convert_bodo_dispatcher_to_udf(rhs, func_ir):
    mhrsf__osu = guard(get_definition, func_ir, rhs.func)
    if isinstance(mhrsf__osu, (ir.Global, ir.FreeVar, ir.Const)):
        loa__ptb = mhrsf__osu.value
    else:
        mexn__jywi = guard(find_callname, func_ir, rhs)
        if not (mexn__jywi and isinstance(mexn__jywi[0], str) and
            isinstance(mexn__jywi[1], str)):
            return
        func_name, func_mod = mexn__jywi
        try:
            import importlib
            npm__cgshr = importlib.import_module(func_mod)
            loa__ptb = getattr(npm__cgshr, func_name)
        except:
            return
    if isinstance(loa__ptb, CPUDispatcher) and issubclass(loa__ptb.
        _compiler.pipeline_class, BodoCompiler
        ) and loa__ptb._compiler.pipeline_class != BodoCompilerUDF:
        loa__ptb._compiler.pipeline_class = BodoCompilerUDF


@register_pass(mutates_CFG=True, analysis_only=False)
class ConvertCallsUDFPass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        for block in state.func_ir.blocks.values():
            for fht__pcml in block.body:
                if is_call_assign(fht__pcml):
                    _convert_bodo_dispatcher_to_udf(fht__pcml.value, state.
                        func_ir)
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoUntypedPass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        xxrjv__hbply = UntypedPass(state.func_ir, state.typingctx, state.
            args, state.locals, state.metadata, state.flags)
        xxrjv__hbply.run()
        return True


def _update_definitions(func_ir, node_list):
    tnlbl__ppozk = ir.Loc('', 0)
    vetc__jubt = ir.Block(ir.Scope(None, tnlbl__ppozk), tnlbl__ppozk)
    vetc__jubt.body = node_list
    build_definitions({(0): vetc__jubt}, func_ir._definitions)


_series_inline_attrs = {'values', 'shape', 'size', 'empty', 'name', 'index',
    'dtype'}
_series_no_inline_methods = {'to_list', 'tolist', 'rolling', 'to_csv',
    'count', 'fillna', 'to_dict', 'map', 'apply', 'pipe', 'combine',
    'bfill', 'ffill', 'pad', 'backfill'}
_series_method_alias = {'isnull': 'isna', 'product': 'prod', 'kurtosis':
    'kurt', 'is_monotonic': 'is_monotonic_increasing', 'notnull': 'notna'}
_dataframe_no_inline_methods = {'apply', 'itertuples', 'pipe', 'to_parquet',
    'to_sql', 'to_csv', 'to_json', 'assign', 'to_string', 'query', 'rolling'}
TypingInfo = namedtuple('TypingInfo', ['typingctx', 'targetctx', 'typemap',
    'calltypes', 'curr_loc'])


def _inline_bodo_getattr(stmt, rhs, rhs_type, new_body, func_ir, typingctx,
    targetctx, typemap, calltypes):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.utils.transform import compile_func_single_block
    if isinstance(rhs_type, SeriesType) and rhs.attr in _series_inline_attrs:
        ghdtd__sbyuj = 'overload_series_' + rhs.attr
        ohxa__pfpli = getattr(bodo.hiframes.series_impl, ghdtd__sbyuj)
    if isinstance(rhs_type, DataFrameType) and rhs.attr in ('index', 'columns'
        ):
        ghdtd__sbyuj = 'overload_dataframe_' + rhs.attr
        ohxa__pfpli = getattr(bodo.hiframes.dataframe_impl, ghdtd__sbyuj)
    else:
        return False
    func_ir._definitions[stmt.target.name].remove(rhs)
    rfuq__hmo = ohxa__pfpli(rhs_type)
    wutt__ond = TypingInfo(typingctx, targetctx, typemap, calltypes, stmt.loc)
    yhky__isthr = compile_func_single_block(rfuq__hmo, (rhs.value,), stmt.
        target, wutt__ond)
    _update_definitions(func_ir, yhky__isthr)
    new_body += yhky__isthr
    return True


def _inline_bodo_call(rhs, i, func_mod, func_name, pass_info, new_body,
    block, typingctx, targetctx, calltypes, work_list):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.utils.transform import replace_func, update_locs
    func_ir = pass_info.func_ir
    typemap = pass_info.typemap
    if isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        SeriesType) and func_name not in _series_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        if (func_name in bodo.hiframes.series_impl.explicit_binop_funcs or 
            func_name.startswith('r') and func_name[1:] in bodo.hiframes.
            series_impl.explicit_binop_funcs):
            return False
        rhs.args.insert(0, func_mod)
        ppnnw__acti = tuple(typemap[jfojr__jmkoy.name] for jfojr__jmkoy in
            rhs.args)
        ocf__rtn = {yku__akcl: typemap[jfojr__jmkoy.name] for yku__akcl,
            jfojr__jmkoy in dict(rhs.kws).items()}
        rfuq__hmo = getattr(bodo.hiframes.series_impl, 'overload_series_' +
            func_name)(*ppnnw__acti, **ocf__rtn)
    elif isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        DataFrameType) and func_name not in _dataframe_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        rhs.args.insert(0, func_mod)
        ppnnw__acti = tuple(typemap[jfojr__jmkoy.name] for jfojr__jmkoy in
            rhs.args)
        ocf__rtn = {yku__akcl: typemap[jfojr__jmkoy.name] for yku__akcl,
            jfojr__jmkoy in dict(rhs.kws).items()}
        rfuq__hmo = getattr(bodo.hiframes.dataframe_impl, 
            'overload_dataframe_' + func_name)(*ppnnw__acti, **ocf__rtn)
    else:
        return False
    ydnqh__vxpqm = replace_func(pass_info, rfuq__hmo, rhs.args, pysig=numba
        .core.utils.pysignature(rfuq__hmo), kws=dict(rhs.kws))
    block.body = new_body + block.body[i:]
    gkev__vni, vggcn__dzg = inline_closure_call(func_ir, ydnqh__vxpqm.glbls,
        block, len(new_body), ydnqh__vxpqm.func, typingctx=typingctx,
        targetctx=targetctx, arg_typs=ydnqh__vxpqm.arg_types, typemap=
        typemap, calltypes=calltypes, work_list=work_list)
    for aqbet__tbv in gkev__vni.values():
        aqbet__tbv.loc = rhs.loc
        update_locs(aqbet__tbv.body, rhs.loc)
    return True


def bodo_overload_inline_pass(func_ir, typingctx, targetctx, typemap, calltypes
    ):
    rcx__vbw = namedtuple('PassInfo', ['func_ir', 'typemap'])
    pass_info = rcx__vbw(func_ir, typemap)
    hujbj__sors = func_ir.blocks
    work_list = list((nfsg__lcpto, hujbj__sors[nfsg__lcpto]) for
        nfsg__lcpto in reversed(hujbj__sors.keys()))
    while work_list:
        ghhh__lojq, block = work_list.pop()
        new_body = []
        eoif__mfgk = False
        for i, stmt in enumerate(block.body):
            if is_assign(stmt) and is_expr(stmt.value, 'getattr'):
                rhs = stmt.value
                rhs_type = typemap[rhs.value.name]
                if _inline_bodo_getattr(stmt, rhs, rhs_type, new_body,
                    func_ir, typingctx, targetctx, typemap, calltypes):
                    continue
            if is_call_assign(stmt):
                rhs = stmt.value
                mexn__jywi = guard(find_callname, func_ir, rhs, typemap)
                if mexn__jywi is None:
                    new_body.append(stmt)
                    continue
                func_name, func_mod = mexn__jywi
                if _inline_bodo_call(rhs, i, func_mod, func_name, pass_info,
                    new_body, block, typingctx, targetctx, calltypes, work_list
                    ):
                    eoif__mfgk = True
                    break
            new_body.append(stmt)
        if not eoif__mfgk:
            hujbj__sors[ghhh__lojq].body = new_body
    func_ir.blocks = ir_utils.simplify_CFG(func_ir.blocks)


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoDistributedPass(FunctionPass):
    _name = 'bodo_distributed_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        from bodo.transforms.distributed_pass import DistributedPass
        kqbdk__ghu = DistributedPass(state.func_ir, state.typingctx, state.
            targetctx, state.type_annotation.typemap, state.type_annotation
            .calltypes, state.return_type, state.metadata, state.flags)
        state.return_type = kqbdk__ghu.run()
        state.type_annotation.blocks = state.func_ir.blocks
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoSeriesPass(FunctionPass):
    _name = 'bodo_series_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        vqx__zal = SeriesPass(state.func_ir, state.typingctx, state.
            targetctx, state.type_annotation.typemap, state.type_annotation
            .calltypes, state.locals)
        vqx__zal.run()
        vqx__zal.run()
        vqx__zal.run()
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoDumpDistDiagnosticsPass(AnalysisPass):
    _name = 'bodo_dump_diagnostics_pass'

    def __init__(self):
        AnalysisPass.__init__(self)

    def run_pass(self, state):
        obihh__tzcel = 0
        ctgp__bpapr = 'BODO_DISTRIBUTED_DIAGNOSTICS'
        try:
            obihh__tzcel = int(os.environ[ctgp__bpapr])
        except:
            pass
        if obihh__tzcel > 0 and 'distributed_diagnostics' in state.metadata:
            state.metadata['distributed_diagnostics'].dump(obihh__tzcel,
                state.metadata)
        return True


class BodoCompilerSeq(BodoCompiler):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=False,
            inline_calls_pass=inline_all_calls)


class BodoCompilerUDF(BodoCompiler):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=False, udf_pipeline=True)


@register_pass(mutates_CFG=False, analysis_only=True)
class LowerParforSeq(FunctionPass):
    _name = 'bodo_lower_parfor_seq_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        bodo.transforms.distributed_pass.lower_parfor_sequential(state.
            typingctx, state.func_ir, state.typemap, state.calltypes, state
            .metadata)
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class LowerBodoIRExtSeq(FunctionPass):
    _name = 'bodo_lower_ir_ext_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        from bodo.transforms.distributed_pass import distributed_run_extensions
        from bodo.transforms.table_column_del_pass import remove_dead_table_columns
        state.func_ir._definitions = build_definitions(state.func_ir.blocks)
        wutt__ond = TypingInfo(state.typingctx, state.targetctx, state.
            typemap, state.calltypes, state.func_ir.loc)
        remove_dead_table_columns(state.func_ir, state.typemap, wutt__ond)
        for block in state.func_ir.blocks.values():
            new_body = []
            for fht__pcml in block.body:
                if type(fht__pcml) in distributed_run_extensions:
                    lahf__kdvcm = distributed_run_extensions[type(fht__pcml)]
                    xvb__emsq = lahf__kdvcm(fht__pcml, None, state.typemap,
                        state.calltypes, state.typingctx, state.targetctx)
                    new_body += xvb__emsq
                elif is_call_assign(fht__pcml):
                    rhs = fht__pcml.value
                    mexn__jywi = guard(find_callname, state.func_ir, rhs)
                    if mexn__jywi == ('gatherv', 'bodo') or mexn__jywi == (
                        'allgatherv', 'bodo'):
                        fht__pcml.value = rhs.args[0]
                    new_body.append(fht__pcml)
                else:
                    new_body.append(fht__pcml)
            block.body = new_body
        state.type_annotation.blocks = state.func_ir.blocks
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoTableColumnDelPass(AnalysisPass):
    _name = 'bodo_table_column_del_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        okdb__ghce = TableColumnDelPass(state.func_ir, state.typingctx,
            state.targetctx, state.type_annotation.typemap, state.
            type_annotation.calltypes)
        return okdb__ghce.run()


def inline_calls(func_ir, _locals, work_list=None, typingctx=None,
    targetctx=None, typemap=None, calltypes=None):
    if work_list is None:
        work_list = list(func_ir.blocks.items())
    oxj__hwg = set()
    while work_list:
        ghhh__lojq, block = work_list.pop()
        oxj__hwg.add(ghhh__lojq)
        for i, inajx__iheeq in enumerate(block.body):
            if isinstance(inajx__iheeq, ir.Assign):
                rrwgq__losv = inajx__iheeq.value
                if isinstance(rrwgq__losv, ir.Expr
                    ) and rrwgq__losv.op == 'call':
                    mhrsf__osu = guard(get_definition, func_ir, rrwgq__losv
                        .func)
                    if isinstance(mhrsf__osu, (ir.Global, ir.FreeVar)
                        ) and isinstance(mhrsf__osu.value, CPUDispatcher
                        ) and issubclass(mhrsf__osu.value._compiler.
                        pipeline_class, BodoCompiler):
                        gfr__hgz = mhrsf__osu.value.py_func
                        arg_types = None
                        if typingctx:
                            nye__mir = dict(rrwgq__losv.kws)
                            znae__dbehs = tuple(typemap[jfojr__jmkoy.name] for
                                jfojr__jmkoy in rrwgq__losv.args)
                            zvzr__xep = {osiwd__qlxtn: typemap[jfojr__jmkoy
                                .name] for osiwd__qlxtn, jfojr__jmkoy in
                                nye__mir.items()}
                            vggcn__dzg, arg_types = (mhrsf__osu.value.
                                fold_argument_types(znae__dbehs, zvzr__xep))
                        vggcn__dzg, tpl__yqshm = inline_closure_call(func_ir,
                            gfr__hgz.__globals__, block, i, gfr__hgz,
                            typingctx=typingctx, targetctx=targetctx,
                            arg_typs=arg_types, typemap=typemap, calltypes=
                            calltypes, work_list=work_list)
                        _locals.update((tpl__yqshm[osiwd__qlxtn].name,
                            jfojr__jmkoy) for osiwd__qlxtn, jfojr__jmkoy in
                            mhrsf__osu.value.locals.items() if osiwd__qlxtn in
                            tpl__yqshm)
                        break
    return oxj__hwg


def udf_jit(signature_or_function=None, **options):
    vtmw__iovb = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    return numba.njit(signature_or_function, parallel=vtmw__iovb,
        pipeline_class=bodo.compiler.BodoCompilerUDF, **options)


def is_udf_call(func_type):
    return isinstance(func_type, numba.core.types.Dispatcher
        ) and func_type.dispatcher._compiler.pipeline_class == BodoCompilerUDF


def is_user_dispatcher(func_type):
    return isinstance(func_type, numba.core.types.functions.ObjModeDispatcher
        ) or isinstance(func_type, numba.core.types.Dispatcher) and issubclass(
        func_type.dispatcher._compiler.pipeline_class, BodoCompiler)


@register_pass(mutates_CFG=False, analysis_only=True)
class DummyCR(FunctionPass):
    _name = 'bodo_dummy_cr'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        state.cr = (state.func_ir, state.typemap, state.calltypes, state.
            return_type)
        return True


def remove_passes_after(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for qge__qxc, (x, vggcn__dzg) in enumerate(pm.passes):
        if x == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes = pm.passes[:qge__qxc + 1]
    pm._finalized = False


class TyperCompiler(BodoCompiler):

    def define_pipelines(self):
        [pm] = self._create_bodo_pipeline()
        remove_passes_after(pm, InlineOverloads)
        pm.add_pass_after(DummyCR, InlineOverloads)
        pm.finalize()
        return [pm]


def get_func_type_info(func, arg_types, kw_types):
    typingctx = numba.core.registry.cpu_target.typing_context
    targetctx = numba.core.registry.cpu_target.target_context
    brp__rrs = None
    lhnvu__vemoi = None
    _locals = {}
    thr__qcj = numba.core.utils.pysignature(func)
    args = bodo.utils.transform.fold_argument_types(thr__qcj, arg_types,
        kw_types)
    vuxw__errs = numba.core.compiler.Flags()
    dcd__kkjsj = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    uibq__auo = {'nopython': True, 'boundscheck': False, 'parallel': dcd__kkjsj
        }
    numba.core.registry.cpu_target.options.parse_as_flags(vuxw__errs, uibq__auo
        )
    nst__itq = TyperCompiler(typingctx, targetctx, brp__rrs, args,
        lhnvu__vemoi, vuxw__errs, _locals)
    return nst__itq.compile_extra(func)
