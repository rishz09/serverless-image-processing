import os
import subprocess
import uuid
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time
import streamlit as st

# ---- Configuration ----
# Define the target VM IP address for processing.
VM1_IP = "192.168.56.101"  # Set to your active VM's IP
VM2_IP = "192.168.56.103"
# For now, support only the sketch endpoint.
ENDPOINTS = {
    "sketch": "/sketch",
    "bg_remove": "/remove_bg",
    "caption": "/caption"
}

# Folders to store the temporarily saved input images and processed outputs.
INPUT_FOLDER = "uploaded"
PROCESSED_FOLDER = "processed"

# Create folders if they do not exist.
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def process_uploaded_images_sketch(operation, uploaded_files):
    """
    Processes a list of uploaded image files using the specified operation in parallel.

    For now, only the "sketch" operation is supported.

    Parameters:
        operation (str): Should be "sketch".
        uploaded_files (list): A list of file-like objects (from st.file_uploader).

    Returns:
        List[str]: A list of file paths for the processed (sketched) images.
    """
    processed_paths = []
    dict={
        "VM1":0,
        "VM2":0,
        "GCP":0
    }

    def process_file(file):
        # Generate a unique filename using the original file extension.
        ext = os.path.splitext(file.name)[1]  # includes the dot
        unique_filename = f"{uuid.uuid4()}{ext}"

        # Save the uploaded file into INPUT_FOLDER.
        input_path = os.path.join(INPUT_FOLDER, unique_filename)
        with open(input_path, "wb") as f:
            f.write(file.read())

        # Define the output path.
        output_path = os.path.join(PROCESSED_FOLDER, unique_filename)

        # Read the choice from choice.txt (defaulting to GCP if any error occurs).
        choice_value = "GCP"
        try:
            with open("choice.txt", "r") as f:
                choice_value = f.read().strip()
        except Exception as e:
            print(f"Unable to read choice.txt: {e}")
            choice_value = "GCP"

        # Determine the target URL based on the choice.
        if choice_value == "VM1":
            url = f"http://{VM1_IP}:8080/sketch"
        elif choice_value == "VM2":
            url = f"http://{VM2_IP}:8080/sketch"
        else:
            # When choice_value is "GCP" (or anything else), use the GCP endpoint.
            url = "https://sketch-app-706743001441.asia-south1.run.app/sketch"
        print(f'Using {choice_value} at {url} for the image {input_path}')
        dict[choice_value]+=1
        # Build the curl command.
        command = [
            "curl", "-s", "-X", "POST",
            url,
            "-F", f"image=@{input_path}",
            "--output", output_path
        ]

        # Execute the curl command.
        subprocess.run(command)
        return output_path

    # Create a ThreadPoolExecutor to process files concurrently.
    with ThreadPoolExecutor(max_workers=len(uploaded_files)) as executor:
        future_to_file = {}
        # Submit each task with a 0.25-second delay between submissions.
        for file in uploaded_files:
            future = executor.submit(process_file, file)
            future_to_file[future] = file
            time.sleep(0.8)  # Delay between task submissions

        # Collect results as they complete.
        for future in as_completed(future_to_file):
            try:
                path = future.result()
                processed_paths.append(path)
            except Exception as e:
                print(f"Error processing file: {e}")
    for key, value in dict.items():
        st.write(f"{key}: {value}")
    return processed_paths

def process_uploaded_images_bg_remove(operation, uploaded_files):
    """
    Processes a list of uploaded image files using the specified operation.
    
    For now, only the "sketch" operation is supported.
    
    Parameters:
        operation (str): Should be "sketch".
        uploaded_files (list): A list of file-like objects (from st.file_uploader).
    
    Returns:
        List[str]: A list of file paths for the processed (sketched) images.
    
    The function:
      - Saves each uploaded image to disk with a unique name in INPUT_FOLDER.
      - Constructs the target URL based on the value in "choice.txt".
      - Executes a curl command (via subprocess.run) to perform image processing.
      - Writes the processed output to PROCESSED_FOLDER with the same unique filename.
    """
    import os
    import uuid
    import subprocess
    import time
    from concurrent.futures import ThreadPoolExecutor, as_completed
    dict={
        "VM1":0,
        "VM2":0,
        "GCP":0
    }
    processed_paths = []

    def process_file(file):
        # Generate a unique filename using the original file extension.
        ext = os.path.splitext(file.name)[1]  # includes the dot
        unique_filename = f"{uuid.uuid4()}{ext}"

        # Save the uploaded file into INPUT_FOLDER.
        input_path = os.path.join(INPUT_FOLDER, unique_filename)
        with open(input_path, "wb") as f:
            f.write(file.read())

        # Define the output path.
        output_path = os.path.join(PROCESSED_FOLDER, unique_filename)

        # Read the choice from "choice.txt" (defaulting to GCP on error).
        choice_value = "GCP"
        try:
            with open("choice.txt", "r") as f:
                choice_value = f.read().strip()
        except Exception as e:
            print(f"Unable to read choice.txt: {e}")
            choice_value = "GCP"
        dict[choice_value]+=1
        # Build the target URL based on the choice.
        if choice_value == "GCP":
            url = "https://remove-bg-706743001441.asia-south1.run.app/remove_bg"
        elif choice_value == "VM1":
            target_ip = VM1_IP
            url = f"http://{target_ip}:8082/remove_bg"
        elif choice_value == "VM2":
            target_ip = VM2_IP
            url = f"http://{target_ip}:8082/remove_bg"
        else:
            url = "https://remove-bg-706743001441.asia-south1.run.app/remove_bg"
        print(f'Using {choice_value} at {url} for the image {input_path}')
        # Build and execute the curl command.
        command = [
            "curl", "-s", "-X", "POST",
            url,
            "-F", f"image=@{input_path}",
            "--output", output_path
        ]
        subprocess.run(command)
        return output_path

    # Use ThreadPoolExecutor and delay task submissions by 0.4 seconds.
    futures = []
    with ThreadPoolExecutor(max_workers=len(uploaded_files)) as executor:
        for file in uploaded_files:
            futures.append(executor.submit(process_file, file))
            time.sleep(0.8)  # Delay between task submissions

        # Collect results as tasks complete.
        for future in as_completed(futures):
            try:
                result = future.result()
                processed_paths.append(result)
            except Exception as e:
                print(f"Error processing file: {e}")
    for key, value in dict.items():
        st.write(f"{key}: {value}")
    return processed_paths


