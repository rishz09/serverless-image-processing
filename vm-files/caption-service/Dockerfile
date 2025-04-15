# Use official Python image
FROM python:3.10-slim

# Install OS dependencies
RUN apt-get update && apt-get install -y git

# Set working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Run the app
CMD ["python", "app.py"]
