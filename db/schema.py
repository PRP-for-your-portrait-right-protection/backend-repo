import mongoengine
from flask_mongoengine import Document, MongoEngine, BaseQuerySet
from db.enum_classes import ScopeClass, StatusClass, FaceTypeClass

db = mongoengine

class User(db.Document):
    _id = db.ObjectIdField()
    email = db.StringField(required=True)
    password = db.StringField(required=True)
    name = db.StringField(required=True)
    phone = db.StringField(required=True, max_length=11)
    is_deleted = db.BooleanField(required=True)
    created_at = db.DateTimeField(required=True)
    updated_at = db.DateTimeField()
    
    def __init__(self, email, password, name, phone, is_deleted, created_at, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.email = email
        self.password = password
        self.name = name
        self.phone = phone
        self.is_deleted = is_deleted
        self.created_at = created_at

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_userid(self):
        return self.email
    
    def get_id(self):
        return self._id
    
class WhitelistFace(db.Document):
    _id = db.ObjectIdField()
    user_id = db.ReferenceField(User, required=True)
    name = db.StringField(required=True)
    is_deleted = db.BooleanField(required=True)
    created_at = db.DateTimeField(required=True)
    updated_at = db.DateTimeField()

    def __init__(self, user_id, name, is_deleted, created_at, *args, **kwargs):
        super(WhitelistFace, self).__init__(*args, **kwargs)
        self.user_id = user_id
        self.name = name
        self.is_deleted = is_deleted
        self.created_at = created_at
        
class WhitelistFaceImage(db.Document):
    _id = db.ObjectIdField()
    whitelist_face_id = db.ReferenceField(WhitelistFace, required=True)
    url = db.StringField(required=True)
    is_deleted = db.BooleanField(required=True)
    created_at = db.DateTimeField(required=True)
    updated_at = db.DateTimeField()
    
    def __init__(self, whitelist_face_id, url, is_deleted, created_at, *args, **kwargs):
        super(WhitelistFaceImage, self).__init__(*args, **kwargs)
        self.whitelist_face_id = whitelist_face_id
        self.url = url
        self.is_deleted = is_deleted
        self.created_at = created_at

class BlockCharacter(db.Document):
    _id = db.ObjectIdField()
    user_id = db.ReferenceField(User, required=True)
    url = db.StringField(required=True)
    scope = db.EnumField(ScopeClass, requried=True)      
    is_deleted = db.BooleanField(required=True)
    created_at = db.DateTimeField(required=True)
    updated_at = db.DateTimeField()
    
    def __init__(self, user_id, url, scope, is_deleted, created_at, *args, **kwargs):
        super(BlockCharacter, self).__init__(*args, **kwargs)
        self.user_id = user_id
        self.url = url
        self.scope = scope
        self.is_deleted = is_deleted
        self.created_at = created_at

class Celery(db.Document):
    _id = db.StringField()
    status = db.StringField()
    result = db.StringField()
    traceback = db.StringField()
    children = db.ListField()
    date_done = db.DateTimeField()

class Video(db.Document):
    _id = db.ObjectIdField()
    user_id = db.ReferenceField(User, required=True)
    origin_url = db.StringField(required=True)
    processed_url_id = db.StringField()
    status = db.StringField(required=True)
    face_type = db.EnumField(FaceTypeClass, required=True)
    block_character_id = db.ReferenceField(BlockCharacter)
    whitelist_faces = db.ListField(db.StringField())
    created_at = db.DateTimeField(required=True)
    completed_at = db.DateTimeField()
    updated_at = db.DateTimeField()
    
    def __init__(self, user_id, origin_url, status, created_at, *args, **kwargs):
        super(Video, self).__init__(*args, **kwargs)
        self.user_id = user_id
        self.origin_url = origin_url
        self.status = status
        self.created_at = created_at
        
    def setBlockCharacterId(self, block_character_id):
        self.block_character_id = block_character_id
