from flask import request
from datetime import datetime

from itsdangerous import NoneAlgorithm

"""
* 다인 다중 파일 url 가져오기
"""
def multiple_get(db, collction_name, user_id):
    if db == None:
        print("Can't connect to DB")
        return False

    try:
        """
        # 1. collction_name 확인
        
        if collction_name == "get_people":
            col = db.people
        else:
            print("can't find collction name")
            return False
        """
        # 1. collction_name 확인
        if collction_name != None:
            col = db.people
        else:
            print("Can't find collection name")
            return False

        # 2. user id에 해당하는 person_name을 중복 제거 하여 가져옴
        colList = col.distinct("person_name", {"user_id" : user_id})

        if colList == None:
            print("Can't find person")
            return False

        # 3. json 형태로 매핑
        colJson = {}

        for name in colList:
            colJson[name] = []
            # if collction_name == "get_people": 
            docs = col.find({"person_name" : name, "user_id" : user_id, "activation_YN" : "Y"})
            for x in docs:
                colJson[name].append(x['person_url'])

        # 4. 다중 파일 json 반환
        if colJson == None:
            print("colJson is None")
            return False
        else:
            return colJson
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False

"""
* 일인 다중 파일 url 가져오기
"""
def single_get(db, collction_name, user_id=""):
    if db == None:
        print("Can't connect to DB")
        return False
    
    try:
        # 1. collction_name 확인 & db에서 url 가져옴
        if collction_name == "get_character": 
            col = db.upload_character
            docs = col.find({"user_id" : user_id, "activation_YN" : "Y"})
            url = "character_url"
        elif collction_name == "get_video_modification": 
            col = db.video_modification
            docs = col.find({"user_id" : user_id, "activation_YN" : "Y"})
            url = "video_modification_url"
        elif collction_name == "get_origin_character":
            col = db.origin_character
            docs = col.find()
            url = "origin_character_url"
        else:
            print("Can't find collection name")
            return False
        
        # 2. json 형태로 매핑
        colJson = {}
        colJson["file"] = []
        for x in docs:
            colJson["file"].append(x[url])

        # 3. 다중 파일 json 반환
        if colJson == None:
            print("colJson is None")
            return False
        else:
            return colJson
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return False
    
"""
* 인물 이름 수정
"""
def single_update(db, user_id, person_name, person_name_after):
    if db == None:
        print("Can't connect to DB")
        return False

    try:
        # 1. 컬렉션 설정
        col = db.people

        if col == None:
            print("Can't find collection")
            return False

        # 2. 주어진 user_id, person_name에 해당하는 Document 수정
        dbResponse = col.update_many(
            {
                "user_id" : user_id,
                "person_name" : person_name
            }, 
            {
                "$set" : 
                {
                    "person_name" : person_name_after,
                    "mod_date" : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        )

        # 3. 수정이 성공적인지 검사
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
* 단일 삭제
"""
def single_delete(db, collection_name, user_id, url):
    if db == None:
        print("Can't connect to DB")
        return False

    try: 
        # 1. 컬렉션 설정
        if collection_name == "people":
            col = db.people
            urlString = "person_url"
        elif collection_name == "video_modification":
            col = db.video_modification
            urlString = "video_modification_url"
        elif collection_name == "character":
            col = db.upload_character
            urlString = "character_url"
        else:
            print("Can't find collection name")
            return False

        # 2. DB에서 유저아이디 && url 일치하는 Document -> activation_YN = N
        dbResponse = col.update_one(
            {
                "user_id" : user_id, 
                f'{urlString}' : url
            }, 
            {
                "$set" : 
                    {
                        "activation_YN" : "N",
                        "mod_date" : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
            }
        )

        # 3. 수정이 성공적인지 검사
        if dbResponse.modified_count == 1:
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
* 다중 삭제
* 1. 특정 인물에 대한 사진 모두 삭제
* 2. 특정 유저에 대한 비디오 결과 모두 삭제
* 3. 특정 유저에 대한 캐릭터 모두 삭제
"""       
def multiple_delete(db, collection_name, user_id, person_name=""):
    if db == None:
        print("Can't connect to DB")
        return False

    try:
        # 1. 컬렉션 설정 후 상황에 맞는 쿼리 설정
        if collection_name == "people":
            col = db.people
            if person_name == None or person_name == "":
                print("Can't find personName")
                return False
            my_query = {
                "user_id" : user_id,
                "person_name" : person_name
            }
        elif collection_name == "video_modification":
            col = db.video_modification
            my_query = {
                "user_id" : user_id
            }
        elif collection_name == "characters":
            col = db.upload_character
            my_query = {
                "user_id" : user_id
            }
        else:
            print("Can't find collection name")
            return False

        # 2. 쿼리에 일치하는 Document 모두 -> activation_YN = N
        dbResponse = col.update_many(
            my_query,
            {"$set" : 
                {
                    "activation_YN" : "N",
                    "mod_date" : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
             }
        )

        # 3. 수정이 성공적인지 검사
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
