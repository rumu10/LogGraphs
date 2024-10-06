import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV data
df = pd.read_csv('eqdq2.csv')

# Clean the column names (remove spaces)
df.columns = df.columns.str.strip()

# Strip leading/trailing spaces in the 'Status' column and convert to integers
df['Status'] = df['Status'].str.strip().map({'False': 0, 'True': 1})

# Convert the Time from nanoseconds to milliseconds
df['Time'] = df['Time'] / 1e6  # Convert to milliseconds

# Detect the densest region in time
time_counts = df['Time'].value_counts().sort_index()
densest_start_time = time_counts.idxmax()
time_window = 16.6667  # Focus on a 50ms window around the densest point

# Automatically zoom to the densest region
start_time = densest_start_time - time_window / 2
end_time = densest_start_time + time_window / 2

# Filter the data within the automatically chosen time window
zoom_df = df[(df['Time'] >= start_time) & (df['Time'] <= end_time)]

# Separate Enqueue and Dequeue events in the filtered data
enqueue_df = zoom_df[zoom_df['Status'] == 0]
dequeue_df = zoom_df[zoom_df['Status'] == 1]

# Plot Enqueue (Status = 0)
plt.scatter(enqueue_df['Time'], [0] * len(enqueue_df), color='blue', label='Enqueue', marker='o')

# Plot Dequeue (Status = 1)
plt.scatter(dequeue_df['Time'], [1] * len(dequeue_df), color='red', label='Dequeue', marker='o')

# Add titles and labels
plt.title('Queue Operations Over Time (Auto Zoom)')
plt.xlabel('Time (milliseconds)')
plt.yticks([0, 1], ['Enqueue', 'Dequeue'])

# Show the legend
plt.legend()

# Display the plot
plt.show()
