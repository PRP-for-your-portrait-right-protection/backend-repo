from flask import Flask
from flask_mongoengine import MongoEngine
from db.db_config import HOST, PORT
from flask_restx import Api
from flask_migrate import Migrate
from namespaces import People, Character, AI, Video, Member

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    "host" : HOST,
    "port" : PORT,
    "db": "silicon",
}
db = MongoEngine(app)
migrate = Migrate(app, db)
print(db)

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

api.add_namespace(Member.Member, '/member')

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
