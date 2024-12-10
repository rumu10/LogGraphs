# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.ticker as ticker
# import os
#
#
# def calculate_average_queue_size(data, column='queue_size(D)'):
#     """
#     Calculate the average queue size for the specified column.
#     """
#     return data[column].mean()
#
#
# def count_interrupts(data, column='dequeue_interval', threshold=33.333334):
#     """
#     Count the number of interrupts in the specified column based on the given threshold.
#     """
#     return (data[column] > threshold).sum()
#
#
# def process_csv(file_path, output_folder):
#     """
#     Process a single CSV file: clean data, calculate metrics, and generate plots.
#     """
#     # Load the CSV file
#     raw_data = pd.read_csv(file_path, header=None)
#
#     # Drop rows that contain any blank (NaN) values
#     cleaned_data = raw_data.dropna(how='any').copy()
#
#     # Save the cleaned data back to a new file in the output folder
#     cleaned_file_name = os.path.basename(file_path).replace(".csv", "_cleaned.csv")
#     cleaned_file_path = os.path.join(output_folder, cleaned_file_name)
#     cleaned_data.to_csv(cleaned_file_path, header=False, index=False)
#     print(f"Cleaned file saved as {cleaned_file_path}")
#
#     # Assign proper column names
#     cleaned_data.columns = [
#         'timer', 'enqueue_interval', 'deque_timer', 'dequeue_interval',
#         'frames_in_queue', 'running_avg_5', 'queue_size(D)', 'expected_sleep', 'sleep_difference'
#     ]
#
#     # Calculate metrics using the modular functions
#     average_queue_size = calculate_average_queue_size(cleaned_data)
#     interrupt_count = count_interrupts(cleaned_data)
#
#     # Define the subplots to include based on cleaned data
#     subplots_to_include = [
#         {
#             'title': 'Enqueue',
#             'x': cleaned_data['timer'],
#             'y': cleaned_data['enqueue_interval'],
#             'ylabel': 'Frame Time [ms]',
#             'color': 'b'
#         },
#         {
#             'title': 'Dequeue',
#             'x': cleaned_data['deque_timer'],
#             'y': cleaned_data['dequeue_interval'],
#             'ylabel': 'Frame Time [ms]',
#             'color': 'r'
#         }
#     ]
#
#     # Create subplots
#     fig, axs = plt.subplots(len(subplots_to_include) + 1, 1,
#                             figsize=(10, (len(subplots_to_include) + 1) * 3),
#                             sharex=True)
#
#     # Plot each subplot dynamically
#     for i, subplot in enumerate(subplots_to_include):
#         axs[i].plot(subplot['x'], subplot['y'], color=subplot['color'])
#         axs[i].set_ylabel(subplot['ylabel'])
#         axs[i].set_title(subplot['title'], pad=10)
#         axs[i].yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
#         axs[i].yaxis.get_major_formatter().set_scientific(False)
#         axs[i].grid(True)
#         axs[i].set_xlim([4, 30])
#         # Synchronize y-axis across all plots
#         axs[i].set_ylim([0, 60])
#
#     # Combined Queue Size plot
#     combined_ax = axs[-1]
#     combined_ax.plot(cleaned_data['timer'], cleaned_data['frames_in_queue'],
#                      label='Queue Size (Enqueue)', color='g')
#     combined_ax.plot(cleaned_data['deque_timer'], cleaned_data['queue_size(D)'],
#                      label='Queue Size (Dequeue)', color='r')
#
#     # Set title and labels for the combined plot
#     combined_ax.set_title('Queue Sizes: Enqueue vs Dequeue', pad=10)
#     combined_ax.set_ylabel('Frames')
#     combined_ax.legend(loc='lower right')
#     combined_ax.grid(True)
#
#     # Annotate the average queue size and interrupt count on the plot
#     combined_ax.text(0.95, 0.95, f"Avg Queue Size: {average_queue_size:.2f}\nInterrupts: {interrupt_count}",
#                      transform=combined_ax.transAxes, fontsize=10,
#                      verticalalignment='top', horizontalalignment='right',
#                      bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
#
#     # Adjust layout
#     plt.subplots_adjust(hspace=0.4)
#     plt.tight_layout()
#
#     # Save the plot to the output folder with a PNG extension
#     output_filename = os.path.join(output_folder, os.path.basename(file_path).replace(".csv", ".png"))
#     plt.savefig(output_filename)
#     print(f"Saved plot for {os.path.basename(file_path)} as {output_filename}")
#
#     # Close the plot to free memory
#     plt.close(fig)
#
#     # Return calculated metrics
#     return average_queue_size, interrupt_count
#
#
# # Main processing script
# def main(folder_path):
#     # Create a summary list to hold results
#     summary_data = []
#
#     # Create a new folder for each iteration
#     for run_idx, filename in enumerate(os.listdir(folder_path), start=1):
#         if filename.endswith(".csv"):
#             file_path = os.path.join(folder_path, filename)
#
#             # Create an output folder for the current run
#             run_folder = os.path.join(folder_path, f"iteration_{run_idx}")
#             os.makedirs(run_folder, exist_ok=True)
#
#             # Process the CSV file and save results in the run folder
#             avg_queue_size, interrupt_count = process_csv(file_path, run_folder)
#
#             # Store the results in the summary list
#             summary_data.append({
#                 "Iteration": run_idx,
#                 "File": filename,
#                 "Average Queue Size (Dequeue)": avg_queue_size,
#                 "Interrupt Count (Dequeue Rate)": interrupt_count
#             })
#
#     # Save the summary data to a CSV file
#     summary_file_path = os.path.join(folder_path, "summary.csv")
#     summary_df = pd.DataFrame(summary_data)
#     summary_df.to_csv(summary_file_path, index=False)
#     print(f"Summary file saved as {summary_file_path}")
#
#
# # Run the script
# if __name__ == "__main__":
#     folder_path = "./data/12-3/NoWhile"  # Update with your folder path
#     main(folder_path)

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os


