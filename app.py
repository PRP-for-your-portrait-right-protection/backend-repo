from flask import Flask
from flask_restx import Api
from db.db_connection import db_connection
from namespaces import Face, OriginCharacter, UserCharacter, BeforeVideo, AfterVideo, User

app = Flask(__name__)

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
api.add_namespace(Face.Faces, '/faces')
api.add_namespace(OriginCharacter.OriginCharacters, '/origin-characters')
api.add_namespace(UserCharacter.UserCharacters, '/user-characters')
api.add_namespace(BeforeVideo.BeforeVideos, '/before-videos')
api.add_namespace(AfterVideo.AfterVideos, '/after-videos')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
