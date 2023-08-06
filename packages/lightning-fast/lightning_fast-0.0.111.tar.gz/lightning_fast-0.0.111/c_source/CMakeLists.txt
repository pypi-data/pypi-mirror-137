cmake_minimum_required(VERSION 3.17)
#project(lightning_fast_c C CXX)
project(lightning_fast_c)

#set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_BUILD_WITH_INSTALL_RPATH ON)
set(Python_FIND_VIRTUALENV FIRST)
#set(CMAKE_INSTALL_RPATH_USE_LINK_PATH OFF)
#set(CMAKE_MACOSX_RPATH OFF)

###### 增加sanitize ######
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -undefined dynamic_lookup")
if (${CMAKE_BUILD_TYPE} STREQUAL 'Debug')
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address")
else ()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")
endif ()
#################################################################################

###### 这里使用conan初始化, 相当于执行conan install . -if ${CMAKE_BINARY_DIR} ######
# Download automatically, you can also just copy the conan.cmake file
if (NOT EXISTS "${CMAKE_SOURCE_DIR}/cmake_tools/conan.cmake")
    if (NOT EXISTS "${CMAKE_BINARY_DIR}/conan.cmake")
        message(STATUS "Downloading conan.cmake from https://github.com/conan-io/cmake-conan")
        file(DOWNLOAD "https://raw.githubusercontent.com/conan-io/cmake-conan/master/conan.cmake"
                "${CMAKE_BINARY_DIR}/conan.cmake")
    endif ()
    include(${CMAKE_BINARY_DIR}/conan.cmake)
else()
    include("${CMAKE_SOURCE_DIR}/cmake_tools/conan.cmake")
endif()

conan_cmake_install(PATH_OR_REFERENCE ${CMAKE_SOURCE_DIR}
        SETTINGS ${settings})
#################################################################################

######这里如果mac则强行指定构建为x86_64######
# 主要因为conda不支持arc64而本人大部分情况下使用conda
IF (APPLE)
    SET(CMAKE_OSX_ARCHITECTURES "x86_64" CACHE STRING "Build architectures for Mac OS X" FORCE)
ENDIF (APPLE)
set(Yellow "${Esc}[33m")
add_custom_target(display_intro ALL COMMAND cmake -E cmake_echo_color --magenta "Current environment is '${CMAKE_BUILD_TYPE}'")
#################################################################################

###### 加载Python3 ######
set(Python3_USE_STATIC_LIBS FALSE)
find_package(Python3 COMPONENTS Interpreter Development)

message(
        "Python_FOUND:${Python3_FOUND}\n"
        "Python_VERSION:${Python3_VERSION}\n"
        "Python_Development_FOUND:${Python3_Development_FOUND}\n"
        "Python_INCLUDE_DIRS:${Python3_INCLUDE_DIRS}\n"
        "Python3_LIBRARIES:${Python3_LIBRARIES}\n"
        "Python3_LIBRARY_DIRS:${Python3_LIBRARY_DIRS}\n"
        "Python_RUNTIME_LIBRARY_DIRS:${Python3_RUNTIME_LIBRARY_DIRS}\n"
)
include_directories(${Python3_INCLUDE_DIRS})
#################################################################################

###### 加载conan生成的cmake ######
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
#conan_basic_setup(TARGETS KEEP_RPATHS NO_OUTPUT_DIRS)
# 这里如果发现CMAKE_LIBRARY_OUTPUT_DIRECTORY已经定义, 则说明目标路径需要自定义, 则保存此目录位置，最后一起复制过去
if (DEFINED CMAKE_LIBRARY_OUTPUT_DIRECTORY)
    set(CUSTOM_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_LIBRARY_OUTPUT_DIRECTORY})
endif()
# 这里初始化conan, 同时会将CMAKE_LIBRARY_OUTPUT_DIRECTORY等变量改为conan默认
conan_basic_setup(TARGETS KEEP_RPATHS)
# 加载boost
find_package(Boost REQUIRED)
#################################################################################

###### 这里将生成文件配置@RPATH ######
# 主要为了同时满足直接编译与在python的pip下编译生成位置不同
if (APPLE)
    set(CMAKE_INSTALL_RPATH "@loader_path;@executable_path/../lib;${Python3_LIBRARY_DIRS}")
else()
    set(CMAKE_INSTALL_RPATH "$ORIGIN/../lib;$ORIGIN;${Python3_LIBRARY_DIRS}")
endif()
#################################################################################

###### 编译所有子目录 ######
add_subdirectory(common_tools)
add_subdirectory(external_include/tpl)
add_subdirectory(tests/label_encoder_test)
add_subdirectory(tests/python_c_api_test)
add_subdirectory(tests/pybind11_api_test)
add_subdirectory(encoders)
add_subdirectory(tests/encoders_test)

#################################################################################

###### 完成编译后执行命令 ######
add_custom_target(
        copy_libs ALL
)

# 如果有保存目标路径, 则将生成文件的lib文件都复制过去
if (DEFINED CUSTOM_LIBRARY_OUTPUT_DIRECTORY)
    add_custom_command(
            TARGET copy_libs POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy_directory
            "${CMAKE_BINARY_DIR}/lib/"
            "${CUSTOM_LIBRARY_OUTPUT_DIRECTORY}"
    )

endif()

# 将完成编译命令设置为依赖其它所有目标以保证最后执行
add_dependencies(
        copy_libs
        display_intro
        common_tools
        tpl
        encoders
        label_encoder_test
        python_c_api_test
        pybind11_api_test
        encoders_test
)


