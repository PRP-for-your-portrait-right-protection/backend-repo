
def init_collection(db):
    upload_character_result = db.create_collection("upload_character", validator={
            '$jsonSchema': {
                'bsonType': 'object',
                'additionalProperties': True,
                'required': ['character_id', 'user_id', 'character_name', 'reg_date'],
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
                    }
                }
            }
        })
    
    print(upload_character_result)
    
    video_origin_result = db.create_collection("video_origin", validator={
            '$jsonSchema': {
                'bsonType': 'object',
                'additionalProperties': True,
                'required': ['video_id', 'user_id', 'video_name', 'reg_date'],
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
                }
            }
        })
    
    print(video_origin_result)
    
    video_modification_result = db.create_collection("video_modification", validator={
            '$jsonSchema': {
                'bsonType': 'object',
                'additionalProperties': True,
                'required': ['video_id', 'user_id', 'video_name', 'reg_date'],
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
                    }
                }
            }
        })
    
    print(video_modification_result)