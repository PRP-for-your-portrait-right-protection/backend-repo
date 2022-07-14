FROM python:latest

RUN mkdir /backend-repo
WORKDIR /backend-repo

COPY . /backend-repo/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# RUN python setup.py
