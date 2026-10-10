import control.GenerateMatrix;
import control.MatrixMultiplication;
import control.PrintMatrix;

public class Main {
    private static final int[] MATRIX_SIZES = {2, 4};

    public static void main(String[] args) {
        for (int size : MATRIX_SIZES) {
            System.out.println("- - - Matrix Multiplication for Size: " + size + " - - - - - - - -");
            multiplyRandomMatrices(size);
            multiplyIdentityMatrices(size);
            multiplyZeroMatrices(size);
        }
    }

    private static void multiplyRandomMatrices(int size) {
        System.out.println("- Random Matrices Multiplication:");
        int[][] matrixA = GenerateMatrix.generateMatrix(size);
        int[][] matrixB = GenerateMatrix.generateMatrix(size);

        int[][] resultMatrix = MatrixMultiplication.multiply(matrixA, matrixB);
        PrintMatrix.printMatrix(resultMatrix);
    }

    private static void multiplyIdentityMatrices(int size) {
        System.out.println("- Identity Matrices Multiplication:");
        int[][] identityMatrix = GenerateMatrix.generateIdentityMatrix(size);

        int[][] resultMatrix = MatrixMultiplication.multiply(identityMatrix, identityMatrix);
        PrintMatrix.printMatrix(resultMatrix);
    }

    private static void multiplyZeroMatrices(int size) {
        System.out.println("- Zero Matrices Multiplication:");
        int[][] zeroMatrix = GenerateMatrix.generateZeroMatrix(size);

        int[][] resultMatrix = MatrixMultiplication.multiply(zeroMatrix, zeroMatrix);
        PrintMatrix.printMatrix(resultMatrix);
    }
}
