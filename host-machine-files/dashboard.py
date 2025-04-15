import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
import os
from datetime import datetime
from scipy.interpolate import make_interp_spline

# Set Streamlit page configuration
st.set_page_config(page_title="VM Load Monitor Dashboard", layout="centered")

st.title("📊 Real-Time VM Load Monitor Dashboard")
st.markdown("""
This dashboard displays **live CPU and RAM usage** for two Virtual Machines (VMs).  
Data is read from files:
- **VM1 CPU:** `./vm_usage/vm1/cpu.txt`
- **VM1 RAM:** `./vm_usage/vm1/ram.txt`
- **VM2 CPU:** `./vm_usage/vm2/cpu.txt`
- **VM2 RAM:** `./vm_usage/vm2/ram.txt`

Each file contains comma-separated float values representing the latest usage readings.
""")
st.markdown("<hr style='margin-top: 1px; margin-bottom: 40px;'>", unsafe_allow_html=True)

def read_values(file_path):
    """
    Reads comma-separated float values from a file and returns them as a list.
    If the file does not exist or is empty, returns an empty list.
    """
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            # Convert comma-separated values into a list of floats.
            return [float(val.strip()) for val in content.split(",") if val.strip()]
    except Exception as e:
        st.error(f"Error reading {file_path}: {e}")
        return []

def smooth_line(x, y):
    """
    Returns a smoothed version of the line using spline interpolation.
    If there are fewer than 4 points, no smoothing is applied.
    """
    if len(x) < 4:
        return x, y
    x_smooth = np.linspace(x.min(), x.max(), 300)
    spline = make_interp_spline(x, y, k=3)
    y_smooth = spline(x_smooth)
    return x_smooth, y_smooth

# Define file paths for each metric.
vm_files = {
    "VM1_CPU": "./vm_usage/vm1/cpu.txt",
    "VM1_RAM": "./vm_usage/vm1/ram.txt",
    "VM2_CPU": "./vm_usage/vm2/cpu.txt",
    "VM2_RAM": "./vm_usage/vm2/ram.txt"
}

# Create column containers for layout: left for VM1, right for VM2.
col_left, col_right = st.columns(2)

# Create placeholders for each graph.
ph_vm1_cpu = col_left.empty()   # Top left: VM1 CPU
ph_vm1_ram = col_left.empty()   # Bottom left: VM1 RAM
ph_vm2_cpu = col_right.empty()  # Top right: VM2 CPU
ph_vm2_ram = col_right.empty()  # Bottom right: VM2 RAM

