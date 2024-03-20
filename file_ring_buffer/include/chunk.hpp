#ifndef CHUNK_HPP
#define CHUNK_HPP

#include <string>
#include <utility>

class Chunk
{
  public:
    Chunk(size_t id, size_t linesLimit, bool keepFiles);
    virtual ~Chunk() = default;
    size_t write(const char* bytes, size_t length);

    size_t getId() const;
    int getCurrentLinesLimit() const;

    virtual bool canBeRemoved() const = 0;

  protected:
    void openIfClosed();
    void closeIf(size_t linesToTransfer);
    bool keepFiles() const;

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
    bool m_keepFiles = false;
    std::string m_chunkTimestampLockName;
};

#endif
