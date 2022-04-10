import threading

import subprocess
import sys

def setupAudioConfig(ac, ww):
    ww.setnchannels(ac.getChannels())
    ww.setsampwidth(ac.getSampleWidth())
    ww.setframerate(ac.getFramerate())

def parseAudioConfig(ac):
    return '--channels={} --format={} --rate={}'.format(ac.getChannels(), ac.getFormat(), ac.getFramerate())

def write_wave(filepath, data, ac):
    import wave
    with wave.open(filepath, "wb") as ww:
        setupAudioConfig(ac, ww)
        ww.writeframesraw(data)

def write_raw(filepath, data, ac):
    with open(filepath, "wb") as f:
        f.write(data)

def get_write_func (output_type):
    if str(output_type) == "wav":
        return write_wave
    if str(output_type) == "raw":
        return write_raw
    if str(output_type) == "mp3":
        return None
    return None

def get_write_func_check (output_type):
    func = get_write_func(str(output_type.name))
    if func == None:
        print ("Not supported {} for parec".format(str(output_type.name)))
        exit (1)
    return func

class PARec:
    def __init__(self, source, sink, output_type, audioConfig):
        global g_write_data_func
        global g_write_data_type
        self.processes = None
        self.output = sink
        self.device = source
        self.thread = None
        self.write_data = get_write_func_check(output_type)
        self.audioConfig = audioConfig
    def start(self, isDaemon = True):
        command = ['/usr/bin/parec', parseAudioConfig(self.audioConfig), '-d', self.device]
        print ("os command: {}".format(" ".join(command)))
        self.process = subprocess.Popen(command, shell = False, stdout = subprocess.PIPE)
        def write():
            data = self.process.communicate()[0]
            self.write_data(self.output, data, self.audioConfig)
        self.thread = threading.Thread(target=write)
        self.thread.deamon = isDaemon
        self.thread.start()
    def stop(self):
        self.process.terminate()
    def wait(self):
        if self.thread.daemon:
            self.thread.join()
        self.process.wait()

def create(source, sink, output_type, audio_config):
    return PARec(source, sink, output_type, audio_config)

def getName():
    return "parec"
