from flask import request
from datetime import datetime
from bson import ObjectId
from db.enum_classes import ScopeClass, StatusClass, FaceTypeClass, SchemaName
import module
"""
* whitelist face upload
"""
def whitelist_face_upload():
    token = request.headers.get('Token')
    user = module.token.get_user(token)
    name = request.form['name']
    id = module.db_module.create_whitelist_face(user, name)
    return id

"""
* WhitelistFace delete
"""
def delete_whitelist_face(_id):
    token = request.headers.get('Token')
    user = module.token.get_user(token)
    result = module.db_module.delete_whitelist_face(user, _id)
    return result

"""
* whitelist face image upload
"""
def whitelist_face_image_upload(whitelistFace):
    token = request.headers.get('Token')
    user = module.token.get_user(token)
    f = request.files['file']
    location = module.file_module.file_upload(user, SchemaName.whitelistFaceImage, f)
    id = module.db_module.create_whitelist_face_image(whitelistFace, location)
    return id

"""
* Whitelist face image delete
"""
def delete_whitelist_face_image(_id):
    token = request.headers.get('Token')
    user = module.token.get_user(token)
    result = module.db_module.delete_whitelist_face_image(user, _id)
    return result

"""
* block character single upload
"""
def block_character_single_upload():
    token = request.headers.get('Token')
    user = module.token.get_user(token)
    f = request.files['file']
    location = module.file_module.file_upload(user, SchemaName.blockCharacter, f)
    id = module.db_module.create_block_character(user, location)
    return id

"""
* block character delete
"""
def delete_block_character_single(_id):
    token = request.headers.get('Token')
    user = module.token.get_user(token)
    result = module.db_module.delete_block_character(user, _id)
    return result

"""
* origin video upload - done
"""
def origin_video_upload():
    token = request.headers.get('Token')
    user = module.token.get_user(token)
    f = request.files['file']
    location = module.file_module.file_upload(user, SchemaName.video, f)
    id = module.db_module.create_video(user, location)
    return id

"""
* update video before save s3
"""
def update_video_upload(video_id):
    token = request.headers.get('Token')
    user = module.token.get_user(token)
    
    faceType = request.form['faceType']
    if faceType == FaceTypeClass.character:
        blockCharacterId = request.form['blockCharacterId']
    else:
        blockCharacterId = None
    whitelistFace = request.form['whitelistFace']
    
    result = module.db_module.update_db_video(video_id, user, faceType, blockCharacterId, whitelistFace)
    return result

"""
* update video after save s3
"""
def update_video_upload(video_id, user, location, status):
    module.db_module.update_location_video(video_id, user, location, status)
    
"""
* video delete
"""
def delete_video(_id):
    token = request.headers.get('Token')
    user = module.token.get_user(token)
    result=module.db_module.delete_video(user, _id)
    return result
