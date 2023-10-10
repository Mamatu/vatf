import tempfile
from vatf.executor import shell
from vatf.utils import libfileringbuffer

import os

from vatf.executor import wait

class CmdRingBuffer:
    def __init__(self, command, fifo_file, chunks_dir, chunk_lines, chunks_count):
        self.command = command
        self.fifo_file = fifo_file
        self.fileringbuffer = libfileringbuffer.make(fifo_file, chunks_dir, chunk_lines, chunks_count)
    def start(self):
        self.bg_process = shell.bg(f"{self.command} > {self.fifo_file}")
        self.fileringbuffer.start()
    def stop(self):
        shell.kill(self.bg_process)
        self.fileringbuffer.stop()

def make(command, fifo_file, chunks_dir, chunk_lines, chunks_count):
    return CmdRingBuffer(command, fifo_file, chunks_dir, chunk_lines, chunks_count)
