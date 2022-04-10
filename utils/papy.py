from enum import Enum
from collections import namedtuple
from subprocess import check_output

import re
import signal

import gstreamer
import parec
import info
import cut

import ac

def get_sources_list():
    out = check_output(["pacmd", "list-sources"])
    return out.decode("utf-8")

def _get_sources_names(raw):
    names = []
    assert raw != None
    assert isinstance(raw, str), "{}".format(raw)
    for line in raw.split("\n"):
        m = re.search(r'name: <(.*)>', line)
        if m != None:
            names.append(m.group(1))
    return names

def get_sources_names():
    sources = get_sources_list()
    assert sources != None
    return _get_sources_names(sources)

testStr = """
    index: 0
        name: <alsa_output.pci-0000_01_00.1.hdmi-stereo.monitor>
        module: 6
        properties:
                device.description = "Monitor of GK107 HDMI Audio Controller Digital Stereo (HDMI)"
    index: 1
        name: <alsa_output.pci-0000_00_1b.0.analog-stereo.monitor>
        properties:

"""

assert _get_sources_names(testStr) == ["alsa_output.pci-0000_01_00.1.hdmi-stereo.monitor", "alsa_output.pci-0000_00_1b.0.analog-stereo.monitor"], "{}".format(_getSourcesNames(testStr))

g_audio_config = ac.AudioConfig(ac.Format.s16le, 1, 44100)
audio_files_path = "/tmp"

g_recorders = []
g_modules = [gstreamer, parec]
g_audio_output_type = "pcm"

g_stoppable = []

def get_output_type():
    global g_audio_output_type
    return str(g_audio_output_type.lower())

def get_file_format():
    return str(get_output_type().lower())

def create_recorder(rec_str, source, sink):
    global g_recorder
    global g_stoppable
    global g_modules
    global g_audio_config
    modules_names = [m.getName() for m in g_modules]
    if not rec_str in modules_names:
        print ("Not supported recorder type: {}".format(rec_str))
    for m in g_modules:
        if rec_str == m.getName():
            g_recorders.append (m.create(source, sink, g_audio_output_type, g_audio_config))
            g_stoppable.append(g_recorders[-1])
            print ("{} -> {}".format(source, sink))

def start_recording():
    for recorder in g_recorders:
        recorder.start()

def get_audio_files_path():
    global audio_files_path
    return audio_files_path

def set_output_type (output_type):
    global g_audio_output_type
    g_audio_output_type = output_type

def set_audio_files_path(path):
    global audio_files_path
    audio_files_path = path

def create_sources_recordings(rec_str):
    sources = get_sources_names()
    for source in sources:
        sink = "{}/{}.{}".format(get_audio_files_path(), source, get_file_format())
        create_recorder(rec_str, source, sink)

def start_sources_recordings():
    global g_recorders
    for recorder in g_recorders:
        recorder.start()

def stop_all_recordings():
    global g_recorders
    for recorder in g_recorders:
        recorder.stop()

def wait_for_all_recordings():
    global g_recorders
    for recorder in g_recorders:
        recorder.wait()

def signal_handler(sig, frame):
    print ("SIGINT")
    global g_stoppable
    for stopable in g_stoppable:
        stopable.stop()

signal.signal(signal.SIGINT, signal_handler)

class RecArgs:
    rec = "--rec"
    dir = "--dir"
    recorder = "--recorder"
    output_type = "--output_type"

import argparse


parser = argparse.ArgumentParser()
parser.add_argument(RecArgs.rec, help = "Start recording and dump into audiofile after Ctrl+C", action="store_true")
parser.add_argument(RecArgs.dir, help = "Directory where audiofiles will be stored")
parser.add_argument(RecArgs.recorder, help = f"Can be {', '.join([module.getName() for module in g_modules])}")
parser.add_argument(RecArgs.output_type, help = "Format of output. It can be raw/pcm, wav or mp3")

class CommonArgs:
    input = "--input"
    output = "--output"
    tool = "--tool"

class WaveformArgs:
    waveform = "--waveform"
    plot = "--plot"

class AudioConfigArgs:
    audio_config = "--audio_config"

class CutArgs:
    cut = "--cut"
    start = "--start"
    end = "--end"
    duration = "--duration"

class ConvertArgs:
    convert="--convert"

class SpectogramArgs:
    spectogram="--spectogram"

class MelspectogramArgs:
    melspectogram="--melspectogram"

class MfccArgs:
    mfcc="--mfcc"

clas ThreadArgs:
    j = "--j"

parser.add_argument(CutArgs.cut, help = "Cut content from wave", action="store_true")
parser.add_argument(CutArgs.start, help = "Start time to cut")
parser.add_argument(CutArgs.end, help = "End time to cut")
parser.add_argument(CutArgs.duration, help = "Duration to cut")

