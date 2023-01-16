def wait_until_true(callback, pause, timeout):
    import time
    start_point = time.time()
    while True:
        status = callback()
        if status: return True
        time.sleep(pause)
        end_point = time.time()
        if (end_point - start_point) > timeout:
            print(f"timeout: {end_point} {start_point}")
            return False
