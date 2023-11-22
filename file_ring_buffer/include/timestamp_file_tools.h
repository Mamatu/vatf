#ifndef TIMESTAMP_FILE_H
#define TIMESTAMP_FILE_H

#include <filesystem>
#include <stdio.h>
#include <sys/file.h>
#include <unistd.h>

namespace timestamp_file
{

  class Fd final
  {
    public:
      Fd(const std::string& path, int mode) { m_fd = open(path.c_str(), mode); }
      ~Fd() { close(m_fd); }
    
      int get() const { return m_fd; }
    private:
      int m_fd = 0;
  };

  template<typename Callback>
  void flockFile(Callback&& callback, int fd)
  {
    class Flock final
    {
      public:
        Flock(int fd) : m_fd(fd) { while (0 != flock(fd, LOCK_EX)) {} }
        ~Flock() { flock(m_fd, LOCK_UN); close(m_fd); }
      private:
        int m_fd;
    };
    Flock flock(fd);
    callback();
  }

  std::string getTimestampLockName(size_t id);
  std::filesystem::path getTimestampLockPath(const std::filesystem::path& dirPath, size_t id);
  Fd openfd(const std::filesystem::path& dirPath, size_t id, int mode);
  void write(const std::filesystem::path& dirPath, size_t id, size_t value);
  void writeCurrentTimestamp(const std::filesystem::path& dirPath, size_t id);
  
  bool existsCurrentTimestampUnderLock(const std::filesystem::path& dirPath, size_t id);
  void writeCurrentTimestampUnderLock(const std::filesystem::path& dirPath, size_t id);
  void removeTimestampFileUnderLock(const std::filesystem::path& dirPath, size_t id);
}

#endif
