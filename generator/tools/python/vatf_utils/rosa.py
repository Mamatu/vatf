import librosa
import librosa.display
import matplotlib.pyplot as plt

import numpy
from numpy import savetxt

import sklearn

SAMPLES_IDX = 0
SAMPLE_RATE_IDX = 1

def loadSamplesSampleRateFromAudioFile(filepath):
    return librosa.load(filepath, sr=None)

def loadSamplesSampleRateFromNumpyFile(filepath):
    data = numpy.load(filepath)
    if not "samples" in data:
        raise Exception(f"Not 'samples' key in {filepath}")
    if not "sample_rate" in data:
        raise Exception(f"Not 'sample_rate' key in {filepath}")
    samples = data["samples"]
    sample_rate = data["sample_rate"]
    sample_rate = sample_rate[0]
    return samples, sample_rate

def getShortFT(filepath, cmplxFilter):
    samples, sample_rate = loadSamplesSampleRateFromAudioFile(filepath)
    sgram = librosa.stft(samples)
    temp = sgram
    sgram = cmplxFilter(sgram)
    sgram = numpy.array(sgram)
    return sgram, samples, sample_rate

def getShortFTRe(filepath):
    return getShortFT(filepath, lambda sgram: [x.real for x in sgram])

def getShortFTIm(filepath):
    return getShortFT(filepath, lambda sgram: [x.imag for x in sgram])

class Waveform:
    def __init__(self, samples, sample_rate):
        self.samples = samples
        self.sample_rate = sample_rate
    @staticmethod
    def fromFile(path):
        samples, sample_rate = loadSamplesSampleRateFromAudioFile(path);
        return Waveform(samples, sample_rate)
    def toCSV(self, pathes):
        if "sample_rate" in pathes:
            with open(pathes['sample_rate'], "w") as f:
                f.write(str(self.sample_rate))
        if "samples" in pathes:
            savetxt(pathes["samples"], self.samples, delimiter=",")
    def toNpy(self, pathes):
        if "sample_rate" in pathes:
            with open(pathes['sample_rate'], "wb") as f:
                numpy.save(f, numpy.array([self.sample_rate]), allow_pickle = False)
        if "samples" in pathes:
            with open(pathes["samples"], "wb") as f:
                numpy.save(f, self.samples, allow_pickle = False)
    def plot(self, output_path):
        plt.figure(figsize=(90, 5))
        librosa.display.waveplot(self.samples, sr=self.sample_rate)
        plt.savefig(output_path)

class Spectogram(Waveform):
    def __init__(self, samples, sample_rate):
        Waveform.__init__(self, samples, sample_rate)
        self.spectogram = librosa.stft(self.samples)
        self.spectogram = [x.real if isinstance(x, complex) else x for x in self.spectogram]
        self.spectogram = numpy.array(self.spectogram)
    @staticmethod
    def fromFile(path):
        samples, sample_rate = loadSamplesSampleRateFromAudioFile(path);
        return Spectogram(samples, sample_rate)
    def toCSV(self, pathes):
        Waveform.toCSV(self, pathes)
        if "spectogram" in pathes:
            savetxt(pathes["spectogram"], self.spectogram, delimiter=",")
    def toNpy(self, pathes):
        Waveform.toNpy(self, pathes)
        if "spectogram" in pathes:
            with open(pathes["spectogram"], "wb") as f:
                numpy.save(f, self.spectogram, allow_pickle = False)
    def plot(self, output_path):
        plt.figure(figsize=(14, 5))
        librosa.display.specshow(self.spectogram)
        plt.savefig(output_path)

class MelSpectogram(Spectogram):
    def __init__(self, samples, sample_rate):
        Spectogram.__init__(self, samples, sample_rate)
        self.melspectogram, _ = librosa.magphase(self.spectogram)
        self.melspectogram = librosa.feature.melspectrogram(S=self.melspectogram, sr=self.sample_rate)
    @staticmethod
    def fromFile(path):
        samples, sample_rate = loadSamplesSampleRateFromAudioFile(path);
        return MelSpectogram(samples, sample_rate)
    def toCSV(self, pathes):
        Spectogram.toCSV(self, pathes)
        if "melspectogram" in pathes:
            savetxt(pathes["melspectogram"], self.melspectogram, delimiter=",")
    def toNpy(self, pathes):
        Spectogram.toNpy(self, pathes)
        if "melspectogram" in pathes:
            with open(pathes["melspectogram"], "wb") as f:
                numpy.save(f, self.melspectogram, allow_pickle = False)
    def plot(self, output_path):
        plt.figure(figsize=(14, 5))
        librosa.display.specshow(self.melspectogram)
        plt.savefig(output_path)

class Mfcc(Waveform):
    def __init__(self, samples, sample_rate):
        Waveform.__init__(self, samples, sample_rate)
        self.mfcc = librosa.feature.mfcc(self.samples, sr=self.sample_rate)
        self.mfcc = sklearn.preprocessing.scale(self.mfcc, axis=1)
    @staticmethod
    def fromFile(path):
        samples, sample_rate = loadSamplesSampleRateFromAudioFile(path);
        return Mfcc(samples, sample_rate)
    def toCSV(self, pathes):
        Waveform.toCSV(self, pathes)
        if "mfcc" in pathes:
            savetxt(pathes["mfcc"], self.mfcc, delimiter=",")
    def toNpy(self, pathes):
        Waveform.toNpy(self, pathes)
        if "mfcc" in pathes:
            with open(pathes["mfcc"], "wb") as f:
                numpy.save(f, self.mfcc, allow_pickle = False)
    def plot(self, output_path):
        plt.figure(figsize=(14, 5))
        librosa.display.specshow(self.mfcc)
        plt.savefig(output_path)

def LoadSamplesSampleRate(input_arg):
    if isinstance(input_arg, str):
        if input_arg.lower().endswith(".npz") or input_arg.lower().endswith(".npy"):
            return loadSamplesSampleRateFromNumpyFile(input_arg)
        return loadSamplesSampleRateFromAudioFile(input_arg)
    if isinstance(input_arg, list) or isinstance(input_arg, tuple):
        return input_arg[0], input_arg[1]
    if isinstance(input_arg, dict):
        sample_rate = input_arg["sample_rate"]
        samples = input_arg["samples"]
        return samples, sample_rate
    raise Exception(f"Not supported of input_args type {type(input_arg)}")

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
