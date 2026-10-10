package control;

import java.util.Random;

public class GenerateMatrix {
    public static Random RANDOM = new Random(777);

    public static int[][] generateMatrix(int n) {
        int[][] matrix = new int[n][n];

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                matrix[i][j] = RANDOM.nextInt(100);
            }
        }
        return matrix;
    }

    public static int[][] generateIdentityMatrix(int n) {
        int[][] matrix = new int[n][n];

        for (int i = 0; i < n; i++) {
            matrix[i][i] = 1;
        }
        return matrix;
    }

    public static int[][] generateZeroMatrix(int n) {
        return new int[n][n];
    }
}
