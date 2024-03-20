#include <gtest/gtest.h>
#include <gmock/gmock.h>

#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>

#include <unistd.h>

#include <chrono>
#include <thread>
#include <list>
#include <vector>

#include "error.hpp"
#include "thrower.hpp"
#include "file_ring.hpp"
#include "fifo_linux.hpp"

#include <filesystem>

#include <condition_variable>

namespace file_ring_tests {

using namespace testing;

class FileRingTests : public Test
{};

class ChunkMock : public Chunk
{
  public:
    ChunkMock(const std::string& path, size_t id, size_t linesLimit) : Chunk(id, linesLimit, false), m_path(path) {}

    Chunk::LenLines getLenToTransfer(const char* bytes, size_t length) const
    {
      return Chunk::getLenToTransfer(bytes, length);
    }

    size_t getCurrentLinesLimit() const
    {
      return Chunk::getCurrentLinesLimit();
    }

    void _open() override {}
    void _close() override {}

    size_t _write(const char* buffer, size_t length) override
    {
      std::string bufferStr(buffer, length);
      m_data += bufferStr;
      return length;
    }

    bool canBeRemoved() const override
    {
      return true;
    }

    std::string m_path;
    std::string m_data;
};

using ChunkMocks = std::vector<std::shared_ptr<ChunkMock>>;
using ChunkMocksList = std::list<std::shared_ptr<ChunkMock>>;

class TestFileRing : public FileRing
{
  public:
    TestFileRing(const std::string& chunksDirPath, const std::string& fifoPath, size_t chunksCount, size_t linesLimit, const ChunkMocks& chunkMocks) : 
      FileRing(chunksDirPath, fifoPath, chunksCount, linesLimit, false), m_chunkMocks(chunkMocks)
    {}

    std::shared_ptr<Chunk> createChunk(const std::string& path, size_t id, bool) override
    {
      if (m_chunkMocks.size() <= m_chunkIdx)
      {
        std::stringstream sstream;
        sstream << "Too low number of chunks in m_chunkMocks m_chunksMocks.size() == " << m_chunkMocks.size() << " ";
        sstream << "m_chunkIdx " << m_chunkIdx;
        throw std::runtime_error(sstream.str());
      }
      auto mock = m_chunkMocks[m_chunkIdx];
      m_chunkIdx++;
      return mock;
    }
 
    std::unique_ptr<Fifo> createFifo(const std::string& path) override
    {
      return std::make_unique<FifoLinux>(path);
    }

    template<typename Chunks>
    static void removeOldChunks(Chunks& chunks, size_t chunksCount)
    {
      FileRing::removeOldChunks(chunks, chunksCount);
    }
  private:
    ChunkMocks m_chunkMocks;
    size_t m_chunkIdx = 0;
};

class FifoWriter
{
  public:
    FifoWriter(const std::string& path) : m_path(path)
    {}

    void write(const std::string& data)
    {
      struct Fd final
      {
        Fd(const std::string& path)
        {
          m_fd = ::open(path.c_str(), O_WRONLY /*| O_NONBLOCK*/);
        }

        ~Fd()
        {
          ::close(m_fd);
        }

        int m_fd = 0;
      };

      Fd fd(m_path);
      ssize_t size = ::write(fd.m_fd, data.data(), data.size() * sizeof(char));
      throw_exception_ifnot(size == data.size() * sizeof(char), [size, &data](auto& in)
      {
        in << __FILE__ << " " << __FUNCTION__ << " size = " << size << " data.size = " << data.size();
      });
    }

    void writeLines (size_t count)
    {
      std::stringstream sstream;
      for (size_t idx = 0; idx < count; ++idx)
      {
        sstream << "line_" << idx << std::endl;
      }
      this->write(sstream.str());
    }

