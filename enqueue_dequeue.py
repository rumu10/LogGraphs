import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'data.csv'  # Replace with your actual file name if different
df = pd.read_csv(file_path, header=None, names=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])

# Create a figure with subplots
fig, axs = plt.subplots(4, 1, figsize=(10, 10), sharex=True)

# Plot for Enqueue (Columns A and B)
axs[0].plot(df['A'], df['B'], color='red')
axs[0].set_ylabel('Frame Time (ms)')
axs[0].set_title('Enqueue')
axs[0].legend(loc="upper right")
axs[0].grid(True)

# Plot for Queue Size (Columns E and F)
axs[1].plot(df['F'], df['E'], color='green')
axs[1].set_ylabel('Frames')
axs[1].set_title('Queue Size')
axs[1].legend(loc="upper right")
axs[1].grid(True)

# Plot for Dequeue (Columns C and D)
axs[2].plot(df['C'], df['D'], color='blue')
axs[2].set_ylabel('Frame Time (ms)')
axs[2].set_title('Dequeue')
axs[2].legend(loc="upper right")
axs[2].grid(True)

# Plot for Moving Average (Columns G and H)
axs[3].plot(df['G'], df['H'], color='purple')
axs[3].set_xlabel('Time (s)')
axs[3].set_ylabel('Moving Average (ns)')
axs[3].set_title('Moving Average')
axs[3].legend(loc="upper right")
axs[3].grid(True)

# Add a main title for the entire figure
fig.suptitle('Adjusted E-Policy - Target Queue 10 No Jitter', fontsize=16)

# Adjust layout to prevent overlapping
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Show the plot
plt.show()
