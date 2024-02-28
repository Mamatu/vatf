#include <array>
#include <csignal>
#include <stdio.h>
#include <fcntl.h>
#include <getopt.h>
#include <string.h>
#include <stdexcept>
#include <memory>

#include <cstddef>
#include <vector>
#include <thread>

#include <sstream>

#include "chunk_file.hpp"
#include "file_ring.hpp"
#include "error.hpp"

struct FileRingSignal
{
  public:
    std::shared_ptr<FileRing> m_fileRing;
};


FileRingSignal frSignal;

void signalHandler(int signum)
{
  if (frSignal.m_fileRing)
  {
    frSignal.m_fileRing->stop();
  }
}

int main(int argc, char* argv[])
{
  signal(SIGTERM, signalHandler);
  std::string fifoPath = "";
  std::string chunksDirPath = "";
  int chunksCount = 0;
  int chunkLines = 0;
  size_t bufferKB = 1024;
  bool timestampLock = false;
  int opt = -1;
  bool keepFiles = false;
  while ((opt = getopt(argc, argv, "d:f:c:l:t:k")) != -1)
  {
    switch (opt)
    {
      case 'd': chunksDirPath = optarg; continue;
      case 'f': fifoPath = optarg; continue;
      case 'c': chunksCount = std::stoi(optarg); continue;
      case 'l': chunkLines = std::stoi(optarg); continue;
      case 't': timestampLock = static_cast<bool>(std::stoi(optarg)); continue;
      case 'k': keepFiles = true; continue;
      break;
    };
  }

  error(!fifoPath.empty(), "fifoPath cannot be empty"); 
  error(!chunksDirPath.empty(), "chunksDirPath cannot be empty"); 
  error(chunksCount != 0, "chunksCount cannot be 0"); 
  error(chunkLines != 0, "chunkLines cannot be 0"); 

  auto fileRing = std::make_shared<FileRing>(chunksDirPath, fifoPath, chunksCount, chunkLines, timestampLock, keepFiles);
  frSignal.m_fileRing = fileRing;
  fileRing->start();
  return 0;
}
