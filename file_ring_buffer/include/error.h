#ifndef ERROR_H
#define ERROR_H

#include <exception>
#include <stdexcept>

inline void error(bool cond, const std::string& msg)
{
  if (!cond)
  {
    throw std::runtime_error(msg);
  }
}

inline void error(bool cond, const std::stringstream& msg)
{
  error(cond, msg.str());
}

#endif