  private:
    std::string m_path;
};

std::string generateLines (size_t min, size_t max)
{
  std::stringstream sstream;
  for (size_t idx = min; idx < max; ++idx)
  {
    sstream << "line_" << idx << std::endl;
  }
  return sstream.str();
}

TEST_F(FileRingTests, test_remove_old_chunks_1)
{
  size_t linesLimit = 100;

  ChunkMocksList list;
  list.push_back(std::make_shared<ChunkMock>("chunk0", 0, linesLimit));
  list.push_back(std::make_shared<ChunkMock>("chunk1", 1, linesLimit)); 
  list.push_back(std::make_shared<ChunkMock>("chunk2", 2, linesLimit));

  TestFileRing::removeOldChunks(list, 2);
  ASSERT_EQ(2, list.size());
  auto it = list.begin();
  EXPECT_EQ((*it)->getId(), 1);
  it++;
  EXPECT_EQ((*it)->getId(), 2);
}

TEST_F(FileRingTests, test_remove_old_chunks_2)
{
  size_t linesLimit = 100;

  ChunkMocksList list;
  list.push_back(std::make_shared<ChunkMock>("chunk0", 0, linesLimit));
  list.push_back(std::make_shared<ChunkMock>("chunk1", 1, linesLimit)); 
  list.push_back(std::make_shared<ChunkMock>("chunk2", 2, linesLimit));

  TestFileRing::removeOldChunks(list, 1);
  ASSERT_EQ(1, list.size());
  auto it = list.begin();
  EXPECT_EQ((*it)->getId(), 2);
}

TEST_F(FileRingTests, test_1)
{
  using namespace std::chrono_literals;
  namespace fs = std::filesystem;

  size_t linesLimit = 100;

  fs::path tmp = fs::temp_directory_path();
  fs::path dir = tmp / "file_ring_buffer";
  std::filesystem::remove_all(dir);

  ChunkMocks cmocks;
  cmocks.push_back(std::make_shared<ChunkMock>("chunk0", 0, linesLimit));
  cmocks.push_back(std::make_shared<ChunkMock>("chunk1", 1, linesLimit)); 
  cmocks.push_back(std::make_shared<ChunkMock>("chunk2", 2, linesLimit));

  fs::path fifoPath =  dir / "fifo";
  ASSERT_TRUE(fs::create_directories(dir));
  ASSERT_TRUE(0 == mkfifo(fifoPath.c_str(), S_IWUSR | S_IRUSR));
  fprintf(stderr, "%s %s %d %s\n", __FUNCTION__, __FILE__, __LINE__, fifoPath.c_str());

  std::condition_variable cv;
  std::mutex mutex;
  bool opened = false;
 
  TestFileRing testFileRing(dir / "chunks", fifoPath, 3, linesLimit, cmocks);

  auto thread = std::thread([&testFileRing](){ testFileRing.start(); });

  FifoWriter fifoWriter(fifoPath);
  fifoWriter.writeLines(300);

  std::this_thread::sleep_for(2s);

  auto dataChunk1 = generateLines(0, 100);
  auto dataChunk2 = generateLines(100, 200);
  auto dataChunk3 = generateLines(200, 300);

  EXPECT_EQ(dataChunk1, cmocks[0]->m_data);
  EXPECT_EQ(dataChunk2, cmocks[1]->m_data);
  EXPECT_EQ(dataChunk3, cmocks[2]->m_data);
  testFileRing.stop();
  thread.join();
}

TEST_F(FileRingTests, test_2)
{
  using namespace std::chrono_literals;
  namespace fs = std::filesystem;

  size_t linesLimit = 100;

  fs::path tmp = fs::temp_directory_path();
  fs::path dir = tmp / "file_ring_buffer";
  std::filesystem::remove_all(dir);

  ChunkMocks cmocks;
  cmocks.push_back(std::make_shared<ChunkMock>("chunk0", 0, linesLimit));
  cmocks.push_back(std::make_shared<ChunkMock>("chunk1", 1, linesLimit)); 
  cmocks.push_back(std::make_shared<ChunkMock>("chunk2", 2, linesLimit));
  cmocks.push_back(std::make_shared<ChunkMock>("chunk3", 3, linesLimit));

  fs::path fifoPath =  tmp / "file_ring_buffer/fifo";
  ASSERT_TRUE(fs::create_directories(dir));
  ASSERT_TRUE(0 == mkfifo(fifoPath.c_str(), S_IWUSR | S_IRUSR));

  std::condition_variable cv;
  std::mutex mutex;
  bool opened = false;

  TestFileRing testFileRing(dir / "chunks", fifoPath, 3, linesLimit, cmocks);
  auto thread = std::thread([&testFileRing](){ testFileRing.start(); });

  FifoWriter fifoWriter(fifoPath);
  fifoWriter.writeLines(400);

  std::this_thread::sleep_for(2s);

  auto dataChunk1 = generateLines(0, 100);
  auto dataChunk2 = generateLines(100, 200);
  auto dataChunk3 = generateLines(200, 300);
  auto dataChunk4 = generateLines(300, 400);

  EXPECT_EQ(dataChunk1, cmocks[0]->m_data);
  EXPECT_EQ(dataChunk2, cmocks[1]->m_data);
  EXPECT_EQ(dataChunk3, cmocks[2]->m_data);
  EXPECT_EQ(dataChunk4, cmocks[3]->m_data);
  testFileRing.stop();
  thread.join();
}

TEST_F(FileRingTests, test_3)
{
  using namespace std::chrono_literals;
  namespace fs = std::filesystem;

  size_t linesLimit = 100;

  fs::path tmp = fs::temp_directory_path();
  fs::path dir = tmp / "file_ring_buffer";
  std::filesystem::remove_all(dir);

  ChunkMocks cmocks;
  cmocks.push_back(std::make_shared<ChunkMock>("chunk0", 0, linesLimit));
  cmocks.push_back(std::make_shared<ChunkMock>("chunk1", 1, linesLimit)); 
  cmocks.push_back(std::make_shared<ChunkMock>("chunk2", 2, linesLimit));
  cmocks.push_back(std::make_shared<ChunkMock>("chunk3", 3, linesLimit));
  cmocks.push_back(std::make_shared<ChunkMock>("chunk4", 4, linesLimit));
  cmocks.push_back(std::make_shared<ChunkMock>("chunk5", 5, linesLimit)); 
  cmocks.push_back(std::make_shared<ChunkMock>("chunk6", 6, linesLimit));
  cmocks.push_back(std::make_shared<ChunkMock>("chunk7", 7, linesLimit));
  cmocks.push_back(std::make_shared<ChunkMock>("chunk8", 8, linesLimit));

  fs::path fifoPath =  tmp / "file_ring_buffer/fifo";
  ASSERT_TRUE(fs::create_directories(dir));
  ASSERT_TRUE(0 == mkfifo(fifoPath.c_str(), S_IWUSR | S_IRUSR));

  std::condition_variable cv;
  std::mutex mutex;
  bool opened = false;

  TestFileRing testFileRing(dir / "chunks", fifoPath, 3, linesLimit, cmocks);
  auto thread = std::thread([&testFileRing](){ testFileRing.start(); });

  FifoWriter fifoWriter(fifoPath);
  fifoWriter.writeLines(900);

  std::this_thread::sleep_for(2s);

  auto dataChunk1 = generateLines(0, 100);
  auto dataChunk2 = generateLines(100, 200);
  auto dataChunk3 = generateLines(200, 300);
  auto dataChunk4 = generateLines(300, 400);
  auto dataChunk5 = generateLines(400, 500);
  auto dataChunk6 = generateLines(500, 600);
  auto dataChunk7 = generateLines(600, 700);
  auto dataChunk8 = generateLines(700, 800);
  auto dataChunk9 = generateLines(800, 900);

  EXPECT_EQ(dataChunk1, cmocks[0]->m_data);
  EXPECT_EQ(dataChunk2, cmocks[1]->m_data);
  EXPECT_EQ(dataChunk3, cmocks[2]->m_data);
  EXPECT_EQ(dataChunk4, cmocks[3]->m_data);
  EXPECT_EQ(dataChunk5, cmocks[4]->m_data);
  EXPECT_EQ(dataChunk6, cmocks[5]->m_data);
  EXPECT_EQ(dataChunk7, cmocks[6]->m_data);
  EXPECT_EQ(dataChunk8, cmocks[7]->m_data);
  EXPECT_EQ(dataChunk9, cmocks[8]->m_data);
  testFileRing.stop();
  thread.join();
}
}
