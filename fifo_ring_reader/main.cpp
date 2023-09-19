#include <csignal>
#include <stdio.h>
#include <fcntl.h>
#include <string.h>
#include <exception>
#include <stdexcept>
#include <memory>

#include <cstddef>
#include <vector>
#include <iostream>

void error(bool cond, const std::string& msg)
{
  if (!cond)
  {
    throw std::runtime_error(msg);
  }
}

bool stopExecution = false;

void signalHandler(int signum)
{
  stopExecution = true;
}

class Fifo final
{
  public:
    Fifo(const std::string& path) : fd(open(path.c_str(), O_RDONLY /*| O_ASYNC*/)) {}
    ~Fifo() {
      close(fd);
    }
    int get() const {
      return fd;
    }
  private:
    int fd = 0;
};

int main(int argc, char* argv[])
{
  signal(SIGTERM, signalHandler);
  std::string fifoPath = "";
  std::string chunksDirPath = "";
  int chunksCount = 0;
  int chunkLines = 0;
  size_t bufferKB = 1024;
  int opt = -1;
  while ((opt = getopt(argc, argv, "d:f:c:l:b:")) != -1)
  {
    switch (opt)
    {
      case 'd': chunksDirPath = optarg; continue;
      case 'f': fifoPath = optarg; continue;
      case 'c': chunksCount = std::stoi(optarg); continue;
      case 'l': chunkLines = std::stoi(optarg); continue;
      case 'b': bufferKB = std::stoi(optarg); continue;
      break;
    };
  }

  error(!fifoPath.empty(), "fifoPath cannot be empty"); 
  error(!chunksDirPath.empty(), "chunksDirPath cannot be empty"); 
  error(chunksCount != 0, "chunksCount cannot be 0"); 
  error(chunkLines != 0, "chunkLines cannot be 0"); 

  auto fclose = [](int fd){ return close(fd); };
  std::cout << __FILE__ << " " << __LINE__ << std::endl;
  Fifo fifo(fifoPath);

  constexpr size_t count = 1024;
  std::byte buffer[count];
  std::vector<std::byte> bytes/*(1024 * bufferKB)*/;
  bytes.reserve(1024 * bufferKB);
  while(!stopExecution) 
  {
    std::cout << __FILE__ << " " << __LINE__ << std::endl;
    ssize_t ccount = read(fifo.get(), buffer, count);
    error (!(ccount < 0), "ccount is lower than zero!");
    bytes.insert(bytes.end(), std::begin(buffer), std::begin(buffer) + ccount);
    std::cout << ccount << std::endl;
    std::cout << reinterpret_cast<char*>(bytes.data()) << std::endl;
    memset(buffer, 0, count);
    bytes.clear();
  }
  return 0;
}
