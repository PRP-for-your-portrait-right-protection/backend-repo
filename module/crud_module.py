from flask import request 
from db.enum_classes import ScopeClass, StatusClass, FaceTypeClass, SchemaName
import module
from static import status_code
from module import db_module, file_module
from celery import Celery

# celery = Celery('celery-repo',
#     broker='amqp://localhost:5672',
#     result_backend='mongodb://localhost:27017/',
#     mongodb_backend_settings = {
#         'database': 'silicon',
#         'taskmeta_collection': 'celery'
#     }
# )
celery = Celery('celery-repo',
    broker='amqp://admin:mypass@rabbitmq:5672',
    result_backend='mongodb://db:27017/',
    mongodb_backend_settings = {
        'database': 'silicon',
        'taskmeta_collection': 'celery'
    }
)

################### WHITELIST FACE ###################

"""
* whitelist face upload
"""
def upload_whitelist_face():
    try:
        token = request.headers.get('Token')
        user = module.token.get_user(token)
        if user == False:
            return False, {"error": status_code.token_error}
        name = request.form.get('name')
        if name == None or name == '':
            return False, {"error": f'{status_code.field_error}name'}
        result, message = db_module.create_whitelist_face(user, name)
        return result, message
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}

"""
* WhitelistFace update
"""
def update_whitelist_face(_id):
    try:
        token = request.headers.get('Token')
        user = module.token.get_user(token)
        if user == False:
            return False, {"error": status_code.token_error}
        name = request.form.get('face_name_after')
        if name == None or name == '':
            return False, {"error": f'{status_code.field_error}face_name_after'}
        result, message = module.db_module.update_whitelist_face(user, _id, name)
        return result, message
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}     

"""
* WhitelistFace delete
"""
def delete_whitelist_face(_id):
    try:
        token = request.headers.get('Token')
        user = module.token.get_user(token)
        if user == False:
            return False, {"error": status_code.token_error}
        result, message = module.db_module.delete_whitelist_face(user, _id)
        return result, message
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}

################### WHITELIST FACE IMAGE ###################

"""
* whitelist face image upload
"""
def whitelist_face_image_upload(whitelistFace):
    try:
        token = request.headers.get('Token')
        user = module.token.get_user(token)
        if user == False:
            return False, {"error": status_code.token_error}
        if 'file' not in request.files:
            return False, {"error": f'{status_code.field_error}file'}
        filename = request.files['file'].filename
        if filename == None or filename == '':
            return False, {"error": f'{status_code.field_error}file'}
        f = request.files['file']
        fileResult, location = file_module.file_upload(user, SchemaName.whitelistFaceImage.value, f)
        if fileResult == False:
            return fileResult, location
        result, message = module.db_module.create_whitelist_face_image(whitelistFace, location)
        return result, message
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}
    
"""
* whitelist face image get
"""
def get_whitelist_face_image():
    try:
        token = request.headers.get("Token")
        user = module.token.get_user(token)
        if user == False:
            return False, {"error": status_code.token_error}
        result, message = module.db_module.read_whitelist_face_image(user)
        return result, message
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}

"""
* Whitelist face image delete
"""
def delete_whitelist_face_image(whitelistFaceId, _id):
    try:
        token = request.headers.get('Token')
        user = module.token.get_user(token)
        if user == False:
            return False, {"error": status_code.token_error}
        result, message = module.db_module.delete_whitelist_face_image(whitelistFaceId, _id)
        return result, message
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}

################### BLOCK CHARACTER ###################

"""
* origin block character get
"""
def get_origin_block_character():
    try:
        token = request.headers.get("Token")
        user = module.token.get_user(token)
        if user == False:
            return False, {"error": status_code.token_error}
        result, message = module.db_module.read_origin_block_character()
        return result, message
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}

"""
* user block character upload
"""
def upload_user_block_character():
    try:
        token = request.headers.get('Token')
        user = module.token.get_user(token)
        if user == False:
            return False, {"error": status_code.token_error}
        if 'file' not in request.files:
            return False, {"error": f'{status_code.field_error}file'}
        filename = request.files['file'].filename
        if filename == None or filename == '':
            return False, {"error": f'{status_code.field_error}file'}
        f = request.files['file']
        fileResult, location = file_module.file_upload(user, SchemaName.blockCharacter.value, f)
        if fileResult == False:
            return fileResult, location
        result, message = module.db_module.create_block_character(user, location)
        return result, message
    except Exception as ex:    
        print(ex)
        return False, {"error": str(ex)}

"""
* user block character get
"""
def get_user_block_character():
    try:
        token = request.headers.get("Token")
        user = module.token.get_user(token)
        if user == False:
            return False, {"error": status_code.token_error}
        result, message = module.db_module.read_user_block_character(user)
        return result, message
    except Exception as ex:    
        print(ex)
        return False, {"error": str(ex)}

"""
* user block character delete
"""
def delete_user_block_character(_id):
    try:
        token = request.headers.get('Token')
        user = module.token.get_user(token)
        if user == False:
            return False, {"error": status_code.token_error}
        result, message = module.db_module.delete_block_character(user, _id)
        return result, message
    except Exception as ex:    
        print(ex)
        return False, {"error": str(ex)}

################### VIDEO ###################

