from enum import Enum

class Format(Enum):
    s16be = 1,
    s16ne = 2,
    s16le = 3,
    s32be = 4,
    s32ne = 5,
    s32le = 6,

class AudioConfig:
    def __init__(self, fformat, channels, framerate):
        if isinstance(fformat, str):
            formatMap = {}
            for f in Format:
                formatMap[f.name] = f
            if fformat not in formatMap.keys():
                raise "f{fformat} is not proper format"
            fformat = formatMap[fformat]
        if isinstance(channels, str):
            channels = int(channels)
        if isinstance(framerate, str):
            framerate = int(framerate)
        self._format = fformat
        self._channels = channels
        self._framerate = framerate
        self._formats = {
            Format.s16be : 2,
            Format.s16ne : 2,
            Format.s16le : 2,
            Format.s32be : 4,
            Format.s32ne : 4,
            Format.s32le : 4,
        }
    @staticmethod
    def ParseArg(arg):
        args = arg.split(",")
        return AudioConfig(args[0], args[1], args[2])
    def getFormat(self):
        return self._format.name
    def getSampleWidth(self):
        return self._formats[self._format]
    def getFramerate(self):
        return self._framerate
    def getChannels(self):
        return self._channels
    def __str__(self):
        fformat = self.getFormat()
        channels = self.getChannels()
        framerate = self.getFramerate()
        return f"{fformat},{channels},{framerate}"
