import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load the CSV file
file_path = 'test2.csv'  # Update with your file path
data = pd.read_csv(file_path)

# Assign appropriate column names
data.columns = ['timer', 'enqueue_interval', 'deque_timer', 'dequeue_interval',
                'frames_in_queue', 'moving_avg', 'running_avg_5']

# Convert string columns to numeric (if applicable)
data['timer'] = pd.to_numeric(data['timer'], errors='coerce')
data['enqueue_interval'] = pd.to_numeric(data['enqueue_interval'], errors='coerce')
data['deque_timer'] = pd.to_numeric(data['deque_timer'], errors='coerce')
data['dequeue_interval'] = pd.to_numeric(data['dequeue_interval'], errors='coerce')
data['frames_in_queue'] = pd.to_numeric(data['frames_in_queue'], errors='coerce')
data['moving_avg'] = pd.to_numeric(data['moving_avg'], errors='coerce')
data['running_avg_5'] = pd.to_numeric(data['running_avg_5'], errors='coerce')

# Drop any rows with missing values after conversion
data.dropna(inplace=True)

# Create subplots
fig, axs = plt.subplots(5, 1, figsize=(10, 20), sharex=True)

# 1. Enqueue timer vs Enqueue interval (in nanoseconds)
axs[0].plot(data['timer'], data['enqueue_interval'], 'b')
axs[0].set_ylabel('Enqueue Interval (B) [ns]')
axs[0].set_title('Enqueue Timer vs Enqueue Interval', pad=0)
axs[0].yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
axs[0].yaxis.get_major_formatter().set_scientific(False)
axs[0].grid(True)

# 2. Dequeue timer vs Dequeue interval (in nanoseconds)
axs[1].plot(data['timer'], data['dequeue_interval'], 'r')
axs[1].set_ylabel('Dequeue Interval (D) [ns]')
axs[1].set_title('Dequeue Timer vs Dequeue Interval')
axs[1].yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
axs[1].yaxis.get_major_formatter().set_scientific(False)
axs[1].grid(True)

# 3. Frames in Queue vs Enqueue timer
axs[2].plot(data['timer'], data['frames_in_queue'], 'g')
axs[2].set_ylabel('Frames in Queue (E)')
axs[2].set_title('Frames in Queue vs Enqueue Timer')
axs[2].yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
axs[2].grid(True)

# 4. Moving Average vs Enqueue timer
axs[3].plot(data['timer'], data['moving_avg'], 'm')
axs[3].set_ylabel('Moving Average (F)')
axs[3].set_title('Moving Average vs Enqueue Timer')
axs[3].yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
axs[3].grid(True)

# 5. Running Average (Window Size 5) vs Enqueue Timer
axs[4].plot(data['timer'], data['running_avg_5'], 'c')
axs[4].set_xlabel('Enqueue Timer (A) [seconds]')
axs[4].set_ylabel('Running Avg (Window 5) (G)')
axs[4].set_title('Running Average (Window Size 5) vs Enqueue Timer')
axs[4].yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
axs[4].grid(True)

# Set the x-axis limits for all subplots
for ax in axs:
    ax.set_xlim([0, 5])

# Automatically adjust subplot parameters to give some padding
plt.tight_layout()

# Save the figure as one image file
plt.savefig('combined_subplots.png')

# Show the figure with all subplots
plt.show()