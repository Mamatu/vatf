#include "timestamp_file_tools.h"
#include "error.h"

#include <chrono>
#include <stdio.h>
#include <sstream>

namespace timestamp_file
{
  class File final
  {
    public:
      File(const std::string& path, const std::string& mode) { m_file = fopen(path.c_str(), mode.c_str()); }
      ~File() { fclose(m_file); }

      FILE* get() const
      {
        return m_file;
      }
    private:
      FILE* m_file;
  };

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

  void write(const std::filesystem::path& dirPath, size_t id, size_t value)
  {
    std::stringstream sstream;
    sstream << id << ".timestamp.lock";
    std::filesystem::path path = dirPath / sstream.str();
    File file(path.c_str(), "w");
    size_t count = fwrite(reinterpret_cast<void*>(&value), sizeof(value), 1, file.get());
    fflush(file.get());
    error(count == 1, "written count is not 1");
  }

  void writeCurrentTimestamp(const std::filesystem::path& dirPath, size_t id)
  {
    const auto now = std::chrono::system_clock::now();
    size_t timestamp = std::chrono::duration_cast<std::chrono::seconds>(now.time_since_epoch()).count();   
    timestamp_file::write(dirPath, id, timestamp);
  }
}
