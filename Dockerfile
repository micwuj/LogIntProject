# Pull the official base image
FROM python:3.12

COPY wait-for-it.sh /usr/wait-for-it.sh

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

RUN apt-get update && apt-get install -y netcat-openbsd
RUN chmod +x /usr/wait-for-it.sh