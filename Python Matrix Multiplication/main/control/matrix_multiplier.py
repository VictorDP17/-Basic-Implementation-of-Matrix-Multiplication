class MatrixMultiplier:

    @staticmethod
    def multiply(matrix_a, matrix_b):
        n = len(matrix_a)
        matrix_c = [[0 for _ in range(n)] for _ in range(n)]

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    matrix_c[i][j] += (matrix_a[i][k] * matrix_b[k][j])

        return matrix_c