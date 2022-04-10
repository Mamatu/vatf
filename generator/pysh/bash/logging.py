from pysh import core
from pysh.bash import scope

def logIntoFile(filepath, body = None):
    core.shnl("exec 3>&1 4>&2")
    core.shnl("trap 'exec 2>&4 1>&3' 0 1 2 3")
    core.shnl("exec 1>{} 2>&1".format(filepath))
    scope.handle(body)
