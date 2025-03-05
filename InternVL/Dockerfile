# 基于Conda环境中的base镜像
FROM pytorch/pytorch:2.2.1-cuda12.1-cudnn8-devel
# FROM ubuntu/python:3.10-22.04_stable
# FROM ubuntu:22.04


# RUN apt-get -y update && apt -get install software-properties-common \
# && add-apt-repository ppa:deadsnakes/ppa && apt install python3.10

RUN apt-get update
# RUN add-apt-repository ppa:deadsnakes/ppa
# apt-get install -y python3.10

WORKDIR /workspace
COPY requirements.txt requirements.txt


RUN apt-get update
RUN apt-get -y install git
RUN apt-get -y install curl
RUN apt-get install libgl1-mesa-glx -y


RUN git clone https://github.com/vllm-project/vllm.git
RUN cd vllm 
RUN python use_existing_torch.py
RUN pip install -r requirements-build.txt
RUN pip install -e . --no-build-isolation

RUN pip install -r requirements.txt
RUN pip3 install opencv-python
RUN pip install opencv-python-headless
RUN pip install --upgrade deepspeed==0.14.4
RUN pip install wandb
RUN pip install flash-attn --no-build-isolation
