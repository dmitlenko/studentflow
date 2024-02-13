# Use an official Python runtime as a parent image
FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /opt/app

# Configure environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH .

# Install dependencies
RUN set -xe \
    && apk update \
    && apk add python3-dev gcc libc-dev --no-cache

# Copy and install Python dependencies
COPY ["requirements.txt", "./"]
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY ["/studentflow/", "./studentflow/"]
COPY [".env", "entrypoint.sh", "./"]

# Set permissions
RUN chmod +x entrypoint.sh