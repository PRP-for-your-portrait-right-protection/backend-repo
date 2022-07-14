from flask import request
import json
from werkzeug.utils import secure_filename
from m_connection import s3_connection, s3_put_object, s3_get_object
from m_config import AWS_S3_BUCKET_NAME
from datetime import datime, timedelta
import hashlib
import jwt



"""로그인"""


@app.route('/users', methods=["POST"])
def create_user():
    idReceive = request.form["id"]
    pwReceive = request.form["password"]
    nameReceive = request.form["name"]

    pwHash = hashlib.sha256(pwReceive.encode('utf-8')).hexdigest()

    now = datetime.now()

    try:
        user = {
            "userId" : idReceive,
            "password" : pwHash,
            "name" : nameReceive,
            "date" : f'{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}',
            "updateDate" : ""
            }

        db.account.insert_one(user)
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps(
                {
                    "message" : "CANNOT CREATE USER"
                }
            ),
            status = 500,
            mimetype = "application/json"
        )
    else:
        return Response(
            response = json.dumps(
                {
                    "result" : "USER CREATED",
                    "id" : idReceive,
                    "token" : token
                }
            ),
            status = 201,
            mimetype = "application/json"
        )


        







"""
* 단일 파일 업로드
"""
def single_upload(s3, db, collction_name):
    try:
        # 1. 파일 가져옴
        f = request.files['file']
        print(f)
        
        # 2. 파일명 secure
        filename = secure_filename(f.filename)
        
        # 3. lcoal에 파일 저장 - 필요 없을 시 삭제
        f.save(filename)
        
        # 4. 버킷에 파일 저장
        if collction_name == 'upload_character':
            ret =s3_put_object(s3, AWS_S3_BUCKET_NAME, f.filename, f"upload_character/{filename}")
            col = db.upload_character
        elif collction_name == 'video_origin':
            ret =s3_put_object(s3, AWS_S3_BUCKET_NAME, f.filename, f"video_origin/{filename}")
            col = db.video_origin
        elif collction_name == 'video_modification':
            ret =s3_put_object(s3, AWS_S3_BUCKET_NAME, f.filename, f"video_modification/{filename}")
            col = db.video_modification
            
        # 5. 버킷에 파일 저장 성공 시 진행
        if ret :
            # 5-1. 현재 시간 가져오기
            now = datetime.now()
            
            # 5-2. db에 저장할 object 생성
            # col = db.collction_name
            
            if collction_name == 'upload_character':
                obj = {
                    "character_id" : col.count()+1, # auto_increase
                    "user_id" : request.form["user_id"],
                    "character_name" : filename,
                    "reg_date": now.strftime('%Y-%m-%d %H:%M:%S')
                }
            elif collction_name == 'video_origin':
                obj = {
                    "video_id" : col.count()+1, # auto_increase
                    "user_id" : request.form["user_id"],
                    "video_name" : filename,
                    "reg_date": now.strftime('%Y-%m-%d %H:%M:%S')
                }
            elif collction_name == 'video_modification':
                obj = {
                    "video_id" : col.count()+1, # auto_increase
                    "user_id" : request.form["user_id"],
                    "video_name" : filename,
                    "reg_date": now.strftime('%Y-%m-%d %H:%M:%S')
                }
            
            # 5-3. db에 저장
            dbResponse = col.insert_one(obj)
            
            # 5-4. 성공 message return
            return True
        
        # 5. 버킷에 파일 저장 실패 시 진행
        else:
            # 5-1. 실패 message return
            return False
    except Exception as ex:
        
            print("******************")
            print(ex)
            print("******************")
            return False
        
"""
* 단일 파일 다운로드
"""
def download(s3, db, collction_name):
    if collction_name == 'upload_character':
        ret =s3_get_object(s3, AWS_S3_BUCKET_NAME, request.form["filename"], request.form["filename"])
            
    elif collction_name == 'video_origin':
        ret =s3_get_object(s3, AWS_S3_BUCKET_NAME, request.form["filename"], request.form["filename"])
    
    elif collction_name == 'video_modification':
        ret =s3_get_object(s3, AWS_S3_BUCKET_NAME, request.form["filename"], request.form["filename"])
    
    if ret :
        return 'file download successfully'
    else:
        return 'file download fail'
    
    
"""
* 다중 파일 업로드
"""
def multiple_upload(s3, db, collction_name):
    try:
        # 1. 파일 가져옴
        fs = request.getlist("file[]")
        
        for f in fs:
            # 2. 파일명 secure
            filename = secure_filename(f.filename)
            
            # 3. lcoal에 파일 저장 - 필요 없을 시 삭제
            # f.save(filename)
            
            # 4. 버킷에 파일 저장
            if collction_name == 'people':
                ret =s3_put_object(s3, AWS_S3_BUCKET_NAME, './temp', f"people/{filename}")
                col = db.people
                
            # 5. 버킷에 파일 저장 성공 시 진행
            if ret :
                # 5-1. 현재 시간 가져오기
                now = datetime.now()
                
                # 5-2. db에 저장할 object 생성
                # col = db.collction_name
                
                if collction_name == 'people':
                    obj = {
                        "people_id" : col.count()+1, # auto_increase
                        "user_id" : request.form["user_id"],
                        "people_name" : filename,
                        "people_num" : 0,
                        "reg_date": now.strftime('%Y-%m-%d %H:%M:%S')
                    }
                
                # 5-3. db에 저장
                dbResponse = col.insert_one(obj)
                
                # 5-4. 성공 message return
                return True
        
            # 5. 버킷에 파일 저장 실패 시 진행
            else:
                # 5-1. 실패 message return
                return False
    except Exception as ex:
        
            print("******************")
            print(ex)
            print("******************")
            return False