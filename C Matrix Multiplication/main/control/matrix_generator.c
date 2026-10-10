#include "matrix_generator.h"
#include <stdlib.h>

int** generateMatrix(int n) {
    int** matrix = malloc(n * sizeof(int*));

    for (int i = 0; i < n; i++) {
        matrix[i] = malloc(n * sizeof(int));

        for (int j = 0; j < n; j++) {
            matrix[i][j] = rand() % 100;
        }
    }
    return matrix;
}

int** generateIdentityMatrix(int n) {
    int** matrix = malloc(n * sizeof(int*));

    for (int i = 0; i < n; i++) {
        matrix[i] = calloc(n, sizeof(int));
        matrix[i][i] = 1;
    }
    return matrix;
}

int** generateZeroMatrix(int n) {
    int** matrix = malloc(n * sizeof(int*));

    for (int i = 0; i < n; i++) {
        matrix[i] = calloc(n, sizeof(int));
    }
    return matrix;
}