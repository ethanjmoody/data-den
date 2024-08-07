FROM nvidia/cuda:12.1.0-base-ubuntu22.04

# Set bash as the default shell
ENV SHELL=/bin/bash

# Create a working directory
WORKDIR /app/

# Build with some basic utilities
RUN apt-get update && apt-get install -y \
    apt-utils \
    ffmpeg \
    git \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    python3-pip \
    vim  

# alias python='python3'
RUN ln -s /usr/bin/python3 /usr/bin/python

# build with some basic python packages
RUN pip install \
    accelerate \
    anthropic \
    bitsandbytes \
    bs4 \
    easyocr \
    ftfy \
    git+https://github.com/huggingface/diffusers \
    IProgress \
    ipywidgets \
    jupyterlab \
    langchain \
    langchainhub \
    langchain-anthropic \
    langchain-community \
    langchain-huggingface \
    langchain-openai \
    langchain-qdrant \
    openai \
    peft \
    pillow \
    protobuf \
    pydub \
    PyMuPDF \
    python-bidi==0.4.2 \
    qdrant-client \
    sentencepiece \
    sentence-transformers \
    streamlit \
    tiktoken \
    torch \
    torchvision \
    torchaudio \
    transformers \
    tqdm \ 
    wikipedia \
    yt_dlp
 
# start jupyter lab
EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "Welcome to EduCreate.py", "--server.port=8501"]
