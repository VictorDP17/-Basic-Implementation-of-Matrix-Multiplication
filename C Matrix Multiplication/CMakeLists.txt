cmake_minimum_required(VERSION 3.20)

project(Matrix_Multiplication_C C)

set(CMAKE_C_STANDARD 11)

set(MATRIX_SOURCES
        main/control/matrix_generator.c
        main/control/matrix_multiplier.c
        main/control/matrix_printer.c
)

add_executable(Matrix_Multiplication_C
        main/main.c
        ${MATRIX_SOURCES}
)

add_executable(Matrix_Benchmark_C
        test/benchmark_main.c
        test/benchmark/benchmark.c
        ${MATRIX_SOURCES}
)

target_include_directories(Matrix_Benchmark_C PRIVATE
        main/control
)