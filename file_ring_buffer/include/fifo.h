#ifndef FIFO_H
#define FIFO_H

#include <cstddef>
#include <string>

class Fifo
{
  public:
    Fifo(const std::string& path);
    virtual ~Fifo() = default;
  
    virtual int getFd() const = 0;
    virtual size_t read(void* buffer, size_t len) = 0;
    
  private:
    std::string m_path;
};

#endif
