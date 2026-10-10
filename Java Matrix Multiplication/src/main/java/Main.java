import control.MatrixGenerator;
import control.MatrixMultiplier;
import control.MatrixPrinter;

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
        int[][] matrixA = MatrixGenerator.generateMatrix(size);
        int[][] matrixB = MatrixGenerator.generateMatrix(size);

        int[][] resultMatrix = MatrixMultiplier.multiply(matrixA, matrixB);
        MatrixPrinter.printMatrix(resultMatrix);
    }

    private static void multiplyIdentityMatrices(int size) {
        System.out.println("- Identity Matrices Multiplication:");
        int[][] identityMatrix = MatrixGenerator.generateIdentityMatrix(size);

        int[][] resultMatrix = MatrixMultiplier.multiply(identityMatrix, identityMatrix);
        MatrixPrinter.printMatrix(resultMatrix);
    }

    private static void multiplyZeroMatrices(int size) {
        System.out.println("- Zero Matrices Multiplication:");
        int[][] zeroMatrix = MatrixGenerator.generateZeroMatrix(size);

        int[][] resultMatrix = MatrixMultiplier.multiply(zeroMatrix, zeroMatrix);
        MatrixPrinter.printMatrix(resultMatrix);
    }
}
