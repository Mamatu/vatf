import time
def wait_until_true(callback, pause, timeout):
    if timeout > 0:
        start_point = time.time()
    while True:
        status = callback()
        if status: return True
        time.sleep(pause)
        if timeout > 0:
            end_point = time.time()
            if (end_point - start_point) > timeout:
                return False
