# Use an official Python runtime as a base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask app on port 8081
EXPOSE 8081

# Run the application
CMD ["python", "main.py"]
