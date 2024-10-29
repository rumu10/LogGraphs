import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load the CSV file
#file_path = "./data/10_22/Q10_J40/J3.csv"  # Update with your actual file path

file_path = "./data/10_29/Q10_J40/J1.csv"  # Update with your actual file path
raw_data = pd.read_csv(file_path, header=None)

# Drop column 5 (mostly NaN) and clean the dataset
cleaned_data = raw_data.drop(columns=[5])
cleaned_data.dropna(subset=[0, 1, 2, 3], inplace=True)

# Assign proper column names
cleaned_data.columns = [
    'timer', 'enqueue_interval', 'deque_timer', 'dequeue_interval',
    'frames_in_queue', 'running_avg_5', 'queue_size(D)'
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
    }
]

# Create subplots
fig, axs = plt.subplots(len(subplots_to_include) + 1, 1,
                        figsize=(10, (len(subplots_to_include) + 1) * 3),
                        sharex=True)

# Plot each subplot dynamically
for i, subplot in enumerate(subplots_to_include):
    axs[i].plot(subplot['x'], subplot['y'], subplot['color'])
    axs[i].set_ylabel(subplot['ylabel'])
    axs[i].set_title(subplot['title'], pad=10)
    axs[i].yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
    axs[i].yaxis.get_major_formatter().set_scientific(False)
    axs[i].grid(True)

    # Set x-axis limit for this subplot
    axs[i].set_xlim([5, 15])
    #axs[i].set_xlim(auto= 'true')

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

# Save the figure
#plt.savefig('combined_subplots_with_queue_sizes.png')

# Show the plot
plt.show()
