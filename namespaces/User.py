from flask import Response
import json
from module import user_module
from flask_restx import Resource, Namespace

####################################회원#######################################
Users = Namespace(
    name= "Users",
    description="Users CRUD를 작성하기 위해 사용하는 API.",
)

parser = Users.parser()
parser.add_argument('email', location='form', required=False)
parser.add_argument('password', location='form', required=False)
parser.add_argument('name', location='form', required=False)
parser.add_argument('phone', location='form', required=False)


@Users.route('/email/validation')
@Users.expect(parser)
@Users.doc(response={200: 'SUCCESS'})
@Users.doc(response={404: 'Failed'})
class UserEmailValidaionClass(Resource):

    def post(self):
        """
        # 아이디 중복체크
        # @form-data : email
        # @return : 200 or 409
        """
        try:
            result, message = user_module.email_validation()
            return Response(
                response = json.dumps(message),
                status = result,
                mimetype = "application/json"
                )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************") 

@Users.route('')
@Users.expect(parser)
@Users.doc(response={200: 'SUCCESS'})
@Users.doc(response={404: 'Failed'})
class UsersClass(Resource):

    def post(self):
        """
        # 회원가입
        # @form-data : email, password, name, phone
        # @return : 200 or 404
        """
        try:
            result, message = user_module.create_users()
            return Response(
                response = json.dumps(message), ##회원가입 성공일때는 status를 201로 받아 나머지는 다 200
                status = result,
                mimetype = "application/json"
            )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")

@Users.route('/email')
@Users.expect(parser)
@Users.doc(responses={200: 'Success'})
@Users.doc(responses={404: 'Failed'})
class UserEmailClass(Resource):

    def post(self):
        """
        # 아이디 찾기
        # @form-data : name, phone
        # @return : {email: "email"}
        """
        try:
            result, message = user_module.find_email()
            return Response(
                response = json.dumps(message),
                status = result,
                mimetype = "application/json"
            )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")

@Users.route('/password/validation')
@Users.expect(parser)
@Users.doc(responses={200: 'Success'})
@Users.doc(responses={404: 'Failed'})
class UserPasswordValidationClass(Resource):
  
    def post(self):
        """
        # 비밀번호 찾기 전 정보 검증
        # @form-data : email, phone
        # @return : message
        """
        try:
            result, message = user_module.password_validation()
            return Response(
                response = json.dumps(message),
                status = result,
                mimetype = "application/json"
            )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")

@Users.route('/password')
@Users.expect(parser)
@Users.doc(responses={200: 'Success'})
@Users.doc(responses={404: 'Failed'})
class UserUpdatePasswordClass(Resource):

    def patch(self):
        """
        # 비밀번호 변경(변경할 비밀번호 정보 받아와서 비밀번호 변경)
        # @form-data : email, phone, password
        # @return : message
        """
        try:
            result, message = user_module.update_password()
            return Response(
                response = json.dumps(message),
                status = result,
                mimetype = "application/json"
            )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")

Auth = Namespace(
    name= "Auth",
    description="User의 Auth를 작성하기 위해 사용하는 API.",
)

parser = Auth.parser()
parser.add_argument('email', location='form')
parser.add_argument('password', location='form')

@Auth.route('')
@Auth.expect(parser)
@Auth.doc(response={200: 'SUCCESS'})
@Auth.doc(response={404: 'Failed'})
class AuthClass(Resource):
   
    def post(self):
        """
        # 로그인
        # @form-data : email, password 
        # @return : {"token": "token", "user_name": "user_name"}
        """
        try:
            result, message = user_module.login()
            return Response(
                response = json.dumps(message),
                status = result,
                mimetype = "application/json"
            )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
