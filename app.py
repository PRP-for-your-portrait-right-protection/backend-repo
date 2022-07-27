from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from db.db_connection import db_connection
from namespaces import BlockCharacter, OriginVideo, ProccessedVideo, User, WhitelistFace

app = Flask(__name__)
CORS(app, resources={r'*': {'origins': 'http://localhost:3000'}})

db_connection(app)

api = Api(
    app,
    version='v1',
    title="Silicon Project's API Server",
    description="PRP!",
    terms_url="/",
    contact="vivian0304@naver.com",
    license="MIT",
    prefix='/api/v1'
)

api.add_namespace(User.Users, '/users')
api.add_namespace(User.Auth, '/auth')
api.add_namespace(WhitelistFace.WhitelistFaces, '/whitelist-faces')
api.add_namespace(BlockCharacter.BlockCharacters, '/block-characters')
api.add_namespace(OriginVideo.OriginVideos, '/origin-videos')
api.add_namespace(ProccessedVideo.ProccessedVideos, '/processed-videos')

if __name__ == "__main__":
    app.run(port=5001, debug=True)
