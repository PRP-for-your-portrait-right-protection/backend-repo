from flask import Response, request
import json
from static import status_code
from module import crud_module
from flask_restx import Resource, Namespace
from werkzeug.datastructures import FileStorage

####################################유저 캐릭터#######################################

UserCharacters = Namespace(
    name="UserCharacters",
    description="UserCharacters CRUD를 작성하기 위해 사용하는 API.",
)

parser = UserCharacters.parser()
parser.add_argument('token', location='headers')
parser.add_argument('file', type=FileStorage, location='files', required=False)
parser.add_argument('selectedYN', location='form', required=False)
parser.add_argument('notSelectedYN', location='form', required=False)

@UserCharacters.route('')
@UserCharacters.expect(parser)
@UserCharacters.doc(responses={200: 'Success'})
@UserCharacters.doc(responses={404: 'Failed'})
class UserCharactersClass(Resource):

    def post(self):
        """
        # 케릭터 한 개 버킷에 저장 후 DB INSERT
        # @header : token
        # @form-data : <file>
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

    def get(self):
        """
        # 케릭터 여러 개 url 가져오기
        # @header : token
        # @return : 
            {
                data: 
                    [
                        {
                            id: "id", 
                            url: "url",
                        },
                        {
                            id: "id", 
                            url: "url",
                        },
                    ]
            }
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

@UserCharacters.route('/bulk')
@UserCharacters.expect(parser)
@UserCharacters.doc(responses={200: 'Success'})
@UserCharacters.doc(responses={404: 'Failed'})
class UserCharactersBulkClass(Resource):
    
    def post(self):
        """
        # 케릭터 여러 개 버킷에 저장 후 DB INSERT
        # @header : token
        # @form-data :
            {
                "selectedYN": "Y" or "N",
                "notSelectedYN": "Y" or "N",
                "selectedCharacter": <file>,
                "notSelectedCharacters": [<file>, <file>, ...]
            }
        # @return : {userCharacterUrls  : "selected character's url" or NULL}
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

@UserCharacters.route('/user/<characterId>')
@UserCharacters.expect(parser)
@UserCharacters.doc(responses={200: 'Success'})
@UserCharacters.doc(responses={404: 'Failed'})
class UserCharactersBulkClass(Resource):
    
    def delete(self,characterId):
        """
        # 캐릭터 한 개 삭제
        # @header : token
        # @return : 200 or 404
        """
        try:
            result = crud_module.delete_block_character_single(characterId)
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
