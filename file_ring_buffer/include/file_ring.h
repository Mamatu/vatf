#ifndef FILE_RING_H
#define FILE_RING_H

#include "chunk.h"
#include "fifo.h"

#include <string>
#include <sstream>
#include <memory>

class FileRing
{
  public:
    FileRing(const std::string& chunksDirPath, const std::string& fifoPath, size_t chunksCount, size_t linesLimit);

    void start();
    void stop();

    std::string getChunksDirPath() const;
    std::string getFifoPath() const;
    size_t getChunksCount() const;
    size_t getLinesLimit() const;

  protected:
    virtual std::shared_ptr<Chunk> createChunk(const std::string& path);
    virtual std::unique_ptr<Fifo> createFifo(const std::string& path);

  private:
    std::string m_chunksDirPath;
    std::string m_fifoPath;
    size_t m_chunksCount;
    size_t m_linesLimit;
    bool m_isStopped = false;
    size_t m_chunksCounter = 0;
};

#endif
