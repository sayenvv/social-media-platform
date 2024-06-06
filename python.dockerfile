# Use a minimal Python 3.11 image as the base image
FROM python:3.11-slim AS builder

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Create a virtual environment and activate it
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install dependencies within the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code (assuming it's in the same directory as the Dockerfile)
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the virtual environment from the builder stage to the container
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy the application code from the builder stage to the container
COPY . /app

# Expose the port on which the application will run
EXPOSE 8000

# Define the command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
