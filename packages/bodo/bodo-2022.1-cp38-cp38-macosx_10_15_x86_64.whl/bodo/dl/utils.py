"""Support distributed deep learning with Horovod
"""
import time
import numba
import numpy as np
from mpi4py import MPI
import bodo
from bodo.libs.distributed_api import create_subcomm_mpi4py, get_host_ranks, get_nodes_first_ranks
dl_status = None


def assert_dl_initialized():
    assert dl_status is not None, 'Horovod has not been initialized. Call bodo.dl.start() first'


class DLStatus(object):

    def __init__(self, framework, gpu_ranks):
        self.framework = framework
        self.gpu_ranks = gpu_ranks


def get_num_gpus(framework):
    if framework == 'torch':
        import torch
        return torch.cuda.device_count()
    elif framework == 'tensorflow':
        import tensorflow as tf
        return len(tf.config.experimental.list_physical_devices('GPU'))
    else:
        raise RuntimeError('Framework {} not recognized'.format(framework))


def get_gpu_ranks(framework):
    rvgaj__vivu = MPI.COMM_WORLD
    bhwl__oxyp = rvgaj__vivu.Get_rank()
    ldep__sshyo = get_host_ranks()
    bilm__ywlas = get_nodes_first_ranks()
    if bhwl__oxyp in bilm__ywlas:
        try:
            xre__xfe = get_num_gpus(framework)
        except Exception as ffo__hys:
            xre__xfe = ffo__hys
        lsvg__pzjs = create_subcomm_mpi4py(bilm__ywlas)
        bkaq__bsiy = lsvg__pzjs.gather(xre__xfe)
        if bhwl__oxyp == 0:
            gpu_ranks = []
            gmcr__rtps = None
            for qxcot__buc, aunj__lfgc in enumerate(ldep__sshyo.values()):
                bwtm__arzqw = bkaq__bsiy[qxcot__buc]
                if isinstance(bwtm__arzqw, Exception):
                    gmcr__rtps = bwtm__arzqw
                    break
                if bwtm__arzqw == 0:
                    continue
                kidv__xvtbb = len(aunj__lfgc) // bwtm__arzqw
                for joma__vvg, qga__suc in enumerate(aunj__lfgc):
                    if joma__vvg % kidv__xvtbb == 0:
                        klfsj__ayg = joma__vvg / kidv__xvtbb
                        if klfsj__ayg < bwtm__arzqw:
                            gpu_ranks.append(qga__suc)
            if gmcr__rtps:
                rvgaj__vivu.bcast(gmcr__rtps)
                raise gmcr__rtps
            else:
                rvgaj__vivu.bcast(gpu_ranks)
    if bhwl__oxyp != 0:
        gpu_ranks = rvgaj__vivu.bcast(None)
        if isinstance(gpu_ranks, Exception):
            ffo__hys = gpu_ranks
            raise ffo__hys
    return gpu_ranks


def is_cuda_available():
    assert_dl_initialized()
    return len(dl_status.gpu_ranks) > 0


def initialize_horovod(framework):
    global dl_status
    if dl_status is not None:
        assert dl_status.framework == framework, 'Attempted to initialize Horovod with different DL frameworks'
        return np.array(dl_status.gpu_ranks, dtype=np.int32)
    gpu_ranks = get_gpu_ranks(framework)
    if framework == 'torch':
        import horovod.torch as hvd
        import torch
        torch.set_num_threads(1)
    elif framework == 'tensorflow':
        import horovod.tensorflow as hvd
        import tensorflow as tf
    else:
        raise RuntimeError('Framework {} not recognized'.format(framework))
    klgkt__jvfv = MPI.COMM_WORLD.rank
    if len(gpu_ranks) > 0:
        lsvg__pzjs = MPI.COMM_WORLD.Split(color=0 if klgkt__jvfv in
            gpu_ranks else MPI.UNDEFINED, key=klgkt__jvfv)
        if lsvg__pzjs != MPI.COMM_NULL:
            hvd.init(comm=lsvg__pzjs)
            if framework == 'torch':
                torch.cuda.set_device(hvd.local_rank())
            elif framework == 'tensorflow':
                jgrwk__jpvz = tf.config.experimental.list_physical_devices(
                    'GPU')
                for eobf__byqv in jgrwk__jpvz:
                    tf.config.experimental.set_memory_growth(eobf__byqv, True)
                tf.config.experimental.set_visible_devices(jgrwk__jpvz[hvd.
                    local_rank()], 'GPU')
    else:
        if klgkt__jvfv == 0:
            print('[BODO-DL]: No GPUs found in cluster. Using CPUs')
        hvd.init()
    dl_status = DLStatus(framework, np.array(gpu_ranks, dtype=np.int32))


@numba.njit
def start(framework):
    with numba.objmode:
        initialize_horovod(framework)


@numba.njit
def end():
    with numba.objmode:
        end_py()


def end_py():
    if is_cuda_available():
        zblwh__alo = 17
        rvgaj__vivu = MPI.COMM_WORLD
        ugwf__cryy = MPI.Get_processor_name()
        atz__ipimb = get_host_ranks()[ugwf__cryy]
        assert_dl_initialized()
        if bodo.get_rank() == atz__ipimb[0]:
            assert bodo.get_rank() in dl_status.gpu_ranks
            for bhwl__oxyp in atz__ipimb[1:]:
                rvgaj__vivu.isend(1, dest=bhwl__oxyp, tag=zblwh__alo)
        else:
            while True:
                shgg__juzwg = MPI.Status()
                wlic__kqlo = rvgaj__vivu.Iprobe(MPI.ANY_SOURCE, MPI.ANY_TAG,
                    shgg__juzwg)
                if wlic__kqlo:
                    assert shgg__juzwg.source == atz__ipimb[0]
                    assert shgg__juzwg.tag == zblwh__alo
                    rvgaj__vivu.recv(source=0, tag=zblwh__alo)
                    break
                time.sleep(1.0)
    else:
        bodo.barrier()


def _prepare_data_get_gpu_ranks():
    assert_dl_initialized()
    return dl_status.gpu_ranks


@numba.njit
def prepare_data(data):
    with numba.objmode(gpu_ranks='int32[:]'):
        gpu_ranks = _prepare_data_get_gpu_ranks()
    if len(gpu_ranks) > 0:
        data = bodo.rebalance(data, dests=list(gpu_ranks), parallel=True)
    else:
        data = bodo.rebalance(data, parallel=True)
    return data
