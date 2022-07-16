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
# @return : {file : [file_url, file_url, file_url]}
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
                        "message":status_code.file_download_02_fail,
                    }
                ),
                status=404,
                mimetype="application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")

"""
# 여러 사람 여러 사진 url 가져오기
# @form-data : user_id
# @return : 
#   {
#       person_name : [
#           file_url, file_url, file_url
#       ], 
#       person_name : [
#           file_url, file_url, file_url
#       ]
#   }
"""
@app.route('/people', methods = ["GET"])
def get_people():
    try:
        result = crud_module.multiple_get(db, "get_people")
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
                        "message":status_code.file_download_02_fail
                    }
                ),
                status=404,
                mimetype="application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")
        
####################################특정인물 사진 여러 개#######################################
'''
# 특정 인물 이름 수정
# @form-data : user_id, person_name, person_name_after
# @return : message
'''
@app.route('/person-all', methods = ["PATCH"])
def update_person_all():
    try:
        if crud_module.single_update(db):
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.file_update_01_success
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.file_update_02_fail
                    }
                ),
                status = 404,
                mimetype = "application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")
        
'''
# 특정 인물에 대한 사진 모두 삭제하기
# @form-data : user_id, person_name
# @return : message
'''
@app.route('/person-all', methods = ["DELETE"])
def delete_person_all():
    try:
        if crud_module.multiple_delete(db, "people"):
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.file_remove_01_success
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.file_remove_02_fail
                    }
                ),
                status = 404,
                mimetype = "application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")

