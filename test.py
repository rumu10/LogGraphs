import pandas as pd
import matplotlib.pyplot as plt

# Load the uploaded CSV file
file_path = "./data/test.csv"
df = pd.read_csv(file_path, header=None, names=['A', 'B', 'C', 'D', 'E'])

# Create 3 subplots: (1) Expected vs Actual Interval, (2) Difference, (3) Update Loop Interval
fig, axs = plt.subplots(3, 1, figsize=(10, 9), sharex=True)

# Subplot 1: Expected vs Actual Interval
axs[0].plot(df['C'], df['A'], 'b-', label='Expected Interval')
axs[0].plot(df['C'], df['D'], 'r-', label='Actual Interval')
axs[0].set_title('Expected vs Actual Interval')
axs[0].set_ylabel('Interval [ms]')
axs[0].legend(loc='upper right')
axs[0].grid(True)

# Subplot 2: Difference between Expected and Actual Interval
axs[1].plot(df['C'], df['E'], 'g-')
axs[1].set_title('Difference (Expected - Actual Interval)')
axs[1].set_ylabel('Difference [ms]')
axs[1].grid(True)

# Subplot 3: Update Loop Interval
axs[2].plot(df['C'], df['B'], 'c-')
axs[2].set_title('Update Loop Interval')
axs[2].set_xlabel('Time [seconds]')
axs[2].set_ylabel('Interval [ms]')
axs[2].grid(True)

# Apply correct x-axis limits based on actual data
x_min = 11.8  # Start at 0 seconds
x_max = 11.9  # End at the maximum value in the 'C' column (e.g., 7 seconds)

for ax in axs:
    ax.set_xlim(x_min, x_max)  # Set the same x-axis limits for all subplots

# Adjust layout to avoid overlap
plt.tight_layout()

# Show the plot
plt.show()
