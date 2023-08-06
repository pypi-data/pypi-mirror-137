include_directories(../../external_include)
include_directories(../../common_tools)
#add_library(label_encoder_test SHARED label_encoder_test.c label_encoder_test.h ../../include/tpl/tpl.c)

add_executable(label_encoder_test label_encoder_test.h label_encoder_test.c error.h main_test.c)

target_link_libraries(label_encoder_test PRIVATE common_tools PRIVATE tpl INTERFACE ${Python3_LIBRARIES})
