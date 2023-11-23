#ifndef FIFO_LINUX_HPP
#define FIFO_LINUX_HPP

#include "fifo.hpp"

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
