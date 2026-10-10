import csv


class BenchmarkSaver:

    @staticmethod
    def save_results(results):
        with open("python_results.csv", "w", newline="") as file:
            fieldnames = ["language", "benchmark", "matrix_size", "time_ms"]

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print("\nResults saved to python_results.csv")
