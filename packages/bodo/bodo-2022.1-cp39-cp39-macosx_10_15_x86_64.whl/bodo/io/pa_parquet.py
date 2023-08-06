import asyncio
import os
import threading
from collections import defaultdict
from concurrent import futures
import pyarrow.parquet as pq
from bodo.io.fs_io import get_s3_bucket_region_njit


def get_parquet_filesnames_from_deltalake(delta_lake_path):
    try:
        from deltalake import DeltaTable
    except Exception as zxfa__tps:
        raise ImportError(
            "Bodo Error: please pip install the 'deltalake' package to read parquet from delta lake"
            )
    tmvzk__bsk = None
    uzh__vcc = delta_lake_path.rstrip('/')
    uwt__dfgln = 'AWS_DEFAULT_REGION' in os.environ
    tasx__nsdq = os.environ.get('AWS_DEFAULT_REGION', '')
    wcif__oze = False
    if delta_lake_path.startswith('s3://'):
        lyqtt__zlywi = get_s3_bucket_region_njit(delta_lake_path, parallel=
            False)
        if lyqtt__zlywi != '':
            os.environ['AWS_DEFAULT_REGION'] = lyqtt__zlywi
            wcif__oze = True
    fbvx__vkh = DeltaTable(delta_lake_path)
    tmvzk__bsk = fbvx__vkh.files()
    tmvzk__bsk = [(uzh__vcc + '/' + hep__htg) for hep__htg in sorted(
        tmvzk__bsk)]
    if wcif__oze:
        if uwt__dfgln:
            os.environ['AWS_DEFAULT_REGION'] = tasx__nsdq
        else:
            del os.environ['AWS_DEFAULT_REGION']
    return tmvzk__bsk


def get_dataset_schema(dataset):
    if dataset.metadata is None and dataset.schema is None:
        if dataset.common_metadata is not None:
            dataset.schema = dataset.common_metadata.schema
        else:
            dataset.schema = dataset.pieces[0].get_metadata().schema
    elif dataset.schema is None:
        dataset.schema = dataset.metadata.schema
    onvtr__klhn = dataset.schema.to_arrow_schema()
    if dataset.partitions is not None:
        for axra__kgvo in dataset.partitions.partition_names:
            if onvtr__klhn.get_field_index(axra__kgvo) != -1:
                alor__ebjt = onvtr__klhn.get_field_index(axra__kgvo)
                onvtr__klhn = onvtr__klhn.remove(alor__ebjt)
    return onvtr__klhn


class VisitLevelThread(threading.Thread):

    def __init__(self, manifest):
        threading.Thread.__init__(self)
        self.manifest = manifest
        self.exc = None

    def run(self):
        try:
            manifest = self.manifest
            manifest.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(manifest.loop)
            manifest.loop.run_until_complete(manifest._visit_level(0,
                manifest.dirpath, []))
        except Exception as zxfa__tps:
            self.exc = zxfa__tps
        finally:
            if hasattr(manifest, 'loop') and not manifest.loop.is_closed():
                manifest.loop.close()

    def join(self):
        super(VisitLevelThread, self).join()
        if self.exc:
            raise self.exc


