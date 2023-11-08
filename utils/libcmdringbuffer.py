import tempfile
from vatf.executor import shell
from vatf.utils import libfileringbuffer

import os

from vatf.executor import wait

class CmdRingBuffer:
    def __init__(self, command, fifo_file, chunks_dir, chunk_lines, chunks_count, redirection_operator = ">"):
        self.command = command
        self.fifo_file = fifo_file
        self.redirection_operator = redirection_operator
        self.fileringbuffer = libfileringbuffer.make(fifo_file, chunks_dir, chunk_lines, chunks_count)
        self.bg_process = None
    def start(self):
        if not os.path.exists(self.fifo_file):
            shell.fg(f"mkfifo {self.fifo_file}")
        self.bg_process = shell.bg(f"{self.command} {self.redirection_operator} {self.fifo_file}")
        self.fileringbuffer.start()
    def stop(self):
        shell.kill(self.bg_process)
        self.fileringbuffer.stop()
        if os.path.exists(self.fifo_file):
            shell.fg(f"rm {self.fifo_file}")

def make(command, fifo_file, chunks_dir, chunk_lines, chunks_count):
    return CmdRingBuffer(command, fifo_file, chunks_dir, chunk_lines, chunks_count)
