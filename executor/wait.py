__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from vatf import vatf_api
from vatf.utils import wait_conditioner

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
    return wait_conditioner.wait_for_regex(regex, timeout, pause, **kwargs)
