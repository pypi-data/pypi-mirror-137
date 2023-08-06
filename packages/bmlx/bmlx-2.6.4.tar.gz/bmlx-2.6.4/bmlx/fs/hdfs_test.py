import os
import unittest

from bmlx.utils import io_utils
from bmlx.fs.hdfs import HadoopFileSystem

class HdfsTest(unittest.TestCase):
    def setUp(self):
        os.chdir("/tmp")
        self.fs, self.path = io_utils.resolve_filesystem_and_path("hdfs://bigo-rt/user/bmlx/bmlx-unittest")

    def tearDown(self):
        pass

    def testHdfsBasic(self):
        test_file = os.path.join(self.path, "hello")

        if self.fs.exists(test_file):
            self.fs.delete(test_file)

        # assert not exist
        self.assertFalse(self.fs.exists(test_file))

        with self.fs.open(test_file, "wb") as f:
            f.write(b"hello, this is bmlx hdfs fs test!")
        # assert exist
        self.assertTrue(self.fs.exists(test_file))
        with self.fs.open(test_file, "rb") as f:
            content = f.read()
            # assert read same content
            self.assertEqual(content, b"hello, this is bmlx hdfs fs test!")
