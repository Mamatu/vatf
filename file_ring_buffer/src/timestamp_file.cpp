#include "timestamp_file.hpp"
#include "thrower.hpp"

#include <errno.h>
#include <cstring>
#include <chrono>
#include <thread>
#include <stdio.h>
#include <sstream>

#include <sys/file.h>

#include <limits>

namespace timestamp_file
{
  class Fd final
  {
    public:
      Fd(const std::string& path, int mode)
      {
        m_fd = open(path.c_str(), mode, 0744);
        throw_exception_ifnot(m_fd > 0, [this, path, mode](auto& in)
        {
          in << __FILE__ << " " << __LINE__ << " fd = " << m_fd << " path = "
          << path << " mode = " << mode << " " << std::strerror(errno);
        });
      }

      ~Fd() { close(m_fd); }
    
      int getFd() const { return m_fd; }

    private:
      int m_fd = 0;
  };

  class File final
  {
    public:
      File(const std::string& path, const std::string& mode)
      {
        m_file = fopen(path.c_str(), mode.c_str());
        throw_exception_ifnot(m_file != nullptr, [&path, &mode](auto& in)
        {
          in << __FILE__ << " " << __LINE__
          << " path = " << path << " mode = " << mode << " " << std::strerror(errno);
        });
      }

      File(int fd, const std::string& mode)
      {
        m_file = fdopen(fd, mode.c_str());
        throw_exception_ifnot(m_file != nullptr, [fd, &mode](auto& in)
        {
          in << __FILE__ << " " << __LINE__
          << " fd = " << fd << " mode = " << mode << " " << std::strerror(errno);
        });
      }

      File(const std::shared_ptr<Fd>& fd, const std::string& mode)
      {
        m_file = fdopen(fd->getFd(), mode.c_str());
        throw_exception_ifnot(m_file != nullptr, [&fd, &mode](auto& in)
        {
          in << __FILE__ << " " << __LINE__
          << " fd = " << fd->getFd() << " mode = " << mode << " " << std::strerror(errno);
        });
      }

      ~File() { fclose(m_file); }

      template<typename T>
      void write(T t, bool flush = false)
      {
        size_t count = fwrite(reinterpret_cast<void*>(&t), sizeof(t), 1, m_file);
        throw_exception_ifnot(count == 1, [count](auto& in)
        {
          in << __FILE__ << " " << __LINE__ << " count = " << count << " " << std::strerror(errno);
        });
        if (flush)
        {
          fflush(m_file);
        }
      }

      template<typename T>
      void read(T& t)
      {
        size_t count = fread(reinterpret_cast<void*>(&t), sizeof(t), 1, m_file);
        throw_exception_ifnot(count == 1, [](auto& in)
        {
          in << __FILE__ << " " << __LINE__ << " " << std::strerror(errno);
        });
      }

      FILE* getFile() const
      {
        return m_file;
      }

    private:
      FILE* m_file;
      void error(FILE* file)
      {
        throw_exception_ifnot(file != nullptr, [](auto& in)
        {
          in << __FILE__ << " " << __LINE__ << " " << std::strerror(errno);
        });
      }
  };

  template<typename Callback>
  void flockFile(Callback&& callback, const std::shared_ptr<Fd>& fd)
  {
    class Flock final
    {
      public:
        Flock(int fd) : m_fd(fd)
        {
          fprintf(stderr, "%s %s %d fd = %d\n",__FUNCTION__, __FILE__, __LINE__, fd);
          while (true)
          {
            auto ret = flock(m_fd, LOCK_EX);
            throw_exception_ifnot(ret == 0, [this](auto& in)
            {
              in << __FILE__ << " " << __LINE__ << " fd = " << m_fd << " " << std::strerror(errno);
            });
            if (ret == 0) { break; }
            using namespace std::chrono_literals;
            std::this_thread::sleep_for(5ms);
          }
          fprintf(stderr, "%s %s %d fd = %d\n",__FUNCTION__, __FILE__, __LINE__, fd);
        }

        ~Flock()
        {
          fprintf(stderr, "%s %s %d fd = %d\n",__FUNCTION__, __FILE__, __LINE__,m_fd);
          //flock(m_fd, LOCK_UN);
          close(m_fd);
          fprintf(stderr, "%s %s %d fd = %d\n",__FUNCTION__, __FILE__, __LINE__,m_fd);
        }

      private:
        int m_fd = -1;
    };
    Flock flock(fd->getFd());
    callback(fd->getFd());
  }

  std::string getTimestampLockName(size_t id)
  {
    std::stringstream sstream;
    sstream << id << ".timestamp.lock";
    return sstream.str();
  }

  std::filesystem::path getTimestampLockPath(const std::filesystem::path& dirPath, size_t id)
  {
    const auto& tlName = getTimestampLockName(id);
    std::filesystem::path path = dirPath / tlName;
    return path;
  }