class ParquetManifest:

    def __init__(self, dirpath, open_file_func=None, filesystem=None,
        pathsep='/', partition_scheme='hive', metadata_nthreads=1):
        filesystem, dirpath = pq._get_filesystem_and_path(filesystem, dirpath)
        self.filesystem = filesystem
        self.open_file_func = open_file_func
        self.pathsep = pathsep
        self.dirpath = pq._stringify_path(dirpath)
        self.partition_scheme = partition_scheme
        self.partitions = pq.ParquetPartitions()
        self.pieces = []
        self._metadata_nthreads = metadata_nthreads
        self._thread_pool = futures.ThreadPoolExecutor(max_workers=
            metadata_nthreads)
        self.common_metadata_path = None
        self.metadata_path = None
        self.delta_lake_filter = set()
        self.partition_vals = defaultdict(set)
        gyw__rhftu = VisitLevelThread(self)
        gyw__rhftu.start()
        gyw__rhftu.join()
        for efcz__mmikj in self.partition_vals.keys():
            self.partition_vals[efcz__mmikj] = sorted(self.partition_vals[
                efcz__mmikj])
        for ouq__ktof in self.partitions.levels:
            ouq__ktof.keys = sorted(ouq__ktof.keys)
        for bty__runhj in self.pieces:
            if bty__runhj.partition_keys is not None:
                bty__runhj.partition_keys = [(rrmr__qra, self.
                    partition_vals[rrmr__qra].index(wng__gpm)) for 
                    rrmr__qra, wng__gpm in bty__runhj.partition_keys]
        self.pieces.sort(key=lambda piece: piece.path)
        if self.common_metadata_path is None:
            self.common_metadata_path = self.metadata_path
        self._thread_pool.shutdown()

    async def _visit_level(self, xipkq__wxu, base_path, apk__rlrt):
        fs = self.filesystem
        ejs__ikal, jltbx__vjzfn, lbmp__kynr = await self.loop.run_in_executor(
            self._thread_pool, lambda fs, base_bath: next(fs.walk(base_path
            )), fs, base_path)
        if xipkq__wxu == 0 and '_delta_log' in jltbx__vjzfn:
            self.delta_lake_filter = set(get_parquet_filesnames_from_deltalake
                (base_path))
        dbbe__igfz = []
        for uzh__vcc in lbmp__kynr:
            if uzh__vcc == '':
                continue
            skv__oucxc = self.pathsep.join((base_path, uzh__vcc))
            if uzh__vcc.endswith('_common_metadata'):
                self.common_metadata_path = skv__oucxc
            elif uzh__vcc.endswith('_metadata'):
                self.metadata_path = skv__oucxc
            elif self._should_silently_exclude(uzh__vcc):
                continue
            elif self.delta_lake_filter and skv__oucxc not in self.delta_lake_filter:
                continue
            else:
                dbbe__igfz.append(skv__oucxc)
        gqaj__avp = [self.pathsep.join((base_path, hwbpy__ewfpo)) for
            hwbpy__ewfpo in jltbx__vjzfn if not pq._is_private_directory(
            hwbpy__ewfpo)]
        dbbe__igfz.sort()
        gqaj__avp.sort()
        if len(dbbe__igfz) > 0 and len(gqaj__avp) > 0:
            raise ValueError('Found files in an intermediate directory: {}'
                .format(base_path))
        elif len(gqaj__avp) > 0:
            await self._visit_directories(xipkq__wxu, gqaj__avp, apk__rlrt)
        else:
            self._push_pieces(dbbe__igfz, apk__rlrt)

    async def _visit_directories(self, xipkq__wxu, jltbx__vjzfn, apk__rlrt):
        wlczm__dskyo = []
        for uzh__vcc in jltbx__vjzfn:
            xtbmx__ysne, pbmx__djl = pq._path_split(uzh__vcc, self.pathsep)
            rrmr__qra, dswll__jtw = pq._parse_hive_partition(pbmx__djl)
            xanaj__dsxc = self.partitions.get_index(xipkq__wxu, rrmr__qra,
                dswll__jtw)
            self.partition_vals[rrmr__qra].add(dswll__jtw)
            egep__rijlz = apk__rlrt + [(rrmr__qra, dswll__jtw)]
            wlczm__dskyo.append(self._visit_level(xipkq__wxu + 1, uzh__vcc,
                egep__rijlz))
        await asyncio.wait(wlczm__dskyo)


ParquetManifest._should_silently_exclude = (pq.ParquetManifest.
    _should_silently_exclude)
ParquetManifest._parse_partition = pq.ParquetManifest._parse_partition
ParquetManifest._push_pieces = pq.ParquetManifest._push_pieces
pq.ParquetManifest = ParquetManifest


def pieces(self):
    return self._pieces


pq.ParquetDataset.pieces = property(pieces)


def partitions(self):
    return self._partitions


pq.ParquetDataset.partitions = property(partitions)
