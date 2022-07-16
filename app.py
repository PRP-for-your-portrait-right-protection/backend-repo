from flask import Flask, Response, request
import json
from static import status_code
from module import file_module,member_module, crud_module
from db import db_connection
app = Flask(__name__)

# DB 연결
db = db_connection.db_connection()

# 스키마 생성
# db_connection.init_collection(db)

####################################여러 사람 여러 사진#######################################
'''
# 여러 사람 여러 사진 버킷에 저장
# @form-data : user_id, file[], name[]
#
'''
@app.route('/people', methods=['POST'])
def upload_people():
    try:
        result = file_module.people_multiple_upload(db, "people")
        if result != False:
            return Response(
                response=json.dumps(result),
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

"""
# 여러 사람 여러 사진 url 가져오기
# @form-data : user_id
#
"""
@app.route('/people', methods = ["GET"])
def get_people():
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
        
####################################특정인물 사진 여러 개#######################################
'''
# 특정 인물 이름 수정 : 수정 필요
# @form-data : user_id, person_name, person_name_after
#
'''
@app.route('/person-all', methods = ["PATCH"])
def update_person_all():
    try:
        if crud_module.single_update(db):
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.fileupdate_01_success
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.fileupdate_02_fail
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
<<<<<<< Updated upstream
# 수정 전 비디오 파일 버킷에 저장
# @form-data : file, user_id
# 필요 없어서 삭제해야되면 삭제하기
=======
# 특정 인물에 대한 사진 모두 삭제하기
# @form-data : user_id, person_name
#
>>>>>>> Stashed changes
'''
@app.route('/person-all', methods = ["DELETE"])
def delete_person_all():
    try:
        if crud_module.multiple_delete(db, "people"):
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.filedelete_01_success
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.filedelete_02_fail
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")

####################################특정인물 사진 한 개#######################################        
'''
# 특정 인물 사진 한개 삭제하기 : 수정 필요
# @form-data : user_id, url        << url로 DB에서 person_url에 해당하는 값을 주면 됨
#
'''
@app.route('/person-single', methods = ["DELETE"])
def delete_person_single():
    try:
        if crud_module.single_delete(db, "people"):
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.filedelete_01_success
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.filedelete_02_fail
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")

####################################기존 케릭터#######################################
"""
# 기존 케릭터 사진 url 가져오기
# @form-data : 없음
# 
"""
@app.route('/origin-characters', methods = ["GET"])
def get_oringin_characters():
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
        
####################################케릭터 한개#######################################
'''
# 케릭터 한 개 버킷에 저장
# @form-data : user_id, file
#
'''
@app.route('/character', methods=['POST'])
def upload_character():
    try:
        result = file_module.single_upload(db, "upload_character")
        if result != False:
            return Response(
                response=json.dumps(result),
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
# 캐릭터 한 개 삭제
# @form-data : user_id, url
#
'''
@app.route('/character', methods = ["DELETE"])
def delete_character():
    try:
        if crud_module.single_delete(db, "character"):
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.filedelete_01_success
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.filedelete_02_fail
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")

####################################케릭터 여러개#######################################
'''
# 케릭터 여러 개 버킷에 저장
# @form-data : user_id, file[]
#
'''
@app.route('/characters', methods=['POST'])
def upload_characters():
    try:
        result = file_module.multiple_upload(db, "upload_character")
        if result != False:
            return Response(
                response=json.dumps(result),
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
        
"""
# 케릭터 여러 개 url 가져오기
# @form-data : user_id
<<<<<<< Updated upstream
# 수정할 필요 없음
=======
# 
>>>>>>> Stashed changes
"""
@app.route('/characters', methods = ["GET"])
def get_characters():
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
        
'''
# 특정 유저에 대한 캐릭터 모두 삭제하기 : 수정 필요
# @form-data : user_id
#
'''
@app.route('/characters', methods = ["DELETE"])
def delete_characters():
    try:
        if crud_module.multiple_delete(db, "characters"):
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.filedelete_01_success
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.filedelete_02_fail
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")

####################################수정 전 비디오#######################################
'''
# 수정 전 비디오 파일 버킷에 저장
# @form-data : user_id, file
#
'''
@app.route('/video-origin', methods=['POST'])
def upload_video_origin():
    try:
        result = file_module.single_upload(db, "video_origin")
        if result != False:
            return Response(
                response=json.dumps(result),
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

####################################수정 후 비디오#######################################
'''
# 수정 후 비디오 파일 버킷에 저장 후 링크 return
# @form-data : user_id, file
#
'''
@app.route('/video-modification', methods=['POST'])
def upload_video_modification():
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

"""
# 수정 후 비디오 파일 다운로드
# @form-data : user_id, filename
#
"""
@app.route('/video-modification', methods=['GET'])
def get_video_modification():
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
# 수정 후 비디오 파일 한 개 삭제하기 : 수정 필요
# @form-data : user_id, url
#
'''
@app.route('/video-modification', methods = ["DELETE"])
def delete_video_modification():
    try:
        if crud_module.single_delete(db, "video_modification"):
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.filedelete_01_success
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.filedelete_02_fail
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")

####################################수정 후 비디오 여러 개#######################################
'''
# 특정 유저에 대한 비디오 결과 모두 삭제하기 : 수정 필요
# @form-data : user_id
#
'''
@app.route('/video-modifications', methods = ["DELETE"])
def delete_video_modifications():
    try:
        if crud_module.multiple_delete(db, "video_modification"):
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.filedelete_01_success
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.filedelete_02_fail
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")
        
####################################AI에 전달 - 수정필요#######################################
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

####################################회원#######################################
'''
# 아이디 중복체크
# @form-data : user_id
#
'''
@app.route('/id-check', methods=['POST'])
def id_check():
    try:
        if member_module.id_duplicate_check(db):
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
# @form-data : user_id, password, name, phone
#
'''
@app.route('/signup', methods=['POST'])
def create_user():
    try:
        idReceive = member_module.create_users(db)
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
        token = member_module.login_modules(db)
        if token == 1:
            return Response(
                response=json.dumps(
                    {
                        "message":status_code.login_02_notmatch,
                    }
                ),
                status=200,
                mimetype="application/json"
            )
        elif token == 2:
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

'''
# 아이디 찾기
# @form-data : name, phone
#
'''
@app.route('/find-id', methods=['POST'])
def find_id():
    try:
        result = member_module.find_id(db)
        if result != None:
            return Response(
                response = json.dumps(result),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.find_id_02_fail
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
# 비밀번호 수정 전 정보 검증 : 수정 필요
# @form-data : user_id, phone
#
'''
@app.route('/check-info', methods=['POST'])
def check_info():
    try:
        if member_module.information_inspection(db):
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.find_password_01_success,
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {
                        "message" :status_code.find_password_02_fail
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
# 비밀번호 수정 : 수정 필요
# @form-data : user_id, phone, password
#
'''
@app.route('/password', methods=['PATCH'])
def password():
    try:
        result = member_module.update_password(db)
        if result != False:
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.find_password_01_success
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.find_password_02_fail
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")

if __name__ == "__main__":
    app.run(port=80, debug=True)