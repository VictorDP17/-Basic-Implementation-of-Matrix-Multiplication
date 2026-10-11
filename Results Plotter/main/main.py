import math
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from control.csv_manager import BENCHMARKS, LANGUAGES, ROOT, CsvManager

JAVA_CSV = "java_results.csv"
PYTHON_CSV = "python_results.csv"
C_CSV = "c_results.csv"

RESULTS_DIR = ROOT / "results"
COMBINED = RESULTS_DIR / "combined_results.csv"
PLOTS_DIR = RESULTS_DIR / "plots"


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    java_results = CsvManager.read_results(CsvManager.find_csv(JAVA_CSV))
    python_results = CsvManager.read_results(CsvManager.find_csv(PYTHON_CSV))
    c_results = CsvManager.read_results(CsvManager.find_csv(C_CSV))

    all_results = java_results + python_results + c_results
    CsvManager.save_csv(COMBINED, all_results)
    print(f"Combined results saved to: {COMBINED}")

    create_plots(all_results)
    print("Finished process.")


def create_plots(rows):
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    for benchmark in BENCHMARKS:
        benchmark_rows = [row for row in rows if row["benchmark"] == benchmark]

        fig_time, ax_time = plt.subplots(figsize=(9, 5.5))
        fig_memory, ax_memory = plt.subplots(figsize=(9, 5.5))

        for language in LANGUAGES:
            language_rows = get_language_rows(benchmark_rows, language)

            means, medians, sd, sizes, bytes_used = get_rows_attributes(language_rows)

            line_color = plot_mean_and_variation(ax_time, language, means, sd, sizes)
            plot_median(ax_time, language, line_color, medians, sizes)
            plot_memory(ax_memory, language, line_color, bytes_used, sizes)

        set_plot_time_parameters(ax_time, benchmark, benchmark_rows, fig_time)
        set_plot_memory_parameters(ax_memory, benchmark, benchmark_rows, fig_memory)

        output_time = PLOTS_DIR / f"time_comparison_{benchmark}.png"
        output_memory = PLOTS_DIR / f"memory_comparison_{benchmark}.png"
        fig_time.savefig(output_time, dpi=200)
        plt.close(fig_time)

        fig_memory.savefig(output_memory, dpi=200)
        plt.close(fig_memory)

        print(f"Created plot: {output_time} and {output_memory}")


def get_language_rows(benchmark_rows, language):
    language_rows = sorted(
        (row for row in benchmark_rows if row["language"] == language),
        key=lambda row: row["matrix_size"],
    )
    return language_rows


def get_rows_attributes(language_rows):
    sizes = [row["matrix_size"] for row in language_rows]
    means = [row["mean_time"] for row in language_rows]
    medians = [row["median_time"] for row in language_rows]
    sd = [math.sqrt(row["variance_time"]) for row in language_rows]
    bytes_used = [row["peak_memory_bytes"] for row in language_rows]

    return means, medians, sd, sizes, bytes_used


def plot_mean_and_variation(ax, language, means, sd, sizes):
    mean_plot = ax.errorbar(
        sizes,
        means,
        yerr=sd,
        marker="o",
        linestyle="-",
        capsize=4,
        label=f"{language} mean ± SD",
    )
    line_color = mean_plot.lines[0].get_color()
    return line_color


def plot_median(ax, language, line_color, medians, sizes):
    ax.plot(
        sizes,
        medians,
        marker="x",
        linestyle="--",
        color=line_color,
        label=f"{language} median",
    )

def plot_memory(ax, language, line_color, bytes_used, sizes):
    ax.plot(
        sizes,
        bytes_used,
        marker="o",
        linestyle="-",
        color=line_color,
        label=f"{language} Bytes used",
    )


def set_plot_time_parameters(ax, benchmark, benchmark_rows, fig):
    sizes = sorted({row["matrix_size"] for row in benchmark_rows})
    ax.set_title(f"Matrix multiplication — {benchmark} matrices")
    ax.set_xlabel("Matrix size (n × n)")
    ax.set_ylabel("Execution time (ms, logarithmic scale)")
    ax.set_xticks(sizes)
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()

def set_plot_memory_parameters(ax, benchmark, benchmark_rows, fig):
    sizes = sorted({row["matrix_size"] for row in benchmark_rows})
    ax.set_title(f"Matrix multiplication — {benchmark} matrices")
    ax.set_xlabel("Matrix size (n × n)")
    ax.set_ylabel("Memory (Bytes, logarithmic scale)")
    ax.set_xticks(sizes)
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()


if __name__ == "__main__":
    main()
