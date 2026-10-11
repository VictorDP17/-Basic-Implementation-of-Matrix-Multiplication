package benchmark;

import org.openjdk.jmh.profile.GCProfiler;
import org.openjdk.jmh.results.format.ResultFormatType;
import org.openjdk.jmh.runner.Runner;
import org.openjdk.jmh.runner.options.Options;
import org.openjdk.jmh.runner.options.OptionsBuilder;
import org.openjdk.jmh.runner.options.TimeValue;

public class BenchmarkMain {

    public static void main(String[] args) throws Exception {

        Options options = new OptionsBuilder()
                .include(BenchmarkRunner.class.getSimpleName())
                .warmupIterations(1)
                .warmupTime(TimeValue.seconds(1))
                .measurementIterations(5)
                .measurementTime(TimeValue.seconds(1))
                .forks(1)
                .addProfiler(GCProfiler.class)
                .result("java_results.csv")
                .resultFormat(ResultFormatType.CSV)
                .build();

        new Runner(options).run();
    }
}
