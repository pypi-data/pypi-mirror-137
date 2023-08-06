cmake_minimum_required(VERSION 3.20)
project(LADEL_suitesparse)

# Find the 64-bit signed integer type in C (usually long on Linux, long long on
# Windows). Unfortunately, we cannot use the C99 int64_t, because the code adds
# an “unsigned” prefix to this type, and “unsigned int64_t” is invalid syntax.
include(IntegerType64.cmake)
if (NOT INTEGER_TYPE_64)
    find_64bit_int_type(INTEGER_TYPE_64)
    set(INTEGER_TYPE_64 ${INTEGER_TYPE_64} CACHE STRING "64-bit integer C type")
endif()

# SuiteSparse config
add_library(suitesparse_config
    "SuiteSparse_config/SuiteSparse_config.c"
)
target_include_directories(suitesparse_config PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/SuiteSparse_config)
target_compile_definitions(suitesparse_config PUBLIC
    SuiteSparse_long=${INTEGER_TYPE_64}
    SuiteSparse_long_max=INT64_MAX
    SuiteSparse_long_idd=PRId64
)
if (MSVC)
    target_compile_definitions(suitesparse_config PUBLIC
        "SuiteSparse_long_id=\"%%\" PRId64")
else()
    target_compile_definitions(suitesparse_config PUBLIC
        "SuiteSparse_long_id=\"%\" PRId64")
endif()
add_library(SuiteSparse::config ALIAS suitesparse_config)

# SuiteSparse approximate minimal degree
set(AMD_SOURCES
    "AMD/Source/amd_1.c"
    "AMD/Source/amd_2.c"
    "AMD/Source/amd_aat.c"
    "AMD/Source/amd_control.c"
    "AMD/Source/amd_defaults.c"
    "AMD/Source/amd_dump.c"
    "AMD/Source/amd_global.c"
    "AMD/Source/amd_info.c"
    "AMD/Source/amd_order.c"
    "AMD/Source/amd_post_tree.c"
    "AMD/Source/amd_postorder.c"
    "AMD/Source/amd_preprocess.c"
    "AMD/Source/amd_valid.c"
)
# Compile as integer version
add_library(amd_c_int OBJECT ${AMD_SOURCES})
target_include_directories(amd_c_int PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/AMD/Include)
target_link_libraries(amd_c_int PUBLIC SuiteSparse::config)
target_compile_definitions(amd_c_int PRIVATE DINT)
# Compile as long (or long long) version
add_library(amd_c_long OBJECT ${AMD_SOURCES})
target_include_directories(amd_c_long PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/AMD/Include)
target_link_libraries(amd_c_long PUBLIC SuiteSparse::config)
target_compile_definitions(amd_c_long PRIVATE DLONG)
# Link both versions
add_library(amd_c)
target_link_libraries(amd_c PUBLIC amd_c_int amd_c_long)
add_library(SuiteSparse::amd ALIAS amd_c)
