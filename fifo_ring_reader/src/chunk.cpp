#include "chunk.h"

#include <stdio.h>

Chunk::Chunk(const std::string& path) : m_path(path), m_file(fopen(path.c_str(), "w+"))
{
}

Chunk::~Chunk()
{
  fclose(m_file);
}

void Chunk::write(const char* bytes) {
   
}
