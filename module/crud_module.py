from flask import request
from datetime import datetime

"""
* 다인 다중 파일 url 가져오기
"""
def multiple_get(db, collction_name):
    try:
        # 1. collction_name 확인
        if collction_name == "get_people":
            col = db.people
        else:
            print("can't find collction name")
            return False

        # 2. user_id 가져오기
        userId = request.form["user_id"]

        # 3. user id에 해당하는 person_name을 중복 제거 하여 가져옴
        col_list = col.distinct("person_name", {"user_id" : userId})

        # 4. json 형태로 매핑
        col_json = {}

        for name in col_list:
            col_json[name] = []
            if collction_name == "get_people":
                docs = col.find({"person_name" : name, "user_id" : userId})
                for x in docs:
                    col_json[name].append(x['person_url'])

        # 5. 다중 파일 json 반환
        return col_json
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False

"""
* 일인 다중 파일 url 가져오기
"""
def single_get(db, collction_name):
    try:
        # 1. collction_name 확인 & db에서 url 가져옴
        if collction_name == "get_character": 
            col = db.upload_character
            userId = request.form["user_id"]
            docs = col.find({"user_id" : userId})
            url = "character_url"
        elif collction_name == "get_video_modification": 
            col = db.upload_character
            userId = request.form["user_id"]
            docs = col.find({"user_id" : userId})
            url = "video_modification_url"
        elif collction_name == "get_origin_character":
            col = db.origin_character
            docs = col.find()
            url = "origin_character_url"
        else:
            print("can't find collction name")
            return False
        
        # 2. json 형태로 매핑
        col_json = {}
        col_json["file"] = []
        for x in docs:
            col_json["file"].append(x[url])
        
        # 3. 다중 파일 json 반환
        return col_json
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False
    
"""
* 인물 이름 수정
"""
def single_update(db):
    try:
        # 컬렉션 설정
        col = db.people

        # 주어진 user_id, person_name에 해당하는 Document 수정
        col.update_many(
            {
                "user_id" : request.form["user_id"], 
                "person_name" : request.form["person_name"]
            }, 
            {
                "$set" : 
                {
                    "person_name" : request.form["person_name_after"], 
                    "mod_date" : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        )
        return True
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False   
    
"""
* 단일 삭제
"""
def single_delete(db, collection_name):
    try: 
        # 1. 컬렉션 설정
        if collection_name == "people":
            col = db.people
            url_string = "person_url"
        elif collection_name == "video_modification":
            col = db.video_modification
            url_string = "video_modification_url"
        elif collection_name == "character":
            col = db.upload_character
            url_string = "character_url"
        
        # 2. 유저 아이디와 url 가져옴
        userId = request.form["user_id"]
        url = request.form["url"]

        # 3. DB에서 유저아이디 && url 일치하는 Document -> activation_YN = N
        col.update_one(
            {
                "user_id" : userId, 
                f'{url_string}' : url
            }, 
            {
                "$set" : 
                    {
                        "activation_YN" : "N",
                        "mod_date" : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
            }
        )
        return True
    except Exception as ex:
            print('*********')
            print(ex)
            print('*********')
            return False    

"""
* 다중 삭제
* 1. 특정 인물에 대한 사진 모두 삭제
* 2. 특정 유저에 대한 비디오 결과 모두 삭제
* 3. 특정 유저에 대한 캐릭터 모두 삭제
"""       
def multiple_delete(db, collection_name):
    try:
        # 1. 컬렉션 설정 후 상황에 맞는 쿼리 설정
        # 1-1. 인물 -> user_id, person_name 필요
        if collection_name == "people":
            col = db.people
            my_query = {
                "user_id" : request.form["user_id"],
                "person_name" : request.form["person_name"]
            }
        # 1-2. 비디오 결과 -> user_id 필요
        elif collection_name == "video_modification":
            col = db.video_modification
            my_query = {
                "user_id" : request.form["user_id"]
            }
        # 1-3. 업로드 캐릭터 -> user_id 필요
        elif collection_name == "characters":
            col = db.upload_character
            my_query = {
                "user_id" : request.form["user_id"]
            }

        # 2. 쿼리에 일치하는 Document 모두 -> activation_YN = N
        col.update_many(
            my_query,
            {"$set" : 
                {
                    "activation_YN" : "N",
                    "mod_date" : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
             }
        )
        return True
    except Exception as ex:
            print('*********')
            print(ex)
            print('*********')
            return False   

