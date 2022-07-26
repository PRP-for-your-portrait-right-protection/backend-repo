from flask import request, jsonify
from datetime import datetime
from db.enum_classes import ScopeClass, StatusClass, FaceTypeClass, SchemaName
# import module이 인식이 안되서 바꿈 -> 해결방법?
from module import token, db_module
from celery import Celery

celery = Celery('celery-repo',
    broker = "amqp://admin:mypass@rabbitmq:5672",
    backend = "mongodb://db:27017/silicon"
)

"""
* whitelist face upload
"""
def whitelist_face_upload(data, user, name):
    whitelistFace = module.db_module.create_whitelist_face(user, name)
    if data.files["whitelistFace"].filename != "":
        files = data.files.getlist('file')
        for f in files:
            whitelist_face_image_single_upload(user, whitelistFace, f)
"""
* whitelist face image upload
"""
def whitelist_face_image_upload(user, whitelistFace, f):
    location = module.file_module.file_upload(user, SchemaName.whitelistFaceImage, f)
    module.db.create_whitelist_face_image(whitelistFace, location)
"""
* whitelist face image single upload - done
"""
def whitelist_face_image_single_upload(whitelistFace):
    token = request.headers.get('token')
    user = module.token.get_user(token)
    f = request.files('file')
    whitelist_face_image_upload(user, whitelistFace, f)
"""
* whitelist face image multi upload
"""
def whitelist_face_image_multi_upload():
    token = request.headers.get('token')
    user = module.token.get_user(token)
    data = request.form['data']
    print(data)
    for name in data:
        print(name)
        whitelist_face_upload(data, user, name.name)
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
    video_id = module.db.create_video(user, location)
    return video_id


"""
* update video before save s3
"""
def update_video_upload():
    # headers.get에서 첫글자 대문자로 해야함
    # 토큰을 가져옴
    # module의 token과 이름이 겹쳐서, token_으로 하였음
    token_ = request.headers.get('Token')

    # user_id (Object_id) 가져옴 -> 정확히는 오브젝트를 가져옴 -> 도트연산자 접근
    user = token.get_user(token_)

    # video id가져옴
    videoId = request.form["videoId"]

    # video url 찾기
    videoUrl = db_module.read_video_url(videoId, user)

    # faceType 가져옴
    faceType = request.form['faceType']

    # blockCharacterId 선택적으로 가져옴
    if faceType == FaceTypeClass.character:
        blockCharacterId = request.form['blockCharacterId'] 
    else:
        blockCharacterId = None
        whitelistFaceId = request.form.getlist["whitelist_face_id"]
        whitelistFace = request.form.getlist['whitelist_face_image_url']

    # True or False 리턴
    result = db_module.update_db_video(videoId, user, faceType, blockCharacterId, whitelistFace)

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

        db_module.update_celeryId_video(videoId, user, task.id, task.status)

        return task.id
    else:
        return False

"""
* update video before after s3
* 버켓에 저장하고 난뒤 vid
"""
################################### READ ######################################

"""
* 여러 사람 여러 사진 url 가져오기
"""
def get_multiple_id_img():
    token_ = request.headers.get("Token")
    userId = token.get_user(token_)

    result = db_module.read_whitelistFaceIdAndUrl(userId)

    if result != None:
        return result

"""
* 기존 캐릭터 사진 url 가져오기
"""
def get_origin_character():
    token_ = request.headers.get("Token")
    userId = token.get_user(token_)

    result = db_module.read_origin_character_url(userId)

    if result != None:
        return result

"""
* 유저 캐릭터 여러 개 url 가져오기
"""
def get_multiple_user_character():
    token_ = request.headers.get("Token")
    userId = token.get_user(token_)

    result = db_module.read_multiple_user_character(userId)

    if result != None:
        return result
"""
* 셀러리 id를 통해 상태 체크
"""
def get_after_video_status(taskId):
    token_ = request.headers.get("Token")
    userId = token.get_user(token_)

    result = db_module.get_after_video_status(userId, taskId)

    if result != None:
        return result
    

"""
* 특정 유저에 대한 비디오 결과 모두 조회하기
"""
def get_multiple_after_video():
    token_ = request.headers.get("Token")
    userId = token.get_user(token_)
    
    result = db_module.read_multiple_after_video(userId)

    if result != None:
        return result

"""
* read celery task status
"""
def read_celery_task_status(taskId):
    status = celery.AsyncResult(taskId, app=celery)
    if status == "SUCCESS":
        result = celery.AsyncResult(taskId).result
        return result
    else:
        return status