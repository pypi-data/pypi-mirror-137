"""
Numba monkey patches to fix issues related to Bodo. Should be imported before any
other module in bodo package.
"""
import copy
import functools
import hashlib
import inspect
import itertools
import operator
import os
import re
import sys
import textwrap
import traceback
import types as pytypes
import warnings
from collections import OrderedDict
from collections.abc import Sequence
from contextlib import ExitStack
import numba
import numba.core.boxing
import numba.core.inline_closurecall
import numba.np.linalg
from numba.core import analysis, cgutils, errors, ir, ir_utils, types
from numba.core.compiler import Compiler
from numba.core.errors import ForceLiteralArg, LiteralTypingError, TypingError
from numba.core.ir_utils import GuardException, _create_function_from_code_obj, analysis, build_definitions, find_callname, guard, has_no_side_effect, mk_unique_var, remove_dead_extensions, replace_vars_inner, require, visit_vars_extensions, visit_vars_inner
from numba.core.types import literal
from numba.core.types.functions import _bt_as_lines, _ResolutionFailures, _termcolor, _unlit_non_poison
from numba.core.typing.templates import AbstractTemplate, Signature, _EmptyImplementationEntry, _inline_info, _OverloadAttributeTemplate, infer_global, signature
from numba.core.typing.typeof import Purpose, typeof
from numba.experimental.jitclass import base as jitclass_base
from numba.experimental.jitclass import decorators as jitclass_decorators
from numba.extending import NativeValue, lower_builtin, typeof_impl
from numba.parfors.parfor import get_expr_args
from bodo.utils.typing import BodoError
_check_numba_change = False
numba.core.typing.templates._IntrinsicTemplate.prefer_literal = True


def run_frontend(func, inline_closures=False, emit_dels=False):
    xof__whb = numba.core.bytecode.FunctionIdentity.from_function(func)
    avsnp__pfhoe = numba.core.interpreter.Interpreter(xof__whb)
    nou__abgq = numba.core.bytecode.ByteCode(func_id=xof__whb)
    func_ir = avsnp__pfhoe.interpret(nou__abgq)
    if inline_closures:
        from numba.core.inline_closurecall import InlineClosureCallPass


        class DummyPipeline:

            def __init__(self, f_ir):
                self.state = numba.core.compiler.StateDict()
                self.state.typingctx = None
                self.state.targetctx = None
                self.state.args = None
                self.state.func_ir = f_ir
                self.state.typemap = None
                self.state.return_type = None
                self.state.calltypes = None
        numba.core.rewrites.rewrite_registry.apply('before-inference',
            DummyPipeline(func_ir).state)
        slgi__exl = InlineClosureCallPass(func_ir, numba.core.cpu.
            ParallelOptions(False), {}, False)
        slgi__exl.run()
    xegw__ntvo = numba.core.postproc.PostProcessor(func_ir)
    xegw__ntvo.run(emit_dels)
    return func_ir


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.run_frontend)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8c2477a793b2c08d56430997880974ac12c5570e69c9e54d37d694b322ea18b6':
        warnings.warn('numba.core.compiler.run_frontend has changed')
numba.core.compiler.run_frontend = run_frontend


def visit_vars_stmt(stmt, callback, cbdata):
    for t, ndcg__dtxx in visit_vars_extensions.items():
        if isinstance(stmt, t):
            ndcg__dtxx(stmt, callback, cbdata)
            return
    if isinstance(stmt, ir.Assign):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Arg):
        stmt.name = visit_vars_inner(stmt.name, callback, cbdata)
    elif isinstance(stmt, ir.Return):
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Raise):
        stmt.exception = visit_vars_inner(stmt.exception, callback, cbdata)
    elif isinstance(stmt, ir.Branch):
        stmt.cond = visit_vars_inner(stmt.cond, callback, cbdata)
    elif isinstance(stmt, ir.Jump):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
    elif isinstance(stmt, ir.Del):
        var = ir.Var(None, stmt.value, stmt.loc)
        var = visit_vars_inner(var, callback, cbdata)
        stmt.value = var.name
    elif isinstance(stmt, ir.DelAttr):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.attr = visit_vars_inner(stmt.attr, callback, cbdata)
    elif isinstance(stmt, ir.SetAttr):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.attr = visit_vars_inner(stmt.attr, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.DelItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index = visit_vars_inner(stmt.index, callback, cbdata)
    elif isinstance(stmt, ir.StaticSetItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index_var = visit_vars_inner(stmt.index_var, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.SetItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index = visit_vars_inner(stmt.index, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Print):
        stmt.args = [visit_vars_inner(x, callback, cbdata) for x in stmt.args]
        stmt.vararg = visit_vars_inner(stmt.vararg, callback, cbdata)
    else:
        pass
    return


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.visit_vars_stmt)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '52b7b645ba65c35f3cf564f936e113261db16a2dff1e80fbee2459af58844117':
        warnings.warn('numba.core.ir_utils.visit_vars_stmt has changed')
numba.core.ir_utils.visit_vars_stmt = visit_vars_stmt
old_run_pass = numba.core.typed_passes.InlineOverloads.run_pass


def InlineOverloads_run_pass(self, state):
    import bodo
    bodo.compiler.bodo_overload_inline_pass(state.func_ir, state.typingctx,
        state.targetctx, state.typemap, state.calltypes)
    return old_run_pass(self, state)


numba.core.typed_passes.InlineOverloads.run_pass = InlineOverloads_run_pass
from numba.core.ir_utils import _add_alias, alias_analysis_extensions, alias_func_extensions
_immutable_type_class = (types.Number, types.scalars._NPDatetimeBase, types
    .iterators.RangeType, types.UnicodeType)


def is_immutable_type(var, typemap):
    if typemap is None or var not in typemap:
        return False
    typ = typemap[var]
    if isinstance(typ, _immutable_type_class):
        return True
    if isinstance(typ, types.BaseTuple) and all(isinstance(t,
        _immutable_type_class) for t in typ.types):
        return True
    return False


def find_potential_aliases(blocks, args, typemap, func_ir, alias_map=None,
    arg_aliases=None):
    if alias_map is None:
        alias_map = {}
    if arg_aliases is None:
        arg_aliases = set(a for a in args if not is_immutable_type(a, typemap))
    func_ir._definitions = build_definitions(func_ir.blocks)
    sdowt__ykjjw = ['ravel', 'transpose', 'reshape']
    for qkmu__lhzrp in blocks.values():
        for bmbou__kyq in qkmu__lhzrp.body:
            if type(bmbou__kyq) in alias_analysis_extensions:
                ndcg__dtxx = alias_analysis_extensions[type(bmbou__kyq)]
                ndcg__dtxx(bmbou__kyq, args, typemap, func_ir, alias_map,
                    arg_aliases)
            if isinstance(bmbou__kyq, ir.Assign):
                ltsko__koq = bmbou__kyq.value
                icj__rycwz = bmbou__kyq.target.name
                if is_immutable_type(icj__rycwz, typemap):
                    continue
                if isinstance(ltsko__koq, ir.Var
                    ) and icj__rycwz != ltsko__koq.name:
                    _add_alias(icj__rycwz, ltsko__koq.name, alias_map,
                        arg_aliases)
                if isinstance(ltsko__koq, ir.Expr) and (ltsko__koq.op ==
                    'cast' or ltsko__koq.op in ['getitem', 'static_getitem']):
                    _add_alias(icj__rycwz, ltsko__koq.value.name, alias_map,
                        arg_aliases)
                if isinstance(ltsko__koq, ir.Expr
                    ) and ltsko__koq.op == 'inplace_binop':
                    _add_alias(icj__rycwz, ltsko__koq.lhs.name, alias_map,
                        arg_aliases)
                if isinstance(ltsko__koq, ir.Expr
                    ) and ltsko__koq.op == 'getattr' and ltsko__koq.attr in [
                    'T', 'ctypes', 'flat']:
                    _add_alias(icj__rycwz, ltsko__koq.value.name, alias_map,
                        arg_aliases)
                if isinstance(ltsko__koq, ir.Expr
                    ) and ltsko__koq.op == 'getattr' and ltsko__koq.attr not in [
                    'shape'] and ltsko__koq.value.name in arg_aliases:
                    _add_alias(icj__rycwz, ltsko__koq.value.name, alias_map,
                        arg_aliases)
                if isinstance(ltsko__koq, ir.Expr
                    ) and ltsko__koq.op == 'getattr' and ltsko__koq.attr in (
                    'loc', 'iloc', 'iat', '_obj', 'obj', 'codes', '_df'):
                    _add_alias(icj__rycwz, ltsko__koq.value.name, alias_map,
                        arg_aliases)
                if isinstance(ltsko__koq, ir.Expr) and ltsko__koq.op in (
                    'build_tuple', 'build_list', 'build_set'
                    ) and not is_immutable_type(icj__rycwz, typemap):
                    for rgjli__jydsh in ltsko__koq.items:
                        _add_alias(icj__rycwz, rgjli__jydsh.name, alias_map,
                            arg_aliases)
                if isinstance(ltsko__koq, ir.Expr) and ltsko__koq.op == 'call':
                    srq__awykq = guard(find_callname, func_ir, ltsko__koq,
                        typemap)
                    if srq__awykq is None:
                        continue
                    rreaj__atj, yagjs__eiyq = srq__awykq
                    if srq__awykq in alias_func_extensions:
                        ohrn__eyk = alias_func_extensions[srq__awykq]
                        ohrn__eyk(icj__rycwz, ltsko__koq.args, alias_map,
                            arg_aliases)
                    if yagjs__eiyq == 'numpy' and rreaj__atj in sdowt__ykjjw:
                        _add_alias(icj__rycwz, ltsko__koq.args[0].name,
                            alias_map, arg_aliases)
                    if isinstance(yagjs__eiyq, ir.Var
                        ) and rreaj__atj in sdowt__ykjjw:
                        _add_alias(icj__rycwz, yagjs__eiyq.name, alias_map,
                            arg_aliases)
    cdc__hhxs = copy.deepcopy(alias_map)
    for rgjli__jydsh in cdc__hhxs:
        for gzen__yoan in cdc__hhxs[rgjli__jydsh]:
            alias_map[rgjli__jydsh] |= alias_map[gzen__yoan]
        for gzen__yoan in cdc__hhxs[rgjli__jydsh]:
            alias_map[gzen__yoan] = alias_map[rgjli__jydsh]
    return alias_map, arg_aliases


if _check_numba_change:
    lines = inspect.getsource(ir_utils.find_potential_aliases)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'e6cf3e0f502f903453eb98346fc6854f87dc4ea1ac62f65c2d6aef3bf690b6c5':
        warnings.warn('ir_utils.find_potential_aliases has changed')
ir_utils.find_potential_aliases = find_potential_aliases
numba.parfors.array_analysis.find_potential_aliases = find_potential_aliases
if _check_numba_change:
    lines = inspect.getsource(ir_utils.dead_code_elimination)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '40a8626300a1a17523944ec7842b093c91258bbc60844bbd72191a35a4c366bf':
        warnings.warn('ir_utils.dead_code_elimination has changed')


def mini_dce(func_ir, typemap=None, alias_map=None, arg_aliases=None):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    gfvmn__tqnc = compute_cfg_from_blocks(func_ir.blocks)
    xgl__xcp = compute_use_defs(func_ir.blocks)
    wmxnd__xtl = compute_live_map(gfvmn__tqnc, func_ir.blocks, xgl__xcp.
        usemap, xgl__xcp.defmap)
    for jqsx__ndv, block in func_ir.blocks.items():
        lives = {rgjli__jydsh.name for rgjli__jydsh in block.terminator.
            list_vars()}
        for tzza__zogk, pbdx__ewum in gfvmn__tqnc.successors(jqsx__ndv):
            lives |= wmxnd__xtl[tzza__zogk]
        bth__tev = [block.terminator]
        for stmt in reversed(block.body[:-1]):
            if isinstance(stmt, ir.Assign):
                icj__rycwz = stmt.target
                kkv__cynaq = stmt.value
                if icj__rycwz.name not in lives:
                    if isinstance(kkv__cynaq, ir.Expr
                        ) and kkv__cynaq.op == 'make_function':
                        continue
                    if isinstance(kkv__cynaq, ir.Expr
                        ) and kkv__cynaq.op == 'getattr':
                        continue
                    if isinstance(kkv__cynaq, ir.Const):
                        continue
                    if typemap and isinstance(typemap.get(icj__rycwz, None),
                        types.Function):
                        continue
                if isinstance(kkv__cynaq, ir.Var
                    ) and icj__rycwz.name == kkv__cynaq.name:
                    continue
            if isinstance(stmt, ir.Del):
                if stmt.value not in lives:
                    continue
            if type(stmt) in analysis.ir_extension_usedefs:
                uaitq__nlo = analysis.ir_extension_usedefs[type(stmt)]
                hfml__uex, bknf__xbym = uaitq__nlo(stmt)
                lives -= bknf__xbym
                lives |= hfml__uex
            else:
                lives |= {rgjli__jydsh.name for rgjli__jydsh in stmt.
                    list_vars()}
                if isinstance(stmt, ir.Assign):
                    lives.remove(icj__rycwz.name)
            bth__tev.append(stmt)
        bth__tev.reverse()
        block.body = bth__tev


ir_utils.dead_code_elimination = mini_dce
numba.core.typed_passes.dead_code_elimination = mini_dce
numba.core.inline_closurecall.dead_code_elimination = mini_dce
from numba.core.cpu_options import InlineOptions


def make_overload_template(func, overload_func, jit_options, strict, inline,
    prefer_literal=False, **kwargs):
    hevv__kugf = getattr(func, '__name__', str(func))
    name = 'OverloadTemplate_%s' % (hevv__kugf,)
    no_unliteral = kwargs.pop('no_unliteral', False)
    base = numba.core.typing.templates._OverloadFunctionTemplate
    ljyzc__pccbk = dict(key=func, _overload_func=staticmethod(overload_func
        ), _impl_cache={}, _compiled_overloads={}, _jit_options=jit_options,
        _strict=strict, _inline=staticmethod(InlineOptions(inline)),
        _inline_overloads={}, prefer_literal=prefer_literal, _no_unliteral=
        no_unliteral, metadata=kwargs)
    return type(base)(name, (base,), ljyzc__pccbk)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        make_overload_template)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '7f6974584cb10e49995b652827540cc6732e497c0b9f8231b44fd83fcc1c0a83':
        warnings.warn(
            'numba.core.typing.templates.make_overload_template has changed')
numba.core.typing.templates.make_overload_template = make_overload_template


def _resolve(self, typ, attr):
    if self._attr != attr:
        return None
    if isinstance(typ, types.TypeRef):
        assert typ == self.key
    else:
        assert isinstance(typ, self.key)


    class MethodTemplate(AbstractTemplate):
        key = self.key, attr
        _inline = self._inline
        _no_unliteral = getattr(self, '_no_unliteral', False)
        _overload_func = staticmethod(self._overload_func)
        _inline_overloads = self._inline_overloads
        prefer_literal = self.prefer_literal

        def generic(_, args, kws):
            args = (typ,) + tuple(args)
            fnty = self._get_function_type(self.context, typ)
            sig = self._get_signature(self.context, fnty, args, kws)
            sig = sig.replace(pysig=numba.core.utils.pysignature(self.
                _overload_func))
            for grhxs__ndsr in fnty.templates:
                self._inline_overloads.update(grhxs__ndsr._inline_overloads)
            if sig is not None:
                return sig.as_method()
    return types.BoundFunction(MethodTemplate, typ)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadMethodTemplate._resolve)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'ce8e0935dc939d0867ef969e1ed2975adb3533a58a4133fcc90ae13c4418e4d6':
        warnings.warn(
            'numba.core.typing.templates._OverloadMethodTemplate._resolve has changed'
            )
numba.core.typing.templates._OverloadMethodTemplate._resolve = _resolve


def make_overload_attribute_template(typ, attr, overload_func, inline,
    prefer_literal=False, base=_OverloadAttributeTemplate, **kwargs):
    assert isinstance(typ, types.Type) or issubclass(typ, types.Type)
    name = 'OverloadAttributeTemplate_%s_%s' % (typ, attr)
    no_unliteral = kwargs.pop('no_unliteral', False)
    ljyzc__pccbk = dict(key=typ, _attr=attr, _impl_cache={}, _inline=
        staticmethod(InlineOptions(inline)), _inline_overloads={},
        _no_unliteral=no_unliteral, _overload_func=staticmethod(
        overload_func), prefer_literal=prefer_literal, metadata=kwargs)
    obj = type(base)(name, (base,), ljyzc__pccbk)
    return obj


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        make_overload_attribute_template)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f066c38c482d6cf8bf5735a529c3264118ba9b52264b24e58aad12a6b1960f5d':
        warnings.warn(
            'numba.core.typing.templates.make_overload_attribute_template has changed'
            )
