#ifndef CHUNK_H
#define CHUNK_H

#include <string>
#include <utility>

class Chunk
{
  public:
    Chunk(size_t id, size_t linesLimit);
    virtual ~Chunk() = default;
    size_t write(const char* bytes, size_t length);

    size_t getId() const;
    int getCurrentLinesLimit() const;

    virtual bool canBeRemoved() const = 0;

  protected:
    void openIfClosed();
    void closeIf(size_t linesToTransfer);

    virtual void _open() = 0;
    virtual void _close() = 0;
    virtual size_t _write(const char* buffer, size_t length) = 0;

    struct LenLines
    {
      size_t length;
      size_t lines;  
    };
    LenLines getLenToTransfer(const char* bytes, size_t length) const;

  private:
    bool m_opened = false;
    size_t m_lineIdx = 0;
    size_t m_id;
    size_t  m_linesLimit = 0;
    std::string m_chunkTimestampLockName;
};

#endif
