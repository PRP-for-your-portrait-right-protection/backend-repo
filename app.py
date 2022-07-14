from flask import Flask, Response, request
import json
from static import status_code
from module import file_module,login_module
from db import db_connection

##
from datetime import datetime, timedelta
import hashlib
import jwt




app = Flask(__name__)

# DB 연결
db = db_connection.db_connection()

# 스키마 생성
#db_connection.init_collection(db)

'''
# 
# @form-data : file, user_id, person_name
#
'''



@app.route('/person', methods=['POST'])
def uploadPerson():
    try:
        if file_module.multiple_upload(db, "people"):
    
            # 5-4. 성공 message return
            return Response(
                response=json.dumps(
                    {
                        "message":status_code.fileupload_01_success,
                    }
                ),
                status=200,
                mimetype="application/json"
            )
        
        # 5. 버킷에 파일 저장 실패 시 진행
     
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")
        
'''
# 
# @form-data : file, user_id
#
'''
@app.route('/character', methods=['POST'])
def uploadCharacter():
    try:
        if file_module.single_upload(db, "upload_character"):
    
            # 5-4. 성공 message return
            return Response(
                response=json.dumps(
                    {
                        "message":status_code.fileupload_01_success,
                    }
                ),
                status=200,
                mimetype="application/json"
            )
        
        # 5. 버킷에 파일 저장 실패 시 진행
        else:
            # 5-1. 실패 message return
            return Response(
                response=json.dumps(
                    {
                        "message":status_code.fileupload_02_fail,
                    }
                ),
                status=200,
                mimetype="application/json"
            )
    except Exception as ex:
            print("******************")
            print(ex)
            print("******************")

'''
# 
# @form-data : file, user_id
#
'''
@app.route('/characters', methods=['POST'])
def uploadCharacters():
    try:
        if file_module.multiple_upload(db, "upload_character"):
    
            # 5-4. 성공 message return
            return Response(
                response=json.dumps(
                    {
                        "message":status_code.fileupload_01_success,
                    }
                ),
                status=200,
                mimetype="application/json"
            )
        
        # 5. 버킷에 파일 저장 실패 시 진행
        else:
            # 5-1. 실패 message return
            return Response(
                response=json.dumps(
                    {
                        "message":status_code.fileupload_02_fail,
                    }
                ),
                status=200,
                mimetype="application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")

'''
# 
# @form-data : file, user_id
#
'''
@app.route('/video-origin', methods=['POST'])
def oringinVideo():
    try:
        if file_module.single_upload(db, "video_origin"):
    
            # 5-4. 성공 message return
            return Response(
                response=json.dumps(
                    {
                        "message":status_code.fileupload_01_success,
                    }
                ),
                status=200,
                mimetype="application/json"
            )
        
        # 5. 버킷에 파일 저장 실패 시 진행
        else:
            # 5-1. 실패 message return
            return Response(
                response=json.dumps(
                    {
                        "message":status_code.fileupload_02_fail,
                    }
                ),
                status=200,
                mimetype="application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")

'''
# 
# @form-data : file, user_id
#
'''
@app.route('/video-modification', methods=['POST'])
def modificationVideo():
    try:
        if file_module.single_upload(db, "video_modification"):
    
            # 5-4. 성공 message return
            return Response(
                response=json.dumps(
                    {
                        "message":status_code.fileupload_01_success,
                    }
                ),
                status=200,
                mimetype="application/json"
            )
        
        # 5. 버킷에 파일 저장 실패 시 진행
        else:
            # 5-1. 실패 message return
            return Response(
                response=json.dumps(
                    {
                        "message":status_code.fileupload_02_fail,
                    }
                ),
                status=200,
                mimetype="application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")

"""
#* 단일 파일 다운로드
"""
@app.route('/video-modification', methods=['GET'])
def filedownload():
    try:
        if file_module.single_download(db, "video_modification") :
            return Response(
                    response=json.dumps(
                        {
                            "message":status_code.filedownload_01_success,
                        }
                    ),
                    status=200,
                    mimetype="application/json"
            )
        else:
            return Response(
                    response=json.dumps(
                        {
                            "message":status_code.filedownload_02_fail,
                        }
                    ),
                    status=200,
                    mimetype="application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")

'''
# 
# @signup : db
#회원가입
'''
@app.route('/signup', methods=['POST'])
def create_user():
    try:
        idReceive = login_module.create_users(db)
        
        if idReceive != None:
         
            return Response(
                response = json.dumps(
                {
                    "result" : status_code.create_01_success,
                    "id" : idReceive,
                    
                }
            ),
            status = 201,
            mimetype = "application/json"
        )
        else:
      
            return Response(
                response = json.dumps(
                {
                    "message" : status_code.create_02_fail
                }
            ),
            status = 200,
            mimetype = "application/json"
        )
        
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")
        return Response(
            response = json.dumps(
                {
                    "message" :  status_code.create_02_fail,
                }
            ),
            status = 500,
            mimetype = "application/json"
        )
        
'''
# 
# @login : db
#로그인
'''
@app.route('/login', methods=['POST'])
def login():
    
    try:
        token = login_module.login_modules(db)

        if token==1:
            return Response(
                    response=json.dumps(
                        {
                            "message":status_code.login_02_notmatch,
                        }
                    ),
                    status=200,
                    mimetype="application/json"
            )
        elif token==2:
            return Response(
                    response=json.dumps(
                        {
                             "message":status_code.login_03_fail,
                        }
                    ),
                    status=424,#이전 요청이 실패하였기 때문에 지금의 요청도 실패
                    mimetype="application/json"
            )
        elif token != None:
             return Response(
                    response=json.dumps(
                        {
                            "message":status_code.login_01_success,
                            "token" : token
                        }
                    ),
                    status=200,
                    mimetype="application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")
        return Response(
                    response=json.dumps(
                        {
                            "message":status_code.login_03_fail,
                        }
                    ),
                    status=500, #서버가 처리 방법을 모르는 상황이 발생했습니다. 서버는 아직 처리 방법을 알 수 없습니다.
                    mimetype="application/json"
            )
if __name__ == "__main__":
    app.run(port=80, debug=True)