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

test.create_suite()
