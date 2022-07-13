from flask import request
from werkzeug.utils import secure_filename
from bucket.m_connection import s3_connection, s3_put_object, s3_get_object
from bucket.m_config import AWS_S3_BUCKET_NAME
from datetime import datetime

#TO-DO 파일명 암호화 후 저장 - 파일명 겹치면 버킷에서 덮어쓰기 됨

"""
* 단일 파일 업로드
* 인물 : 한 명인 경우에만 가능
"""
def single_upload(db, collction_name):
    try:
        s3 = s3_connection()
        
        # 1. 파일 가져옴
        f = request.files['file']
        
        # 2. 파일명 secure
        filename = secure_filename(f.filename)
        
        # 3. lcoal에 파일 저장 - 필요 없을 시 삭제
        # f.save(filename)
        
        # 4. 버킷에 파일 저장
        if collction_name == 'upload_character':
            ret =s3_put_object(s3, AWS_S3_BUCKET_NAME, f.filename, f"upload_character/{filename}")
            location = f'https://siliconproject.s3.us-east-1.amazonaws.com/upload_character/{filename}'
            col = db.upload_character
        elif collction_name == 'video_origin':
            ret =s3_put_object(s3, AWS_S3_BUCKET_NAME, f.filename, f"video_origin/{filename}")
            location = f'https://siliconproject.s3.us-east-1.amazonaws.com/video_origin/{filename}'        
            col = db.video_origin
        elif collction_name == 'video_modification':
            ret =s3_put_object(s3, AWS_S3_BUCKET_NAME, f.filename, f"video_modification/{filename}")
            location = f'https://siliconproject.s3.us-east-1.amazonaws.com/video_modification/{filename}'
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
                    "reg_date": now.strftime('%Y-%m-%d %H:%M:%S'),
                    "character_url" : location
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
                    "video_modification_url" : location
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
        print(fs)
        
        for f in fs:
            # 2. 파일명 secure
            filename = secure_filename(f.filename)
            print(filename)
            
            f.save(filename)
            
            # 3. lcoal에 파일 저장 - 필요 없을 시 삭제
            # f.save(filename)
            
            # 4. 버킷에 파일 저장
            if collction_name == 'upload_character':
                ret =s3_put_object(s3, AWS_S3_BUCKET_NAME, filename, f"upload_character/{filename}")
                location = f'https://siliconproject.s3.us-east-1.amazonaws.com/upload_character/{filename}'
                col = db.upload_character
            if collction_name == 'people':
                ret =s3_put_object(s3, AWS_S3_BUCKET_NAME, f.filename, f"people/{filename}")
                location = f'https://siliconproject.s3.us-east-1.amazonaws.com/people/{filename}'
                col = db.people
                
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
                        "reg_date": now.strftime('%Y-%m-%d %H:%M:%S'),
                        "character_url" : location
                    }
                if collction_name == 'people':
                    obj = {
                        "person_id" : col.count()+1, # auto_increase
                        "user_id" : request.form["user_id"],
                        "person_img_name" : filename,
                        "person_name" : request.values.get("person_name"),
                        "reg_date": now.strftime('%Y-%m-%d %H:%M:%S'),
                        "person_img_url" : location
                    }
                
                # 5-3. db에 저장
                dbResponse = col.insert_one(obj)
        
            # 5. 버킷에 파일 저장 실패 시 진행
            else:
                # 5-1. 실패 message return
                return False
            
        # 6. 성공 message return
        return True
    except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
            return False
        
        
"""
* 다수 인물 다중 파일 업로드
"""
'''
프론트에서 작업해줘야 함
사람들 갯수를 counting하고 그 수만큼 api와 통신하면서 진행!

예)
사람1 - 4장
사람2 - 5장
사람3 - 3장

for(int i=0; i<3; i++)
    // 여기서 video-modification에 post 반복
    // param으로 사람이름 보내기 -> 동명이인 고려X
        // 동명이인 정도는 사용자가 알아서 하겠찌,,,
'''