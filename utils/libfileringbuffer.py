import tempfile
from vatf.executor import shell
from vatf.utils.thread_with_stop import Thread
from pathlib import Path
import os

from vatf.executor import wait

class FileRingBuffer:
    """
    Ringbuffer realized by files in the fs
    """
    def __init__(self, fifo_file, chunks_dir, chunk_lines, chunks_count, timestamp_lock = True):
        self.fifo_file = fifo_file
        self.chunks_dir = chunks_dir
        self.chunk_lines = chunk_lines
        self.chunks_count = chunks_count
        self.bg_process = None
        self.timestamp_lock = 1 if timestamp_lock else 0
    def start(self):
        if not os.path.exists(self.fifo_file):
            shell.fg(f"mkfifo {self.fifo_file}")
        try:
            os.makedirs(self.chunks_dir)
        except:
            pass
        if not os.path.exists(self.chunks_dir):
            raise Exception(f"Chunks dir doesn't exist {self.chunks_dir}")
        vatf_path = Path(__file__).parents[1]
        file_ring_buffer_path = os.path.join(vatf_path, "bin/file_ring_buffer")
        self.bg_process = shell.bg(f"{file_ring_buffer_path} -d {self.chunks_dir} -f {self.fifo_file} -c {self.chunks_count} -l {self.chunk_lines} -t {self.timestamp_lock}")
    def stop(self):
        shell.kill(self.bg_process)
        if os.path.exists(self.fifo_file):
            shell.fg(f"rm {self.fifo_file}")

def make(fifo_file, chunks_dir, chunk_lines, chunks_count, timestamp_lock):
    return FileRingBuffer(fifo_file, chunks_dir, chunk_lines, chunks_count, timestamp_lock)
