from ._base import D51_DirSyncTestCase
from . import trees


class MkTreeTests(D51_DirSyncTestCase):

    init_trees = (('src', trees.simple),)

    def test_simple_tree(self):

        self.assertIsFile('src/file1.txt')
        self.assertIsDir('src/dir')
        self.assertListDir('src/dir', ['file4.txt'])
        self.assertIsDir('src/empty_dir')
        self.assertListDir('src/empty_dir', [])
