from vatf.api import test

def set_up():
    print("set_up")

def tear_down():
    print("tear_down")

def Test_1():
    print("Test_1")

def Test_2():
    print("Test_2")

test.create_suite()
