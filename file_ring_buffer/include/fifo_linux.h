#ifndef FIFO_LINUX_H
#define FIFO_LINUX_H

#include "fifo.h"

class FifoLinux : public Fifo
{
  public:
    FifoLinux(const std::string& path);

    ~FifoLinux() override;

    int getFd() const override;
    size_t read(void* buffer, size_t bufferLen) override;
  private:
    int fd = 0;
};

#endif
