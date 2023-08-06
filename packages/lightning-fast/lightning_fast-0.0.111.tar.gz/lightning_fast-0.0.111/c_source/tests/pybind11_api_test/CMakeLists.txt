#pybind11_add_module(pybind11_api_test pybind11_api_test.cpp)
add_library(pybind11_api_test SHARED pybind11_api_test.cpp)

#target_link_libraries(spam ${Python3_LIBRARIES})

if(APPLE)
    set(CMAKE_SHARED_LIBRARY_SUFFIX ".so")
    set_target_properties(
            pybind11_api_test
            PROPERTIES
            LINK_FLAGS "-undefined dynamic_lookup"
    )
endif(APPLE)
set_target_properties(
        pybind11_api_test
        PROPERTIES
        PREFIX ""
        OUTPUT_NAME "pybind11_api_test"
        LINKER_LANGUAGE C
)