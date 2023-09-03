#include <csignal>
#include <stdio.h>
#include <fcntl.h>
#include <string.h>
#include <exception>
#include <memory>

#include <cstddef>

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

int main(int argc, char* argv[])
{
  signal(SIGTERM, signalHandler);
  std::string fifoPath = "";
  std::string chunksDirPath = "";
  int chunksCount = 0;
  int chunkLines = 0;
  size_t bufferKB = 1024;
  for (;;)
  {
    switch (getopt(argc, argv, "d:f:c:l:b:"))
    {
      case 'd': chunksDirPath = optarg; continue;
      case 'f': fifoPath = optarg; continue;
      case 'c': chunksCount = std::stoi(optarg); continue;
      case 'l': chunksLine = std::stoi(optarg); continue;
      case 'b': bufferKB = std::stoi(optarg); continue;
      break;
    };
  }

  error(!fifoPath.empty(), "fifoPath cannot be empty"); 
  error(!chunksDirPath.empty(), "chunksDirPath cannot be empty"); 
  error(chunksCount != 0, "chunksCount cannot be 0"); 
  error(chunkLines != 0, "chunkLines cannot be 0"); 

  std::unique_ptr<int> fifo = nullptr;
  fifo = std::unique_ptr<int>(open(fifoPath.c_str(), O_RDONLY | O_ASYNC), [](int fifo){ close(fifo); });

  constexpr size_t count = 1024;
  std::byte buffer[count];
  std::vector<std::byte> bytes(1024 * bufferKB);

  while(!stopExecution) 
  {
    ssize_t ccount = read(fifo.get(), buffer, count);
    error (!(ccount < 0), "ccount is lower than zero!");
    bytes.insert(bytes.end(), std::begin(buffer), std::begin(buffer) + ccount);
  }
  return 0;
}
