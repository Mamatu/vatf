#include "chunk_file.h"
#include "file_ring.h"
#include "error.h"

#include <array>
#include <csignal>
#include <stdio.h>
#include <fcntl.h>
#include <string.h>
#include <list>
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

  std::array<char, 1024> buffer;
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
  std::list<std::shared_ptr<Chunk>> chunks;

  auto removeOldChunks = [&chunks, this]()
  {
    while (chunks.size() >= m_chunksCount)
    {
      chunks.pop_front();
    }
  };

  while(!m_isStopped) 
  {
    removeOldChunks();
    ssize_t ccount = read(fifo.get(), buffer.data(), buffer.size());
    std::stringstream msg;
    msg << "ccount is lower than zero: " << ccount;
    error (!(ccount < 0), msg);
    if (ccount > 0)
    {
      auto len = chunk->write(buffer.data(), ccount);
      if (len < ccount)
      {
        m_chunksCounter++;
        chunks.push_back(std::move(chunk));
        chunk = createChunk(getPath());
        chunk->write(buffer.data() + len, ccount - len);
      }
      else if (len == ccount && chunk->getCurrentLinesLimit() == 0)
      {
        m_chunksCounter++;
        chunks.push_back(std::move(chunk));
        chunk = createChunk(getPath());
      }
      memset(buffer.data(), 0, buffer.size());
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
