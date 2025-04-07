import paramiko
import time

hostname = "130.215.30.228"
username = "claypool"  # Adjust if necessary
password = "1012"  # Use an empty string if no password
remote_script_path = "C:/Users/claypool/Desktop/rumu/GitHub/LogGraphs/startAndStopServer.py"
python_path = "C:/Users/claypool/AppData/Local/Programs/Python/Python313/python.exe"  # Adjust path to Python
timeout = 4  # Timeout in seconds

try:
    print("Connecting to the server...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port=22, username=username, password=password)
    print("Connected successfully!")

    # Execute the remote script
    print(f"Executing script: {remote_script_path}")
    command = f'"{python_path}" {remote_script_path}'
    stdin, stdout, stderr = ssh.exec_command(command)

    # Monitor the output and wait for a specific signal or timeout
    start_time = time.time()
    while True:
        if stdout.channel.recv_ready():  # Check if there is any output
            output = stdout.read().decode('utf-8', errors='replace')
            print("Script output:")
            # print(output)
            if "Page reloaded." in output:  # Example: signal from Selenium
                print("Detected successful execution. Stopping script...")
                break

        if time.time() - start_time > timeout:  # Timeout
            print("Timeout reached. Stopping the script.")
            break

        time.sleep(.5)  # Avoid busy-waiting

    # Print errors if any
    if stderr.channel.recv_ready():
        errors = stderr.read().decode('utf-8', errors='replace')
        print("Script errors:")
        # print(errors)

    # Close the streams and SSH connection
    stdin.close()
    stdout.close()
    stderr.close()
    ssh.close()
    print("Disconnected from the server.")
except Exception as e:
    print(f"An error occurred: {e}")
