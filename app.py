#-*- coding:utf-8 -*-
from flask import Flask, render_template, redirect, request, url_for
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import boto3
app = Flask(__name__)
client = MongoClient(
    host="localhost",
    port=27017,
    serverSelectionTimeoutMS = 5000 #5초 동안 접속이 되지 않을경우 에러메세지 발생
    )
def s3_connection():
    try:
        s3 = boto3.client(
            service_name = "s3",
            region_name = "ap-northease-2", #자신이 설정한 버켓 region
            aws_access_key_id = 'AWSAccessKeyId=AKIAYXSYOOKJM5S6R2DJ',
            aws_secret_access_key = 'AWSSecretKey=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',
        )
    except Exception as e:
        print("***********************************************************")
        print(e)
        print("***********************************************************")
    else:
        print("***********************************************************")
        print("S3 bucket connected!")
        print("***********************************************************")
        return s3
@app.route('/')
def hello():
    return "Hello!"
@app.route('/test')
def prt():
    return "hi"
s3 = s3_connection()

@app.route("/images", methods=["POST"])
def upload(s3): #프론트에서 멀티플 설정필요?, 파일형식 설정?
    if Flask.request.method == "POST": #POST일 경우에 작동
        image = request.files("image") #이미지 형식
        # for image in images:
        s3.put_object(
            Bucket = "jhmys3bucket35", #BUCKET_NAME
            Body = image,
            key = image,
            ContentType = "profile_image.jpg"
        )
        print("파일 저장 성공   ")

@app.route('/upload', methods=['GET', 'POST'])
def uploader_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file upload successfully'

if __name__ == '__main__':
    app.run(debug=True , host='0.0.0.0', port=5000)
    #port번호 : 0 0 0 0 으로 설정해야 외부에서 접근 가능
    #port : 5000번으로 설정