parser.add_argument(SpectogramArgs.spectogram, help = "Creates spectogram from data", action="store_true")
parser.add_argument(MelspectogramArgs.melspectogram, help = "Creates mel spectogram from data", action="store_true")
parser.add_argument(MfccArgs.mfcc, help = "Creates mffc (mel frequency cepstral coefficients) from data", action="store_true")

parser.add_argument(CommonArgs.input, help = "Input file")
parser.add_argument(CommonArgs.output, help = "Output file")
parser.add_argument(CommonArgs.tool, help = "Tool command")

parser.add_argument(ConvertArgs.convert, help = "Convert command", action="store_true")

parser.add_argument(WaveformArgs.waveform, help = "Waveform which can be plotted", action="store_true")
parser.add_argument(WaveformArgs.plot, help = "Plot chart", action="store_true")

parser.add_argument(AudioConfigArgs.audio_config, help = f"Audio config for instance: {AudioConfigArgs.audio_config} s16le,1,44100 (it means format, channels, framerate)")

parser.add_argument(ThreadArgs.j, help = f"Enable multi threading: --j 4")

args = parser.parse_args()

if args.rec:
    if args.output_type:
        set_output_type (args.output_type)
    if args.dir:
        set_audio_files_path(args.dir)
    if args.recorder:
        create_sources_recordings(args.recorder)
    if args.rec:
        start_sources_recordings()
    wait_for_all_recordings()

if args.cut:
    if args.duration and args.end:
        print ("Cannot use duration and end at the same time")
        exit(1)
    startTime = None
    inputPath = None
    outputPath = None
    endTime = None
    duration = None
    if args.input:
        inputPath = args.input
    if args.output:
        outputPath = args.output
    if args.start:
        startTime = args.start
    if args.end:
        endTime = args.end
    if args.duration:
        duration = args.duration
    if startTime == None:
        print ("Start time is not set: {}".format(CutArgs.start))
        exit(1)
    if inputPath == None:
        print ("Input path is not set: {}".format(CutArgs.input))
        exit(1)
    if outputPath == None:
        print ("Output path is not set: {}".format(CutArgs.output))
        exit(1)
    if endTime != None:
        cut.cut_point_to_point_save_to_file (inputPath, startTime, endTime, outputPath)
    elif duration != None:
        cut.cut_segment_save_to_file (inputPath, startTime, duration, outputPath)
    else:
        print ("At least one arguments should be set: --end or --duration")
        exit (1)

if args.convert:
    inputPath = None
    outputPath = None
    audioConfig = None
    command = None

    if args.input:
        inputPath = args.input
    else:
        print("Input not defined")
        exit(1)

    if args.output:
        outputPath = args.output
    else:
        print("Output not defined")
        exit(1)

    if args.audio_config:
        audioConfig = ac.AudioConfig.ParseArg(args.audio_config)
    else:
        print ("Not specified audio config")
        exit(1)

    if args.tool == "ffmpeg":
        import ffmpeg
        command = ffmpeg

    g_stoppable.append(command)
    command.convert(inputPath, outputPath, audioConfig)

if args.waveform:
    from rosa import Waveform
    inputPath = None
    if args.input:
        inputPath = args.input
    else:
        print("Input not defined")
        exit(1)
    wf = Waveform.fromFile(inputPath)
    if args.output:
        outputPath = args.output
        wf.toCSV({"samples" : outputPath})
    if args.plot:
        wf.plot()

if args.spectogram:
    from rosa import Spectogram
    inputPath = None
    if args.input:
        inputPath = args.input
    else:
        print("Input not defined")
        exit(1)
    spec = Spectogram.fromFile(inputPath)
    if args.output:
        outputPath = args.output
        spec.toCSV({"spectogram" : outputPath})
    if args.plot:
        spec.plot()

if args.melspectogram:
    from rosa import MelSpectogram
    inputPath = None
    if args.input:
        inputPath = args.input
    else:
        print("Input not defined")
        exit(1)
    mel = MelSpectogram.fromFile(inputPath)
    if args.output:
        outputPath = args.output
        mel.toCSV({"melspectogram" : outputPath})
    if args.plot:
        mel.plot()

if args.mfcc:
    from rosa import Mfcc
    inputPath = None
    if args.input:
        inputPath = args.input
    else:
        print("Input not defined")
        exit(1)
    mfcc = Mfcc.fromFile(inputPath)
    if args.output:
        outputPath = args.output
        mfcc.toCSV({"mfcc" : outputPath})
    if args.plot:
        mfcc.plot()
