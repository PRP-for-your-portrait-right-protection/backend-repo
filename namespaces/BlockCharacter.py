from flask import Response
import json
from module import crud_module
from flask_restx import Resource, Namespace
from werkzeug.datastructures import FileStorage

####################################기존 캐릭터#######################################

BlockCharacters = Namespace(
    name="Characters",
    description="Characters CRUD를 작성하기 위해 사용하는 API.",
)

parser = BlockCharacters.parser()
parser.add_argument('token', location='headers')
parser.add_argument('file', type=FileStorage, location='files', required=False)

@BlockCharacters.route('/origin')
@BlockCharacters.expect(parser)
@BlockCharacters.doc(responses={200: 'Success'})
@BlockCharacters.doc(responses={404: 'Failed'})
class OriginBlockCharactersClass(Resource):

    def get(self):
        """
        # 기존 케릭터 사진 url 가져오기
        # @header : token
        # @return 
            {
                data: [
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
            result, message = crud_module.get_origin_block_character()
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

####################################유저 캐릭터#######################################

@BlockCharacters.route('/user')
@BlockCharacters.expect(parser)
@BlockCharacters.doc(responses={200: 'Success'})
@BlockCharacters.doc(responses={404: 'Failed'})
class UserBlockCharactersClass(Resource):
  
    def post(self):
        '''
        # 케릭터 한 개 버킷에 저장
        # @form-data : {file: <file>}
        # @header : token
        # @return : {id:"", url: ""}
        '''
        try:
            result, message = crud_module.upload_user_block_character()
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
            

    def get(self):
        """
        # 유저 케릭터 여러 개 url 가져오기
        # @header : token
        # @return : 
            {
                data: [
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
            result, message = crud_module.get_user_block_character() 
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

@BlockCharacters.route('/user/<characterId>')
@BlockCharacters.expect(parser)
@BlockCharacters.doc(responses={200: 'Success'})
@BlockCharacters.doc(responses={404: 'Failed'})
class UserBlockCharactersIdClass(Resource):
 
    def delete(self ,characterId):
        """
        # 캐릭터 한 개 삭제
        # @header : token
        # @return : 200 or 404
        """
        try:
            result, message = crud_module.delete_user_block_character(characterId)
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
