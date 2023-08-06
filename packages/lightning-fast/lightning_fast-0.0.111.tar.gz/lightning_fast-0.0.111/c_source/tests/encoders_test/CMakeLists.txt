include_directories(../../external_include)
include_directories(../../encoders)
include_directories(Boost::headers)

add_executable(encoders_test main_test.cpp label_encoder_test.cpp label_encoder_test.h)

target_link_libraries(encoders_test PRIVATE Boost::headers INTERFACE ${Python3_LIBRARIES} PRIVATE encoders INTERFACE CONAN_PKG::boost)
