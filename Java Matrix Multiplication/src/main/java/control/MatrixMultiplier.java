package control;

public class MatrixMultiplier {

    public static int[][] multiply(int[][] matrixA, int[][] matrixB) {
        int n = matrixA.length;

        int[][] matrixC = new int[n][n];

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                for (int k = 0; k < n; k++) {
                    matrixC[i][j] += matrixA[i][k] * matrixB[k][j];
                }
            }
        }
        return matrixC;
    }
}
