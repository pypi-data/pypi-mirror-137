from ._base import D51_DirSyncTestCase
from . import trees

from d51_dirsync import sync


class UpdateTestsWithDst(D51_DirSyncTestCase):

    init_trees = (('src', trees.simple),)

    def setUp(self):
        super(UpdateTestsWithDst, self).setUp()
        sync('src', 'dst', 'sync', create=True)

    def test_del_src_dir(self):
        self.rm('src/dir')

        sync('src', 'dst', 'update')

        self.assertNotExists('src/dir')
        self.assertExists('dst/dir')
