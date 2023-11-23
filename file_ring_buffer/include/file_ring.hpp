#ifndef FILE_RING_HPP
#define FILE_RING_HPP

#include "chunk.hpp"
#include "fifo.hpp"
#include "callbacks.hpp"

#include <functional>
#include <list>
#include <memory>
#include <string>
#include <sstream>

class FileRing
{
  public:
    FileRing(const std::string& chunksDirPath, const std::string& fifoPath, size_t chunksCount, size_t linesLimit, bool timestampLock);

    void start();
    void stop();

    std::string getChunksDirPath() const;
    std::string getFifoPath() const;
    size_t getChunksCount() const;
    size_t getLinesLimit() const;

    Callbacks<int>& onFifoOpen()
    {
      return m_openCallbacks;
    }

  protected:
    virtual std::shared_ptr<Chunk> createChunk(const std::string& path, size_t id);
    virtual std::unique_ptr<Fifo> createFifo(const std::string& path);

    template<typename Chunks>
    static void removeOldChunks(Chunks& chunks, size_t chunksCount)
    {
      if (chunksCount >= chunks.size())
      {
        return;
      }
      ssize_t _chunksCount = chunksCount;
      auto it = chunks.begin();
      auto eit = chunks.end();
      std::advance(eit, -_chunksCount);
      for (; it != eit && it != chunks.end();)
      {
        if ((*it)->canBeRemoved())
        {
          it = chunks.erase(it);
        }
        else
        {
          it++;
        }
      }
    }

  private:
    std::string m_chunksDirPath;
    std::string m_fifoPath;
    size_t m_chunksCount;
    size_t m_linesLimit;
    bool m_isStopped = false;
    size_t m_chunksCounter = 0;
    bool m_timestampLock = false;

    CallbacksCall<int> m_openCallbacks;
};

#endif
