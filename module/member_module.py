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
        # payload 변수에 jwt토큰을 decode
        payload = jwt.decode(my_token, SECRET_KEY, algorithms = "HS256")

        # 토큰이 만료된 경우
        if payload['exp'] < datetime.utcnow():
            payload = None  

    #부적절한 토큰인 경우 예외 발생 
    except jwt.InvalidTokenError:
        payload = None
    else:
        return payload

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwagrs):
        # 토큰을 가져옴
        # 추후에 가져오는 방법이 바뀔 수 있음
        # 프론트에서 JWT토큰을 헤더에 넣어 'my_token' 키로 전달
        my_token = request.headers.get("my_token")

        # 토큰을 가져오면
        if my_token != None:
            payload = decode_token(my_token)
            # 토큰 Decode가 실패하면
            if payload == None:
                return False
        # 토큰 가져오는 것을 실패하면
        else:
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
        # 토큰을 가져옴
        # 추후에 가져오는 방법이 바뀔 수 있음
        # 프론트에서 JWT토큰을 헤더에 넣어 'my_token' 키로 전달
        my_token = request.headers.get("my_token")

        #JWT 토큰을 Decode
        payload = jwt.decode(my_token, SECRET_KEY, algorithms = "HS256")

        # 토큰이 만료된 경우
        if payload['exp'] < datetime.utcnow():
            payload = None
    #부적절한 토큰인 경우 예외 발생 
    except jwt.InvalidTokenError:
        payload = None

    try:
        # Payload가 있으면
        if payload != None:
            user_id = payload['user_id']
            # user_id 리턴
            return user_id
        else:
            return False
    except Exception as ex:
        print("***********")
        print(ex)
        print("***********")