numba.core.typing.templates.make_overload_attribute_template = (
    make_overload_attribute_template)


def generic(self, args, kws):
    from numba.core.typed_passes import PreLowerStripPhis
    fdvd__issq, hzrsz__ipnyv = self._get_impl(args, kws)
    if fdvd__issq is None:
        return
    ded__xdlo = types.Dispatcher(fdvd__issq)
    if not self._inline.is_never_inline:
        from numba.core import compiler, typed_passes
        from numba.core.inline_closurecall import InlineWorker
        lcint__ckqof = fdvd__issq._compiler
        flags = compiler.Flags()
        uxd__ntxjz = lcint__ckqof.targetdescr.typing_context
        fyp__blv = lcint__ckqof.targetdescr.target_context
        ulpz__zdrw = lcint__ckqof.pipeline_class(uxd__ntxjz, fyp__blv, None,
            None, None, flags, None)
        hrw__xeo = InlineWorker(uxd__ntxjz, fyp__blv, lcint__ckqof.locals,
            ulpz__zdrw, flags, None)
        yrijf__ftfmi = ded__xdlo.dispatcher.get_call_template
        grhxs__ndsr, hfgw__wjl, tis__phkgg, kws = yrijf__ftfmi(hzrsz__ipnyv,
            kws)
        if tis__phkgg in self._inline_overloads:
            return self._inline_overloads[tis__phkgg]['iinfo'].signature
        ir = hrw__xeo.run_untyped_passes(ded__xdlo.dispatcher.py_func,
            enable_ssa=True)
        typemap, return_type, calltypes, _ = typed_passes.type_inference_stage(
            self.context, fyp__blv, ir, tis__phkgg, None)
        ir = PreLowerStripPhis()._strip_phi_nodes(ir)
        ir._definitions = numba.core.ir_utils.build_definitions(ir.blocks)
        sig = Signature(return_type, tis__phkgg, None)
        self._inline_overloads[sig.args] = {'folded_args': tis__phkgg}
        rwjs__iwd = _EmptyImplementationEntry('always inlined')
        self._compiled_overloads[sig.args] = rwjs__iwd
        if not self._inline.is_always_inline:
            sig = ded__xdlo.get_call_type(self.context, hzrsz__ipnyv, kws)
            self._compiled_overloads[sig.args] = ded__xdlo.get_overload(sig)
        yiwt__acacc = _inline_info(ir, typemap, calltypes, sig)
        self._inline_overloads[sig.args] = {'folded_args': tis__phkgg,
            'iinfo': yiwt__acacc}
    else:
        sig = ded__xdlo.get_call_type(self.context, hzrsz__ipnyv, kws)
        if sig is None:
            return None
        self._compiled_overloads[sig.args] = ded__xdlo.get_overload(sig)
    return sig


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadFunctionTemplate.generic)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5d453a6d0215ebf0bab1279ff59eb0040b34938623be99142ce20acc09cdeb64':
        warnings.warn(
            'numba.core.typing.templates._OverloadFunctionTemplate.generic has changed'
            )
numba.core.typing.templates._OverloadFunctionTemplate.generic = generic


def bound_function(template_key, no_unliteral=False):

    def wrapper(method_resolver):

        @functools.wraps(method_resolver)
        def attribute_resolver(self, ty):


            class MethodTemplate(AbstractTemplate):
                key = template_key

                def generic(_, args, kws):
                    sig = method_resolver(self, ty, args, kws)
                    if sig is not None and sig.recvr is None:
                        sig = sig.replace(recvr=ty)
                    return sig
            MethodTemplate._no_unliteral = no_unliteral
            return types.BoundFunction(MethodTemplate, ty)
        return attribute_resolver
    return wrapper


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.bound_function)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a2feefe64eae6a15c56affc47bf0c1d04461f9566913442d539452b397103322':
        warnings.warn('numba.core.typing.templates.bound_function has changed')
numba.core.typing.templates.bound_function = bound_function


def get_call_type(self, context, args, kws):
    from numba.core import utils
    kyby__wyozf = [True, False]
    ztzlu__iori = [False, True]
    etm__upx = _ResolutionFailures(context, self, args, kws, depth=self._depth)
    from numba.core.target_extension import get_local_target
    yev__ysk = get_local_target(context)
    vudc__fng = utils.order_by_target_specificity(yev__ysk, self.templates,
        fnkey=self.key[0])
    self._depth += 1
    for ekac__foi in vudc__fng:
        twx__ucfxn = ekac__foi(context)
        saald__uowwx = (kyby__wyozf if twx__ucfxn.prefer_literal else
            ztzlu__iori)
        saald__uowwx = [True] if getattr(twx__ucfxn, '_no_unliteral', False
            ) else saald__uowwx
        for xav__hfd in saald__uowwx:
            try:
                if xav__hfd:
                    sig = twx__ucfxn.apply(args, kws)
                else:
                    jmwfh__jjczi = tuple([_unlit_non_poison(a) for a in args])
                    yjbg__aks = {aewyp__jmy: _unlit_non_poison(rgjli__jydsh
                        ) for aewyp__jmy, rgjli__jydsh in kws.items()}
                    sig = twx__ucfxn.apply(jmwfh__jjczi, yjbg__aks)
            except Exception as e:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                else:
                    sig = None
                    etm__upx.add_error(twx__ucfxn, False, e, xav__hfd)
            else:
                if sig is not None:
                    self._impl_keys[sig.args] = twx__ucfxn.get_impl_key(sig)
                    self._depth -= 1
                    return sig
                else:
                    nktom__hxxr = getattr(twx__ucfxn, 'cases', None)
                    if nktom__hxxr is not None:
                        msg = 'No match for registered cases:\n%s'
                        msg = msg % '\n'.join(' * {}'.format(x) for x in
                            nktom__hxxr)
                    else:
                        msg = 'No match.'
                    etm__upx.add_error(twx__ucfxn, True, msg, xav__hfd)
    etm__upx.raise_error()


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.BaseFunction.
        get_call_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '25f038a7216f8e6f40068ea81e11fd9af8ad25d19888f7304a549941b01b7015':
        warnings.warn(
            'numba.core.types.functions.BaseFunction.get_call_type has changed'
            )
numba.core.types.functions.BaseFunction.get_call_type = get_call_type
bodo_typing_error_info = """
This is often caused by the use of unsupported features or typing issues.
See https://docs.bodo.ai/
"""


def get_call_type2(self, context, args, kws):
    grhxs__ndsr = self.template(context)
    efqyc__uuo = None
    smfbc__buev = None
    ssz__krezl = None
    saald__uowwx = [True, False] if grhxs__ndsr.prefer_literal else [False,
        True]
    saald__uowwx = [True] if getattr(grhxs__ndsr, '_no_unliteral', False
        ) else saald__uowwx
    for xav__hfd in saald__uowwx:
        if xav__hfd:
            try:
                ssz__krezl = grhxs__ndsr.apply(args, kws)
            except Exception as mutdh__upcm:
                if isinstance(mutdh__upcm, errors.ForceLiteralArg):
                    raise mutdh__upcm
                efqyc__uuo = mutdh__upcm
                ssz__krezl = None
            else:
                break
        else:
            zak__fvo = tuple([_unlit_non_poison(a) for a in args])
            rap__swx = {aewyp__jmy: _unlit_non_poison(rgjli__jydsh) for 
                aewyp__jmy, rgjli__jydsh in kws.items()}
            eajvi__oysb = zak__fvo == args and kws == rap__swx
            if not eajvi__oysb and ssz__krezl is None:
                try:
                    ssz__krezl = grhxs__ndsr.apply(zak__fvo, rap__swx)
                except Exception as mutdh__upcm:
                    from numba.core import utils
                    if utils.use_new_style_errors() and not isinstance(
                        mutdh__upcm, errors.NumbaError):
                        raise mutdh__upcm
                    if isinstance(mutdh__upcm, errors.ForceLiteralArg):
                        if grhxs__ndsr.prefer_literal:
                            raise mutdh__upcm
                    smfbc__buev = mutdh__upcm
                else:
                    break
    if ssz__krezl is None and (smfbc__buev is not None or efqyc__uuo is not
        None):
        snck__ibvlg = '- Resolution failure for {} arguments:\n{}\n'
        lrbw__ohxh = _termcolor.highlight(snck__ibvlg)
        if numba.core.config.DEVELOPER_MODE:
            uze__fmon = ' ' * 4

            def add_bt(error):
                if isinstance(error, BaseException):
                    oluc__lvl = traceback.format_exception(type(error),
                        error, error.__traceback__)
                else:
                    oluc__lvl = ['']
                zxk__ksgiw = '\n{}'.format(2 * uze__fmon)
                cvh__zwq = _termcolor.reset(zxk__ksgiw + zxk__ksgiw.join(
                    _bt_as_lines(oluc__lvl)))
                return _termcolor.reset(cvh__zwq)
        else:
            add_bt = lambda X: ''

        def nested_msg(literalness, e):
            aow__ohr = str(e)
            aow__ohr = aow__ohr if aow__ohr else str(repr(e)) + add_bt(e)
            uwpf__kmgjf = errors.TypingError(textwrap.dedent(aow__ohr))
            return lrbw__ohxh.format(literalness, str(uwpf__kmgjf))
        import bodo
        if isinstance(efqyc__uuo, bodo.utils.typing.BodoError):
            raise efqyc__uuo
        if numba.core.config.DEVELOPER_MODE:
            raise errors.TypingError(nested_msg('literal', efqyc__uuo) +
                nested_msg('non-literal', smfbc__buev))
        else:
            msg = 'Compilation error for '
            if isinstance(self.this, bodo.hiframes.pd_dataframe_ext.
                DataFrameType):
                msg += 'DataFrame.'
            elif isinstance(self.this, bodo.hiframes.pd_series_ext.SeriesType):
                msg += 'Series.'
            msg += f'{self.typing_key[1]}().{bodo_typing_error_info}'
            raise errors.TypingError(msg)
    return ssz__krezl


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.BoundFunction.
        get_call_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '502cd77c0084452e903a45a0f1f8107550bfbde7179363b57dabd617ce135f4a':
        warnings.warn(
            'numba.core.types.functions.BoundFunction.get_call_type has changed'
            )
numba.core.types.functions.BoundFunction.get_call_type = get_call_type2


def string_from_string_and_size(self, string, size):
    from llvmlite.llvmpy.core import Type
    fnty = Type.function(self.pyobj, [self.cstring, self.py_ssize_t])
    rreaj__atj = 'PyUnicode_FromStringAndSize'
    fn = self._get_function(fnty, name=rreaj__atj)
    return self.builder.call(fn, [string, size])


numba.core.pythonapi.PythonAPI.string_from_string_and_size = (
    string_from_string_and_size)


def _compile_for_args(self, *args, **kws):
    assert not kws
    self._compilation_chain_init_hook()
    import bodo

    def error_rewrite(e, issue_type):
        if numba.core.config.SHOW_HELP:
            mezs__ulsms = errors.error_extras[issue_type]
            e.patch_message('\n'.join((str(e).rstrip(), mezs__ulsms)))
        if numba.core.config.FULL_TRACEBACKS:
            raise e
        else:
            raise e.with_traceback(None)
    deg__ewxm = []
    for a in args:
        if isinstance(a, numba.core.dispatcher.OmittedArg):
            deg__ewxm.append(types.Omitted(a.value))
        else:
            deg__ewxm.append(self.typeof_pyval(a))
    cvd__gdd = None
    try:
        error = None
        cvd__gdd = self.compile(tuple(deg__ewxm))
    except errors.ForceLiteralArg as e:
        akyj__fwt = [vyuxe__bxxrr for vyuxe__bxxrr in e.requested_args if 
            isinstance(args[vyuxe__bxxrr], types.Literal) and not
            isinstance(args[vyuxe__bxxrr], types.LiteralStrKeyDict)]
        if akyj__fwt:
            uvbks__zqns = """Repeated literal typing request.
{}.
This is likely caused by an error in typing. Please see nested and suppressed exceptions."""
            afty__vwgrd = ', '.join('Arg #{} is {}'.format(vyuxe__bxxrr,
                args[vyuxe__bxxrr]) for vyuxe__bxxrr in sorted(akyj__fwt))
            raise errors.CompilerError(uvbks__zqns.format(afty__vwgrd))
        hzrsz__ipnyv = []
        try:
            for vyuxe__bxxrr, rgjli__jydsh in enumerate(args):
                if vyuxe__bxxrr in e.requested_args:
                    if vyuxe__bxxrr in e.file_infos:
                        hzrsz__ipnyv.append(types.FilenameType(args[
                            vyuxe__bxxrr], e.file_infos[vyuxe__bxxrr]))
                    else:
                        hzrsz__ipnyv.append(types.literal(args[vyuxe__bxxrr]))
                else:
                    hzrsz__ipnyv.append(args[vyuxe__bxxrr])
            args = hzrsz__ipnyv
        except (OSError, FileNotFoundError) as vsu__qhq:
            error = FileNotFoundError(str(vsu__qhq) + '\n' + e.loc.
                strformat() + '\n')
        except bodo.utils.typing.BodoError as e:
            error = bodo.utils.typing.BodoError(str(e))
        if error is None:
            try:
                cvd__gdd = self._compile_for_args(*args)
            except TypingError as e:
                error = errors.TypingError(str(e))
            except bodo.utils.typing.BodoError as e:
                error = bodo.utils.typing.BodoError(str(e))
    except errors.TypingError as e:
        oyc__jjyxv = []
        for vyuxe__bxxrr, iflq__zpf in enumerate(args):
            val = iflq__zpf.value if isinstance(iflq__zpf, numba.core.
                dispatcher.OmittedArg) else iflq__zpf
            try:
                wgzi__xemnq = typeof(val, Purpose.argument)
            except ValueError as vcopd__aazo:
                oyc__jjyxv.append((vyuxe__bxxrr, str(vcopd__aazo)))
            else:
                if wgzi__xemnq is None:
                    oyc__jjyxv.append((vyuxe__bxxrr,
                        f'cannot determine Numba type of value {val}'))
        if oyc__jjyxv:
            aaspv__fwes = '\n'.join(
                f'- argument {vyuxe__bxxrr}: {pyvgh__szqs}' for 
                vyuxe__bxxrr, pyvgh__szqs in oyc__jjyxv)
            msg = f"""{str(e).rstrip()} 

This error may have been caused by the following argument(s):
{aaspv__fwes}
"""
            e.patch_message(msg)
        if "Cannot determine Numba type of <class 'numpy.ufunc'>" in e.msg:
            msg = 'Unsupported Numpy ufunc encountered in JIT code'
            error = bodo.utils.typing.BodoError(msg, loc=e.loc)
        elif not numba.core.config.DEVELOPER_MODE:
            if bodo_typing_error_info not in e.msg:
                dteg__jgz = ['Failed in nopython mode pipeline',
                    'Failed in bodo mode pipeline', 'numba', 'Overload',
                    'lowering']
                dcy__qyac = False
                for jaix__gwlbe in dteg__jgz:
                    if jaix__gwlbe in e.msg:
                        msg = 'Compilation error. '
                        msg += f'{bodo_typing_error_info}'
                        dcy__qyac = True
                        break
                if not dcy__qyac:
                    msg = f'{str(e)}'
                msg += '\n' + e.loc.strformat() + '\n'
                e.patch_message(msg)
        error_rewrite(e, 'typing')
    except errors.UnsupportedError as e:
        error_rewrite(e, 'unsupported_error')
    except (errors.NotDefinedError, errors.RedefinedError, errors.
        VerificationError) as e:
        error_rewrite(e, 'interpreter')
    except errors.ConstantInferenceError as e:
        error_rewrite(e, 'constant_inference')
    except bodo.utils.typing.BodoError as e:
        error = bodo.utils.typing.BodoError(str(e))
    except Exception as e:
        if numba.core.config.SHOW_HELP:
            if hasattr(e, 'patch_message'):
                mezs__ulsms = errors.error_extras['reportable']
                e.patch_message('\n'.join((str(e).rstrip(), mezs__ulsms)))
        raise e
    finally:
        self._types_active_call = []
        del args
        if error:
            raise error
    return cvd__gdd


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher._DispatcherBase.
        _compile_for_args)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5cdfbf0b13a528abf9f0408e70f67207a03e81d610c26b1acab5b2dc1f79bf06':
        warnings.warn(
            'numba.core.dispatcher._DispatcherBase._compile_for_args has changed'
            )
numba.core.dispatcher._DispatcherBase._compile_for_args = _compile_for_args


