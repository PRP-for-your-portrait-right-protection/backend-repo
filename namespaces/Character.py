from flask import Response, request
import json
from static import status_code
from db import db_connection
from module import file_module, crud_module
from flask_restx import Resource, Api, Namespace
from werkzeug.datastructures import FileStorage

####################################기존 케릭터#######################################

OriginCharacter = Namespace(
    name="OriginCharacter",
    description="OriginCharacter CRUD를 작성하기 위해 사용하는 API.",
)

@OriginCharacter.route('')
@OriginCharacter.doc(responses={200: 'Success'})
@OriginCharacter.doc(responses={404: 'Failed'})
class OriginCharacterClass(Resource):

    def get(self):
        """
        # 기존 케릭터 사진 url 가져오기
        # @form-data : 없음
        # @return : {file : [file_url, file_url, file_url]}
        """
        try:
            db = db_connection.db_connection()
            result = crud_module.single_get(db, "get_origin_character")
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
        
####################################케릭터 한개#######################################

Character = Namespace(
    name="Character",
    description="Character CRUD를 작성하기 위해 사용하는 API.",
)

parser = Character.parser()
parser.add_argument('file', location='form', required=False)

@Character.route('/<user_id>')
@Character.doc(responses={200: 'Success'})
@Character.doc(responses={404: 'Failed'})
class CharacterClass(Resource):
    
    @Character.expect(parser)#post에서 formdata 사용하기 때문
    def post(self,user_id):
        '''
        # 케릭터 한 개 버킷에 저장
        # @form-data : user_id, file
        # @return : {file : file_url}
        '''
        try:
            db = db_connection.db_connection()
            result = file_module.single_upload(db, "upload_character","file",user_id)
            if result != False:
                return Response(
                    response=json.dumps(result),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    response=json.dumps(
                        {
                            "message":status_code.file_save_02_fail,
                        }
                    ),
                    status=404,
                    mimetype="application/json"
                )
        except Exception as ex:
                print("******************")
                print(ex)
                print("******************")
    
    @Character.doc(params={'url': {'description': 'url', 'type': 'string'}})   
    def delete(self,user_id):
        '''
        # 캐릭터 한 개 삭제
        # @form-data : user_id, url
        # @return : message
        '''
        try:
            url=request.args.get('url', type = str)#  form data 아닐때
            db = db_connection.db_connection()
            if crud_module.single_delete(db, "character",user_id,url):
                return Response(
                    response = json.dumps(
                        {
                            "message" : status_code.file_remove_01_success
                        }
                    ),
                    status = 200,
                    mimetype = "application/json"
                )
            else:
                return Response(
                    response = json.dumps(
                        {
                            "message" : status_code.file_remove_02_fail
                        }
                    ),
                    status = 404,
                    mimetype = "application/json"
                )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")

####################################케릭터 여러개#######################################

Characters = Namespace(
    name="Characters",
    description="Characters CRUD를 작성하기 위해 사용하는 API.",
)

parser = Characters.parser()
parser.add_argument('file', type=FileStorage, location='files', required=False)

@Characters.route('/<user_id>')

@Characters.doc(responses={200: 'Success'})
@Characters.doc(responses={404: 'Failed'})
class CharactersClass(Resource):

    @Characters.expect(parser)
    def post(self,user_id):
        '''
        # 케릭터 여러 개 버킷에 저장
        # @form-data : user_id, file[]
        # @return : {file : [file_url, file_url, file_url]}
        '''
        try:
            db = db_connection.db_connection()
            result = file_module.multiple_upload(db, "upload_character","file",user_id)
            if result != False:
                return Response(
                    response=json.dumps(result),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    response=json.dumps(
                        {
                            "message":status_code.file_save_02_fail,
                        }
                    ),
                    status=404,
                    mimetype="application/json"
                )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
    
    def get(self,user_id):
        """
        # 케릭터 여러 개 url 가져오기
        # @form-data : user_id
        # @return : {file : [file_url, file_url, file_url]}
        """
        try:
            db = db_connection.db_connection()
            result = crud_module.single_get(db, "get_character",user_id)
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

    def delete(self,user_id):
        '''
        # 특정 유저에 대한 캐릭터 모두 삭제하기
        # @form-data : user_id
        # @return : message
        '''
        try:
            db = db_connection.db_connection()
            person_name=request.args.get('person_name', type = str)
            if crud_module.multiple_delete(db, "characters",user_id,person_name):
                return Response(
                    response = json.dumps(
                        {
                            "message" : status_code.file_remove_01_success
                        }
                    ),
                    status = 200,
                    mimetype = "application/json"
                )
            else:
                return Response(
                    response = json.dumps(
                        {
                            "message" : status_code.file_remove_02_fail
                        }
                    ),
                    status = 404,
                    mimetype = "application/json"
                )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
