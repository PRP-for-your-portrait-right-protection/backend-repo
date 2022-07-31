from flask import request
import hashlib
from datetime import datetime
from module.token import create_token
from module.db_module import create_whitelist_face
from static import status_code
from db import schema

"""
* 이메일 중복체크
"""
def email_validation():
    try:
        email = request.form.get('email')
        if email == None or email == '':
            return False, {"error": f'{status_code.field_error}email'}
        user = schema.User.objects(email = email)
        if user.count() != 0:
            print("This email is already exist")
            return False, {"error": status_code.user_email_validation_03_already}
        else:
           return True, {"message": status_code.user_email_validation_01_success}
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False, {"error": str(ex)}
       
"""
* 회원가입
"""
def create_users():
    try:
        email = request.form.get('email')
        if email == None or email == '':
            return False, {"error": f'{status_code.field_error}email'}
        password = request.form.get('password')
        if password == None or password == '':
            return False, {"error": f'{status_code.field_error}password'}
        name = request.form.get('name')
        if name == None or name == '':
            return False, {"error": f'{status_code.field_error}name'}
        phone = request.form.get('phone')
        if phone == None or phone == '':
            return False, {"error": f'{status_code.field_error}phone'}
        
        pwHash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        user = schema.User(email, pwHash, name, phone, False, datetime.now())
        result = schema.User.objects().insert(user)
        result, message = create_whitelist_face(result._id, name)
        if result == False:
            return result, message
        return True, {"id": user.email}
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False, {"error": str(ex)}
    
"""
* 로그인
"""
def login():
    try:
        email = request.form.get('email')
        if email == None or email == '':
            return False, {"error": f'{status_code.field_error}email'}
        password = request.form.get('password')
        if password == None or password == '':
            return False, {"error": f'{status_code.field_error}password'}

        pwHash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        user = schema.User.objects(email = email, password = pwHash)
        if user.count() == 0:
            return False, {"error": "Can't find user"}
        userId = str(user.first().get_id())
        result, token = create_token(userId)
        if result == False:
            return result, token
        else:
            return True, {"token": token, "email": user.first().email}
    except Exception as ex:
        print('*********')
        print("???????????")
        print(ex)
        print('*********')
        return False, {"error": str(ex)}

"""
* 이메일 찾기
"""
def find_email():
    try:
        name = request.form.get('name')
        if name == None or name == '':
            return False, {"error": f'{status_code.field_error}name'}
        phone = request.form.get('phone')
        if phone == None or phone == '':
            return False, {"error": f'{status_code.field_error}phone'}

        user = schema.User.objects(name = name, phone = phone).first()
        if user == None:
            print("Can't find user")
            return False, {"error": status_code.user_email_find_02_fail}
        else:
            return True, {"email": user.email}
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False, {"error": str(ex)}
    
'''
* 비밀번호 찾기 전 확인
'''
def password_validation():
    try:
        email = request.form.get('email')
        if email == None or email == '':
            return False, {"error": f'{status_code.field_error}email'}
        phone = request.form.get('phone')
        if phone == None or phone == '':
            return False, {"error": f'{status_code.field_error}phone'}
        
        user = schema.User.objects(email = email, phone = phone).first()
        if user == None:
            print("Can't find user")  
            return False, {"error": "Can't find user"}
        else:
            return True, {"message": status_code.user_password_validation_01_success}
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False, {"error": str(ex)}

'''
* 비밀 번호 변경
'''
def update_password():
    try:
        email = request.form.get('email')
        if email == None or email == '':
            return False, {"error": f'{status_code.field_error}email'}
        password = request.form.get('password')
        if password == None or password == '':
            return False, {"error": f'{status_code.field_error}password'}
        phone = request.form.get('phone')
        if phone == None or phone == '':
            return False, {"error": f'{status_code.field_error}phone'}
        
        pwHash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        dbResponse = schema.User.objects(email = email, phone = phone).update(set__password = pwHash, set__updated_at = datetime.now())
        if dbResponse > 0:
            return True, {"message": status_code.user_password_replace_01_success}
        else:
            print("Can't be modified")
            return False, {"error": status_code.user_password_replace_02_fail}
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False, {"error": str(ex)}

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
