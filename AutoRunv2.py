import subprocess
import time
import psutil
import pyautogui
import pandas as pd
import csv
from datetime import datetime
import os

# Path configurations
unity_path = r"C:\Users\claypool-316\Desktop\Rumu\Build\UnityClient.exe"
python_path = r"C:\Users\claypool-316\Desktop\Rumu\pythonProject\.venv\Scripts\python"
jitter_script = "jitter.py"
stop_jitter_script = "stopJitter.py"
server_script = "runServerScript.py"
log_from_server_script = "restart_server.py"
config_file = r"C:\Users\claypool-316\AppData\LocalLow\DefaultCompany\UnityClient\Resources\config.csv"


# Create a single folder for the batch
base_dir = r"C:\Users\claypool-316\Desktop\Rumu\pythonProject\data"
batch_dir_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
batch_directory = os.path.join(base_dir, batch_dir_name)
os.makedirs(batch_directory, exist_ok=True)
print(f"Batch directory created: {batch_directory}")

# Total number of runs
run_count = 5
run_unity= 30

#algo 0 = E policy, 1- I-policy, 2=QM

# Configuration for splitting runs
configs = [
    # {"bufferSize": 2, "timeToWait": 2, "roundDuration": 300, "jitterValue": 20, "run_count": 1},
    # {"bufferSize": 10, "timeToWait": 2, "roundDuration": 300, "jitterValue": 40, "run_count": 1},
    # {"bufferSize": 2, "timeToWait": 2, "roundDuration": 300, "jitterValue": 0, "run_count": run_count, "algo": 0},
    # {"bufferSize": 2, "timeToWait": 2, "roundDuration": 300, "jitterValue": 20, "run_count": run_count, "algo": 0},
    # {"bufferSize": 2, "timeToWait": 2, "roundDuration": 300, "jitterValue": 20, "run_count": run_count, "algo": 2},
    # {"bufferSize": 2, "timeToWait": 2, "roundDuration": 300, "jitterValue": 40, "run_count": run_count,"algo": 0},
    # {"bufferSize": 10, "timeToWait": 2, "roundDuration": 300, "jitterValue": 20, "run_count": run_count,"algo": 0},
    {"bufferSize": 10, "timeToWait": 2, "roundDuration": 300, "jitterValue": 20, "run_count": run_count, "algo": 2},
    # {"bufferSize": 10, "timeToWait": 2, "roundDuration": 300, "jitterValue": 40, "run_count": run_count,"algo": 2},
    {"bufferSize": 10, "timeToWait": 2, "roundDuration": 300, "jitterValue": 0, "run_count": run_count,"algo": 0},
    {"bufferSize": 10, "timeToWait": 2, "roundDuration": 300, "jitterValue": 0, "run_count": run_count, "algo": 2},
    # {"bufferSize": 5, "timeToWait": 2, "roundDuration": 300, "jitterValue": 20, "run_count": run_count,"algo": 0},
    # {"bufferSize": 5, "timeToWait": 2, "roundDuration": 300, "jitterValue": 0, "run_count": run_count,"algo": 0},
    # {"bufferSize": 5, "timeToWait": 2, "roundDuration": 300, "jitterValue": 40, "run_count": run_count,"algo": 2},
    # {"bufferSize": 1, "timeToWait": 2, "roundDuration": 300, "jitterValue": 40, "run_count": run_count,"algo": 2},
    # {"bufferSize": 1, "timeToWait": 2, "roundDuration": 300, "jitterValue": 20, "run_count": run_count,"algo": 2},
    # {"bufferSize": 1, "timeToWait": 2, "roundDuration": 300, "jitterValue": 0, "run_count": run_count,"algo": 2},
    {"bufferSize": 0, "timeToWait": 2, "roundDuration": 300, "jitterValue": 20, "run_count": run_count,"algo": 0},
    {"bufferSize": 0, "timeToWait": 2, "roundDuration": 300, "jitterValue": 20, "run_count": run_count, "algo": 2},
    {"bufferSize": 0, "timeToWait": 2, "roundDuration": 300, "jitterValue": 0, "run_count": run_count,"algo": 2},
    # {"bufferSize": 0, "timeToWait": 2, "roundDuration": 300, "jitterValue": 20, "run_count": run_count,"algo": 2},
]

