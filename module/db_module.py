from datetime import datetime
from db.enum_classes import ScopeClass, StatusClass, FaceTypeClass
import os
from db import schema
from bson import ObjectId

########## CREATE #############

"""
* WhitelistFace create
"""
def create_whitelist_face(user, name):
    whitelistFace = schema.WhitelistFace(user, name, False, datetime.now())
    whitelistFace.save()

"""
* WhitelistFaceImage create
"""
def create_whitelist_face_image(whitelistFace, location):
    whitelistFaceImage = schema.WhitelistFaceImage(whitelistFace, location, False, datetime.now())
    whitelistFaceImage.save()

"""
* BlockCharacter create
"""
def create_block_character(user, location):
    blockCharacter = schema.BlockCharacter(user, location, ScopeClass.user, False, datetime.now())
    blockCharacter.save()

"""
* Video create
"""
def create_video(user, location):
    video = schema.Video(user, location, StatusClass.origin, datetime.now())
    video.save()

############# READ #################
"""
* 여러 사람 여러 사진 url 가져오기
"""
def read_whitelistFaceIdAndUrl(userId):
    temp = schema.WhitelistFace.objects(_id = userId)
    tempJson = {}
    tempJson['data'] = []

    for x in temp:
        tempUrl = schema.WhitelistFaceImage.objects(_id = x.id)
        tempJson1 = {
                "whitelistFaceId" : x._id,
                "whitelistFaceName" : x.name,
                "whitelistFaceImages" : []
            }
        for y in tempUrl:
            tempJson1["whitelistFaceImages"].append({"id" : y.id, "url" : y.url})
        tempJson.append(tempJson1)

    return tempJson

"""
* 기존 캐릭터 사진 url 가져오기
"""
def read_origin_character_url(userId):
    temp = schema.BlockCharacter.objects(scope = "origin")
    tempJson = {}
    tempJson["originCharacterUrls"] = []

    for x in temp:
        tempJson["originCharacterUrls"].append(x.url)

    return tempJson

"""
* 유저 캐릭터 여러 개 url 가져오기
"""
def read_multiple_user_character(userId):
    temp = schema.BlockCharacter.objects(scope = "user")
    tempJson = {}
    tempJson['data'] = []

    for x in temp:
        tempJson1 = {"id" : x._id, "url" : x.url}
        tempJson['data'].append(tempJson1)

    return tempJson

"""
* 셀러리 id를 통해 상태 체크
"""
def get_after_video_status(userId, taskId):
    temp = schema.Video.objects(user_id = userId, processed_url_id = ObjectId(taskId))
    temp2 = temp.processed_url_id
    temp3 = schema.Celery.objects(_id = temp2).first()
    return temp3

"""
* 특정 유저에 대한 비디오 결과 모두 조회하기
"""
def read_multiple_after_video(userId):
    temp = schema.Video.objects(user_id = userId, status = "SUCCESS")
    tempJson = {}
    tempJson['processedVideoUrls'] = []
    for x in temp:
        # 셀러리 id
        temp2 = schema.Celery.objects(_id = x.processed_url_id).first()
        tempJson1 = {"id" : x._id, "url" : temp2.result}
        tempJson['processedVideoUrls'].append(tempJson1)

    return tempJson

"""
* read video url
* 
"""
def read_video_url(_id, user_id):
    video = schema.Video.objects(_id = _id, user_id = user_id).first()
    return video.origin_url

############# UPDATE ###############

"""
* Video db update
"""
def update_db_video(_id, user, faceType, whitelistFace, blockCharacterId=""):
    if faceType not in FaceTypeClass:
        print("Can't find face type") 
        return False
    processedVideo = schema.Video.objects(
                                            _id = _id,
                                            user_id = user
                                        ).update(
                                            status = StatusClass.processed, 
                                            face_type = faceType, 
                                            block_character_id = blockCharacterId, 
                                            whitelist_faces = whitelistFace, 
                                            compledted_at = datetime.now()
                                        )
    if processedVideo > 0:
        return True
    else:
        print("Can't be modified")  
        return False

"""
* Video location update
"""
def update_location_video(_id, user, location, status):
    if status not in StatusClass:
        print("Can't find stauts") 
        return False
    processedVideo = schema.Video.objects(
                                            _id = _id,
                                            user_id = user._id
                                        ).update(
                                            status = status, 
                                            location = location, 
                                            compledted_at = datetime.now()
                                        )
    if processedVideo > 0:
        return True
    else:
        print("Can't be modified")  
        return False

"""
* Video celeryId update
"""
def update_celeryId_video(_id, user, taskId, status):
    if status not in StatusClass:
        print("Can't find stauts") 
        return False
    processedVideo = schema.Video.objects(
                                            _id = _id,
                                            user_id = ObjectId(user)
                                        ).update(
                                            status = status, 
                                            processed_url_id = taskId, 
                                            compledted_at = datetime.now()
                                        )
    if processedVideo > 0:
        return True
    else:
        print("Can't be modified")  
        return False
