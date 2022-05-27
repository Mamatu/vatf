# Voice Assistance Test Framework

> :warning: recomended version of python is >= 3.8. Unittest are runned on 3.6, 3.7, 3.8, 3.9 versions, but production is developed on python 3.8

## Voice Assistance Test Framework - Executor
This part of vatf is used in test script to execute test.

Executor launches playing audio files, audio inputs and outputs of test station recording, sampling and sleeps test code. 

> test station is any device where vatf is launched. It can be self-tested (testing application on test station) or can test external device.

## Voice Assistance Test Framework - Generator
This part of vatf provides modules to create custom test scenario for voice assistance.

They include playing audio files, audio inputs and outputs of test station recording, sampling and sleep test code. 

> test station is any device where vatf is launched. It can be self-tested (testing application on test station) or can test external device.

## Voice Assistance Test Framework - Utils
This part of vatf contains common utilities which can be used in vatf_executor and vatf_generator.

> test station is any device where vatf is launched. It can be self-tested (testing application on test station) or can test external device.

#### Dependencies

Remember about update all submodules

```
apt install parallel libsndfile1
pip install librosa psutil jsonschema matplotlib watchdog
git submodule update --init --recursive --remote --force
```
