#include "chunk_file.hpp"
#include "fifo_linux.hpp"
#include "file_ring.hpp"
#include "error.hpp"

#include <array>
#include <csignal>
#include <filesystem>
#include <stdio.h>
#include <string.h>
#include <list>
#include <vector>

FileRing::FileRing(const std::string& chunksDirPath, const std::string& fifoPath, size_t chunksCount, size_t linesLimit, bool timestampLock, bool keepFiles) :
        m_chunksDirPath(chunksDirPath),
        m_fifoPath(fifoPath),
        m_chunksCount(chunksCount),
        m_linesLimit(linesLimit),
        m_timestampLock(timestampLock),
        m_keepFiles(keepFiles)
{
}

void FileRing::start()
{
  auto fifo = createFifo(m_fifoPath);
  int fd = fifo->getFd();
  m_openCallbacks.call(fd);

  std::array<char, 1024> buffer;
  std::vector<char> bytes/*(1024 * bufferKB)*/;

  auto getPath = [this]() {
    return std::make_pair(m_chunksDirPath, m_chunksCounter);
  };

  std::shared_ptr<Chunk> chunk = nullptr;
  std::list<std::shared_ptr<Chunk>> chunks;

  auto removeOldChunks = [&chunks, this]()
  {
    if (!m_keepFiles) {
        FileRing::removeOldChunks(chunks, m_chunksCount);
    }
  };

  while(!m_isStopped) 
  {
    removeOldChunks();
    ssize_t bufferSizeWithData = fifo->read(buffer.data(), buffer.size());
    std::stringstream msg;
    msg << "bufferSizeWithData is lower than zero: " << bufferSizeWithData;

    //error (!(bufferSizeWithData < 0), msg);
    if (bufferSizeWithData <= 0) { continue; }

    ssize_t len = 0;
    while (bufferSizeWithData - len > 0)
    {
      if (!chunk)
      {
        const auto& pathId = getPath();
        chunk = createChunk(pathId.first, pathId.second, m_keepFiles);
        chunks.push_back(chunk);
      }
      len = len + chunk->write(buffer.data() + len, bufferSizeWithData - len);
      if (chunk->getCurrentLinesLimit() <= 0)
      {
        m_chunksCounter++;
        chunk = nullptr;
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

std::shared_ptr<Chunk> FileRing::createChunk(const std::string& path, size_t id, bool keepFiles)
{
  return std::make_shared<ChunkFile>(path, id, m_linesLimit, keepFiles, m_timestampLock);
}

std::unique_ptr<Fifo> FileRing::createFifo(const std::string& path)
{
  return std::make_unique<FifoLinux>(path);
}
