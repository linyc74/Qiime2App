from src.controller import parse_screen_ls
from .setup import TestCase


class TestFunction(TestCase):

    def test_parse_screen_ls(self):
        stdout = f'''\
There are screens on:
	835269.outdir_1	(02/16/2025 09:12:36 PM)	(Detached)
	833015.outdir_2	(02/16/2025 03:25:51 PM)	(Detached)
2 Sockets in /run/screen/S-linyc74.'''
        jobs = parse_screen_ls(stdout=stdout)
        self.assertTupleEqual(('835269.outdir_1', '02/16/2025 09:12:36 PM'), jobs[0][0:2])
        self.assertTupleEqual(('833015.outdir_2', '02/16/2025 03:25:51 PM'), jobs[1][0:2])