def resolve_gb_agg_funcs(cres):
    from bodo.ir.aggregate import gb_agg_cfunc_addr
    for kmcj__hijj in cres.library._codegen._engine._defined_symbols:
        if kmcj__hijj.startswith('cfunc'
            ) and 'get_agg_udf_addr' not in kmcj__hijj and (
            'bodo_gb_udf_update_local' in kmcj__hijj or 
            'bodo_gb_udf_combine' in kmcj__hijj or 'bodo_gb_udf_eval' in
            kmcj__hijj or 'bodo_gb_apply_general_udfs' in kmcj__hijj):
            gb_agg_cfunc_addr[kmcj__hijj
                ] = cres.library.get_pointer_to_function(kmcj__hijj)


def resolve_join_general_cond_funcs(cres):
    from bodo.ir.join import join_gen_cond_cfunc_addr
    for kmcj__hijj in cres.library._codegen._engine._defined_symbols:
        if kmcj__hijj.startswith('cfunc') and ('get_join_cond_addr' not in
            kmcj__hijj or 'bodo_join_gen_cond' in kmcj__hijj):
            join_gen_cond_cfunc_addr[kmcj__hijj
                ] = cres.library.get_pointer_to_function(kmcj__hijj)


def compile(self, sig):
    import numba.core.event as ev
    from numba.core import sigutils
    from numba.core.compiler_lock import global_compiler_lock
    fdvd__issq = self._get_dispatcher_for_current_target()
    if fdvd__issq is not self:
        return fdvd__issq.compile(sig)
    with ExitStack() as scope:
        cres = None

        def cb_compiler(dur):
            if cres is not None:
                self._callback_add_compiler_timer(dur, cres)

        def cb_llvm(dur):
            if cres is not None:
                self._callback_add_llvm_timer(dur, cres)
        scope.enter_context(ev.install_timer('numba:compiler_lock',
            cb_compiler))
        scope.enter_context(ev.install_timer('numba:llvm_lock', cb_llvm))
        scope.enter_context(global_compiler_lock)
        if not self._can_compile:
            raise RuntimeError('compilation disabled')
        with self._compiling_counter:
            args, return_type = sigutils.normalize_signature(sig)
            rdcqz__eflwo = self.overloads.get(tuple(args))
            if rdcqz__eflwo is not None:
                return rdcqz__eflwo.entry_point
            cres = self._cache.load_overload(sig, self.targetctx)
            if cres is not None:
                resolve_gb_agg_funcs(cres)
                resolve_join_general_cond_funcs(cres)
                self._cache_hits[sig] += 1
                if not cres.objectmode:
                    self.targetctx.insert_user_function(cres.entry_point,
                        cres.fndesc, [cres.library])
                self.add_overload(cres)
                return cres.entry_point
            self._cache_misses[sig] += 1
            suv__zni = dict(dispatcher=self, args=args, return_type=return_type
                )
            with ev.trigger_event('numba:compile', data=suv__zni):
                try:
                    cres = self._compiler.compile(args, return_type)
                except errors.ForceLiteralArg as e:

                    def folded(args, kws):
                        return self._compiler.fold_argument_types(args, kws)[1]
                    raise e.bind_fold_arguments(folded)
                self.add_overload(cres)
            self._cache.save_overload(sig, cres)
            return cres.entry_point


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.Dispatcher.compile)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '934ec993577ea3b1c7dd2181ac02728abf8559fd42c17062cc821541b092ff8f':
        warnings.warn('numba.core.dispatcher.Dispatcher.compile has changed')
numba.core.dispatcher.Dispatcher.compile = compile


def _get_module_for_linking(self):
    import llvmlite.binding as ll
    self._ensure_finalized()
    if self._shared_module is not None:
        return self._shared_module
    lnjb__azfm = self._final_module
    piqg__opxpb = []
    zlnu__xlt = 0
    for fn in lnjb__azfm.functions:
        zlnu__xlt += 1
        if not fn.is_declaration and fn.linkage == ll.Linkage.external:
            if 'get_agg_udf_addr' not in fn.name:
                if 'bodo_gb_udf_update_local' in fn.name:
                    continue
                if 'bodo_gb_udf_combine' in fn.name:
                    continue
                if 'bodo_gb_udf_eval' in fn.name:
                    continue
                if 'bodo_gb_apply_general_udfs' in fn.name:
                    continue
            if 'get_join_cond_addr' not in fn.name:
                if 'bodo_join_gen_cond' in fn.name:
                    continue
            piqg__opxpb.append(fn.name)
    if zlnu__xlt == 0:
        raise RuntimeError(
            'library unfit for linking: no available functions in %s' % (self,)
            )
    if piqg__opxpb:
        lnjb__azfm = lnjb__azfm.clone()
        for name in piqg__opxpb:
            lnjb__azfm.get_function(name).linkage = 'linkonce_odr'
    self._shared_module = lnjb__azfm
    return lnjb__azfm


if _check_numba_change:
    lines = inspect.getsource(numba.core.codegen.CPUCodeLibrary.
        _get_module_for_linking)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '56dde0e0555b5ec85b93b97c81821bce60784515a1fbf99e4542e92d02ff0a73':
        warnings.warn(
            'numba.core.codegen.CPUCodeLibrary._get_module_for_linking has changed'
            )
numba.core.codegen.CPUCodeLibrary._get_module_for_linking = (
    _get_module_for_linking)


def propagate(self, typeinfer):
    import bodo
    errors = []
    for vlo__jkhfd in self.constraints:
        loc = vlo__jkhfd.loc
        with typeinfer.warnings.catch_warnings(filename=loc.filename,
            lineno=loc.line):
            try:
                vlo__jkhfd(typeinfer)
            except numba.core.errors.ForceLiteralArg as e:
                errors.append(e)
            except numba.core.errors.TypingError as e:
                numba.core.typeinfer._logger.debug('captured error', exc_info=e
                    )
                ynmqa__hdodl = numba.core.errors.TypingError(str(e), loc=
                    vlo__jkhfd.loc, highlighting=False)
                errors.append(numba.core.utils.chain_exception(ynmqa__hdodl, e)
                    )
            except bodo.utils.typing.BodoError as e:
                if loc not in e.locs_in_msg:
                    errors.append(bodo.utils.typing.BodoError(str(e.msg) +
                        '\n' + loc.strformat() + '\n', locs_in_msg=e.
                        locs_in_msg + [loc]))
                else:
                    errors.append(bodo.utils.typing.BodoError(e.msg,
                        locs_in_msg=e.locs_in_msg))
            except Exception as e:
                from numba.core import utils
                if utils.use_old_style_errors():
                    numba.core.typeinfer._logger.debug('captured error',
                        exc_info=e)
                    msg = """Internal error at {con}.
{err}
Enable logging at debug level for details."""
                    ynmqa__hdodl = numba.core.errors.TypingError(msg.format
                        (con=vlo__jkhfd, err=str(e)), loc=vlo__jkhfd.loc,
                        highlighting=False)
                    errors.append(utils.chain_exception(ynmqa__hdodl, e))
                elif utils.use_new_style_errors():
                    raise e
                else:
                    msg = (
                        f"Unknown CAPTURED_ERRORS style: '{numba.core.config.CAPTURED_ERRORS}'."
                        )
                    assert 0, msg
    return errors


if _check_numba_change:
    lines = inspect.getsource(numba.core.typeinfer.ConstraintNetwork.propagate)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1e73635eeba9ba43cb3372f395b747ae214ce73b729fb0adba0a55237a1cb063':
        warnings.warn(
            'numba.core.typeinfer.ConstraintNetwork.propagate has changed')
numba.core.typeinfer.ConstraintNetwork.propagate = propagate


def raise_error(self):
    import bodo
    for knxyp__dec in self._failures.values():
        for fqxa__lwlv in knxyp__dec:
            if isinstance(fqxa__lwlv.error, ForceLiteralArg):
                raise fqxa__lwlv.error
            if isinstance(fqxa__lwlv.error, bodo.utils.typing.BodoError):
                raise fqxa__lwlv.error
    raise TypingError(self.format())


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.
        _ResolutionFailures.raise_error)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '84b89430f5c8b46cfc684804e6037f00a0f170005cd128ad245551787b2568ea':
        warnings.warn(
            'numba.core.types.functions._ResolutionFailures.raise_error has changed'
            )
numba.core.types.functions._ResolutionFailures.raise_error = raise_error


def bodo_remove_dead_block(block, lives, call_table, arg_aliases, alias_map,
    alias_set, func_ir, typemap):
    from bodo.transforms.distributed_pass import saved_array_analysis
    from bodo.utils.utils import is_array_typ, is_expr
    bweio__ncq = False
    bth__tev = [block.terminator]
    for stmt in reversed(block.body[:-1]):
        qss__fyu = set()
        bhz__eek = lives & alias_set
        for rgjli__jydsh in bhz__eek:
            qss__fyu |= alias_map[rgjli__jydsh]
        lives_n_aliases = lives | qss__fyu | arg_aliases
        if type(stmt) in remove_dead_extensions:
            ndcg__dtxx = remove_dead_extensions[type(stmt)]
            stmt = ndcg__dtxx(stmt, lives, lives_n_aliases, arg_aliases,
                alias_map, func_ir, typemap)
            if stmt is None:
                bweio__ncq = True
                continue
        if isinstance(stmt, ir.Assign):
            icj__rycwz = stmt.target
            kkv__cynaq = stmt.value
            if icj__rycwz.name not in lives and has_no_side_effect(kkv__cynaq,
                lives_n_aliases, call_table):
                bweio__ncq = True
                continue
            if saved_array_analysis and icj__rycwz.name in lives and is_expr(
                kkv__cynaq, 'getattr'
                ) and kkv__cynaq.attr == 'shape' and is_array_typ(typemap[
                kkv__cynaq.value.name]) and kkv__cynaq.value.name not in lives:
                dnd__divbg = {rgjli__jydsh: aewyp__jmy for aewyp__jmy,
                    rgjli__jydsh in func_ir.blocks.items()}
                if block in dnd__divbg:
                    jqsx__ndv = dnd__divbg[block]
                    vjqa__gdda = saved_array_analysis.get_equiv_set(jqsx__ndv)
                    eopel__ccw = vjqa__gdda.get_equiv_set(kkv__cynaq.value)
                    if eopel__ccw is not None:
                        for rgjli__jydsh in eopel__ccw:
                            if rgjli__jydsh.endswith('#0'):
                                rgjli__jydsh = rgjli__jydsh[:-2]
                            if rgjli__jydsh in typemap and is_array_typ(typemap
                                [rgjli__jydsh]) and rgjli__jydsh in lives:
                                kkv__cynaq.value = ir.Var(kkv__cynaq.value.
                                    scope, rgjli__jydsh, kkv__cynaq.value.loc)
                                bweio__ncq = True
                                break
            if isinstance(kkv__cynaq, ir.Var
                ) and icj__rycwz.name == kkv__cynaq.name:
                bweio__ncq = True
                continue
        if isinstance(stmt, ir.Del):
            if stmt.value not in lives:
                bweio__ncq = True
                continue
        if isinstance(stmt, ir.SetItem):
            name = stmt.target.name
            if name not in lives_n_aliases:
                continue
        if type(stmt) in analysis.ir_extension_usedefs:
            uaitq__nlo = analysis.ir_extension_usedefs[type(stmt)]
            hfml__uex, bknf__xbym = uaitq__nlo(stmt)
            lives -= bknf__xbym
            lives |= hfml__uex
        else:
            lives |= {rgjli__jydsh.name for rgjli__jydsh in stmt.list_vars()}
            if isinstance(stmt, ir.Assign):
                vkbtd__mea = set()
                if isinstance(kkv__cynaq, ir.Expr):
                    vkbtd__mea = {rgjli__jydsh.name for rgjli__jydsh in
                        kkv__cynaq.list_vars()}
                if icj__rycwz.name not in vkbtd__mea:
                    lives.remove(icj__rycwz.name)
        bth__tev.append(stmt)
    bth__tev.reverse()
    block.body = bth__tev
    return bweio__ncq


ir_utils.remove_dead_block = bodo_remove_dead_block


@infer_global(set)
class SetBuiltin(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if args:
            rosad__chq, = args
            if isinstance(rosad__chq, types.IterableType):
                dtype = rosad__chq.iterator_type.yield_type
                if isinstance(dtype, types.Hashable
                    ) or dtype == numba.core.types.unicode_type:
                    return signature(types.Set(dtype), rosad__chq)
        else:
            return signature(types.Set(types.undefined))


def Set__init__(self, dtype, reflected=False):
    assert isinstance(dtype, (types.Hashable, types.Undefined)
        ) or dtype == numba.core.types.unicode_type
    self.dtype = dtype
    self.reflected = reflected
    ljja__sjjw = 'reflected set' if reflected else 'set'
    name = '%s(%s)' % (ljja__sjjw, self.dtype)
    super(types.Set, self).__init__(name=name)


types.Set.__init__ = Set__init__


@lower_builtin(operator.eq, types.UnicodeType, types.UnicodeType)
def eq_str(context, builder, sig, args):
    func = numba.cpython.unicode.unicode_eq(*sig.args)
    return context.compile_internal(builder, func, sig, args)


numba.parfors.parfor.push_call_vars = (lambda blocks, saved_globals,
    saved_getattrs, typemap, nested=False: None)


def maybe_literal(value):
    if isinstance(value, (list, dict, pytypes.FunctionType)):
        return
    if isinstance(value, tuple):
        try:
            return types.Tuple([literal(x) for x in value])
        except LiteralTypingError as hmeej__ghyq:
            return
    try:
        return literal(value)
    except LiteralTypingError as hmeej__ghyq:
        return


if _check_numba_change:
    lines = inspect.getsource(types.maybe_literal)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8fb2fd93acf214b28e33e37d19dc2f7290a42792ec59b650553ac278854b5081':
        warnings.warn('types.maybe_literal has changed')
types.maybe_literal = maybe_literal
types.misc.maybe_literal = maybe_literal


def CacheImpl__init__(self, py_func):
    self._lineno = py_func.__code__.co_firstlineno
    try:
        unkp__qgsuo = py_func.__qualname__
    except AttributeError as hmeej__ghyq:
        unkp__qgsuo = py_func.__name__
    vvj__bbzb = inspect.getfile(py_func)
    for cls in self._locator_classes:
        wtwo__ghp = cls.from_function(py_func, vvj__bbzb)
        if wtwo__ghp is not None:
            break
    else:
        raise RuntimeError(
            'cannot cache function %r: no locator available for file %r' %
            (unkp__qgsuo, vvj__bbzb))
    self._locator = wtwo__ghp
    kuqbv__epfy = inspect.getfile(py_func)
    jenaf__nry = os.path.splitext(os.path.basename(kuqbv__epfy))[0]
    if vvj__bbzb.startswith('<ipython-'):
        largi__shl = re.sub('(ipython-input)(-\\d+)(-[0-9a-fA-F]+)',
            '\\1\\3', jenaf__nry, count=1)
        if largi__shl == jenaf__nry:
            warnings.warn(
                'Did not recognize ipython module name syntax. Caching might not work'
                )
        jenaf__nry = largi__shl
    yzbb__azcwc = '%s.%s' % (jenaf__nry, unkp__qgsuo)
    pmuy__faba = getattr(sys, 'abiflags', '')
    self._filename_base = self.get_filename_base(yzbb__azcwc, pmuy__faba)


if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheImpl.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b46d298146e3844e9eaeef29d36f5165ba4796c270ca50d2b35f9fcdc0fa032a':
        warnings.warn('numba.core.caching._CacheImpl.__init__ has changed')
numba.core.caching._CacheImpl.__init__ = CacheImpl__init__


def _analyze_broadcast(self, scope, equiv_set, loc, args, fn):
    from numba.parfors.array_analysis import ArrayAnalysis
    sykfc__gyegw = list(filter(lambda a: self._istuple(a.name), args))
    if len(sykfc__gyegw) == 2 and fn.__name__ == 'add':
        flw__rmav = self.typemap[sykfc__gyegw[0].name]
        byd__tpxnf = self.typemap[sykfc__gyegw[1].name]
        if flw__rmav.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                sykfc__gyegw[1]))
        if byd__tpxnf.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                sykfc__gyegw[0]))
        try:
            gxhd__hyyu = [equiv_set.get_shape(x) for x in sykfc__gyegw]
            if None in gxhd__hyyu:
                return None
            kqcc__qjoj = sum(gxhd__hyyu, ())
            return ArrayAnalysis.AnalyzeResult(shape=kqcc__qjoj)
        except GuardException as hmeej__ghyq:
            return None
    soopi__xhd = list(filter(lambda a: self._isarray(a.name), args))
    require(len(soopi__xhd) > 0)
    bmipp__azbqd = [x.name for x in soopi__xhd]
    wudzz__szva = [self.typemap[x.name].ndim for x in soopi__xhd]
    npo__qcx = max(wudzz__szva)
    require(npo__qcx > 0)
    gxhd__hyyu = [equiv_set.get_shape(x) for x in soopi__xhd]
    if any(a is None for a in gxhd__hyyu):
        return ArrayAnalysis.AnalyzeResult(shape=soopi__xhd[0], pre=self.
            _call_assert_equiv(scope, loc, equiv_set, soopi__xhd))
    return self._broadcast_assert_shapes(scope, equiv_set, loc, gxhd__hyyu,
        bmipp__azbqd)


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.array_analysis.ArrayAnalysis.
        _analyze_broadcast)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '6c91fec038f56111338ea2b08f5f0e7f61ebdab1c81fb811fe26658cc354e40f':
        warnings.warn(
            'numba.parfors.array_analysis.ArrayAnalysis._analyze_broadcast has changed'
            )
