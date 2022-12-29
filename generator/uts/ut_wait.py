__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import logging
from unittest import TestCase
from unittest.mock import ANY, call, Mock, patch

import textwrap
from vatf.generator import wait

class WaitTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    def setUp(self):
        logging.getLogger().setLevel(logging.INFO)
    #@patch("vatf.vatf_api.is_registered")
    #@patch("vatf.generator.gen_tests.verify_call")
    #def test_sleep_random_generator_stage(self, verify_call, is_registered):
    #    is_registered.return_value = True
    #    wait.sleep_random(1, 2, wait.RandomStage.GENERATOR)
    #    expected1 = call('wait.sleep(1)')
    #    expected2 = call('wait.sleep(2)')
    #    self.assertTrue(verify_call.call_args_list == [expected1] or verify_call.call_args_list == [expected2])
    #@patch("vatf.vatf_api.is_registered")
    #@patch("vatf.generator.gen_tests.verify_call")
    #def test_sleep_random_executor_stage(self, verify_call, is_registered):
    #    is_registered.return_value = True
    #    wait.sleep_random(1, 2, wait.RandomStage.EXECUTOR)
    #    verify_call.assert_has_calls([call("wait.sleep_random(1, 2)")])
    #@patch("vatf.vatf_api.is_registered")
    #@patch("vatf.generator.gen_tests.verify_call")
    #def test_wait_for_regex(self, verify_call, is_registered):
    #    is_registered.return_value = True
    #    wait.wait_for_regex(".*", "/tmp/tmp.log", timeout = 10, pause = 0.5)
    #    verify_call.assert_has_calls([call("wait.wait_for_regex('.*', '/tmp/tmp.log', timeout = 10, pause = 0.5)")])
