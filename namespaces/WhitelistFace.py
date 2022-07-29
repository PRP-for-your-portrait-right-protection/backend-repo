from flask import Response, request
import json
from static import status_code
from module import crud_module
from flask_restx import Resource, Api, Namespace
from werkzeug.datastructures import FileStorage

####################################사람얼굴 이름 및 이미지#######################################

WhitelistFaces = Namespace(
    name="WhitelistFaces",
    description="WhitelistFaces CRUD를 작성하기 위해 사용하는 API.",
)

parser = WhitelistFaces.parser()
parser.add_argument('token', location='headers')
parser.add_argument('name', location='form', required=False)
parser.add_argument('file', type=FileStorage, location='files', required=False)
parser.add_argument('face_name_after', location='form', required=False)

@WhitelistFaces.route('')
@WhitelistFaces.expect(parser)
@WhitelistFaces.doc(responses={200: 'Success'})
@WhitelistFaces.doc(responses={404: 'Failed'})
class WhitelistFacesClass(Resource):

    def post(self):
        """
        # 인물 저장
        # @header : token
        # @form-data: {name : ""}
        # @header : token
        # @return : {id: "id"}
        """
        try:
            result = crud_module.upload_whitelist_face()
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
                            "message":status_code.create_02_fail,
                        }
                    ),
                    status=404,
                    mimetype="application/json"
                )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
            
@WhitelistFaces.route('/<whitelistFaceId>')
@WhitelistFaces.expect(parser)
@WhitelistFaces.doc(responses={200: 'Success'})
@WhitelistFaces.doc(responses={404: 'Failed'})
class WhitelistFacesIdClass(Resource):

    def patch(self, whitelistFaceId):
        """
        # 특정 인물 이름 수정
        # @header : token
        # @form-data : face_name_after
        # @return : 200 or 404
        """
        try:
            result = crud_module.update_whitelist_face(whitelistFaceId)
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
                            "message":status_code.update_02_fail,
                        }
                    ),
                    status=404,
                    mimetype="application/json"
                )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
            
    def delete(self, whitelistFaceId):
        """
        # 특정 인물에 대한 사진 모두 삭제
        # @header : token 
        # @return : 200 or 404
        """
        try:
            result = crud_module.delete_whitelist_face(whitelistFaceId)
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
                            "message":status_code.delete_02_fail,
                        }
                    ),
                    status=404,
                    mimetype="application/json"
                )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")

@WhitelistFaces.route('/<whitelistFaceId>/images')
@WhitelistFaces.expect(parser)
@WhitelistFaces.doc(responses={200: 'Success'})
@WhitelistFaces.doc(responses={404: 'Failed'})
class WhitelistFacesImagesClass(Resource):

    def post(self, whitelistFaceId):
        '''
        # 특정 인물 사진 한개 추가
        # @header : token
        # @form-data: {file: <file>}
        # @return : {id: "id"}
        '''
        try:
            result = crud_module.whitelist_face_image_upload(whitelistFaceId)
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
                            "message":status_code.create_02_fail,
                        }
                    ),
                    status=404,
                    mimetype="application/json"
                )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")

@WhitelistFaces.route('/images')
@WhitelistFaces.expect(parser)
@WhitelistFaces.doc(responses={200: 'Success'})
@WhitelistFaces.doc(responses={404: 'Failed'})
class WhitelistFacesImagesClass(Resource):

    def get(self):
        """
        # user에 대한 이미지 사람별로 전부 가져오기
        # @header : token
        # @return : 
        {
                data: 
                [
            {
                whitelistFaceId: "id", 
                        whitelistFaceName: "",
                whitelistFaceImages: [
                            {
                                id: "id",
                                url: "url"
                            },
                            {
                                id: "id",
                                url: "url"
                            },
                        ]
            },
                    {
                whitelistFaceId: "id", 
                        whitelistFaceName: "name",
                        whitelistFaceImages: 
                            {
                                id: "id",
                                url: "url"
                            },
                            {
                                id: "id",
                                url: "url"
                        }
                }
            ]
        }
        """
        try:
            result = crud_module.get_whitelist_face_image()
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
                            "message":status_code.read_02_fail,
                        }
                    ),
                    status=404,
                    mimetype="application/json"
                )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")

@WhitelistFaces.route('/<whitelistFaceId>/images/<imageId>')
@WhitelistFaces.expect(parser)
@WhitelistFaces.doc(responses={200: 'Success'})
@WhitelistFaces.doc(responses={404: 'Failed'})
class WhitelistFacesImageIdClass(Resource):

    def delete(self, whitelistFaceId, imageId):
        '''
        # 특정 인물 사진 한개 삭제하기
        # @header : token
        # @return : message
        '''
        try:
            result = crud_module.delete_whitelist_face_image(whitelistFaceId, imageId)
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
                            "message":status_code.delete_02_fail,
                        }
                    ),
                    status=404,
                    mimetype="application/json"
                )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
