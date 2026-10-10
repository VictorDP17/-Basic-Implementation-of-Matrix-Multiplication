from pathlib import Path
import matplotlib.pyplot as plt

from control.csv_manager import CsvManager

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

JAVA_CSV = "java_results.csv"
PYTHON_CSV = "python_results.csv"
C_CSV = "c_results.csv"

RESULTS_DIR = ROOT / "results"
JAVA_NORMALIZED = RESULTS_DIR / "java_normalized.csv"
COMBINED = RESULTS_DIR / "combined_results.csv"
PLOTS_DIR = RESULTS_DIR / "plots"

LANGUAGES = ["Java", "Python", "C"]
BENCHMARKS = ["random", "identity", "zero"]


def create_plots(rows):
    PLOTS_DIR.mkdir(exist_ok=True)

    for benchmark in BENCHMARKS:
        benchmark_rows = [row for row in rows if row["benchmark"] == benchmark]
        if not benchmark_rows:
            continue

        fig, ax = plt.subplots(figsize=(8, 5))
        for language in LANGUAGES:
            language_rows = sorted(
                (row for row in benchmark_rows if row["language"] == language),
                key=lambda row: row["matrix_size"],
            )
            if language_rows:
                ax.plot(
                    [row["matrix_size"] for row in language_rows],
                    [row["time_ms"] for row in language_rows],
                    marker="o",
                    label=language,
                )

        sizes = sorted({row["matrix_size"] for row in benchmark_rows})
        ax.set_title(f"Matrix multiplication — {benchmark} matrices")
        ax.set_xlabel("Matrix size (n × n)")
        ax.set_ylabel("Average execution time (ms)")
        ax.set_xticks(sizes)
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.tight_layout()
        output = PLOTS_DIR / f"time_comparison_{benchmark}.png"
        fig.savefig(output, dpi=200)
        plt.close(fig)
        print(f"Created {benchmark} plot in: {output}")


def main():
    java_results = CsvManager.read_java(CsvManager.find_csv(JAVA_CSV))
    python_results = CsvManager.read_python_or_c(CsvManager.find_csv(PYTHON_CSV), "Python")
    c_results = CsvManager.read_python_or_c(CsvManager.find_csv(C_CSV), "C")

    RESULTS_DIR.mkdir(exist_ok=True)
    CsvManager.save_csv(JAVA_NORMALIZED, java_results)
    print(f"Created normalized Java CSV in: {JAVA_NORMALIZED}")

    CsvManager.save_csv(COMBINED, java_results + python_results + c_results)
    print(f"Created combined results CSV in: {COMBINED}")

    create_plots(java_results + python_results + c_results)

    print("Finished process.")


if __name__ == "__main__":
    main()
