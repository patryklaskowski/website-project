# Use an official Python runtime as a parent image
FROM python:3.9-alpine

# Install required OS dependencies
RUN apk update && \
    apk add bash && \
    apk add --no-cache make

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Perform software installation
RUN make install

# Make port available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV DEBUG False

# Run app.py when the container launches
CMD ["python", "website_project/main.py"]
