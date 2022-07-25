from datetime import datetime
from db.enum_classes import ScopeClass, StatusClass, FaceTypeClass
import os
from db import schema

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
* read video url
* 
"""
def read_video_url(videoId):
    video = schema.Video.objects(
        _id = _id,
        user_id = user
    )


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
