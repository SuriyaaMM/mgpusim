import os
import subprocess
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def build_benchmarks(benchmarks_dir : str, benchmark_algorithms: list) -> None:
    for root, dirs, files in os.walk(benchmarks_dir):
        for benchmark_algorithm in benchmark_algorithms:
            if benchmark_algorithm in dirs:
                benchmark_algorithm_dir = os.path.join(root, benchmark_algorithm)
                print(f'Building {benchmark_algorithm} in {benchmark_algorithm_dir}')

                run_result = subprocess.run(['go', 'build'], cwd = benchmark_algorithm_dir, capture_output = True, text = True)

                if run_result.returncode != 0:
                    print(f'Failed to build {benchmark_algorithm}!!')
                else:
                    print(f"{benchmark_algorithm} build successfully")

                executable_path = os.path.join(benchmark_algorithm_dir, f"{benchmark_algorithm}.exe")

                print(f'Generating metrics for {executable_path}')
                generate_metrics = subprocess.run([executable_path, '-timing', '--report-all'], cwd=benchmark_algorithm_dir, capture_output=True, text=True)

                if generate_metrics.returncode != 0:
                    print(f'Failed to generate metrics for {benchmark_algorithm}!!')
                else:
                    print(f"Metrics generated successfully for {benchmark_algorithm}")


# GPT generated
def parse_metrics(file_path):
    metrics = {
        "L1VTLB": {"hit": 0, "miss": 0, "mshr-hit": 0},
        "L1STLB": {"hit": 0, "miss": 0, "mshr-hit": 0},
        "L1ITLB": {"hit": 0, "miss": 0, "mshr-hit": 0},
        "L2TLB": {"hit": 0, "miss": 0, "mshr-hit": 0},
        "L1VCache": {"read-hit": 0, "read-miss": 0, "read-mshr-hit": 0, "write-hit": 0, "write-miss": 0, "write-mshr-hit": 0},
        "L1SCache": {"read-hit": 0, "read-miss": 0, "read-mshr-hit": 0, "write-hit": 0, "write-miss": 0, "write-mshr-hit": 0},
        "L1ICache": {"read-hit": 0, "read-miss": 0, "read-mshr-hit": 0, "write-hit": 0, "write-miss": 0, "write-mshr-hit": 0},
        "L2Cache": {"read-hit": 0, "read-miss": 0, "read-mshr-hit": 0, "write-hit": 0, "write-miss": 0, "write-mshr-hit": 0}
    }

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) < 4:
                continue

            # Extract TLB/Cache type
            tlb_info = parts[1].split('.')[-1]
            tlb_type = tlb_info.split('[')[0]

            # Extract metric type
            metric_type = parts[2].strip()

            # Convert count to a float value
            try:
                count = float(parts[3].strip())
            except ValueError:
                continue

            # Update metrics if the type and metric are found in the dictionary
            if tlb_type in metrics and metric_type in metrics[tlb_type]:
                metrics[tlb_type][metric_type] += count

    return metrics

def plot_metrics(metrics, algorithm_name: str, output_file: str) -> None:
    labels = list(metrics.keys())
    
    # TLB Data
    hits = []
    misses = []
    mshr_hits = []

    # Cache Data
    read_hits = []
    read_misses = []
    read_mshr_hits = []
    write_hits = []
    write_misses = []
    write_mshr_hits = []

    for label in labels:
        if "hit" in metrics[label]: 
            hits.append(metrics[label]["hit"])
            misses.append(metrics[label]["miss"])
            mshr_hits.append(metrics[label]["mshr-hit"])
            read_hits.append(0)
            read_misses.append(0)
            read_mshr_hits.append(0)
            write_hits.append(0)
            write_misses.append(0)
            write_mshr_hits.append(0)
        else:  
            read_hits.append(metrics[label]["read-hit"])
            read_misses.append(metrics[label]["read-miss"])
            read_mshr_hits.append(metrics[label]["read-mshr-hit"])
            write_hits.append(metrics[label]["write-hit"])
            write_misses.append(metrics[label]["write-miss"])
            write_mshr_hits.append(metrics[label]["write-mshr-hit"])
            hits.append(0)
            misses.append(0)
            mshr_hits.append(0)

    x = range(len(labels))
    width = 0.15

    plt.figure(figsize=(14, 10))

    # GPT Generated

    # TLB bars
    plt.bar([i - 1.5 * width for i in x], hits, width=width, label='Hits', color='#6baed6', edgecolor='black', hatch='/')
    plt.bar([i - 0.5 * width for i in x], misses, width=width, label='Misses', color='#fd8d3c', edgecolor='black', hatch='\\')
    plt.bar([i + 0.5 * width for i in x], mshr_hits, width=width, label='MSHR Hits', color='#31a354', edgecolor='black', hatch='x')

    # Cache bars (read/write)
    plt.bar([i + 1.5 * width for i in x], read_hits, width=width, label='Read Hits', color='#3182bd', edgecolor='black', hatch='//')
    plt.bar([i + 2.5 * width for i in x], read_misses, width=width, label='Read Misses', color='#e6550d', edgecolor='black', hatch='\\\\')
    plt.bar([i + 3.5 * width for i in x], read_mshr_hits, width=width, label='Read MSHR Hits', color='#74c476', edgecolor='black', hatch='xx')
    plt.bar([i + 4.5 * width for i in x], write_hits, width=width, label='Write Hits', color='#2171b5', edgecolor='black', hatch='*')
    plt.bar([i + 5.5 * width for i in x], write_misses, width=width, label='Write Misses', color='#a63603', edgecolor='black', hatch='o')
    plt.bar([i + 6.5 * width for i in x], write_mshr_hits, width=width, label='Write MSHR Hits', color='#238b45', edgecolor='black', hatch='.')

    plt.xlabel('TLB/Cache Types')
    plt.ylabel('Counts')
    plt.title(f'Performance Metrics for {algorithm_name}')
    plt.xticks(x, labels, rotation=45)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()



def process_metrics(benchmarks_dir: str, benchmark_algorithms: list) -> None:
    for benchmark_algorithm in benchmark_algorithms:
        algorithm_dir = os.path.join(benchmarks_dir, benchmark_algorithm)
        metrics_file = os.path.join(algorithm_dir, 'metrics.csv')
        output_file = os.path.join(algorithm_dir, f'{benchmark_algorithm}_metrics_plot.png')

        if os.path.exists(metrics_file):
            print(f"Processing {metrics_file} for {benchmark_algorithm}")
            metrics = parse_metrics(metrics_file)
            plot_metrics(metrics, benchmark_algorithm, output_file)
            print(f"Plot saved to {output_file}")

def main() -> None:
    sns.set_theme(style="darkgrid", palette="icefire", font_scale=1.2)
    benchmark_dir = './samples'
    # Add algorithms for benchmarking if needed
    benchmark_algorithms = ['pagerank']
    build_benchmarks(benchmark_dir, benchmark_algorithms)
    process_metrics(benchmark_dir, benchmark_algorithms)

if __name__ == '__main__':
    main()
