from flask import Response, request
import json
from static import status_code
from module import crud_module
from flask_restx import Resource, Namespace

####################################기존 캐릭터#######################################

OriginCharacters = Namespace(
    name="OriginCharacters",
    description="OriginCharacters CRUD를 작성하기 위해 사용하는 API.",
)

parser = OriginCharacters.parser()
parser.add_argument('token', location='headers')

@OriginCharacters.route('')
@OriginCharacters.expect(parser)
@OriginCharacters.doc(responses={200: 'Success'})
@OriginCharacters.doc(responses={404: 'Failed'})
class OriginCharactersClass(Resource):

    def get(self):
        """
        # 기존 케릭터 사진 url 가져오기
        # @header : token
        # @return : {originCharacterUrls : [file_url, file_url,  file_url]}
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
