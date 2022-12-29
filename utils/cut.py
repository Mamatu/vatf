__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import wave
import info
from datetime import timedelta

def parse_time_to_microsecs(time):
    try:
        if type(time) is timedelta:
            return time.microseconds
        if type(time) is str:
            import datetime
            formats = [float, int, "%M:%S", "%H:%M:%S"]
            stime = None
            for format in formats:
                try:
                    if type(format) is str:
                        stime = datetime.strptime(time, format).microseconds
                    else:
                        stime = format(time)
                except Exception:
                    pass
            if stime == None:
                raise Exception("Cannot parse time from string. It can be {}".format(formats))
            elif type(stime) is datetime.datetime:
                return (stime - datetime.datetime(year=1990, month=1, day=1)).microseconds
            return stime 
        return time
    except Exception as e:
        import traceback
        print("Error during parsing: {}".format(str(e)))
        traceback.print_exc()
        exit(1)

def cut_point_to_point(wvf, startTime, endTime):
    if type(wvf) is str:
        wvf = wave.open(wvf, "rb")
    startTime = parse_time_to_microsecs(startTime)
    endTime = parse_time_to_microsecs(endTime)
    assert startTime < endTime
    framerate = wvf.getframerate()
    duration = endTime - startTime
    startFrame = int(framerate * startTime)
    wvf.setpos(startFrame)
    frames = int(duration * framerate)
    return wvf.readframes(frames)

def cut_segment(wvf, startTime, duration):
    startTime = parse_time_to_microsecs(startTime)
    duration = parse_time_to_microsecs(duration)
    return cut_point_to_point(wvf, startTime, startTime + duration)

def cut_point_to_point_save_to_file(wvf, startTime, endTime, path):
    bbytes = cut_point_to_point (wvf, startTime, endTime)
    with wave.open(path, "wb") as wv:
        wv.setnchannels(info.getnchannels(wvf))
        wv.setsampwidth(info.getsampwidth(wvf))
        wv.setframerate(info.getframerate(wvf))
        wv.writeframesraw(bbytes)

def cut_segment_save_to_file(wvf, startTime, duration, path):
    bbytes = cut_segment (wvf, startTime, duration)
    with wave.open(path, "wb") as wv:
        wv.setnchannels(info.getnchannels(wvf))
        wv.setsampwidth(info.getsampwidth(wvf))
        wv.setframerate(info.getframerate(wvf))
        wv.writeframesraw(bbytes)
