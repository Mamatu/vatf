import tempfile
from vatf.executor import shell
from vatf.utils.thread_with_stop import Thread

import os

from vatf.executor import wait

class FileRingBuffer:
    """
    Ringbuffer realized by files in the fs
    """
    def __init__(self, fifo_file, chunks_dir, chunk_lines, chunks_count):
        self.fifo_file = fifo_file
        self.chunks_dir = chunks_dir
        self.chunk_lines = chunk_lines
        self.chunks_count = chunks_count
    def start(self):
        self.bg_process = shell.bg(f"bin/file_ring_buffer -d {self.chunks_dir} -f {self.fifo_file} -c {self.chunks_count} -l {self.chunk_lines}")
    def stop(self):
        shell.kill(self.bg_process)

def make(fifo_file, chunks_dir, chunk_lines, chunks_count):
    return FileRingBuffer(fifo_file, chunks_dir, chunk_lines, chunks_count)
