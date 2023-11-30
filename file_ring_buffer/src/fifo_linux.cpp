#include "fifo_linux.hpp"
#include "thrower.hpp"

#include <cstring>
#include <fcntl.h>
#include <string>
#include <unistd.h>
#include <stdio.h>
#include <errno.h>

FifoLinux::FifoLinux(const std::string& path) : Fifo(path)
{
  fd = ::open(path.c_str(), O_RDONLY);
  throw_exception_ifnot(fd > 0, [this](auto& in)
  {
    in << __FUNCTION__ << " " << __LINE__ << " fd = " << fd << " " << std::strerror(errno); 
  });
}

FifoLinux::~FifoLinux()
{
  ::close(fd);
}

int FifoLinux::getFd() const
{
  return fd;
}

size_t FifoLinux::read(void* buffer, size_t bufferLen)
{
  return ::read(fd, buffer, bufferLen);
}
