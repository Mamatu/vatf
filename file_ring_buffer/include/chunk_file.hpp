#ifndef CHUNK_FILE_HPP
#define CHUNK_FILE_HPP

#include "chunk.hpp"
#include <stdio.h>

class ChunkFile : public Chunk
{
  public:
    ChunkFile(const std::string& dirpath, size_t id, size_t linesLimit, bool keepFiles, bool timestampLock);
    virtual ~ChunkFile();

    std::string getFilePath() const;
    bool canBeRemoved() const override;

  protected:
    void _open() override;
    void _close() override;
    size_t _write(const char* buffer, size_t length) override;

    size_t getLenToTransfer(const char* bytes, size_t length) const;
    size_t getLinesLimit() const;

  private:
    bool m_isClosed = false;
    void close();
    std::string m_dirpath;
    std::string m_filepath;
    FILE* m_file;
    bool m_timestampLock = false;
};

#endif