  std::shared_ptr<Fd> openfd(const std::filesystem::path& dirPath, size_t id, int mode, bool waitForOpen = false)
  {
    const auto& tlPath = getTimestampLockPath(dirPath, id);
    std::shared_ptr<Fd> fd = nullptr;
    bool isFirstInvocation = false;
    while (true)
    {
      try
      {
        fd = std::make_shared<Fd>(tlPath.c_str(), mode);
        fprintf(stderr, "%s %s %d fd = %d path = %s mode = %d\n",__FUNCTION__, __FILE__, __LINE__, fd->getFd(), tlPath.c_str(), mode);
        return fd;
      } catch (const std::runtime_error& error)
      {
        if (!isFirstInvocation && waitForOpen)
        {
          fprintf(stderr, "EXCEPTION %s %s %d path = %s, mode = %d\n", __FUNCTION__, __FILE__, __LINE__, tlPath.c_str(), mode);
          isFirstInvocation = true;
        }
        if (!waitForOpen)
        {
          throw error;
        }
        using namespace std::chrono_literals;
        std::this_thread::sleep_for(10ms);
      }
    }
    return fd;
  }

  void writeCurrentTimestamp(const std::filesystem::path& dirPath, size_t id)
  {
    const auto now = std::chrono::system_clock::now();
    size_t timestamp = std::chrono::duration_cast<std::chrono::seconds>(now.time_since_epoch()).count();   
    const auto& tlPath = getTimestampLockPath(dirPath, id);
    File file(tlPath.c_str(), "wb");
    file.write(timestamp, true);
  }

  void writeCurrentTimestamp(int fd)
  {
    const auto now = std::chrono::system_clock::now();
    size_t timestamp = std::chrono::duration_cast<std::chrono::seconds>(now.time_since_epoch()).count();   
    File file(fd, "wb");
    file.write(timestamp, true);
  }

  bool isCurrentTimestampUnderLock(const std::filesystem::path& dirPath, size_t id)
  {
    const auto& tlPath = getTimestampLockPath(dirPath, id); 
    fprintf(stderr, "%s %s %d %s\n",__FUNCTION__, __FILE__, __LINE__, tlPath.c_str());
    std::shared_ptr<Fd> fd = nullptr;
    try
    {
      fd = openfd(dirPath, id, O_RDWR);
    } catch(const std::runtime_error& error)
    {
      return false;
    }
    bool exists = false;
    fprintf(stderr, "%s %s %d\n",__FUNCTION__, __FILE__, __LINE__);
    if (fd)
    {
      flockFile([&tlPath, &exists](int fd)
      {
        exists = std::filesystem::exists(tlPath);
        if (exists)
        {
          File file(fd, "r+b");
          constexpr auto maxSize = std::numeric_limits<size_t>::max();
          size_t timestamp = maxSize;
          file.read(timestamp);
          exists =  (timestamp > 0 && timestamp < maxSize);
        }
      }, fd);
    }
    fprintf(stderr, "%s %s %d exists = %d \n",__FUNCTION__, __FILE__, __LINE__, exists);
    return exists;
  }

  void writeCurrentTimestampUnderLock(const std::filesystem::path& dirPath, size_t id)
  {
    const auto& tlPath = getTimestampLockPath(dirPath, id); 
    fprintf(stderr, "%s %s %d %s\n",__FUNCTION__, __FILE__, __LINE__, tlPath.c_str());
    auto fd = openfd(dirPath, id, O_RDWR | O_CREAT, true);
    fprintf(stderr, "%s %s %d fd = %d\n",__FUNCTION__, __FILE__, __LINE__, fd->getFd());
    flockFile([](int fd) { writeCurrentTimestamp(fd); }, fd);
    fprintf(stderr, "%s %s %d\n",__FUNCTION__, __FILE__, __LINE__);
  }

  void removeTimestampFileUnderLock(const std::filesystem::path& dirPath, size_t id)
  {
    const auto& tlPath = getTimestampLockPath(dirPath, id); 
    fprintf(stderr, "%s %s %d %s\n",__FUNCTION__, __FILE__, __LINE__, tlPath.c_str());
    auto fd = openfd(dirPath, id, O_RDWR | O_CREAT, true);
    fprintf(stderr, "%s %s %d\n",__FUNCTION__, __FILE__, __LINE__);
    flockFile([tlPath](int) {
                    fprintf(stderr, "REMOVE %s %s %d %s\n",__FUNCTION__, __FILE__, __LINE__, tlPath.c_str());
                    std::filesystem::remove(tlPath);
                    }, fd);
    fprintf(stderr, "%s %s %d\n",__FUNCTION__, __FILE__, __LINE__);
  }
}
