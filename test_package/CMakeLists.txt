project(PackageTest CXX)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(rocks_sample rocksdb.cpp)
target_link_libraries(rocks_sample ${CONAN_LIBS})