numba.parfors.array_analysis.ArrayAnalysis._analyze_broadcast = (
    _analyze_broadcast)


def convert_code_obj_to_function(code_obj, caller_ir):
    import bodo
    ehbw__zbu = code_obj.code
    bxcxv__afqp = len(ehbw__zbu.co_freevars)
    fxv__mosrb = ehbw__zbu.co_freevars
    if code_obj.closure is not None:
        assert isinstance(code_obj.closure, ir.Var)
        tbdg__mnk, op = ir_utils.find_build_sequence(caller_ir, code_obj.
            closure)
        assert op == 'build_tuple'
        fxv__mosrb = [rgjli__jydsh.name for rgjli__jydsh in tbdg__mnk]
    mnpg__licvp = caller_ir.func_id.func.__globals__
    try:
        mnpg__licvp = getattr(code_obj, 'globals', mnpg__licvp)
    except KeyError as hmeej__ghyq:
        pass
    msg = (
        "Inner function is using non-constant variable '{}' from outer function. Please pass as argument if possible. See https://docs.bodo.ai/latest/source/programming_with_bodo/bodo_api_reference/udfs.html"
        )
    ytpv__kubhi = []
    for x in fxv__mosrb:
        try:
            icga__eqzu = caller_ir.get_definition(x)
        except KeyError as hmeej__ghyq:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
        from numba.core.registry import CPUDispatcher
        if isinstance(icga__eqzu, (ir.Const, ir.Global, ir.FreeVar)):
            val = icga__eqzu.value
            if isinstance(val, str):
                val = "'{}'".format(val)
            if isinstance(val, pytypes.FunctionType):
                hevv__kugf = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                mnpg__licvp[hevv__kugf] = bodo.jit(distributed=False)(val)
                mnpg__licvp[hevv__kugf].is_nested_func = True
                val = hevv__kugf
            if isinstance(val, CPUDispatcher):
                hevv__kugf = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                mnpg__licvp[hevv__kugf] = val
                val = hevv__kugf
            ytpv__kubhi.append(val)
        elif isinstance(icga__eqzu, ir.Expr
            ) and icga__eqzu.op == 'make_function':
            ugchi__gwx = convert_code_obj_to_function(icga__eqzu, caller_ir)
            hevv__kugf = ir_utils.mk_unique_var('nested_func').replace('.', '_'
                )
            mnpg__licvp[hevv__kugf] = bodo.jit(distributed=False)(ugchi__gwx)
            mnpg__licvp[hevv__kugf].is_nested_func = True
            ytpv__kubhi.append(hevv__kugf)
        else:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
    frz__ugmhx = '\n'.join([('\tc_%d = %s' % (vyuxe__bxxrr, x)) for 
        vyuxe__bxxrr, x in enumerate(ytpv__kubhi)])
    bbi__rmmp = ','.join([('c_%d' % vyuxe__bxxrr) for vyuxe__bxxrr in range
        (bxcxv__afqp)])
    tkhzu__iyow = list(ehbw__zbu.co_varnames)
    cegzf__gad = 0
    miulg__xmz = ehbw__zbu.co_argcount
    jodfn__esoca = caller_ir.get_definition(code_obj.defaults)
    if jodfn__esoca is not None:
        if isinstance(jodfn__esoca, tuple):
            ftab__nlyb = [caller_ir.get_definition(x).value for x in
                jodfn__esoca]
            xki__ofj = tuple(ftab__nlyb)
        else:
            ftab__nlyb = [caller_ir.get_definition(x).value for x in
                jodfn__esoca.items]
            xki__ofj = tuple(ftab__nlyb)
        cegzf__gad = len(xki__ofj)
    wqs__azfp = miulg__xmz - cegzf__gad
    vxwa__rwvkd = ','.join([('%s' % tkhzu__iyow[vyuxe__bxxrr]) for
        vyuxe__bxxrr in range(wqs__azfp)])
    if cegzf__gad:
        vood__zyh = [('%s = %s' % (tkhzu__iyow[vyuxe__bxxrr + wqs__azfp],
            xki__ofj[vyuxe__bxxrr])) for vyuxe__bxxrr in range(cegzf__gad)]
        vxwa__rwvkd += ', '
        vxwa__rwvkd += ', '.join(vood__zyh)
    return _create_function_from_code_obj(ehbw__zbu, frz__ugmhx,
        vxwa__rwvkd, bbi__rmmp, mnpg__licvp)


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.convert_code_obj_to_function)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b840769812418d589460e924a15477e83e7919aac8a3dcb0188ff447344aa8ac':
        warnings.warn(
            'numba.core.ir_utils.convert_code_obj_to_function has changed')
numba.core.ir_utils.convert_code_obj_to_function = convert_code_obj_to_function
numba.core.untyped_passes.convert_code_obj_to_function = (
    convert_code_obj_to_function)


def passmanager_run(self, state):
    from numba.core.compiler import _EarlyPipelineCompletion
    if not self.finalized:
        raise RuntimeError('Cannot run non-finalised pipeline')
    from numba.core.compiler_machinery import CompilerPass, _pass_registry
    import bodo
    for ypoif__tzglc, (bszpf__swxgl, hfiv__pcw) in enumerate(self.passes):
        try:
            numba.core.tracing.event('-- %s' % hfiv__pcw)
            ylaiy__ktlcs = _pass_registry.get(bszpf__swxgl).pass_inst
            if isinstance(ylaiy__ktlcs, CompilerPass):
                self._runPass(ypoif__tzglc, ylaiy__ktlcs, state)
            else:
                raise BaseException('Legacy pass in use')
        except _EarlyPipelineCompletion as e:
            raise e
        except bodo.utils.typing.BodoError as e:
            raise
        except Exception as e:
            if numba.core.config.DEVELOPER_MODE:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                msg = 'Failed in %s mode pipeline (step: %s)' % (self.
                    pipeline_name, hfiv__pcw)
                sca__ibi = self._patch_error(msg, e)
                raise sca__ibi
            else:
                raise e


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler_machinery.PassManager.run)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '43505782e15e690fd2d7e53ea716543bec37aa0633502956864edf649e790cdb':
        warnings.warn(
            'numba.core.compiler_machinery.PassManager.run has changed')
numba.core.compiler_machinery.PassManager.run = passmanager_run
if _check_numba_change:
    lines = inspect.getsource(numba.np.ufunc.parallel._launch_threads)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a57ef28c4168fdd436a5513bba4351ebc6d9fba76c5819f44046431a79b9030f':
        warnings.warn('numba.np.ufunc.parallel._launch_threads has changed')
numba.np.ufunc.parallel._launch_threads = lambda : None


def get_reduce_nodes(reduction_node, nodes, func_ir):
    nitc__uke = None
    bknf__xbym = {}

    def lookup(var, already_seen, varonly=True):
        val = bknf__xbym.get(var.name, None)
        if isinstance(val, ir.Var):
            if val.name in already_seen:
                return var
            already_seen.add(val.name)
            return lookup(val, already_seen, varonly)
        else:
            return var if varonly or val is None else val
    name = reduction_node.name
    saq__tfzvb = reduction_node.unversioned_name
    for vyuxe__bxxrr, stmt in enumerate(nodes):
        icj__rycwz = stmt.target
        kkv__cynaq = stmt.value
        bknf__xbym[icj__rycwz.name] = kkv__cynaq
        if isinstance(kkv__cynaq, ir.Var) and kkv__cynaq.name in bknf__xbym:
            kkv__cynaq = lookup(kkv__cynaq, set())
        if isinstance(kkv__cynaq, ir.Expr):
            rjz__pleye = set(lookup(rgjli__jydsh, set(), True).name for
                rgjli__jydsh in kkv__cynaq.list_vars())
            if name in rjz__pleye:
                args = [(x.name, lookup(x, set(), True)) for x in
                    get_expr_args(kkv__cynaq)]
                aldbn__evbvs = [x for x, zhr__twx in args if zhr__twx.name !=
                    name]
                args = [(x, zhr__twx) for x, zhr__twx in args if x !=
                    zhr__twx.name]
                pqgfn__irf = dict(args)
                if len(aldbn__evbvs) == 1:
                    pqgfn__irf[aldbn__evbvs[0]] = ir.Var(icj__rycwz.scope, 
                        name + '#init', icj__rycwz.loc)
                replace_vars_inner(kkv__cynaq, pqgfn__irf)
                nitc__uke = nodes[vyuxe__bxxrr:]
                break
    return nitc__uke


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_reduce_nodes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a05b52aff9cb02e595a510cd34e973857303a71097fc5530567cb70ca183ef3b':
        warnings.warn('numba.parfors.parfor.get_reduce_nodes has changed')
numba.parfors.parfor.get_reduce_nodes = get_reduce_nodes


def _can_reorder_stmts(stmt, next_stmt, func_ir, call_table, alias_map,
    arg_aliases):
    from numba.parfors.parfor import Parfor, expand_aliases, is_assert_equiv
    if isinstance(stmt, Parfor) and not isinstance(next_stmt, Parfor
        ) and not isinstance(next_stmt, ir.Print) and (not isinstance(
        next_stmt, ir.Assign) or has_no_side_effect(next_stmt.value, set(),
        call_table) or guard(is_assert_equiv, func_ir, next_stmt.value)):
        ijmgj__eipu = expand_aliases({rgjli__jydsh.name for rgjli__jydsh in
            stmt.list_vars()}, alias_map, arg_aliases)
        ugsi__idrhm = expand_aliases(get_parfor_writes(stmt, func_ir),
            alias_map, arg_aliases)
        arxcb__nfo = expand_aliases({rgjli__jydsh.name for rgjli__jydsh in
            next_stmt.list_vars()}, alias_map, arg_aliases)
        bon__piftt = expand_aliases(get_stmt_writes(next_stmt, func_ir),
            alias_map, arg_aliases)
        if len(ugsi__idrhm & arxcb__nfo | bon__piftt & ijmgj__eipu) == 0:
            return True
    return False


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor._can_reorder_stmts)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '18caa9a01b21ab92b4f79f164cfdbc8574f15ea29deedf7bafdf9b0e755d777c':
        warnings.warn('numba.parfors.parfor._can_reorder_stmts has changed')
numba.parfors.parfor._can_reorder_stmts = _can_reorder_stmts


def get_parfor_writes(parfor, func_ir):
    from numba.parfors.parfor import Parfor
    assert isinstance(parfor, Parfor)
    ujtky__gvs = set()
    blocks = parfor.loop_body.copy()
    blocks[-1] = parfor.init_block
    for block in blocks.values():
        for stmt in block.body:
            ujtky__gvs.update(get_stmt_writes(stmt, func_ir))
            if isinstance(stmt, Parfor):
                ujtky__gvs.update(get_parfor_writes(stmt, func_ir))
    return ujtky__gvs


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_parfor_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a7b29cd76832b6f6f1f2d2397ec0678c1409b57a6eab588bffd344b775b1546f':
        warnings.warn('numba.parfors.parfor.get_parfor_writes has changed')


def get_stmt_writes(stmt, func_ir):
    import bodo
    from bodo.utils.utils import is_call_assign
    ujtky__gvs = set()
    if isinstance(stmt, (ir.Assign, ir.SetItem, ir.StaticSetItem)):
        ujtky__gvs.add(stmt.target.name)
    if isinstance(stmt, bodo.ir.aggregate.Aggregate):
        ujtky__gvs = {rgjli__jydsh.name for rgjli__jydsh in stmt.
            df_out_vars.values()}
        if stmt.out_key_vars is not None:
            ujtky__gvs.update({rgjli__jydsh.name for rgjli__jydsh in stmt.
                out_key_vars})
    if isinstance(stmt, (bodo.ir.csv_ext.CsvReader, bodo.ir.parquet_ext.
        ParquetReader)):
        ujtky__gvs = {rgjli__jydsh.name for rgjli__jydsh in stmt.out_vars}
    if isinstance(stmt, bodo.ir.join.Join):
        ujtky__gvs = {rgjli__jydsh.name for rgjli__jydsh in stmt.
            out_data_vars.values()}
    if isinstance(stmt, bodo.ir.sort.Sort):
        if not stmt.inplace:
            ujtky__gvs.update({rgjli__jydsh.name for rgjli__jydsh in stmt.
                out_key_arrs})
            ujtky__gvs.update({rgjli__jydsh.name for rgjli__jydsh in stmt.
                df_out_vars.values()})
    if is_call_assign(stmt):
        srq__awykq = guard(find_callname, func_ir, stmt.value)
        if srq__awykq in (('setitem_str_arr_ptr', 'bodo.libs.str_arr_ext'),
            ('setna', 'bodo.libs.array_kernels'), (
            'str_arr_item_to_numeric', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_int_to_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_NA_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_set_not_na', 'bodo.libs.str_arr_ext'), (
            'set_bit_to_arr', 'bodo.libs.int_arr_ext')):
            ujtky__gvs.add(stmt.value.args[0].name)
    return ujtky__gvs


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.get_stmt_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1a7a80b64c9a0eb27e99dc8eaae187bde379d4da0b74c84fbf87296d87939974':
        warnings.warn('numba.core.ir_utils.get_stmt_writes has changed')


def patch_message(self, new_message):
    self.msg = new_message
    self.args = (new_message,) + self.args[1:]


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.NumbaError.patch_message)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'ed189a428a7305837e76573596d767b6e840e99f75c05af6941192e0214fa899':
        warnings.warn('numba.core.errors.NumbaError.patch_message has changed')
numba.core.errors.NumbaError.patch_message = patch_message


def add_context(self, msg):
    if numba.core.config.DEVELOPER_MODE:
        self.contexts.append(msg)
        ndcg__dtxx = _termcolor.errmsg('{0}') + _termcolor.filename(
            'During: {1}')
        ohd__ycv = ndcg__dtxx.format(self, msg)
        self.args = ohd__ycv,
    else:
        ndcg__dtxx = _termcolor.errmsg('{0}')
        ohd__ycv = ndcg__dtxx.format(self)
        self.args = ohd__ycv,
    return self


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.NumbaError.add_context)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '6a388d87788f8432c2152ac55ca9acaa94dbc3b55be973b2cf22dd4ee7179ab8':
        warnings.warn('numba.core.errors.NumbaError.add_context has changed')
numba.core.errors.NumbaError.add_context = add_context


def _get_dist_spec_from_options(spec, **options):
    from bodo.transforms.distributed_analysis import Distribution
    dist_spec = {}
    if 'distributed' in options:
        for jfnj__zpsh in options['distributed']:
            dist_spec[jfnj__zpsh] = Distribution.OneD_Var
    if 'distributed_block' in options:
        for jfnj__zpsh in options['distributed_block']:
            dist_spec[jfnj__zpsh] = Distribution.OneD
    return dist_spec


