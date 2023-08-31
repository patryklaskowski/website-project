# Use an official Python runtime as a parent image
FROM python:3.9

# Install required OS dependencies
RUN apt-get update && \
    apt-get install -y bash make git

# Set the working directory
WORKDIR /website_project

# Copy the current directory contents into the container at /app
COPY . /website_project

# Perform software installation
RUN make install

# Make port available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "website_project/main.py"]
