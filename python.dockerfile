# Use a minimal Python 3.11 image as the base image
FROM python:3.11-slim AS builder

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Start with a base image for the build stage
FROM python:3.11-slim AS builder

# Create a virtual environment and activate it
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

# Install dependencies within the virtual environment
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code (assuming it's in the same directory as the Dockerfile)
COPY . /app

# Create the final stage
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the virtual environment from the builder stage to the container
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy the application code from the builder stage to the container
COPY --from=builder /app /app

# Expose the port on which the application will run
EXPOSE 8000

# Collect static files and then run the application
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]
