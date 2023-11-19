#ifndef TIMESTAMP_FILE_H
#define TIMESTAMP_FILE_H

#include <filesystem>

namespace timestamp_file
{
  std::string getTimestampLockName(size_t id);
  std::filesystem::path getTimestampLockPath(const std::filesystem::path& dirPath, size_t id);
  void write(const std::filesystem::path& dirPath, size_t id, size_t value);
  void writeCurrentTimestamp(const std::filesystem::path& dirPath, size_t id);
}

#endif
