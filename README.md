# Serverless Image Processing with Multi-User Concurrency and Distributed Computing

## 📄 Project Overview
This project presents a **scalable image processing system** that leverages a hybrid cloud architecture combining local virtual machines (VMs) and serverless cloud containers. It supports multiple concurrent users via a Streamlit-based frontend and intelligently distributes image processing tasks using a custom load balancer based on real-time CPU utilization metrics.

## 🔧 Features
- Modular microservices for:
  - **Image-to-sketch conversion**
  - **Background removal**
  - **Image caption generation (using Salesforce BLIP)**
- Real-time **CPU and RAM monitoring** of VMs
- Automatic task offloading to **Google Cloud Run** when VM load exceeds a threshold
- REST APIs and socket communication for robust inter-process coordination
- Dynamic **dashboard** for monitoring system health and task status
- Support for **multiple concurrent users and image uploads**

## 🧠 Architecture Summary
- **Frontend:** Streamlit UI for task selection, image upload, and result visualization.
- **Backend:** 
  - Flask APIs for communication between components.
  - A load balancer that chooses between VMs or Google Cloud Run based on current load.
  - Dockerized microservices hosted locally or on GCP.
- **Monitoring:** Real-time metrics shared via `psutil` and socket programming.
- **Cloud Integration:** Auto-scaling containers deployed on Cloud Run.

## 🖥️ System Workflow
1. User selects an operation and uploads images via the Streamlit UI.
2. Task is routed by the load balancer to the most optimal resource (VM or GCP).
3. Image processing is executed and results returned to the frontend.
4. Admin dashboard updates live resource metrics for monitoring.

## 📦 Technologies Used
- Python, Flask, Streamlit
- Google Cloud Run
- Docker
- `psutil`, `socket`, `OpenCV`, `rembg`, `transformers` (for BLIP)

## 📁 Project Structure
- `/frontend/` - Streamlit app (`homepage.py`)
- `/load_balancer/` - Load distribution logic, live metrics management
- `/vm_tasks/` - Flask APIs for image processing services
- `/containers/` - Dockerfiles and deployment configs for GCP
- `/monitoring/` - Admin dashboard and resource logging

## 📌 Prerequisites
- Python 3.8+
- Docker installed and configured
- Google Cloud CLI configured with billing and IAM roles set up
- VirtualBox or another VM environment (if running local VMs)

## 📈 Outputs
- Demonstrated scalability via autoscaling containers
- Live visualization of system resource usage
- Successful processing of complex image tasks (e.g., BLIP captioning) with intelligent load redirection

## 🚀 Future Scope
- Horizontal VM autoscaling using infrastructure-as-code
- ML-based predictive routing in the load balancer
- Support for additional cloud providers (Azure, AWS) to avoid vendor lock-in
- Secure API layer and data encryption for sensitive workloads

## 🙌 Team Contributions
- **Rishabh Acharya:** System design, VM networking, container deployment on GCP.
- **Harshit Goyal:** Socket communication, REST API development, overall orchestration.
- **Pujit Jha:** Load balancer implementation, Docker container creation, frontend UI, documentation.

## 🔗 Repository
[GitHub - Serverless Image Processing](https://github.com/rishz09/serverless-image-processing)

## 📜 License
This project is intended for academic and research purposes only.


# serverless-image-processing

* [Youtube Link](https://youtu.be/ikRHIUXGJwE?si=c-6cQNpvZhma2xzd)
