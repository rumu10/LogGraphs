import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load the CSV file
file_path = "./data/11_11/Q2_J100/jitter_values_20241112_114403.csv"   # Update with your actual file path
raw_data = pd.read_csv(file_path, header=None)

# Drop rows that contain any blank (NaN) values
cleaned_data = raw_data.dropna(how='any').copy()

# Assign proper column names, including the new columns
cleaned_data.columns = [
    'timer', 'enqueue_interval', 'deque_timer', 'dequeue_interval',
    'frames_in_queue', 'running_avg_5', 'queue_size(D)', 'expected_sleep', 'sleep_difference'
]

# Define the subplots to include based on cleaned data
subplots_to_include = [
    {
        'title': 'Enqueue',
        'x': cleaned_data['timer'],
        'y': cleaned_data['enqueue_interval'],
        'ylabel': 'Frame Time [ms]',
        'color': 'b'
    },
    {
        'title': 'Dequeue',
        'x': cleaned_data['deque_timer'],
        'y': cleaned_data['dequeue_interval'],
        'ylabel': 'Frame Time [ms]',
        'color': 'r'
    },
    # {
    #     'title': 'Time Taken to Execute Update',
    #     'x': cleaned_data['timer'],
    #     'y': cleaned_data['time_taken_update'],
    #     'ylabel': 'Time [ms]',
    #     'color': 'purple'
    # },
    # {
    #     'title': 'Sleep Difference (Real - Expected)',
    #     'x': cleaned_data['timer'],
    #     'y': cleaned_data['sleep_difference'],
    #     'ylabel': 'Time [ms]',
    #     'color': 'brown'
    # },
    # {
    #     'title': 'Start Time Interval',
    #     'x': cleaned_data['timer'],
    #     'y': cleaned_data['start_time_interval'],
    #     'ylabel': 'Time Interval [ms]',
    #     'color': 'cyan'
    # }
]

# Create subplots
fig, axs = plt.subplots(len(subplots_to_include) + 1, 1,
                        figsize=(10, (len(subplots_to_include) + 1) * 3),
                        sharex=True)

# Plot each subplot dynamically
for i, subplot in enumerate(subplots_to_include):
    axs[i].plot(subplot['x'], subplot['y'], color=subplot['color'])
    axs[i].set_ylabel(subplot['ylabel'])
    axs[i].set_title(subplot['title'], pad=10)
    axs[i].yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
    axs[i].yaxis.get_major_formatter().set_scientific(False)
    axs[i].grid(True)

    # Set x-axis limit for this subplot
    axs[i].set_xlim([2, 60])

# Combined Queue Size plot
combined_ax = axs[-1]
combined_ax.plot(cleaned_data['timer'], cleaned_data['frames_in_queue'],
                 label='Queue Size (Enqueue)', color='g')
combined_ax.plot(cleaned_data['deque_timer'], cleaned_data['queue_size(D)'],
                 label='Queue Size (Dequeue)', color='r')

# Set title and labels for the combined plot
combined_ax.set_title('Queue Sizes: Enqueue vs Dequeue', pad=10)
combined_ax.set_ylabel('Frames')
combined_ax.legend(loc='lower right')
combined_ax.grid(True)

# Avoid scientific notation on the y-axis
combined_ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
combined_ax.yaxis.get_major_formatter().set_scientific(False)

# Set the x-axis label only on the last subplot
axs[-1].set_xlabel('Time [seconds]')

# Adjust layout
plt.subplots_adjust(hspace=0.4)  # Increase spacing between subplots
plt.tight_layout()

# Show the plot
plt.show()