def calculate_average_queue_size(data, column='queue_size(D)'):
    """
    Calculate the average queue size for the specified column.
    """
    return data[column].mean()


def calculate_standard_deviation(data, column='queue_size(D)'):
    """
    Calculate the standard deviation of the queue size for the specified column.
    """
    return data[column].std()


def count_interrupts(data, column='dequeue_interval', threshold=33.333334):
    """
    Count the number of interrupts in the specified column based on the given threshold.
    """
    return (data[column] > threshold).sum()


def calculate_interrupt_magnitude(data, column='dequeue_interval', threshold=33.333334):
    """
    Get the magnitudes of interrupts as a comma-separated string.
    Each interrupt magnitude is the value exceeding the threshold.
    """
    interrupt_values = data[column][data[column] > threshold]
    return ", ".join(map(str, interrupt_values))



def process_csv(file_path, output_folder):
    """
    Process a single CSV file: clean data, calculate metrics, and generate plots.
    """
    # Load the CSV file
    raw_data = pd.read_csv(file_path, header=None)

    # Drop rows that contain any blank (NaN) values
    cleaned_data = raw_data.dropna(how='any').copy()

    # Save the cleaned data back to a new file in the output folder
    cleaned_file_name = os.path.basename(file_path).replace(".csv", "_cleaned.csv")
    cleaned_file_path = os.path.join(output_folder, cleaned_file_name)
    cleaned_data.to_csv(cleaned_file_path, header=False, index=False)
    print(f"Cleaned file saved as {cleaned_file_path}")

    # Assign proper column names
    cleaned_data.columns = [
        'timer', 'enqueue_interval', 'deque_timer', 'dequeue_interval',
        'frames_in_queue', 'running_avg_5', 'queue_size(D)', 'expected_sleep', 'sleep_difference'
    ]

    # Calculate metrics using the modular functions
    average_queue_size = calculate_average_queue_size(cleaned_data)
    std_queue_size = calculate_standard_deviation(cleaned_data)
    interrupt_count = count_interrupts(cleaned_data)
    interrupt_magnitude = calculate_interrupt_magnitude(cleaned_data)

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
        axs[i].set_xlim(cleaned_data['timer'].min(), cleaned_data['timer'].max())
        axs[i].set_ylim(cleaned_data['enqueue_interval'].min(), cleaned_data['enqueue_interval'].max())

        # Synchronize y-axis across all plots

    # Combined Queue Size plot
    combined_ax = axs[-1]
    combined_ax.plot(cleaned_data['timer'], cleaned_data['frames_in_queue'],
                     label='Queue Size (Enqueue)', color='g')
    combined_ax.plot(cleaned_data['deque_timer'], cleaned_data['queue_size(D)'],
                     label='Queue Size (Dequeue)', color='r')

    # Set title and labels for the combined plot
    combined_ax.set_title('Queue Sizes: Enqueue vs Dequeue', pad=10)
    combined_ax.set_ylabel('Frames')
    # combined_ax.legend(loc='lower right')
    combined_ax.grid(True)

    combined_ax.text(
        0.95,
        0.95,
        f"Avg Queue Size: {average_queue_size:.2f}\n"
        f"Interrupts: {interrupt_count}\n"
        f"Interrupt Mag: {interrupt_magnitude}\n"  # Remove .2f for the string
        f"Std Dev: {std_queue_size:.2f}",
        transform=combined_ax.transAxes,
        fontsize=10,
        verticalalignment='bottom',
        horizontalalignment='right',
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5)
    )

    # Adjust layout
    plt.subplots_adjust(hspace=0.4)
    plt.tight_layout()

    # Save the plot to the output folder with a PNG extension
    output_filename = os.path.join(output_folder, os.path.basename(file_path).replace(".csv", ".png"))
    plt.savefig(output_filename)
    print(f"Saved plot for {os.path.basename(file_path)} as {output_filename}")

    # Close the plot to free memory
    plt.close(fig)

    # Return calculated metrics
    return average_queue_size, std_queue_size, interrupt_count, interrupt_magnitude


