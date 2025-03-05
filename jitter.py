# import paramiko
# import time
#
# ssh = paramiko.SSHClient()
# key = paramiko.AutoAddPolicy()
# ssh.set_missing_host_key_policy(key)
# ssh.connect('192.168.1.1',22,'ubuntu', 'wpipassword',timeout=5)
#
# ssh.exec_command('sudo tc qdisc del dev eth0 root')
# time.sleep(0.5)
# ssh.exec_command('sudo tc qdisc add dev eth0 root netem delay 0.1ms 20ms distribution f1300 rate 1000mbit')
# ssh.close()

import paramiko
import time
import sys

# Get jitter value from command-line argument
if len(sys.argv) < 2:
    print("Usage: python jitter.py <jitter_value>")
    sys.exit(1)

jitter_value = int(sys.argv[1])
print(f"Running jitter with value: {jitter_value}")

jitter_value = sys.argv[1]  # Get the jitter value (e.g., 20ms)

ssh = paramiko.SSHClient()
key = paramiko.AutoAddPolicy()
ssh.set_missing_host_key_policy(key)
ssh.connect('192.168.1.1', 22, 'ubuntu', 'wpipassword', timeout=5)

ssh.exec_command('sudo tc qdisc del dev eth0 root')
time.sleep(0.5)
ssh.exec_command(f'sudo tc qdisc add dev eth0 root netem delay 50ms {jitter_value}ms distribution f1300 rate 1000mbit')
ssh.close()

print(f"Jitter script executed with delay: {jitter_value}ms")