"""
* origin video upload
"""
def origin_video_upload():
    try:
        token = request.headers.get('Token')
        user = module.token.get_user(token)
        if user == False:
            return False, {"error": status_code.token_error}
        if 'file' not in request.files:
            return False, {"error": f'{status_code.field_error}file'}
        filename = request.files['file'].filename
        if filename == None or filename == '':
            return False, {"error": f'{status_code.field_error}file'}
        f = request.files['file']
        fileResult, location = file_module.file_upload(user, SchemaName.video.value, f)
        if fileResult == False:
            return fileResult, location
        result, message = module.db_module.create_video(user, location)
        if result:
            return result, {"id" : message, "url": location}
        else:
            return result, message
    except Exception as ex:    
        print(ex)
        return False, {"error": str(ex)}
    
"""
* video delete
"""
def delete_video(_id):
    try:
        token = request.headers.get('Token')
        user = module.token.get_user(token)
        if user == False:
            return False, {"error": status_code.token_error}
        result, message = db_module.delete_video(user, _id)
        return result, message
    except Exception as ex:    
        print(ex)
        return False, {"error": str(ex)}

"""
* update video before save s3
"""
def update_video_upload():
    try:
        token = request.headers.get('Token')
        user = module.token.get_user(token)
        if user == False:
            return False, {"error": status_code.token_error}
        
        # video id가져옴
        videoId = request.form.get('video_id')
        if videoId == None or videoId == '':
            return False, {"error": f'{status_code.field_error}video_id'}

        # video url 찾기
        result, videoUrl = db_module.read_origin_video(videoId, user)
        if result == False:
            return result, videoUrl

        # faceType 가져옴
        faceType = request.form.get('face_type')
        if faceType == None or faceType == '':
            return False, {"error": f'{status_code.field_error}face_type'}
        
        if faceType != FaceTypeClass.character.value and faceType != FaceTypeClass.mosaic.value:
            return False, {"error": f'{status_code.enum_class_error}face_type'}

        # blockCharacterId 선택적으로 가져옴
        if faceType == FaceTypeClass.character.value:
            blockCharacterId = request.form.get('block_character_id')
            if blockCharacterId == None or blockCharacterId == '':
                return False, {"error": f'{status_code.field_error}block_character_id'}
            result, blockCharacterImg = db_module.read_block_character_url(blockCharacterId)
            if result == False:
                return result, blockCharacterImg
        else:
            blockCharacterId = None
            blockCharacterImg = None
        
        # TODO - whitelistFaceId 없을 경우에 대한 것 처리하기
        whitelistFaceId = request.form.getlist("whitelist_face_id")
        result, whitelistFaceImgList = db_module.read_whitelist_face_url(user, whitelistFaceId)
        if result == False:
            return result, whitelistFaceImgList

        # True or False 리턴
        result, message = db_module.update_video(videoId, user, faceType, whitelistFaceId, blockCharacterId) # ID를 받아와서 찾은다음에 url

        if result == True:
            if faceType == FaceTypeClass.mosaic.value:
                task = celery.send_task('tasks.run_mosaic', kwargs= 
                    {
                        'whitelistFaceImgList' : whitelistFaceImgList, # url 리스트
                        'videoUrl' : videoUrl,
                        "user" : str(user)
                    })
                result2, message = db_module.update_video_celery(videoId, user, task, task.status)

                if result2 == True:
                    return True, {"id" : str(task.id)}
                else:
                    return False, {"error":status_code.update_02_fail}
            elif faceType == FaceTypeClass.character.value:
                task = celery.send_task('tasks.run_character', kwargs=
                    {
                        'whitelistFaceImgList' : whitelistFaceImgList, 
                        'blockCharacterImgUrl' : blockCharacterImg, 
                        'videoUrl' : videoUrl,
                        "user" : str(user)
                    })
                result2 = db_module.update_video_celery(videoId, user, task, task.status)

                if result2 == True:
                    return True, {"id" : str(task.id)}
                else:
                    return False, {"error":status_code.update_02_fail}
        else:
            return result, message
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}

"""
* 셀러리 id를 통해 상태 체크
"""
def get_after_video_status(taskId):
    try:
        token = request.headers.get("Token")
        user = module.token.get_user(token)
        if user == False:
            return False, {"error": status_code.token_error}
        result, message = db_module.read_celery_status(user, taskId)
        if message == StatusClass.failure.value:
            status = celery.AsyncResult(taskId, app=celery)
            result2 = db_module.update_video_celery_failure(user, taskId) #video컬렉션의 status를 FAILURE로 업데이트
            if result2 == True:
                return True, {"status" : StatusClass.failure.value} #셀러리의 결과과 failure이고, video 컬렉션의 status 업데이트를 성공한 경우
            else:
                return False, {"error", status_code.update_02_fail} #셀러리의 결과과 failure이고, video 컬렉션의 status 업데이트를 실패한 경우
        elif result == 0:
                return True, {"status" : StatusClass.pending.value} #PENDING
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}
    
"""
* 특정 유저에 대한 비디오 결과 모두 조회하기
"""
def get_multiple_after_video():
    try:
        token = request.headers.get("Token")
        user = module.token.get_user(token)
        if user == False:
            return False, {"error": status_code.token_error}
        result, message = module.db_module.read_proccessed_video(user)
        return result, message
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}

"""
* read celery task status
"""
def read_celery_task_status(taskId):
    try:
        status = celery.AsyncResult(taskId, app=celery)
        if status == StatusClass.success:
            result = celery.AsyncResult(taskId).result
            return True, {"status", result}
        else:
            return False, {"status", status}
    except Exception as ex:
        print(ex)
        return False, {"error": str(ex)}
