from flask import request
from datetime import datetime
from db.enum_classes import ScopeClass, StatusClass, FaceTypeClass, SchemaName
import module

"""
* whitelist face upload
"""
def whitelist_face_upload():
    token = request.headers.get('token')
    user = module.token.get_user(token)
    
    names = request.form['name']
    for name in names:
        module.db_module.create_whitelist_face(user, name)

"""
* whitelist face image single upload
"""
def whitelist_face_image_single_upload(whitelistFace):
    token = request.headers.get('token')
    user = module.token.get_user(token)
    
    f = request.files['file']
    
    location = module.file_module.file_upload(user, SchemaName.whitelistFaceImage, f)
    module.db.create_whitelist_face_image(whitelistFace, location)
    
"""
* whitelist face image multi upload
"""
def whitelist_face_image_multi_upload(whitelistFace):
    token = request.headers.get('token')
    user = module.token.get_user(token)
    
    f = request.files['file']
    
    location = module.file_module.file_upload(user, SchemaName.whitelistFaceImage, f)
    module.db.create_whitelist_face_image(whitelistFace, location)
    
"""
* block character single upload - done
"""
def block_character_single_upload():
    token = request.headers.get('token')
    user = module.token.get_user(token)
    
    f = request.files['file']
    
    location = module.file_module.file_upload(user, SchemaName.blockCharacter, f)
    module.db.create_block_character(user, location)

"""
* origin video upload - done
"""
def origin_video_upload():
    token = request.headers.get('token')
    user = module.token.get_user(token)
    
    f = request.files['file']
    
    location = module.file_module.file_upload(user, SchemaName.video, f)
    module.db.create_video(user, location)

"""
* update video before save s3
"""
def update_video_upload():
    token = request.headers.get('token')
    user = module.token.get_user(token)
    
    # location = module.file_module.file_upload(user, SchemaName.blockCharacter, f)
    # module.db.create_block_character(user, location)

"""
* update video after save s3
"""
def update_video_upload():
    token = request.headers.get('token')
    user = module.token.get_user(token)
    
    faceType = request.form['faceType']
    if faceType == FaceTypeClass.character:
        blockCharacterId = request.form['blockCharacterId']
    else:
        blockCharacterId = None
    whitelistFace = request.form['whitelistFace']
    
    module.db.update_db_video(user, faceType, blockCharacterId, whitelistFace)
    
