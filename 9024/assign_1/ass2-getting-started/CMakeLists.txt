cmake_minimum_required(VERSION 3.15)
project(ass2_getting_started)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)

add_executable(ass2_getting_started
        exTkns.c
        sample1.txt)
