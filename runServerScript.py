import requests

server_ip = "130.215.30.198"  # Replace with the server's IP address

# Restart the server
try:
    restart_response = requests.post(f"http://{server_ip}:5000/restart")
    print("Restart response:", restart_response.json())
except Exception as e:
    print(f"Error restarting server: {e}")


