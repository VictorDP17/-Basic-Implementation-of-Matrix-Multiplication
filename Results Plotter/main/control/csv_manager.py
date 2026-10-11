import csv
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = next(
    (
        folder
        for folder in (SCRIPT_DIR, *SCRIPT_DIR.parents)
        if folder.name.endswith("Basic-Implementation-of-Matrix-Multiplication")
    ),
    None
)
if ROOT is None:
    raise FileNotFoundError(
        "The root folder Basic-Implementation-of-Matrix-Multiplication was not found"
    )

COLUMNS = ["language", "benchmark", "matrix_size", "mean_time", "median_time", "variance_time", "peak_memory_bytes"]
LANGUAGES = ["Java", "Python", "C"]
BENCHMARKS = ["random", "identity", "zero"]
JAVA_BENCHMARKS = {
    "multiplyRandomMatrices": "random",
    "multiplyIdentityMatrices": "identity",
    "multiplyZeroMatrices": "zero",
}

class CsvManager:

    @staticmethod
    def find_csv(filename):
        path = next(
            (p for p in ROOT.rglob(filename) if p.is_file()),
            None
        )

        if path is None:
            raise FileNotFoundError(
                f"{filename} was not found in {ROOT}"
            )

        return path

    @staticmethod
    def read_java(path):
        results = []
        with path.open(newline="", encoding="utf-8-sig") as file:
            for row in csv.DictReader(file):
                method = row["Benchmark"].rsplit(".", 1)[-1]
                score_ms = float(row["Score"].replace(",", "."))
                results.append({
                    "language": "Java",
                    "benchmark": JAVA_BENCHMARKS[method],
                    "matrix_size": int(row["Param: MATRIX_SIZE"]),
                    "time_ms": score_ms
                })
        return results

    @staticmethod
    def read_python_or_c(path, language):
        results = []
        with path.open(newline="", encoding="utf-8-sig") as file:
            for row in csv.DictReader(file):
                results.append({
                    "language": language,
                    "benchmark": row["benchmark"],
                    "matrix_size": int(row["matrix_size"]),
                    "time_ms": float(row["time_ms"].replace(",", "."))
                })
        return results

    def save_csv(path, rows):
        rows = sorted(
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
            for row in rows:
                writer.writerow({
                    **row,
                    "time_ms": f"{row['time_ms']:.6f}",
                })
