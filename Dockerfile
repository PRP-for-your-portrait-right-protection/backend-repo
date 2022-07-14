#FROM python:3.8-alpine
FROM python:latest


RUN mkdir /backend-repo
WORKDIR /backend-repo

#COPY requirements.txt /backend
#ADD는 압축을 풀어서 해제후 복사한다.

COPY . /backend-repo/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python__init__.py



CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

#CMD ["app.py"]

