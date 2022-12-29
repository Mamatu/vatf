__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import psutil

import subprocess
import sys
from vatf.utils import ac

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

pulsesrc_source = [["date '+%Y-%m-%d %H:%M:%S.%6N' > {sink}.date && gst-launch-1.0 -e", "pulsesrc device = {source}"], "queue", "audioresample", "audioconvert", "{audio_config}"]

mp3_sink = ["lamemp3enc name=enc target=0 qauality=2", "xingmux", "id3mux", "filesink location={sink} append=false"]
wave_sink = ["wavenc", "filesink location={sink} append=false"]
raw_sink = ["filesink location={sink} append=false"]

def get_sink_pipeline (output_type):
    if output_type == "wav":
        return wave_sink
    if output_type == "raw" or output_type == "pcm":
        return raw_sink
    if output_type == "mp3":
        return mp3_sink
    return None

def get_sink_pipeline_check (output_type):
    pipeline = get_sink_pipeline(output_type)
    if pipeline == None:
        print ("Not supported {} for gstreamer".format(str(output_type.name)))
        exit (1)
    return pipeline

def pipeline_to_str(pln):
    temp = []
    for x in pln:
        if isinstance(x, list):
            x = " ".join(x)
        temp.append(x)
    return " ! ".join(temp)

def merge_pipelines(source, sink):
    src = pipeline_to_str(source)
    snk = pipeline_to_str(sink)
    return "{} ! {}".format(src, snk)

def parseAudioConfig(ac):
    return "audio/x-raw,rate={},channels={}".format(ac.getFramerate(), ac.getChannels())

def make_json_info(recording_path, json_file_path, ac, creation_time = None):
    import datetime
    global DATE_FORMAT
    if creation_time == None:
        creation_time = datetime.datetime.now().strftime(DATE_FORMAT)
    else:
        creation_time = creation_time.strftime(DATE_FORMAT)
    json = {}
    json['info'] = []
    info = {"recording_path": recording_path, "creation_time" : creation_time, "samples_rate" : ac.getFramerate(), "format": ac.getFormat(), "channels" : ac.getChannels()}
    json['info'].append(info)
    with open(json_file_path, "w") as f:
        import json as j
        j.dump(json, f)

class GstRec:
    def __init__(self, source, sink, output_type, audioConfig):
        self.process = None
        self.source = source
        self.sink = sink
        self.audioConfig = audioConfig
        self.command = merge_pipelines(pulsesrc_source, get_sink_pipeline_check(output_type))
        self.command = self.command.format(source = source, sink = sink, audio_config = parseAudioConfig(audioConfig))
    def start(self):
        print ("os command: {}".format(self.command))
        make_json_info(self.sink, f"{self.sink}.json", self.audioConfig)
        self.process = subprocess.Popen(self.command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
    def stop(self):
        parent = psutil.Process(self.process.pid)
        children = parent.children(recursive=True)
        for child in children:
            child.kill()
        self.process.terminate()
    def wait(self):
        self.process.wait()

def create(source, sink, output_type, audio_config):
    return GstRec(source, sink, output_type, audio_config)

def getName():
    return "gst"
