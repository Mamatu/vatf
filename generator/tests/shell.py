from unittest import TestCase
from unittest.mock import ANY, call, Mock, patch

import logging
import textwrap
from vatf.generator import shell

class ShellTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    @patch("vatf.vatf_api.is_registered")
    @patch("vatf.generator.gen_tests.verify_call")
    def test_fg(self, verify_call, is_registered):
        is_registered.return_value = True
        shell.fg("echo \"A\"")
        verify_call.assert_has_calls([call('shell.fg(\'echo "A"\')')])
    @patch("vatf.vatf_api.is_registered")
    @patch("vatf.generator.gen_tests.verify_call")
    def test_bg(self, verify_call, is_registered):
        is_registered.return_value = True
        shell.bg("echo \"A\"")
        verify_call.assert_has_calls([call('shell.bg(\'echo "A"\')')])
