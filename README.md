# Voice Assistance Test Framework

> :warning: recomended version of python is >= 3.8. Unittest are runned on 3.6, 3.7, 3.8, 3.9 versions, but production is developed on python 3.8

## Voice Assistance Test Framework - Executor
This part of vatf is used in test script to execute test.

Executor launches playing audio files, audio inputs and outputs of test station recording, sampling and sleeps test code. 

> test station is any device where vatf is launched. It can be self-tested (testing application on test station) or can test external device.

## Voice Assistance Test Framework - Utils
This part of vatf contains common utilities which are used in vatf.executor and vatf.generator.

> test station is any device where vatf is launched. It can be self-tested (testing application on test station) or can test external device.

### Dependencies

To get actual list of dependencies please look at .github/workflows/python.yaml

### vatf init
In every test file is required to import `vatf_init.py` which initializes starndard executor api.

### wait\_for\_regex
wait\_for\_regex is mechaninsm to wait for specific regex in the log.

There are two modes how this mechanism work:
1) command - if can be used any specific command which provides the log from tested device from the moment of running that command
2) log/chunks - this mode creates
