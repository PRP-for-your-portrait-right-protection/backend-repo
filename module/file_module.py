from flask import request
from bucket.m_connection import s3_connection, s3_put_object, s3_get_object
from bucket.m_config import AWS_S3_BUCKET_NAME, AWS_S3_BUCKET_URL
from datetime import datetime
import hashlib
import os

"""
* 파일 업로드
"""
def upload(s3, db, collction_name, f, user_id, name=""):
    try:
        # 1. 파일 가져옴
        # f = request.files[file_name]
        
        # 2. lcoal에 파일 저장 - 파일 경로 때문에 저장해야함
        f.save(f.filename)
        
        # 3. 현재시간으로 파일명 secure
        # 3-1. 현재시간 string으로 가져옴
        now = datetime.now()
        time = now.strftime('%Y-%m-%d %H:%M:%S') + f.filename
        # 3-2. 파일명 암호화
        filename = hashlib.sha256(time.encode("utf-8")).hexdigest() + os.path.splitext(f.filename)[1]
        
        # 4. 버킷에 파일 저장
        if collction_name == 'upload_character':
            ret =s3_put_object(s3, AWS_S3_BUCKET_NAME, f.filename, f"upload_character/{filename}")
            location = f'{AWS_S3_BUCKET_URL}/upload_character/{filename}'
            col = db.upload_character
        elif collction_name == 'video_origin':
            ret =s3_put_object(s3, AWS_S3_BUCKET_NAME, f.filename, f"video_origin/{filename}")
            location = f'{AWS_S3_BUCKET_URL}/video_origin/{filename}'        
            col = db.video_origin
        elif collction_name == 'video_modification':
            ret =s3_put_object(s3, AWS_S3_BUCKET_NAME, f.filename, f"video_modification/{filename}")
            location = f'{AWS_S3_BUCKET_URL}/video_modification/{filename}'
            col = db.video_modification
        elif collction_name == 'people':
            ret =s3_put_object(s3, AWS_S3_BUCKET_NAME, f.filename, f"people/{filename}")
            location = f'{AWS_S3_BUCKET_URL}/people/{filename}'
            col = db.people
        
        # 5. local에 저장된 파일 삭제
        os.remove(f.filename)
            
        # 6. 버킷에 파일 저장 성공 시 진행
        if ret :
            
            # 6-1. obj 생성
            if collction_name == 'upload_character':
                obj = {
                    "character_id" : col.count()+1, # auto_increase
                    "user_id" : user_id,
                    "character_name" : filename,
                    "reg_date": now.strftime('%Y-%m-%d %H:%M:%S'),
                    "character_url" : location,
                    "activation_YN" : "Y"
                }
            elif collction_name == 'video_origin':
                obj = {
                    "video_id" : col.count()+1, # auto_increase
                    "user_id" : user_id,
                    "video_name" : filename,
                    "reg_date": now.strftime('%Y-%m-%d %H:%M:%S'),
                    "video_url" : location
                }
            elif collction_name == 'video_modification':
                obj = {
                    "video_id" : col.count()+1, # auto_increase
                    "user_id" : user_id,
                    "video_name" : filename,
                    "reg_date": now.strftime('%Y-%m-%d %H:%M:%S'),
                    "video_modification_url" : location,
                    "activation_YN" : "Y"
                }
            elif collction_name == 'people':
                obj = {
                    "person_id" : col.count()+1, # auto_increase
                    "user_id" : user_id,
                    "person_img_name" : filename,
                    "person_name" : name,
                    "reg_date": time,
                    "person_url" : location,
                    "activation_YN" : "Y"
                }
                
            # 6-2. db에 저장
            dbResponse = col.insert_one(obj)
            
            # 6-3. 성공 message return
            return location
        
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
* 단일 파일 업로드
"""
def single_upload(db, collction_name):
    try:
        # 1. 버킷 연결
        s3 = s3_connection()
        
        # 2. 아이디 가져옴
        user_id = request.form['user_id']
        
        # 4. return할 url json 형태로 생성
        col_json = {}
        col_json["file"] = []
        
        # 5. 파일 가져옴
        f = request.files['file']
        
        # 6. 파일 저장
        result = upload(s3, db, collction_name, f, user_id)
        
        # 7. json에 url 넣기
        col_json["file"] = result
            
        # 7. 성공 시 url json return
        return col_json
    except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
            return False
        
"""                                  
* 다중 파일 업로드 : front에 리스트로 묶어서 보내주기
"""
def multiple_upload(db, collction_name):
    try:
        # 1. 버킷 연결
        s3 = s3_connection()
        
        # 2. 아이디 가져옴
        user_id = request.form['user_id']
        
        # 4. return할 url json 형태로 생성
        col_json = {}
        col_json["file"] = []
        
        fs = request.files.getlist("file")
        
        # 6. 이름에 해당하는 파일 반복
        for f in fs:
            # 7. 파일 하나씩 저장
            result = upload(s3, db, collction_name, f, user_id)
            # 8. json에 url 넣기
            col_json["file"].append(result)
            
        # 7. 성공 시 url json return
        return col_json
    except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
            return False

"""                                  
* 사람 다중 파일 업로드 : front에 리스트로 묶어서 보내주기
"""
def people_multiple_upload(db, collction_name):
    try:
        # 1. 버킷 연결
        s3 = s3_connection()
        
        # 2. 아이디 가져옴
        user_id = request.form['user_id']
        
        # 3. 이름 가져옴
        names = request.form.getlist('name')
        
        # 4. return할 url json 형태로 생성
        col_json = {}
        col_json["file"] = []
        
        # 5. 이름에 해당하는 파일 가져옴
        for name in names:
            fs = request.files.getlist(name)
            
            # 6. 이름에 해당하는 파일 반복
            for f in fs:
                # 7. 파일 하나씩 저장
                result = upload(s3, db, collction_name, f, user_id, name)
                # 8. json에 url 넣기
                col_json["file"].append(result)
        
        # 7. 성공 시 url json return
        return col_json
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

