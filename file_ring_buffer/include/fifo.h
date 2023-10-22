#ifndef FIFO_H
#define FIFO_H

#include <cstddef>
#include <string>

class Fifo
{
  public:
    Fifo(const std::string& path);
    virtual ~Fifo() = default;

    virtual size_t read(void* buffer, size_t len) = 0;

    void setUserData(void* userData = nullptr) {
      m_userData = userData;
    }

    void* getUserData() {
      return m_userData;
    }

  private:
    void* m_userData;
    std::string m_path;
};

#endif
