From python:3.9.16-slim-buster

# Create app directory
RUN mkdir -p /app

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt


EXPOSE 8080

# Run main.py when the container launches
ENTRYPOINT ["python3", "main.py"]
