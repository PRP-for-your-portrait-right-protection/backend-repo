from flask import Response
import json
from module import crud_module
from flask_restx import Resource, Namespace
from werkzeug.datastructures import FileStorage

####################################수정 전 비디오#######################################

OriginVideos = Namespace(
    name="OriginVideos",
    description="OriginVideos CRUD를 작성하기 위해 사용하는 API.",
)

parser = OriginVideos.parser()
parser.add_argument('token', location='headers')
parser.add_argument('file', type=FileStorage, location='files', required=False)

from app import common_counter,histogram
@OriginVideos.route('')
@OriginVideos.expect(parser)
@OriginVideos.doc(responses={200: 'Success'})
@OriginVideos.doc(responses={404: 'Failed'})
class OriginVideosClass(Resource):
    @common_counter
    @histogram
    def post(self):
        """
        # 수정 전 비디오 파일 버킷에 저장 후 DB INSERT
        # @header : token
        # @form-data : <file>
        # @return : {id : "id", url: "url"}
        """
        try:
            result, message = crud_module.origin_video_upload()
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
