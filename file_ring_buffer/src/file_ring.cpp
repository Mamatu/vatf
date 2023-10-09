#include "chunk_file.h"
#include "file_ring.h"
#include "error.h"

#include <array>
#include <csignal>
#include <stdio.h>
#include <fcntl.h>
#include <string.h>
#include <vector>
#include <iostream>

class Fifo final
{
  public:
    Fifo(const std::string& path) : fd(open(path.c_str(), O_RDONLY /*| O_NONBLOCK*/)) {}

    ~Fifo() {
      close(fd);
    }

    int get() const {
      return fd;
    }

  private:
    int fd = 0;
};

FileRing::FileRing(const std::string& chunksDirPath, const std::string& fifoPath, size_t chunksCount, size_t linesLimit) :
        m_chunksDirPath(chunksDirPath), m_fifoPath(fifoPath), m_chunksCount(chunksCount), m_linesLimit(linesLimit)
{
}

void FileRing::start()
{
  std::cout << __FILE__ << " " << __LINE__ << std::endl;
  Fifo fifo(m_fifoPath);

  constexpr size_t count = 1024;
  std::array<char, count> buffer;
  std::vector<char> bytes/*(1024 * bufferKB)*/;
  

  size_t chunksCounter = 0;
  auto getPath = [&chunksCounter, this]() {
    std::stringstream sstream;
    sstream << m_chunksDirPath;
    sstream << "/";
    sstream << m_chunksCounter;
    return sstream.str();
  };

  auto chunk = createChunk(getPath());

  while(!m_isStopped) 
  {
    ssize_t ccount = read(fifo.get(), buffer.data(), count);
    std::stringstream msg;
    msg << "ccount is lower than zero: " << ccount;
    error (!(ccount < 0), msg);
    if (ccount > 0)
    {
      auto len = chunk->write(buffer.data(), buffer.size());
      if (len < buffer.size())
      {
        m_chunksCounter++;
        chunk = createChunk(getPath());
      }
      memset(buffer.data(), 0, count);
      bytes.clear();
    }
  }
}

void FileRing::stop()
{
  m_isStopped = true;
}

std::unique_ptr<Chunk> FileRing::createChunk(const std::string& path)
{
  return std::make_unique<ChunkFile>(path, m_linesLimit);
}
