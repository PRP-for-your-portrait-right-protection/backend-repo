from datetime import datetime
from db.enum_classes import ScopeClass, StatusClass, FaceTypeClass
from static import status_code
from db import schema
from bson import ObjectId

################### WHITELIST FACE ###################

"""
* WhitelistFace create
"""
def create_whitelist_face(user, name):
    try:
        whitelistFace = schema.WhitelistFace(user, name, False, datetime.now())
        result = schema.WhitelistFace.objects().insert(whitelistFace)
        return True, {"id" : str(result._id)}
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}

"""
* WhitelistFace update
"""
def update_whitelist_face(user, _id, name):
    try:
        whitelistFace = schema.WhitelistFace.objects(_id = ObjectId(_id), user_id = user, is_deleted=False)
        if whitelistFace.count() == 0:
            return False, {"error": f'{status_code.id_error}whitelist_face'}
        updateWhitelistFace = whitelistFace.update(
            name = name,
            updated_at = datetime.now()
        )
        if updateWhitelistFace > 0:
            return True, {"message": status_code.update_01_success}
        else:
            print("Can't be modified")
            return False, {"error": status_code.update_02_fail}
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}

"""
* WhitelistFace delete
"""
def delete_whitelist_face(user, _id):  ##white list image 도 같이 지워져야 한다.
    try:
        whitelistFace = schema.WhitelistFace.objects(_id = ObjectId(_id), user_id = user, is_deleted=False)
        if whitelistFace.count() == 0:
            return False, {"error": f'{status_code.id_error}whitelist_face'}
        deleteWhitelistFace = whitelistFace.update(
            is_deleted=True,
            updated_at =datetime.now()
        )
        if deleteWhitelistFace > 0:
            schema.WhitelistFaceImage.objects(whitelist_face_id = ObjectId(_id), is_deleted=False).update(
                is_deleted=True,
                updated_at =datetime.now()
            )
            return True, {"message": status_code.delete_01_success}
        else:
            print("Can't be deleted")
            return False, {"error": status_code.delete_02_fail}
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}

################### WHITELIST FACE IMAGE ###################

"""
* WhitelistFaceImage create
"""
def create_whitelist_face_image(whitelistFace, location):
    try:
        whitelistFaceImage = schema.WhitelistFaceImage(whitelistFace, location, False, datetime.now())
        result = schema.WhitelistFaceImage.objects().insert(whitelistFaceImage)
        return True, {"id" : str(result._id)}
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}

"""
* WhitelistFaceImage read
"""
def read_whitelist_face_image(user):
    try:
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
        return True, data
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}
    
"""
* WhitelistFaceImage delete
"""
def delete_whitelist_face_image(whitelistFaceId, _id):
    try:
        whilelistFaceImage = schema.WhitelistFaceImage.objects(_id = ObjectId(_id), whitelist_face_id = whitelistFaceId, is_deleted=False)
        if whilelistFaceImage.count() == 0:
            return False, {"error": f'{status_code.id_error}whitelist_face_image'}
        deleteWhilelistFaceImage = whilelistFaceImage.update(
            is_deleted=True,
            updated_at =datetime.now()
        )
        if deleteWhilelistFaceImage > 0:
            return True, {"message": status_code.delete_01_success}
        else:
            print("Can't be deleted")
            return False, {"error": status_code.delete_02_fail}
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}

"""
* WhitelistFaceImg corresponding to id read
"""
def read_whitelist_face_url(user, whitelistFaceId): #id 리스트로 받아옴
    try:
        whitelistFaceImgList = []
        for x in whitelistFaceId:
            temp = schema.WhitelistFace.objects(user_id = ObjectId(user), _id = ObjectId(x), is_deleted = False).first()
            for y in schema.WhitelistFaceImage.objects(whitelist_face_id = temp._id, is_deleted=False):
                whitelistFaceImgList.append(y.url) 
        return True, whitelistFaceImgList
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}

################################################ BLOCkCHARACTER ################################################
"""
* OriginBlockCharacter read
"""
def read_origin_block_character():
    try:
        temp = schema.BlockCharacter.objects(scope = ScopeClass.origin, is_deleted=False)
        tempJson = {}
        tempJson["data"] = []   
        for x in temp:
            tempJson1 = {"id" : str(x._id), "url" : x.url}
            tempJson["data"].append(tempJson1)
        return True, tempJson
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}

"""
* BlockCharacter create
"""
def create_block_character(user, location):
    try:
        blockCharacter = schema.BlockCharacter(user, location, ScopeClass.user, False, datetime.now())
        result = schema.BlockCharacter.objects().insert(blockCharacter)
        return True, {"id": str(result._id)}
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}

"""
* UserBlockCharacter read
"""
def read_user_block_character(user):
    try:
        temp = schema.BlockCharacter.objects(user_id = ObjectId(user), scope = ScopeClass.user, is_deleted=False)
        tempJson = {}
        tempJson['data'] = []
        for x in temp:
            tempJson1 = {"id" : str(x._id), "url" : x.url}
            tempJson['data'].append(tempJson1)
        return True, tempJson
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}

