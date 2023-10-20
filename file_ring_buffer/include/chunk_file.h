#ifndef CHUNK_FILE_H
#define CHUNK_FILE_H

#include "chunk.h"
#include <stdio.h>

class ChunkFile : public Chunk
{
  public:
    ChunkFile(const std::string& path, size_t linesLimit);
    virtual ~ChunkFile();

  protected:
    void _open() override;
    void _close() override;
    size_t _write(const char* buffer, size_t length) override;

    size_t getLenToTransfer(const char* bytes, size_t length) const;
    size_t getLinesLimit() const;

  private:
    bool m_isClosed = false;
    void close();
    std::string m_path;
    FILE* m_file;
};

#endif
