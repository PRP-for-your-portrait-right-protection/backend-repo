from flask import Flask
from db import db_connection
from flask_restx import Api
from werkzeug.datastructures import FileStorage
from namespaces import People, Character, AI, Video

# 스키마 생성
# db_connection.init_collection(db)

# DB 연결
db = db_connection.db_connection()

app = Flask(__name__)

api = Api(
    app,
    version='0.1',
    title="Silicon Project's API Server",
    description="PRP!",
    terms_url="/",
    contact="vivian0304@naver.com",
    license="MIT"
)

api.add_namespace(People.People, '/people')
api.add_namespace(People.PersonAll, '/person-all')
api.add_namespace(People.PersonSingle, '/person-single')

api.add_namespace(Character.Character, '/character')
api.add_namespace(Character.Characters, '/characters')
api.add_namespace(Character.OriginCharacter, '/origin-character')

api.add_namespace(Video.VideoOrigin, '/video-origin')
api.add_namespace(Video.VideoModification, '/video-modification')
api.add_namespace(Video.VideoModifications, '/video-modifications')

api.add_namespace(AI.AI, '/ai')

if __name__ == "__main__":
    app.run(port=80, debug=True)
