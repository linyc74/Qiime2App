from src.io import IO
from .setup import TestCase


class TestIO(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_read_txt(self):
        actual = IO().read(f'{self.indir}/parameters.txt')
        self.assertEqual(actual['User'], 'me')
        self.assertEqual(actual['skip-otu'], True)

    def test_read_tsv(self):
        actual = IO().read(f'{self.indir}/parameters.tsv')
        self.assertEqual(actual['User'], 'me')
        self.assertEqual(actual['skip-otu'], True)

    def test_read_csv(self):
        actual = IO().read(f'{self.indir}/parameters.csv')
        self.assertEqual(actual['User'], 'me')
        self.assertEqual(actual['skip-otu'], True)

    def test_write_txt(self):
        IO().write(
            parameters={
                'User': 'me',
                'Host': '255.255.255.255',
                'skip-otu': True,
                'flag': False,
            },
            file=f'{self.outdir}/parameters.txt'
        )
        self.assertFileEqual(
            f'{self.outdir}/parameters.txt',
            f'{self.indir}/parameters.txt'
        )
