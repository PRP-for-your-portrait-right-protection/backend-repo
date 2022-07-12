from flask import Flask, Response, request
import json
from static import status_code
from module import file_module
from db import db_connection
app = Flask(__name__)

# DB 연결
db = db_connection.db_connection()

# 스키마 생성
# db_connection.init_collection(db)

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
* 단일 파일 다운로드
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


if __name__ == "__main__":
    app.run(port=80, debug=True)