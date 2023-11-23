#ifndef TIMESTAMP_FILE_HPP
#define TIMESTAMP_FILE_HPP

#include <filesystem>
#include <stdio.h>
#include <sys/file.h>
#include <unistd.h>

namespace timestamp_file
{
  std::string getTimestampLockName(size_t id);
  std::filesystem::path getTimestampLockPath(const std::filesystem::path& dirPath, size_t id);
  void writeCurrentTimestamp(const std::filesystem::path& dirPath, size_t id);
  void writeCurrentTimestamp(int fd);
  
  bool isCurrentTimestampUnderLock(const std::filesystem::path& dirPath, size_t id);
  void writeCurrentTimestampUnderLock(const std::filesystem::path& dirPath, size_t id);
  void removeTimestampFileUnderLock(const std::filesystem::path& dirPath, size_t id);
}

#endif
