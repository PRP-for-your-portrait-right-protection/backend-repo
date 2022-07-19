from flask import Flask, Response, request
import json
from static import status_code
from module import file_module, member_module, crud_module
from db import db_connection
from flask_restx import Resource, Api, Namespace
from werkzeug.datastructures import FileStorage

####################################수정 전 비디오#######################################

VideoOrigin = Namespace(
    name="VideoOrigin",
    description="VideoOrigin CRUD를 작성하기 위해 사용하는 API."
)

parserVideoOrigin = VideoOrigin.parser()
parserVideoOrigin.add_argument('file', type=FileStorage, location='files', required=False)

@VideoOrigin.route('/<user_id>')
@VideoOrigin.expect(parserVideoOrigin)
@VideoOrigin.doc(responses={200: 'Success'})
@VideoOrigin.doc(responses={404: 'Failed'})
class VideoOriginClass(Resource):

    def post(self, user_id):
        '''
        # 수정 전 비디오 파일 버킷에 저장
        # @form-data : user_id, file
        # @return : {file : file_url}
        '''
        try:
            db = db_connection.db_connection()
            result = file_module.single_upload(db, "video_origin", "video_origin", user_id)
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

####################################수정 후 비디오#######################################

VideoModification = Namespace(
    name="VideoModification",
    description="VideoModification CRUD를 작성하기 위해 사용하는 API.",
)

parserVideoModification = VideoOrigin.parser()
parserVideoModification.add_argument('file', type=FileStorage, location='files', required=False)

@VideoModification.route('/<user_id>')
@VideoModification.doc(responses={200: 'Success'})
@VideoModification.doc(responses={404: 'Failed'})
class VideoModificationClass(Resource):
    @VideoModification.expect(parserVideoModification)
    def post(self, user_id):
        '''
        # 수정 후 비디오 파일 버킷에 저장 후 링크 return
        # @form-data : user_id, file
        # @return : {file : file_url}
        '''
        
        try:
            db = db_connection.db_connection()
            result = file_module.single_upload(db, "video_modification", "video_modification", user_id)
            if result != False:
                return Response(
                    response = json.dumps(result),
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

    @VideoModification.doc(params={'filename': {'description': 'file name', 'type': 'string'}})
    def get(self, user_id):
        """
        # 수정 후 비디오 파일 다운로드 : 자동 다운로드
        # @form-data : user_id, filename
        # @return : message
        """
        try:
            file_name = request.args.get('filename', type = str)
            db = db_connection.db_connection()
            if file_module.single_download(db, "video_modification", user_id, file_name) :
                return Response(
                    response=json.dumps(
                        {
                            "message":status_code.file_download_01_success,
                        }
                    ),
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
        
    @VideoModification.doc(params={'url': {'description': 'url', 'type': 'string'}})
    def delete(self, user_id):
        '''
        # 수정 후 비디오 파일 한 개 삭제하기
        # @form-data : user_id, url
        # @retutrn : message
        '''
        try:
            url = request.args.get('url', type = str)
            db = db_connection.db_connection()
            if crud_module.single_delete(db, "video_modification", user_id, url):
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

####################################수정 후 비디오 여러 개#######################################

VideoModifications = Namespace(
    name="VideoModifications",
    description="VideoModifications CRUD를 작성하기 위해 사용하는 API.",
)

@VideoModifications.route('/<user_id>')
@VideoModifications.doc(responses={200: 'Success'})
@VideoModifications.doc(responses={404: 'Failed'})
class VideoModificationsClass(Resource):

    def get(self, user_id):
        '''
        # 특정 유저에 대한 비디오 결과 모두 조회하기
        # @form-data : user_id
        # @return : {file : [file_url, file_url, file_url]}
        '''
        try:
            db = db_connection.db_connection()
            result = crud_module.single_get(db, "get_video_modification", user_id)
            if result != False:
                return Response(
                    response = json.dumps(result),
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
    
    @VideoModifications.doc(params={'person_name': {'description': 'person name', 'type': 'string'}})
    def delete(self, user_id):
        '''
        # 특정 유저에 대한 비디오 결과 모두 삭제하기
        # @form-data : user_id, person_name <<
        # @return : message
        '''
        try:
            person_name = request.args.get('person_name', type = str)
            db = db_connection.db_connection()
            if crud_module.multiple_delete(db, "video_modification", user_id, person_name):
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
