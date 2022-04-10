from pysh import core
from pysh.bash import scope, func

def _sox_trim_audio_file():
    cmd = core.Command()
    cmd.cmdStr("sox $1 $1 trim $3 $4")
    return cmd

sox_trim_audio_file = func.declare("sox_trim_audio_file", _sox_trim_audio_file())
