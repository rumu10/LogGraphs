import subprocess
import time
import os

# Configurable variables
pm2_app_name = "phaser"
pm2_path = "C:/Users/claypool/AppData/Roaming/npm/pm2.cmd"
python_path = r"C:/Users/claypool/AppData/Local/Programs/Python/Python313/python.exe"
browser_script = "C:/Users/claypool/Desktop/rumu/GitHub/LogGraphs/reloadBrowser.py"



import subprocess

def stop_server():
    print("Stopping the server...")
    try:
        # Update this command as needed
        subprocess.run([pm2_path, "stop", pm2_app_name], check=True)
        print("Server stopped successfully.")
    except Exception as e:
        print(f"An error occurred while stopping the server: {e}")

def start_server():
    print("Starting the server...")
    try:
        # Update this command as needed
        subprocess.run([pm2_path, "start", pm2_app_name], check=True)
        print("Server started successfully.")
    except Exception as e:
        print(f"An error occurred while starting the server: {e}")

if __name__ == "__main__":
    stop_server()
    time.sleep(0.5)
    # s_clean = subprocess.Popen([python_path, browser_script])
    # s_clean.wait()

    start_server()
    time.sleep(0.5)
    s_clean = subprocess.Popen([python_path, browser_script])
    s_clean.wait()
    print("done")


