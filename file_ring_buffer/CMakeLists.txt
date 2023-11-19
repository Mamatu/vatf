cmake_minimum_required(VERSION 3.19)
project(file_ring_buffer CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

add_subdirectory(uts)

file(GLOB SRC "src/*.cpp")
#file(GLOB HEADERS "include/*.h")
set(CMAKE_CXX_STANDARD 17)
include_directories(include)
add_executable(file_ring_buffer main.cpp ${SRC})
install(TARGETS file_ring_buffer DESTINATION ${CMAKE_INSTALL_PREFIX})
