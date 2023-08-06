cmake_minimum_required(VERSION 3.20)
project(LADEL VERSION 0.1.0)

option (LADEL_SIMPLE_COL_COUNTS
    "Simplify symbolic analysis (worse asymptotic time complexity)" On)
option (LADEL_USE_AMD
    "Use approximate minimum degree ordering" On)
option (LADEL_LONG
    "Use long long integers for indexing" On)
option (LADEL_FLOAT
    "Use single precision instead of double" Off)
option (LADEL_WITH_MEX
    "Compile the MATLAB interface" Off)

# Main LADEL library
add_library(ladel
    "src/ladel_debug_print.c"
    "src/ladel_scale.c"
    "src/ladel_upper_diag.c"
    "src/ladel_col_counts.c"
    "src/ladel_ldl_symbolic.c"
    "src/ladel_global.c"
    "src/ladel_ldl_numeric.c"
    "src/ladel_add.c"
    "src/ladel_transpose.c"
    "src/ladel_etree.c"
    "src/ladel_permutation.c"
    "src/ladel_matvec.c"
    "src/ladel_postorder.c"
    "src/ladel_copy.c"
    "src/ladel_pattern.c"
    "src/ladel_submatrix.c"
    "src/ladel_row_mod.c"
    "src/ladel.c"
    "src/ladel_matmat.c"
    "src/ladel_rank1_mod.c"
)
target_include_directories(ladel
    PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
           $<INSTALL_INTERFACE:include>)
if (LADEL_USE_AMD)
    target_compile_definitions(ladel PUBLIC DAMD)
    add_subdirectory(../thirdparty/SuiteSparse SuiteSparse EXCLUDE_FROM_ALL)
    target_link_libraries(ladel PRIVATE SuiteSparse::amd)
endif()
if (LADEL_SIMPLE_COL_COUNTS)
    target_compile_definitions(ladel PUBLIC SIMPLE_COL_COUNTS)
endif()
if (LADEL_LONG)
    target_compile_definitions(ladel PUBLIC DLONG)
endif()
if (LADEL_FLOAT)
    target_compile_definitions(ladel PUBLIC DFLOAT)
endif()
add_library(ladel::ladel ALIAS ladel)

# Sanity check
include(CheckTypeSize)
CHECK_TYPE_SIZE("long long" LONG_LONG_SIZE BUILTIN_TYPES_ONLY LANGUAGE C)
if (NOT LONG_LONG_SIZE EQUAL 8)
    message(WARNING "The C type long long does not appear to be 64 bits wide, "
                    "make sure that the integer types are compatible with "
                    "SuiteSparse.")
endif()

# MATLAB interface
if (LADEL_WITH_MEX)
    add_subdirectory(mex)
endif()
