import socket
import json
import threading
import time
import os

# Global lock for synchronizing file writes
log_lock = threading.Lock()

def process_usage_list(usages):
    """
    Accepts either:
      - a Python list of dicts, e.g. [{"id": "1", "cpu": 10, "ram": 20}, ...]
      - a JSON string representing such a list.
    
    Each dict must have 'id', 'cpu', and 'ram' keys.
    Writes to individual files:
      - "./vm_usage/vm1.txt" for VM1 (id '1')
      - "./vm_usage/vm2.txt" for VM2 (id '2')
    
    Each file will contain only the last 5 CPU usage values, comma separated.
    Additionally, the usage is appended to logs.txt as <ID>_<CPU>_<RAM>
    """
    # Decode JSON string if necessary.
    if isinstance(usages, str):
        try:
            usage_list = json.loads(usages)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON string passed to process_usage_list") from e
    else:
        usage_list = usages

    if not isinstance(usage_list, list):
        raise ValueError("process_usage_list expects a list of usage dicts")

    for usage in usage_list:
        identifier = usage.get('id')
        cpu = usage.get('cpu')
        ram = usage.get('ram')
        
        # Determine target file based on identifier.
        if str(identifier) == '1':
            target_file_cpu = "./vm_usage/vm1/cpu.txt"
            target_file_ram = "./vm_usage/vm1/ram.txt"
            
        elif str(identifier) == '2':
            target_file_cpu = "./vm_usage/vm2/cpu.txt"
            target_file_ram = "./vm_usage/vm2/ram.txt"
            
        else:
            print(f"Unknown VM identifier: {identifier}")
            continue
        
        # Ensure the directory exists
        if not os.path.exists("./vm_usage"):
            os.makedirs("./vm_usage")
        
        # Use the lock to ensure thread safety during file operations.
        with log_lock:
            # Read the current content from the file (if any)
            current_values = []
            if os.path.exists(target_file_cpu):
                with open(target_file_cpu, "r") as f:
                    content = f.read().strip()
                    if content:
                        try:
                            current_values = [float(val) for val in content.split(',') if val]
                        except Exception as e:
                            print(f"Error parsing values from {target_file_cpu}: {e}")
                            current_values = []
            
            # Append the new CPU value.
            current_values.append(float(cpu))
            # Keep only the last 5 CPU values.
            if len(current_values) > 5:
                current_values = current_values[-5:]
            
            # Write the updated CPU values back to the file, comma separated.
            with open(target_file_cpu, "w") as f:
                f.write(",".join(str(val) for val in current_values))
                
        with log_lock:
            # Read the current content from the file (if any)
            current_values = []
            if os.path.exists(target_file_ram):
                with open(target_file_ram, "r") as f:
                    content = f.read().strip()
                    if content:
                        try:
                            current_values = [float(val) for val in content.split(',') if val]
                        except Exception as e:
                            print(f"Error parsing values from {target_file_ram}: {e}")
                            current_values = []
            
            # Append the new CPU value.
            current_values.append(float(ram))
            # Keep only the last 5 CPU values.
            if len(current_values) > 5:
                current_values = current_values[-5:]
            
            # Write the updated CPU values back to the file, comma separated.
            with open(target_file_ram, "w") as f:
                f.write(",".join(str(val) for val in current_values))
        
        print(f"ID: {identifier} | CPU: {cpu}% | RAM: {ram}%")
        # Also log the raw usage.
        log_line = f"{identifier}_{cpu}_{ram}\n"
        with log_lock:
            with open("logs.txt", "a") as log_file:
                log_file.write(log_line)

def handle_client(conn, addr):
    """
    Handles communication with a connected client.
    Receives newline-terminated JSON messages and passes parsed usage data to process_usage_list.
    """
    print(f"[✓] Connected by {addr}")
    try:
        with conn.makefile('r') as sockfile:
            for raw_line in sockfile:
                line = raw_line.strip()
                if not line:
                    continue

                try:
                    raw_list = json.loads(line)
                except json.JSONDecodeError:
                    print("[!] Invalid JSON:", line)
                    continue

                if not isinstance(raw_list, list) or len(raw_list) != 3:
                    print(f"[!] Unexpected format: {raw_list}")
                    continue

                try:
                    identifier, cpu_val, ram_val = raw_list
                    usage_list = [{
                        "id": identifier,
                        "cpu": float(cpu_val),
                        "ram": float(ram_val)
                    }]
                except Exception as e:
                    print(f"[!] Failed to parse {raw_list}: {e}")
                    continue

                process_usage_list(usage_list)
    except Exception as e:
        print(f"[!] Error handling client {addr}: {e}")
    finally:
        conn.close()

def accept_connections(server_socket):
    """
    Loops on accept() and spawns a new thread to handle each incoming client.
    """
    while True:
        try:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.daemon = True
            client_thread.start()
        except Exception as e:
            print(f"[!] Exception in accept_connections: {e}")
            break

def main():
    HOST = '0.0.0.0'
    PORT_VM1 = 9876  # Dedicated port for VM1
    PORT_VM2 = 9877  # Dedicated port for VM2

    # Create server socket for VM1.
    server_socket_vm1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_vm1.bind((HOST, PORT_VM1))
    server_socket_vm1.listen()
    print(f"[✓] Listening for VM1 on {HOST}:{PORT_VM1}…")

    # Create server socket for VM2.
    server_socket_vm2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_vm2.bind((HOST, PORT_VM2))
    server_socket_vm2.listen()
    print(f"[✓] Listening for VM2 on {HOST}:{PORT_VM2}…")

    # Start a thread to accept connections on VM1's socket.
    t1 = threading.Thread(target=accept_connections, args=(server_socket_vm1,))
    t1.daemon = True
    t1.start()
    print(f"[✓] Accept thread for VM1 started.")

    # Start a thread to accept connections on VM2's socket.
    t2 = threading.Thread(target=accept_connections, args=(server_socket_vm2,))
    t2.daemon = True
    t2.start()
    print(f"[✓] Accept thread for VM2 started.")

    # Keep the main thread running.
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[✓] Shutting down servers...")
        server_socket_vm1.close()
        server_socket_vm2.close()

if __name__ == "__main__":
    main()
