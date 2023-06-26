# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Run a Python script when the container launches
CMD ["python", "romeo_and_juliet.py"]
