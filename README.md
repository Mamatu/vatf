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
This part of vatf contains common utilities which are used in vatf.executor and vatf.generator.

> test station is any device where vatf is launched. It can be self-tested (testing application on test station) or can test external device.

### Dependencies

Remember about update all submodules

```
apt install parallel libsndfile1
pip install librosa psutil jsonschema matplotlib watchdog
git submodule update --init --recursive --remote --force
```

### Generator and executor
Generator part allows to generate specific test or tests suite in specific directory. This directory can be transferred into specific test device, where tests are executed.
All recordings, logs and etc. for the test are stored in this directory. Test code is executed in generator with overloaded vatf api (functions with @public\_api decorator) by
"empty implementation" only for syntax and errors verification.
