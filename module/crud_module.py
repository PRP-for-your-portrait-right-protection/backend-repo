from flask import request
from bucket.m_connection import s3_connection
from bucket.m_config import AWS_S3_BUCKET_NAME 
import boto3 #버켓의 사진 삭제 

"""
* 인물 삭제
* 해당 인물 사진까지 삭제
"""
def deleteTEMP(db, one_or_many):
    if one_or_many == "one":
        try: 
            # 버켓 연결
            s3 = s3_connection()

            # 유저 아이디, 사진 URL 가져옴
            userId = request.form["user_id"]
            personImgUrl = request.form["person_img_url"]

            # 컬렉션 연결
            col = db.people

            # 버켓에서 삭제
            # 문자열 처리 예시 : "https://s3.console.aws.amazon.com/s3/object/
            # jhmys3bucket35?region=ap-northeast-2&prefix=images/image_0.jpg" -------------> image_0.jpg
            s3Key = personImgUrl.split('/')[4]

            # 버켓에서 삭제
            # f스트링 예시 -> people/image_0.jpg
            s3.delete_object(Bucket = AWS_S3_BUCKET_NAME, Key = f'people/{s3Key}')  

            # DB에서 유저아이디 && url 일치하는 Document 삭제
            col.delete_one({"user_id" : userId, "person_img_url" : personImgUrl}) 

            return True
        except:
            print('*********')
            print(ex)
            print('*********')
            return False
    if one_or_many == "many":
        try:
            # 버켓 연결
            s3 = s3_connection()

            # 유저 아이디, 사람 이름 가져옴
            userId = request.form["user_id"]
            personName = request.form["person_name"]

            # 컬렉션 연결
            col = db.people

            # URL 가져온 후 버켓에서 삭제
            col.find

            # 유저아이디 && 사람이름 일치하는 Document 모두 삭제
            col.delete_many({"user_id" : userId, "person_name" : personName})

            return True
        except Exception as ex:
            print('*********')
            print(ex)
            print('*********')
            return False

"""
* 사람 이름 수정
"""
def updateTEMP():


