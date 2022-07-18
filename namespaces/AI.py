from flask import Flask, Response, request
from module import file_module
from db import db_connection
from flask_restx import Resource, Api, Namespace
from werkzeug.datastructures import FileStorage

####################################AI에 전달 - AI 함수로 전달하는 부분 수정필요#######################################

AI = Namespace(
    name="AI",
    description="AI CRUD를 작성하기 위해 사용하는 API.",
)

parser = AI.parser()
parser.add_argument('not_new_people_YN', location='form', required=True)
parser.add_argument('not_new_people', location='form', required=False)
parser.add_argument('new_people_YN', location='form', required=True)
parser.add_argument('name', location='form', required=False)
parser.add_argument('file', type=FileStorage, location='files', required=False)
parser.add_argument('video', type=FileStorage, location='files', required=True)
parser.add_argument('mode_method', location='form', required=True)
parser.add_argument('new_character_YN', location='form', required=False)
parser.add_argument('character_file', location='form', required=False)
parser.add_argument('character_file', type=FileStorage, location='files', required=False)

@AI.route('/<user_id>')
@AI.expect(parser)
@AI.doc(responses={200: 'Success'})
@AI.doc(responses={404: 'Failed'})
class AIClass(Resource):

    def post(self, user_id):
        '''
        # AI에 파일 링크 한 번에 던지기 : 원본 파일명, 케릭터 파일명, 모자이크 안 할 대상들 파일명
        # @form-data : user_id, files[], video, mode_method, character_new_YN(선택), file(선택)
        # @return : AI 함수
        '''
        try:
            # 1. ai에 전송할 json 생성
            col_json = {}
            
            # 2. user_id
            col_json["user_id"] = user_id
            
            # 3. 모자이크 제외할 사람 얼굴 사진 링크 json에 추가
            col_json["people_file"] = []
            # 3-1. 기존사람
            if request.form["not_new_people_YN"] == "Y":
                not_new_people = request.form.getlist('not_new_people')
                for people in not_new_people:
                    col_json["people_file"].append(people)
            
            # 3-2. 새로운 사람
            if request.form["new_people_YN"] == "Y":
                new_people = file_module.people_multiple_upload(db, "people", user_id)
                for people in new_people:
                    col_json["people_file"].append(people)
            
            # 4. video 추가
            video = file_module.single_upload(db, "origin_video", "video", user_id)
            col_json["video"] = video
            
            # 5. 모자이크화 할 것인지 케릭터화 할 것인지 확인
            mode_method = request.form["mode_method"]
            
            # 6. 모자이크나 케릭터 선택
            # 6-1. 모자이크
            if mode_method == "mosaic":
                # 모자이크 기능 함수로 json 보냄 > ai 함수에서 수정완료 > '수정 후 비디오 저장 API'로 라우팅
                return col_json
            # 6-2. 케릭터화
            elif mode_method == "character ":
                # 케릭터 사진이 새로운 사진인지 검사
                character_new_YN = request.form["character_new_YN"]
                # 새로운 사진
                if character_new_YN == "Y":
                    # 새로운 사진 파일 버킷과 db에 저장 후 url 받아옴
                    db = db_connection.db_connection()
                    character_file = file_module.single_upload(db, "upload_character", "character_file", user_id)
                    col_json["character_file"] = character_file
                    return col_json
                # 존재하던 사진
                elif character_new_YN == "N":
                    # 존재하던 사진 url 받아와서 json에 추가
                    character_file = request.form["character_file"]
                    col_json["character_file"] = character_file
                    return col_json
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
