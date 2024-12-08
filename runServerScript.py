import paramiko

hostname = "130.215.30.198"
username = "sudipta"  # Adjust if necessary
password = "1012"  # Use an empty string if no password
remote_script_path = "C:/Users/Sudipta/Documents/GitHub/LogGraphs/restartAndReload.py"
python_path = "C:/Users/Sudipta/AppData/Local/Programs/Python/Python313/python.exe"  # Adjust path to Python

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

    # Print script output
    print("Script output:")
    print(stdout.read().decode())

    # Print script errors
    print("Script errors:")
    print(stderr.read().decode())

    ssh.close()
    print("Disconnected from the server.")
except Exception as e:
    print(f"An error occurred: {e}")
