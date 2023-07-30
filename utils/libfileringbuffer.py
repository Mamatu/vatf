import tempfile
from vatf.executor import shell
from vatf.utils.thread_with_stop import Thread

import os

class FileRingBuffer:
    """
    Ringbuffer realized by files in the fs
    """
    def __init__(self, command, fifo_file, chunk_lines, chunks_count, chunks_dir):
        self.command = command
        self.fifo_file = fifo_file
        self.chunk_lines = chunk_lines
        self.chunks_count = chunks_count
        self.chunks_dir = chunks_dir
        self.bg_process = None
        def target(fifo_file, chunk_lines, chunks_count, is_stopped):
            idx = 0
            get_chunk_name = lambda: os.path.join(self.chunks_dir, f"chunk_{idx}.log")
            chunk_file = get_chunk_name()
            while not is_stopped():
                shell.fg(f"cat {fifo_file} >> {chunk_file}")
                wc_chunk_file = shell.fg(f"wc -l {chunk_file}")
                wc = int(wc_chunk_file.strip(" ")[0])
                if wc > chunk_lines:
                    idx = idx + 1
                    chunk_file = get_chunk_name()
        self.thread = Thread(target = target, args = [self.fifo_file, self.chunk_lines, self.chunks_count])
    def start(self, chunks_dir_must_not_exist = False):
        self.bg_process = shell.bg(f"mkfifo {self.fifo_file}; {self.command} > {self.fifo_file}")
        try:
            os.makedirs(self.chunks_dir)
        except FileExistsError:
            if chunks_dir_must_not_exist:
                raise Exception("Chunk dir {self.chunks_dir} already exists!")
        self.thread.start()
    def stop(self):
        shell.kill(self.bg_process)
        self.thread.stop()
        os.remove(self.fifo_file)

def make(command, fifo_file, chunk_lines, chunks_count, chunks_dir):
    return FileRingBuffer(command, fifo_file, chunk_lines, chunks_count, chunks_dir)
