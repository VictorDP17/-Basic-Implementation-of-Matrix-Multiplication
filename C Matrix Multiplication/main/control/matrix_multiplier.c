#include "../control/matrix_multiplier.h"
#include <stdlib.h>

int** multiply(int** matrixA, int** matrixB, int n) {
    int** matrixC = malloc(n * sizeof(int*));

    for (int i = 0; i < n; i++) {
        matrixC[i] = calloc(n, sizeof(int));

        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                matrixC[i][j] += matrixA[i][k] * matrixB[k][j];
            }
        }
    }

    return matrixC;
}
