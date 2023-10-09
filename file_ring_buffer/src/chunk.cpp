#include "chunk.h"

#include <stdexcept>
#include <stdio.h>

Chunk::Chunk(size_t linesLimit) : m_linesLimit(linesLimit)
{}

size_t Chunk::write(const char* bytes, size_t length)
{
  openIfClosed();
  auto [lenToTransfer, linesToTransfer] = getLenToTransfer(bytes, length);
  size_t _len = _write(bytes, lenToTransfer);
  if (_len !=  lenToTransfer)
  {
    throw std::runtime_error("Wrong len transferred");
  }
  closeIf(linesToTransfer);
  m_lineIdx += linesToTransfer;
  return _len;
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

size_t Chunk::getCurrentLinesLimit() const
{
  return m_linesLimit - m_lineIdx;
}
