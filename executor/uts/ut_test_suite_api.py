__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from vatf.api import test
from vatf.api import wait

def set_up():
    print("set_up")

def tear_down():
    print("tear_down")

def Test_1():
    print("Test_1")

def Test_2():
    print("Test_2")
    wait.sleep_random(1, 2)

#test.create_suite()
