from datetime import datetime
from db.enum_classes import ScopeClass, StatusClass, FaceTypeClass
import os
from db import schema
from bson import ObjectId

################### WHITELIST FACE ###################

"""
* WhitelistFace create - done
"""
def create_whitelist_face(user, name):
    whitelistFace = schema.WhitelistFace(user, name, False, datetime.now())
    result = schema.WhitelistFace.objects().insert(whitelistFace)
    return str(result._id)

"""
* WhitelistFace update - done
"""
def update_whitelist_face(user, _id, name):
    updateWhitelistFace = schema.WhitelistFace.objects(_id = ObjectId(_id), user_id = user, is_deleted=False).update(
        name = name,
        updated_at = datetime.now()
    )
    if updateWhitelistFace > 0:
        return True
    else:
        print("Can't be modified")
        return False

"""
* WhitelistFace delete - done
"""
def delete_whitelist_face(user, _id):  ##white list image 도 같이 지워져야 한다.
    deleteWhitelistFace = schema.WhitelistFace.objects(_id = ObjectId(_id), user_id = user, is_deleted=False).update(
        is_deleted=True,
        updated_at =datetime.now()
    )
    if deleteWhitelistFace > 0:
        schema.WhitelistFaceImage.objects(whitelist_face_id = ObjectId(_id), is_deleted=False).update(
            is_deleted=True,
            updated_at =datetime.now()
        )
        return True
    else:
        print("Can't be deleted")
        return False

################### WHITELIST FACE IMAGE ###################

"""
* WhitelistFaceImage create
"""
def create_whitelist_face_image(whitelistFace, location):
    whitelistFaceImage = schema.WhitelistFaceImage(whitelistFace, location, False, datetime.now())
    result = schema.WhitelistFaceImage.objects().insert(whitelistFaceImage)
    return str(result._id)

"""
* WhitelistFaceImage read
"""
def read_whitelist_face_image(user):
    result = schema.WhitelistFace.objects(user_id = ObjectId(user), is_deleted=False)
    data = {}
    data["data"] = []

    for x in result:
        arr = {
            "whitelistFaceId" : str(x._id),
            "whitelistFaceName" : x.name,
            "whitelistFaceImages" : []
        }
        imageResult = schema.WhitelistFaceImage.objects(whitelist_face_id = x._id, is_deleted=False)
        for y in imageResult:
            arr["whitelistFaceImages"].append({"id" : str(y._id), "url" : y.url})
        data["data"].append(arr)
    return data

"""
* WhitelistFaceImage delete
"""
def delete_whitelist_face_image(whitelistFaceId, _id):
    deleteWhilelistFaceImage = schema.WhitelistFaceImage.objects(_id = ObjectId(_id), whitelist_face_id = whitelistFaceId, is_deleted=False).update(
        is_deleted=True,
        updated_at =datetime.now()
    )
    if deleteWhilelistFaceImage > 0:
        return True
    else:
        print("Can't be deleted")
        return False

"""
* WhitelistFaceImg corresponding to id read
"""
def read_whitelist_face_url(user, whitelistFaceId): #id 리스트로 받아옴
    whitelistFaceImgList = []

    print(type(user))
    print(type(whitelistFaceId))
    print(user)
    print(whitelistFaceId)
    for x in whitelistFaceId:
        temp = schema.WhitelistFace.objects(user_id = ObjectId(user), _id = ObjectId(x), is_deleted = False).first()
        for y in schema.WhitelistFaceImage.objects(whitelist_face_id = temp._id, is_deleted=False):
            whitelistFaceImgList.append(y.url) 
            
    return whitelistFaceImgList

################################################ BLOCkCHARACTER ################################################
"""
* OriginBlockCharacter read
"""
def read_origin_block_character():
    temp = schema.BlockCharacter.objects(scope = ScopeClass.origin, is_deleted=False)
    tempJson = {}
    tempJson["data"] = []

    for x in temp:
        tempJson1 = {"id" : str(x._id), "url" : x.url}
        tempJson["data"].append(tempJson1)

    return tempJson

"""
* BlockCharacter create
"""
def create_block_character(user, location):
    blockCharacter = schema.BlockCharacter(user, location, ScopeClass.user, False, datetime.now())
    result = schema.BlockCharacter.objects().insert(blockCharacter)
    return str(result._id)

"""
* UserBlockCharacter read
"""
def read_user_block_character(user):
    temp = schema.BlockCharacter.objects(user_id = ObjectId(user), scope = ScopeClass.user, is_deleted=False)
    tempJson = {}
    tempJson['data'] = []

    for x in temp:
        tempJson1 = {"id" : str(x._id), "url" : x.url}
        tempJson['data'].append(tempJson1)

    return tempJson

