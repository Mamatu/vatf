from unittest import TestCase
from unittest.mock import ANY, call, Mock, patch

import logging
import textwrap
from vatf.generator import wait

class WaitTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    @patch("vatf.vatf_register.is_registered")
    @patch("vatf.utils.os_proxy.write_to_file")
    def test_sleep(self, os_proxy_write_to_file, is_registered):
        is_registered.return_value = True
        wait.sleep(1)
        os_proxy_write_to_file.assert_has_calls([call(ANY, "wait.sleep(1)\n")])
    @patch("vatf.vatf_register.is_registered")
    @patch("vatf.utils.os_proxy.write_to_file")
    def test_sleep_random_generator_stage(self, os_proxy_write_to_file, is_registered):
        is_registered.return_value = True
        wait.sleep_random(1, 2, wait.RandomStage.GENERATOR)
        expected1 = call(ANY, 'wait.sleep(1)\n')
        expected2 = call(ANY, 'wait.sleep(2)\n')
        self.assertTrue(os_proxy_write_to_file.call_args_list == [expected1] or os_proxy_write_to_file.call_args_list == [expected2])
    @patch("vatf.vatf_register.is_registered")
    @patch("vatf.utils.os_proxy.write_to_file")
    def test_sleep_random_executor_stage(self, os_proxy_write_to_file, is_registered):
        is_registered.return_value = True
        wait.sleep_random(1, 2, wait.RandomStage.EXECUTOR)
        os_proxy_write_to_file.assert_has_calls([call(ANY, "wait.sleep_random(1, 2)\n")])
    @patch("vatf.vatf_register.is_registered")
    @patch("vatf.utils.os_proxy.write_to_file")
    def test_wait_for_regex(self, os_proxy_write_to_file, is_registered):
        is_registered.return_value = True
        wait.wait_for_regex(".*", "/tmp/tmp.log", timeout = 10, pause = 0.5)
        os_proxy_write_to_file.assert_has_calls([call(ANY, "wait.wait_for_regex('.*', '/tmp/tmp.log', timeout = 10, pause = 0.5)\n")])