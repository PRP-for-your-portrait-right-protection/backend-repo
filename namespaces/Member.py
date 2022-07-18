from flask import Flask, Response, request
import json
from static import status_code
from module import file_module, member_module, crud_module
from db import db_connection
from flask_restx import Resource, Api, Namespace
from werkzeug.datastructures import FileStorage
from namespaces import People

db = db_connection.db_connection()

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