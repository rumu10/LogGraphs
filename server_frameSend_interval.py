import pandas as pd
import matplotlib.pyplot as plt
import os

def process_server_log(file_path):
    """
    Process a single server log file: clean data, calculate metrics, and generate plots.
    """
    # Load the server log file
    raw_data = pd.read_csv(file_path, header=None)

    # Drop rows that contain any blank (NaN) values
    cleaned_data = raw_data.dropna(how='any').copy()

    # Assign proper column names
    cleaned_data.columns = ['Interval', 'Timer']

    # Convert columns to numeric, handling errors
    cleaned_data['Interval'] = pd.to_numeric(cleaned_data['Interval'], errors='coerce')
    cleaned_data['Timer'] = pd.to_numeric(cleaned_data['Timer'], errors='coerce')

    # Drop rows with invalid data
    cleaned_data = cleaned_data.dropna().reset_index(drop=True)

    # Save the cleaned data back to a new file in the output folder
    # cleaned_file_name = os.path.basename(file_path).replace(".csv", "_cleaned.csv")
    # cleaned_file_path = os.path.join(file_path, cleaned_file_name)
    # cleaned_data.to_csv(cleaned_file_path, header=True, index=False)
    # print(f"Cleaned server log saved as {cleaned_file_path}")

    # Generate the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the data with a smooth line
    ax.plot(cleaned_data['Timer'], cleaned_data['Interval'], label='Interval vs Timer', color='blue', linewidth=2)

    # Highlight individual points if needed
    # ax.scatter(cleaned_data['Timer'], cleaned_data['Interval'], color='red', s=10, label='Data Points')

    # Set title and labels
    ax.set_title('Server Log: Interval vs Timer')
    ax.set_xlabel('Timer (s)')
    ax.set_ylabel('Interval (ms)')

    # Add grid for better visualization
    # ax.grid(True, linestyle='--', linewidth=0.5)

    # Set axis limits dynamically based on data range
    ax.set_xlim([3, 60])
    ax.set_ylim([0, 60])

    # Add a legend
    ax.legend()

    # Save the plot to the output folder
    plot_file_path = os.path.join(file_path, os.path.basename(file_path).replace(".csv", ".png"))
    # plt.savefig(plot_file_path)
    # print(f"Plot saved as {plot_file_path}")

    plt.show()

    # Close the plot to free memory
    plt.close(fig)

def main(server_logs_folder):
    """
    Main function to process all server logs and save output to the corresponding iteration folders.
    """
    # List all server log files
    server_log_files = [f for f in os.listdir(server_logs_folder) if f.endswith(".csv")]

    if not server_log_files:
        print("No server log files found.")
        return

    # Process each server log file
    for idx, log_file in enumerate(server_log_files, start=1):
        # Determine the corresponding iteration folder
        # iteration_folder = os.path.join(iteration_folders_base, f"iteration_{idx}")

        # Ensure the iteration folder exists
        # if not os.path.exists(iteration_folder):
        #     print(f"Warning: Iteration folder '{iteration_folder}' does not exist. Skipping {log_file}.")
        #     continue
        #
        # Process the server log and save the output in the iteration folder
        file_path = os.path.join(server_logs_folder, log_file)
        process_server_log(file_path)


if __name__ == "__main__":
    # Folder containing the server logs
    server_logs_folder = "./data/2025-02-10_18-39-05/Server"   # Update path as needed

    # Base folder for iteration folders
    # iteration_folders_base = "./data/2025-02-10_18-39-05/Server"  # Update path as needed

    # Run the main processing function
    main(server_logs_folder)
