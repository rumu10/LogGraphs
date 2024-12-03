import requests


def restart_server():
    try:
        # Replace with your Node.js server's URL
        url = "http://130.215.30.198:7777/restart"  # Update with your server's actual URL
        response = requests.post(url, json={"message": "Restart requested"})

        if response.status_code == 200:
            print(response.text)
            print("Server restart message sent successfully!")
        else:
            print(f"Failed to restart server. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Error occurred while restarting the server: {e}")


if __name__ == "__main__":
    restart_server()
