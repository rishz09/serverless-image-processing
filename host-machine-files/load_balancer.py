import time

# Mapping from VM ID to its IP address.
vm_ips = {
    "VM1": "192.168.56.101",
    "VM2": "192.168.56.103"
}

# Mapping from VM ID to file path for CPU usage values.
vm_cpu_files = {
    "VM1": "./vm_usage/vm1/cpu.txt",
    "VM2": "./vm_usage/vm2/cpu.txt"
}

def read_cpu_values(file_path):
    """
    Reads comma-separated float values from the specified file.
    Returns a list of float values.
    If the file doesn't exist or an error occurs, returns an empty list.
    """
    try:
        with open(file_path, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            # Split the content by commas and convert each part to a float.
            values = [float(val.strip()) for val in content.split(",") if val.strip()]
            return values
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def compute_average(values):
    """
    Computes the average of a list of numbers.
    Returns 0 if the list is empty.
    """
    if not values:
        return 0.0
    return sum(values) / len(values)

def main():
    print("Load Balancer is running.")
    
    while True:
        
        # Read CPU usage values from each VM's file.
        vm1_values = read_cpu_values(vm_cpu_files["VM1"])
        vm2_values = read_cpu_values(vm_cpu_files["VM2"])
        
        # Get the latest CPU usage value from each VM.
        latest_vm1 = vm1_values[-1] if vm1_values else None
        latest_vm2 = vm2_values[-1] if vm2_values else None
        
        # Compute the running average (of the last 5 values) for each VM.
        avg_vm1 = compute_average(vm1_values)
        avg_vm2 = compute_average(vm2_values)
        
        # print(f"Average CPU -> VM1: {avg_vm1:.2f}%, VM2: {avg_vm2:.2f}%")
        
        # Choose the VM with the lower average CPU usage.
        if avg_vm1 < avg_vm2:
            selected_vm = "VM1"
            selected_avg = avg_vm1
            choice_val=selected_vm
        else:
            selected_vm = "VM2"
            selected_avg = avg_vm2
            choice_val=selected_vm
            
        if selected_avg > 40:
            choice_val = "GCP"
            
        try:
            with open("choice.txt", "w") as f:
                f.write(choice_val)
            # print(f"choice.txt updated with: {choice_val}")
        except Exception as e:
            time.sleep(0.15)
            # print(f"Error writing to choice.txt: {e}")
            
        time.sleep(0.15)
    

if __name__ == "__main__":
    main()
