import pandas as pd
import numpy as np

import gradio as gr

import os

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

def get_path(path):
    if not os.path.exists(path):
        raise ValueError(f"Path {path} does not exist")
    import zipfile
    if zipfile.is_zipfile(path):
        import tempfile
        temp_dir = tempfile.TemporaryDirectory()
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir.name)
        return temp_dir.name
    return path

def iterate_dir(path, callback_dir = None, callback_file = None):
    import os
    for item in os.listdir(path):
        abs_path = os.path.join(path, item)
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
        output = libaudiocompare.calculate_aligment(output)
        outputs[idx] = output
    return outputs

def create_matrix(audio_data):
    matrix = []
    for idx in audio_data:
        row = []
        for idx2 in audio_data:
            if idx == idx2:
                row.append(0)
            else:
                row.append(audio_data[idx].compare(audio_data[idx2]))
        matrix.append(row)
    return matrix

def create_app(tests):
    app = gr.Blocks()
    with app:
        for test in tests:
            with gr.Accordion(test.name, open = False):
                audio_data = compare_samples_in_sessions(test)
                #audio_matrix = create_matrix(audio_data)
                gr.DataFrame(value = [[1, 2, 3], [1, 2, 3], [1, 2, 3]])
                for session in test.sessions:
                    with gr.Accordion(session.name, open = False):
                        for sample in session.samples:
                            gr.Audio(sample)
                        for log in session.logs:
                            gr.File(log)
    return app

if __name__ == "__main__":
    import sys
    path = get_path(sys.argv[1])
    tests = load_data(path)
    app = create_app(tests)
    app.launch()
