cmake_minimum_required(VERSION 3.10)

project(wnnc)

set (CMAKE_CXX_FLAGS "-std=c++17 -O3 -Wall -shared  -fPIC ${CMAKE_CXX_FLAGS}")

# add_subdirectory(pybind11)
find_package(pybind11 REQUIRED)
pybind11_add_module(wnnc 
    wnnc.cc
    ../cc/utils/mapping.cc
    ../cc/utils/utils.cc
    ../cc/wisard.cc
    ../cc/regression_wisard.cc
    ../cc/bleaching_wisard.cc
    ../cc/bloom_wisard.cc
    ../cc/bleaching_bloom_wisard.cc
    bleaching_bloom_wisard_bind.cc
    bleaching_wisard_bind.cc
    bleaching_wisard_bind.cc
    wisard_bind.cc
)

target_compile_definitions(wnnc PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})