__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from unittest.mock import Mock
from unittest.mock import patch

import datetime
import logging
import numpy
import os
import random

from vatf.utils import rosa

class TestRosa:
    @staticmethod
    def _get_temp_filename():
        import tempfile
        return tempfile.NamedTemporaryFile().name
    def test_waveform_npz_load_save_print(self):
        file1 = self._get_temp_filename()
        file1 = f"{file1}.npz"
        sample_rate = 16000
        samples = [i for i in range(sample_rate)]
        rosa.SaveWaveformToNpzFile((samples, sample_rate), file1)
        loaded = rosa.LoadSamplesSampleRate(file1)
        loaded_sample_rate = loaded[1]
        loaded_samples = loaded[0]
        assert(None != loaded_sample_rate)
        assert (16000 == loaded_sample_rate)
        samples = numpy.array(samples)
        is_equal = numpy.array_equal(samples, loaded_samples)
        assert (is_equal)
        rosa.PrintSamplesSampleRate(loaded)
        os.remove(file1)
    def test_waveform_npz_save(self):
        file1 = self._get_temp_filename()
        file1 = f"{file1}.npz"
        sample_rate = 16000
        samples = [i for i in range(sample_rate)]
        rosa.SaveWaveformToNpzFile((samples, sample_rate), file1)
        loaded_sample_rate = None
        loaded_samples = None
        data = numpy.load(file1, allow_pickle=False)
        loaded_sample_rate = data["sample_rate"]
        loaded_samples = data["samples"]
        assert(None != loaded_sample_rate)
        assert (16000 == loaded_sample_rate)
        samples = numpy.array(samples)
        is_equal = numpy.array_equal(samples, loaded_samples)
        assert(is_equal)
        os.remove(file1)
    def test_calculate_means(self):
        sample_rate = 16000
        samples = []
        samples = [1] * sample_rate
        samples = samples + [2] * sample_rate
        samples = samples + [3] * sample_rate
        samples = numpy.array(samples)
        means, sample_rate = rosa.CalculateMeans((samples, sample_rate), normalize = False)
        assert(3 == len(means))
        assert(1 == sample_rate)
        assert(1 == means[0])
        assert(2 == means[1])
        assert(3 == means[2])
    def test_calculate_means_with_normalization(self):
        sample_rate = 16000
        samples = []
        samples = [1] * sample_rate
        samples = samples + [2] * sample_rate
        samples = samples + [3] * sample_rate
        samples = samples + [4] * sample_rate
        samples = numpy.array(samples)
        means, sample_rate = rosa.CalculateMeans((samples, sample_rate), normalize = True)
        assert(4 == len(means))
        assert(1 == sample_rate)
        assert(0.25 == means[0])
        assert(.5 == means[1])
        assert(.75 == means[2])
        assert(1 == means[3])
    def test_calculate_means_float(self):
        sample_rate = 16000
        samples = [1] * sample_rate
        samples = samples + [2] * sample_rate
        samples = samples + [3] * sample_rate
        samples = numpy.array(samples)
        means, sample_rate = rosa.CalculateMeans((samples, sample_rate), segment_duration = 0.01, normalize = False)
        assert(300 == len(means))
        assert(100 == sample_rate)
        assert(numpy.array_equal([1]*100, means[0:100]))
        assert(numpy.array_equal([2]*100, means[100:200]))
        assert(numpy.array_equal([3]*100, means[200:300]))
