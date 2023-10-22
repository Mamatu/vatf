#include "fifo_linux.h"

#include <fcntl.h>
#include <string>
#include <unistd.h>

FifoLinux::FifoLinux(const std::string& path) : Fifo(path), fd(::open(path.c_str(), O_RDONLY /*| O_NONBLOCK*/)) {}

FifoLinux::~FifoLinux()
{
  ::close(fd);
}

size_t FifoLinux::read(void* buffer, size_t bufferLen)
{
  return ::read(fd, buffer, bufferLen);
}
