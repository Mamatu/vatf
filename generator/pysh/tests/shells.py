from unittest import TestCase
import pytest

from pysh import core, shells

class CtxTests(TestCase):
    def test_empty_shell(self):
        exception = None
        try:
            empty = shells.Empty()
            empty("abc")
            assert empty.size() == 0
        except Exception as ex:
            exception = ex
        assert exception != None
