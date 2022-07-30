FROM python:latest

RUN mkdir /backend
WORKDIR /backend

COPY . /backend/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# for error message
ENV PYTHONUNBUFFERED 1
