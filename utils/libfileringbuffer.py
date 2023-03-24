import tempfile
from vatf.executor import shell
from vatf.utils.thread_with_stop import Thread

class FileRingBuffer:
    """
    Ringbuffer realized by files in the fs
    """
    def __init__(self, command, fifo_file, ringbuffer_timeout_or_lines, wait_timeout, chunks_dir,  chunks_count = 10):
        self.command = command
        self.fifo_file = fifo_file
        self.ringbuffer_timeout_or_lines = ringbuffer_timeout_or_lines
        self.chunks_count = chunks_count
        self.chunk_timeout = self.ringbuffer_timeout / self.chunks_count
        self.wait_timeout = wait_timeout
        self.chunks_dir = chunks_dir
        self.bg_process = None
        def target(fifo_file, chunks_count, wait_timeout, is_stopped):
            while not is_stopped():
                shell.bg(f"cat {fifo_file} > ")
                pass
        self.thread = Thread(target = target, args = [self.fifo_file, self.chunks_count, self.wait_timeout])
    def start(self):
        self.bg_process = shell.bg(f"mkfifo {self.fifo_file}; {self.command} > {self.fifo_file}")

    def stop(self):
        shell.kill(self.bg_process)
        self.thread.stop()
