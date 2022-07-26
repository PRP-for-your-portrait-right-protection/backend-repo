from flask import Flask, Response, request
import json
from static import status_code
from module import crud_module
from flask_restx import Resource, Api, Namespace
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
        # @return : {id : "id"}
        """
        try:
            result = crud_module.origin_video_upload()
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