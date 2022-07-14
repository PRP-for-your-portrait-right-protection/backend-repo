from flask import Flask, Response, request
import json
from static import status_code
from module import file_module,login_module
from db import db_connection
app = Flask(__name__)

# DB 연결
db = db_connection.db_connection()

# 스키마 생성
#db_connection.init_collection(db)

'''
# 다인 다중 사람 사진 버킷에 저장
# @form-data : file, user_id, person_name
#
'''
@app.route('/person', methods=['POST'])
def uploadPerson():
    try:
        if file_module.multiple_upload(db, "people"):
            return Response(
                response=json.dumps(
                    {
                        "message":status_code.fileupload_01_success,
                    }
                ),
                status=200,
                mimetype="application/json"
            )
        else:
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
# 일인 한 개 케릭터 사진 버킷에 저장
# @form-data : file, user_id
#
'''
@app.route('/character', methods=['POST'])
def uploadCharacter():
    try:
        if file_module.single_upload(db, "upload_character"):
            return Response(
                response=json.dumps(
                    {
                        "message":status_code.fileupload_01_success,
                    }
                ),
                status=200,
                mimetype="application/json"
            )
        else:
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
# 일인 다중 케릭터 사진 버킷에 저장
# @form-data : file, user_id
#
'''
@app.route('/characters', methods=['POST'])
def uploadCharacters():
    try:
        if file_module.multiple_upload(db, "upload_character"):
            return Response(
                response=json.dumps(
                    {
                        "message":status_code.fileupload_01_success,
                    }
                ),
                status=200,
                mimetype="application/json"
            )
        else:
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
# 수정 전 비디오 파일 버킷에 저장
# @form-data : file, user_id
#
'''
@app.route('/video-origin', methods=['POST'])
def oringinVideo():
    try:
        if file_module.single_upload(db, "video_origin"):
            return Response(
                response=json.dumps(
                    {
                        "message":status_code.fileupload_01_success,
                    }
                ),
                status=200,
                mimetype="application/json"
            )
        else:
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
# 수정 후 비디오 파일 버킷에 저장 후 링크 return
# @form-data : file, user_id
#
'''
@app.route('/video-modification', methods=['POST'])
def modificationVideo():
    try:
        result = file_module.single_upload(db, "video_modification")
        if result != False:
            return Response(
                response = json.dumps(result),
                status=200,
                mimetype="application/json"
            )
        else:
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
# AI에 파일 링크 한 번에 던지기 : 원본 파일명, 케릭터 파일명, 모자이크 안 할 대상들 파일명
# @form-data : origin_video_name, mod_method, user_id
# 
'''
@app.route('/ai', methods=['POST'])
def ai():
    try:
        result = file_module.multiple_get(db, "get_people")
        if result != False:
            result["origin_video_name"] = request.form["origin_video_name"]
            result["mod_method"] = request.form["mod_method"]
            return Response(
                response = json.dumps(result),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response=json.dumps(
                    {
                        "message":status_code.filedownload_02_fail
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
# 단일 파일 다운로드
# @form-data : user_id
#
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

"""
# 기존 케릭터 사진 url 가져오기
# @form-data : 없음
# 
"""
@app.route('/origin-characters', methods = ["GET"])
def oringinCharacterDownload():
    try:
        result = file_module.single_get(db, "get_origin_character")
        if result != False:
            return Response(
                response = json.dumps(result),
                status = 200,
                mimetype = "application/json"
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

"""
# 일인 다중 케릭터 사진 url 가져오기
# @form-data : user_id
# 
"""
@app.route('/characters', methods = ["GET"])
def characterDownload():
    try:
        result = file_module.single_get(db, "get_character")
        if result != False:
            return Response(
                response = json.dumps(result),
                status = 200,
                mimetype = "application/json"
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
        
"""
# 다인 다중 사람 사진 url 가져오기
# @form-data : user_id
#
"""
@app.route('/people', methods = ["GET"])
def peopleDownload():
    try:
        result = file_module.multiple_get(db, "get_people")
        if result != False:
            return Response(
                response = json.dumps(result),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response=json.dumps(
                    {
                        "message":status_code.filedownload_02_fail
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
# 아이디 중복체크
# @form-data : user_id
#
'''
@app.route('/id-check', methods=['POST'])
def id_check():
    try:
        if login_module.id_duplicate_check(db):
            return Response(
                response = json.dumps(
                {
                    "result" : status_code.id_check_01_success,
                }
            ),
            status = 200,
            mimetype = "application/json"
        )
        else:
            return Response(
                response = json.dumps(
                {
                    "message" : status_code.id_check_02_fail
                }
            ),
            status = 200,
            mimetype = "application/json"
        )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")
        
'''
# 회원가입
# @form-data : user_id, password, name
#
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

'''
# 로그인
# @form-data : user_id, password
# 
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
                status=424, #이전 요청이 실패하였기 때문에 지금의 요청도 실패
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

if __name__ == "__main__":
    app.run(port=80, debug=True)