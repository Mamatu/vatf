__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import wave
from datetime import timedelta

def duration(wvf):
    def get_duration(wv):
        framerate = wv.getframerate()
        frames = wv.getnframe()
        seconds = frames / float(framerate)
        microseconds = seconds * 1000000
        return timedelta(microseconds = microseconds)
    if type (wvf) is str:
        with wave.open(wvf, "rb") as wv:
            return get_duration(wv)
    return get_duration(wvf)

def getnchannels(wvf):
    if type (wvf) is str:
        wvf = wave.open(wvf, "rb")
    return wvf.getnchannels()

def getframerate(wvf):
    if type (wvf) is str:
        wvf = wave.open(wvf, "rb")
    return wvf.getframerate()

def getsampwidth(wvf):
    if type (wvf) is str:
        wvf = wave.open(wvf, "rb")
    return wvf.getsampwidth()

def test_1(TestObj):
    assert duration(TestObj(2, 4)) == timedelta(milliseconds = 500),"{} != {}".format(duration(TestObj(2, 4)), timedelta(milliseconds = 2))

def test_2(TestObj):
    assert duration(TestObj(4, 2)) == timedelta(milliseconds = 2000),"{} != {}".format(duration(TestObj(4, 2)), timedelta(milliseconds = 2))

def tests():
    class TestObj:
        def __init__(self, nframe, framerate):
            self.nframe = nframe
            self.framerate = framerate
        def getnframe(self):
            return self.nframe
        def getframerate(self):
            return self.framerate
    test_1(TestObj)
    test_2(TestObj)
tests()
