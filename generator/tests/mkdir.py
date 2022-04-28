from unittest import TestCase
from unittest.mock import ANY, call, Mock, patch

import logging
import textwrap
from vatf.generator import mkdir

class MkdirTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    @patch("vatf.vatf_register.is_registered")
    @patch("vatf.utils.os_proxy.write_to_file")
    def test_mkdir(self, os_proxy_write_to_file, is_registered):
        is_registered.return_value = True
        mkdir.mkdir("/tmp/session")
        os_proxy_write_to_file.assert_has_calls([call(ANY, "mkdir.mkdir('/tmp/session')\n")])
    @patch("vatf.vatf_register.is_registered")
    @patch("vatf.utils.os_proxy.write_to_file")
    def test_mkdir_with_counter(self, os_proxy_write_to_file, is_registered):
        is_registered.return_value = True
        mkdir.mkdir_with_counter("/tmp/session")
        os_proxy_write_to_file.assert_has_calls([call(ANY, "mkdir.mkdir_with_counter('/tmp/session')\n")])
