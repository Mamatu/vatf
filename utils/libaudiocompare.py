import sys, librosa
import librosa.display
import matplotlib.pyplot as plt

from dataclasses import dataclass

from numpy.linalg import norm
from dtw import dtw, dtwPlot, dtwPlotThreeWay

def init_audio_data_from_files(pathes):
    audio_data = {}
    for path in pathes:
        y, sr = librosa.load(path)
        audio_data[path] = AudioData(path = path, y = y, sr = sr)
    return audio_data

def calculate_mfcc(audio_data):
    for key, value in audio_data.items():
        mfcc = librosa.feature.mfcc(y = value.y, sr = value.sr)
        value.mfcc = mfcc
    return audio_data

def _dtw(audio_data1, audio_data2, keep_internals):
    try:
        return dtw(audio_data1.mfcc.T, audio_data2.mfcc.T, keep_internals=True)
    except Exception as e:
        print(f"{audio_data1.path} {audio_data1.mfcc.shape} and {audio_data2.path} {audio_data2.mfcc.shape}: {e}", file=sys.stderr)
        raise e

def calculate_alignment(audio_data):
    keys = _get_pathes_tuples(audio_data)
    idx = 0
    for key in keys:
        value1 = audio_data[key[0]]
        value2 = audio_data[key[1]]
        try:
            alignment1 = _dtw(value1, value2, keep_internals=True)
            alignment2 = _dtw(value2, value1, keep_internals=True) #to optimize, alignment2 can be created from alignment1
            audio_data[key[0]].alignments[key[1]] = alignment1
            audio_data[key[1]].alignments[key[0]] = alignment2
        except Exception as e:
            print(f"Error in {key[0]} and {key[1]}: {e}", file=sys.stderr)
    return audio_data

def get_distances(audio_data):
    keys = _get_pathes_tuples(audio_data)
    output = {}
    for key in keys:
        value1 = audio_data[key[0]]
        value2 = audio_data[key[1]]
        distance = value1.alignments[key[1]].distance
        output[key] = distance
    return output

class AudioData:
    def __init__(self, path = None, y = None, sr = None, mfcc = None):
        self.path = path
        self.y = y
        self.sr = sr
        self.mfcc = mfcc
        self.alignments = {}

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
