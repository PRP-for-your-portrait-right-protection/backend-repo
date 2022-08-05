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

@OriginVideos.route('')
@OriginVideos.expect(parser)
@OriginVideos.doc(responses={200: 'Success'})
@OriginVideos.doc(responses={404: 'Failed'})
class OriginVideosClass(Resource):

    def post(self):
        """
        # 수정 전 비디오 파일 버킷에 저장 후 DB INSERT
        # @header : token
        # @form-data : <file>
        # @return : {id : "id", url: "url"}
        """
        try:
            result, message = crud_module.origin_video_upload()
            return Response(
                response = json.dumps(message),
                status = result,
                mimetype = "application/json"
            )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
