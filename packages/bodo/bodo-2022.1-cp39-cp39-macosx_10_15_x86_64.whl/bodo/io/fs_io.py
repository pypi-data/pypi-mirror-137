"""
S3 & Hadoop file system supports, and file system dependent calls
"""
import glob
import os
import warnings
from urllib.parse import urlparse
import llvmlite.binding as ll
import numba
import numpy as np
from numba.core import types
from numba.extending import overload
import bodo
from bodo.io import csv_cpp
from bodo.libs.distributed_api import Reduce_Type
from bodo.libs.str_ext import unicode_to_utf8, unicode_to_utf8_and_len
from bodo.utils.typing import BodoError, BodoWarning
from bodo.utils.utils import check_java_installation
_csv_write = types.ExternalFunction('csv_write', types.void(types.voidptr,
    types.voidptr, types.int64, types.int64, types.bool_, types.voidptr))
ll.add_symbol('csv_write', csv_cpp.csv_write)
bodo_error_msg = """
    Some possible causes:
        (1) Incorrect path: Specified file/directory doesn't exist or is unreachable.
        (2) Missing credentials: You haven't provided S3 credentials, neither through 
            environment variables, nor through a local AWS setup 
            that makes the credentials available at ~/.aws/credentials.
        (3) Incorrect credentials: Your S3 credentials are incorrect or do not have
            the correct permissions.
    """


def get_proxy_uri_from_env_vars():
    return os.environ.get('http_proxy', None) or os.environ.get('https_proxy',
        None) or os.environ.get('HTTP_PROXY', None) or os.environ.get(
        'HTTPS_PROXY', None)


def get_s3_fs(region=None, storage_options=None):
    from bodo.io.pyarrow_s3fs_fsspec_wrapper import PyArrowS3FS
    qmh__byc = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    nkosv__fagnm = False
    mvxl__wks = get_proxy_uri_from_env_vars()
    if storage_options:
        nkosv__fagnm = storage_options.get('anon', False)
    PyArrowS3FS.clear_instance_cache()
    fs = PyArrowS3FS(region=region, endpoint_override=qmh__byc, anonymous=
        nkosv__fagnm, proxy_options=mvxl__wks)
    return fs


def get_s3_subtree_fs(bucket_name, region=None, storage_options=None):
    from pyarrow._fs import SubTreeFileSystem
    from pyarrow._s3fs import S3FileSystem
    qmh__byc = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    nkosv__fagnm = False
    mvxl__wks = get_proxy_uri_from_env_vars()
    if storage_options:
        nkosv__fagnm = storage_options.get('anon', False)
    fs = S3FileSystem(region=region, endpoint_override=qmh__byc, anonymous=
        nkosv__fagnm, proxy_options=mvxl__wks)
    return SubTreeFileSystem(bucket_name, fs)


def get_s3_fs_from_path(path, parallel=False, storage_options=None):
    region = get_s3_bucket_region_njit(path, parallel=parallel)
    if region == '':
        region = None
    return get_s3_fs(region, storage_options)


def get_hdfs_fs(path):
    from pyarrow.hdfs import HadoopFileSystem as HdFS
    bio__auvpx = urlparse(path)
    if bio__auvpx.scheme in ('abfs', 'abfss'):
        krof__nxnd = path
        if bio__auvpx.port is None:
            gup__ilqz = 0
        else:
            gup__ilqz = bio__auvpx.port
        bkore__eqwh = None
    else:
        krof__nxnd = bio__auvpx.hostname
        gup__ilqz = bio__auvpx.port
        bkore__eqwh = bio__auvpx.username
    try:
        fs = HdFS(host=krof__nxnd, port=gup__ilqz, user=bkore__eqwh)
    except Exception as zky__zgrnh:
        raise BodoError('Hadoop file system cannot be created: {}'.format(
            zky__zgrnh))
    return fs


