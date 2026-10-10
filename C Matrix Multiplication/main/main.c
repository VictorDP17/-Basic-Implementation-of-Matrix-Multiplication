#include <stdio.h>
#include <stdlib.h>

#include "control/matrix_generator.h"
#include "control/matrix_multiplier.h"
#include "control/matrix_printer.h"

#define NUM_SIZES 2

static const int MATRIX_SIZES[NUM_SIZES] = {2, 4};

static void freeMatrix(int** matrix, int n) {
    for (int i = 0; i < n; i++) {
        free(matrix[i]);
    }

    free(matrix);
}

static void multiplyRandomMatrices(int size) {
    printf("- Random Matrices Multiplication:\n");

    int** matrixA = generateMatrix(size);
    int** matrixB = generateMatrix(size);

    int** resultMatrix = multiply(matrixA, matrixB, size);

    printMatrix(resultMatrix, size);

    freeMatrix(matrixA, size);
    freeMatrix(matrixB, size);
    freeMatrix(resultMatrix, size);
}

static void multiplyIdentityMatrices(int size) {
    printf("- Identity Matrices Multiplication:\n");

    int** identityMatrix = generateIdentityMatrix(size);

    int** resultMatrix = multiply(identityMatrix, identityMatrix, size);

    printMatrix(resultMatrix, size);

    freeMatrix(identityMatrix, size);
    freeMatrix(resultMatrix, size);
}

static void multiplyZeroMatrices(int size) {
    printf("- Zero Matrices Multiplication:\n");

    int** zeroMatrix = generateZeroMatrix(size);

    int** resultMatrix = multiply(zeroMatrix, zeroMatrix, size);

    printMatrix(resultMatrix, size);

    freeMatrix(zeroMatrix, size);
    freeMatrix(resultMatrix, size);
}

int main() {
    srand(777);

    for (int i = 0; i < NUM_SIZES; i++) {
        const int size = MATRIX_SIZES[i];

        printf("- - - Matrix Multiplication for Size: %d - - - - - - - -\n", size);

        multiplyRandomMatrices(size);
        multiplyIdentityMatrices(size);
        multiplyZeroMatrices(size);
    }
    return 0;
}
