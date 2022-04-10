from unittest import TestCase
import pytest

from pysh.bash import date
from pysh import core, shells
from pysh.tests import test

class DateTests(TestCase):
    def test_date(self):
        def body():
            date.print()
        test.inShell(body, 0)
    def test_convert_to_grep_year(self):
        def body():
            pattern = date.convertToSearchPattern("%Y")
            core.shnl('echo "2021" | grep -E "{}"'.format(pattern))
        test.inShell(body, 0)
    def test_convert_to_grep_month(self):
        def body():
            pattern = date.convertToSearchPattern("%m")
            core.shnl('echo "08" | grep -E "{}"'.format(pattern))
        test.inShell(body, 0)
    def test_convert_to_grep_month_fail(self):
        def body():
            pattern = date.convertToSearchPattern("%m")
            core.shnl('echo "13" | grep -E "{}"'.format(pattern))
        test.inShell(body, 0)
    def test_convert_to_grep_date_1(self):
        def body():
            pattern = date.convertToSearchPattern("%Y/%m")
            core.shnl('echo "2021/02" | grep -E "{}"'.format(pattern))
        test.inShell(body, 0)
    def test_convert_to_grep_date(self):
        def body():
            pattern = date.convertToSearchPattern("%Y/%m/%d %H:%M:%S.%6N")
            core.shnl('echo "2021/02/03 14:33:22.456895" | grep -E "{}"'.format(pattern))
        test.inShell(body, 0)
