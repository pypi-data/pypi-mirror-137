add_library(python_c_api_test SHARED python_c_api_test.c)

#target_link_libraries(spam ${Python3_LIBRARIES})

if(APPLE)
    set(CMAKE_SHARED_LIBRARY_SUFFIX ".so")
    set_target_properties(
            python_c_api_test
            PROPERTIES
            LINK_FLAGS "-undefined dynamic_lookup"
    )
endif(APPLE)
set_target_properties(
        python_c_api_test
        PROPERTIES
        PREFIX ""
        OUTPUT_NAME "python_c_api_test"
        LINKER_LANGUAGE C
)