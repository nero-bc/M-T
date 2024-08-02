# Base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt .

# Install the dependencies with the latest versions
RUN pip3 install --upgrade -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["python3", "main.py"]
