from flask import request
import jwt
import hashlib
from datetime import datetime, timedelta
from module.module_config import SECRET_KEY, TOKEN_EXPIRED

"""
* 아이디 중복체크
"""
def id_duplicate_check(db):
    idReceive = request.form["user_id"]
    try:
        findUser = db.member.find_one({"user_id" : idReceive})
        if findUser != None:
            print("Can't find user")
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
    name = request.form["name"]
    phone = request.form["phone"]
    
    pwHash = hashlib.sha256(pwReceive.encode('utf-8')).hexdigest()
    now = datetime.now()
    try:
        user = {
            "user_id" : idReceive,
            "password" : pwHash,
            "name" : name,
            "phone" : phone,
            "activation_YN" : "Y",
            "reg_date" : now.strftime('%Y-%m-%d %H:%M:%S'),
            "mod_date" : ""
        }
        #여기에서 dbResponse
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
        if findUser != None:
            payload = {
                "user_id" : idReceive,
                "exp" : datetime.utcnow() + timedelta(seconds = TOKEN_EXPIRED) 
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm = 'HS256')

            if token == None:
                print("Error occurred")
                return 2

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
    try: #변수형식으로 바꿔도 상관x
        name = request.form["name"]
        phone = request.form["phone"]

        findUser = db.member.find_one(
            {
                "name" : name,
                "phone" : phone
            },
            {
                "user_id":1, 
                "_id":0
            }
        )
        if findUser == None:
            print("Can't find user")
            return False
        else:
            return findUser
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False
    
'''
* 비밀번호 찾기 전 확인
'''
def information_inspection(db):
    try:
        idReceive = request.form["user_id"]
        phone = request.form["phone"]
        
        findUser = db.member.find_one(
            {"$and":[{"user_id":idReceive}, {"phone": phone}]}  
         ) 
        if findUser == None: 
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
def update_password(db):
    try:
        idReceive = request.form["user_id"]
        phone = request.form["phone"]
        pwReceive = request.form["password"]

        now = datetime.now()
        pwHash = hashlib.sha256(pwReceive.encode('utf-8')).hexdigest()
    
        dbResponse = db.member.update_many(
        {      
            "user_id" : idReceive, 
            "phone": phone
        }, 
        {
            "$set" : 
            {
                "password" :  pwHash, 
                "mod_date" : now.strftime('%Y-%m-%d %H:%M:%S')
            }
        })

        if dbResponse.modified_count != 0:
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
def delete_member(db):
    try:
        # 1. 유저 아이디와 url 가져옴
        userId = request.form["user_id"]

        # 2. DB에서 유저아이디 일치하는 Document -> activation_YN = N
        dbResponse = db.member.update_one(
            {
                "user_id" : userId
            }, 
            {
                "$set" : 
                    {
                        "activation_YN" : "N",
                        "mod_date" : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
            }
        )

        if dbResponse.modified_count != 0:
            return True
        else:
            print("Can't be modified")
            return False

    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False

"""
* 토큰 유효성 검사
* 로그인 유효성 검사가 필요한 함수 위에 @login_required를 넣으면 됨
*   예시)    @app.route('/action', methods = ["POST"])
*            @login_required
*            def sample_action():
*                ###
*                ###
*                return Response()
* 수정이 필요할 수 있음
* 페이지를 넘길 때 유효성 검사를 하려면 어떻게 해야..
* 토큰이 만료된 경우 처음화면으로 돌아가게 할 수 있나?
* app.py에 적용 필요함
"""
def decode_token(my_token): # 매개 변수로 토큰을 받아옴
    try:
        # 1. payload 변수에 jwt토큰을 decode
        payload = jwt.decode(my_token, SECRET_KEY, algorithms = "HS256")

        # 2. 토큰이 만료된 경우
        if payload['exp'] < datetime.utcnow():
            payload = None  

    # 3. 부적절한 토큰인 경우 예외 발생 
    except jwt.InvalidTokenError:
        print("Invalid token")
        payload = None
        return payload
    else:
        return payload

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwagrs):
        # 1. 토큰을 가져옴
        # 추후에 가져오는 방법이 바뀔 수 있음
        # 프론트에서 JWT토큰을 헤더에 넣어 'my_token' 키로 전달
        my_token = request.headers.get("my_token")

        # 2-1. 토큰을 가져오면
        if my_token != None:
            payload = decode_token(my_token)
            # 토큰 Decode가 실패하면
            if payload == None:
                print("Can't decode token")
                return False
        # 2-2. 토큰 가져오는 것을 실패하면
        else:
            print("Can't find token")
            return False
        return f(*args, **kwagrs)
    return decorated_function

"""
* 토큰으로부터 user_id 얻기
* 수정이 필요할 수 있음
* app.py에 적용 필요함
"""
def get_id():
    try:
        # 1. 토큰을 가져옴
        # 추후에 가져오는 방법이 바뀔 수 있음
        # 프론트에서 JWT토큰을 헤더에 넣어 'my_token' 키로 전달
        my_token = request.headers.get("my_token")

        # 2. JWT 토큰을 Decode
        payload = jwt.decode(my_token, SECRET_KEY, algorithms = "HS256")

        # 3. 토큰이 만료된 경우
        if payload['exp'] < datetime.utcnow():
            payload = None
    # 4. 부적절한 토큰인 경우 예외 발생 
    except jwt.InvalidTokenError:
        print("Invalid token")
        payload = None
        return payload

    try:
        if payload != None:
            user_id = payload['user_id']
            return user_id
        else:
            return False
    except Exception as ex:
        print("***********")
        print(ex)
        print("***********")
