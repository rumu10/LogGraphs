import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV data
df = pd.read_csv('eqdq.csv')

# Clean the column names (remove spaces)
df.columns = df.columns.str.strip()

# Strip leading/trailing spaces in the 'Status' column and convert it to integers
df['Status'] = df['Status'].str.strip().map({'False': 0, 'True': 1})

# Convert the Time from nanoseconds to milliseconds (or microseconds)
df['Time'] = df['Time'] / 1e6  # Convert to milliseconds (adjust as needed)

# Define the time window to zoom in on (e.g., 412700 to 412800 milliseconds)
start_time = 4.41275e6
end_time = 4.41300e6

# Filter the data within the selected time window
zoom_df = df[(df['Time'] >= start_time) & (df['Time'] <= end_time)]

# Separate the Enqueue and Dequeue events in the filtered data
enqueue_df = zoom_df[zoom_df['Status'] == 0]
dequeue_df = zoom_df[zoom_df['Status'] == 1]

# Add jitter to separate overlapping points visually
enqueue_y_jitter = np.random.normal(0, 0.01, len(enqueue_df))
dequeue_y_jitter = np.random.normal(0, 0.01, len(dequeue_df))

# Plot Enqueue (Status = 0) as blue dots with jitter
plt.scatter(enqueue_df['Time'], [0 + jitter for jitter in enqueue_y_jitter], color='blue', label='Enqueue', marker='o')

# Plot Dequeue (Status = 1) as red dots with jitter
plt.scatter(dequeue_df['Time'], [1 + jitter for jitter in dequeue_y_jitter], color='red', label='Dequeue', marker='o')

# Add titles and labels
plt.title('Queue Operations Over Time (Zoomed)')
plt.xlabel('Time (milliseconds)')
plt.yticks([0, 1], ['Enqueue', 'Dequeue'])  # Set y-axis labels as Enqueue and Dequeue

# Show the legend to differentiate between Enqueue and Dequeue
plt.legend()

# Display the plot
plt.show()
