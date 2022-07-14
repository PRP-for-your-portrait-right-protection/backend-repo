import pymongo
from db.db_config import HOST, PORT

def db_connection():
    db = None
    
    print("=================================")
    print(HOST)
    print("=================================")

    try:
        # mongo = pymongo.MongoClient(
        #     # host = os.environ['DB_PORT_27017_TCP_ADDR'], 
        #     host = HOST,
        #     port = PORT
        #     # serverSelectionTimeoutMS = 1000
        # )
        # MongoClient('mongodb://user:' + password + '@127.0.0.1')

        mongo = pymongo.MongoClient('mongodb://root:root@db:27017')
        db = mongo.silicon
        mongo.server_info() # trigger exception if cannot connect to db
        return db
    # except:
    #     print("ERROR - Cannot connect to db")
    #     return False
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")
    
def init_collection(db):
    people_result = db.create_collection("people", validator={
            '$jsonSchema': {
                'bsonType': 'object',
                'additionalProperties': True,
                'required': ['person_id', 'user_id', 'person_img_name', 'person_name', 'reg_date', 'person_img_url'],
                'properties': {
                    "person_id" : {
                        'bsonType': 'number'
                    },
                    "user_id" : {
                        'bsonType': 'string'
                    },
                    "person_img_name" : {
                        'bsonType': 'string'
                    },
                    "person_name" : {
                        'bsonType': 'string'
                    },
                    "person_url" : {
                        'bsonType': 'string'
                    },
                    "reg_date": {
                        'bsonType': 'string'
                    },
                    "person_img_url" : {
                        'bsontype' : 'string'
                    }
                    }
                }
            }
        })
    
    print(people_result) 
    
    upload_character_result = db.create_collection("upload_character", validator={
            '$jsonSchema': {
                'bsonType': 'object',
                'additionalProperties': True,
                'required': ['character_id', 'user_id', 'character_name', 'reg_date', 'character_url'],
                'properties': {
                    "character_id": {
                        'bsonType': 'number'
                    },
                    "user_id" : {
                        'bsonType': 'string'
                    },
                    "character_name" : {
                        'bsonType': 'string'
                    },
                    "reg_date": {
                        'bsonType': 'string'
                    },
                    "character_url" : {
                        'bsontype' : 'string'
                    }
                }
            }
        })
    
    print(upload_character_result)
    
    video_origin_result = db.create_collection("video_origin", validator={
            '$jsonSchema': {
                'bsonType': 'object',
                'additionalProperties': True,
                'required': ['video_id', 'user_id', 'video_name', 'reg_date', 'video_url'],
                'properties': {
                    "video_id" : {
                        'bsonType': 'number',
                    },
                    "user_id" : {
                        'bsonType': 'string',
                    },
                    "video_name" : {
                        'bsonType': 'string',
                    },
                    "reg_date": {
                        'bsonType': 'string',
                    },
                    "video_url" : {
                        'bsontype' : 'string'
                    }
                }
            }
        })
    
    print(video_origin_result)
    
    video_modification_result = db.create_collection("video_modification", validator={
            '$jsonSchema': {
                'bsonType': 'object',
                'additionalProperties': True,
                'required': ['video_id', 'user_id', 'video_name', 'reg_date', 'video_modification_url'],
                'properties': {
                    "video_id" : {
                        'bsonType': 'number'
                    },
                    "user_id" : {
                        'bsonType': 'string'
                    },
                    "video_name" : {
                        'bsonType': 'string'
                    },
                    "reg_date": {
                        'bsonType': 'string'
                    },
                    "video_modification_url" : {
                        'bsontype' : 'string'
                    }
                }
            }
        })
    
    print(video_modification_result)