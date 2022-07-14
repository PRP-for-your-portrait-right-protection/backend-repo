from datetime import datetime, timedelta
import hashlib
import jwt
from flask import request
from module.module_config import SECRET_KEY, TOKEN_EXPIRED

"""
* 아이디 중복체크
"""
def id_duplicate_check(db):
    idReceive = request.form["user_id"]
    try:
        findUser = db.member.find_one({"userId" : idReceive})
        if findUser is not None:
            return False
        else:
           return True
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return 2
       
"""
* 회원가입
"""
def create_users(db):
    idReceive = request.form["user_id"]
    pwReceive = request.form["password"]
    pwHash = hashlib.sha256(pwReceive.encode('utf-8')).hexdigest()
    now = datetime.now()
    try:
        user = {
            "userId" : idReceive,
            "password" : pwHash,
            "name" : request.form["name"],
            "date" : now.strftime('%Y-%m-%d %H:%M:%S'),
            "updateDate" : ""
        }
        db.member.insert_one(user)
        return idReceive
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False
    
"""
* 로그인
"""
def login_modules(db):
    idReceive = request.form["user_id"]
    pwReceive = request.form["password"]
    pwHash = hashlib.sha256(pwReceive.encode("utf-8")).hexdigest()
    try:
        findUser = db.member.find_one(
            {
            "userId" : idReceive,
            "password" : pwHash
            }
        )
        if findUser is not None:
            payload = {
                "userId" : idReceive,
                "exp" : datetime.utcnow() + timedelta(seconds = TOKEN_EXPIRED) 
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm = 'HS256')
            return token
        else:
           return 1
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return 2
       