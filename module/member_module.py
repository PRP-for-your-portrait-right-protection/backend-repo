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
        findUser = db.member.find_one({"user_id" : idReceive})
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
            "user_id" : idReceive,
            "password" : pwHash,
            "name" : request.form["name"],
            "phone" : request.form["phone"],
            "reg_date" : now.strftime('%Y-%m-%d %H:%M:%S'),
            "mod_date" : ""
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
            "user_id" : idReceive,
            "password" : pwHash
            }
        )
        if findUser is not None:
            payload = {
                "user_id" : idReceive,
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

"""
* 아이디 찾기
"""
def find_id(db):
    try:
        findUser = db.member.find_one(
            {
                "name" : request.form["name"],
                "phone" : request.form["phone"]
            },
            {"user_id":1, "_id":0}
        )
        if findUser == None:
            return False
        else:
            return findUser
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False
    

'''
* 정보검사 핸드폰번호와 아이디가 맞는 지 확인한다.
'''

def information_inspection(db):
    try:
        idReceive = request.form["user_id"]
        phoneNum=request.form["phone"]
        
        findUser = db.member.find_one(
            {"$and":[{"user_id":idReceive}, {"phone":phoneNum}]}  
         ) 
        print(findUser)
        if findUser == None:   
            return False
        else:
            return True

    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False

'''
*수정날짜와 바뀐 비밀 번호 업데이트 
'''

def find_password(db):
  
    try:

        idReceive = request.form["user_id"]
        phoneNum=request.form["phone"]

        now = datetime.now()
        pwReceive = request.form["password"]
        pwHash = hashlib.sha256(pwReceive.encode('utf-8')).hexdigest()
    
        result = db.member.update_many(
        {      
            "user_id" : idReceive, 
            "phone": phoneNum
        }, 
        {"$set" : 
            {
                "password" :  pwHash, 
                "mod_date" : now.strftime('%Y-%m-%d %H:%M:%S')
            }
        })

        return True

    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False
    