def gcs_is_directory(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    try:
        kerj__tet = fs.isdir(path)
    except gcsfs.utils.HttpError as zky__zgrnh:
        raise BodoError(
            f'{zky__zgrnh}. Make sure your google cloud credentials are set!')
    return kerj__tet


def gcs_list_dir_fnames(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    return [dfmlv__vwhfe.split('/')[-1] for dfmlv__vwhfe in fs.ls(path)]


def s3_is_directory(fs, path):
    from pyarrow import fs as pa_fs
    try:
        bio__auvpx = urlparse(path)
        xdfpd__hfbe = (bio__auvpx.netloc + bio__auvpx.path).rstrip('/')
        ypmd__rnicl = fs.get_file_info(xdfpd__hfbe)
        if ypmd__rnicl.type in (pa_fs.FileType.NotFound, pa_fs.FileType.Unknown
            ):
            raise FileNotFoundError('{} is a non-existing or unreachable file'
                .format(path))
        if (not ypmd__rnicl.size and ypmd__rnicl.type == pa_fs.FileType.
            Directory):
            return True
        return False
    except (FileNotFoundError, OSError) as zky__zgrnh:
        raise
    except BodoError as lyhsu__iva:
        raise
    except Exception as zky__zgrnh:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(zky__zgrnh).__name__}: {str(zky__zgrnh)}
{bodo_error_msg}"""
            )


def s3_list_dir_fnames(fs, path):
    from pyarrow import fs as pa_fs
    jckmh__ezoid = None
    try:
        if s3_is_directory(fs, path):
            bio__auvpx = urlparse(path)
            xdfpd__hfbe = (bio__auvpx.netloc + bio__auvpx.path).rstrip('/')
            tdbh__ubej = pa_fs.FileSelector(xdfpd__hfbe, recursive=False)
            jbrn__msu = fs.get_file_info(tdbh__ubej)
            if jbrn__msu and jbrn__msu[0].path in [xdfpd__hfbe,
                f'{xdfpd__hfbe}/'] and int(jbrn__msu[0].size or 0) == 0:
                jbrn__msu = jbrn__msu[1:]
            jckmh__ezoid = [pwobf__dnzhb.base_name for pwobf__dnzhb in
                jbrn__msu]
    except BodoError as lyhsu__iva:
        raise
    except Exception as zky__zgrnh:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(zky__zgrnh).__name__}: {str(zky__zgrnh)}
{bodo_error_msg}"""
            )
    return jckmh__ezoid


def hdfs_is_directory(path):
    from pyarrow.fs import FileType, HadoopFileSystem
    check_java_installation(path)
    bio__auvpx = urlparse(path)
    vqv__xmmc = bio__auvpx.path
    try:
        igcp__tioso = HadoopFileSystem.from_uri(path)
    except Exception as zky__zgrnh:
        raise BodoError(' Hadoop file system cannot be created: {}'.format(
            zky__zgrnh))
    rfk__ivgb = igcp__tioso.get_file_info([vqv__xmmc])
    if rfk__ivgb[0].type in (FileType.NotFound, FileType.Unknown):
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if not rfk__ivgb[0].size and rfk__ivgb[0].type == FileType.Directory:
        return igcp__tioso, True
    return igcp__tioso, False


def hdfs_list_dir_fnames(path):
    from pyarrow.fs import FileSelector
    jckmh__ezoid = None
    igcp__tioso, kerj__tet = hdfs_is_directory(path)
    if kerj__tet:
        bio__auvpx = urlparse(path)
        vqv__xmmc = bio__auvpx.path
        tdbh__ubej = FileSelector(vqv__xmmc, recursive=True)
        try:
            jbrn__msu = igcp__tioso.get_file_info(tdbh__ubej)
        except Exception as zky__zgrnh:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(vqv__xmmc, zky__zgrnh))
        jckmh__ezoid = [pwobf__dnzhb.base_name for pwobf__dnzhb in jbrn__msu]
    return igcp__tioso, jckmh__ezoid


