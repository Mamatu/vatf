#include "chunk_file.h"

ChunkFile::ChunkFile(const std::string& path, size_t linesLimit) : Chunk(linesLimit), m_path(path)
{
}

void ChunkFile::_open()
{
  m_file = fopen(m_path.c_str(), "w+");
}

void ChunkFile::_close()
{
  fclose(m_file);
}

size_t ChunkFile::_write(const char* buffer, size_t length)
{
  return fwrite(buffer, sizeof(char), length, m_file);
}