def register_class_type(cls, spec, class_ctor, builder, **options):
    import typing as pt
    from numba.core.typing.asnumbatype import as_numba_type
    import bodo
    dist_spec = _get_dist_spec_from_options(spec, **options)
    rrz__duoog = options.get('returns_maybe_distributed', True)
    if spec is None:
        spec = OrderedDict()
    elif isinstance(spec, Sequence):
        spec = OrderedDict(spec)
    for attr, ljzn__uxq in pt.get_type_hints(cls).items():
        if attr not in spec:
            spec[attr] = as_numba_type(ljzn__uxq)
    jitclass_base._validate_spec(spec)
    spec = jitclass_base._fix_up_private_attr(cls.__name__, spec)
    modjq__rtui = {}
    for bsuh__rcwc in reversed(inspect.getmro(cls)):
        modjq__rtui.update(bsuh__rcwc.__dict__)
    gvtr__zuqzl, hoq__ypzun, rpk__uxt, dyl__drc = {}, {}, {}, {}
    for aewyp__jmy, rgjli__jydsh in modjq__rtui.items():
        if isinstance(rgjli__jydsh, pytypes.FunctionType):
            gvtr__zuqzl[aewyp__jmy] = rgjli__jydsh
        elif isinstance(rgjli__jydsh, property):
            hoq__ypzun[aewyp__jmy] = rgjli__jydsh
        elif isinstance(rgjli__jydsh, staticmethod):
            rpk__uxt[aewyp__jmy] = rgjli__jydsh
        else:
            dyl__drc[aewyp__jmy] = rgjli__jydsh
    dbayf__jno = (set(gvtr__zuqzl) | set(hoq__ypzun) | set(rpk__uxt)) & set(
        spec)
    if dbayf__jno:
        raise NameError('name shadowing: {0}'.format(', '.join(dbayf__jno)))
    rbqyb__dhve = dyl__drc.pop('__doc__', '')
    jitclass_base._drop_ignored_attrs(dyl__drc)
    if dyl__drc:
        msg = 'class members are not yet supported: {0}'
        zsvs__ypjwa = ', '.join(dyl__drc.keys())
        raise TypeError(msg.format(zsvs__ypjwa))
    for aewyp__jmy, rgjli__jydsh in hoq__ypzun.items():
        if rgjli__jydsh.fdel is not None:
            raise TypeError('deleter is not supported: {0}'.format(aewyp__jmy))
    jit_methods = {aewyp__jmy: bodo.jit(returns_maybe_distributed=
        rrz__duoog)(rgjli__jydsh) for aewyp__jmy, rgjli__jydsh in
        gvtr__zuqzl.items()}
    jit_props = {}
    for aewyp__jmy, rgjli__jydsh in hoq__ypzun.items():
        ljyzc__pccbk = {}
        if rgjli__jydsh.fget:
            ljyzc__pccbk['get'] = bodo.jit(rgjli__jydsh.fget)
        if rgjli__jydsh.fset:
            ljyzc__pccbk['set'] = bodo.jit(rgjli__jydsh.fset)
        jit_props[aewyp__jmy] = ljyzc__pccbk
    jit_static_methods = {aewyp__jmy: bodo.jit(rgjli__jydsh.__func__) for 
        aewyp__jmy, rgjli__jydsh in rpk__uxt.items()}
    yvsa__shco = class_ctor(cls, jitclass_base.ConstructorTemplate, spec,
        jit_methods, jit_props, jit_static_methods, dist_spec)
    kckd__dztmm = dict(class_type=yvsa__shco, __doc__=rbqyb__dhve)
    kckd__dztmm.update(jit_static_methods)
    cls = jitclass_base.JitClassType(cls.__name__, (cls,), kckd__dztmm)
    typingctx = numba.core.registry.cpu_target.typing_context
    typingctx.insert_global(cls, yvsa__shco)
    targetctx = numba.core.registry.cpu_target.target_context
    builder(yvsa__shco, typingctx, targetctx).register()
    as_numba_type.register(cls, yvsa__shco.instance_type)
    return cls


if _check_numba_change:
    lines = inspect.getsource(jitclass_base.register_class_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '005e6e2e89a47f77a19ba86305565050d4dbc2412fc4717395adf2da348671a9':
        warnings.warn('jitclass_base.register_class_type has changed')
jitclass_base.register_class_type = register_class_type


def ClassType__init__(self, class_def, ctor_template_cls, struct,
    jit_methods, jit_props, jit_static_methods, dist_spec=None):
    if dist_spec is None:
        dist_spec = {}
    self.class_name = class_def.__name__
    self.class_doc = class_def.__doc__
    self._ctor_template_class = ctor_template_cls
    self.jit_methods = jit_methods
    self.jit_props = jit_props
    self.jit_static_methods = jit_static_methods
    self.struct = struct
    self.dist_spec = dist_spec
    cztqn__bniu = ','.join('{0}:{1}'.format(aewyp__jmy, rgjli__jydsh) for 
        aewyp__jmy, rgjli__jydsh in struct.items())
    ymw__yrq = ','.join('{0}:{1}'.format(aewyp__jmy, rgjli__jydsh) for 
        aewyp__jmy, rgjli__jydsh in dist_spec.items())
    name = '{0}.{1}#{2:x}<{3}><{4}>'.format(self.name_prefix, self.
        class_name, id(self), cztqn__bniu, ymw__yrq)
    super(types.misc.ClassType, self).__init__(name)


if _check_numba_change:
    lines = inspect.getsource(types.misc.ClassType.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '2b848ea82946c88f540e81f93ba95dfa7cd66045d944152a337fe2fc43451c30':
        warnings.warn('types.misc.ClassType.__init__ has changed')
types.misc.ClassType.__init__ = ClassType__init__


def jitclass(cls_or_spec=None, spec=None, **options):
    if cls_or_spec is not None and spec is None and not isinstance(cls_or_spec,
        type):
        spec = cls_or_spec
        cls_or_spec = None

    def wrap(cls):
        if numba.core.config.DISABLE_JIT:
            return cls
        else:
            from numba.experimental.jitclass.base import ClassBuilder
            return register_class_type(cls, spec, types.ClassType,
                ClassBuilder, **options)
    if cls_or_spec is None:
        return wrap
    else:
        return wrap(cls_or_spec)


if _check_numba_change:
    lines = inspect.getsource(jitclass_decorators.jitclass)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '265f1953ee5881d1a5d90238d3c932cd300732e41495657e65bf51e59f7f4af5':
        warnings.warn('jitclass_decorators.jitclass has changed')


def CallConstraint_resolve(self, typeinfer, typevars, fnty):
    assert fnty
    context = typeinfer.context
    dssb__lgum = numba.core.typeinfer.fold_arg_vars(typevars, self.args,
        self.vararg, self.kws)
    if dssb__lgum is None:
        return
    wkrs__vchn, vpfv__rjf = dssb__lgum
    for a in itertools.chain(wkrs__vchn, vpfv__rjf.values()):
        if not a.is_precise() and not isinstance(a, types.Array):
            return
    if isinstance(fnty, types.TypeRef):
        fnty = fnty.instance_type
    try:
        sig = typeinfer.resolve_call(fnty, wkrs__vchn, vpfv__rjf)
    except ForceLiteralArg as e:
        lmti__hmu = (fnty.this,) + tuple(self.args) if isinstance(fnty,
            types.BoundFunction) else self.args
        folded = e.fold_arguments(lmti__hmu, self.kws)
        ebhpi__rlf = set()
        irl__nap = set()
        cztlg__njacd = {}
        for ypoif__tzglc in e.requested_args:
            ctxhv__tzb = typeinfer.func_ir.get_definition(folded[ypoif__tzglc])
            if isinstance(ctxhv__tzb, ir.Arg):
                ebhpi__rlf.add(ctxhv__tzb.index)
                if ctxhv__tzb.index in e.file_infos:
                    cztlg__njacd[ctxhv__tzb.index] = e.file_infos[
                        ctxhv__tzb.index]
            else:
                irl__nap.add(ypoif__tzglc)
        if irl__nap:
            raise TypingError('Cannot request literal type.', loc=self.loc)
        elif ebhpi__rlf:
            raise ForceLiteralArg(ebhpi__rlf, loc=self.loc, file_infos=
                cztlg__njacd)
    if sig is None:
        epzdo__cicjf = 'Invalid use of {0} with parameters ({1})'
        args = [str(a) for a in wkrs__vchn]
        args += [('%s=%s' % (aewyp__jmy, rgjli__jydsh)) for aewyp__jmy,
            rgjli__jydsh in sorted(vpfv__rjf.items())]
        fodr__xcygu = epzdo__cicjf.format(fnty, ', '.join(map(str, args)))
        yyady__sot = context.explain_function_type(fnty)
        msg = '\n'.join([fodr__xcygu, yyady__sot])
        raise TypingError(msg)
    typeinfer.add_type(self.target, sig.return_type, loc=self.loc)
    if isinstance(fnty, types.BoundFunction
        ) and sig.recvr is not None and sig.recvr != fnty.this:
        nxc__dudnc = context.unify_pairs(sig.recvr, fnty.this)
        if nxc__dudnc is None and fnty.this.is_precise(
            ) and sig.recvr.is_precise():
            msg = 'Cannot refine type {} to {}'.format(sig.recvr, fnty.this)
            raise TypingError(msg, loc=self.loc)
        if nxc__dudnc is not None and nxc__dudnc.is_precise():
            ngbdg__zegb = fnty.copy(this=nxc__dudnc)
            typeinfer.propagate_refined_type(self.func, ngbdg__zegb)
    if not sig.return_type.is_precise():
        ymv__xsf = typevars[self.target]
        if ymv__xsf.defined:
            swh__rvozh = ymv__xsf.getone()
            if context.unify_pairs(swh__rvozh, sig.return_type) == swh__rvozh:
                sig = sig.replace(return_type=swh__rvozh)
    self.signature = sig
    self._add_refine_map(typeinfer, typevars, sig)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typeinfer.CallConstraint.resolve)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c78cd8ffc64b836a6a2ddf0362d481b52b9d380c5249920a87ff4da052ce081f':
        warnings.warn('numba.core.typeinfer.CallConstraint.resolve has changed'
            )
numba.core.typeinfer.CallConstraint.resolve = CallConstraint_resolve


def ForceLiteralArg__init__(self, arg_indices, fold_arguments=None, loc=
    None, file_infos=None):
    super(ForceLiteralArg, self).__init__(
        'Pseudo-exception to force literal arguments in the dispatcher',
        loc=loc)
    self.requested_args = frozenset(arg_indices)
    self.fold_arguments = fold_arguments
    if file_infos is None:
        self.file_infos = {}
    else:
        self.file_infos = file_infos


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b241d5e36a4cf7f4c73a7ad3238693612926606c7a278cad1978070b82fb55ef':
        warnings.warn('numba.core.errors.ForceLiteralArg.__init__ has changed')
numba.core.errors.ForceLiteralArg.__init__ = ForceLiteralArg__init__


def ForceLiteralArg_bind_fold_arguments(self, fold_arguments):
    e = ForceLiteralArg(self.requested_args, fold_arguments, loc=self.loc,
        file_infos=self.file_infos)
    return numba.core.utils.chain_exception(e, self)


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.
        bind_fold_arguments)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1e93cca558f7c604a47214a8f2ec33ee994104cb3e5051166f16d7cc9315141d':
        warnings.warn(
            'numba.core.errors.ForceLiteralArg.bind_fold_arguments has changed'
            )
numba.core.errors.ForceLiteralArg.bind_fold_arguments = (
    ForceLiteralArg_bind_fold_arguments)


def ForceLiteralArg_combine(self, other):
    if not isinstance(other, ForceLiteralArg):
        uvbks__zqns = '*other* must be a {} but got a {} instead'
        raise TypeError(uvbks__zqns.format(ForceLiteralArg, type(other)))
    return ForceLiteralArg(self.requested_args | other.requested_args, {**
        self.file_infos, **other.file_infos})


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.combine)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '49bf06612776f5d755c1c7d1c5eb91831a57665a8fed88b5651935f3bf33e899':
        warnings.warn('numba.core.errors.ForceLiteralArg.combine has changed')
numba.core.errors.ForceLiteralArg.combine = ForceLiteralArg_combine


def _get_global_type(self, gv):
    from bodo.utils.typing import FunctionLiteral
    ty = self._lookup_global(gv)
    if ty is not None:
        return ty
    if isinstance(gv, pytypes.ModuleType):
        return types.Module(gv)
    if isinstance(gv, pytypes.FunctionType):
        return FunctionLiteral(gv)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.context.BaseContext.
        _get_global_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8ffe6b81175d1eecd62a37639b5005514b4477d88f35f5b5395041ac8c945a4a':
        warnings.warn(
            'numba.core.typing.context.BaseContext._get_global_type has changed'
            )
numba.core.typing.context.BaseContext._get_global_type = _get_global_type


def _legalize_args(self, func_ir, args, kwargs, loc, func_globals,
    func_closures):
    from numba.core import sigutils
    from bodo.utils.transform import get_const_value_inner
    if args:
        raise errors.CompilerError(
            "objectmode context doesn't take any positional arguments")
    hnyjs__xmrw = {}

    def report_error(varname, msg, loc):
        raise errors.CompilerError(
            f'Error handling objmode argument {varname!r}. {msg}', loc=loc)
    for aewyp__jmy, rgjli__jydsh in kwargs.items():
        ogm__vvjs = None
        try:
            depd__whpb = ir.Var(ir.Scope(None, loc), ir_utils.mk_unique_var
                ('dummy'), loc)
            func_ir._definitions[depd__whpb.name] = [rgjli__jydsh]
            ogm__vvjs = get_const_value_inner(func_ir, depd__whpb)
            func_ir._definitions.pop(depd__whpb.name)
            if isinstance(ogm__vvjs, str):
                ogm__vvjs = sigutils._parse_signature_string(ogm__vvjs)
            if isinstance(ogm__vvjs, types.abstract._TypeMetaclass):
                raise BodoError(
                    f"""objmode type annotations require full data types, not just data type classes. For example, 'bodo.DataFrameType((bodo.float64[::1],), bodo.RangeIndexType(), ('A',))' is a valid data type but 'bodo.DataFrameType' is not.
Variable {aewyp__jmy} is annotated as type class {ogm__vvjs}."""
                    )
            assert isinstance(ogm__vvjs, types.Type)
            if isinstance(ogm__vvjs, (types.List, types.Set)):
                ogm__vvjs = ogm__vvjs.copy(reflected=False)
            hnyjs__xmrw[aewyp__jmy] = ogm__vvjs
        except BodoError as hmeej__ghyq:
            raise
        except:
            msg = (
                'The value must be a compile-time constant either as a non-local variable or an expression that refers to a Bodo type.'
                )
            if isinstance(ogm__vvjs, ir.UndefinedType):
                msg = f'not defined.'
                if isinstance(rgjli__jydsh, ir.Global):
                    msg = f'Global {rgjli__jydsh.name!r} is not defined.'
                if isinstance(rgjli__jydsh, ir.FreeVar):
                    msg = f'Freevar {rgjli__jydsh.name!r} is not defined.'
            if isinstance(rgjli__jydsh, ir.Expr
                ) and rgjli__jydsh.op == 'getattr':
                msg = 'Getattr cannot be resolved at compile-time.'
            report_error(varname=aewyp__jmy, msg=msg, loc=loc)
    for name, typ in hnyjs__xmrw.items():
        self._legalize_arg_type(name, typ, loc)
    return hnyjs__xmrw


if _check_numba_change:
    lines = inspect.getsource(numba.core.withcontexts._ObjModeContextType.
        _legalize_args)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '867c9ba7f1bcf438be56c38e26906bb551f59a99f853a9f68b71208b107c880e':
        warnings.warn(
            'numba.core.withcontexts._ObjModeContextType._legalize_args has changed'
            )
numba.core.withcontexts._ObjModeContextType._legalize_args = _legalize_args


def op_FORMAT_VALUE_byteflow(self, state, inst):
    flags = inst.arg
    if flags & 3 != 0:
        msg = 'str/repr/ascii conversion in f-strings not supported yet'
        raise errors.UnsupportedError(msg, loc=self.get_debug_loc(inst.lineno))
    format_spec = None
    if flags & 4 == 4:
        format_spec = state.pop()
    value = state.pop()
    fmtvar = state.make_temp()
    res = state.make_temp()
    state.append(inst, value=value, res=res, fmtvar=fmtvar, format_spec=
        format_spec)
    state.push(res)


def op_BUILD_STRING_byteflow(self, state, inst):
    hqvgt__cxm = inst.arg
    assert hqvgt__cxm > 0, 'invalid BUILD_STRING count'
    strings = list(reversed([state.pop() for _ in range(hqvgt__cxm)]))
    tmps = [state.make_temp() for _ in range(hqvgt__cxm - 1)]
    state.append(inst, strings=strings, tmps=tmps)
    state.push(tmps[-1])


numba.core.byteflow.TraceRunner.op_FORMAT_VALUE = op_FORMAT_VALUE_byteflow
numba.core.byteflow.TraceRunner.op_BUILD_STRING = op_BUILD_STRING_byteflow


def op_FORMAT_VALUE_interpreter(self, inst, value, res, fmtvar, format_spec):
    value = self.get(value)
    tkn__tgqtf = ir.Global('format', format, loc=self.loc)
    self.store(value=tkn__tgqtf, name=fmtvar)
    args = (value, self.get(format_spec)) if format_spec else (value,)
    gkc__snaac = ir.Expr.call(self.get(fmtvar), args, (), loc=self.loc)
    self.store(value=gkc__snaac, name=res)


