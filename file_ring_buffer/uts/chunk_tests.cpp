#include <gtest/gtest.h>
#include <gmock/gmock.h>

#include "chunk.hpp"

namespace chunk_tests {

using namespace testing;

class ChunkTests : public Test
{};

class ChunkMock : public Chunk
{
  public:
    ChunkMock(size_t id, size_t linesLimit) : Chunk(id, linesLimit) {}

    Chunk::LenLines getLenToTransfer(const char* bytes, size_t length) const
    {
      return Chunk::getLenToTransfer(bytes, length);
    }

    size_t getCurrentLinesLimit() const
    {
      return Chunk::getCurrentLinesLimit();
    }

    bool canBeRemoved() const override
    {
      return true;
    }

    MOCK_METHOD(void, _open, (), (override));
    MOCK_METHOD(void, _close, (), (override));
    MOCK_METHOD(size_t, _write, (const char* buffer, size_t length), (override));
};

TEST_F(ChunkTests, emptyBuffer) {
  ChunkMock chunk(0, 1);
  std::string buffer = "";
  EXPECT_CALL(chunk, _write(_, _)).Times(1).WillOnce(Return(buffer.size()));
  EXPECT_CALL(chunk, _open()).Times(1);
  EXPECT_CALL(chunk, _close()).Times(0);
  auto lenLines = chunk.getLenToTransfer(buffer.c_str(), buffer.size());
  ASSERT_EQ(buffer.size(), lenLines.length);
  ASSERT_EQ(0, chunk.write(buffer.c_str(), buffer.size()));
}

TEST_F(ChunkTests, 1lineBuffer) {
  ChunkMock chunk(0, 1);
  std::string buffer = "a\n";
  EXPECT_CALL(chunk, _write(_, _)).Times(1).WillOnce(Return(buffer.size()));
  EXPECT_CALL(chunk, _open()).Times(1);
  EXPECT_CALL(chunk, _close()).Times(1);
  auto lenLines = chunk.getLenToTransfer(buffer.c_str(), buffer.size());
  ASSERT_EQ(buffer.size(), lenLines.length);
  ASSERT_EQ(buffer.size(), chunk.write(buffer.c_str(), buffer.size()));
}

TEST_F(ChunkTests, 3linesBuffer3linesLimit2buffers) {
  ChunkMock chunk(0, 3);
  std::string buffer1 = "a\nb\n";
  std::string buffer2 = "c\n";
  EXPECT_CALL(chunk, _write(buffer1.data(), buffer1.size())).Times(1).WillOnce(Return(buffer1.size()));
  EXPECT_CALL(chunk, _write(buffer2.data(), buffer2.size())).Times(1).WillOnce(Return(buffer2.size()));
  EXPECT_CALL(chunk, _open()).Times(1);
  EXPECT_CALL(chunk, _close()).Times(1);
  auto lenLines = chunk.getLenToTransfer(buffer1.c_str(), buffer1.size());
  ASSERT_EQ(4, lenLines.length);
  ASSERT_EQ(2, lenLines.lines);
  lenLines = chunk.getLenToTransfer(buffer2.c_str(), buffer2.size());
  ASSERT_EQ(2, lenLines.length);
  ASSERT_EQ(1, lenLines.lines);
  ASSERT_EQ(buffer1.size(), chunk.write(buffer1.c_str(), buffer1.size()));
  ASSERT_EQ(buffer2.size(), chunk.write(buffer2.c_str(), buffer2.size()));
}

TEST_F(ChunkTests, 3linesBuffer2linesLimit) {
  ChunkMock chunk(0, 2);
  std::string subbuffer = "a\nb\n";
  std::string buffer = subbuffer + "c\n";
  EXPECT_CALL(chunk, _write(buffer.data(), subbuffer.size())).Times(1).WillOnce(Return(subbuffer.size()));
  EXPECT_CALL(chunk, _open()).Times(1);
  EXPECT_CALL(chunk, _close()).Times(1);
  auto lenLines = chunk.getLenToTransfer(buffer.c_str(), buffer.size());
  ASSERT_EQ(4, lenLines.length);
  ASSERT_EQ(2, lenLines.lines);
  ASSERT_EQ(subbuffer.size(), chunk.write(buffer.c_str(), buffer.size()));
}
}
