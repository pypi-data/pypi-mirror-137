import unittest
from r2d2.argument_parser import ArgumentParser
from r2d2.http.dataset import DatasetHTTP


class TestAERONETv3(unittest.TestCase):
    pyear = None
    pmon = None
    pday = None

    def setUp(self):
        self.argument_parser = ArgumentParser()

    def test_download(self):
        args = self.argument_parser.parse_args({
            '--config','./conf/aeronet-v3/config.cfg',
            '--param_year', str(self.pyear),
            '--param_month', str(self.pmon),
            '--param_day', str(self.pday)})
        self._assert_download_succeeded(args)

    def _assert_download_succeeded(self, args):
        self.assertTrue(DatasetHTTP(args).main())#, '{0} argument has not been initialized correctly'.format(argument))


if __name__ == "__main__":
    import sys
    from datetime import datetime
    dt = datetime.strptime(sys.argv[1], "%Y%m%d")
    TestAERONETv3.pyear = dt.year
    TestAERONETv3.pmon = dt.month
    TestAERONETv3.pday = dt.day
    unittest.main(argv=[sys.argv[1]])
