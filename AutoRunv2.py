import subprocess
import time
import psutil
import pyautogui
import csv
from datetime import datetime
import pandas as pd

# Path configurations
unity_path = r"C:\Users\claypool-316\Desktop\Rumu\Build\UnityClient.exe"
python_path = r"C:\Users\claypool-316\Desktop\Rumu\pythonProject\.venv\Scripts\python"
jitter_script = "jitter.py"
config_file = "config.csv"  # Path to your config CSV
log_file_path = "run_logs.csv"

# Load the config CSV
config_data = pd.read_csv(config_file)

# Ensure columns exist
required_columns = {"param", "value"}
if not required_columns.issubset(config_data.columns):
    raise ValueError(f"Config CSV must contain columns: {required_columns}")

# Extract parameters from the config
buffer_sizes = config_data.loc[config_data['param'] == 'bufferSize', 'value'].astype(int).tolist()
time_to_waits = config_data.loc[config_data['param'] == 'timeToWait', 'value'].astype(float).tolist()
round_durations = config_data.loc[config_data['param'] == 'roundDuration', 'value'].astype(int).tolist()
algorithms = config_data.loc[config_data['param'] == 'algo', 'value'].tolist()

# Calculate the total number of runs for each parameter set
total_runs = len(buffer_sizes)
if len(buffer_sizes) != len(time_to_waits) or len(buffer_sizes) != len(round_durations) or len(buffer_sizes) != len(algorithms):
    raise ValueError("Config parameters (bufferSize, timeToWait, roundDuration, algo) must have the same number of entries.")

# Initialize CSV logging
with open(log_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Run Number", "Start Time", "End Time", "Jitter Duration (s)", "Run Duration (s)", "Stop Time (s)", "Buffer Size", "Time To Wait", "Round Duration", "Algorithm"])

# Function to log messages to the CSV file
def log_to_csv(run_number, start_time, end_time, jitter_duration, run_duration, stop_time, buffer_size, time_to_wait, round_duration, algo):
    with open(log_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            run_number,
            start_time,
            end_time,
            jitter_duration,
            run_duration,
            stop_time,
            buffer_size,
            time_to_wait,
            round_duration,
            algo,
        ])

# Main script
for i in range(total_runs):
    print(f"Starting UnityClient.exe (Run {i + 1}/{total_runs})")

    # Extract parameters for this run
    buffer_size = buffer_sizes[i]
    time_to_wait = time_to_waits[i]
    round_duration = round_durations[i]
    algo = algorithms[i]

    # Update the jitter script with the buffer size and algo
    jitter_command = [python_path, jitter_script, str(buffer_size), algo]

    # Log start time
    start_time = datetime.now()

    # Start Raspberry Pi jitter script
    jitter_start = time.time()
    s_clean = subprocess.Popen(jitter_command)
    s_clean.wait()
    jitter_end = time.time()
    jitter_duration = jitter_end - jitter_start

    # Launch UnityClient.exe
    process = subprocess.Popen(unity_path)

    # Run Unity for the set duration
    time.sleep(round_duration)

    # Close UnityClient.exe using Alt+F4
    stop_start = time.time()
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'UnityClient.exe':
            print("Attempting to close UnityClient.exe with Alt+F4...")
            pyautogui.hotkey("alt", "f4")
            time.sleep(6)
            if proc.is_running():
                proc.terminate()
                print("Forcefully terminated UnityClient.exe as it was still running.")
    stop_end = time.time()
    stop_duration = stop_end - stop_start

    # Log end time
    end_time = datetime.now()

    # Log details to the CSV file
    log_to_csv(
        run_number=i + 1,
        start_time=start_time.strftime('%Y-%m-%d %H:%M:%S'),
        end_time=end_time.strftime('%Y-%m-%d %H:%M:%S'),
        jitter_duration=round(jitter_duration, 2),
        run_duration=round_duration,
        stop_time=round(stop_duration, 2),
        buffer_size=buffer_size,
        time_to_wait=time_to_wait,
        round_duration=round_duration,
        algo=algo,
    )

    print(f"Run {i + 1}/{total_runs} logged successfully.")

print("All runs completed. Logs saved to", log_file_path)
