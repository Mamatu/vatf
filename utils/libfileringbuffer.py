import tempfile
from vatf.executor import shell
from vatf.utils.thread_with_stop import Thread

import os

from vatf.executor import wait

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
            bg_process = None
            print(f"thread {is_stopped()}")
            while not is_stopped():
                chunk_name = get_chunk_name()
                shell.fg(f"sed -n 1,2p {fifo_file} > {chunk_name}")
                wc_chunk_file = shell.fg(f"wc -l {chunk_name}")
                wc = int(wc_chunk_file.strip(" ")[0])
                print(f"{wc}")
                if wc > chunk_lines:
                    idx = idx + 1
            wait.sleep(10)
        self.thread = Thread(target = target, args = [self.fifo_file, self.chunk_lines, self.chunks_count])
    def start(self, chunks_dir_must_not_exist = False):
        shell.fg(f"mkfifo {self.fifo_file}")
        self.thread.start()
        if self.bg_process is not None:
            raise Exception(f"command {self.bg_process} is not none!")
        self.bg_process = shell.bg(f"{self.command} > {self.fifo_file}")
        try:
            os.makedirs(self.chunks_dir)
        except FileExistsError:
            if chunks_dir_must_not_exist:
                raise Exception("Chunk dir {self.chunks_dir} already exists!")
    def stop(self):
        shell.kill(self.bg_process)
        self.bg_process = None
        self.thread.stop()
        self.thread.join()
        os.remove(self.fifo_file)

def make(command, fifo_file, chunk_lines, chunks_count, chunks_dir):
    return FileRingBuffer(command, fifo_file, chunk_lines, chunks_count, chunks_dir)
