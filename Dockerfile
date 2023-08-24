# Use an official Python runtime as a parent image
FROM python:3.8-alpine

# Install required OS dependencies
RUN apk update && \
    apk add bash && \
    apk add gcc libressl-dev musl-dev libffi-dev && \
    apk add make git curl

# To add poetry bin to path
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Perform software installation
RUN make init

# Make port available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "website_project/main.py"]
