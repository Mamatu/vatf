cmake_minimum_required(VERSION 3.19)
project(fifo_ring_reader CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

add_subdirectory(uts)

file(GLOB SRC "src/*.cpp")
#file(GLOB HEADERS "include/*.h")
set(CMAKE_CXX_STANDARD 17)
include_directories(include)
add_executable(fifo_ring_reader main.cpp ${SRC})