# Main loop to update the dashboard continuously.
while True:
    # Read current values from each file.
    vm1_cpu = read_values(vm_files["VM1_CPU"])
    vm1_ram = read_values(vm_files["VM1_RAM"])
    vm2_cpu = read_values(vm_files["VM2_CPU"])
    vm2_ram = read_values(vm_files["VM2_RAM"])
    
    # Create indices for x-axis based on the length of each data series.
    x_vm1_cpu = np.arange(len(vm1_cpu))
    x_vm1_ram = np.arange(len(vm1_ram))
    x_vm2_cpu = np.arange(len(vm2_cpu))
    x_vm2_ram = np.arange(len(vm2_ram))
    
    # Apply smoothing if there are enough points (at least 4).
    if len(vm1_cpu) >= 4:
        x_vm1_cpu_s, y_vm1_cpu_s = smooth_line(x_vm1_cpu, np.array(vm1_cpu))
    else:
        x_vm1_cpu_s, y_vm1_cpu_s = x_vm1_cpu, vm1_cpu

    if len(vm1_ram) >= 4:
        x_vm1_ram_s, y_vm1_ram_s = smooth_line(x_vm1_ram, np.array(vm1_ram))
    else:
        x_vm1_ram_s, y_vm1_ram_s = x_vm1_ram, vm1_ram

    if len(vm2_cpu) >= 4:
        x_vm2_cpu_s, y_vm2_cpu_s = smooth_line(x_vm2_cpu, np.array(vm2_cpu))
    else:
        x_vm2_cpu_s, y_vm2_cpu_s = x_vm2_cpu, vm2_cpu

    if len(vm2_ram) >= 4:
        x_vm2_ram_s, y_vm2_ram_s = smooth_line(x_vm2_ram, np.array(vm2_ram))
    else:
        x_vm2_ram_s, y_vm2_ram_s = x_vm2_ram, vm2_ram

    # Update VM1 CPU graph and latest value.
    with ph_vm1_cpu.container():
        fig1, ax1 = plt.subplots(figsize=(5, 3))
        if len(x_vm1_cpu_s) > 0:
            ax1.plot(x_vm1_cpu_s, y_vm1_cpu_s, label="VM1 CPU", color='royalblue')
        ax1.set_title("VM1 CPU Usage")
        ax1.set_ylabel("CPU (%)")
        ax1.set_ylim(0, 100)
        ax1.grid(True)
        st.pyplot(fig1)
        if vm1_cpu:
            st.markdown(f"<p style='text-align: center; font-size: 16px;'><strong>Latest: {vm1_cpu[-1]:.2f}%</strong></p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='text-align: center; font-size: 16px;'><strong>Latest: No data</strong></p>", unsafe_allow_html=True)

    # Update VM1 RAM graph and latest value.
    with ph_vm1_ram.container():
        fig2, ax2 = plt.subplots(figsize=(5, 3))
        if len(x_vm1_ram_s) > 0:
            ax2.plot(x_vm1_ram_s, y_vm1_ram_s, label="VM1 RAM", color='tomato')
        ax2.set_title("VM1 RAM Usage")
        ax2.set_ylabel("RAM (%)")
        ax2.set_ylim(0, 100)
        ax2.grid(True)
        st.pyplot(fig2)
        if vm1_ram:
            st.markdown(f"<p style='text-align: center; font-size: 16px;'><strong>Latest: {vm1_ram[-1]:.2f}%</strong></p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='text-align: center; font-size: 16px;'><strong>Latest: No data</strong></p>", unsafe_allow_html=True)

    # Update VM2 CPU graph and latest value.
    with ph_vm2_cpu.container():
        fig3, ax3 = plt.subplots(figsize=(5, 3))
        if len(x_vm2_cpu_s) > 0:
            ax3.plot(x_vm2_cpu_s, y_vm2_cpu_s, label="VM2 CPU", color='seagreen')
        ax3.set_title("VM2 CPU Usage")
        ax3.set_ylabel("CPU (%)")
        ax3.set_ylim(0, 100)
        ax3.grid(True)
        st.pyplot(fig3)
        if vm2_cpu:
            st.markdown(f"<p style='text-align: center; font-size: 16px;'><strong>Latest: {vm2_cpu[-1]:.2f}%</strong></p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='text-align: center; font-size: 16px;'><strong>Latest: No data</strong></p>", unsafe_allow_html=True)

    # Update VM2 RAM graph and latest value.
    with ph_vm2_ram.container():
        fig4, ax4 = plt.subplots(figsize=(5, 3))
        if len(x_vm2_ram_s) > 0:
            ax4.plot(x_vm2_ram_s, y_vm2_ram_s, label="VM2 RAM", color='mediumvioletred')
        ax4.set_title("VM2 RAM Usage")
        ax4.set_ylabel("RAM (%)")
        ax4.set_xlabel("Data Points")
        ax4.set_ylim(0, 100)
        ax4.grid(True)
        st.pyplot(fig4)
        if vm2_ram:
            st.markdown(f"<p style='text-align: center; font-size: 16px;'><strong>Latest: {vm2_ram[-1]:.2f}%</strong></p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='text-align: center; font-size: 16px;'><strong>Latest: No data</strong></p>", unsafe_allow_html=True)

    # Pause briefly before the next update.
    time.sleep(0.2)
