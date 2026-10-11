import csv


class BenchmarkSaver:

    @staticmethod
    def save_results(results):
        with open("python_results.csv", "w", newline="") as file:
            fieldnames = ["language", "benchmark", "matrix_size", "mean_time", "median_time", "variance_time", "peak_memory_bytes"]

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print("\nResults saved to python_results.csv")
