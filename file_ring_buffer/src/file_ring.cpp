#include "chunk_file.h"
#include "fifo_linux.h"
#include "file_ring.h"
#include "error.h"

#include <array>
#include <csignal>
#include <stdio.h>
#include <string.h>
#include <list>
#include <vector>
#include <iostream>

FileRing::FileRing(const std::string& chunksDirPath, const std::string& fifoPath, size_t chunksCount, size_t linesLimit) :
        m_chunksDirPath(chunksDirPath), m_fifoPath(fifoPath), m_chunksCount(chunksCount), m_linesLimit(linesLimit)
{
}

void FileRing::start()
{
  std::cout << __FILE__ << " " << __LINE__ << std::endl;
  auto fifo = createFifo(m_fifoPath);

  std::array<char, 1024> buffer;
  std::vector<char> bytes/*(1024 * bufferKB)*/;

  auto getPath = [this]() {
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
    ssize_t bufferSizeWithData = fifo->read(buffer.data(), buffer.size());
    std::stringstream msg;
    msg << "bufferSizeWithData is lower than zero: " << bufferSizeWithData;
    error (!(bufferSizeWithData < 0), msg);
    if (bufferSizeWithData == 0) { continue; }
    
    ssize_t len = 0;
    while (bufferSizeWithData - len > 0)
    {
      if (!chunk)
      {
        chunk = createChunk(getPath());  
      }
      len = len + chunk->write(buffer.data() + len, bufferSizeWithData - len);
      if (chunk->getCurrentLinesLimit() <= 0)
      {
        m_chunksCounter++;
        chunks.push_back(std::move(chunk));
      }
    }
    memset(buffer.data(), 0, buffer.size());
    bytes.clear();
  }
}

void FileRing::stop()
{
  m_isStopped = true;
}

std::string FileRing::getChunksDirPath() const
{
  return m_chunksDirPath;
}

std::string FileRing::getFifoPath() const
{
  return m_fifoPath;
}

size_t FileRing::getChunksCount() const
{
  return m_chunksCount;
}

size_t FileRing::getLinesLimit() const
{
  return m_linesLimit;
}

std::shared_ptr<Chunk> FileRing::createChunk(const std::string& path)
{
  return std::make_shared<ChunkFile>(path, m_linesLimit);
}

std::unique_ptr<Fifo> FileRing::createFifo(const std::string& path)
{
  return std::make_unique<FifoLinux>(path);
}
