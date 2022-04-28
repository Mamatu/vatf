from unittest import TestCase
from unittest.mock import ANY, call, Mock, patch

import logging
import textwrap
from vatf.generator import shell

class ShellTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    @patch("vatf.vatf_register.is_registered")
    @patch("vatf.utils.os_proxy.write_to_file")
    def test_fg(self, os_proxy_write_to_file, is_registered):
        is_registered.return_value = True
        shell.fg("echo \"A\"")
        os_proxy_write_to_file.assert_has_calls([call(ANY, 'shell.fg(\'echo "A"\')\n')])
    @patch("vatf.vatf_register.is_registered")
    @patch("vatf.utils.os_proxy.write_to_file")
    def test_bg(self, os_proxy_write_to_file, is_registered):
        is_registered.return_value = True
        shell.bg("echo \"A\"")
        os_proxy_write_to_file.assert_has_calls([call(ANY, 'shell.bg(\'echo "A"\')\n')])
