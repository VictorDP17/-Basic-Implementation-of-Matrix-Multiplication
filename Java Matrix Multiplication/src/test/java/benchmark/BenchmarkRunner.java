package benchmark;

import org.openjdk.jmh.annotations.*;
import java.util.concurrent.TimeUnit;
import org.openjdk.jmh.infra.Blackhole;

import control.*;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@State(Scope.Benchmark)
public class BenchmarkRunner {

    @Param({"100", "200", "300", "400", "500"})
    private int MATRIX_SIZE;

    private int[][] matrixA;
    private int[][] matrixB;
    private int[][] identityMatrix;
    private int[][] zeroMatrix;

    @Setup(Level.Trial)
    public void setup() {
        matrixA = MatrixGenerator.generateMatrix(MATRIX_SIZE);
        matrixB = MatrixGenerator.generateMatrix(MATRIX_SIZE);
        identityMatrix = MatrixGenerator.generateIdentityMatrix(MATRIX_SIZE);
        zeroMatrix = MatrixGenerator.generateZeroMatrix(MATRIX_SIZE);
    }

    @Benchmark
    public void multiplyRandomMatrices(Blackhole blackhole) {
        blackhole.consume(MatrixMultiplier.multiply(matrixA, matrixB));
    }

    @Benchmark
    public void multiplyIdentityMatrices(Blackhole blackhole) {
        blackhole.consume(MatrixMultiplier.multiply(identityMatrix, identityMatrix));
    }

    @Benchmark
    public void multiplyZeroMatrices(Blackhole blackhole) {
        blackhole.consume(MatrixMultiplier.multiply(zeroMatrix, zeroMatrix));
    }
}
