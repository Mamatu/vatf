__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import librosa
import librosa.display
import matplotlib.pyplot as plt

import numpy
from numpy import savetxt

import sklearn

SAMPLES_IDX = 0
SAMPLE_RATE_IDX = 1

def LoadSamplesSampleRate(input_arg):
    if isinstance(input_arg, str):
        if input_arg.lower().endswith(".npz") or input_arg.lower().endswith(".npy"):
            return LoadSamplesSampleRateFromNumpyFile(input_arg)
        return LoadSamplesSampleRateFromAudioFile(input_arg)
    if isinstance(input_arg, list) or isinstance(input_arg, tuple):
        return input_arg[0], input_arg[1]
    if isinstance(input_arg, dict):
        sample_rate = input_arg["sample_rate"]
        samples = input_arg["samples"]
        return samples, sample_rate
    raise Exception(f"Not supported of input_args type {type(input_arg)}")

def LoadMfcc(input_arg):
    if isinstance(input_arg, dict):
        return input_arg['mfcc']

def LoadSamplesSampleRateFromNumpyData(data):
    if not "samples" in data:
        raise Exception(f"None 'samples' key in data")
    if not "sample_rate" in data:
        raise Exception(f"None 'sample_rate' key in data")
    samples = data["samples"]
    sample_rate = data["sample_rate"]
    sample_rate = sample_rate[0]
    return samples, sample_rate

def LoadMfccFromNumpyData(data):
    data = numpy.Load(filepath)
    if not "mfcc" in data:
        raise Exception(f"None 'mfcc' key in data")
    return data['mfcc']

def LoadSamplesSampleRateFromAudioFile(filepath):
    return librosa.load(filepath, sr=None)

def LoadMfccFromAudioFile(filepath):
    data = librosa.load(filepath, sr=None)
    mfcc = CreateMfcc(data)
    return mfcc

def LoadSamplesSampleRateFromNumpyFile(filepath):
    data = numpy.load(filepath)
    return LoadSamplesSampleRateFromNumpyData(data)

def CreateMfcc(input_arg):
    ssr = LoadSamplesSampleRate(input_arg)
    mfcc = librosa.feature.mfcc(ssr[0], sr=ssr[1])
    mfcc = sklearn.preprocessing.scale(mfcc, axis=1)
    return mfcc

def CreateMfccAndSaveToImageFile(input_arg, output_path, figsize = (90, 5)):
    mfcc = CreateMfcc(input_arg)
    plt.figure(figsize = figsize)
    librosa.display.specshow(mfcc)
    plt.savefig(output_path)

def SaveWaveformToImageFile(input_arg, output_path, figsize = (90, 5)):
    ssr = LoadSamplesSampleRate(input_arg)
    plt.figure(figsize = figsize)
    librosa.display.waveplot(ssr[0], sr = ssr[1])
    plt.savefig(output_path)

def SaveWaveformToNpzFile(input_arg, output_path):
    global SAMPLES_IDX, SAMPLE_RATE_IDX
    ssr = LoadSamplesSampleRate(input_arg)
    data = {}
    data["samples"] = ssr[SAMPLES_IDX]
    data["sample_rate"] = numpy.array([ssr[SAMPLE_RATE_IDX]])
    numpy.savez(output_path, **data)

def RemoveIfEmpty(path):
    samples, sample_rate = LoadSamplesSampleRate(path)
    amax = 0
    if len(samples_rate) > 0:
        amax = numpy.amax(samples)
    if amax == 0:
        import os
        os.remove(path)

def Normalize(input_arg):
    samples, sample_rate = LoadSamplesSampleRate(input_arg)
    amax = numpy.amax(samples)
    if amax != 0:
        samples = samples / amax
    return samples, sample_rate

def NormalizeAndSaveTo(input_arg, output_path):
    ssr = Normalize(input_arg)
    SaveWaveformToNpzFile(ssr, output_path)

def CalculateMeans(input_arg, segment_duration = 1, normalize = True):
    samples, sample_rate = LoadSamplesSampleRate(input_arg)
    if normalize:
        samples, sample_rate = Normalize((samples, sample_rate))
    step = sample_rate * segment_duration 
    step = int(step)
    if step > len(samples):
        raise Exception("Samples are smaller than single step!")
    sample_rate = sample_rate / step
    mean_segments = [samples[x : x + step] for x in range(0, len(samples), step)]
    mean_segments = [numpy.mean(ms) for ms in mean_segments]
    return mean_segments, sample_rate

def CalculateMeansAndSaveTo(input_arg, output_path, segment_duration = 1):
    ssr = CalculateMeans(input_arg, segment_duration)
    SaveWaveformToNpzFile(ssr, output_path)

def PrintSamplesSampleRate(input_arg):
    ssr = LoadSamplesSampleRate(input_arg)
    print()
    print(f"Data from {input_arg}")
    print(f"sample_rate: {ssr[1]}")
    print(f"samples: {ssr[0]}")