def op_BUILD_STRING_interpreter(self, inst, strings, tmps):
    hqvgt__cxm = inst.arg
    assert hqvgt__cxm > 0, 'invalid BUILD_STRING count'
    sjalf__aua = self.get(strings[0])
    for other, dofo__lddkv in zip(strings[1:], tmps):
        other = self.get(other)
        ltsko__koq = ir.Expr.binop(operator.add, lhs=sjalf__aua, rhs=other,
            loc=self.loc)
        self.store(ltsko__koq, dofo__lddkv)
        sjalf__aua = self.get(dofo__lddkv)


numba.core.interpreter.Interpreter.op_FORMAT_VALUE = (
    op_FORMAT_VALUE_interpreter)
numba.core.interpreter.Interpreter.op_BUILD_STRING = (
    op_BUILD_STRING_interpreter)


def object_hasattr_string(self, obj, attr):
    from llvmlite.llvmpy.core import Type
    svi__xgwpq = self.context.insert_const_string(self.module, attr)
    fnty = Type.function(Type.int(), [self.pyobj, self.cstring])
    fn = self._get_function(fnty, name='PyObject_HasAttrString')
    return self.builder.call(fn, [obj, svi__xgwpq])


numba.core.pythonapi.PythonAPI.object_hasattr_string = object_hasattr_string


def _created_inlined_var_name(function_name, var_name):
    kaf__kcb = mk_unique_var(f'{var_name}')
    slano__gdvk = kaf__kcb.replace('<', '_').replace('>', '_')
    slano__gdvk = slano__gdvk.replace('.', '_').replace('$', '_v')
    return slano__gdvk


if _check_numba_change:
    lines = inspect.getsource(numba.core.inline_closurecall.
        _created_inlined_var_name)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '0d91aac55cd0243e58809afe9d252562f9ae2899cde1112cc01a46804e01821e':
        warnings.warn(
            'numba.core.inline_closurecall._created_inlined_var_name has changed'
            )
numba.core.inline_closurecall._created_inlined_var_name = (
    _created_inlined_var_name)


def resolve_number___call__(self, classty):
    import numpy as np
    from numba.core.typing.templates import make_callable_template
    ty = classty.instance_type

    def typer(val):
        if isinstance(val, (types.BaseTuple, types.Sequence)):
            fnty = self.context.resolve_value_type(np.array)
            sig = fnty.get_call_type(self.context, (val, types.DType(ty)), {})
            return sig.return_type
        elif isinstance(val, (types.Number, types.Boolean, types.IntEnumMember)
            ):
            return ty
        elif val == types.unicode_type:
            return ty
        elif isinstance(val, (types.NPDatetime, types.NPTimedelta)):
            if ty.bitwidth == 64:
                return ty
            else:
                msg = f'Cannot cast {val} to {ty} as {ty} is not 64 bits wide.'
                raise errors.TypingError(msg)
        elif isinstance(val, types.Array
            ) and val.ndim == 0 and val.dtype == ty:
            return ty
        else:
            msg = f'Casting {val} to {ty} directly is unsupported.'
            if isinstance(val, types.Array):
                msg += f" Try doing '<array>.astype(np.{ty})' instead"
            raise errors.TypingError(msg)
    return types.Function(make_callable_template(key=ty, typer=typer))


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.builtins.
        NumberClassAttribute.resolve___call__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'fdaf0c7d0820130481bb2bd922985257b9281b670f0bafffe10e51cabf0d5081':
        warnings.warn(
            'numba.core.typing.builtins.NumberClassAttribute.resolve___call__ has changed'
            )
numba.core.typing.builtins.NumberClassAttribute.resolve___call__ = (
    resolve_number___call__)


def on_assign(self, states, assign):
    if assign.target.name == states['varname']:
        scope = states['scope']
        czs__cwqz = states['defmap']
        if len(czs__cwqz) == 0:
            fzi__bgmn = assign.target
            numba.core.ssa._logger.debug('first assign: %s', fzi__bgmn)
            if fzi__bgmn.name not in scope.localvars:
                fzi__bgmn = scope.define(assign.target.name, loc=assign.loc)
        else:
            fzi__bgmn = scope.redefine(assign.target.name, loc=assign.loc)
        assign = ir.Assign(target=fzi__bgmn, value=assign.value, loc=assign.loc
            )
        czs__cwqz[states['label']].append(assign)
    return assign


if _check_numba_change:
    lines = inspect.getsource(numba.core.ssa._FreshVarHandler.on_assign)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '922c4f9807455f81600b794bbab36f9c6edfecfa83fda877bf85f465db7865e8':
        warnings.warn('_FreshVarHandler on_assign has changed')
numba.core.ssa._FreshVarHandler.on_assign = on_assign


def get_np_ufunc_typ_lst(func):
    from numba.core import typing
    ajr__yebz = []
    for aewyp__jmy, rgjli__jydsh in typing.npydecl.registry.globals:
        if aewyp__jmy == func:
            ajr__yebz.append(rgjli__jydsh)
    for aewyp__jmy, rgjli__jydsh in typing.templates.builtin_registry.globals:
        if aewyp__jmy == func:
            ajr__yebz.append(rgjli__jydsh)
    if len(ajr__yebz) == 0:
        raise RuntimeError('type for func ', func, ' not found')
    return ajr__yebz


def canonicalize_array_math(func_ir, typemap, calltypes, typingctx):
    import numpy
    from numba.core.ir_utils import arr_math, find_topo_order, mk_unique_var
    blocks = func_ir.blocks
    ive__xhi = {}
    dskzp__tthrj = find_topo_order(blocks)
    kfqfz__upmw = {}
    for jqsx__ndv in dskzp__tthrj:
        block = blocks[jqsx__ndv]
        bth__tev = []
        for stmt in block.body:
            if isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr):
                icj__rycwz = stmt.target.name
                kkv__cynaq = stmt.value
                if (kkv__cynaq.op == 'getattr' and kkv__cynaq.attr in
                    arr_math and isinstance(typemap[kkv__cynaq.value.name],
                    types.npytypes.Array)):
                    kkv__cynaq = stmt.value
                    cdfg__xij = kkv__cynaq.value
                    ive__xhi[icj__rycwz] = cdfg__xij
                    scope = cdfg__xij.scope
                    loc = cdfg__xij.loc
                    rkx__ufkzv = ir.Var(scope, mk_unique_var('$np_g_var'), loc)
                    typemap[rkx__ufkzv.name] = types.misc.Module(numpy)
                    ctagm__blyx = ir.Global('np', numpy, loc)
                    efjq__tkv = ir.Assign(ctagm__blyx, rkx__ufkzv, loc)
                    kkv__cynaq.value = rkx__ufkzv
                    bth__tev.append(efjq__tkv)
                    func_ir._definitions[rkx__ufkzv.name] = [ctagm__blyx]
                    func = getattr(numpy, kkv__cynaq.attr)
                    zhd__cyki = get_np_ufunc_typ_lst(func)
                    kfqfz__upmw[icj__rycwz] = zhd__cyki
                if (kkv__cynaq.op == 'call' and kkv__cynaq.func.name in
                    ive__xhi):
                    cdfg__xij = ive__xhi[kkv__cynaq.func.name]
                    gleuv__qzjf = calltypes.pop(kkv__cynaq)
                    nrev__saqck = gleuv__qzjf.args[:len(kkv__cynaq.args)]
                    puwu__etam = {name: typemap[rgjli__jydsh.name] for name,
                        rgjli__jydsh in kkv__cynaq.kws}
                    ctyt__tkqwt = kfqfz__upmw[kkv__cynaq.func.name]
                    hpnu__qiwgn = None
                    for llgey__qqcq in ctyt__tkqwt:
                        try:
                            hpnu__qiwgn = llgey__qqcq.get_call_type(typingctx,
                                [typemap[cdfg__xij.name]] + list(
                                nrev__saqck), puwu__etam)
                            typemap.pop(kkv__cynaq.func.name)
                            typemap[kkv__cynaq.func.name] = llgey__qqcq
                            calltypes[kkv__cynaq] = hpnu__qiwgn
                            break
                        except Exception as hmeej__ghyq:
                            pass
                    if hpnu__qiwgn is None:
                        raise TypeError(
                            f'No valid template found for {kkv__cynaq.func.name}'
                            )
                    kkv__cynaq.args = [cdfg__xij] + kkv__cynaq.args
            bth__tev.append(stmt)
        block.body = bth__tev


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.canonicalize_array_math)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b2200e9100613631cc554f4b640bc1181ba7cea0ece83630122d15b86941be2e':
        warnings.warn('canonicalize_array_math has changed')
numba.core.ir_utils.canonicalize_array_math = canonicalize_array_math
numba.parfors.parfor.canonicalize_array_math = canonicalize_array_math
numba.core.inline_closurecall.canonicalize_array_math = canonicalize_array_math


def _Numpy_Rules_ufunc_handle_inputs(cls, ufunc, args, kws):
    napg__ioyux = ufunc.nin
    pdji__pbuj = ufunc.nout
    wqs__azfp = ufunc.nargs
    assert wqs__azfp == napg__ioyux + pdji__pbuj
    if len(args) < napg__ioyux:
        msg = "ufunc '{0}': not enough arguments ({1} found, {2} required)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args),
            napg__ioyux))
    if len(args) > wqs__azfp:
        msg = "ufunc '{0}': too many arguments ({1} found, {2} maximum)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), wqs__azfp))
    args = [(a.as_array if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else a) for a in args]
    waxwf__jrj = [(a.ndim if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else 0) for a in args]
    levmr__fvnqe = max(waxwf__jrj)
    mdj__ukbe = args[napg__ioyux:]
    if not all(ftab__nlyb == levmr__fvnqe for ftab__nlyb in waxwf__jrj[
        napg__ioyux:]):
        msg = "ufunc '{0}' called with unsuitable explicit output arrays."
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(isinstance(nvy__bzoo, types.ArrayCompatible) and not
        isinstance(nvy__bzoo, types.Bytes) for nvy__bzoo in mdj__ukbe):
        msg = "ufunc '{0}' called with an explicit output that is not an array"
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(nvy__bzoo.mutable for nvy__bzoo in mdj__ukbe):
        msg = "ufunc '{0}' called with an explicit output that is read-only"
        raise TypingError(msg=msg.format(ufunc.__name__))
    ahjht__yrkj = [(x.dtype if isinstance(x, types.ArrayCompatible) and not
        isinstance(x, types.Bytes) else x) for x in args]
    jid__gjuh = None
    if levmr__fvnqe > 0 and len(mdj__ukbe) < ufunc.nout:
        jid__gjuh = 'C'
        exx__xcjdr = [(x.layout if isinstance(x, types.ArrayCompatible) and
            not isinstance(x, types.Bytes) else '') for x in args]
        if 'C' not in exx__xcjdr and 'F' in exx__xcjdr:
            jid__gjuh = 'F'
    return ahjht__yrkj, mdj__ukbe, levmr__fvnqe, jid__gjuh


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.npydecl.Numpy_rules_ufunc.
        _handle_inputs)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4b97c64ad9c3d50e082538795054f35cf6d2fe962c3ca40e8377a4601b344d5c':
        warnings.warn('Numpy_rules_ufunc._handle_inputs has changed')
numba.core.typing.npydecl.Numpy_rules_ufunc._handle_inputs = (
    _Numpy_Rules_ufunc_handle_inputs)
numba.np.ufunc.dufunc.npydecl.Numpy_rules_ufunc._handle_inputs = (
    _Numpy_Rules_ufunc_handle_inputs)


def DictType__init__(self, keyty, valty, initial_value=None):
    from numba.types import DictType, InitialValue, NoneType, Optional, Tuple, TypeRef, unliteral
    assert not isinstance(keyty, TypeRef)
    assert not isinstance(valty, TypeRef)
    keyty = unliteral(keyty)
    valty = unliteral(valty)
    if isinstance(keyty, (Optional, NoneType)):
        qefnj__xzjuw = 'Dict.key_type cannot be of type {}'
        raise TypingError(qefnj__xzjuw.format(keyty))
    if isinstance(valty, (Optional, NoneType)):
        qefnj__xzjuw = 'Dict.value_type cannot be of type {}'
        raise TypingError(qefnj__xzjuw.format(valty))
    self.key_type = keyty
    self.value_type = valty
    self.keyvalue_type = Tuple([keyty, valty])
    name = '{}[{},{}]<iv={}>'.format(self.__class__.__name__, keyty, valty,
        initial_value)
    super(DictType, self).__init__(name)
    InitialValue.__init__(self, initial_value)


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.containers.DictType.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '475acd71224bd51526750343246e064ff071320c0d10c17b8b8ac81d5070d094':
        warnings.warn('DictType.__init__ has changed')
numba.core.types.containers.DictType.__init__ = DictType__init__


def _legalize_arg_types(self, args):
    for vyuxe__bxxrr, a in enumerate(args, start=1):
        if isinstance(a, types.Dispatcher):
            msg = (
                'Does not support function type inputs into with-context for arg {}'
                )
            raise errors.TypingError(msg.format(vyuxe__bxxrr))


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.ObjModeLiftedWith.
        _legalize_arg_types)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4793f44ebc7da8843e8f298e08cd8a5428b4b84b89fd9d5c650273fdb8fee5ee':
        warnings.warn('ObjModeLiftedWith._legalize_arg_types has changed')
numba.core.dispatcher.ObjModeLiftedWith._legalize_arg_types = (
    _legalize_arg_types)


def _overload_template_get_impl(self, args, kws):
    cikj__rqp = self.context, tuple(args), tuple(kws.items())
    try:
        whfh__xmy, args = self._impl_cache[cikj__rqp]
        return whfh__xmy, args
    except KeyError as hmeej__ghyq:
        pass
    whfh__xmy, args = self._build_impl(cikj__rqp, args, kws)
    return whfh__xmy, args


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadFunctionTemplate._get_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4e27d07b214ca16d6e8ed88f70d886b6b095e160d8f77f8df369dd4ed2eb3fae':
        warnings.warn(
            'numba.core.typing.templates._OverloadFunctionTemplate._get_impl has changed'
            )
numba.core.typing.templates._OverloadFunctionTemplate._get_impl = (
    _overload_template_get_impl)


