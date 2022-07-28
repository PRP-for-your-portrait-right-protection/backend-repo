from flask import request, jsonify 
from datetime import datetime
from bson import ObjectId
from db.enum_classes import ScopeClass, StatusClass, FaceTypeClass, SchemaName
import module
from module import db_module, file_module
from celery import Celery


celery = Celery('celery-repo',
    broker='amqp://localhost:5672',
    result_backend='mongodb://localhost:27017/',
    mongodb_backend_settings = {
        'database': 'silicon',
        'taskmeta_collection': 'celery'
    }
)
# celery = Celery('celery-repo',
#     broker='amqp://admin:mypass@rabbitmq:5672',
#     result_backend='mongodb://db:27017/',
#     mongodb_backend_settings = {
#         'database': 'silicon',
#         'taskmeta_collection': 'celery'
#     }
# )

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
    return {"id" : id, "url": location}

# """
# * update video before save s3
# """
# def update_video_upload(video_id):
#     token = request.headers.get('Token')
#     user = module.token.get_user(token)
#     if user == False:
#         return False
#     faceType = request.form['faceType']
#     if faceType == FaceTypeClass.character:
#         blockCharacterId = request.form['block_character_id']
#     else:
#         blockCharacterId = None
#     whitelistFace = request.form['whitelist_Face']
    
#     result = db_module.update_video(video_id, user, faceType, blockCharacterId, whitelistFace)
#     return result

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
    # result=module.db_module.delete_video(user, _id)
    result=db_module.delete_video(user, _id)
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
    videoId = request.form["video_id"]

    # video url 찾기
    videoUrl = db_module.read_origin_video(videoId, user)

    # faceType 가져옴
    faceType = request.form['face_type']

    # blockCharacterId 선택적으로 가져옴
    if faceType == FaceTypeClass.character.value:
        blockCharacterId = request.form['block_character_id']
        blockCharacterImg = db_module.read_block_character_url(blockCharacterId)
        print(blockCharacterImg)
    else:
        blockCharacterImg = None
        blockCharacterId = None
    
    whitelistFaceId = request.form.getlist("whitelist_face_id") #이미지 없을경우 예외처리
    whitelistFaceImgList = db_module.read_whitelist_face_url(user, whitelistFaceId)

    # True or False 리턴
    result = db_module.update_video(videoId, user, faceType, whitelistFaceId, blockCharacterId) # ID를 받아와서 찾은다음에 url

    if result == True:
        # 키 이름은 나중에 수정 필요
        # ai에 요청하게 될 부분임
        task = celery.send_task('tasks.test_celery', kwargs=
            {
                'faceType' : faceType, # 모자이크 또는 캐릭터
                'whitelistFaceImgList' : whitelistFaceImgList, # url 리스트
                'blockCharacterImgUrl' : blockCharacterImg, # url로 가져와야함
                'videoUrl' : videoUrl,
                "user" : str(user)
            })
        # taskId 리턴
        db_module.update_video_celery(videoId, user, task, task.status)

        return {"id" : str(task.id)}
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

    result = db_module.read_celery_status(user, taskId)

    if result != None:
        return {"status" : result}
    
"""
* 특정 유저에 대한 비디오 결과 모두 조회하기
"""
def get_multiple_after_video():
    token = request.headers.get("Token")

    user = module.token.get_user(token)

    if user == False:
        return False

    result = module.db_module.read_proccessed_video(user)

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
