mkdir bin
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=../bin ../file_ring_buffer
make
make install
cd -
rm -r build
