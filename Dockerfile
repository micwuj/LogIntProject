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

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev \
    libleptonica-dev \
    libopencv-dev \
    python3-opencv \
    netcat-openbsd \
    adb \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . /code/

RUN apt-get update && apt-get install -y netcat-openbsd
RUN chmod +x /usr/wait-for-it.sh