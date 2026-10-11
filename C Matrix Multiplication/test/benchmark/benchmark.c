#include "benchmark.h"

#include "../../main/control/matrix_generator.h"
#include "../../main/control/matrix_multiplier.h"

#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <time.h>

#define NUM_SIZES 5
#define WARMUP_ITERATIONS 1
#define MEASUREMENT_ITERATIONS 5

static const int MATRIX_SIZES[NUM_SIZES] = {100, 200, 300, 400, 500};


typedef struct {
    double meanTime;
    double medianTime;
    double varianceTime;
    size_t peakMemoryBytes;
} BenchmarkStats;


static double getTime() {
    struct timespec time;

    clock_gettime(CLOCK_MONOTONIC, &time);

    return time.tv_sec + time.tv_nsec / 1e9;
}


static void freeMatrix(int **matrix, int n) {
    if (matrix == NULL) {
        return;
    }
    for (int i = 0; i < n; i++) {
        free(matrix[i]);
    }
    free(matrix);
}


static void preventIgnoreResult(int **result) {
    volatile int value = result[0][0];
    (void)value;
}


static double benchmarkMultiplication(int **matrixA, int **matrixB, int n) {
    double start = getTime();

    int **result = multiply(matrixA, matrixB, n);

    double end = getTime();

    preventIgnoreResult(result);
    freeMatrix(result, n);

    return (end - start) * 1000.0;
}


static size_t estimateResultMatrixMemory(int n) {
    size_t pointerBytes = (size_t)n * sizeof(int *);
    size_t elementBytes = (size_t)n * (size_t)n * sizeof(int);

    return pointerBytes + elementBytes;
}


static int compareDoubles(const void *a, const void *b) {
    double x = *(const double *)a;
    double y = *(const double *)b;

    return (x > y) - (x < y);
}


static void doWarmUp(int size, int **matrixA, int **matrixB) {
    for (int i = 0; i < WARMUP_ITERATIONS; i++) {
        int **result = multiply(matrixA, matrixB, size);

        preventIgnoreResult(result);
        freeMatrix(result, size);
    }
}

static void doMeasurements(int size, int **matrixA, int **matrixB, double *timeSamples, double *totalTime) {
    *totalTime = 0.0;

    for (int i = 0; i < MEASUREMENT_ITERATIONS; i++) {
        timeSamples[i] = benchmarkMultiplication(matrixA, matrixB, size);
        *totalTime += timeSamples[i];
    }
}

static double calculateMean(double totalTime) {
    return totalTime / MEASUREMENT_ITERATIONS;
}


static double calculateMedian(const double *timeSamples) {
    double sortedSamples[MEASUREMENT_ITERATIONS];

    for (int i = 0; i < MEASUREMENT_ITERATIONS; i++) {
        sortedSamples[i] = timeSamples[i];
    }

    qsort(
        sortedSamples,
        MEASUREMENT_ITERATIONS,
        sizeof(double),
        compareDoubles
    );

    int middle = MEASUREMENT_ITERATIONS / 2;

    if (MEASUREMENT_ITERATIONS % 2 == 0) {
        return (sortedSamples[middle - 1] + sortedSamples[middle]) / 2.0;
    }

    return sortedSamples[middle];
}


static double calculateVariance(const double *timeSamples, double meanTime) {
    if (MEASUREMENT_ITERATIONS <= 1) {
        return 0.0;
    }

    double squaredDifferences = 0.0;

    for (int i = 0; i < MEASUREMENT_ITERATIONS; i++) {
        double difference = timeSamples[i] - meanTime;
        squaredDifferences += difference * difference;
    }

    return squaredDifferences / (MEASUREMENT_ITERATIONS - 1);
}


static void printBenchmarkStats(const char *benchmarkName, const BenchmarkStats *stats) {
    printf(
        "%s: mean=%.6f ms, median=%.6f ms, "
        "variance=%.9f ms^2, estimated output memory=%zu bytes\n",
        benchmarkName,
        stats->meanTime,
        stats->medianTime,
        stats->varianceTime,
        stats->peakMemoryBytes
    );
}


static BenchmarkStats matrixMultiplicationTest(const char *benchmarkName, int size, int **matrixA, int **matrixB) {
    doWarmUp(size, matrixA, matrixB);

    double totalTime;
    double timeSamples[MEASUREMENT_ITERATIONS];
    doMeasurements(size, matrixA, matrixB, timeSamples, &totalTime);

    double meanTime = calculateMean(totalTime);

    BenchmarkStats stats = {
        meanTime,
        calculateMedian(timeSamples),
        calculateVariance(timeSamples, meanTime),
        estimateResultMatrixMemory(size)
    };

    printBenchmarkStats(benchmarkName, &stats);
    return stats;
}


static void saveResult(FILE *file, const char *benchmarkName, int size, BenchmarkStats stats) {
    fprintf(
        file,
        "C,%s,%d,%.9f,%.9f,%.9f,%zu\n",
        benchmarkName,
        size,
        stats.meanTime,
        stats.medianTime,
        stats.varianceTime,
        stats.peakMemoryBytes
    );
}


static void runAndSaveBenchmark(FILE *file, const char *benchmarkName, int size, int **matrixA, int **matrixB) {
    BenchmarkStats stats = matrixMultiplicationTest(benchmarkName, size, matrixA, matrixB);
    saveResult(file, benchmarkName, size, stats);
}


static FILE *createCsv(void) {
    FILE *file = fopen("c_results.csv", "w");

    if (file == NULL) {
        perror("Error creating c_results.csv");
        return NULL;
    }

    fprintf(
        file,
        "language,benchmark,matrix_size,"
        "mean_time,median_time,variance_time,peak_memory_bytes\n"
    );
    return file;
}


static void freeAllMatrices(int size, int **matrixA, int **matrixB, int **identityMatrix, int **zeroMatrix) {
    freeMatrix(matrixA, size);
    freeMatrix(matrixB, size);
    freeMatrix(identityMatrix, size);
    freeMatrix(zeroMatrix, size);
}


void runBenchmark(void) {
    FILE *file = createCsv();

    if (file == NULL) {
        return;
    }

    for (int s = 0; s < NUM_SIZES; s++) {
        int size = MATRIX_SIZES[s];

        printf("\n- - - Matrix Size: %d - - -\n", size);

        int **matrixA = generateMatrix(size);
        int **matrixB = generateMatrix(size);
        int **identityMatrix = generateIdentityMatrix(size);
        int **zeroMatrix = generateZeroMatrix(size);

        runAndSaveBenchmark(file, "random", size, matrixA, matrixB);
        runAndSaveBenchmark(file, "identity", size, identityMatrix, identityMatrix);
        runAndSaveBenchmark(file, "zero", size, zeroMatrix, zeroMatrix);

        freeAllMatrices(size, matrixA, matrixB, identityMatrix, zeroMatrix);
    }

    fclose(file);
    printf("\nResults saved to c_results.csv\n");
}
