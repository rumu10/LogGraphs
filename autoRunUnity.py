import subprocess
import time
import psutil
import pyautogui

# Path to UnityClient.exe
unity_path = r"C:\Users\claypool-316\Desktop\Rumu\Build\UnityClient.exe"
python_path = r"C:\Users\claypool-316\Desktop\Rumu\pythonProject\.venv\Scripts\python"  # Adjust path to your Python interpreter
restart_script = "restart_server.py"

# Number of times to run UnityClient.exe
run_count = 50
run_duration = 30

for i in range(run_count):
    print(f"Starting UnityClient.exe (Run {i+1}/{run_count})")

    # Start Raspberry Pi jitter script
    s_clean = subprocess.Popen([python_path, 'jitter.py'])
    s_clean.wait()

    # Launch UnityClient.exe
    process = subprocess.Popen(unity_path)

    # Restart the Node.js server
    # print("Restarting the server...")
    # s_restart = subprocess.Popen([python_path, restart_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # stdout, stderr = s_restart.communicate()
    # print(f"Server restart output: {stdout.decode()}")
    # print(f"Server restart errors: {stderr.decode()}")
    # time.sleep(5)  # Wait for the server to stabilize

    # Run Unity for the set duration
    time.sleep(run_duration)

    # Close UnityClient.exe using Alt+F4
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'UnityClient.exe':
            print("Attempting to close UnityClient.exe with Alt+F4...")
            pyautogui.hotkey("alt", "f4")
            time.sleep(6)
            if proc.is_running():
                proc.terminate()
                print("Forcefully terminated UnityClient.exe as it was still running.")

print("All runs completed.")
