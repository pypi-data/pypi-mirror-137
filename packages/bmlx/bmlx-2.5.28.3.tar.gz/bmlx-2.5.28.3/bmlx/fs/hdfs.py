import os
import io
import sys
import posixpath
import contextlib
from pyarrow.hdfs import HadoopFileSystem, _libhdfs_walk_files_dirs
from bmlx.fs.file_system import FileSystem


class HadoopFileSystem(HadoopFileSystem, FileSystem):
    def __init__(
        self,
        host="default",
        port=0,
        user=None,
        kerb_ticket=None,
        driver="libhdfs",
        extra_conf=None,
    ):
        super().__init__(host=host, port=port, user=user, kerb_ticket=kerb_ticket, driver=driver, extra_conf=extra_conf)

    def __reduce__(self):
        return (
            HadoopFileSystem,
            (
                self.host,
                self.port,
                self.user,
                self.kerb_ticket,
                self.extra_conf,
            ),
        )

    def _isfilestore(self):
        return True

    def isdir(self, path):
        return super().isdir(path)

    def isfile(self, path):
        return super().isfile(path)

    def delete(self, path, recursive=False):
        return super().delete(path, recursive)

    def mkdir(self, path, **kwargs):
        return super().mkdir(path)

    def rename(self, path, new_path):
        return super().rename(path, new_path)

    def exists(self, path):
        return super().exists(path)

    def ls(self, path, detail=False):
        return super().ls(path, detail)

    def walk(self, top_path):
        contents = self.ls(top_path, detail=True)

        directories, files = _libhdfs_walk_files_dirs(top_path, contents)
        yield top_path, directories, files
        for dirname in directories:
            yield from self.walk(self._path_join(top_path, dirname))

    def upload(self, local_file, hdfs_file):
        with open(local_file, "rb") as rf:
            super().upload(path=hdfs_file, stream=rf)

    def download(self, hdfs_file, local_file):
        with open(local_file, "wb") as wf:
            super().download(hdfs_file, wf)


def connect(
    host="default", port=0, user=None, kerb_ticket=None, extra_conf=None
):
    fs = HadoopFileSystem(
        host=host,
        port=port,
        user=user,
        kerb_ticket=kerb_ticket,
        extra_conf=extra_conf,
    )
    return fs
