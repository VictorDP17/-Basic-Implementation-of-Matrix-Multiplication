from control.matrix_generator import MatrixGenerator
from control.matrix_multiplier import MatrixMultiplier
from control.matrix_printer import MatrixPrinter

MATRIX_SIZES = [2, 4]


def main():
    for size in MATRIX_SIZES:
        print(f"- - - Matrix Multiplication for Size: {size} - - - - - - - -")
        multiply_random_matrices(size)
        multiply_identity_matrices(size)
        multiply_zero_matrices(size)


def multiply_random_matrices(size):
    print("- Random Matrices Multiplication:")
    matrix_a = MatrixGenerator.generate_matrix(size)
    matrix_b = MatrixGenerator.generate_matrix(size)

    result_matrix = MatrixMultiplier.multiply(matrix_a, matrix_b)
    MatrixPrinter.print_matrix(result_matrix)


def multiply_identity_matrices(size):
    print("- Identity Matrices Multiplication:")
    identity_matrix = MatrixGenerator.generate_identity_matrix(size)

    result_matrix = MatrixMultiplier.multiply(identity_matrix, identity_matrix)
    MatrixPrinter.print_matrix(result_matrix)


def multiply_zero_matrices(size):
    print("- Zero Matrices Multiplication:")
    zero_matrix = MatrixGenerator.generate_zero_matrix(size)

    result_matrix = MatrixMultiplier.multiply(zero_matrix, zero_matrix)
    MatrixPrinter.print_matrix(result_matrix)


if __name__ == "__main__":
    main()
