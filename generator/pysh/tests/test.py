from pysh import shells, core

def inShell(func, exitCode, shell = shells.RuntimeShell, onEnd = None):
    commExitCode = None
    try:
        with core.Test(shell):
            func()
    except shells.CommExitCode as cec:
        commExitCode = cec
    if exitCode == 0:
        assert commExitCode == None, commExitCode
    if exitCode != 0:
        assert commExitCode != None
        assert commExitCode.exitCode == exitCode
    if onEnd:
        onEnd()
