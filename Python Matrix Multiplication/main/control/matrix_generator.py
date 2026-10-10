import random


class MatrixGenerator:
    RANDOM = random.Random(777)

    @staticmethod
    def generate_matrix(n):
        matrix = [[0 for _ in range(n)] for _ in range(n)]

        for i in range(n):
            for j in range(n):
                matrix[i][j] = MatrixGenerator.RANDOM.randrange(100)

        return matrix

    @staticmethod
    def generate_identity_matrix(n):
        matrix = [[0 for _ in range(n)] for _ in range(n)]

        for i in range(n):
            matrix[i][i] = 1

        return matrix

    @staticmethod
    def generate_zero_matrix(n):
        return [[0 for _ in range(n)] for _ in range(n)]
