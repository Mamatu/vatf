class CommExitCode(Exception):
    def __init__(self, command, path, exitCode, stdout, stderr):
        self.command = command
        self.path = path
        self.exitCode = exitCode
        self.stdout = stdout
        self.stderr = stderr
    def __str__(self):
        def handleStd(name, var):
            return "\n{}: {}".format(name, var.read()) if var else ""
        std = "{}{}".format(handleStd("stdout", self.stdout), handleStd("stderr", self.stderr))
        if self.command != None:
            return "{} {}{}".format(self.command, self.exitCode, std)
        if self.path != None:
            return "{} {}{}".format(self.path, self.exitCode, std)

class Empty:
    def __init__(self):
        pass
    def __call__(self, command):
        raise Exception("Command written into not initialized shell")
    def exec(self):
        pass
    def size(self):
        return 0

class RuntimeShell:
    def __init__(self):
        self.command = ""
        self.commands = []
        self.first = True
    def __call__(self, command):
        if self.first:
            self.first = False
            self("#!/bin/bash\n")
            self("set -x\n")
        self.command = "{}{}".format(self.command, command)
        if self.command[-1] == '\r' or self.command[-1] == '\n':
            self.__appendCmd(self.command)
            self.command = ""
    def __appendCmd(self, command):
        self.commands.append(command)
    def exec(self):
        if len(self.commands) > 0:
            command = "".join(self.commands)
            import subprocess as sub
            p = sub.Popen(command, shell=True, stdout=sub.PIPE, stderr=sub.PIPE, executable='/bin/bash')
            p.wait()
            self.command = []
            if p.returncode != 0:
                raise CommExitCode(command, None, p.returncode, p.stdout, p.stderr)
    def size(self):
        _size = 0
        for fa in self.commands:
            _size = _size + len(self.commands)
        return _size

class BashFile:
    def __init__(self, path = "/tmp/script.sh"):
        self.file = open(path, "w")
        self.path = path
        self.first = True
    def __call__(self, command):
        if self.first:
            self.first = False
            self("#!/bin/bash\n")
            self("set -x\n")
        self.file.write(command)
        self.file.flush()
    def exec(self):
        import subprocess as sub
        p = sub.Popen("bash {}; exit $?".format(self.path), shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
        p.wait()
        if p.returncode != 0:
            raise CommExitCode(None, self.path, p.returncode, p.stdout, p.stderr)
    def size():
        self.file.seek(0, os.SEEK_END)
        return self.file.tell()
