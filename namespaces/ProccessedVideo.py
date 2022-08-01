from flask import Response
import json
from module import crud_module
from flask_restx import Resource, Namespace

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

from app import common_counter,histogram
@ProccessedVideos.route('')
@ProccessedVideos.expect(parser)
@ProccessedVideos.doc(responses={200: 'Success'})
@ProccessedVideos.doc(responses={404: 'Failed'})
class ProccessedVideosClass(Resource):
    @common_counter
    @histogram
    def post(self):
        """
        # 프론트에서 백으로 수정할 비디오 정보 전달하면 샐러리에 전달
        # @header : token
        # @form-data :
            {
                필수 : "video_id" : "id",
                필수 : "whitelist_face_id" : ["id", "id"],
                필수 : "face_type" : "character or mosaic",
                선택 : "block_character_id" : "id",
            }
        # @return : {celeryId : "id"}
        """
        try:
            result, message = crud_module.update_video_upload()
            if result != False:
                return Response(
                    response = json.dumps(message),
                    status = 200,
                    mimetype = "application/json"
                )
            else:
                return Response(
                    response=json.dumps(message),
                    status=404,
                    mimetype="application/json"
                )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
    @common_counter
    @histogram       
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
            result, message = crud_module.get_multiple_after_video()
            if result != False:
                return Response(
                    response = json.dumps(message),
                    status = 200,
                    mimetype = "application/json"
                )
            else:
                return Response(
                    response=json.dumps(message),
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
    @common_counter
    @histogram
    def get(self, taskId):
        """
        # 셀러리 id를 통해 상태 체크 후 SUCCESS 이면 video 컬렉션의 status를 SUCCESS로 바꾸고 리턴
        # @header : token
        # @return : {status: "status"}
        """
        try:
            result, message = crud_module.get_after_video_status(taskId)
            if result != False:
                return Response(
                    response = json.dumps(message),
                    status = 200,
                    mimetype = "application/json"
                )
            elif result == False:
                return Response(
                    response=json.dumps(message),
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
    @common_counter
    @histogram
    def delete(self,videoId):
        """
        # '수정 후 비디오' 파일 한 개 삭제하기
        # @header : token
        # @return : 200 or 404
        """
        try:
            result, message = crud_module.delete_video(videoId)
            if result != False:
                return Response(
                    response = json.dumps(message),
                    status = 200,
                    mimetype = "application/json"
                )
            else:
                return Response(
                    response=json.dumps(message),
                    status=404,
                    mimetype="application/json"
                )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
