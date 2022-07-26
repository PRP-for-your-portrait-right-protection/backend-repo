from datetime import datetime
from db.enum_classes import ScopeClass, StatusClass, FaceTypeClass
import os
from db import schema
from bson import ObjectId

"""
* WhitelistFace create
"""
def create_whitelist_face(user, name):
    whitelistFace = schema.WhitelistFace(user, name, False, datetime.now())
    whitelistFace.save()
    return whitelistFace._id

"""
* WhitelistFace delete
"""
def delete_whitelist_face(user, _id):  ##white list image 도 같이 지워져야 한다.
    deleteWhilelistFace = schema.WhitelistFace.objects(_id = ObjectId(_id), user_id=user).update(
        is_deleted=True,
        updated_at =datetime.now()
    )
    if deleteWhilelistFace > 0:
        schema.WhitelistFaceImage.objects(whitelist_face_id = ObjectId(_id)).update(
            is_deleted=True,
            updated_at =datetime.now()
        )
        return True
    else:
        print("Can't be deleted")
        return False

"""
* WhitelistFaceImage create
"""
def create_whitelist_face_image(whitelistFace, location):
    whitelistFaceImage = schema.WhitelistFaceImage(whitelistFace, location, False, datetime.now())
    whitelistFaceImage.save()
    return whitelistFaceImage._id

"""
* WhitelistFaceImage delete
"""
def delete_whitelist_face_image(user, _id):
    deleteWhilelistFaceImage = schema.WhitelistFaceImage.objects(_id = ObjectId(_id), user_id = user).update(
        is_deleted=True,
        updated_at =datetime.now()
    )
    if deleteWhilelistFaceImage > 0:
        return True
    else:
        print("Can't be deleted")
        return False

"""
* BlockCharacter create
"""
def create_block_character(user, location):
    blockCharacter = schema.BlockCharacter(user, location, ScopeClass.user, False, datetime.now())
    blockCharacter.save()
    return blockCharacter._id

"""
* BlockCharacter delete
"""
def delete_block_character(user, _id):
    deleteBlockCharacter = schema.BlockCharacter.objects(_id = ObjectId(_id), user_id = user).update(
        is_deleted=True,
        updated_at =datetime.now()
    )
    if deleteBlockCharacter > 0:
        return True
    else:
        print("Can't be deleted")  
        return False

"""
* Video create
"""
def create_video(user, location):
    video = schema.Video(user, location, StatusClass.origin, datetime.now())
    video.save()
    return video._id

"""
* Video db update
"""
def update_db_video(_id, user, faceType, whitelistFace, blockCharacterId=""):
    if faceType not in FaceTypeClass:
        print("Can't find face type") 
        return False
    processedVideo = schema.Video.objects(
                                            _id = _id,
                                            user_id = user._id
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
* video delete
"""
def delete_video(user, _id):
    deleteVideo = schema.BlockCharacter.objects(_id = ObjectId(_id) , user_id = user).update(
        status=StatusClass.deleted,
        updated_at =datetime.now()
    )
    if deleteVideo > 0:
        return True
    else:
        print("Can't be deleted")
        return False
    
