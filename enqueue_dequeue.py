import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load the CSV file
file_path = './data/10_16/Q10_J40_SRA.csv'  # Update with your actual file path
data = pd.read_csv(file_path)

# Assign appropriate column names
data.columns = ['timer', 'enqueue_interval', 'deque_timer', 'dequeue_interval',
                'frames_in_queue', 'moving_avg', 'running_avg_5', 'queue_size(D)']

# Convert string columns to numeric (if applicable)
for col in data.columns:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Drop any rows with missing values after conversion
data.dropna(inplace=True)

# Define the subplots you want to include
subplots_to_include = []

# Enqueue subplot
subplots_to_include.append({
    'title': 'Enqueue',
    'x': data['timer'],
    'y': data['enqueue_interval'],
    'ylabel': 'Frame Time [ms]',
    'color': 'b'
})

# Uncomment to add Queue Size during Enqueue subplot
# subplots_to_include.append({
#     'title': 'Queue Size (Enqueue)',
#     'x': data['timer'],
#     'y': data['frames_in_queue'],
#     'ylabel': 'Frames',
#     'color': 'g'
# })

# Dequeue subplot
subplots_to_include.append({
    'title': 'Dequeue',
    'x': data['deque_timer'],
    'y': data['dequeue_interval'],
    'ylabel': 'Frame Time [ms]',
    'color': 'r'
})

# Uncomment to add Queue Size during Dequeue subplot
# subplots_to_include.append({
#     'title': 'Queue Size (Dequeue)',
#     'x': data['deque_timer'],
#     'y': data['queue_size(D)'],
#     'ylabel': 'Frames',
#     'color': 'b'
# })

# Running Average subplot
# subplots_to_include.append({
#     'title': 'Running Average vs Enqueue Timer',
#     'x': data['timer'],
#     'y': data['running_avg_5'],
#     'ylabel': 'Running Avg',
#     'xlabel': 'Time [seconds]',
#     'color': 'c'
# })

# Moving Average vs Enqueue Timer subplot
# subplots_to_include.append({
#     'title': 'Moving Average vs Enqueue Timer',
#     'x': data['timer'],
#     'y': data['moving_avg'],
#     'ylabel': 'Moving Average',
#     'color': 'm'
# })

# Create subplots including the combined queue size plot
fig, axs = plt.subplots(len(subplots_to_include) + 1, 1,
                        figsize=(10, (len(subplots_to_include) + 1) * 3),
                        sharex=True)

# Loop through each subplot data and plot dynamically
for i, subplot in enumerate(subplots_to_include):
    axs[i].plot(subplot['x'], subplot['y'], subplot['color'])
    axs[i].set_ylabel(subplot['ylabel'])
    axs[i].set_title(subplot['title'], pad=10)
    axs[i].yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
    axs[i].yaxis.get_major_formatter().set_scientific(False)
    axs[i].grid(True)

# Combined queue size subplot
combined_ax = axs[-1]
combined_ax.plot(data['timer'], data['frames_in_queue'], label='Queue Size (Enqueue)', color='g')
combined_ax.plot(data['deque_timer'], data['queue_size(D)'], label='Queue Size (Dequeue)', color='r')

# Set title and labels for the combined plot
combined_ax.set_title('Queue Sizes: Enqueue vs Dequeue', pad=10)
combined_ax.set_ylabel('Frames')
combined_ax.legend(loc='upper right')
combined_ax.grid(True)

# Use scalar formatter to avoid scientific notation
combined_ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
combined_ax.yaxis.get_major_formatter().set_scientific(False)

# Set x-axis label only on the last subplot
axs[-1].set_xlabel('Time [seconds]')

# Adjust layout
plt.subplots_adjust(hspace=0.4)  # Increase spacing between subplots
plt.tight_layout()

# Save the figure
plt.savefig('combined_subplots_with_queue_sizes.png')

# Show the figure
plt.show()