# Main processing script
def main(folder_path, run_logs_path, summary_file_path):
    # Create a summary list to hold results
    # Load run_logs.csv
    run_logs = pd.read_csv(run_logs_path)
    summary_data = []

    # Create a new folder for each iteration
    for run_idx, filename in enumerate(os.listdir(folder_path), start=1):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)

            # Create an output folder for the current run
            run_folder = os.path.join(folder_path, f"iteration_{run_idx}")
            os.makedirs(run_folder, exist_ok=True)

            # Process the CSV file and save results in the run folder
            avg_queue_size, std_queue_size, interrupt_count, interrupt_magnitude = process_csv(file_path, run_folder)

            # Fetch corresponding buffer size and jitter value from run_logs.csv
            buffer_size = run_logs.loc[run_idx - 1, 'Buffer Size']
            jitter_value = run_logs.loc[run_idx - 1, 'Jitter Magnitude']

            # Append to summary
            summary_data.append({
                "Iteration": run_idx,
                "File": filename,
                "Buffer Size": buffer_size,
                "Added Jitter Magnitude": jitter_value,
                "Average Queue Size": avg_queue_size,
                "Std Dev Queue Size": std_queue_size,
                "Interrupt Count": interrupt_count,
                "Interrupts Magnitude(ms)": interrupt_magnitude
            })

        # Save the summary data to a new CSV file
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv(summary_file_path, index=False)
        print(f"Summary file saved as {summary_file_path}")


# Run the script
if __name__ == "__main__":
    folder_path = "./data/2024-12-09_18-00-46/Runs"  # Update with your folder path
    run_logs_path = "./data/2024-12-09_18-00-46/script_summary.csv"  # Path to run_logs.csv
    summary_file_path = "./data/2024-12-09_18-00-46/iteration_summary.csv"  # Path for the new summary file
    main(folder_path, run_logs_path, summary_file_path)
