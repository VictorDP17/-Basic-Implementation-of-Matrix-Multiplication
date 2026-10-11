import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

COLUMNS = [
    "language",
    "benchmark",
    "matrix_size",
    "mean_time",
    "median_time",
    "variance_time",
    "peak_memory_bytes",
]
LANGUAGES = ["Java", "Python", "C"]
BENCHMARKS = ["random", "identity", "zero"]


class CsvManager:
    @staticmethod
    def find_csv(filename):
        path = ROOT / filename
        if not path.is_file():
            raise FileNotFoundError(
                f"{filename} was not found in project root: {ROOT}"
            )
        return path


    @staticmethod
    def read_results(path):
        with path.open(newline="", encoding="utf-8") as file:
            return [
                {
                    "language": row["language"],
                    "benchmark": row["benchmark"],
                    "matrix_size": int(row["matrix_size"]),
                    "mean_time": float(row["mean_time"]),
                    "median_time": float(row["median_time"]),
                    "variance_time": float(row["variance_time"]),
                    "peak_memory_bytes": float(row["peak_memory_bytes"]),
                }
                for row in csv.DictReader(file)
            ]


    @staticmethod
    def save_csv(path, rows):
        sorted_rows = sorted(
            rows,
            key=lambda row: (
                BENCHMARKS.index(row["benchmark"]),
                row["matrix_size"],
                LANGUAGES.index(row["language"]),
            ),
        )
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(sorted_rows)

