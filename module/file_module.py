from flask import request
from werkzeug.utils import secure_filename
from bucket.m_connection import s3_connection, s3_put_object, s3_get_object
from bucket.m_config import AWS_S3_BUCKET_NAME
from datetime import datetime
import hashlib
import os

"""
* 단일 파일 업로드
"""
def single_upload(db, collction_name):
    try:
        s3 = s3_connection()
        
        # 1. 파일 가져옴
        f = request.files['file']
        
        # 2. lcoal에 파일 저장 - 파일 경로 때문에 저장해야함
        f.save(f.filename)
        
        # 3. 현재시간으로 파일명 secure
        # 3-1. 현재시간 string으로 가져옴
        now = datetime.now()
        time = now.strftime('%Y-%m-%d %H:%M:%S')
        # 3-2. 파일명 암호화
        filename = hashlib.sha256(time.encode("utf-8")).hexdigest() + os.path.splitext(f.filename)[1]
        
        # 4. 버킷에 파일 저장
        if collction_name == 'upload_character':
            ret =s3_put_object(s3, AWS_S3_BUCKET_NAME, f.filename, f"upload_character/{filename}")
            location = f'https://prpproject.s3.ap-northeast-2.amazonaws.com/upload_character/{filename}'
            col = db.upload_character
        elif collction_name == 'video_origin':
            ret =s3_put_object(s3, AWS_S3_BUCKET_NAME, f.filename, f"video_origin/{filename}")
            location = f'https://prpproject.s3.ap-northeast-2.amazonaws.com/video_origin/{filename}'        
            col = db.video_origin
        elif collction_name == 'video_modification':
            ret =s3_put_object(s3, AWS_S3_BUCKET_NAME, f.filename, f"video_modification/{filename}")
            location = f'https://prpproject.s3.ap-northeast-2.amazonaws.com/video_modification/{filename}'
            col = db.video_modification
        
        # 5. local에 저장된 파일 삭제
        os.remove(f.filename)
            
        # 6. 버킷에 파일 저장 성공 시 진행
        if ret :
            
            # 6-1. obj 생성
            if collction_name == 'upload_character':
                obj = {
                    "character_id" : col.count()+1, # auto_increase
                    "user_id" : request.form["user_id"],
                    "character_name" : filename,
                    "reg_date": now.strftime('%Y-%m-%d %H:%M:%S'),
                    "character_url" : location,
                    "activation_YN" : "Y"
                }
            elif collction_name == 'video_origin':
                obj = {
                    "video_id" : col.count()+1, # auto_increase
                    "user_id" : request.form["user_id"],
                    "video_name" : filename,
                    "reg_date": now.strftime('%Y-%m-%d %H:%M:%S'),
                    "video_url" : location
                }
            elif collction_name == 'video_modification':
                obj = {
                    "video_id" : col.count()+1, # auto_increase
                    "user_id" : request.form["user_id"],
                    "video_name" : filename,
                    "reg_date": now.strftime('%Y-%m-%d %H:%M:%S'),
                    "video_modification_url" : location,
                    "activation_YN" : "Y"
                }
                
            # 6-2. db에 저장
            dbResponse = col.insert_one(obj)
            
            if collction_name == 'video_modification':
                return location
            # 6-3. 성공 message return
            return True
        
        # 6. 버킷에 파일 저장 실패 시 진행
        else:
            # 6-1. 실패 message return
            return False
    except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
            return False
        
"""
* 단일 파일 다운로드 - 동영상 다운로드에서만 사용
"""
def single_download(db, collction_name):
    s3 = s3_connection()
    filename = request.form["filename"]
    if collction_name == 'video_modification':
        ret =s3_get_object(s3, AWS_S3_BUCKET_NAME, f"video_modification/{filename}", filename)
    elif collction_name == 'video_origin':
        ret =s3_get_object(s3, AWS_S3_BUCKET_NAME, f"video_origin/{filename}", filename)
    elif collction_name == 'upload_character':
        ret =s3_get_object(s3, AWS_S3_BUCKET_NAME, f"upload_character/{filename}", filename)
    if ret :
        return True
    else:
        return False
    
