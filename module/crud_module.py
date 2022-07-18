from flask import request
from datetime import datetime

from itsdangerous import NoneAlgorithm

"""
* 다인 다중 파일 url 가져오기
"""
def multiple_get(db, collction_name):
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

        # 2. user_id 가져오기
        userId = request.form["user_id"]

        # 3. user id에 해당하는 person_name을 중복 제거 하여 가져옴
        colList = col.distinct("person_name", {"user_id" : userId})

        if colList == None:
            print("Can't find person")
            return False

        # 4. json 형태로 매핑
        colJson = {}

        for name in colList:
            colJson[name] = []
            # if collction_name == "get_people": 
            docs = col.find({"person_name" : name, "user_id" : userId})
            for x in docs:
                colJson[name].append(x['person_url'])

        # 5. 다중 파일 json 반환
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
def single_get(db, collction_name):
    if db == None:
        print("Can't connect to DB")
        return False
    
    try:
        # 1. collction_name 확인 & db에서 url 가져옴
        if collction_name == "get_character": 
            col = db.upload_character
            userId = request.form["user_id"]
            docs = col.find({"user_id" : userId})
            url = "character_url"
        elif collction_name == "get_video_modification": 
            col = db.video_modification
            userId = request.form["user_id"]
            docs = col.find({"user_id" : userId})
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
def single_update(db):
    if db == None:
        print("Can't connect to DB")
        return False

    try:
        # 0. 컬렉션 설정
        col = db.people

        if col == None:
            print("Can't find collection")
            return False

        # 1. userId와 personName을 가져옴
        userId = request.form["user_id"]
        personName = request.form["person_name"]
        personNameAfter = request.form["person_name_after"]

        # 2. 주어진 user_id, person_name에 해당하는 Document 수정
        dbResponse = col.update_many(
            {
                "user_id" : userId,
                "person_name" : personName
            }, 
            {
                "$set" : 
                {
                    "person_name" : personNameAfter,
                    "mod_date" : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        )

        # 3. 수정이 성공적으로 되었는 지 검사
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
* 단일 삭제
"""
def single_delete(db, collection_name):
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

        # 2. 유저 아이디와 url 가져옴
        userId = request.form["user_id"]
        url = request.form["url"]

        # 3. DB에서 유저아이디 && url 일치하는 Document -> activation_YN = N
        dbResponse = col.update_one(
            {
                "user_id" : userId, 
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

        # 4. 수정이 성공적으로 되었는 지 검사
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
def multiple_delete(db, collection_name):
    if db == None:
        print("Can't connect to DB")
        return False

    try:
        # 1. 컬렉션 설정 후 상황에 맞는 쿼리 설정
        # 1-1. 인물 -> user_id, person_name 필요
        userId = request.form["user_id"]

        if collection_name == "people":
            col = db.people
            personName = request.form["person_name"]

            if personName == None:
                print("Can't find personName")
                return False

            my_query = {
                "user_id" : userId,
                "person_name" : personName
            }
        # 1-2. 비디오 결과 -> user_id 필요
        elif collection_name == "video_modification":
            col = db.video_modification
            my_query = {
                "user_id" : userId
            }
        # 1-3. 업로드 캐릭터 -> user_id 필요
        elif collection_name == "characters":
            col = db.upload_character
            my_query = {
                "user_id" : userId
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

        # 수정이 성공적으로 되었는 지 검사
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