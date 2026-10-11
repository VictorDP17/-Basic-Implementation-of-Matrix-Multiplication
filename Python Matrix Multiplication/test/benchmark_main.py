import time
import gc
import tracemalloc
import statistics

from control.matrix_generator import MatrixGenerator
from control.matrix_multiplier import MatrixMultiplier
from benchmark_saver import BenchmarkSaver

MATRIX_SIZES = [100, 200, 300, 400, 500]

WARMUP_ITERATIONS = 1
MEASUREMENT_ITERATIONS = 2


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
            average_time, median_peak_bytes = calculate_metrics(benchmark_name, matrix_1, matrix_2, results, size)

            print(
                f"{benchmark_name}: "
                f"{average_time:.6f} ms; "
                f"{median_peak_bytes} B/op"
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


def calculate_metrics(benchmark_name, matrix_1, matrix_2, results, size):
    for _ in range(WARMUP_ITERATIONS):
        MatrixMultiplier.multiply(matrix_1, matrix_2)

    mean_time, median_time, variance_time = calculate_time(matrix_1, matrix_2)

    median_peak_bytes = calculate_memory(matrix_1, matrix_2)

    results.append({
        "language": "Python",
        "benchmark": benchmark_name,
        "matrix_size": size,
        "mean_time": mean_time,
        "median_time": median_time,
        "variance_time": variance_time,
        "peak_memory_bytes": median_peak_bytes
    })
    return mean_time, median_peak_bytes


def calculate_time(matrix_1, matrix_2):
    time_samples = []

    for _ in range(MEASUREMENT_ITERATIONS):
        time_ms = benchmark_multiplication(matrix_1, matrix_2)
        time_samples.append(time_ms)

    mean_time = statistics.mean(time_samples)
    median_time = statistics.median(time_samples)
    variance_time = statistics.variance(time_samples)

    return mean_time, median_time, variance_time


def calculate_memory(matrix_1, matrix_2):
    memory_samples = []

    for _ in range(MEASUREMENT_ITERATIONS):
        peak_bytes = measure_peak_memory(matrix_1, matrix_2)
        memory_samples.append(peak_bytes)

    median_peak_bytes = statistics.median(memory_samples)
    return median_peak_bytes


def measure_peak_memory(matrix_a, matrix_b):
    gc.collect()
    tracemalloc.start()
    try:
        tracemalloc.reset_peak()

        result = MatrixMultiplier.multiply(matrix_a, matrix_b)

        _, peak_bytes = tracemalloc.get_traced_memory()

        del result
        return peak_bytes
    finally:
        tracemalloc.stop()


if __name__ == "__main__":
    run_benchmark()
