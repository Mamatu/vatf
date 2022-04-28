from unittest import TestCase
from unittest.mock import ANY, call, Mock, patch

import logging
import textwrap
from vatf.generator import audio

class AudioTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    @patch("vatf.vatf_register.is_registered")
    @patch("vatf.utils.os_proxy.write_to_file")
    def test_record_inputs_outputs(self, os_proxy_write_to_file, is_registered):
        is_registered.return_value = True
        audio.record_inputs_outputs()
        os_proxy_write_to_file.assert_has_calls([call(ANY, "audio.record_inputs_outputs()\n")])