def process_uploaded_images_caption(operation, uploaded_files):
    """
    Processes a list of uploaded image files using the "caption" operation concurrently.

    Parameters:
        operation (str): Should be "caption".
        uploaded_files (list): A list of file-like objects (from st.file_uploader).

    Returns:
        List[tuple]: A list of tuples of the form (input_image_path, caption).

    The function:
      - Saves each uploaded image to disk with a unique name in INPUT_FOLDER.
      - Determines the target endpoint based on the content of "choice.txt":
            If "GCP": uses the GCP Flask API endpoint.
            If "VM1"/"VM2": uses the corresponding virtual machine endpoint.
      - Executes a curl command (via subprocess.run) to perform the image captioning.
      - Parses the JSON response and returns, for each image, its file path together with the generated caption.
    """
    processed_results = []
    dict={
        "VM1":0,
        "VM2":0,
        "GCP":0
    }
    def process_file(file):
        # Generate a unique filename.
        ext = os.path.splitext(file.name)[1]  # includes the dot
        unique_filename = f"{uuid.uuid4()}{ext}"

        # Save the uploaded file into INPUT_FOLDER.
        input_path = os.path.join(INPUT_FOLDER, unique_filename)
        with open(input_path, "wb") as f:
            f.write(file.read())

        # Determine the desired endpoint from choice.txt (default to "GCP").
        choice_value = "GCP"
        try:
            with open("choice.txt", "r") as f:
                choice_value = f.read().strip()
        except Exception as e:
            print(f"Unable to read choice.txt: {e}")
            choice_value = "GCP"
        dict[choice_value]+=1
        # Select the target URL based on the choice.
        if choice_value == "GCP":
            url = "https://caption-service-706743001441.asia-south1.run.app/caption"
        elif choice_value == "VM1":
            target_ip = VM1_IP
            url = f"http://{target_ip}:8081/caption"
        elif choice_value == "VM2":
            target_ip = VM2_IP
            url = f"http://{target_ip}:8081/caption"
        else:
            # Fallback in case an unexpected choice value is found.
            url = "https://caption-service-706743001441.asia-south1.run.app/caption"

        # Build the curl command.
        print(f'Using {choice_value} at {url} for the image {input_path}')
        command = [
            "curl.exe", "-s", "-X", "POST",
            url,
            "-F", f"image=@{input_path}"
        ]

        # Execute the curl command and capture the output.
        output = subprocess.run(command, capture_output=True, text=True)
        try:
            # Parse the JSON response to extract the caption.
            response = json.loads(output.stdout)["caption"]
        except Exception as e:
            response = f"Error generating caption: {e}"
        return (input_path, response)

    # Use ThreadPoolExecutor to process each file concurrently.
    processed_results = []
    futures = []

    with ThreadPoolExecutor(max_workers=len(uploaded_files)) as executor:
        # Submit each task with a delay between submissions.
        for file in uploaded_files:
            futures.append(executor.submit(process_file, file))
            time.sleep(0.8)  # Delay between task submissions

        # Optionally, process the futures as they complete.
        for future in as_completed(futures):
            try:
                result = future.result()
                processed_results.append(result)
            except Exception as e:
                print(f"Error processing file: {e}")
    for key, value in dict.items():
        st.write(f"{key}: {value}")
    return processed_results

if __name__ == "__main__":
    # For isolated testing, uncomment the code below.
    # with open("input_images/example.jpg", "rb") as test_file:
    #     fake_uploaded_files = [test_file]
    # processed = process_uploaded_images("sketch", fake_uploaded_files)
    # print("Processed files:", processed)
    pass
