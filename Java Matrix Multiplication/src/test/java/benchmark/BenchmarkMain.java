package benchmark;

import org.openjdk.jmh.profile.GCProfiler;
import org.openjdk.jmh.results.Result;
import org.openjdk.jmh.results.RunResult;
import org.openjdk.jmh.runner.Runner;
import org.openjdk.jmh.runner.options.Options;
import org.openjdk.jmh.runner.options.OptionsBuilder;
import org.openjdk.jmh.runner.options.TimeValue;
import org.openjdk.jmh.util.Statistics;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Collection;
import java.util.Locale;

public class BenchmarkMain {

    private static final String RESULTS_FILE = "java_results.csv";

    public static void main(String[] args) throws Exception {
        Options options = new OptionsBuilder()
                .include(BenchmarkRunner.class.getSimpleName())
                .warmupIterations(1)
                .warmupTime(TimeValue.seconds(1))
                .measurementIterations(5)
                .measurementTime(TimeValue.seconds(1))
                .forks(1)
                .addProfiler(GCProfiler.class)
                .build();

        Collection<RunResult> results = new Runner(options).run();

        saveResults(results);
        System.out.println("Results saved to " + RESULTS_FILE);
    }

    private static void saveResults(Collection<RunResult> results) throws IOException {

        try (BufferedWriter writer = Files.newBufferedWriter(Path.of(RESULTS_FILE), StandardCharsets.UTF_8)) {

            writer.write(
                    "language,benchmark,matrix_size," +
                            "mean_time,median_time,variance_time," +
                            "peak_memory_bytes"
            );
            writer.newLine();

            for (RunResult runResult : results) {
                Result<?> timeResult = runResult.getPrimaryResult();
                Statistics stats = timeResult.getStatistics();

                String benchmark = normalizeBenchmarkName(runResult.getParams().getBenchmark());
                String matrixSize = runResult.getParams().getParam("MATRIX_SIZE");
                Result<?> memoryResult = runResult.getSecondaryResults().get("gc.alloc.rate.norm");

                double mean = stats.getMean();
                double median = stats.getPercentile(50);
                double variance = stats.getVariance();
                double allocatedBytesPerOp = memoryResult.getScore();

                writer.write(String.format(
                        Locale.US,
                        "Java,%s,%s,%.9f,%.9f,%.9f,%.3f",
                        benchmark,
                        matrixSize,
                        mean,
                        median,
                        variance,
                        allocatedBytesPerOp
                ));
                writer.newLine();
            }
        }
    }

    private static String normalizeBenchmarkName(String name) {
        if (name.endsWith("multiplyRandomMatrices")) {
            return "random";
        }
        if (name.endsWith("multiplyIdentityMatrices")) {
            return "identity";
        }
        if (name.endsWith("multiplyZeroMatrices")) {
            return "zero";
        }
        throw new IllegalArgumentException(
                "Unknown benchmark: " + name
        );
    }
}
