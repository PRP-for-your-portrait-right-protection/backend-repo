from flask import Flask, Response, request
import json
from static import status_code
from module import crud_module
from flask_restx import Resource, Api, Namespace

####################################수정 후 비디오#######################################

ProccessedVideos = Namespace(
    name="ProccessedVideos",
    description="ProccessedVideos CRUD를 작성하기 위해 사용하는 API.",
)

parser = ProccessedVideos.parser()
parser.add_argument('token', location='headers')
parser.add_argument('video_id', location='form', required=False)
parser.add_argument('whitelist_face_id', location='form', required=False)
parser.add_argument('faceType', location='form', required=False)
parser.add_argument('block_character_id', location='form', required=False)

@ProccessedVideos.route('')
@ProccessedVideos.expect(parser)
@ProccessedVideos.doc(responses={200: 'Success'})
@ProccessedVideos.doc(responses={404: 'Failed'})
class ProccessedVideosClass(Resource):
    def post(self):
        """
        # 프론트에서 백으로 수정할 비디오 정보 전달하면 샐러리에 전달
        # @header : token
        # @form-data :
            {
                필수 : "video_id" : "id",
                필수 : "whitelist_face_id" : ["id", "id"],
                필수 : "faceType" : "character or mosaic",
                선택 : "block_character_id" : "id",
            }
        # @return : {celeryId : "id"}
        """
        try:
            result = crud_module.update_video_upload()
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
            
    def get(self):
        '''
        # 특정 유저에 대한 비디오 결과 모두 조회하기
        # @header : token
        # @return : 
                {
                    data : [
                        {id : "id", url: "url"},
                        {id : "id", url: "url"}
                    ]
                }
        '''
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

@ProccessedVideos.route('/status/<taskId>')
@ProccessedVideos.doc(responses={200: 'Success'})
@ProccessedVideos.doc(responses={404: 'Failed'})
class ProccessedVideosCeleryStatusCheckClass(Resource):
    def get(self, taskId):
        """
        # ai 작업 후 버킷 url을 돌려주면 db에 저장하는 과정 상태체크 후 현재상태 return
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

@ProccessedVideos.route('/<videoId>')
@ProccessedVideos.doc(responses={200: 'Success'})
@ProccessedVideos.doc(responses={404: 'Failed'})
class ProccessedVideosOneCheckClass(Resource):
    def delete(self,videoId):
        """
        # '수정 후 비디오' 파일 한 개 삭제하기
        # @header : token
        # @return : 200 or 404
        """
        try:
            result = crud_module.delete_video(videoId)
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
                            "message":status_code.file_remove_02_fail,
                        }
                    ),
                    status=404,
                    mimetype="application/json"
                )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")