def abfs_is_directory(path):
    igcp__tioso = get_hdfs_fs(path)
    try:
        rfk__ivgb = igcp__tioso.info(path)
    except OSError as lyhsu__iva:
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if rfk__ivgb['size'] == 0 and rfk__ivgb['kind'].lower() == 'directory':
        return igcp__tioso, True
    return igcp__tioso, False


def abfs_list_dir_fnames(path):
    jckmh__ezoid = None
    igcp__tioso, kerj__tet = abfs_is_directory(path)
    if kerj__tet:
        bio__auvpx = urlparse(path)
        vqv__xmmc = bio__auvpx.path
        try:
            popw__euhz = igcp__tioso.ls(vqv__xmmc)
        except Exception as zky__zgrnh:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(vqv__xmmc, zky__zgrnh))
        jckmh__ezoid = [fname[fname.rindex('/') + 1:] for fname in popw__euhz]
    return igcp__tioso, jckmh__ezoid


def directory_of_files_common_filter(fname):
    return not (fname.endswith('.crc') or fname.endswith('_$folder$') or
        fname.startswith('.') or fname.startswith('_') and fname !=
        '_delta_log')


def find_file_name_or_handler(path, ftype):
    from urllib.parse import urlparse
    ildh__ecufp = urlparse(path)
    fname = path
    fs = None
    dxg__obhsn = 'read_json' if ftype == 'json' else 'read_csv'
    sot__vzbzz = (
        f'pd.{dxg__obhsn}(): there is no {ftype} file in directory: {fname}')
    iju__hxpd = directory_of_files_common_filter
    if ildh__ecufp.scheme == 's3':
        oawa__kdh = True
        fs = get_s3_fs_from_path(path)
        phx__bmgae = s3_list_dir_fnames(fs, path)
        xdfpd__hfbe = (ildh__ecufp.netloc + ildh__ecufp.path).rstrip('/')
        fname = xdfpd__hfbe
        if phx__bmgae:
            phx__bmgae = [(xdfpd__hfbe + '/' + dfmlv__vwhfe) for
                dfmlv__vwhfe in sorted(filter(iju__hxpd, phx__bmgae))]
            tiu__lcf = [dfmlv__vwhfe for dfmlv__vwhfe in phx__bmgae if int(
                fs.get_file_info(dfmlv__vwhfe).size or 0) > 0]
            if len(tiu__lcf) == 0:
                raise BodoError(sot__vzbzz)
            fname = tiu__lcf[0]
        osxak__uuleu = int(fs.get_file_info(fname).size or 0)
        xnnuo__ekq = fs.open_input_file(fname)
    elif ildh__ecufp.scheme == 'hdfs':
        oawa__kdh = True
        fs, phx__bmgae = hdfs_list_dir_fnames(path)
        osxak__uuleu = fs.get_file_info([ildh__ecufp.path])[0].size
        if phx__bmgae:
            path = path.rstrip('/')
            phx__bmgae = [(path + '/' + dfmlv__vwhfe) for dfmlv__vwhfe in
                sorted(filter(iju__hxpd, phx__bmgae))]
            tiu__lcf = [dfmlv__vwhfe for dfmlv__vwhfe in phx__bmgae if fs.
                get_file_info([urlparse(dfmlv__vwhfe).path])[0].size > 0]
            if len(tiu__lcf) == 0:
                raise BodoError(sot__vzbzz)
            fname = tiu__lcf[0]
            fname = urlparse(fname).path
            osxak__uuleu = fs.get_file_info([fname])[0].size
        xnnuo__ekq = fs.open_input_file(fname)
    elif ildh__ecufp.scheme in ('abfs', 'abfss'):
        oawa__kdh = True
        fs, phx__bmgae = abfs_list_dir_fnames(path)
        osxak__uuleu = fs.info(fname)['size']
        if phx__bmgae:
            path = path.rstrip('/')
            phx__bmgae = [(path + '/' + dfmlv__vwhfe) for dfmlv__vwhfe in
                sorted(filter(iju__hxpd, phx__bmgae))]
            tiu__lcf = [dfmlv__vwhfe for dfmlv__vwhfe in phx__bmgae if fs.
                info(dfmlv__vwhfe)['size'] > 0]
            if len(tiu__lcf) == 0:
                raise BodoError(sot__vzbzz)
            fname = tiu__lcf[0]
            osxak__uuleu = fs.info(fname)['size']
            fname = urlparse(fname).path
        xnnuo__ekq = fs.open(fname, 'rb')
    else:
        if ildh__ecufp.scheme != '':
            raise BodoError(
                f'Unrecognized scheme {ildh__ecufp.scheme}. Please refer to https://docs.bodo.ai/latest/source/file_io.html'
                )
        oawa__kdh = False
        if os.path.isdir(path):
            popw__euhz = filter(iju__hxpd, glob.glob(os.path.join(os.path.
                abspath(path), '*')))
            tiu__lcf = [dfmlv__vwhfe for dfmlv__vwhfe in sorted(popw__euhz) if
                os.path.getsize(dfmlv__vwhfe) > 0]
            if len(tiu__lcf) == 0:
                raise BodoError(sot__vzbzz)
            fname = tiu__lcf[0]
        osxak__uuleu = os.path.getsize(fname)
        xnnuo__ekq = fname
    return oawa__kdh, xnnuo__ekq, osxak__uuleu, fs


