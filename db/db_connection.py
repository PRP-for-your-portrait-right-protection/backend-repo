from flask_mongoengine import MongoEngine
from flask_migrate import Migrate
from db.db_config import HOST, PORT

def db_connection(app):

    app.config['MONGODB_SETTINGS'] = {
        "host" : HOST,
        "port" : PORT,
        "db": "silicon",
    }
    db = MongoEngine(app)
    migrate = Migrate(app, db)
    print(db)
