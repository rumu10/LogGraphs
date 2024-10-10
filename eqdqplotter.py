import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import numpy as np

# Load the CSV file (replace with the actual file path on your system)
file_path = 'data/10_9/eqdq_data_Q10_J40.csv'
data = pd.read_csv(file_path)

# Strip any leading/trailing whitespace from the column names
data.columns = data.columns.str.strip()

print(data)
# Extract the time and status data
time = data['Time'] / 1e6  # Convert time from ns to ms
status_numeric = data['Status']

# Plot the full dataset as a single plot (same as the original plot)
plt.figure(figsize=(20, 5))  # Increase figure size to make all points visible

# Line plot connecting all points
plt.plot(time, status_numeric, color='blue', linewidth=1, label='Status (connected)')

# Plot True values (1) as green and False values (0) as red
plt.scatter(time[status_numeric == 1], status_numeric[status_numeric == 1], color='green', label='True (1)', s=20)
plt.scatter(time[status_numeric == 0], status_numeric[status_numeric == 0], color='red', label='False (0)', s=20)

# Adjust y-axis ticks to 0 and 1
plt.gca().set_yticks([0, 1])
plt.gca().set_yticklabels(['Enqueue', 'Dequeue'])

# Remove scientific notation from x-axis
plt.gca().xaxis.set_major_formatter(ScalarFormatter(useOffset=False))
plt.ticklabel_format(style='plain', axis='x')

# Ensure all data points are shown by adjusting the x-axis limits
plt.xlim(time.min(), time.max())

# Labels and title
plt.xlabel('Time (ms)')  # Update the label to reflect ms
plt.ylabel('Status')

# Display legend
plt.legend()

# Show the first plot
plt.show()

# Now create multiple subplots, zoomed in to show around 30 sets of data
chunk_size = 30
num_chunks = int(np.ceil(len(time) / chunk_size))  # Determine the number of subplots needed

# Create subplots
fig, axs = plt.subplots(num_chunks, 1, figsize=(20, num_chunks * 3), sharey=True)

# Plot each chunk
for i in range(num_chunks):
    # Define the range for each chunk
    start_idx = i * chunk_size
    end_idx = min((i + 1) * chunk_size, len(time))

    # Plot the status data for this chunk
    axs[i].plot(time[start_idx:end_idx], status_numeric[start_idx:end_idx], color='blue', linewidth=1)
    axs[i].scatter(time[start_idx:end_idx][status_numeric[start_idx:end_idx] == 1], 
                   status_numeric[start_idx:end_idx][status_numeric[start_idx:end_idx] == 1], 
                   color='green', s=20, label='True (1)')
    axs[i].scatter(time[start_idx:end_idx][status_numeric[start_idx:end_idx] == 0], 
                   status_numeric[start_idx:end_idx][status_numeric[start_idx:end_idx] == 0], 
                   color='red', s=20, label='False (0)')
    
    # Adjust y-axis ticks to 0 and 1
    axs[i].set_yticks([0, 1])
    axs[i].set_yticklabels(['Enqueue', 'Dequeue'])
    
    # Set x-axis limits for each chunk
    axs[i].set_xlim(time[start_idx], time[end_idx - 1])
    axs[i].set_xlabel('Time (ms)')
    axs[i].set_ylabel('Status')
    
    # Set the title for each subplot
    axs[i].set_title(f'Time from {time[start_idx]:.2f} ms to {time[end_idx - 1]:.2f} ms')

# Add a legend to the last subplot
axs[-1].legend()

# Remove scientific notation from x-axis
for ax in axs:
    ax.xaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    ax.ticklabel_format(style='plain', axis='x')

# Adjust layout
plt.tight_layout()

# Show the subplots
plt.show()
