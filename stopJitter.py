import paramiko
import time

ssh = paramiko.SSHClient()
key = paramiko.AutoAddPolicy()
ssh.set_missing_host_key_policy(key)
ssh.connect('192.168.1.1',22,'ubuntu', 'wpipassword',timeout=5)

ssh.exec_command('sudo tc qdisc del dev eth0 root')
# time.sleep(0.5)
# ssh.exec_command('sudo tc qdisc add dev eth0 root netem delay 0.1ms 20ms distribution f750 rate 1000mbit')
ssh.close()
print(f"Jitter stopped.")