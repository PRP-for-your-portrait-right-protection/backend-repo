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
    if db == None:
        print("Can't connect to DB")
        return False

    try:
        # 1. 파일 가져옴
        # f = request.files[file_name]

        # 2. lcoal에 파일 저장 - 파일 경로 때문에 저장해야함
        f.save(f.filename)
        
        # 3. 현재시간으로 파일명 secure
        # 3-1. 현재시간 string으로 가져옴
        now = datetime.now()
        time = now.strftime('%Y-%m-%d %H:%M:%S')
        fileTime = now.strftime('%Y-%m-%d')

        # 3-2. 파일명 암호화 : 파일명 암호화 필요한가?
        # filename = hashlib.sha256(f.filename.encode("utf-8")).hexdigest() + hashlib.sha256(.encode("utf-8")).hexdigest() + os.path.splitext(f.filename)[1]
        name, ext = os.path.splitext(f.filename)
        filename = user_id + "_" + name + "_" + fileTime + ext

        # 4. 버킷에 파일 저장
        if collction_name == 'upload_character':
            ret = s3_put_object(s3, AWS_S3_BUCKET_NAME, f.filename, f"upload_character/{filename}")
            location = f'{AWS_S3_BUCKET_URL}/upload_character/{filename}'
            col = db.upload_character
        elif collction_name == 'video_origin':
            ret = s3_put_object(s3, AWS_S3_BUCKET_NAME, f.filename, f"video_origin/{filename}")
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
        else:
            print("Can't find collection")
            return False

        # 5. local에 저장된 파일 삭제
        os.remove(f.filename)
            
        # 6. 버킷에 파일 저장 성공 시 진행
        if ret :
            
            # 6-1. obj 생성
            if collction_name == 'upload_character':
                obj = {
                    "character_id" : 1, # auto_increase
                    "user_id" : user_id,
                    "character_name" : filename,
                    "character_url" : location,
                    "activation_YN" : "Y",
                    "reg_date": now.strftime('%Y-%m-%d %H:%M:%S')
                }
            elif collction_name == 'video_origin':
                obj = {
                    "video_id" : 1, # auto_increase
                    "user_id" : user_id,
                    "video_name" : filename,
                    "video_url" : location,
                    "reg_date": now.strftime('%Y-%m-%d %H:%M:%S')
                }
            elif collction_name == 'video_modification':
                obj = {
                    "video_id" : 1, # auto_increase
                    "user_id" : user_id,
                    "video_name" : filename,
                    "video_modification_url" : location,
                    "activation_YN" : "Y",
                    "reg_date": now.strftime('%Y-%m-%d %H:%M:%S'),
                }
            elif collction_name == 'people':
                obj = {
                    "person_id" : 1, # auto_increase
                    "user_id" : user_id,
                    "person_img_name" : filename,
                    "person_name" : name,
                    "person_url" : location,
                    "activation_YN" : "Y",
                    "reg_date": time
                }
            else:
                print("Can't find collection")
                return False
                
            # 6-2. db에 저장
            col.insert_one(obj)

            # 6-3. 성공 message return
            if location != None:
                return location
            else:
                print("Can't find location")
                return False
        
        # 6. 버킷에 파일 저장 실패 시 진행 (ret == False 일 경우)
        else:
            return False
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")
        return False

"""                                  
* 단일 파일 업로드
"""
def single_upload(db, collction_name, file_key, user_id):
    if db == None:
        print("Can't connect to DB")
        return False

    try:
        # 1. 버킷 연결
        s3 = s3_connection()

        # 2. return할 url json 형태로 생성
        colJson = {}
  
        # 3. 파일 가져옴
        f = request.files[file_key]
        
        # 4. 파일 저장
        result = upload(s3, db, collction_name, f, user_id)
        
        if result == False:
            print("file upload failed")
            return False

        # 5. json에 url 넣기
        colJson[file_key] = result
        
        if colJson == None:
            print("colJson is None")
            return False
            
        # 6. 성공 시 url json return
        else:
            return colJson
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")
        return False
        
"""                                  
* 다중 파일 업로드 : front에 리스트로 묶어서 보내주기
"""
def multiple_upload(db, collction_name, file_key, user_id):
    if db == None:
        print("Can't connect to DB")
        return False

    try:
        # 1. 버킷 연결
        s3 = s3_connection()
        
        # 2. return할 url json 형태로 생성
        colJson = {}
        colJson[file_key] = []
        
        fs = request.files.getlist(file_key)

        # 3. 이름에 해당하는 파일 반복
        for f in fs:
            # 3-1. 파일 하나씩 저장
            result = upload(s3, db, collction_name, f, user_id)
            if result == None or result == False:
                print("Error occurred in uploading file")
                return False
            # 3-2. json에 url 넣기
            colJson[file_key].append(result)
            
        # 4. 성공 시 url json return
        return colJson
    except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
            return False

"""                                  
* 사람 다중 파일 업로드 : front에 리스트로 묶어서 보내주기
"""
def people_multiple_upload(db, collction_name, user_id):
    if db == None:
        print("Can't connect to DB")
        return False

    try:
        # 1. 버킷 연결
        s3 = s3_connection()
        
        # 2. 이름 가져옴
        names = request.form.getlist('name')

        for name in names:
            if name == None or name == "":
                print("Can't find name")
                return False
        
        # 3. return할 url json 형태로 생성
        colJson = {}
        colJson["file"] = []
        
        # 4. 이름에 해당하는 파일 가져옴
        for name in names:
            # 여기서 에러 검출 불가 : names 안에 없는 값이 들어오는 경우에 대한 에러 검출 안함
            fs = request.files.getlist(name)

            # 5. 이름에 해당하는 파일 반복
            for f in fs:
                # 5-1. 파일 하나씩 저장
                result = upload(s3, db, collction_name, f, user_id, name)
                if result == None or result == False:
                    print("Error occurred in file uploading")
                    return False
                # 5-2. json에 url 넣기
                colJson["file"].append(result)

        # 6. 성공 시 url json return
        return colJson
    except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
            return False

"""
* 단일 파일 다운로드 - 동영상 다운로드에서만 사용
"""
def single_download(db, collction_name, user_id, filename):
    s3 = s3_connection()

    if collction_name == 'video_modification':
        ret = s3_get_object(s3, AWS_S3_BUCKET_NAME, f"video_modification/{filename}", filename)
    elif collction_name == 'video_origin':
        ret = s3_get_object(s3, AWS_S3_BUCKET_NAME, f"video_origin/{filename}", filename)
    elif collction_name == 'upload_character':
        ret = s3_get_object(s3, AWS_S3_BUCKET_NAME, f"upload_character/{filename}", filename)
    else:
        print("Can't find collection")
        return False

    if ret :
        return True
    else:
        print("file downloading fail")
        return False
