import psutil
import socket
import time
import json

HOST = '192.168.56.1'  
PORT = 9877           

while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            while True:
                cpu = psutil.cpu_percent(interval=1)
                ram = psutil.virtual_memory().percent
                data_list=["2", cpu, ram]
                print(data_list)
                s.sendall(json.dumps(data_list).encode() + b'\n')
                time.sleep(0.1)
    except Exception as e:
        print(f"[!] Reconnecting... {e}")
        time.sleep(1)