def remove_dead_parfor(parfor, lives, lives_n_aliases, arg_aliases,
    alias_map, func_ir, typemap):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    from numba.core.ir_utils import find_topo_order
    from numba.parfors.parfor import _add_liveness_return_block, _update_parfor_get_setitems, dummy_return_in_loop_body, get_index_var, remove_dead_parfor_recursive, simplify_parfor_body_CFG
    with dummy_return_in_loop_body(parfor.loop_body):
        kbs__zzz = find_topo_order(parfor.loop_body)
    qigk__cla = kbs__zzz[0]
    afe__riahn = {}
    _update_parfor_get_setitems(parfor.loop_body[qigk__cla].body, parfor.
        index_var, alias_map, afe__riahn, lives_n_aliases)
    rmu__emkw = set(afe__riahn.keys())
    for fnka__silo in kbs__zzz:
        if fnka__silo == qigk__cla:
            continue
        for stmt in parfor.loop_body[fnka__silo].body:
            if (isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.
                Expr) and stmt.value.op == 'getitem' and stmt.value.index.
                name == parfor.index_var.name):
                continue
            cjwuh__exo = set(rgjli__jydsh.name for rgjli__jydsh in stmt.
                list_vars())
            lzj__eck = cjwuh__exo & rmu__emkw
            for a in lzj__eck:
                afe__riahn.pop(a, None)
    for fnka__silo in kbs__zzz:
        if fnka__silo == qigk__cla:
            continue
        block = parfor.loop_body[fnka__silo]
        krlv__gjwj = afe__riahn.copy()
        _update_parfor_get_setitems(block.body, parfor.index_var, alias_map,
            krlv__gjwj, lives_n_aliases)
    blocks = parfor.loop_body.copy()
    jrfzg__cmy = max(blocks.keys())
    kno__etx, tuq__fkn = _add_liveness_return_block(blocks, lives_n_aliases,
        typemap)
    fve__fie = ir.Jump(kno__etx, ir.Loc('parfors_dummy', -1))
    blocks[jrfzg__cmy].body.append(fve__fie)
    gfvmn__tqnc = compute_cfg_from_blocks(blocks)
    xgl__xcp = compute_use_defs(blocks)
    wmxnd__xtl = compute_live_map(gfvmn__tqnc, blocks, xgl__xcp.usemap,
        xgl__xcp.defmap)
    alias_set = set(alias_map.keys())
    for jqsx__ndv, block in blocks.items():
        bth__tev = []
        kthp__hgwoh = {rgjli__jydsh.name for rgjli__jydsh in block.
            terminator.list_vars()}
        for tzza__zogk, pbdx__ewum in gfvmn__tqnc.successors(jqsx__ndv):
            kthp__hgwoh |= wmxnd__xtl[tzza__zogk]
        for stmt in reversed(block.body):
            qss__fyu = kthp__hgwoh & alias_set
            for rgjli__jydsh in qss__fyu:
                kthp__hgwoh |= alias_map[rgjli__jydsh]
            if (isinstance(stmt, (ir.StaticSetItem, ir.SetItem)) and 
                get_index_var(stmt).name == parfor.index_var.name and stmt.
                target.name not in kthp__hgwoh and stmt.target.name not in
                arg_aliases):
                continue
            elif isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
                ) and stmt.value.op == 'call':
                srq__awykq = guard(find_callname, func_ir, stmt.value)
                if srq__awykq == ('setna', 'bodo.libs.array_kernels'
                    ) and stmt.value.args[0
                    ].name not in kthp__hgwoh and stmt.value.args[0
                    ].name not in arg_aliases:
                    continue
            kthp__hgwoh |= {rgjli__jydsh.name for rgjli__jydsh in stmt.
                list_vars()}
            bth__tev.append(stmt)
        bth__tev.reverse()
        block.body = bth__tev
    typemap.pop(tuq__fkn.name)
    blocks[jrfzg__cmy].body.pop()

    def trim_empty_parfor_branches(parfor):
        oepzo__ipajf = False
        blocks = parfor.loop_body.copy()
        for jqsx__ndv, block in blocks.items():
            if len(block.body):
                gzd__qpgi = block.body[-1]
                if isinstance(gzd__qpgi, ir.Branch):
                    if len(blocks[gzd__qpgi.truebr].body) == 1 and len(blocks
                        [gzd__qpgi.falsebr].body) == 1:
                        pjlee__jbrd = blocks[gzd__qpgi.truebr].body[0]
                        fkbcg__kpkwo = blocks[gzd__qpgi.falsebr].body[0]
                        if isinstance(pjlee__jbrd, ir.Jump) and isinstance(
                            fkbcg__kpkwo, ir.Jump
                            ) and pjlee__jbrd.target == fkbcg__kpkwo.target:
                            parfor.loop_body[jqsx__ndv].body[-1] = ir.Jump(
                                pjlee__jbrd.target, gzd__qpgi.loc)
                            oepzo__ipajf = True
                    elif len(blocks[gzd__qpgi.truebr].body) == 1:
                        pjlee__jbrd = blocks[gzd__qpgi.truebr].body[0]
                        if isinstance(pjlee__jbrd, ir.Jump
                            ) and pjlee__jbrd.target == gzd__qpgi.falsebr:
                            parfor.loop_body[jqsx__ndv].body[-1] = ir.Jump(
                                pjlee__jbrd.target, gzd__qpgi.loc)
                            oepzo__ipajf = True
                    elif len(blocks[gzd__qpgi.falsebr].body) == 1:
                        fkbcg__kpkwo = blocks[gzd__qpgi.falsebr].body[0]
                        if isinstance(fkbcg__kpkwo, ir.Jump
                            ) and fkbcg__kpkwo.target == gzd__qpgi.truebr:
                            parfor.loop_body[jqsx__ndv].body[-1] = ir.Jump(
                                fkbcg__kpkwo.target, gzd__qpgi.loc)
                            oepzo__ipajf = True
        return oepzo__ipajf
    oepzo__ipajf = True
    while oepzo__ipajf:
        """
        Process parfor body recursively.
        Note that this is the only place in this function that uses the
        argument lives instead of lives_n_aliases.  The former does not
        include the aliases of live variables but only the live variable
        names themselves.  See a comment in this function for how that
        is used.
        """
        remove_dead_parfor_recursive(parfor, lives, arg_aliases, alias_map,
            func_ir, typemap)
        simplify_parfor_body_CFG(func_ir.blocks)
        oepzo__ipajf = trim_empty_parfor_branches(parfor)
    xiqab__gion = len(parfor.init_block.body) == 0
    for block in parfor.loop_body.values():
        xiqab__gion &= len(block.body) == 0
    if xiqab__gion:
        return None
    return parfor


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.remove_dead_parfor)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1c9b008a7ead13e988e1efe67618d8f87f0b9f3d092cc2cd6bfcd806b1fdb859':
        warnings.warn('remove_dead_parfor has changed')
numba.parfors.parfor.remove_dead_parfor = remove_dead_parfor
numba.core.ir_utils.remove_dead_extensions[numba.parfors.parfor.Parfor
    ] = remove_dead_parfor


def simplify_parfor_body_CFG(blocks):
    from numba.core.analysis import compute_cfg_from_blocks
    from numba.core.ir_utils import simplify_CFG
    from numba.parfors.parfor import Parfor
    bhm__frlg = 0
    for block in blocks.values():
        for stmt in block.body:
            if isinstance(stmt, Parfor):
                bhm__frlg += 1
                parfor = stmt
                ucs__eoxj = parfor.loop_body[max(parfor.loop_body.keys())]
                scope = ucs__eoxj.scope
                loc = ir.Loc('parfors_dummy', -1)
                wnnoa__fdpb = ir.Var(scope, mk_unique_var('$const'), loc)
                ucs__eoxj.body.append(ir.Assign(ir.Const(0, loc),
                    wnnoa__fdpb, loc))
                ucs__eoxj.body.append(ir.Return(wnnoa__fdpb, loc))
                gfvmn__tqnc = compute_cfg_from_blocks(parfor.loop_body)
                for htje__anb in gfvmn__tqnc.dead_nodes():
                    del parfor.loop_body[htje__anb]
                parfor.loop_body = simplify_CFG(parfor.loop_body)
                ucs__eoxj = parfor.loop_body[max(parfor.loop_body.keys())]
                ucs__eoxj.body.pop()
                ucs__eoxj.body.pop()
                simplify_parfor_body_CFG(parfor.loop_body)
    return bhm__frlg


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.simplify_parfor_body_CFG)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '437ae96a5e8ec64a2b69a4f23ba8402a1d170262a5400aa0aa7bfe59e03bf726':
        warnings.warn('simplify_parfor_body_CFG has changed')
numba.parfors.parfor.simplify_parfor_body_CFG = simplify_parfor_body_CFG


def _lifted_compile(self, sig):
    import numba.core.event as ev
    from numba.core import compiler, sigutils
    from numba.core.compiler_lock import global_compiler_lock
    from numba.core.ir_utils import remove_dels
    with ExitStack() as scope:
        cres = None

        def cb_compiler(dur):
            if cres is not None:
                self._callback_add_compiler_timer(dur, cres)

        def cb_llvm(dur):
            if cres is not None:
                self._callback_add_llvm_timer(dur, cres)
        scope.enter_context(ev.install_timer('numba:compiler_lock',
            cb_compiler))
        scope.enter_context(ev.install_timer('numba:llvm_lock', cb_llvm))
        scope.enter_context(global_compiler_lock)
        with self._compiling_counter:
            flags = self.flags
            args, return_type = sigutils.normalize_signature(sig)
            rdcqz__eflwo = self.overloads.get(tuple(args))
            if rdcqz__eflwo is not None:
                return rdcqz__eflwo.entry_point
            self._pre_compile(args, return_type, flags)
            roasy__qek = self.func_ir
            suv__zni = dict(dispatcher=self, args=args, return_type=return_type
                )
            with ev.trigger_event('numba:compile', data=suv__zni):
                cres = compiler.compile_ir(typingctx=self.typingctx,
                    targetctx=self.targetctx, func_ir=roasy__qek, args=args,
                    return_type=return_type, flags=flags, locals=self.
                    locals, lifted=(), lifted_from=self.lifted_from,
                    is_lifted_loop=True)
                if cres.typing_error is not None and not flags.enable_pyobject:
                    raise cres.typing_error
                self.add_overload(cres)
            remove_dels(self.func_ir.blocks)
            return cres.entry_point


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.LiftedCode.compile)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1351ebc5d8812dc8da167b30dad30eafb2ca9bf191b49aaed6241c21e03afff1':
        warnings.warn('numba.core.dispatcher.LiftedCode.compile has changed')
numba.core.dispatcher.LiftedCode.compile = _lifted_compile


def compile_ir(typingctx, targetctx, func_ir, args, return_type, flags,
    locals, lifted=(), lifted_from=None, is_lifted_loop=False, library=None,
    pipeline_class=Compiler):
    if is_lifted_loop:
        juaa__oyr = copy.deepcopy(flags)
        juaa__oyr.no_rewrites = True

        def compile_local(the_ir, the_flags):
            tbwz__vho = pipeline_class(typingctx, targetctx, library, args,
                return_type, the_flags, locals)
            return tbwz__vho.compile_ir(func_ir=the_ir, lifted=lifted,
                lifted_from=lifted_from)
        xcfkg__nmf = compile_local(func_ir, juaa__oyr)
        kpind__ikrrs = None
        if not flags.no_rewrites:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', errors.NumbaWarning)
                try:
                    kpind__ikrrs = compile_local(func_ir, flags)
                except Exception as hmeej__ghyq:
                    pass
        if kpind__ikrrs is not None:
            cres = kpind__ikrrs
        else:
            cres = xcfkg__nmf
        return cres
    else:
        tbwz__vho = pipeline_class(typingctx, targetctx, library, args,
            return_type, flags, locals)
        return tbwz__vho.compile_ir(func_ir=func_ir, lifted=lifted,
            lifted_from=lifted_from)


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.compile_ir)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c48ce5493f4c43326e8cbdd46f3ea038b2b9045352d9d25894244798388e5e5b':
        warnings.warn('numba.core.compiler.compile_ir has changed')
numba.core.compiler.compile_ir = compile_ir


def make_constant_array(self, builder, typ, ary):
    import math
    from llvmlite import ir as lir
    from llvmlite.llvmpy.core import Constant, Type
    qnisf__vhzup = self.get_data_type(typ.dtype)
    rud__fgd = 10 ** 7
    if self.allow_dynamic_globals and (typ.layout not in 'FC' or ary.nbytes >
        rud__fgd):
        snit__kfskh = ary.ctypes.data
        kiet__fdwpz = self.add_dynamic_addr(builder, snit__kfskh, info=str(
            type(snit__kfskh)))
        fpt__krn = self.add_dynamic_addr(builder, id(ary), info=str(type(ary)))
        self.global_arrays.append(ary)
    else:
        plxq__aqd = ary.flatten(order=typ.layout)
        if isinstance(typ.dtype, (types.NPDatetime, types.NPTimedelta)):
            plxq__aqd = plxq__aqd.view('int64')
        tbkvh__ymbl = Constant.array(Type.int(8), bytearray(plxq__aqd.data))
        kiet__fdwpz = cgutils.global_constant(builder, '.const.array.data',
            tbkvh__ymbl)
        kiet__fdwpz.align = self.get_abi_alignment(qnisf__vhzup)
        fpt__krn = None
    lvav__xhoqr = self.get_value_type(types.intp)
    erp__brpd = [self.get_constant(types.intp, pfr__ryly) for pfr__ryly in
        ary.shape]
    raxha__kuxxm = Constant.array(lvav__xhoqr, erp__brpd)
    ihfa__ffn = [self.get_constant(types.intp, pfr__ryly) for pfr__ryly in
        ary.strides]
    dgtss__lnt = Constant.array(lvav__xhoqr, ihfa__ffn)
    njdo__pnx = self.get_constant(types.intp, ary.dtype.itemsize)
    kyq__obbs = self.get_constant(types.intp, math.prod(ary.shape))
    return lir.Constant.literal_struct([self.get_constant_null(types.
        MemInfoPointer(typ.dtype)), self.get_constant_null(types.pyobject),
        kyq__obbs, njdo__pnx, kiet__fdwpz.bitcast(self.get_value_type(types
        .CPointer(typ.dtype))), raxha__kuxxm, dgtss__lnt])


if _check_numba_change:
    lines = inspect.getsource(numba.core.base.BaseContext.make_constant_array)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5721b5360b51f782f79bd794f7bf4d48657911ecdc05c30db22fd55f15dad821':
        warnings.warn(
            'numba.core.base.BaseContext.make_constant_array has changed')
numba.core.base.BaseContext.make_constant_array = make_constant_array


def _define_atomic_inc_dec(module, op, ordering):
    from llvmlite import ir as lir
    from numba.core.runtime.nrtdynmod import _word_type
    knygh__xgs = lir.FunctionType(_word_type, [_word_type.as_pointer()])
    vyent__wxjh = lir.Function(module, knygh__xgs, name='nrt_atomic_{0}'.
        format(op))
    [vvv__qpb] = vyent__wxjh.args
    upae__vekf = vyent__wxjh.append_basic_block()
    builder = lir.IRBuilder(upae__vekf)
    lvrq__jugcs = lir.Constant(_word_type, 1)
    if False:
        rgh__uhf = builder.atomic_rmw(op, vvv__qpb, lvrq__jugcs, ordering=
            ordering)
        res = getattr(builder, op)(rgh__uhf, lvrq__jugcs)
        builder.ret(res)
    else:
        rgh__uhf = builder.load(vvv__qpb)
        teao__gkxk = getattr(builder, op)(rgh__uhf, lvrq__jugcs)
        mma__kzfu = builder.icmp_signed('!=', rgh__uhf, lir.Constant(
            rgh__uhf.type, -1))
        with cgutils.if_likely(builder, mma__kzfu):
            builder.store(teao__gkxk, vvv__qpb)
        builder.ret(teao__gkxk)
    return vyent__wxjh


if _check_numba_change:
    lines = inspect.getsource(numba.core.runtime.nrtdynmod.
        _define_atomic_inc_dec)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '9cc02c532b2980b6537b702f5608ea603a1ff93c6d3c785ae2cf48bace273f48':
        warnings.warn(
            'numba.core.runtime.nrtdynmod._define_atomic_inc_dec has changed')
numba.core.runtime.nrtdynmod._define_atomic_inc_dec = _define_atomic_inc_dec


def NativeLowering_run_pass(self, state):
    from llvmlite import binding as llvm
    from numba.core import funcdesc, lowering
    from numba.core.typed_passes import fallback_context
    if state.library is None:
        nterh__tdfq = state.targetctx.codegen()
        state.library = nterh__tdfq.create_library(state.func_id.func_qualname)
        state.library.enable_object_caching()
    library = state.library
    targetctx = state.targetctx
    avsnp__pfhoe = state.func_ir
    typemap = state.typemap
    lzh__iacbh = state.return_type
    calltypes = state.calltypes
    flags = state.flags
    sjzh__bmuk = state.metadata
    bvlvm__jjo = llvm.passmanagers.dump_refprune_stats()
    msg = 'Function %s failed at nopython mode lowering' % (state.func_id.
        func_name,)
    with fallback_context(state, msg):
        sjkzc__nwwrf = (funcdesc.PythonFunctionDescriptor.
            from_specialized_function(avsnp__pfhoe, typemap, lzh__iacbh,
            calltypes, mangler=targetctx.mangler, inline=flags.forceinline,
            noalias=flags.noalias, abi_tags=[flags.get_mangle_string()]))
        targetctx.global_arrays = []
        with targetctx.push_code_library(library):
            ipwh__pfv = lowering.Lower(targetctx, library, sjkzc__nwwrf,
                avsnp__pfhoe, metadata=sjzh__bmuk)
            ipwh__pfv.lower()
            if not flags.no_cpython_wrapper:
                ipwh__pfv.create_cpython_wrapper(flags.release_gil)
            if not flags.no_cfunc_wrapper:
                for t in state.args:
                    if isinstance(t, (types.Omitted, types.Generator)):
                        break
                else:
                    if isinstance(lzh__iacbh, (types.Optional, types.Generator)
                        ):
                        pass
                    else:
                        ipwh__pfv.create_cfunc_wrapper()
            sxik__hrm = ipwh__pfv.env
            bvl__fgp = ipwh__pfv.call_helper
            del ipwh__pfv
        from numba.core.compiler import _LowerResult
        if flags.no_compile:
            state['cr'] = _LowerResult(sjkzc__nwwrf, bvl__fgp, cfunc=None,
                env=sxik__hrm)
        else:
            tnpog__hjk = targetctx.get_executable(library, sjkzc__nwwrf,
                sxik__hrm)
            targetctx.insert_user_function(tnpog__hjk, sjkzc__nwwrf, [library])
            state['cr'] = _LowerResult(sjkzc__nwwrf, bvl__fgp, cfunc=
                tnpog__hjk, env=sxik__hrm)
        sjzh__bmuk['global_arrs'] = targetctx.global_arrays
        targetctx.global_arrays = []
        makap__siqyn = llvm.passmanagers.dump_refprune_stats()
        sjzh__bmuk['prune_stats'] = makap__siqyn - bvlvm__jjo
        sjzh__bmuk['llvm_pass_timings'] = library.recorded_timings
    return True


