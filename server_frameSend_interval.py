import pandas as pd
import matplotlib.pyplot as plt
import os

def process_server_log(file_path, output_folder):
    """
    Process a single server log file: clean data, remove unwanted rows, and generate plots.
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

    # Drop invalid rows
    cleaned_data = cleaned_data.dropna().reset_index(drop=True)

    # **Keep only data where 3.0 <= Timer <= 63.0**
    cleaned_data = cleaned_data[(cleaned_data["Timer"] >= 5.0) & (cleaned_data["Timer"] <= 63.0)].reset_index(drop=True)

    if cleaned_data.empty:
        print(f"Skipping {file_path} (no valid Timer data in range 3.0 - 63.0).")
        return

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Save the cleaned data
    cleaned_file_name = os.path.basename(file_path).replace(".csv", "_cleaned.csv")
    cleaned_file_path = os.path.join(output_folder, cleaned_file_name)
    cleaned_data.to_csv(cleaned_file_path, header=True, index=False)
    print(f"Cleaned server log saved as {cleaned_file_path}")

    # Generate the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the data
    ax.plot(cleaned_data['Timer'], cleaned_data['Interval'], label='Interval vs Timer', color='blue', linewidth=2)

    # Set title and labels
    ax.set_title('Server Log: Interval vs Timer', fontsize=14, fontweight='bold')
    ax.set_xlabel('Timer (s)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Interval (ms)', fontsize=12, fontweight='bold')

    # Add grid for better visualization
    ax.grid(True, linestyle='--', linewidth=0.5)

    # Set axis limits to 3 - 63
    ax.set_xlim([3, 63])
    ax.set_ylim([cleaned_data["Interval"].min() * 0.9, cleaned_data["Interval"].max() * 1.1])

    # Add a legend
    ax.legend(loc="upper right")

    # Save the plot in the same "plots/" folder
    plot_file_path = os.path.join(output_folder, os.path.basename(file_path).replace(".csv", ".png"))
    plt.savefig(plot_file_path, bbox_inches="tight")
    print(f"Plot saved as {plot_file_path}")

    # Close the plot to free memory
    plt.close(fig)

def main(server_logs_folder, plots_folder):
    """
    Main function to process all server logs and save output to the plots folder.
    """
    # Ensure the plots folder exists
    os.makedirs(plots_folder, exist_ok=True)

    # List all server log files
    server_log_files = [f for f in os.listdir(server_logs_folder) if f.endswith(".csv")]

    if not server_log_files:
        print("No server log files found.")
        return

    # Process each server log file
    for log_file in server_log_files:
        file_path = os.path.join(server_logs_folder, log_file)
        process_server_log(file_path, plots_folder)

if __name__ == "__main__":
    # Folder containing the server logs
    server_logs_folder = "./data/2025-02-27_18-35-52/Server"  # Update path as needed

    # Folder to store all cleaned files & plots
    plots_folder = "./data/2025-02-27_18-35-52/Server/plots"  # Save everything here

    # Run the main processing function
    main(server_logs_folder, plots_folder)
