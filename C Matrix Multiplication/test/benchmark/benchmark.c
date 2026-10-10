#include "benchmark.h"

#include <stdbool.h>

#include "../../main/control/matrix_generator.h"
#include "../../main/control/matrix_multiplier.h"

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define NUM_SIZES 4
#define WARMUP_ITERATIONS 1
#define MEASUREMENT_ITERATIONS 5

static const int MATRIX_SIZES[NUM_SIZES] = {100, 200, 500, 1000};

static double getTime() {
    struct timespec time;

    clock_gettime(CLOCK_MONOTONIC, &time);

    return time.tv_sec + time.tv_nsec / 1e9;
}


static void freeMatrix(int **matrix, int n) {
    for (int i = 0; i < n; i++) {
        free(matrix[i]);
    }
    free(matrix);
}


static void preventIgnoreResult(int **result) {
    volatile int value = result[0][0];
    (void) value;
}


static double benchmarkMultiplication(int **matrixA, int **matrixB, int n) {
    double start = getTime();
    int **result = multiply(matrixA, matrixB, n);
    double end = getTime();

    preventIgnoreResult(result);
    freeMatrix(result, n);

    return (end - start) * 1000.0;
}


static bool createCsv(FILE **file) {
    *file = fopen("c_results.csv", "w");

    if (*file == NULL) {
        printf("Error creating CSV file.\n");
        return true;
    }

    fprintf(*file, "language,benchmark,matrix_size,time_ms\n");
    return false;
}

static void randomMatricesMultiplicationTest(FILE *file, const char *benchmarkName, int size, int **matrixA, int **matrixB, double *averageTime) {
    double totalTime = 0.0;

    for (int i = 0; i < WARMUP_ITERATIONS; i++) {
        int **result = multiply(matrixA, matrixB, size);
        freeMatrix(result, size);
    }

    for (int i = 0; i < MEASUREMENT_ITERATIONS; i++) {
        totalTime += benchmarkMultiplication(
            matrixA,
            matrixB,
            size
        );
    }

    *averageTime = totalTime / MEASUREMENT_ITERATIONS;

    printf("%s: %.6f ms\n", benchmarkName, *averageTime);

    fprintf(
        file,
        "C,%s,%d,%.6f\n",
        benchmarkName,
        size,
        *averageTime
    );
}

static void freeAllMatrices(int size, int **matrixA, int **matrixB, int **identityMatrix, int **zeroMatrix) {
    freeMatrix(matrixA, size);
    freeMatrix(matrixB, size);
    freeMatrix(identityMatrix, size);
    freeMatrix(zeroMatrix, size);
}

void runBenchmark() {
    FILE *file;
    if (createCsv(&file)) return;

    for (int s = 0; s < NUM_SIZES; s++) {
        int size = MATRIX_SIZES[s];

        printf("\n- - - Matrix Size: %d - - -\n", size);

        int **matrixA = generateMatrix(size);
        int **matrixB = generateMatrix(size);

        int **identityMatrix = generateIdentityMatrix(size);
        int **zeroMatrix = generateZeroMatrix(size);

        double averageTime;
        randomMatricesMultiplicationTest(file, "random", size, matrixA, matrixB, &averageTime);
        randomMatricesMultiplicationTest(file, "identity", size, identityMatrix, identityMatrix, &averageTime);
        randomMatricesMultiplicationTest(file, "zero", size, zeroMatrix, zeroMatrix, &averageTime);

        freeAllMatrices(size, matrixA, matrixB, identityMatrix, zeroMatrix);
    }
    fclose(file);
    printf("\nResults saved to c_results.csv\n");
}