"""
* BlockCharacter delete
"""
def delete_block_character(user, _id):
    try:
        blockCharacter = schema.BlockCharacter.objects(_id = ObjectId(_id), scope = ScopeClass.user, user_id = user, is_deleted=False)
        if blockCharacter.count() == 0:
            return False, {"error": f'{status_code.id_error}block_character'}
        deleteBlockCharacter = blockCharacter.update(
            is_deleted=True,
            updated_at =datetime.now()
        )
        if deleteBlockCharacter > 0:
            return True, {"message": status_code.delete_01_success}
        else:
            print("Can't be deleted")  
            return False, {"error": status_code.delete_02_fail}
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}

"""
* BlockCharacter corresponding to id read
"""
def read_block_character_url(blockCharacterId):
    try:
        blockCharacter = schema.BlockCharacter.objects(_id = ObjectId(blockCharacterId), is_deleted=False).first()
        return True, blockCharacter.url
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}
    
################################################ VIDEO ################################################
"""
* Video create
"""
def create_video(user, location):
    try:
        video = schema.Video(user, location, ScopeClass.origin.value, datetime.now())
        result = schema.Video.objects().insert(video)
        return True, str(result._id)
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}

"""
* OriginVideo read
"""
def read_origin_video(_id, user):
    try:
        video = schema.Video.objects(_id = _id, user_id = user).first()
        if video.processed_url_id == None:
            return True, video.origin_url
        else:
            return False, {"error": status_code.celery_error}
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}

"""
* ProccessedVideo read
"""
def read_proccessed_video(user):
    try:
        temp = schema.Video.objects(user_id = ObjectId(user), status = StatusClass.success.value)
        tempJson = {}
        tempJson['data'] = []
        for x in temp:
            # 셀러리 id
            temp2 = schema.Celery.objects(_id = x.processed_url_id).first()
            if temp2 == None:
                continue
            tempJson1 = {"id" : str(x._id), "url" : temp2.result.replace('\"', '')}
            tempJson['data'].append(tempJson1)
        return True, tempJson
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}

"""
* Video db update
"""
def update_video(_id, user, faceType, whitelistFace, blockCharacterId=""):
    try:
        if faceType != FaceTypeClass.character.value and faceType != FaceTypeClass.mosaic.value:
            print("Can't find face type") 
            return False, {"error": f'{status_code.enum_class_error}face type'}
        video = schema.Video.objects(_id = ObjectId(_id), user_id = user)
        if video.count() == 0:
            return False, {"error": f'{status_code.id_error}video'}
        if blockCharacterId == "" or blockCharacterId == None:
            processedVideo = video.update(
                status = StatusClass.processed.value, 
                face_type = faceType, 
                whitelist_faces = whitelistFace, 
                completed_at = datetime.now()
            )
        else:
            processedVideo = video.update(
                status = StatusClass.processed.value, 
                face_type = faceType, 
                block_character_id = ObjectId(blockCharacterId), 
                whitelist_faces = whitelistFace, 
                completed_at = datetime.now()
            )
        if processedVideo > 0:
            return True, {"message": status_code.update_01_success}
        else:
            print("Can't be modified")  
            return False, {"error": status_code.update_02_fail}
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}

"""
* Video celeryId update
"""
def update_video_celery(_id, user, task, status):
    try:
        # if status not in StatusClass:
        #     print("Can't find stauts") 
        #     return False
        video = schema.Video.objects(_id = ObjectId(_id), user_id = user)
        if video.count() == 0:
            return False, {"error": f'{status_code.id_error}video'}
        processedVideo = video.update(
            status = status, 
            processed_url_id = task.id, 
            completed_at = datetime.now()
        )
        if processedVideo > 0:
            return True, {"message" : status_code.update_01_success}
        else:
            print("Can't be modified")  
            return False, {"error" : status_code.update_02_fail}
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}

"""
* video delete
"""
def delete_video(user, _id):
    try:
        video = schema.Video.objects(_id = ObjectId(_id), user_id = user)
        if video.count() == 0:
            return False, {"error": f'{status_code.id_error}video'}
        deleteVideo = video.update(
            status = "deleted",
            updated_at = datetime.now()
        )
        if deleteVideo > 0:
            return True, {"message" : status_code.delete_01_success}
        else:
            print("Can't be deleted")
            return False, {"error" : status_code.delete_02_fail}
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)} 
    
"""
* read celery status
"""
def read_celery_status(user, taskId):
    try:
        temp = schema.Video.objects(user_id = user, processed_url_id = taskId).first()
        temp3 = schema.Celery.objects(_id = temp.processed_url_id).first()
        if temp3 != None:
            if temp3.status == StatusClass.success.value:
                temp2 = schema.Video.objects(user_id = user, processed_url_id = taskId).update(status = StatusClass.success.value)
                if temp2 > 0:
                    return True, {"status":temp3.status}
                else:
                    # db 업데이트 실패
                    return False, {"error" : status_code.update_02_fail}
            elif temp3.status == StatusClass.failure.value:
                # failure일 경우
                return True, {"status":temp3.status}
        else:
            # pending일 경우 (셀러리 결과가 db에 저장되지 않음)
            return 0
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)} 

"""
* video status update when the celery status is failure
"""
def update_video_celery_failure(user, taskId):
    video = schema.Video.objects(user_id = user, processed_url_id = taskId)
    if video.count() == 0:
        return False
    updateVideo = video.update(status = StatusClass.failure.value)
    if updateVideo > 0:
        return True
    else:
        return False
