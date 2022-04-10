import psutil
import subprocess

def __getCommandRaw(input, output, fformat, framerate, channels):
    return f"ffmpeg -f {fformat} -ar {framerate} -ac {channels} -i {input} {output}"

def __getCommand(input, output, audioConfig):
    fformat = audioConfig.getFormat()
    framerate = audioConfig.getFramerate()
    channels = audioConfig.getChannels()
    return __getCommandRaw (input, output, fformat, framerate, channels)

_g_process = None

def convert (input, output, audioConfig):
    global _g_process
    print(f"Convert {input} -> {output} ({audioConfig})")
    command = __getCommand(input, output, audioConfig)
    print(f"{command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    _g_process = process
    process.wait()
    exitCode = process.returncode
    if exitCode != 0:
        print (f"Exit code is {exitCode}")
        exit(1)

def stop():
    global _g_process
    pid = _g_process.pid
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    for child in children:
        child.kill()
    _g_process.terminate()
    _g_process = None
