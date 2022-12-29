from vatf import vatf_api

@vatf_api.public_api("wait")
def sleep(duration):
    import time as t
    t.sleep(duration)

@vatf_api.public_api("wait")
def sleep_random(t1, t2):
    import time as t
    from random import randint
    t.sleep(randint(t1, t2))

@vatf_api.public_api("wait")
def wait_for_regex(regex, timeout = 30, pause = 0.5, **kwargs):
    from vatf.utils import wait_conditioner
    return wait_conditioner.wait_for_regex(regex, timeout, pause, **kwargs)
