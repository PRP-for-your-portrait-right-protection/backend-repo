from flask import Flask, Response, request
import json
from static import status_code
from module import file_module, user_module, crud_module
from flask_restx import Resource, Api, Namespace
from werkzeug.datastructures import FileStorage

####################################수정 후 비디오#######################################

AfterVideos = Namespace(
    name="AfterVideos",
    description="AfterVideos CRUD를 작성하기 위해 사용하는 API.",
)

parser = AfterVideos.parser()
parser.add_argument('token', location='headers')
parser.add_argument('file', type=FileStorage, location='files', required=False)
parser.add_argument('face_file', location='form', required=False)
parser.add_argument('video', location='form', required=False)
parser.add_argument('mode_method', location='form', required=False)
parser.add_argument('character_file', location='form', required=False)

@AfterVideos.route('')
@AfterVideos.expect(parser)
@AfterVideos.doc(responses={200: 'Success'})
@AfterVideos.doc(responses={404: 'Failed'})
class AfterVideosClass(Resource):

    def post(self):
        """
        # 프론트에서 백으로 수정할 비디오 정보 전달하면 샐러리에 전달
        # @header : token
        # @form-data :
            {
                "whitelist_face_id" : "id",
                "whitelist_face_image_url": [url, url, url, url],   # (required)
                "video_url": url,                                   # (required)
                "faceType": "character" or "mosaic",                # (required)
                "block_character_id": "id"
            }
        # @return : {celeryId : "id"}
        """
        try:
            # db에 저장(update) / 셀러리에 원본 동영상, 모자이크 캐릭터 유무, 캐릭터 url, 화이트리스트 이미지 / update

            # db에 저장 -> 셀러리 호출 -> task_id 리턴
            taskId = crud_module.update_video_upload()

            if taskId != False:
                return Response(
                    response = json.dumps(taskId),
                    status = 200,
                    mimetype = "application/json"
                )
            else:
                return Response(
                    response=json.dumps(
                        {
                            "message":status_code.file_download_02_fail,
                        }
                    ),
                    status=404,
                    mimetype="application/json"
                )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
            
    def get(self):
        """
        # 특정 유저에 대한 비디오 결과 모두 조회하기 -> 태원님께서 taskid 리스트를 돌면서 하나하나 api를 호출한다고 하셨기
        # 때문에 한 번에 하나의 결과만 조회하도록 하였음
        # @header : token
        # @return : {afterVideoUrls: ["url", "url", "url", ...]}
        """
        try:
            # task id를 가져옴
            taskId = request.args.get('task_id')

            # task id를 넘겨주고 상태를 체크함 -> 상태가 SUCCESS이면 db에 저장하고 url을 리턴
            result = crud_module.read_celery_task_status(taskId)

            if result != False:
                return Response(
                    response = json.dumps(result),
                    status = 200,
                    mimetype = "application/json"
                )
            else:
                return Response(
                    response=json.dumps(
                        {
                            "message":status_code.file_download_02_fail,
                        }
                    ),
                    status=404,
                    mimetype="application/json"
                )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")

# 궁금한 점
    # 1. 프론트에서 비디오 처리 요청
    # 2. 백엔드에서 처리 요청을 받으면 프론트로 taskId리턴
    # 3. 프론트에서 taskId의 status를 체크하는 api를 호출
    # 4. 백엔드에서 status가 <PENDING, FAILURE> 중 하나 이면 그래도 리턴 / SUCCESS이면 버켓 URL 리턴 (Ai에서 버켓에 저장)
        # ------> 그러면
            # 지금 현재 플라스크에는 수현님께서 작성해놓으신
            # <task를 요청하는 api, 상태를 체크하는 api, 버켓 url을 db에 저장하는 api>가 있는데
            # 프론트에서 3가지를 다 호출하는 지?
            # task를 요청하는 api에서는 정보를 넘겨주지만
            # 상태를 체크하는 api에서는 넘겨주지 않는다
            # 버켓 url을 db에 저장하는 api에서도 넘겨줄 수 있나? --> db도큐먼트를 불러오는데 정보가 필요함
@AfterVideos.route('/status/<taskId>')
@AfterVideos.doc(responses={200: 'Success'})
@AfterVideos.doc(responses={404: 'Failed'})
class AfterVideosCeleryStatusCheckClass(Resource):

    def get(self, taksId):
        """
        # ai 작업 후 버킷 url을 돌려주면 db에 저장하는 과정 상태체크 후 현재상태 return 
        # @header : token
        # @return : {status: "status"}
        """
        try:
            result = crud_module.update_video_upload(taskId)

            if result != False:
                return Response(
                    response = json.dumps(result),
                    status = 200,
                    mimetype = "application/json"
                )
            else:
                return Response(
                    response=json.dumps(
                        {
                            "message":status_code.file_download_02_fail,
                        }
                    ),
                    status=404,
                    mimetype="application/json"
                )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")

@AfterVideos.route('/<videoId>')
@AfterVideos.doc(responses={200: 'Success'})
@AfterVideos.doc(responses={404: 'Failed'})
class AfterVideosOneCheckClass(Resource):

    def delete(self):
        """
        # '수정 후 비디오' 파일 한 개 삭제하기
        # @header : token
        # @return : 200 or 404
        """
        try:
            result = crud_module.single_get("get_origin_character")
            if result != False:
                return Response(
                    response = json.dumps(result),
                    status = 200,
                    mimetype = "application/json"
                )
            else:
                return Response(
                    response=json.dumps(
                        {
                            "message":status_code.file_download_02_fail,
                        }
                    ),
                    status=404,
                    mimetype="application/json"
                )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
