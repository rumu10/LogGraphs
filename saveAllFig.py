import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

# Specify the folder path containing the CSV files
folder_path = "./data/11_11/Q2_J4"  # Update with your folder path

# Iterate through all CSV files in the specified folder
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)

        # Load the CSV file
        raw_data = pd.read_csv(file_path, header=None)

        # Drop rows that contain any blank (NaN) values
        cleaned_data = raw_data.dropna(how='any').copy()

        # Assign proper column names
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
            }
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
        plt.subplots_adjust(hspace=0.4)
        plt.tight_layout()

        # Save the plot to the same folder with a PNG extension
        output_filename = os.path.join(folder_path, filename.replace(".csv", ".png"))
        plt.savefig(output_filename)
        print(f"Saved plot for {filename} as {output_filename}")

        # Close the plot to free memory
        plt.close(fig)
