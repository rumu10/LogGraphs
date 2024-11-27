import subprocess
import time
import psutil
import pyautogui


# Path to UnityClient.exe
unity_path = r"C:\Users\claypool-316\Desktop\Rumu\Build\UnityClient.exe"

# Number of times to run UnityClient.exe
run_count = 20  # Set your desired number of runs
run_duration = 30

for i in range(run_count):
    print(f"Starting UnityClient.exe (Run {i+1}/{run_count})")

    # Launch UnityClient.exe
    process = subprocess.Popen(unity_path)
    # time.sleep(5)
    s_clean = subprocess.Popen(['python', 'jitter.py'])  # Use 'python3' if required
    # s_clean.wait()
    # Wait for 1 minute (60 seconds)
    time.sleep(run_duration)

    # Try to close UnityClient.exe using Alt+F4, which acts as a natural close request
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'UnityClient.exe':
            print("Attempting to close UnityClient.exe with Alt+F4...")
            pyautogui.hotkey("alt", "f4")

            # Give Unity some time to save data before forcing termination
            time.sleep(6)

            # If still running, forcefully terminate
            if proc.is_running():
                proc.terminate()
                print("Forcefully terminated UnityClient.exe as it was still running.")

    # Wait a bit before restarting, if necessary
    # time.sleep(3)  # Adjust delay as needed
    # s_stop = subprocess.Popen(['python','stopJitter.py'])
    # s_stop.wait()

print("All runs completed.")
