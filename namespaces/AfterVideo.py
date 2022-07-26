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
        # 특정 유저에 대한 비디오 결과 모두 조회하기
        # @header : token
        # @return : {afterVideoUrls: ["url", "url", "url", ...]}
        """
        try:
            result = crud_module.get_multiple_after_video()

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

@AfterVideos.route('/status/<taskId>')
@AfterVideos.doc(responses={200: 'Success'})
@AfterVideos.doc(responses={404: 'Failed'})
class AfterVideosCeleryStatusCheckClass(Resource):

    def get(self, taskId):
        """
        # 셀러리 id를 통해 상태 체크
        # @header : token
        # @return : {status: "status"}
        """
        try:
            result = crud_module.get_after_video_status(taskId)

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
