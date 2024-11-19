import subprocess
import time
import psutil
import requests

# Path to UnityClient.exe
unity_path = r"C:\Users\claypool-316\Desktop\Rumu\Build\UnityClient.exe"

# Server restart endpoint
server_restart_url = "http://localhost:7777/restart"

# Number of times to run UnityClient.exe
run_count = 5  # Set your desired number of runs

def restart_server():
    try:
        response = requests.post(server_restart_url)
        if response.status_code == 200:
            print("Server restart signal sent successfully.")
        else:
            print("Failed to send server restart signal.")
    except Exception as e:
        print(f"Error while sending restart signal: {e}")

for i in range(run_count):
    print(f"Starting UnityClient.exe (Run {i+1}/{run_count})")

    # Launch UnityClient.exe
    process = subprocess.Popen(unity_path)

    # Wait for the Unity run to complete (1 minute here)
    time.sleep(60)

    # Close UnityClient.exe using Alt+F4
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'UnityClient.exe':
            print("Attempting to close UnityClient.exe with Alt+F4...")
            proc.terminate()

            # Wait a bit to ensure it shuts down gracefully
            time.sleep(10)

            # Force terminate if still running
            if proc.is_running():
                proc.kill()
                print("Forcefully terminated UnityClient.exe as it was still running.")

    # Send a restart signal to the server
    restart_server()

    # Wait a bit before restarting the next run
    time.sleep(5)

print("All runs completed.")
