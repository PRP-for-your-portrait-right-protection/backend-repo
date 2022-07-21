from datetime import datetime
from db import schema

"""
* 다인 다중 파일 url 가져오기
"""
def multiple_get(collction_name, user_id):
    try:
        """
        # 1. collction_name 확인
        
        if collction_name == "get_people":
            col = db.people
        else:
            print("can't find collction name")
            return False
        """

        # 2. user id에 해당하는 person_name을 중복 제거 하여 가져옴
        # colList = col.distinct("person_name", {"user_id" : user_id})
        colList = schema.People.objects(user_id = user_id).distinct('person_name')
        if colList == None:
            print("Can't find person")
            return False

        # 3. json 형태로 매핑
        colJson = {}

        for name in colList:
            colJson[name] = []
            # if collction_name == "get_people": 
            docs = schema.People.objects(person_name = name, user_id = user_id, activation_YN = "Y")
            # docs = col.find({"person_name" : name, "user_id" : user_id, "activation_YN" : "Y"})
            for x in docs:
                colJson[name].append(x.person_url)

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
def single_get(collction_name, user_id=""):
    try:
        # 1. collction_name 확인 & db에서 url 가져옴
        if collction_name == "get_character": 
            docs = schema.UploadCharacter.objects(user_id = user_id, activation_YN = "Y")
        elif collction_name == "get_video_modification": 
            docs = schema.VideoModification.objects(user_id = user_id, activation_YN = "Y")
        elif collction_name == "get_origin_character":
            docs = schema.OriginCharacter.objects()
        else:
            print("Can't find collection name")
            return False
        
        # 2. json 형태로 매핑
        colJson = {}
        colJson["file"] = []
        for x in docs:
            if collction_name == "get_character": 
                colJson["file"].append(x.character_url)
            elif collction_name == "get_video_modification": 
                colJson["file"].append(x.video_modification_url)
            elif collction_name == "get_origin_character":
                colJson["file"].append(x.origin_character_url)

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
def single_update(user_id, person_name, person_name_after):
    try:
        # 2. 주어진 user_id, person_name에 해당하는 Document 수정
        dbResponse = schema.People.objects(user_id = user_id, person_name = person_name).update(set__person_name = person_name_after, set__mod_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        # 3. 수정이 성공적인지 검사
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
    
"""
* 단일 삭제
"""
def single_delete(collection_name, user_id, url):
    try: 
        # 1. DB에서 유저아이디 && url 일치하는 Document -> activation_YN = N
        if collection_name == "people":
            dbResponse = schema.People.objects(user_id = user_id, person_url = url).update(set__activation_YN = "N", set__mod_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        elif collection_name == "character":
            dbResponse = schema.UploadCharacter.objects(user_id = user_id, character_url = url).update(set__activation_YN = "N", set__mod_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            print("Can't find collection name")
            return False

        # 3. 수정이 성공적인지 검사
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

"""
* 다중 삭제
* 1. 특정 인물에 대한 사진 모두 삭제
* 2. 특정 유저에 대한 비디오 결과 모두 삭제
* 3. 특정 유저에 대한 캐릭터 모두 삭제
"""       
def multiple_delete(collection_name, user_id, person_name=""):
    try:
        # 1. 쿼리에 일치하는 Document 모두 -> activation_YN = N
        if collection_name == "people":
            # 회원에 대한 사람사진 모두 삭제
            if person_name == None or person_name == "":
                dbResponse = schema.People.objects(user_id = user_id).update(set__activation_YN = "N", set__mod_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            # 특정 회원의 특정 사람에 대한 사람사진 모두 삭제
            else :
                dbResponse = schema.People.objects(user_id = user_id, person_name = person_name).update(set__activation_YN = "N", set__mod_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        elif collection_name == "video_modification":
           dbResponse = schema.VideoModification.objects(user_id = user_id).update(set__activation_YN = "N", set__mod_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        elif collection_name == "characters":
            dbResponse = schema.UploadCharacter.objects(user_id = user_id).update(set__activation_YN = "N", set__mod_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            print("Can't find collection name")
            return False

        # 3. 수정이 성공적인지 검사
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
