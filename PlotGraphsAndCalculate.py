import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import numpy as np

threshold = 33.333334
# threshold = 25.000005

def calculate_average_queue_size(data, column='queue_size(D)'):
    return data[column].mean()

def calculate_standard_deviation_avg_queue(data, column='queue_size(D)'):
    return data[column].std()

def calculate_average_frame_time(data, column='dequeue_interval'):
    return data[column].mean()

def calculate_standard_deviation_frame_time(data, column='dequeue_interval'):
    return data[column].std()

def count_interrupts(data, column='dequeue_interval', threshold=threshold):
    """Count the number of interrupts in the specified column based on the given threshold."""
    return (data[column] > threshold).sum()

def calculate_interrupt_magnitude(data, column='dequeue_interval', threshold=threshold):
    """Get the magnitudes of interrupts as a comma-separated string."""
    interrupt_values = data[column][data[column] > threshold]
    return ", ".join(map(str, interrupt_values))


def calculate_interrupt_magnitude_per_second(data, column='dequeue_interval', threshold=threshold):
    """
    Calculate the total magnitude of interrupts per second.
    Interrupt magnitude is calculated as (interrupt_value - threshold),
    then summed and divided by total run time.
    """
    # Filter values greater than the threshold
    interrupt_values = data[column][data[column] > threshold]
    # Adjust interrupt values by subtracting the threshold
    adjusted_interrupt_values = interrupt_values - threshold
    # Sum the adjusted interrupt magnitudes
    total_magnitude = adjusted_interrupt_values.sum()
    # Get the total duration from the timer column
    total_duration = data['timer'].max()  # timer is in seconds
    # Compute Interrupt Magnitude per second (IM/s)
    if total_duration > 0:
        return total_magnitude / total_duration
    else:
        return 0  # Prevent division by zero
def calculate_interrupt_std(data, column='dequeue_interval', threshold=threshold):
    """
    Calculate the standard deviation of interrupt magnitudes.
    This measures how much the interrupt values fluctuate from the average excess delay.
    """
    interrupt_values = data[column][data[column] > threshold] - threshold  # Only consider values exceeding threshold
    return np.std(interrupt_values) if len(interrupt_values) > 0 else 0  # Return 0 if no interrupts
def calculate_interrupt_frequency(data, column='dequeue_interval', threshold=threshold):
    """Calculate the interrupt frequency (number of interrupts per second)."""
    total_time = data['timer'].max()  # Get total duration of the run from the timer column
    interrupt_count = (data[column] > threshold).sum()
    return interrupt_count / total_time if total_time > 0 else 0


def process_csv(file_path, output_folder):
    """Process a single CSV file: clean data, calculate metrics, and generate plots."""
    raw_data = pd.read_csv(file_path, header=None)
    cleaned_data = raw_data.dropna(how='any').copy()

    # Save the cleaned data back to a new file
    cleaned_file_name = os.path.basename(file_path).replace(".csv", "_cleaned.csv")
    cleaned_file_path = os.path.join(output_folder, cleaned_file_name)
    cleaned_data.to_csv(cleaned_file_path, header=False, index=False)
    print(f"Cleaned file saved as {cleaned_file_path}")

    # Assign proper column names
    cleaned_data.columns = [
        'timer', 'enqueue_interval', 'deque_timer', 'dequeue_interval',
        'frames_in_queue', 'running_avg_5', 'queue_size(D)', 'expected_sleep', 'sleep_difference',
        'display_latency', 'gap'
    ]

    # Get total run time
    total_run_time = cleaned_data['timer'].max()

    # Calculate metrics
    average_queue_size = calculate_average_queue_size(cleaned_data)
    average_frame_time = calculate_average_frame_time(cleaned_data)
    std_queue_size = calculate_standard_deviation_avg_queue(cleaned_data)
    std_frame_time = calculate_standard_deviation_frame_time(cleaned_data)
    interrupt_count = count_interrupts(cleaned_data)
    interrupt_magnitude = calculate_interrupt_magnitude(cleaned_data)
    interrupt_magnitude_per_second = calculate_interrupt_magnitude_per_second(cleaned_data)
    std_IM = calculate_interrupt_std(cleaned_data)
    interrupt_frequency = calculate_interrupt_frequency(cleaned_data)

    # Define subplots
    subplots_to_include = [
        {'title': 'Enqueue', 'x': cleaned_data['timer'], 'y': cleaned_data['enqueue_interval'], 'ylabel': 'Frame Time [ms]', 'color': 'b'},
        {'title': 'Dequeue', 'x': cleaned_data['deque_timer'], 'y': cleaned_data['dequeue_interval'], 'ylabel': 'Frame Time [ms]', 'color': 'r'}
    ]

    # Create subplots
    fig, axs = plt.subplots(len(subplots_to_include) + 1, 1, figsize=(10, (len(subplots_to_include) + 1) * 3), sharex=True)

    # Plot each subplot
    for i, subplot in enumerate(subplots_to_include):
        axs[i].plot(subplot['x'], subplot['y'], color=subplot['color'])
        axs[i].set_ylabel(subplot['ylabel'])
        axs[i].set_title(subplot['title'], pad=10)
        axs[i].yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
        axs[i].yaxis.get_major_formatter().set_scientific(False)
        axs[i].grid(True)
        axs[i].set_xlim(cleaned_data['timer'].min(), cleaned_data['timer'].max())
        axs[i].set_ylim(cleaned_data['enqueue_interval'].min(), cleaned_data['enqueue_interval'].max())

    # Combined Queue Size plot
    combined_ax = axs[-1]
    combined_ax.plot(cleaned_data['timer'], cleaned_data['frames_in_queue'], label='Queue Size (Enqueue)', color='g')
    combined_ax.plot(cleaned_data['deque_timer'], cleaned_data['queue_size(D)'], label='Queue Size (Dequeue)', color='r')
    combined_ax.set_title('Queue Sizes: Enqueue vs Dequeue', pad=10)
    combined_ax.set_ylabel('Frames')
    combined_ax.grid(True)

    # combined_ax.text(
    #     0.95, 0.95,
    #     f"Avg Queue Size: {average_queue_size:.2f}\n"
    #     f"Interrupts: {interrupt_count}\n"
    #     f"Interrupt Mag: {interrupt_magnitude}\n"
    #     f"Interrupt Mag (ms/s): {interrupt_magnitude_per_second:.2f}\n"
    #     f"Interrupt Freq (/s): {interrupt_frequency:.2f}\n"
    #     f"Std Dev Frame Time: {std_frame_time:.2f}\n"
    #     f"Std Dev Queue Size: {std_queue_size:.2f}",
    #     transform=combined_ax.transAxes,
    #     fontsize=10,
    #     verticalalignment='bottom',
    #     horizontalalignment='right',
    #     bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5)
    # )

    # Save the plot
    output_filename = os.path.join(output_folder, os.path.basename(file_path).replace(".csv", ".png"))
    plt.savefig(output_filename)
    print(f"Saved plot for {os.path.basename(file_path)} as {output_filename}")
    plt.close(fig)

    return average_queue_size,average_frame_time, std_queue_size, std_frame_time, interrupt_count, interrupt_magnitude, interrupt_magnitude_per_second, std_IM , interrupt_frequency

