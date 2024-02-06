import sys, librosa
import librosa.display
import matplotlib.pyplot as plt

from dataclasses import dataclass

from numpy.linalg import norm

class AudioData:
    def __init__(self, path = None, y = None, sr = None, mfcc = None):
        self.path = path
        self.y = y
        self.sr = sr
        self.mfcc = mfcc
        self.aligments = {}

def _get_pathes_tuples(audio_data):
    keys = [(x,y) for x in audio_data.keys() for y in audio_data.keys() if x != y]
    output = []
    existed = []
    for k in keys:
        if k not in existed:
            existed.append(k)
            existed.append((k[1], k[0]))
            output.append(k)
    return output

def get_audio_data_from_files(pathes):
    audio_data = {}
    for path in pathes:
        y, sr = librosa.load(file)
        audio_data[path] = AudioData(path = path, y = y, sr = sr)
    return audio_data

def calculate_mfcc(audio_data):
    for key, value in audio_data.items():
        mfcc = librosa.feature.mfcc(y = value.y, sr = value.sr)
        value.mfcc = mfcc
    return audio_data

def calculate_aligment(audio_data):
    from dtw import dtw, dtwPlot, dtwPlotThreeWay
    keys = _get_pathes_tuples(audio_data)
    idx = 0
    for key in keys:
        value1 = audio_data[key[0]]
        value2 = audio_data[key[1]]
        aligment1 = dtw(value1.mfcc.T, value2.mfcc.T, keep_internals=True)
        aligment2 = dtw(value2.mfcc.T, value1.mfcc.T, keep_internals=True)
        audio_data[key[0]].aligments[key[1]] = aligment1
        audio_data[key[1]].aligments[key[0]] = aligment2
    return audio_data

def get_distances(audio_data):
    keys = _get_pathes_tuples(audio_data)
    output = {}
    for key in keys:
        value1 = audio_data[key[0]]
        value2 = audio_data[key[1]]
        distance = value1.aligments[key[1]].distance
        output[key] = distance
    return output
