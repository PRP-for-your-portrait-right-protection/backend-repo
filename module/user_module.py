from flask import request
import hashlib
from datetime import datetime
from module.token import create_token
from module.db_module import create_whitelist_face
from db import schema

"""
* 이메일 중복체크
"""
def email_validation():
    try:
        email = request.form["email"]
        
        user = schema.User.objects(email = email)
        if user.count() != 0:
            print("This email is already exist")
            return False
        else:
           return True
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
       
"""
* 회원가입
"""
def create_users():
    email = request.form["email"]
    password = request.form["password"]
    name = request.form["name"]
    phone = request.form["phone"]
    
    pwHash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    try:
        user = schema.User(email, pwHash, name, phone, False, datetime.now())
        result = schema.User.objects().insert(user)
        create_whitelist_face(result._id, name)
        return user.email
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False
    
"""
* 로그인
"""
def login():
    email = request.form["email"]
    password = request.form["password"]

    pwHash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    try:
        userId = str(schema.User.objects(email = email, password = pwHash).first().get_id())
        token = create_token(userId)
        return token    
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return 2

"""
* 이메일 찾기
"""
def find_email():
    try:
        name = request.form["name"]
        phone = request.form["phone"]

        user = schema.User.objects(name = name, phone = phone).first()
        if user == None:
            print("Can't find user")
            return False
        else:
            return user.email
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False
    
'''
* 비밀번호 찾기 전 확인
'''
def password_validation():
    try:
        email = request.form["email"]
        phone = request.form["phone"]
        
        user = schema.User.objects(email = email, phone = phone).first()
        if user == None:
            print("Can't find user")  
            return False
        else:
            return True
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False

'''
* 비밀 번호 변경
'''
def update_password():
    try:
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        pwHash = hashlib.sha256(password.encode('utf-8')).hexdigest()

        dbResponse = schema.User.objects(email = email, phone = phone).update(set__password = pwHash, set__updated_at = datetime.now())

        if dbResponse > 0:
            return True
        else:
            print("Can't be modified")
            return False
        
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False

'''
* 회원탈퇴
'''
# def delete_member(user_id):
#     try:
        
#         # user_id는 token
#         idReceive = get_id(user_id)

#         # 2. DB에서 유저아이디 일치하는 Document -> activation_YN = N
#         dbResponse = schema.UploadCharacter.objects(user_id = idReceive).update(set__activation_YN = "N", set__mod_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

#         if dbResponse.modified_count > 0:
#             return True
#         else:
#             print("Can't be modified")
#             return False

#     except Exception as ex:
#         print('*********')
#         print(ex)
#         print('*********')
#         return False
