#include "chunk.hpp"

#include "timestamp_file.hpp"

#include <stdexcept>
#include <stdio.h>

Chunk::Chunk(size_t id, size_t linesLimit) : m_id(id), m_linesLimit(linesLimit)
{}

size_t Chunk::write(const char* bytes, size_t length)
{
  openIfClosed();
  auto [lenToTransfer, linesToTransfer] = getLenToTransfer(bytes, length);
  size_t _realLenTransferred = _write(bytes, lenToTransfer);
  if (_realLenTransferred !=  lenToTransfer)
  {
    throw std::runtime_error("Wrong len transferred");
  }
  closeIf(linesToTransfer);
  m_lineIdx += linesToTransfer;
  return _realLenTransferred;
}

void Chunk::openIfClosed()
{
  if (!m_opened)
  {
    _open();
    m_opened = true;
  }
}

void Chunk::closeIf(size_t linesToTransfer)
{
  if (linesToTransfer >= getCurrentLinesLimit())
  {
    _close();
    m_opened = false;
  }
}

Chunk::LenLines Chunk::getLenToTransfer(const char* bytes, size_t length) const
{
  size_t count = 0;
  for (size_t idx = 0; idx < length; ++idx)
  {
    const auto& c = bytes[idx];
    if (c == '\n')
    {
      count++;
      if (count == getCurrentLinesLimit())
      {
        LenLines lenLines;
        lenLines.length = idx + 1;
        lenLines.lines = count;
        return lenLines;
      }
    }
  }
  LenLines lenLines;
  lenLines.length = length;
  lenLines.lines = count;
  return lenLines;
}

size_t Chunk::getId() const
{
  return m_id;
}

int Chunk::getCurrentLinesLimit() const
{
  return m_linesLimit - m_lineIdx;
}
