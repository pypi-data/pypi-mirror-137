from urllib.parse import urlparse
import pyarrow.fs as pa_fs
from fsspec import AbstractFileSystem
from pyarrow.fs import S3FileSystem


class PyArrowS3FS(AbstractFileSystem):
    protocol = 's3'

    def __init__(self, *, access_key=None, secret_key=None, session_token=
        None, anonymous=False, region=None, scheme=None, endpoint_override=
        None, background_writes=True, role_arn=None, session_name=None,
        external_id=None, load_frequency=900, proxy_options=None, **kwargs):
        super().__init__(self, **kwargs)
        self.pa_s3fs = S3FileSystem(access_key=access_key, secret_key=
            secret_key, session_token=session_token, anonymous=anonymous,
            region=region, scheme=scheme, endpoint_override=
            endpoint_override, background_writes=background_writes,
            role_arn=role_arn, session_name=session_name, external_id=
            external_id, load_frequency=load_frequency, proxy_options=
            proxy_options)

    def __getattribute__(self, name: str):
        if name == '__class__':
            return PyArrowS3FS
        if name in ['__init__', '__getattribute__', '_open', 'open', 'ls',
            'isdir', 'isfile']:
            return lambda *args, **kw: getattr(PyArrowS3FS, name)(self, *
                args, **kw)
        ssi__tasl = object.__getattribute__(self, '__dict__')
        zimy__opapp = ssi__tasl.get('pa_s3fs', None)
        if name == 'pa_s3fs':
            return zimy__opapp
        if zimy__opapp is not None and hasattr(zimy__opapp, name):
            return getattr(zimy__opapp, name)
        return super().__getattribute__(name)

    def _open(self, path, mode='rb', block_size=None, autocommit=True,
        cache_options=None, **kwargs):
        ugyva__ujqe = urlparse(path)
        tbna__nlvu = ugyva__ujqe.netloc + ugyva__ujqe.path
        return self.pa_s3fs.open_input_file(tbna__nlvu)

    def ls(self, path, detail=True, **kwargs):
        ugyva__ujqe = urlparse(path)
        tbna__nlvu = (ugyva__ujqe.netloc + ugyva__ujqe.path).rstrip('/')
        vqa__fzsss = pa_fs.FileSelector(tbna__nlvu, recursive=False)
        xgc__inh = self.pa_s3fs.get_file_info(vqa__fzsss)
        if len(xgc__inh) == 0:
            if self.isfile(path):
                if detail:
                    return [{'type': 'file', 'name': tbna__nlvu}]
                else:
                    return [tbna__nlvu]
            return []
        if xgc__inh and xgc__inh[0].path in [tbna__nlvu, f'{tbna__nlvu}/'
            ] and int(xgc__inh[0].size or 0) == 0:
            xgc__inh = xgc__inh[1:]
        pkf__jdab = []
        if detail:
            for sfvt__zfrcv in xgc__inh:
                wko__crfi = {}
                if sfvt__zfrcv.type == pa_fs.FileType.Directory:
                    wko__crfi['type'] = 'directory'
                elif sfvt__zfrcv.type == pa_fs.FileType.File:
                    wko__crfi['type'] = 'file'
                else:
                    wko__crfi['type'] = 'unknown'
                wko__crfi['name'] = sfvt__zfrcv.base_name
                pkf__jdab.append(wko__crfi)
        else:
            pkf__jdab = [sfvt__zfrcv.base_name for sfvt__zfrcv in xgc__inh]
        return pkf__jdab

    def isdir(self, path):
        ugyva__ujqe = urlparse(path)
        tbna__nlvu = (ugyva__ujqe.netloc + ugyva__ujqe.path).rstrip('/')
        gcnjv__ecm = self.pa_s3fs.get_file_info(tbna__nlvu)
        return (not gcnjv__ecm.size and gcnjv__ecm.type == pa_fs.FileType.
            Directory)

    def isfile(self, path):
        ugyva__ujqe = urlparse(path)
        tbna__nlvu = (ugyva__ujqe.netloc + ugyva__ujqe.path).rstrip('/')
        gcnjv__ecm = self.pa_s3fs.get_file_info(tbna__nlvu)
        return gcnjv__ecm.type == pa_fs.FileType.File