def main(folder_path, run_logs_path, summary_file_path):
    run_logs = pd.read_csv(run_logs_path)
    summary_data = []

    for run_idx, filename in enumerate(os.listdir(folder_path), start=1):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            run_folder = os.path.join(folder_path, f"iteration_{run_idx}")
            os.makedirs(run_folder, exist_ok=True)

            # Process CSV and fetch values
            avg_queue_size,average_frame_time, std_queue_size, std_frame_time, interrupt_count, interrupt_magnitude, interrupt_magnitude_per_second, std_IM , interrupt_frequency = process_csv(file_path, run_folder)

            # Fetch corresponding buffer size, jitter value, and policy
            buffer_size = run_logs.loc[run_idx - 1, 'Buffer Size'] if run_idx - 1 < len(run_logs) else "N/A"
            jitter_value = run_logs.loc[run_idx - 1, 'Jitter Magnitude'] if run_idx - 1 < len(run_logs) else "N/A"
            policy = run_logs.loc[run_idx - 1, 'Policy'] if run_idx - 1 < len(run_logs) else "N/A"
            base_length_qm = run_logs.loc[run_idx - 1, 'baseLength'] if run_idx - 1 < len(run_logs) else "N/A"
            threshold_qm = run_logs.loc[run_idx - 1, 'threshold'] if run_idx - 1 < len(run_logs) else "N/A"
            decay_qm = run_logs.loc[run_idx - 1, 'decay'] if run_idx - 1 < len(run_logs) else "N/A"

            if policy == 0:
                policy = "E-Policy"
            elif policy == 2:
                policy = "QM"
            else:
                policy = "I-Policy"

            summary_data.append({
                "Iteration": run_idx,
                "File": filename,
                "Buffer Size": buffer_size,
                "Jitter Magnitude": jitter_value,
                "Policy": policy,
                "Base Length for Thresholding": base_length_qm,
                "Threshold": threshold_qm,
                "Decay": decay_qm,
                "Average Queue Size": avg_queue_size,
                "Std Dev Queue Size": std_queue_size,
                "Average Frame Time": average_frame_time,
                "Std Dev Frame Time": std_frame_time,
                "Interrupt Count": interrupt_count,
                "Interrupts Magnitude(ms)": interrupt_magnitude,
                "Interrupt Mag (ms/s)": interrupt_magnitude_per_second,
                "Std Interrupt Mag":std_IM,
                "Interrupt Frequency (/s)": interrupt_frequency
            })

    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(summary_file_path, index=False)
    print(f"Summary file saved as {summary_file_path}")

def create_settings_based_csv(iteration_summary_path, settings_output_folder):
    # Load the iteration summary file
    summary_df = pd.read_csv(iteration_summary_path)

    # Select columns that define unique settings (excluding base length)
    settings_columns = ["Buffer Size", "Jitter Magnitude", "Policy", "Threshold", "Decay"]

    # Create the settings_runs folder if it doesn't exist
    os.makedirs(settings_output_folder, exist_ok=True)

    # Group the data based on unique settings
    grouped = summary_df.groupby(settings_columns)

    for setting_values, group in grouped:
        # Generate a unique filename based on the setting values
        buffer_size, jitter, policy, threshold, decay = setting_values
        filename = f"policy_{policy}_buffer_{buffer_size}_jitter_{jitter}_threshold_{threshold}_decay_{decay}.csv"

        # Define the file path
        file_path = os.path.join(settings_output_folder, filename)

        # Save the grouped data to CSV
        group.to_csv(file_path, index=False)

        print(f"Saved settings-based CSV: {file_path}")

if __name__ == "__main__":
    folder_path = "./data/2025-02-27_18-35-52/Client"
    run_logs_path = "./data/2025-02-27_18-35-52/script_summary.csv"
    iteration_summary_path = "./data/2025-02-27_18-35-52/iteration_summary.csv"
    settings_output_folder = "./data/2025-02-27_18-35-52/settings_runs"
    main(folder_path, run_logs_path, iteration_summary_path)

    create_settings_based_csv(iteration_summary_path, settings_output_folder)

