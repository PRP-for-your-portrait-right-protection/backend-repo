from flask import request, jsonify 
from datetime import datetime
from bson import ObjectId
from db.enum_classes import ScopeClass, StatusClass, FaceTypeClass, SchemaName
import module
from module import db_module, file_module
from celery import Celery

celery = Celery('celery-repo',
    broker = "amqp://admin:mypass@rabbitmq:5672",
    backend = "mongodb://db:27017/silicon"
) 

################### WHITELIST FACE ###################

"""
* whitelist face upload - done
"""
def upload_whitelist_face():
    token = request.headers.get('Token')
    user = module.token.get_user(token)
    if user == False:
        return False
    name = request.form['name']
    id = db_module.create_whitelist_face(user, name)
    return {"id" : id}

"""
* WhitelistFace update - done
"""
def update_whitelist_face(_id):
    token = request.headers.get('Token')
    user = module.token.get_user(token)
    if user == False:
        return False
    name = request.form['face_name_after']
    result = module.db_module.update_whitelist_face(user, _id, name)
    if result == False:
        return False
    return result

"""
* WhitelistFace delete - done
"""
def delete_whitelist_face(_id):
    token = request.headers.get('Token')
    user = module.token.get_user(token)
    if user == False:
        return False
    result = module.db_module.delete_whitelist_face(user, _id)
    if result == False:
        return False
    return result

################### WHITELIST FACE IMAGE ###################

"""
* whitelist face image upload
"""
def whitelist_face_image_upload(whitelistFace):
    token = request.headers.get('Token')
    user = module.token.get_user(token)
    if user == False:
        return False
    f = request.files['file']
    location = file_module.file_upload(user, SchemaName.whitelistFaceImage, f)
    if location == False:
        return False
    id = module.db_module.create_whitelist_face_image(whitelistFace, location)
    return {"id" : id}

"""
* whitelist face image get
"""
def get_whitelist_face_image():
    token = request.headers.get("Token")
    user = module.token.get_user(token)
    if user == False:
        return False
    result = module.db_module.read_whitelist_face_image(user)
    if result == None:
        result = False
    return result

"""
* Whitelist face image delete
"""
def delete_whitelist_face_image(whitelistFaceId, _id):
    token = request.headers.get('Token')
    user = module.token.get_user(token)
    if user == False:
        return False
    result = module.db_module.delete_whitelist_face_image(whitelistFaceId, _id)
    if result == False:
        return False
    return result

################### BLOCK CHARACTER ###################

"""
* origin block character get
"""
def get_origin_block_character():
    token = request.headers.get("Token")
    user = module.token.get_user(token)
    if user == False:
        return False
    result = module.db_module.read_origin_block_character()

    if result != None:
        return result

"""
* user block character upload
"""
def upload_user_block_character():
    token = request.headers.get('Token')
    user = module.token.get_user(token)
    if user == False:
        return False
    f = request.files['file']
    location = file_module.file_upload(user, SchemaName.blockCharacter, f)
    if location == False:
        return False
    id = module.db_module.create_block_character(user, location)
    return {"id" : id}

"""
* user block character get
"""
def get_user_block_character():
    token = request.headers.get("Token")
    user = module.token.get_user(token)
    if user == False:
        return False
    result = module.db_module.read_user_block_character(user)

    if result != None:
        return result

"""
* user block character delete
"""
def delete_user_block_character(_id):
    token = request.headers.get('Token')
    user = module.token.get_user(token)
    if user == False:
        return False
    result = module.db_module.delete_block_character(user, _id)
    if result == False:
        return False
    return result

################### VIDEO ###################

"""
* origin video upload - done
"""
def origin_video_upload():
    token = request.headers.get('Token')
    user = module.token.get_user(token)
    if user == False:
        return False
    f = request.files['file']
    location = file_module.file_upload(user, SchemaName.video, f)
    if location == False:
        return False
    id = module.db_module.create_video(user, location)
    return {"id" : id}

"""
* update video before save s3
"""
def update_video_upload(video_id):
    token = request.headers.get('Token')
    user = module.token.get_user(token)
    if user == False:
        return False
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
# def update_video_upload(video_id, user, location, status):
#     module.db_module.update_video_celery(video_id, user, location, status)
    
"""
* video delete
"""
def delete_video(_id):
    token = request.headers.get('Token')
    user = module.token.get_user(token)
    if user == False:
        return False
    result=module.db_module.delete_video(user, _id)
    if result == False:
        return False
    return result

"""
* update video before save s3
"""
def update_video_upload():
    token = request.headers.get('Token')

    # user_id (Object_id) 가져옴 -> 정확히는 오브젝트를 가져옴 -> 도트연산자 접근
    user = module.token.get_user(token)
    if user == False:
        return False
    
    # video id가져옴
    videoId = request.form["videoId"]

    # video url 찾기
    videoUrl = module.db_module.read_video_url(videoId, user)

    # faceType 가져옴
    faceType = request.form['faceType']

    # blockCharacterId 선택적으로 가져옴
    if faceType == FaceTypeClass.character:
        blockCharacterId = request.form['blockCharacterId'] 
    else:
        blockCharacterId = None
    
    whitelistFaceId = request.form.getlist["whitelist_face_id"]
    
    # True or False 리턴
    result = module.db_module.update_video(videoId, user, faceType, blockCharacterId, whitelistFaceId)

    if result == True:
        # 키 이름은 나중에 수정 필요
        # ai에 요청하게 될 부분임
        task = celery.send_task('tasks.test_celery', kwargs=
            {
                'b' : faceType, # 모자이크 또는 캐릭터
                'c' : whitelistFace, # url 리스트
                'd' : blockCharacterId, # url로 가져와야함
                # 'a' : video_id,
                'e' : videoUrl
            })
        # taskId 리턴

        module.db_module.update_celeryId_video(videoId, user, task.id, task.status)

        return task.id
    else:
        return False

"""
* 셀러리 id를 통해 상태 체크
"""
def get_after_video_status(taskId):
    token = request.headers.get("Token")
    user = module.token.get_user(token)
    if user == False:
        return False
    result = module.db_module.get_after_video_status(user, taskId)

    if result != None:
        return result
    
"""
* 특정 유저에 대한 비디오 결과 모두 조회하기
"""
def get_multiple_after_video():
    token = request.headers.get("Token")
    user = module.token.get_user(token)
    if user == False:
        return False
    result = module.db_module.read_multiple_after_video(user)

    if result != None:
        return result

"""
* read celery task status
"""
def read_celery_task_status(taskId):
    status = celery.AsyncResult(taskId, app=celery)
    if status == StatusClass.success:
        result = celery.AsyncResult(taskId).result
        return result
    else:
        return status