if _check_numba_change:
    lines = inspect.getsource(numba.core.typed_passes.NativeLowering.run_pass)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a777ce6ce1bb2b1cbaa3ac6c2c0e2adab69a9c23888dff5f1cbb67bfb176b5de':
        warnings.warn(
            'numba.core.typed_passes.NativeLowering.run_pass has changed')
numba.core.typed_passes.NativeLowering.run_pass = NativeLowering_run_pass


def _python_list_to_native(typ, obj, c, size, listptr, errorptr):
    from llvmlite import ir as lir
    from numba.core.boxing import _NumbaTypeHelper
    from numba.cpython import listobj

    def check_element_type(nth, itemobj, expected_typobj):
        avwkb__mhasj = nth.typeof(itemobj)
        with c.builder.if_then(cgutils.is_null(c.builder, avwkb__mhasj),
            likely=False):
            c.builder.store(cgutils.true_bit, errorptr)
            loop.do_break()
        tpeaz__xutti = c.builder.icmp_signed('!=', avwkb__mhasj,
            expected_typobj)
        if not isinstance(typ.dtype, types.Optional):
            with c.builder.if_then(tpeaz__xutti, likely=False):
                c.builder.store(cgutils.true_bit, errorptr)
                c.pyapi.err_format('PyExc_TypeError',
                    "can't unbox heterogeneous list: %S != %S",
                    expected_typobj, avwkb__mhasj)
                c.pyapi.decref(avwkb__mhasj)
                loop.do_break()
        c.pyapi.decref(avwkb__mhasj)
    gpeg__pdh, list = listobj.ListInstance.allocate_ex(c.context, c.builder,
        typ, size)
    with c.builder.if_else(gpeg__pdh, likely=True) as (if_ok, if_not_ok):
        with if_ok:
            list.size = size
            erqy__dge = lir.Constant(size.type, 0)
            with c.builder.if_then(c.builder.icmp_signed('>', size,
                erqy__dge), likely=True):
                with _NumbaTypeHelper(c) as nth:
                    expected_typobj = nth.typeof(c.pyapi.list_getitem(obj,
                        erqy__dge))
                    with cgutils.for_range(c.builder, size) as loop:
                        itemobj = c.pyapi.list_getitem(obj, loop.index)
                        check_element_type(nth, itemobj, expected_typobj)
                        kkvhw__kkq = c.unbox(typ.dtype, itemobj)
                        with c.builder.if_then(kkvhw__kkq.is_error, likely=
                            False):
                            c.builder.store(cgutils.true_bit, errorptr)
                            loop.do_break()
                        list.setitem(loop.index, kkvhw__kkq.value, incref=False
                            )
                    c.pyapi.decref(expected_typobj)
            if typ.reflected:
                list.parent = obj
            with c.builder.if_then(c.builder.not_(c.builder.load(errorptr)),
                likely=False):
                c.pyapi.object_set_private_data(obj, list.meminfo)
            list.set_dirty(False)
            c.builder.store(list.value, listptr)
        with if_not_ok:
            c.builder.store(cgutils.true_bit, errorptr)
    with c.builder.if_then(c.builder.load(errorptr)):
        c.context.nrt.decref(c.builder, typ, list.value)


if _check_numba_change:
    lines = inspect.getsource(numba.core.boxing._python_list_to_native)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f8e546df8b07adfe74a16b6aafb1d4fddbae7d3516d7944b3247cc7c9b7ea88a':
        warnings.warn('numba.core.boxing._python_list_to_native has changed')
numba.core.boxing._python_list_to_native = _python_list_to_native


def make_string_from_constant(context, builder, typ, literal_string):
    from llvmlite import ir as lir
    from numba.cpython.hashing import _Py_hash_t
    from numba.cpython.unicode import compile_time_get_string_data
    jwt__wntz, lzty__znfw, eocl__itj, ohlrb__yfj, cvx__foe = (
        compile_time_get_string_data(literal_string))
    lnjb__azfm = builder.module
    gv = context.insert_const_bytes(lnjb__azfm, jwt__wntz)
    return lir.Constant.literal_struct([gv, context.get_constant(types.intp,
        lzty__znfw), context.get_constant(types.int32, eocl__itj), context.
        get_constant(types.uint32, ohlrb__yfj), context.get_constant(
        _Py_hash_t, -1), context.get_constant_null(types.MemInfoPointer(
        types.voidptr)), context.get_constant_null(types.pyobject)])


if _check_numba_change:
    lines = inspect.getsource(numba.cpython.unicode.make_string_from_constant)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '525bd507383e06152763e2f046dae246cd60aba027184f50ef0fc9a80d4cd7fa':
        warnings.warn(
            'numba.cpython.unicode.make_string_from_constant has changed')
numba.cpython.unicode.make_string_from_constant = make_string_from_constant


def parse_shape(shape):
    xlrb__qqeha = None
    if isinstance(shape, types.Integer):
        xlrb__qqeha = 1
    elif isinstance(shape, (types.Tuple, types.UniTuple)):
        if all(isinstance(pfr__ryly, (types.Integer, types.IntEnumMember)) for
            pfr__ryly in shape):
            xlrb__qqeha = len(shape)
    return xlrb__qqeha


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.npydecl.parse_shape)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'e62e3ff09d36df5ac9374055947d6a8be27160ce32960d3ef6cb67f89bd16429':
        warnings.warn('numba.core.typing.npydecl.parse_shape has changed')
numba.core.typing.npydecl.parse_shape = parse_shape


def _get_names(self, obj):
    if isinstance(obj, ir.Var) or isinstance(obj, str):
        name = obj if isinstance(obj, str) else obj.name
        if name not in self.typemap:
            return name,
        typ = self.typemap[name]
        if isinstance(typ, (types.BaseTuple, types.ArrayCompatible)):
            xlrb__qqeha = typ.ndim if isinstance(typ, types.ArrayCompatible
                ) else len(typ)
            if xlrb__qqeha == 0:
                return name,
            else:
                return tuple('{}#{}'.format(name, vyuxe__bxxrr) for
                    vyuxe__bxxrr in range(xlrb__qqeha))
        else:
            return name,
    elif isinstance(obj, ir.Const):
        if isinstance(obj.value, tuple):
            return obj.value
        else:
            return obj.value,
    elif isinstance(obj, tuple):

        def get_names(x):
            bmipp__azbqd = self._get_names(x)
            if len(bmipp__azbqd) != 0:
                return bmipp__azbqd[0]
            return bmipp__azbqd
        return tuple(get_names(x) for x in obj)
    elif isinstance(obj, int):
        return obj,
    return ()


def get_equiv_const(self, obj):
    bmipp__azbqd = self._get_names(obj)
    if len(bmipp__azbqd) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_const(bmipp__azbqd[0])


def get_equiv_set(self, obj):
    bmipp__azbqd = self._get_names(obj)
    if len(bmipp__azbqd) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_set(bmipp__azbqd[0])


if _check_numba_change:
    for name, orig, new, hash in ((
        'numba.parfors.array_analysis.ShapeEquivSet._get_names', numba.
        parfors.array_analysis.ShapeEquivSet._get_names, _get_names,
        '8c9bf136109028d5445fd0a82387b6abeb70c23b20b41e2b50c34ba5359516ee'),
        ('numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const',
        numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const,
        get_equiv_const,
        'bef410ca31a9e29df9ee74a4a27d339cc332564e4a237828b8a4decf625ce44e'),
        ('numba.parfors.array_analysis.ShapeEquivSet.get_equiv_set', numba.
        parfors.array_analysis.ShapeEquivSet.get_equiv_set, get_equiv_set,
        'ec936d340c488461122eb74f28a28b88227cb1f1bca2b9ba3c19258cfe1eb40a')):
        lines = inspect.getsource(orig)
        if hashlib.sha256(lines.encode()).hexdigest() != hash:
            warnings.warn(f'{name} has changed')
numba.parfors.array_analysis.ShapeEquivSet._get_names = _get_names
numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const = get_equiv_const
numba.parfors.array_analysis.ShapeEquivSet.get_equiv_set = get_equiv_set


def raise_on_unsupported_feature(func_ir, typemap):
    import numpy
    blglp__pqbef = []
    for vili__xqwrk in func_ir.arg_names:
        if vili__xqwrk in typemap and isinstance(typemap[vili__xqwrk],
            types.containers.UniTuple) and typemap[vili__xqwrk].count > 1000:
            msg = (
                """Tuple '{}' length must be smaller than 1000.
Large tuples lead to the generation of a prohibitively large LLVM IR which causes excessive memory pressure and large compile times.
As an alternative, the use of a 'list' is recommended in place of a 'tuple' as lists do not suffer from this problem."""
                .format(vili__xqwrk))
            raise errors.UnsupportedError(msg, func_ir.loc)
    for ldu__wsv in func_ir.blocks.values():
        for stmt in ldu__wsv.find_insts(ir.Assign):
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'make_function':
                    val = stmt.value
                    jln__bcktv = getattr(val, 'code', None)
                    if jln__bcktv is not None:
                        if getattr(val, 'closure', None) is not None:
                            sahez__klule = (
                                '<creating a function from a closure>')
                            ltsko__koq = ''
                        else:
                            sahez__klule = jln__bcktv.co_name
                            ltsko__koq = '(%s) ' % sahez__klule
                    else:
                        sahez__klule = '<could not ascertain use case>'
                        ltsko__koq = ''
                    msg = (
                        'Numba encountered the use of a language feature it does not support in this context: %s (op code: make_function not supported). If the feature is explicitly supported it is likely that the result of the expression %sis being used in an unsupported manner.'
                         % (sahez__klule, ltsko__koq))
                    raise errors.UnsupportedError(msg, stmt.value.loc)
            if isinstance(stmt.value, (ir.Global, ir.FreeVar)):
                val = stmt.value
                val = getattr(val, 'value', None)
                if val is None:
                    continue
                vetxv__pyib = False
                if isinstance(val, pytypes.FunctionType):
                    vetxv__pyib = val in {numba.gdb, numba.gdb_init}
                if not vetxv__pyib:
                    vetxv__pyib = getattr(val, '_name', '') == 'gdb_internal'
                if vetxv__pyib:
                    blglp__pqbef.append(stmt.loc)
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'getattr' and stmt.value.attr == 'view':
                    var = stmt.value.value.name
                    if isinstance(typemap[var], types.Array):
                        continue
                    wzbn__cxz = func_ir.get_definition(var)
                    nqs__dpbkk = guard(find_callname, func_ir, wzbn__cxz)
                    if nqs__dpbkk and nqs__dpbkk[1] == 'numpy':
                        ty = getattr(numpy, nqs__dpbkk[0])
                        if numpy.issubdtype(ty, numpy.integer
                            ) or numpy.issubdtype(ty, numpy.floating):
                            continue
                    dmkjd__xcfu = '' if var.startswith('$'
                        ) else "'{}' ".format(var)
                    raise TypingError(
                        "'view' can only be called on NumPy dtypes, try wrapping the variable {}with 'np.<dtype>()'"
                        .format(dmkjd__xcfu), loc=stmt.loc)
            if isinstance(stmt.value, ir.Global):
                ty = typemap[stmt.target.name]
                msg = (
                    "The use of a %s type, assigned to variable '%s' in globals, is not supported as globals are considered compile-time constants and there is no known way to compile a %s type as a constant."
                    )
                if getattr(ty, 'reflected', False) or isinstance(ty, types.
                    ListType):
                    raise TypingError(msg % (ty, stmt.value.name, ty), loc=
                        stmt.loc)
            if isinstance(stmt.value, ir.Yield) and not func_ir.is_generator:
                msg = 'The use of generator expressions is unsupported.'
                raise errors.UnsupportedError(msg, loc=stmt.loc)


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.raise_on_unsupported_feature)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'eca43ce27128a243039d2b20d5da0cb8823403911814135b9b74f2b6549daf3d':
        warnings.warn(
            'numba.core.ir_utils.raise_on_unsupported_feature has changed')
numba.core.ir_utils.raise_on_unsupported_feature = raise_on_unsupported_feature
numba.core.typed_passes.raise_on_unsupported_feature = (
    raise_on_unsupported_feature)


@typeof_impl.register(dict)
def _typeof_dict(val, c):
    if len(val) == 0:
        raise ValueError('Cannot type empty dict')
    aewyp__jmy, rgjli__jydsh = next(iter(val.items()))
    zwz__pmtn = typeof_impl(aewyp__jmy, c)
    ues__spr = typeof_impl(rgjli__jydsh, c)
    if zwz__pmtn is None or ues__spr is None:
        raise ValueError(
            f'Cannot type dict element type {type(aewyp__jmy)}, {type(rgjli__jydsh)}'
            )
    return types.DictType(zwz__pmtn, ues__spr)


def unbox_dicttype(typ, val, c):
    from llvmlite import ir as lir
    from numba.typed import dictobject
    from numba.typed.typeddict import Dict
    context = c.context
    ibn__errcu = cgutils.alloca_once_value(c.builder, val)
    ghth__zbzwc = c.pyapi.object_hasattr_string(val, '_opaque')
    auu__tgyyh = c.builder.icmp_unsigned('==', ghth__zbzwc, lir.Constant(
        ghth__zbzwc.type, 0))
    jct__tjksl = typ.key_type
    bma__xqy = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(jct__tjksl, bma__xqy)

    def copy_dict(out_dict, in_dict):
        for aewyp__jmy, rgjli__jydsh in in_dict.items():
            out_dict[aewyp__jmy] = rgjli__jydsh
    with c.builder.if_then(auu__tgyyh):
        wjn__nuy = c.pyapi.unserialize(c.pyapi.serialize_object(make_dict))
        budf__nsq = c.pyapi.call_function_objargs(wjn__nuy, [])
        vsnod__yqx = c.pyapi.unserialize(c.pyapi.serialize_object(copy_dict))
        c.pyapi.call_function_objargs(vsnod__yqx, [budf__nsq, val])
        c.builder.store(budf__nsq, ibn__errcu)
    val = c.builder.load(ibn__errcu)
    jbqz__fsnpx = c.pyapi.unserialize(c.pyapi.serialize_object(Dict))
    sdo__enb = c.pyapi.object_type(val)
    wmft__ypx = c.builder.icmp_unsigned('==', sdo__enb, jbqz__fsnpx)
    with c.builder.if_else(wmft__ypx) as (then, orelse):
        with then:
            xwe__uaj = c.pyapi.object_getattr_string(val, '_opaque')
            ndhh__pkpt = types.MemInfoPointer(types.voidptr)
            kkvhw__kkq = c.unbox(ndhh__pkpt, xwe__uaj)
            mi = kkvhw__kkq.value
            deg__ewxm = ndhh__pkpt, typeof(typ)

            def convert(mi, typ):
                return dictobject._from_meminfo(mi, typ)
            sig = signature(typ, *deg__ewxm)
            vmyw__vcitk = context.get_constant_null(deg__ewxm[1])
            args = mi, vmyw__vcitk
            fxgwi__jpkfm, evk__nfd = c.pyapi.call_jit_code(convert, sig, args)
            c.context.nrt.decref(c.builder, typ, evk__nfd)
            c.pyapi.decref(xwe__uaj)
            xhkyx__plrir = c.builder.basic_block
        with orelse:
            c.pyapi.err_format('PyExc_TypeError',
                "can't unbox a %S as a %S", sdo__enb, jbqz__fsnpx)
            stvp__cwd = c.builder.basic_block
    gno__ljgc = c.builder.phi(evk__nfd.type)
    xufz__eisw = c.builder.phi(fxgwi__jpkfm.type)
    gno__ljgc.add_incoming(evk__nfd, xhkyx__plrir)
    gno__ljgc.add_incoming(evk__nfd.type(None), stvp__cwd)
    xufz__eisw.add_incoming(fxgwi__jpkfm, xhkyx__plrir)
    xufz__eisw.add_incoming(cgutils.true_bit, stvp__cwd)
    c.pyapi.decref(jbqz__fsnpx)
    c.pyapi.decref(sdo__enb)
    with c.builder.if_then(auu__tgyyh):
        c.pyapi.decref(val)
    return NativeValue(gno__ljgc, is_error=xufz__eisw)


import numba.typed.typeddict
if _check_numba_change:
    lines = inspect.getsource(numba.core.pythonapi._unboxers.functions[
        numba.core.types.DictType])
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5f6f183b94dc57838538c668a54c2476576c85d8553843f3219f5162c61e7816':
        warnings.warn('unbox_dicttype has changed')
numba.core.pythonapi._unboxers.functions[types.DictType] = unbox_dicttype
