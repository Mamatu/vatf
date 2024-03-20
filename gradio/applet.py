import pandas as pd
import numpy as np

import gradio as gr

import os
import shutil

from vatf.utils import libaudiocompare

class Session:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.audio = []
        self.samples = []
        self.logs = []
    def __str__(self):
        return self.name

class Test:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.sessions = []
    def __str__(self):
        return self.name

class _Path:
    def __init__(self, path, obj = None):
        self.path = path
        self.obj = obj
    def __str__(self):
        return self.path
    def __repr__(self):
        return self.path
    def __del__(self):
        if self.obj:
            del self.obj
            print("_Path: __del__ {self.path}", file = sys.stderr)
            #shutil.rmtree(self.path)

def get_path(path):
    if not os.path.exists(path):
        raise ValueError(f"Path {path} does not exist")
    import zipfile
    if zipfile.is_zipfile(path):
        print(f"File is zipfile {path}", file = sys.stderr)
        import tempfile
        temp_dir = tempfile.TemporaryDirectory()
        print(f"{temp_dir.name}", file = sys.stderr)
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir.name)
        return _Path(os.path.join(temp_dir.name, "logs/data"), temp_dir)
    return _Path(path)

def iterate_dir(path, callback_dir = None, callback_file = None):
    import os
    for item in os.listdir(str(path)):
        abs_path = os.path.join(str(path), item)
        if os.path.isfile(abs_path):
            if callback_file:
                callback_file(item, abs_path)
        elif os.path.isdir(abs_path):
            if callback_dir:
                callback_dir(item, abs_path)

def iterate_audio(path, session):
    def callback_file(item, path):
        session.audio.append(path)
    iterate_dir(path, callback_file = callback_file)

def iterate_samples(path, session):
    def callback_file(item, path):
        session.samples.append(path)
    iterate_dir(path, callback_file = callback_file)

def iterate_log(path, session):
    def callback_file(item, path):
        session.logs.append(path)
    iterate_dir(path, callback_file = callback_file)

def iterate_session(session, test):
    def callback_dir(item, path):
        if "audio" in item:
            iterate_audio(path, session)
        if "log" in item:
            iterate_log(path, session)
        if "samples" in item:
            iterate_samples(path, session)
    iterate_dir(session.path, callback_dir = callback_dir)

def iterate_test(test):
    def callback_dir(item, path):
        if "session_" in item:
            session = Session(item, path)
            test.sessions.append(session)
            iterate_session(session, test)
    iterate_dir(test.path, callback_dir = callback_dir)

def load_data(path):
    tests = []
    import os
    def callback_dir(item, path):
        if "test_" in item:
            test = Test(item, path)
            tests.append(test)
            iterate_test(test)
    iterate_dir(path, callback_dir = callback_dir)
    return tests

def compare_samples_in_sessions(test):
    lens = []
    outputs = {}
    for session in test.sessions:
        lens.append(len(session.samples))
    max_len = max(lens)
    audio_data = {}
    for idx in range(max_len):
        audio_data[idx] = []
        for session in test.sessions:
            if idx < len(session.samples):
                audio_data[idx].append(session.samples[idx])
    for idx in range(max_len):
        output = libaudiocompare.init_audio_data_from_files(audio_data[idx])
        output = libaudiocompare.calculate_mfcc(output)
        output = libaudiocompare.calculate_alignment(output)
        outputs[idx] = output
    return outputs

import matplotlib.pyplot as plt

def create_app(tests):
    app = gr.Blocks()
    with app:
        for test in tests:
            with gr.Accordion(test.name, open = False):
                audio_data = compare_samples_in_sessions(test)
                for session in test.sessions:
                    with gr.Accordion(session.name, open = False):
                        for sample in session.samples:
                            value = None
                            for key in audio_data.keys():
                                if sample in audio_data[key]:
                                    _distances = [alignment.normalizedDistance for key1, alignment in audio_data[key][sample].alignments.items()]
                                    if len(_distances) > 0:
                                        value = sum(_distances) / float(len(_distances))
                            label = str(sample.split("/")[-1])
                            if value:
                                label = f"{label}: (mean distance: {value})"
                            with gr.Accordion(label, open = False):
                                if not value:
                                    gr.Audio(sample, label = label)
                                else:
                                    gr.Audio(sample, label = label)
                                    #gr.Label(value = value)
                        for log in session.logs:
                            gr.File(log)
    return app

if __name__ == "__main__":
    path = None
    import atexit
    def exit_handler():
        if path:
            shutil.rmtree(str(path))
    #atexit.register(exit_handler)
    import sys
    path = get_path(sys.argv[1])
    print(f"Path: {path}")
    tests = load_data(path)
    app = create_app(tests)
    app.launch()
