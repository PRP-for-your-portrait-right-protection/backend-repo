from flask import Response, request
import json
from static import status_code
from db import db_connection
from module import file_module, crud_module
from flask_restx import Resource, Api, Namespace
from werkzeug.datastructures import FileStorage

####################################여러 사람 여러 사진#######################################

People = Namespace(
    name="People",
    description="People CRUD를 작성하기 위해 사용하는 API.",
)

parser = People.parser()
parser.add_argument('file', type=FileStorage, location='files', required=False)

@People.route('/<user_id>')

@People.doc(responses={200: 'Success'})
@People.doc(responses={404: 'Failed'})
class PeopleClass(Resource):
    
    @People.expect(parser)
    def post(self,user_id):
        '''
        # 여러 사람 여러 사진 버킷에 저장
        # @form-data : user_id, file[], name[]
        # @return : {file : [file_url, file_url, file_url]}
        '''
        try:
           
            db = db_connection.db_connection()
            result = file_module.people_multiple_upload(db, "people",user_id)
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

    def get(self,user_id):
        """
        # 여러 사람 여러 사진 url 가져오기
        # @form-data : user_id
        # @return : 
        #   {
        #       person_name : [
        #           file_url, file_url, file_url
        #       ], 
        #       person_name : [
        #           file_url, file_url, file_url
        #       ]
        #   }
        """
        try:
            db = db_connection.db_connection()
            result = crud_module.multiple_get(db, "get_people",user_id)
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
                            "message":status_code.file_download_02_fail
                        }
                    ),
                    status=404,
                    mimetype="application/json"
                )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")

####################################특정인물 사진 여러 개#######################################

PersonAll = Namespace(
    name="PersonAll",
    description="PersonAll CRUD를 작성하기 위해 사용하는 API."
)

@PersonAll.route('/<user_id>')
@PersonAll.doc(responses={200: 'Success'})
@PersonAll.doc(responses={404: 'Failed'})
class PersonAllClass(Resource):

    @PersonAll.doc(params=
        {
            'person_name': {'description': 'person name', 'type': 'string'},
            'person_name_after': {'description': 'person name after', 'type': 'string'}
        }
    )
    def patch(self, user_id):
        '''
        # 특정 인물 이름 수정
        # @form-data : user_id, person_name, person_name_after
        # @return : message
        '''
        try:
            person_name = request.args.get('person_name', type = str)
            person_name_after = request.args.get('person_name_after', type = str)
            db = db_connection.db_connection()
            if crud_module.single_update(db, user_id, person_name, person_name_after):
                return Response(
                    response = json.dumps(
                        {
                            "message" : status_code.file_update_01_success
                        }
                    ),
                    status = 200,
                    mimetype = "application/json"
                )
            else:
                return Response(
                    response = json.dumps(
                        {
                            "message" : status_code.file_update_02_fail
                        }
                    ),
                    status = 404,
                    mimetype = "application/json"
                )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
            
    @PersonAll.doc(params={'person_name': {'description': 'person name', 'type': 'string'}})   
    def delete(self, user_id):
        '''
        # 특정 인물에 대한 사진 모두 삭제하기
        # @form-data : user_id, person_name
        # @return : message
        '''
        try:
            person_name = request.args.get('person_name', type = str)
            db = db_connection.db_connection()
            if crud_module.multiple_delete(db, "people", user_id, person_name):
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

####################################특정인물 사진 한 개#######################################      

PersonSingle = Namespace(
    name="PersonSingle",
    description="PersonSingle CRUD를 작성하기 위해 사용하는 API.",
)

@PersonSingle.route('/<user_id>')
@PersonSingle.doc(responses={200: 'Success'})
@PersonSingle.doc(responses={404: 'Failed'})
class PersonSingleClass(Resource):

    @PersonSingle.doc(params={'url': {'description': 'url', 'type': 'string'}})   
    def delete(self, user_id):
        '''
        # 특정 인물 사진 한개 삭제하기
        # @form-data : user_id, url  << url로 DB에서 person_url에 해당하는 값을 주면 됨
        # @return : message
        '''
        try:
            url = request.args.get('url', type = str)
            db = db_connection.db_connection()
            if crud_module.single_delete(db, "people", user_id, url):
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
