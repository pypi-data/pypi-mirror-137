include_directories("../external_include" Boost::headers)
add_library(
        encoders SHARED
        binder/label_encoder_binder.cpp src/label_encoder.cpp interface/label_encoder.h
)


target_link_libraries(encoders PRIVATE Boost::headers INTERFACE ${Python3_LIBRARIES} PRIVATE CONAN_PKG::boost)
#target_link_libraries(encoders PRIVATE Boost::headers CONAN_PKG::boost)

if (APPLE)
    set(CMAKE_SHARED_LIBRARY_SUFFIX ".so")
    set_target_properties(
            encoders
            PROPERTIES
            LINK_FLAGS "-undefined dynamic_lookup"
    )
endif (APPLE)
set_target_properties(
        encoders
        PROPERTIES
        PREFIX ""
        OUTPUT_NAME "encoders"
        LINKER_LANGUAGE C
#        LINK_FLAGS "-undefined dynamic_lookup"
#        INSTALL_RPATH "${Python3_LIBRARY_DIRS}"
)