####################################특정인물 사진 한 개#######################################        
'''
# 특정 인물 사진 한개 삭제하기
# @form-data : user_id, url  << url로 DB에서 person_url에 해당하는 값을 주면 됨
# @return : message
'''
@app.route('/person-single', methods = ["DELETE"])
def delete_person_single():
    try:
        if crud_module.single_delete(db, "people"):
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.file_remove_01_success
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.file_remove_02_fail
                    }
                ),
                status = 404,
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
# @return : {file : [file_url, file_url, file_url]}
"""
@app.route('/origin-characters', methods = ["GET"])
def get_oringin_characters():
    try:
        result = crud_module.single_get(db, "get_origin_character")
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
                        "message":status_code.file_download_02_fail,
                    }
                ),
                status=404,
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
# @return : {file : file_url}
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
                        "message":status_code.file_save_02_fail,
                    }
                ),
                status=404,
                mimetype="application/json"
            )
    except Exception as ex:
            print("******************")
            print(ex)
            print("******************")

'''
# 캐릭터 한 개 삭제
# @form-data : user_id, url
# @return : message
'''
@app.route('/character', methods = ["DELETE"])
def delete_character():
    try:
        if crud_module.single_delete(db, "character"):
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.file_remove_01_success
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.file_remove_02_fail
                    }
                ),
                status = 404,
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
# @return : {file : [file_url, file_url, file_url]}
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
                        "message":status_code.file_save_02_fail,
                    }
                ),
                status=404,
                mimetype="application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")
        
"""
# 케릭터 여러 개 url 가져오기
# @form-data : user_id
# @return : {file : [file_url, file_url, file_url]}
"""
@app.route('/characters', methods = ["GET"])
def get_characters():
    try:
        result = crud_module.single_get(db, "get_character")
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
                        "message":status_code.file_download_02_fail,
                    }
                ),
                status=404,
                mimetype="application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")
        
'''
# 특정 유저에 대한 캐릭터 모두 삭제하기
# @form-data : user_id
# @return : message
'''
@app.route('/characters', methods = ["DELETE"])
def delete_characters():
    try:
        if crud_module.multiple_delete(db, "characters"):
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.file_remove_01_success
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.file_remove_02_fail
                    }
                ),
                status = 404,
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
# @return : {file : file_url}
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
                        "message":status_code.file_save_02_fail,
                    }
                ),
                status=404,
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
# @return : {file : file_url}
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
                        "message":status_code.file_save_02_fail,
                    }
                ),
                status=404,
                mimetype="application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")

"""
# 수정 후 비디오 파일 다운로드 : 자동 다운로드
# @form-data : user_id, filename
# @return : message
"""
@app.route('/video-modification', methods=['GET'])
def get_video_modification():
    try:
        if file_module.single_download(db, "video_modification") :
            return Response(
                response=json.dumps(
                    {
                        "message":status_code.file_download_01_success,
                    }
                ),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps(
                    {
                        "message":status_code.file_download_02_fail,
                    }
                ),
                status=404,
                mimetype="application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")
        
'''
# 수정 후 비디오 파일 한 개 삭제하기
# @form-data : user_id, url
# @retutrn : message
'''
@app.route('/video-modification', methods = ["DELETE"])
def delete_video_modification():
    try:
        if crud_module.single_delete(db, "video_modification"):
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.file_remove_01_success
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.file_remove_02_fail
                    }
                ),
                status = 404,
                mimetype = "application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")

####################################수정 후 비디오 여러 개#######################################
'''
# 특정 유저에 대한 비디오 결과 모두 조회하기
# @form-data : user_id
# @return : {file : [file_url, file_url, file_url]}
'''
@app.route('/video-modifications', methods = ["GET"])
def get_video_modifications():
    try:
        result = crud_module.single_get(db, "get_video_modification")
        if result != False:
            return Response(
                response = json.dumps(result),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.file_remove_02_fail
                    }
                ),
                status = 404,
                mimetype = "application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")
        
'''
# 특정 유저에 대한 비디오 결과 모두 삭제하기
# @form-data : user_id
# @return : message
'''
@app.route('/video-modifications', methods = ["DELETE"])
def delete_video_modifications():
    try:
        if crud_module.multiple_delete(db, "video_modification"):
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.file_remove_01_success
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.file_remove_02_fail
                    }
                ),
                status = 404,
                mimetype = "application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")
        
####################################AI에 전달 - AI 함수로 전달하는 부분 수정필요#######################################
'''
# AI에 파일 링크 한 번에 던지기 : 원본 파일명, 케릭터 파일명, 모자이크 안 할 대상들 파일명
# @form-data : user_id, files[], video, mode_method, character_new_YN(선택), file(선택)
# @return : AI 함수
'''
@app.route('/ai', methods=['POST'])
def ai():
    try:
        # 1. ai에 전송할 json 생성
        col_json = {}
        
        # 2. json에 추가
        # 2-1. 모자이크 제외할 사람 얼굴 사진 링크
        col_json["file"] = []
        fs = request.files.getlist("files")
        for f in fs:
            col_json["file"].append(f)
        
        # 2-2. user_id
        user_id = request.form["user_id"]
        col_json["user_id"] = user_id
        
        # 2-3. video
        video = request.form["video"]
        col_json["video"] = video
        
        # 3. 모자이크화 할 것인지 케릭터화 할 것인지 확인
        mode_method = request.form["mode_method"]
        
        # 3-1. 모자이크
        if mode_method == "mosaic":
            # 모자이크 기능 함수로 json 보냄 > ai 함수에서 수정완료 > '수정 후 비디오 저장 API'로 라우팅
            return col_json
        
        # 3-2. 케릭터화
        elif mode_method == "character ":
            # 케릭터 사진이 새로운 사진인지 검사
            character_new_YN = request.form["character_new_YN"]
            
            # 새로운 사진
            if character_new_YN == "Y":
                # 새로운 사진 파일 버킷과 db에 저장 후 url 받아옴
                character_file = file_module.single_upload(db, "upload_character")
                col_json["character_file"] = character_file
                return col_json
            # 존재하던 사진
            elif character_new_YN == "N":
                # 존재하던 사진 url 받아와서 json에 추가
                character_file = request.form["file"]
                col_json["character_file"] = character_file
                return col_json
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")

####################################회원#######################################
'''
# 아이디 중복체크
# @form-data : user_id
# @return : message
'''
@app.route('/id-check', methods=['POST'])
def id_check():
    try:
        if member_module.id_duplicate_check(db):
            return Response(
                response = json.dumps(
                    {
                        "result" : status_code.member_id_check_01_success,
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.member_id_check_02_fail
                    }
                ),
                status = 404,
                mimetype = "application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")

'''
# 회원가입
# @form-data : user_id, password, name, phone
# @return : message
'''
@app.route('/signup', methods=['POST'])
def create_user():
    try:
        idReceive = member_module.create_users(db)
        if idReceive != None:
            return Response(
                response = json.dumps(
                    {
                        "result" : status_code.member_signup_01_success,
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
                        "message" : status_code.member_signup_02_fail
                    }
                ),
                status = 404,
                mimetype = "application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")

'''
# 로그인
# @form-data : user_id, password
# @return : message, token
'''
@app.route('/login', methods=['POST'])
def login():
    try:
        token = member_module.login_modules(db)
        if token == 1:
            return Response(
                response=json.dumps(
                    {
                        "message":status_code.member_login_02_notmatch,
                    }
                ),
                status=404,
                mimetype="application/json"
            )
        elif token == 2:
            return Response(
                response=json.dumps(
                    {
                        "message":status_code.member_login_03_fail,
                    }
                ),
                status=424, #이전 요청이 실패하였기 때문에 지금의 요청도 실패
                mimetype="application/json"
            )
        elif token != None:
             return Response(
                response=json.dumps(
                    {
                        "message":status_code.member_login_01_success,
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
# @return : {user_id : "user_id"}
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
                        "message" : status_code.member_find_id_02_fail
                    }
                ),
                status = 404,
                mimetype = "application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")

'''
# 비밀번호 찾기 전 정보 검증
# @form-data : user_id, phone
# @return : message
'''
@app.route('/check-info', methods=['POST'])
def check_info():
    try:
        if member_module.information_inspection(db):
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.member_find_password_01_success,
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {
                        "message" :status_code.member_find_password_02_fail
                    }
                ),
                status = 404,
                mimetype = "application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")

'''
# 비밀번호 찾기(변경할 비밀번호 정보 받아와서 비밀번호 변경)
# @form-data : user_id, phone, password
# @return : message
'''
@app.route('/password', methods=['PATCH'])
def password():
    try:
        if member_module.update_password(db):
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.member_replace_password_01_success
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.member_replace_password_02_fail
                    }
                ),
                status = 404,
                mimetype = "application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")

'''
# 회원탈퇴
# @form-data : user_id
# @return : message
'''
@app.route('/member', methods=['DELETE'])
def delete_member():
    try:
        if member_module.delete_member(db):
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.member_delete_01_success
                    }
                ),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {
                        "message" : status_code.member_delete_01_fail
                    }
                ),
                status = 404,
                mimetype = "application/json"
            )
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")
        
if __name__ == "__main__":
    app.run(port=80, debug=True)
