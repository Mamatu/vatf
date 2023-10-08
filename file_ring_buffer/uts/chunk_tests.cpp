#include <gtest/gtest.h>
#include <gmock/gmock.h>

#include "chunk.h"

using namespace testing;

class ChunkTests : public Test
{
  public:

};

class ChunkMock : public Chunk
{
  public:
    ChunkMock(size_t linesLimit) : Chunk(linesLimit) {}

    Chunk::LenLines getLenToTransfer(const char* bytes, size_t length) const
    {
      return Chunk::getLenToTransfer(bytes, length);
    }

    size_t getCurrentLinesLimit() const
    {
      return Chunk::getCurrentLinesLimit();
    }

    MOCK_METHOD(void, _open, (), (override));
    MOCK_METHOD(void, _close, (), (override));
    MOCK_METHOD(size_t, _write, (const char* buffer, size_t length), (override));
};

TEST_F(ChunkTests, emptyBuffer) {
  ChunkMock chunk(1);
  std::string buffer = "";
  EXPECT_CALL(chunk, _write(_, _)).Times(1).WillOnce(Return(buffer.size()));
  EXPECT_CALL(chunk, _open()).Times(1);
  EXPECT_CALL(chunk, _close()).Times(0);
  auto lenLines = chunk.getLenToTransfer(buffer.c_str(), buffer.size());
  ASSERT_EQ(buffer.size(), lenLines.length);
  ASSERT_EQ(0, chunk.write(buffer.c_str(), buffer.size()));
}

TEST_F(ChunkTests, 1lineBuffer) {
  ChunkMock chunk(1);
  std::string buffer = "a\n";
  EXPECT_CALL(chunk, _write(_, _)).Times(1).WillOnce(Return(buffer.size()));
  EXPECT_CALL(chunk, _open()).Times(1);
  EXPECT_CALL(chunk, _close()).Times(1);
  auto lenLines = chunk.getLenToTransfer(buffer.c_str(), buffer.size());
  ASSERT_EQ(buffer.size(), lenLines.length);
  ASSERT_EQ(buffer.size(), chunk.write(buffer.c_str(), buffer.size()));
}

TEST_F(ChunkTests, 3linesBuffer2linesLimit) {
  ChunkMock chunk(2);
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
