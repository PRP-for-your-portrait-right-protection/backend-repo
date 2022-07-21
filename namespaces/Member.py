from flask import Flask, Response, request
import json
from static import status_code
from module import file_module, member_module, crud_module
from flask_restx import Resource, Api, Namespace
from werkzeug.datastructures import FileStorage
from namespaces import People

####################################회원#######################################
Member = Namespace(
    name= "Member",
    description="OriginCharacter CRUD를 작성하기 위해 사용하는 API.",
)

parser = Member.parser()
parser.add_argument('user_id', location='form', required=False)
parser.add_argument('password', location='form', required=False)
parser.add_argument('name', location='form', required=False)
parser.add_argument('phone', location='form', required=False)

@Member.route('/id-check')
@Member.doc(response={200: 'SUCCESS'})
@Member.doc(response={404: 'Failed'})
class MemberIdCheck(Resource):
    @Member.expect(parser)
    def post(self):
        '''
        # 아이디 중복체크
        # @form-data : user_id
        # @return : message
        '''
        try:
            if member_module.id_duplicate_check():
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

@Member.route('/sign-up')
@Member.doc(response={200: 'SUCCESS'})
@Member.doc(response={404: 'Failed'})
class MemberSignUp(Resource):
    @Member.expect(parser)
    def post(self):
        '''
        # 회원가입
        # @form-data : user_id, password, name, phone
        # @return : message
        '''
        try:
            idReceive = member_module.create_users()
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

@Member.route('/login')
@Member.doc(response={200: 'SUCCESS'})
@Member.doc(response={404: 'Failed'})
class MemberLogin(Resource):
    @Member.expect(parser)
    def post(self):
        '''
        # 로그인
        # @form-data : user_id, password 
        # @return : message, token
        '''
        try:
            token = member_module.login_modules()
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

@Member.route('/id-find')
@Member.doc(responses={200: 'Success'})
@Member.doc(responses={404: 'Failed'})
class memberFindIdClass(Resource):
    @Member.expect(parser)
    def post(self):
        '''
        # 아이디 찾기
        # @form-data : name, phone
        # @return : {user_id : "user_id"}
        '''
        try:
            result = member_module.find_id()
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

@Member.route('/check-info')
@Member.doc(responses={200: 'Success'})
@Member.doc(responses={404: 'Failed'})
class memberInformationInspectionClass(Resource):
    @Member.expect(parser)
    def post(self):
        '''
        # 비밀번호 찾기 전 정보 검증
        # @form-data : user_id, phone
        # @return : message
        '''
        try:
            if member_module.information_inspection():
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

@Member.route('/find-password')
@Member.doc(responses={200: 'Success'})
@Member.doc(responses={404: 'Failed'})
class memberUpdatePasswordClass(Resource):
    @Member.expect(parser)
    def post(self):
        '''
        # 비밀번호 찾기(변경할 비밀번호 정보 받아와서 비밀번호 변경)
        # @form-data : user_id, phone, password
        # @return : message
        '''
        try:
            if member_module.update_password():
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

@Member.route('/delete')
@Member.doc(responses={200: 'Success'})
@Member.doc(responses={404: 'Failed'})
class memberDeleteClass(Resource):
    @Member.expect(parser)
    def post(self):
        '''
        # 회원탈퇴
        # @form-data : user_id
        # @return : message
        '''
        try:
            if member_module.delete_member():
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
