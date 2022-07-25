from flask import Flask, Response, request
import json
from static import status_code
from module import file_module, member_module, crud_module
from flask_restx import Resource, Api, Namespace
from werkzeug.datastructures import FileStorage

####################################수정 전 비디오#######################################

BeforeVideos = Namespace(
    name="BeforeVideos",
    description="BeforeVideos CRUD를 작성하기 위해 사용하는 API.",
)

parser = BeforeVideos.parser()
parser.add_argument('token', location='headers')
parser.add_argument('file', type=FileStorage, location='files', required=False)

@BeforeVideos.route('')
@BeforeVideos.expect(parser)
@BeforeVideos.doc(responses={200: 'Success'})
@BeforeVideos.doc(responses={404: 'Failed'})
class BeforeVideosClass(Resource):

    def post(self):
        """
        # 수정 전 비디오 파일 버킷에 저장 후 DB INSERT
        # @header : token
        # @form-data : <file>
        # @return : {beforeVideosUrl : "url"}
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
