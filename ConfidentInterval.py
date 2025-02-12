import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os


# Function to compute confidence interval
def compute_confidence_interval(data):
    """Computes 95% confidence interval, handling edge cases."""
    data = np.array(data)
    data = data[~np.isnan(data)]  # Remove NaN values

    if len(data) < 2:
        return np.nan, np.nan  # Avoid calculation for insufficient data

    mean = np.mean(data)
    std_err = stats.sem(data)  # Standard error of the mean

    if np.std(data) == 0:
        return mean, mean  # If no variation, CI is just the mean

    ci = stats.t.interval(0.95, len(data) - 1, loc=mean, scale=std_err)
    return ci


# Load the iteration summary CSV
iteration_summary_path = "./data/2025-02-10_18-39-05/iteration_summary.csv"

if not os.path.exists(iteration_summary_path):
    raise FileNotFoundError(f"Error: {iteration_summary_path} not found.")

df = pd.read_csv(iteration_summary_path)

# Multiply jitter values by 2
df["Jitter Magnitude"] = df["Jitter Magnitude"] * 2

# Extract relevant columns
metrics = {
    "Average Queue": "Average Queue Size",
    "IM (ms/s)": "Interrupt Mag (ms/s)",
    "Average FT": "Average Frame Time",
    "FTSD":"Std Dev Frame Time"
}

# Unique jitter values
jitter_values = sorted(df["Jitter Magnitude"].unique()) * 2

# Unique policies based on buffer size and thresholding method
df["Policy"] = df.apply(lambda row: f"{row['Policy']}({row['Buffer Size']})" if "E-Policy" in row["Policy"]
else f"{row['Policy']}({row['Buffer Size']}, T={row['Threshold']}, D={row['Decay']})", axis=1)
policies = df["Policy"].unique()

# Generate individual plots
for metric_name, column_name in metrics.items():
    plt.figure(figsize=(8, 5))
    plt.title(f"{metric_name} with Confidence Interval")

    for policy in policies:
        means, ci_lows, ci_highs, jitter_positions = [], [], [], []

        for jitter in jitter_values:
            subset = df[(df["Jitter Magnitude"] == jitter) & (df["Policy"] == policy)][column_name]

            if subset.empty:
                continue  # Skip missing settings

            mean_value = np.mean(subset)
            ci_low, ci_high = compute_confidence_interval(subset)

            means.append(mean_value)
            ci_lows.append(ci_low)
            ci_highs.append(ci_high)
            jitter_positions.append(jitter)

        if means:
            # Plot error bars for confidence intervals
            plt.errorbar(jitter_positions, means,
                         yerr=[np.array(means) - np.array(ci_lows), np.array(ci_highs) - np.array(means)],
                         fmt='o', capsize=5, label=policy)

    plt.xlabel("Jitter Magnitude (ms)")
    plt.ylabel(metric_name)
    plt.xticks(jitter_values)
    plt.grid(True)
    plt.legend(title="Policy", loc="lower right", bbox_to_anchor=(1, 1))  # Legend moved outside for clarity
    plt.show()
