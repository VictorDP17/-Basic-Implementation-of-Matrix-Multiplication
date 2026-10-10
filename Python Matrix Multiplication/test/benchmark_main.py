import time

from control.matrix_generator import MatrixGenerator
from control.matrix_multiplier import MatrixMultiplier
from benchmark_saver import BenchmarkSaver

MATRIX_SIZES = [100, 200, 500, 1000]

WARMUP_ITERATIONS = 1
MEASUREMENT_ITERATIONS = 5


def run_benchmark():
    results = []

    for size in MATRIX_SIZES:
        print(f"\n- - - Matrix Size: {size} - - -")

        matrix_a, matrix_b, identity_matrix, zero_matrix = setup(size)
        benchmarks = {
            "random": (matrix_a, matrix_b),
            "identity": (identity_matrix, identity_matrix),
            "zero": (zero_matrix, zero_matrix)
        }

        for benchmark_name, matrices in benchmarks.items():
            matrix_1, matrix_2 = matrices

            for _ in range(WARMUP_ITERATIONS):
                MatrixMultiplier.multiply(matrix_1, matrix_2)

            measurements = []
            for _ in range(MEASUREMENT_ITERATIONS):
                time_ms = benchmark_multiplication(matrix_1, matrix_2)
                measurements.append(time_ms)
            average_time = sum(measurements) / len(measurements)

            results.append({
                "language": "Python",
                "benchmark": benchmark_name,
                "matrix_size": size,
                "time_ms": average_time
            })

            print(
                f"{benchmark_name}: "
                f"{average_time:.6f} ms"
            )
    BenchmarkSaver.save_results(results)


def setup(size):
    matrix_a = MatrixGenerator.generate_matrix(size)
    matrix_b = MatrixGenerator.generate_matrix(size)
    identity_matrix = MatrixGenerator.generate_identity_matrix(size)
    zero_matrix = MatrixGenerator.generate_zero_matrix(size)

    return matrix_a, matrix_b, identity_matrix, zero_matrix


def benchmark_multiplication(matrix_a, matrix_b):
    start = time.perf_counter()

    MatrixMultiplier.multiply(matrix_a, matrix_b)

    end = time.perf_counter()

    return (end - start) * 1000


if __name__ == "__main__":
    run_benchmark()
