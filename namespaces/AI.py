from flask import Flask, Response, request
import json
from static import status_code
from module import file_module, member_module, crud_module
from db import db_connection
from flask_restx import Resource, Api, Namespace
from werkzeug.datastructures import FileStorage
from namespaces import People

####################################AI에 전달 - AI 함수로 전달하는 부분 수정필요#######################################

AI = Namespace(
    name="AI",
    description="AI CRUD를 작성하기 위해 사용하는 API.",
)

parser = AI.parser()
parser.add_argument('user_id', location='form', required=False)
parser.add_argument('name', location='form', required=False)
parser.add_argument('file', type=FileStorage, location='files', required=False)

@AI.route('')
@AI.expect(parser)
@AI.doc(responses={200: 'Success'})
@AI.doc(responses={404: 'Failed'})
class AIClass(Resource):

    def post():
        '''
        # AI에 파일 링크 한 번에 던지기 : 원본 파일명, 케릭터 파일명, 모자이크 안 할 대상들 파일명
        # @form-data : user_id, files[], video, mode_method, character_new_YN(선택), file(선택)
        # @return : AI 함수
        '''
        try:
            # 1. ai에 전송할 json 생성
            col_json = {}
            
            # 2. json에 추가
            # 2-1. 모자이크 제외할 사람 얼굴 사진 링크
            col_json["file"] = []
            fs = request.files.getlist("files")
            for f in fs:
                col_json["file"].append(f)
            
            # 2-2. user_id
            user_id = request.form["user_id"]
            col_json["user_id"] = user_id
            
            # 2-3. video
            video = request.form["video"]
            col_json["video"] = video
            
            # 3. 모자이크화 할 것인지 케릭터화 할 것인지 확인
            mode_method = request.form["mode_method"]
            
            # 3-1. 모자이크
            if mode_method == "mosaic":
                # 모자이크 기능 함수로 json 보냄 > ai 함수에서 수정완료 > '수정 후 비디오 저장 API'로 라우팅
                return col_json
            
            # 3-2. 케릭터화
            elif mode_method == "character ":
                # 케릭터 사진이 새로운 사진인지 검사
                character_new_YN = request.form["character_new_YN"]
                
                # 새로운 사진
                if character_new_YN == "Y":
                    # 새로운 사진 파일 버킷과 db에 저장 후 url 받아옴
                    db = db_connection.db_connection()
                    character_file = file_module.single_upload(db, "upload_character")
                    col_json["character_file"] = character_file
                    return col_json
                # 존재하던 사진
                elif character_new_YN == "N":
                    # 존재하던 사진 url 받아와서 json에 추가
                    character_file = request.form["file"]
                    col_json["character_file"] = character_file
                    return col_json
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
