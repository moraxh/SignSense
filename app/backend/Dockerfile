# Use a base image with NVIDIA GPU and CUDA support
FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04

# Install Python and system dependencies
RUN apt-get update && apt-get install -y \
  python3.10 python3.10-venv python3-pip \
  libgl1-mesa-glx libglib2.0-0 \
  libsm6 libxext6 libxrender-dev \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set Python and pip as default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

WORKDIR /app/backend

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5100
EXPOSE 5101

COPY . .
