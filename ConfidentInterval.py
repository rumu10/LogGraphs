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
    "FTSD": "Std Dev Frame Time"
}

# Unique jitter values
jitter_values = sorted(df["Jitter Magnitude"].unique())

# Unique policies based on buffer size and thresholding method
df["Policy"] = df.apply(lambda row: f"{row['Policy']}({row['Buffer Size']})" if "E-Policy" in row["Policy"]
else f"{row['Policy']}({row['Buffer Size']}, T={row['Threshold']}, D={row['Decay']})", axis=1)
policies = df["Policy"].unique()

# Define custom bright neon-like colors
custom_colors = [
    "#FF5733",  # Bright Orange
    "#33FF57",  # Neon Green
    "#3357FF",  # Bright Blue
    "#B833FF",  # Vibrant Purple
    "#FF33A1",  # Hot Pink
    "#33FFF3",  # Cyan
    "#F3FF33",  # Bright Yellow-Green
    "#FF8C33",  # Neon Orange
]

# Jittering function based on y-values to prevent overlap
def jitter(values, y_values, base_scale=3.5):
    """Applies jittering based on y-values to keep sorting."""
    scale_factors = np.interp(y_values, (min(y_values), max(y_values)), (base_scale, 2.5))  # Lower y-values get more jitter
    return values + np.random.uniform(-scale_factors, scale_factors, size=len(values))

# Generate individual plots
for metric_name, column_name in metrics.items():
    plt.figure(figsize=(8, 5))
    plt.title(f"{metric_name} with Confidence Interval")

    all_means = []  # Store means for sorting
    all_policies = []

    for policy in policies:
        means, ci_lows, ci_highs, jitter_positions = [], [], [], []

        for jitter_value in jitter_values:
            subset = df[(df["Jitter Magnitude"] == jitter_value) & (df["Policy"] == policy)][column_name]

            if subset.empty:
                continue  # Skip missing settings

            mean_value = np.mean(subset)
            ci_low, ci_high = compute_confidence_interval(subset)

            means.append(mean_value)
            ci_lows.append(ci_low)
            ci_highs.append(ci_high)
            jitter_positions.append(jitter_value)

        if means:
            all_means.append((policy, means, ci_lows, ci_highs, jitter_positions))
            all_policies.append(policy)

    # Sort policies by the first mean value (y-axis sorting)
    all_means.sort(key=lambda x: np.mean(x[1]))  # Sorting based on average y-value

    # Replot using sorted policies
    for i, (policy, means, ci_lows, ci_highs, jitter_positions) in enumerate(all_means):
        jittered_x = jitter(np.array(jitter_positions), np.array(means), base_scale=3.5)  # Apply jitter based on y-values
        color = custom_colors[i % len(custom_colors)]  # Assign color

        # Plot error bars for confidence intervals
        plt.errorbar(jittered_x, means,
                     yerr=[np.array(means) - np.array(ci_lows), np.array(ci_highs) - np.array(means)],
                     fmt='o', capsize=5, label=policy, alpha=0.9, color=color)

        # Draw lines connecting the points for better visualization
        sorted_indices = np.argsort(jittered_x)  # Ensure lines follow correct order
        plt.plot(np.array(jittered_x)[sorted_indices], np.array(means)[sorted_indices],
                 linestyle='-', alpha=0.8, color=color)

    plt.xlabel("Jitter Magnitude (ms)")
    plt.ylabel(metric_name)
    plt.xticks(jitter_values)
    # plt.grid(True)
    plt.legend(title="Policy", loc="lower right", bbox_to_anchor=(1, 1))  # Legend moved outside for clarity
    plt.show()
