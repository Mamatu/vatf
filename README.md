# Voice Assitance Test Framework - Executor

> :warning: recomended version of python should be > 3.6. Tested are 3.6, 3.7, 3.8, 3.9 versions

This part of vatf is used in test script to execute test.

Executor launches playing audio files, audio inputs and outputs of test station recording, sampling and sleep test code. 

> test station is any device where vatf is launched. It can be self-tested (testing application on test station) or can test external device.

# Voice Assitance Test Framework - Generator

> :warning: recomended version of python should be > 3.6. Tested are 3.6, 3.7, 3.8, 3.9 versions

This part of vatf provides modules to create custom test scenario for voice assistance.

They include playing audio files, audio inputs and outputs of test station recording, sampling and sleep test code. 

> test station is any device where vatf is launched. It can be self-tested (testing application on test station) or can test external device.

# Voice Assitance Test Framework - Utils

> :warning: recomended version of python should be > 3.6. Tested are 3.6, 3.7, 3.8, 3.9 versions

This part of vatf contains common utilities which can be used in vatf_executor and vatf_generator.

> test station is any device where vatf is launched. It can be self-tested (testing application on test station) or can test external device.

#### Dependencies

Remember about update all submodules

```
git submodule update --init --recursive --remote --force
```

```
apt install parallel libsndfile1
```
```
pip install librosa psutil jsonschema matplotlib watchdog
```
