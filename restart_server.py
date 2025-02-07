import requests
import os
import csv
import sys
from datetime import datetime
import json

def save_server_log(batch_dir, run_number, log_data):
    """
    Save server logs to a CSV file in the batch directory with a timestamp.
    """
    # Generate a unique file name with timestamp for the log
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(batch_dir, f"server_log_run_{run_number}_{timestamp}.csv")

    if not log_data:  # Check if the log data is empty
        print(f"Run {run_number}: No log data received. Skipping log creation.")
        return

    # Parse and save the log data
    with open(log_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Interval", "Time"])  # Write column headers
        for entry in log_data:
            try:
                interval, time_val = entry.split(",")
                writer.writerow([interval.strip(), time_val.strip()])
            except ValueError:
                print(f"Skipping malformed entry: {entry}")
    print(f"Server log saved: {log_file}")


def restart_server(batch_dir, run_number):
    """
    Restart the server and save logs in the batch directory.
    """
    try:
        # Replace with your Node.js server's URL
        url = "http://130.215.30.29:7777/restart"
        response = requests.post(url, json={"message": "Restart requested"})

        if response.status_code == 200:
            log_data = json.loads(response.text).get("serverLog", [])  # Parse the JSON response and get the "serverLog" array
            print(f"Run {run_number}: Received log data.")
            save_server_log(batch_dir, run_number, log_data)
        else:
            print(
                f"Run {run_number}: Failed to restart server. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Run {run_number}: Error occurred while restarting the server: {e}")


if __name__ == "__main__":
    # Get the run number and batch directory from the command-line arguments
    if len(sys.argv) < 3:
        print("Error: Run number and batch directory are required as command-line arguments.")
        sys.exit(1)

    run_number = sys.argv[1]  # Run number passed from the auto-run script
    batch_directory = sys.argv[2]  # Batch directory passed from the auto-run script

    # Process the current run
    print(f"Processing run {run_number}")
    restart_server(batch_directory, run_number)
