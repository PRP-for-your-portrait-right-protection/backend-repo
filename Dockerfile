#FROM python:3.8-alpine
FROM python:latest


RUN mkdir /backend
WORKDIR /backend

#COPY requirements.txt /backend
#ADD는 압축을 풀어서 해제후 복사한다.

COPY . /backend/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

#CMD ["app.py"]

