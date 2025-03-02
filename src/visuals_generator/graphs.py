import matplotlib.pyplot as plt
import numpy as np

def __generate_graph__(metric_name, metric_values, directory):
    schedulers = list(metric_values.keys())
    values = list(metric_values.values())
 
    x_axis = np.arange(len(schedulers))
    fig, ax = plt.subplots()
    bars = plt.bar(x = x_axis, height = values)
    ax.bar_label(bars)
    for bars in ax.containers:
        ax.bar_label(bars)
    
    plt.axhline(0, color = "black", linewidth = 1)  
    plt.xticks(x_axis, schedulers)
    plt.ylabel(metric_name)
    plt.xlabel("Scheduler")
    plt.title(metric_name + " vs Scheduler")
    plt.savefig(directory + metric_name.lower().replace(" ", "_") + ".png")

def save_comparison_graphs(results, directory):
    schedulers = list(results.keys())
    rew_mean = {}
    tardiness_mean = {}
    makespan_mean = {}
    gap_to_solver = {}

    for scheduler in schedulers:
        if scheduler != "solver":
            rew_mean[scheduler] = results[scheduler]["rew_mean"]
            tardiness_mean[scheduler] = results[scheduler]["tardiness_mean"]
            if "gap_to_solver" in results[scheduler]:
                gap_to_solver[scheduler] = results[scheduler]["gap_to_solver"]
            
        makespan_mean[scheduler] = results[scheduler]["makespan_mean"]
        
    metrics = {"Average Reward": rew_mean, "Average Tardiness":tardiness_mean, 
                "Average Makespan": makespan_mean}
    if len(gap_to_solver) > 0:
        metrics["Gap To Solver"] = gap_to_solver

    for metric_name in metrics:
        __generate_graph__(metric_name, metrics[metric_name], directory)