log_file_path = os.path.join(batch_directory, "script_summary.csv")
# Initialize CSV logging
with open(log_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([
        "Run Number", "Run Start Time", "Run End Time", "Jitter.py Run Duration (s)", "Unity,exe Run Duration (s)","Server Restart Duration (s)",
        "Total Script Run Duration (s)",
        "Unity.exe Stop Duration (s)", "Buffer Size", "Jitter Magnitude"
    ])

# Function to log messages to the CSV file
def log_to_csv(run_number, start_time, end_time, jitter_duration, unity_run_duration,server_duration, total_duration, stop_time, buffer_size, jitter_magnitude):
    with open(log_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            run_number, start_time, end_time, jitter_duration, unity_run_duration,server_duration, total_duration,
            stop_time, buffer_size, jitter_magnitude
        ])

def update_config_file(buffer_size, time_to_wait, round_duration, jitter_value):
    """
    Update the config.csv file with the given parameters.
    """
    data = {
        "param": ["bufferSize", "timeToWait", "roundDuration", "jitterValue"],
        "value": [buffer_size, time_to_wait, round_duration, jitter_value],
    }
    df = pd.DataFrame(data)
    df.to_csv(config_file, index=False)
    print(f"Updated config file: bufferSize={buffer_size}, timeToWait={time_to_wait}, roundDuration={round_duration}, jitterValue={jitter_value}")

def stop_unity_client():
    """
    Close UnityClient.exe using Alt+F4 or force terminate if necessary.
    """
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'UnityClient.exe':
            print("Attempting to close UnityClient.exe with Alt+F4...")
            pyautogui.hotkey("alt", "f4")
            time.sleep(1)
            if proc.is_running():
                proc.terminate()
                print("Forcefully terminated UnityClient.exe as it was still running.")

def run_batch(runs, buffer_size, time_to_wait, round_duration, jitter_value):
    """
    Run a batch of Unity clients with the given parameters.
    """
    start_runbatch = time.time()
    update_config_file(buffer_size, time_to_wait, round_duration, jitter_value)

    for i in range(runs):
        print(f"Starting UnityClient.exe (Run {i + 1}/{runs})")

        # Log start time
        start_time = datetime.now()

        server_start = time.time()
        # Start server log script with the run index
        s_clean = subprocess.Popen([python_path, server_script])
        s_clean.wait()

        server_end = time.time()
        server_duration =  server_end - server_start

        jitter_duration = 0  # Initialize jitter_duration to 0 in case jitter is not applied
        jitter_start = time.time()
        if jitter_value != 0:

            s_clean = subprocess.Popen([python_path, jitter_script, str(jitter_value)])

        else:
            s_clean = subprocess.Popen([python_path, stop_jitter_script])

        s_clean.wait()
        jitter_end = time.time()
        jitter_duration = jitter_end - jitter_start

        # Launch UnityClient.exe
        process = subprocess.Popen(unity_path)

        # Run Unity for the set duration
        time.sleep(run_unity)

        # Close Unity client
        stop_start = time.time()
        stop_unity_client()
        end_runbatch = time.time()
        stop_end = time.time()
        stop_duration = stop_end - stop_start

        s_clean = subprocess.Popen([python_path, log_from_server_script, str(i + 1), batch_directory])
        s_clean.wait()
        # Log end time
        end_time = datetime.now()
        print(start_time.strftime('%Y-%m-%d %H:%M:%S'))

        # Log details to the CSV file
        log_to_csv(
            run_number=i + 1,
            start_time=f"'{start_time.strftime('%Y-%m-%d %H:%M:%S')}",
            end_time=f"'{end_time.strftime('%Y-%m-%d %H:%M:%S')}",
            jitter_duration=round(jitter_duration, 2),
            unity_run_duration= run_unity,
            server_duration= server_duration,
            total_duration= end_runbatch - start_runbatch,
            stop_time=round(stop_duration, 2),
            buffer_size=buffer_size,
            jitter_magnitude=jitter_value,
        )

        print(f"Run {i + 1}/{runs} logged successfully.")

# Execute batches based on the configurations
for config in configs:
    run_batch(
        runs=config["run_count"],
        buffer_size=config["bufferSize"],
        time_to_wait=config["timeToWait"],
        round_duration=config["roundDuration"],
        jitter_value=config["jitterValue"],
    )
print("All runs completed. Logs saved to", log_file_path)
