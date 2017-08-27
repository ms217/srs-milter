cmake_minimum_required(VERSION 2.8)
project(srs_milter)

set(SOURCE_FILES
    src/srs-filter.c)

add_executable(srs-filter ${SOURCE_FILES})
target_link_libraries(srs-filter milter pthread spf2 srs2)
