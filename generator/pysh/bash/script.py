from pysh import core, shells
from pysh.bash import scope

_scripts = []

def declare(filepath, body):
    global _scripts
    bash = shells.BashFile(filepath)
    core.pushShell(bash)
    scope.handle(body)
    core.popShell()
    _scripts.append(filepath)
    return filepath

def call(filepath, *args):
    if filepath != None and filepath != "":
        if filepath not in _scripts:
            raise Exception("Script {} was not created by 'declare' function".format(filepath))
        core.sh("bash {} {}\n".format(filepath, " ".join(args)))
