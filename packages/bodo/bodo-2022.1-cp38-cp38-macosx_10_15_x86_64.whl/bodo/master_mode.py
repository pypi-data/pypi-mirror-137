import gc
import inspect
import sys
import types as pytypes
import bodo
master_mode_on = False
MASTER_RANK = 0


class MasterModeDispatcher(object):

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def __call__(self, *args, **kwargs):
        assert bodo.get_rank() == MASTER_RANK
        return master_wrapper(self.dispatcher, *args, **kwargs)

    def __getstate__(self):
        assert bodo.get_rank() == MASTER_RANK
        return self.dispatcher.py_func

    def __setstate__(self, state):
        assert bodo.get_rank() != MASTER_RANK
        ogqwy__papph = state
        kuet__kpvx = inspect.getsourcelines(ogqwy__papph)[0][0]
        assert kuet__kpvx.startswith('@bodo.jit') or kuet__kpvx.startswith(
            '@jit')
        dgeb__pegu = eval(kuet__kpvx[1:])
        self.dispatcher = dgeb__pegu(ogqwy__papph)


def worker_loop():
    assert bodo.get_rank() != MASTER_RANK
    eam__ciifs = MPI.COMM_WORLD
    while True:
        tunzc__krf = eam__ciifs.bcast(None, root=MASTER_RANK)
        if tunzc__krf[0] == 'exec':
            ogqwy__papph = pickle.loads(tunzc__krf[1])
            for ufel__kmvi, bgfr__ixay in list(ogqwy__papph.__globals__.items()
                ):
                if isinstance(bgfr__ixay, MasterModeDispatcher):
                    ogqwy__papph.__globals__[ufel__kmvi
                        ] = bgfr__ixay.dispatcher
            if ogqwy__papph.__module__ not in sys.modules:
                sys.modules[ogqwy__papph.__module__] = pytypes.ModuleType(
                    ogqwy__papph.__module__)
            kuet__kpvx = inspect.getsourcelines(ogqwy__papph)[0][0]
            assert kuet__kpvx.startswith('@bodo.jit') or kuet__kpvx.startswith(
                '@jit')
            dgeb__pegu = eval(kuet__kpvx[1:])
            func = dgeb__pegu(ogqwy__papph)
            jhbz__mmh = tunzc__krf[2]
            siivi__rcq = tunzc__krf[3]
            pzgv__ktkv = []
            for njeun__xtmnd in jhbz__mmh:
                if njeun__xtmnd == 'scatter':
                    pzgv__ktkv.append(bodo.scatterv(None))
                elif njeun__xtmnd == 'bcast':
                    pzgv__ktkv.append(eam__ciifs.bcast(None, root=MASTER_RANK))
            rizq__uirny = {}
            for argname, njeun__xtmnd in siivi__rcq.items():
                if njeun__xtmnd == 'scatter':
                    rizq__uirny[argname] = bodo.scatterv(None)
                elif njeun__xtmnd == 'bcast':
                    rizq__uirny[argname] = eam__ciifs.bcast(None, root=
                        MASTER_RANK)
            krov__bdoub = func(*pzgv__ktkv, **rizq__uirny)
            if krov__bdoub is not None and func.overloads[func.signatures[0]
                ].metadata['is_return_distributed']:
                bodo.gatherv(krov__bdoub)
            del (tunzc__krf, ogqwy__papph, func, dgeb__pegu, jhbz__mmh,
                siivi__rcq, pzgv__ktkv, rizq__uirny, krov__bdoub)
            gc.collect()
        elif tunzc__krf[0] == 'exit':
            exit()
    assert False


def master_wrapper(func, *args, **kwargs):
    eam__ciifs = MPI.COMM_WORLD
    if {'all_args_distributed', 'all_args_distributed_block',
        'all_args_distributed_varlength'} & set(func.targetoptions.keys()):
        jhbz__mmh = ['scatter' for zqwf__cxj in range(len(args))]
        siivi__rcq = {argname: 'scatter' for argname in kwargs.keys()}
    else:
        kceg__sredz = func.py_func.__code__.co_varnames
        flhd__wxxn = func.targetoptions

        def get_distribution(argname):
            if argname in flhd__wxxn.get('distributed', []
                ) or argname in flhd__wxxn.get('distributed_block', []):
                return 'scatter'
            else:
                return 'bcast'
        jhbz__mmh = [get_distribution(argname) for argname in kceg__sredz[:
            len(args)]]
        siivi__rcq = {argname: get_distribution(argname) for argname in
            kwargs.keys()}
    dwgwz__vevqu = pickle.dumps(func.py_func)
    eam__ciifs.bcast(['exec', dwgwz__vevqu, jhbz__mmh, siivi__rcq])
    pzgv__ktkv = []
    for rxz__uchzj, njeun__xtmnd in zip(args, jhbz__mmh):
        if njeun__xtmnd == 'scatter':
            pzgv__ktkv.append(bodo.scatterv(rxz__uchzj))
        elif njeun__xtmnd == 'bcast':
            eam__ciifs.bcast(rxz__uchzj)
            pzgv__ktkv.append(rxz__uchzj)
    rizq__uirny = {}
    for argname, rxz__uchzj in kwargs.items():
        njeun__xtmnd = siivi__rcq[argname]
        if njeun__xtmnd == 'scatter':
            rizq__uirny[argname] = bodo.scatterv(rxz__uchzj)
        elif njeun__xtmnd == 'bcast':
            eam__ciifs.bcast(rxz__uchzj)
            rizq__uirny[argname] = rxz__uchzj
    iyyrp__peyh = []
    for ufel__kmvi, bgfr__ixay in list(func.py_func.__globals__.items()):
        if isinstance(bgfr__ixay, MasterModeDispatcher):
            iyyrp__peyh.append((func.py_func.__globals__, ufel__kmvi, func.
                py_func.__globals__[ufel__kmvi]))
            func.py_func.__globals__[ufel__kmvi] = bgfr__ixay.dispatcher
    krov__bdoub = func(*pzgv__ktkv, **rizq__uirny)
    for mbvqx__gtjbl, ufel__kmvi, bgfr__ixay in iyyrp__peyh:
        mbvqx__gtjbl[ufel__kmvi] = bgfr__ixay
    if krov__bdoub is not None and func.overloads[func.signatures[0]].metadata[
        'is_return_distributed']:
        krov__bdoub = bodo.gatherv(krov__bdoub)
    return krov__bdoub


def init_master_mode():
    if bodo.get_size() == 1:
        return
    global master_mode_on
    assert master_mode_on is False, 'init_master_mode can only be called once on each process'
    master_mode_on = True
    assert sys.version_info[:2] >= (3, 8
        ), 'Python 3.8+ required for master mode'
    from bodo import jit
    globals()['jit'] = jit
    import cloudpickle
    from mpi4py import MPI
    globals()['pickle'] = cloudpickle
    globals()['MPI'] = MPI

    def master_exit():
        MPI.COMM_WORLD.bcast(['exit'])
    if bodo.get_rank() == MASTER_RANK:
        import atexit
        atexit.register(master_exit)
    else:
        worker_loop()