"""
* BlockCharacter delete
"""
def delete_block_character(user, _id):
    deleteBlockCharacter = schema.BlockCharacter.objects(_id = ObjectId(_id), scope = ScopeClass.user, user_id = user, is_deleted=False).update(
        is_deleted=True,
        updated_at =datetime.now()
    )
    if deleteBlockCharacter > 0:
        return True
    else:
        print("Can't be deleted")  
        return False

"""
* BlockCharacter corresponding to id read
"""
def read_block_character_url(blockCharacterId):
    blockCharacter = schema.BlockCharacter.objects(_id = ObjectId(blockCharacterId), is_deleted=False).first()
    print("CCCCCCCCCCCCCCCC")
    return blockCharacter.url

################################################ VIDEO ################################################
"""
* Video create
"""
def create_video(user, location):
    video = schema.Video(user, location, "origin", datetime.now())
    result = schema.Video.objects().insert(video)
    return str(result._id)

"""
* OriginVideo read
"""
def read_origin_video(_id, user):
    video = schema.Video.objects(_id = _id, user_id = user).first()
    return video.origin_url

"""
* ProccessedVideo read
"""
def read_proccessed_video(user):
    temp = schema.Video.objects(user_id = ObjectId(user), status = "SUCCESS")
    tempJson = {}
    tempJson['data'] = []
    for x in temp:
        # 셀러리 id
        temp2 = schema.Celery.objects(_id = x.processed_url_id).first()
        tempJson1 = {"id" : str(x._id), "url" : temp2.result.replace('\"', '')}
        tempJson['data'].append(tempJson1)

    return tempJson

"""
* Video db update
"""
def update_video(_id, user, faceType, whitelistFace, blockCharacterId=""):
    print(type(_id))
    if faceType != FaceTypeClass.character.value and faceType != FaceTypeClass.mosaic.value:
        print("Can't find face type") 
        return False

    if blockCharacterId == "" or blockCharacterId == None:
        processedVideo = schema.Video.objects(
            _id = ObjectId(_id),
            user_id = user
        ).update(
            status = StatusClass.processed.value, 
            face_type = faceType, 
            # block_character_id = blockCharacterId, 
            whitelist_faces = whitelistFace, 
            completed_at = datetime.now()
        )
    else:
        processedVideo = schema.Video.objects(
            _id = ObjectId(_id),
            user_id = user
        ).update(
            status = StatusClass.processed.value, 
            face_type = faceType, 
            block_character_id = ObjectId(blockCharacterId), 
            whitelist_faces = whitelistFace, 
            completed_at = datetime.now()
        )
    if processedVideo > 0:
        return True
    else:
        print("Can't be modified")  
        return False

"""
* Video celeryId update
"""
def update_video_celery(_id, user, task, status):
    # if status not in StatusClass:
    #     print("Can't find stauts") 
    #     return False
    print("?????????????????")
    processedVideo = schema.Video.objects(
        _id = ObjectId(_id),
        user_id = user
    ).update(
        status = status, 
        processed_url_id = task.id, 
        completed_at = datetime.now()
    )
    if processedVideo > 0:
        return True
    else:
        print("Can't be modified")  
        return False

"""
* video delete
"""
def delete_video(user, _id):
    # deleteVideo = schema.BlockCharacter.objects(_id = ObjectId(_id) , user_id = user).update(
    deleteVideo = schema.Video.objects(_id = ObjectId(_id) , user_id = user).update(
        status = "deleted",
        updated_at = datetime.now()
    )
    if deleteVideo > 0:
        return True
    else:
        print("Can't be deleted")
        return False
    
"""
* read celery status
"""
def read_celery_status(user, taskId):
    temp = schema.Video.objects(user_id = user, processed_url_id = taskId).first()
    # if temp == None:
    #     return False
    print(temp)
    
    #failure 일때도 바꾸도록 수정필요

    temp3 = schema.Celery.objects(_id = temp.processed_url_id).first()

    if temp3 != None:
        if temp3.status == "SUCCESS":
            temp2 = schema.Video.objects(user_id = user, processed_url_id = taskId).update(status = "SUCCESS")
            if temp2 > 0:
                return temp3.status
            else:
                # db 업데이트 실패
                return "update Failure"
        elif temp3.status == "FAILURE":
            # failure일 경우
            return temp3.status
    else:
        # pending일 경우 (셀러리 결과가 db에 저장되지 않음)
        return 0

"""
* video status update when the celery status is failure
"""
def update_video_celery_failure(user, taskId):
    update = schema.Video.objects(
        user_id = user, 
        processed_url_id = taskId
        ).update(
        status = StatusClass.failure.value
    )
    if update > 0:
        return True
    else:
        return False
    