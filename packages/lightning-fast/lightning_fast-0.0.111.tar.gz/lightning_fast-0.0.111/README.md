# lightning_fast

# Project Dependence

1. gcc
2. cmake

# Test(Old)
1. cd c_source
2. cmake compile cmake --build ./cmake-build-debug --target test -- -j 3
3. cd cmake-build-debug
4. make
5. copy liblabel_encoder.dylib to lightning_fast/c_dynamic_library
6. run lightning_fast/main.py
7. lightning_fast/tmp test result

# Test(New)
just run make run_test

# install as package
1. need cmake and gcc and conan
2. pip from git
