import pymongo
from db.db_config import HOST, PORT
def db_connection():
    db = None
    try:
        # mongo = pymongo.MongoClient('mongodb://testuser:testpass@localhost:27017')
        mongo = pymongo.MongoClient(
            host = HOST,
            port = PORT,
            serverSelectionTimeoutMS = 1000
        )
        db = mongo.silicon
        mongo.server_info() # trigger exception if cannot connect to db
        return db
    except Exception as ex:
        print("******************")
        print("ERROR - Cannot connect to db")
        print(ex)
        print("******************")
        
def init_collection(db):
    people_result = db.create_collection("people", validator={
            '$jsonSchema': {
                'bsonType': 'object',
                'additionalProperties': True,
                'required': ['person_id', 'user_id', 'person_img_name', 'person_name', 'person_url', 'reg_date'],
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
                    "activation_YN": {
                        'bsonType': 'string'
                    },
                    "reg_date": {
                        'bsonType': 'string'
                    },
                    "mod_date": {
                        'bsonType': 'string'
                    }
                }
            }
        }
    )
    print(people_result)
    upload_character_result = db.create_collection("upload_character", validator={
            '$jsonSchema': {
                'bsonType': 'object',
                'additionalProperties': True,
                'required': ['character_id', 'user_id', 'character_name', 'character_url', 'reg_date'],
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
                    "character_url" : {
                        'bsonType' : 'string'
                    },
                    "activation_YN": {
                        'bsonType': 'string'
                    },
                    "reg_date": {
                        'bsonType': 'string'
                    },
                    "mod_date": {
                        'bsonType': 'string'
                    }
                }
            }
        }
    )
    print(upload_character_result)
    video_origin_result = db.create_collection("video_origin", validator={
            '$jsonSchema': {
                'bsonType': 'object',
                'additionalProperties': True,
                'required': ['video_id', 'user_id', 'video_name', 'video_url', 'reg_date'],
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
                    "video_url" : {
                        'bsonType' : 'string'
                    },
                    "reg_date": {
                        'bsonType': 'string',
                    },
                    "mod_date": {
                        'bsonType': 'string'
                    }
                }
            }
        }
    )
    print(video_origin_result)
    video_modification_result = db.create_collection("video_modification", validator={
            '$jsonSchema': {
                'bsonType': 'object',
                'additionalProperties': True,
                'required': ['video_id', 'user_id', 'video_name', 'video_modification_url', 'reg_date'],
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
                    "video_modification_url" : {
                        'bsonType' : 'string'
                    },
                    "activation_YN": {
                        'bsonType': 'string'
                    },
                    "reg_date": {
                        'bsonType': 'string'
                    },
                    "mod_date": {
                        'bsonType': 'string'
                    }
                }
            }
        }
    )
    print(video_modification_result)
    member = db.create_collection("member", validator={
            '$jsonSchema': {
                'bsonType': 'object',
                'additionalProperties': True,
                'required': ['user_id', 'password', 'name', 'phone', 'activation_YN', 'reg_date'],
                'properties': {
                    "member_id" : {
                        'bsonType': 'number'
                    },
                    "user_id" : {
                        'bsonType': 'string'
                    },
                    "password" : {
                        'bsonType': 'string'
                    },
                    "name" : {
                        'bsonType': 'string'
                    },
                    "phone" : {
                        'bsonType': 'string'
                    },
                    "token": {
                        'bsonType': 'string'
                    },
                    "activation_YN": {
                        'bsonType': 'string'
                    },
                    "reg_date": {
                        'bsonType': 'string'
                    },
                     "mod_date": {
                        'bsonType': 'string'
                    }
                }
            }
        }
    )
    print(member)
    