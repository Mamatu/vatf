import tempfile

class FileRingBuffer:
    """
    Ringbuffer realized by files in the fs
    """
    def __init__(self, ringbuffer_timeout, chunks_count):
        self.ringbuffer_timeout = ringbuffer_timeout
        self.chunks_count = chunks_count
        self.chunk_timeout = self.ringbuffer_timeout / self.chunks_count
    def start(self):
