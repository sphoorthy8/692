import matplotlib.pyplot as plt
import sys

# Path to your stats.txt file (replace with your path)
STATS_FILE = (
    "/home/sphoo/gem5/configs/example/stats_multi_workload/add_run1/stats.txt"
)

# Metrics to plot (customize this list)
METRICS_TO_PLOT = [
    "system.cpu.dcache.overall_miss_rate::total",
    "system.cpu.icache.overall_miss_rate::total",
    "system.cpu.numCycles",
    "system.cpu.committedInsts",
]


def plot_metrics():
    metrics = []
    values = []
    try:
        with open(STATS_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("----------"):
                    parts = line.split()
                    metric_name = parts[0]
                    if metric_name in METRICS_TO_PLOT:
                        metrics.append(metric_name)
                        values.append(float(parts[1]))

        plt.figure(figsize=(12, 6))
        plt.bar(metrics, values, color="skyblue")
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Value")
        plt.title("Gem5 Simulation Metrics")
        plt.tight_layout()
        plt.savefig("metrics_plot.png")
        print("Plot saved to metrics_plot.png")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    plot_metrics()
