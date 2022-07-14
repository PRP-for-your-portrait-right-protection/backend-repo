from datetime import datetime, timedelta
import hashlib
import jwt
from flask import request,Response,jsonify
import json

"""회원가입"""



def create_users(db):
    idReceive = request.form["id"]
    pwReceive = request.form["password"]
    nameReceive = request.form["name"]
    pwHash = hashlib.sha256(pwReceive.encode('utf-8')).hexdigest()
    now = datetime.now()
   
    try:

        user = {
            "userId" : idReceive,
            "password" : pwHash,
            "name" : nameReceive,
            "date" : now.strftime('%Y-%m-%d %H:%M:%S'),
            "updateDate" : ""
            }

        db.member.insert_one(user)
    
        return idReceive
    except Exception as ex:
        print(ex)
        return None
    
 
 
"""로그인"""

def login_modules(db):
    idReceive = request.form["id"]
    pwReceive = request.form["password"]

    pwHash = hashlib.sha256(pwReceive.encode("utf-8")).hexdigest()

    try:
        findUser = db.member.find_one({
            "userId" : idReceive,
            "password" : pwHash
            })
        if findUser is not None:
            payload = {
                "userId" : idReceive,
                "exp" : datetime.utcnow() + timedelta(seconds = 3600) 
            }

            SECRET_KEY = "soohyun"

            token = jwt.encode(payload, SECRET_KEY, algorithm = 'HS256')
            #SECRETKEY 설정필요
            return token
            
        else:
           return 1
       
    except Exception as ex:
        print(ex)
        return 2
       

