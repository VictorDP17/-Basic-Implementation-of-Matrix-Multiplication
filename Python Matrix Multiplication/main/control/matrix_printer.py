class MatrixPrinter:

    @staticmethod
    def print_matrix(matrix):
        for row in matrix:
            for value in row:
                print(value, end=" ")
            print()
