#include <array>
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
#include <thread>

#include <sstream>

#include "chunk_file.h"

void error(bool cond, const std::string& msg)
{
  if (!cond)
  {
    throw std::runtime_error(msg);
  }
}

void error(bool cond, const std::stringstream& msg)
{
  error(cond, msg.str());
}

bool stopExecution = false;

void signalHandler(int signum)
{
  stopExecution = true;
}

class Fifo final
{
  public:
    Fifo(const std::string& path) : fd(open(path.c_str(), O_RDONLY /*| O_NONBLOCK*/)) {}
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

  std::cout << __FILE__ << " " << __LINE__ << std::endl;
  Fifo fifo(fifoPath);

  constexpr size_t count = 1024;
  std::array<char, count> buffer;
  std::vector<char> bytes/*(1024 * bufferKB)*/;
  
  size_t chunksCounter = 0;
  auto getPath = [&chunksCounter, chunksDirPath]() {
    std::stringstream sstream;
    sstream << chunksDirPath;
    sstream << "/";
    sstream << chunksCounter;
    return sstream.str();
  };
  auto chunk = std::make_unique<ChunkFile>(getPath(), chunkLines);
  while(!stopExecution) 
  {
    ssize_t ccount = read(fifo.get(), buffer.data(), count);
    std::stringstream msg;
    msg << "ccount is lower than zero: " << ccount;
    error (!(ccount < 0), msg);
    if (ccount > 0)
    {
      //std::cout << reinterpret_cast<char*>(buffer.data());
      //chunk->write(buffer.data(), buffer.size()); 
      memset(buffer.data(), 0, count);
      bytes.clear();
    }
  }
  return 0;
}
