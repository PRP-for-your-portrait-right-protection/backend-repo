from flask import request
from bucket.m_connection import s3_connection
from bucket.m_config import AWS_S3_BUCKET_NAME 
from datetime import datetime
import boto3 #버켓의 사진 삭제 

"""
* 단일 삭제
"""
def single_delete(db, collection_name):
    try: 
        # 컬렉션 설정 후 URL 가져옴 (인물, 비디오 결과, 업로드 캐릭터 모두 가능)
        if collection_name == "people":
            col = db.people
            url = request.form["url"]
            url_string = "person_url"
        elif collection_name == "video_modification":
            col = db.video_modification
            url = request.form["url"]
            url_string = "video_modification_url"
        elif collection_name == "character":
            col = db.upload_character
            url = request.form["url"]
            url_string = "character_url"
        
        # 유저 아이디 가져옴
        userId = request.form["user_id"]

        # DB에서 유저아이디 && url 일치하는 Document -> activation_YN = N
        col.update_one(
            {
                "user_id" : userId, 
                "f'{url_string}'" : url
            }, 
            {"$set" : 
                {
                    "activation_YN" : "N"
                }
            }) 
        return True
    except Exception as ex:
            print('*********')
            print(ex)
            print('*********')
            return False    

"""
* 다중 삭제
* 1. 특정 인물에 대한 사진 모두 삭제
* 2. 특정 유저에 대한 비디오 결과 모두 삭제
* 3. 특정 유저에 대한 캐릭터 모두 삭제
"""       
def multiple_delete(db, collection_name):
    try:
        # 컬렉션 설정 후 상황에 맞는 쿼리 설정
            # 인물 -> user_id, person_name 필요
            # 비디오 결과 -> user_id 필요
            # 업로드 캐릭터 -> user_id 필요
        if collection_name == "people":
            col = db.people
            my_query = {
                    "user_id" : request.form["user_id"],
                    "person_name" : request.form["person_name"]
                }
        elif collection_name == "video_modification":
            col = db.video_modification
            my_query = {
                    "user_id" : request.form["user_id"]
                }
        elif collection_name == "characters":
            col = db.upload_character
            my_query = {
                    "user_id" : request.form["user_id"]
                }

        # 쿼리에 일치하는 Document 모두 -> activation_YN = N
        col.update_many(
            my_query,
            {"$set" : 
                {
                    "activation_YN" : "N"
                }
            })
        return True
    except Exception as ex:
            print('*********')
            print(ex)
            print('*********')
            return False   

"""
* 인물 이름 수정
"""
def single_update(db):
    try:
        # 컬렉션 설정
        col = db.people

        # 주어진 user_id, person_name에 해당하는 Document 수정
        col.update_many(
            {
                "user_id" : request.form["user_id"], 
                "person_name" : request.form["person_name"]
            }, 
            {"$set" : 
                {
                    "person_name" : request.form["person_name_after"], 
                    "mod_date" : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            })
        return True
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False   