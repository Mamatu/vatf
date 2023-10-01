#ifndef CHUNK_H
#define CHUNK_H

#include <string>

class Chunk
{
  public:
    Chunk(const std::string& path);
    virtual ~Chunk();
    void write(const char* bytes);

  protected:

  private:
    std::string m_path;
    FILE* m_file;
};

#endif
