__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

import datetime
import logging
import numpy
import os
import random

from vatf.utils import rosa

class RosaTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
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
        self.assertNotEqual(None, loaded_sample_rate)
        self.assertEqual(16000, loaded_sample_rate)
        samples = numpy.array(samples)
        is_equal = numpy.array_equal(samples, loaded_samples)
        self.assertTrue(is_equal)
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
        self.assertNotEqual(None, loaded_sample_rate)
        self.assertEqual(16000, loaded_sample_rate)
        samples = numpy.array(samples)
        is_equal = numpy.array_equal(samples, loaded_samples)
        self.assertTrue(is_equal)
        os.remove(file1)
    def test_calculate_means(self):
        sample_rate = 16000
        samples = []
        samples = [1] * sample_rate
        samples = samples + [2] * sample_rate
        samples = samples + [3] * sample_rate
        samples = numpy.array(samples)
        means, sample_rate = rosa.CalculateMeans((samples, sample_rate), normalize = False)
        self.assertEqual(3, len(means))
        self.assertEqual(1, sample_rate)
        self.assertEqual(1, means[0])
        self.assertEqual(2, means[1])
        self.assertEqual(3, means[2])
    def test_calculate_means_with_normalization(self):
        sample_rate = 16000
        samples = []
        samples = [1] * sample_rate
        samples = samples + [2] * sample_rate
        samples = samples + [3] * sample_rate
        samples = samples + [4] * sample_rate
        samples = numpy.array(samples)
        means, sample_rate = rosa.CalculateMeans((samples, sample_rate), normalize = True)
        self.assertEqual(4, len(means))
        self.assertEqual(1, sample_rate)
        self.assertEqual(0.25, means[0])
        self.assertEqual(.5, means[1])
        self.assertEqual(.75, means[2])
        self.assertEqual(1, means[3])
    def test_calculate_means_float(self):
        sample_rate = 16000
        samples = [1] * sample_rate
        samples = samples + [2] * sample_rate
        samples = samples + [3] * sample_rate
        samples = numpy.array(samples)
        means, sample_rate = rosa.CalculateMeans((samples, sample_rate), segment_duration = 0.01, normalize = False)
        self.assertEqual(300, len(means))
        self.assertEqual(100, sample_rate)
        self.assertTrue(numpy.array_equal([1]*100, means[0:100]))
        self.assertTrue(numpy.array_equal([2]*100, means[100:200]))
        self.assertTrue(numpy.array_equal([3]*100, means[200:300]))
