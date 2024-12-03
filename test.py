import subprocess
import time
import psutil
import pyautogui
import csv
from datetime import datetime

# Path configurations
unity_path = r"C:\Users\claypool-316\Desktop\Rumu\Build\UnityClient.exe"
python_path = r"C:\Users\claypool-316\Desktop\Rumu\pythonProject\.venv\Scripts\python"
jitter_script = "jitter.py"
log_file_path = "run_logs.csv"

# Number of runs and duration
run_count = 50
run_duration = 30  # seconds

# Initialize CSV logging
with open(log_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Run Number", "Start Time", "End Time", "Jitter Duration (s)", "Run Duration (s)", "Stop Time (s)"])

# Function to log messages to the CSV file
def log_to_csv(run_number, start_time, end_time, jitter_duration, run_duration, stop_time):
    with open(log_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([run_number, start_time, end_time, jitter_duration, run_duration, stop_time])

for i in range(run_count):
    print(f"Starting UnityClient.exe (Run {i + 1}/{run_count})")

    # Log start time
    start_time = datetime.now()

    # Start Raspberry Pi jitter script
    jitter_start = time.time()
    s_clean = subprocess.Popen([python_path, jitter_script])
    s_clean.wait()
    jitter_end = time.time()
    jitter_duration = jitter_end - jitter_start

    # Launch UnityClient.exe
    process = subprocess.Popen(unity_path)

    # Run Unity for the set duration
    time.sleep(run_duration)

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
        run_duration=run_duration,
        stop_time=round(stop_duration, 2),
    )

    print(f"Run {i + 1}/{run_count} logged successfully.")

print("All runs completed. Logs saved to", log_file_path)
