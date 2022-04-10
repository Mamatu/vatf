from pysh import core
import os

class BackgroundProcess:
    Counter = 0
    def __init__(self, command, killSig = 9, pidDir = "/tmp/"):
        self.command = command
        self.killSig = killSig
        self.pidDir = pidDir
        self.pidFile = None
    def launchCmd(self):
        cmd = core.Command()
        cmd.cmdStr("{} &".format(str(self.command)))
        cmd.cmdNL()
        cmd.cmdStr("sleep 0.2")
        cmd.cmdNL()
        return cmd
    def pidCmd(self):
        self.pidFile = "tf_{}.pid".format(BackgroundProcess.Counter)
        self.pidFile = os.path.join(self.pidDir, self.pidFile)
        pidCmd = "echo $! > {}".format(self.pidFile)
        cmd = core.Command()
        cmd.cmdStr(pidCmd)
        cmd.cmdNL()
        BackgroundProcess.Counter = BackgroundProcess.Counter + 1
        return cmd
    def killCmd(self):
        if self.pidFile == None:
            raise Exception ("PID is not storred anywhere")
        killCmd = "ls {1} && kill -{0} $(cat {1}) && rm {1}".format(self.killSig, self.pidFile)
        cmd = core.Command()
        cmd.cmdStr(killCmd)
        cmd.cmdNL()
        return cmd
    def getPidFile(self):
        return self.pidFile
    def launch(self):
        cmd = core.Command()
        cmd.cmdStr(self.launchCmd())
        cmd.cmdStr(self.pidCmd())
        return cmd
    def run(self):
        return self.launch()
    def kill(self):
        cmd = core.Command()
        cmd.cmdStr(self.killCmd())
        return cmd
