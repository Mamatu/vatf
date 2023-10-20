#include "chunk_file.h"

#include <cstdio>

ChunkFile::ChunkFile(const std::string& path, size_t linesLimit) : Chunk(linesLimit), m_path(path)
{
}

ChunkFile::~ChunkFile()
{
  close();
  remove(m_path.c_str());
}

void ChunkFile::_open()
{
  m_file = fopen(m_path.c_str(), "w+");
}

void ChunkFile::_close()
{
  close();
}

void ChunkFile::close()
{
  if (!m_isClosed) {
    fclose(m_file);
    m_isClosed = true;
  }
}

size_t ChunkFile::_write(const char* buffer, size_t length)
{
  std::string m(buffer, length);
  fprintf(stderr, "\n");
  fprintf(stderr, "%s\n", m_path.c_str());
  fprintf(stderr, "%s", m.c_str());
  auto writeSize = fwrite(buffer, sizeof(char), length, m_file);
  fflush(m_file);
  return writeSize;
}
