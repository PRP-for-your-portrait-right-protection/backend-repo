from flask import Response, request
import json
from static import status_code
from module import file_module, crud_module
from flask_restx import Resource, Api, Namespace
from werkzeug.datastructures import FileStorage

####################################여러 사람 여러 사진#######################################

Faces = Namespace(
    name="Faces",
    description="Faces CRUD를 작성하기 위해 사용하는 API.",
)

parser = Faces.parser()
parser.add_argument('token', location='headers')
parser.add_argument('name', location='form', required=False)
parser.add_argument('file', type=FileStorage, location='files', required=False)
parser.add_argument('face_name_after', location='form', required=False)

@Faces.route('')
@Faces.expect(parser)
@Faces.doc(responses={200: 'Success'})
@Faces.doc(responses={404: 'Failed'})
class FacesClass(Resource):

    def post(self):
        """
        # 여러 사람 여러 사진 버킷에 저장 후 DB INSERT
        # @header : token
        # @form-data :  {
                            name : [a1 ,a2, a3, a4],
                            a1 : [file, file, file, ...],
                            a2 : [file, file, file, ...],
                            a3 : [file, file, ...],
                            a4 : [file, ...]
                        }
        # @return : {faceImageUrls : [file_url, file_url, file_url]}
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
        # 여러 사람 여러 사진 url 가져오기
        # @header : token 
        # @return : 
            {
                data: 
                    [
                        {
                            nameId: "nameId", 
                            name: "name",
                            pictures: 
                                [
                                    {pictureId: "pictureId", pictureUrl: "pictureUrl"},
                                    {pictureId: "pictureId", pictureUrl: "pictureUrl"},
                                ],
                        },
                        {
                            nameId: "nameId", 
                            name: "name",
                            pictures: 
                                [
                                    {pictureId: "pictureId", pictureUrl: "pictureUrl"},
                                    {pictureId: "pictureId", pictureUrl: "pictureUrl"},
                                ]
                        }
                    ]
            }
        """
        try:
            result = crud_module.get_multiple_id_img()
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
            
####################################특정 인물 사진 여러 개#######################################

@Faces.route('/<faceNameId>')
@Faces.expect(parser)
@Faces.doc(responses={200: 'Success'})
@Faces.doc(responses={404: 'Failed'})
class FacesSpecificPersonImageBulkClass(Resource):

    def patch(self):
        """
        # 특정 인물 이름 수정
        # @header : token
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
            
    def delete(self):
        """
        # 특정 인물에 대한 사진 모두 삭제
        # @header : token 
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
            
####################################특정 인물 사진 한 개#######################################

@Faces.route('/<faceNameId>/imgaes/<imageId>')
@Faces.expect(parser)
@Faces.doc(responses={200: 'Success'})
@Faces.doc(responses={404: 'Failed'})
class FacesSpecificPersonIamgeOneClass(Resource):

    def delete(self):
        """
        # 특정 인물 사진 한 개 삭제
        # @header : token
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
