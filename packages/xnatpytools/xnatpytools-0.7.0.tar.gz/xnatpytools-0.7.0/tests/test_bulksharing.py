import os

from xnatpytools.utils import MyTestCase, MyTestArguments
from xnatpytools import bulksharing


class TestBulkSharing(MyTestCase):

    def setup(self):
        self.args = MyTestArguments(**{
            'log_dir': '/Users/Ralph',
            'host': 'https://xnat.acc.dh.unimaas.nl/',
            'user': open(os.path.join(os.environ['HOME'], 'xnatuser.txt'), 'r').readline().strip(),
            'password': open(os.path.join(os.environ['HOME'], 'xnatpassword_acc.txt'), 'r').readline().strip(),
            'source_project': 'DMS',
            'target_project': 'TestProject1',
            'test_run': 1,
            'experiments': '1022791_DICOM_HEAD, 1022815_DICOM_HEAD',
            'experiments_file': 'experiments.txt',
        })

    def test_get_client(self):
        self.assertIsNotNone(bulksharing.get_client(self.args))

    def test_get_experiments(self):
        self.assertTrue(len(bulksharing.get_experiments(self.args)) == 2)

    def test_get_experiments_from_file(self):
        self.args.experiments = None
        self.assertTrue(len(bulksharing.get_experiments(self.args)) == 2)

    def test_share_experiments(self):
        bulksharing.share_experiments(bulksharing.get_experiments(self.args), self.args)

    def test_share_experiments_no_test_run(self):
        self.args.test_run = 0
        bulksharing.share_experiments(bulksharing.get_experiments(self.args), self.args)
