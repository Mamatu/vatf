from pysh import core

def _p(time):
    cmd = core.Command()
    cmd.cmdStr('TIME={} && echo "sleep for $TIME" && sleep $TIME'.format(time))
    return cmd

def sleep(time):
    cmd = None
    if type(time) is list:
        import random
        idx = random.randrange(0, len(time))
        cmd = _p(time[idx])
    if type(time) is tuple:
        assert len(time) == 2 or len(time) == 3
        step = 1
        if len(time) == 3:
            step = time[2]
        import random
        value = random.randrange(time[0] / float(step), time[1] / float(step), 1)
        cmd = _p(value * step)
    if type(time) is int:
        cmd = _p(time)
    if type(time) is float:
        cmd = _p(time)
    if cmd == None:
        raise Exception ("not supported yet")
    return cmd
