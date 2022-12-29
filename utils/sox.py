__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import psutil
import subprocess

def __getCommand(input, threads):
    return f"sox {input} -n stat -freq"

class _labelIdx:
    samples = 0
    duration = 1

_g_labels = [
"Samples read:",
"Length (seconds):",
"Scaled by:",
"Maximum amplitude:",
"Minimum amplitude:",
"Midline amplitude:",
"Mean    norm:",
"Mean    amplitude:",
"RMS     amplitude:",
"Maximum delta:",
"Minimum delta:",
"Mean    delta:",
"RMS     delta:",
"Rough   frequency:",
"Volume adjustment:"
]

def _processOutput(exitCode, outputData, output):
    if isinstance(output, str):
        output = open(output, "w")
    out = "".join(outputData);
    output.write(out)
    output.flush()

_g_proc = None
_g_threads = 1

def setThreads(threads):
    global _g_threads
    _g_threads = threads

def _getTempFileName():
    import tempfile
    return tempfile.NamedTemporaryFile().name

def _hasSpectogram(lines):
    global _g_labels
    text = "".join(lines)
    for label in _g_labels:
        if text.find(label) < 0:
            return False
    return True

def spectogram (input, output):
    import sys
    global _g_proc, _g_threads
    print("Creating spectogram...")
    command = __getCommand(input, _g_threads)
    print(f"{command}")
    _stdout = []
    _stderr = []

    exitCode = 12

    fstdout = open(_getTempFileName(), "w+")
    fstderr = open(_getTempFileName(), "w+")

    _g_proc = subprocess.Popen(command, shell=True, stdout=fstdout, stderr=fstderr, close_fds=True, universal_newlines=True)
    _g_proc.wait()

    fstderr.flush()
    fstdout.flush()

    exitCode = _g_proc.returncode
    if exitCode != 0:
        print("Exit with {}".format(exitCode))
        print("Error: {}".format(stderr))
        exit(1)
    
    outputData = None
    fstdout.seek(0)
    dataout = fstdout.readlines()
    fstderr.seek(0)
    dataerr = fstderr.readlines()

    if _hasSpectogram(dataout):
        outputData = dataout
    elif _hasSpectogram(dataerr):
        outputData = dataerr
    if outputData == None:
        raise Exception("None spectogram data in file")

    _processOutput(exitCode, outputData, output)

def stop():
    global _g_proc
    pid = _g_proc.pid
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    for child in children:
        child.kill()
    _g_proc.terminate()
    _g_proc = None
