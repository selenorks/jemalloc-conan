PROJECT(MyHello)
cmake_minimum_required(VERSION 3.0)

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR}/..)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)

CONAN_BASIC_SETUP()

find_package(Jemalloc)

IF(JEMALLOC_FOUND)
    include_directories(${JEMALLOC_INCLUDE_DIR})
    add_executable(main main.c)
    target_link_libraries(main jemalloc)
else()
    message(FATAL_ERROR "JeMalloc NOT FOUND!")
endif()
