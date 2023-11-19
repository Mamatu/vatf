#include "fifo_linux.h"

#include <fcntl.h>
#include <string>
#include <unistd.h>
#include <stdio.h>

FifoLinux::FifoLinux(const std::string& path) : Fifo(path), fd(::open(path.c_str(), O_RDONLY | O_CREAT)) {
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
