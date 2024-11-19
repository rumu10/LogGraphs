import subprocess
import time
import psutil
import pyautogui

# Path to UnityClient.exe
unity_path = r"C:\Users\claypool-316\Desktop\Rumu\Build\UnityClient.exe"

# Number of times to run UnityClient.exe
run_count = 3  # Set your desired number of runs

for i in range(run_count):
    print(f"Starting UnityClient.exe (Run {i+1}/{run_count})")

    # Launch UnityClient.exe
    process = subprocess.Popen(unity_path)

    # Wait for 1 minute (60 seconds)
    time.sleep(30)

    # Try to close UnityClient.exe using Alt+F4, which acts as a natural close request
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'UnityClient.exe':
            print("Attempting to close UnityClient.exe with Alt+F4...")
            pyautogui.hotkey("alt", "f4")

            # Give Unity some time to save data before forcing termination
            time.sleep(10)

            # If still running, forcefully terminate
            if proc.is_running():
                proc.terminate()
                print("Forcefully terminated UnityClient.exe as it was still running.")

    # Wait a bit before restarting, if necessary
    time.sleep(1)  # Adjust delay as needed

print("All runs completed.")
