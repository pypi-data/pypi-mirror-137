

import unittest
from mapgenerator.plotting.config import ArgumentParser


class TestArgumentParser(unittest.TestCase):
    def setUp(self):
        self.argument_parser = ArgumentParser()

    def test_argument_parser_is_initialized_with_right_arguments(self):
        arguments_list = ['--config', '--protocol', '--req_type', '--help', '--version', '--config', '--protocol', '--class', '--stream', '--type',
                          '--date', '--time', '--levtype', '--levelist', '--step',
                          '--param', '--origin', '--system', '--method', '--number',
                          '--fcmonth', '--qos']

        self._assert_arguments_in_parser(self.argument_parser, arguments_list)

    def _assert_arguments_in_parser(self, argument_parser, arguments_list):
        for argument in arguments_list:
            initialized = False
            for action in argument_parser.parser._actions:
                if argument in action.option_strings:
                    initialized = True
                    break
            self.assertTrue(initialized, '{0} argument has not been initialized correctly'.format(argument))


if __name__ == "__main__":
    unittest.main()