def get_s3_bucket_region(s3_filepath, parallel):
    try:
        from pyarrow import fs as pa_fs
    except:
        raise BodoError('Reading from s3 requires pyarrow currently.')
    from mpi4py import MPI
    rwsv__jndfc = MPI.COMM_WORLD
    bucket_loc = None
    if parallel and bodo.get_rank() == 0 or not parallel:
        try:
            bmr__krnqk, cvohn__kxmk = pa_fs.S3FileSystem.from_uri(s3_filepath)
            bucket_loc = bmr__krnqk.region
        except Exception as zky__zgrnh:
            if os.environ.get('AWS_DEFAULT_REGION', '') == '':
                warnings.warn(BodoWarning(
                    f"""Unable to get S3 Bucket Region.
{zky__zgrnh}.
Value not defined in the AWS_DEFAULT_REGION environment variable either. Region defaults to us-east-1 currently."""
                    ))
            bucket_loc = ''
    if parallel:
        bucket_loc = rwsv__jndfc.bcast(bucket_loc)
    return bucket_loc


@numba.njit()
def get_s3_bucket_region_njit(s3_filepath, parallel):
    with numba.objmode(bucket_loc='unicode_type'):
        bucket_loc = ''
        if isinstance(s3_filepath, list):
            s3_filepath = s3_filepath[0]
        if s3_filepath.startswith('s3://'):
            bucket_loc = get_s3_bucket_region(s3_filepath, parallel)
    return bucket_loc


def csv_write(path_or_buf, D, is_parallel=False):
    return None


@overload(csv_write, no_unliteral=True)
def csv_write_overload(path_or_buf, D, is_parallel=False):

    def impl(path_or_buf, D, is_parallel=False):
        uvz__nrhl = get_s3_bucket_region_njit(path_or_buf, parallel=is_parallel
            )
        mev__xfke, hcjf__ppt = unicode_to_utf8_and_len(D)
        kkhd__alxbd = 0
        if is_parallel:
            kkhd__alxbd = bodo.libs.distributed_api.dist_exscan(hcjf__ppt,
                np.int32(Reduce_Type.Sum.value))
        _csv_write(unicode_to_utf8(path_or_buf), mev__xfke, kkhd__alxbd,
            hcjf__ppt, is_parallel, unicode_to_utf8(uvz__nrhl))
        bodo.utils.utils.check_and_propagate_cpp_exception()
    return impl
