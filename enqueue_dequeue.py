import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load the CSV file
file_path = './data/10_9/Q10_NJ_RA.csv'  # Update with your file path
data = pd.read_csv(file_path)

# Assign appropriate column names
data.columns = ['timer', 'enqueue_interval', 'deque_timer', 'dequeue_interval',
                'frames_in_queue', 'moving_avg', 'running_avg_5', 'queue_size(D)']

# Convert string columns to numeric (if applicable)
data['timer'] = pd.to_numeric(data['timer'], errors='coerce')
data['enqueue_interval'] = pd.to_numeric(data['enqueue_interval'], errors='coerce')
data['deque_timer'] = pd.to_numeric(data['deque_timer'], errors='coerce')
data['dequeue_interval'] = pd.to_numeric(data['dequeue_interval'], errors='coerce')
data['frames_in_queue'] = pd.to_numeric(data['frames_in_queue'], errors='coerce')
data['moving_avg'] = pd.to_numeric(data['moving_avg'], errors='coerce')
data['running_avg_5'] = pd.to_numeric(data['running_avg_5'], errors='coerce')
data['queue_size(D)'] = pd.to_numeric(data['queue_size(D)'], errors='coerce')

# Drop any rows with missing values after conversion
data.dropna(inplace=True)

# Define the subplots you want to include dynamically
subplots_to_include = []

# Enqueue subplot
subplots_to_include.append({
    'title': 'Enqueue',
    'x': data['timer'],
    'y': data['enqueue_interval'],
    'ylabel': 'Frame Time[ms]',
    'color': 'b'
})

# Uncomment to add Queue Size during Enqueue subplot
subplots_to_include.append({
    'title': 'Queue Size(Enqueue)',
    'x': data['timer'],
    'y': data['frames_in_queue'],
    'ylabel': 'Frames',
    'color': 'g'
})

# Dequeue subplot
subplots_to_include.append({
    'title': 'Dequeue',
    'x': data['deque_timer'],
    'y': data['dequeue_interval'],
    'ylabel': 'Frame Time[ms]',
    'color': 'r'
})

# Uncomment to add Queue Size during Dequeue subplot
# subplots_to_include.append({
#     'title': 'Queue Size(Dequeue)',
#     'x': data['deque_timer'],
#     'y': data['queue_size(D)'],
#     'ylabel': 'Frames',
#     'color': 'b'
# })

# Running Average subplot
subplots_to_include.append({
    'title': 'Running Average vs Enqueue Timer',
    'x': data['timer'],
    'y': data['running_avg_5'],
    'ylabel': 'Running Avg',
    'xlabel': 'Time(second)',
    'color': 'c'
})

# Moving Average vs Enqueue Timer subplot
# subplots_to_include.append({
#     'title': 'Moving Average vs Enqueue Timer',
#     'x': data['timer'],
#     'y': data['moving_avg'],
#     'ylabel': 'Moving Average',
#     'color': 'm'
# })

# Create subplots dynamically based on how many are in the 'subplots_to_include' list
fig, axs = plt.subplots(len(subplots_to_include), 1, figsize=(10, len(subplots_to_include) * 3), sharex=True)

# Loop through each subplot data and plot dynamically
for i, subplot in enumerate(subplots_to_include):
    axs[i].plot(subplot['x'], subplot['y'], subplot['color'])
    axs[i].set_ylabel(subplot['ylabel'])
    axs[i].set_title(subplot['title'], pad=0)
    axs[i].yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
    axs[i].yaxis.get_major_formatter().set_scientific(False)
    axs[i].grid(True)

# Adjust spacing between subplots
plt.subplots_adjust(hspace=0.4)  # Increase the height spacing between subplots

# Add x-axis label (Time [seconds]) to the last subplot
axs[-1].set_xlabel('Time [seconds]')

# Set the x-axis limits for all subplots
for ax in axs:
    # ax.set_xlim([0, 7])
    ax.set_xlim(auto='true')

# Automatically adjust subplot parameters to give some padding
plt.tight_layout()

# Save the figure as one image file
plt.savefig('combined_subplots_dynamic.png')

# Show the figure with all subplots
plt.show()