"""                                  
* 다중 파일 업로드
"""
def multiple_upload(db, collction_name):
    try:
        s3 = s3_connection()
        
        # 1. 파일 가져옴
        fs = request.files.getlist("file")
        
        for f in fs:
            # 2. lcoal에 파일 저장 - 파일 경로 때문에 저장해야함
            f.save(f.filename)
            
            # 3. 현재시간으로 파일명 secure
            # 3-1. 현재시간 string으로 가져옴
            now = datetime.now()
            time = now.strftime('%Y-%m-%d %H:%M:%S')
            # 3-2. 파일명 암호화
            filename = hashlib.sha256(time.encode("utf-8")).hexdigest() + os.path.splitext(f.filename)[1]

            # 4. 버킷에 파일 저장
            if collction_name == 'upload_character':
                ret =s3_put_object(s3, AWS_S3_BUCKET_NAME, f.filename, f"upload_character/{filename}")
                location = f'https://prpproject.s3.ap-northeast-2.amazonaws.com/upload_character/{filename}'
                col = db.upload_character
            if collction_name == 'people':
                ret =s3_put_object(s3, AWS_S3_BUCKET_NAME, f.filename, f"people/{filename}")
                location = f'https://prpproject.s3.ap-northeast-2.amazonaws.com/people/{filename}'
                col = db.people
            
            # 5. local에 저장된 파일 삭제
            os.remove(f.filename)
            
            # 6. 버킷에 파일 저장 성공 시 진행
            if ret :
                
                # 6-1. db에 저장할 object 생성
                if collction_name == 'upload_character':
                    obj = {
                        "character_id" : col.count()+1, # auto_increase
                        "user_id" : request.form["user_id"],
                        "character_name" : filename,
                        "reg_date": time,
                        "character_url" : location,
                        "activation_YN" : "Y"
                    }
                if collction_name == 'people':
                    obj = {
                        "person_id" : col.count()+1, # auto_increase
                        "user_id" : request.form["user_id"],
                        "person_img_name" : filename,
                        "person_name" : request.values.get("person_name"),
                        "reg_date": time,
                        "person_url" : location,
                        "activation_YN" : "Y"
                    }
                
                # 6-2. db에 저장
                dbResponse = col.insert_one(obj)
        
            # 6. 버킷에 파일 저장 실패 시 진행
            else:
                # 6-1. 실패 message return
                return False
            
        # 7. 성공 message return
        return True
    except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
            return False
    
"""
* 일인 다중 파일 url 가져오기
"""
def single_get(db, collction_name):
    try:
        # 1. collction_name 확인 & user_id 가져오기
        if collction_name == "get_character": 
            col = db.upload_character
            userId = request.form["user_id"]
        elif collction_name == "get_origin_character":
            col = db.origin_character
            userId = "origin_character"
        else:
            print("can't find collction name")
            return False
        
        # 2. user_id에 해당하는 값 모두 가져오기
        docs = col.find({"user_id" : userId})

        # 3. json 형태로 매핑
        col_json = {}
        col_json[userId] = []
        for x in docs:
            col_json[userId].append(x['character_url'])

        # 4. 다중 파일 json 반환
        return col_json
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False

"""
* 다인 다중 파일 url 가져오기
"""
def multiple_get(db, collction_name):
    try:
        # 1. collction_name 확인
        if collction_name == "get_people":
            col = db.people
        else:
            print("can't find collction name")
            return False

        # 2. user_id 가져오기
        userId = request.form["user_id"]

        # 3. user id에 해당하는 person_name을 중복 제거 하여 가져옴
        col_list = col.distinct("person_name", {"user_id" : userId})

        # 4. json 형태로 매핑
        col_json = {}

        for name in col_list:
            col_json[name] = []
            if collction_name == "get_people":
                docs = col.find({"person_name" : name, "user_id" : userId})
                for x in docs:
                    col_json[name].append(x['person_img_url'])

        # 5. 다중 파일 json 반환
        return col_json
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False