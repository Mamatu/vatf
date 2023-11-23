#include "chunk_file.hpp"
#include "timestamp_file_tools.hpp"

#include <filesystem>
#include <sstream>

ChunkFile::ChunkFile(const std::string& dirpath, size_t id, size_t linesLimit, bool timestampLock) : Chunk(id, linesLimit), m_dirpath(dirpath), m_timestampLock(timestampLock)
{
  std::stringstream sstream;
  sstream << id;
  std::filesystem::path path = m_dirpath;
  path = path / sstream.str();
  m_filepath = path;
}

ChunkFile::~ChunkFile()
{
  close();
  if (m_timestampLock)
  {
    //timestamp_file::removeTimestampFileUnderLock(m_dirpath, getId());
  }
  std::filesystem::remove(getFilePath().c_str());
}

std::string ChunkFile::getFilePath() const
{
  return m_filepath;
}

void ChunkFile::_open()
{
  const auto& filepath = getFilePath();
  m_file = fopen(filepath.c_str(), "w+");
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
  auto writeSize = fwrite(buffer, sizeof(char), length, m_file);
  fflush(m_file);
  if (m_timestampLock)
  {
    timestamp_file::writeCurrentTimestampUnderLock(m_dirpath, getId());
  }
  return writeSize;
}

bool ChunkFile::canBeRemoved() const
{
  if (!m_timestampLock)
  {
    return true;
  }
  const bool exists = timestamp_file::isCurrentTimestampUnderLock(m_dirpath, getId());
  return !exists;
}
