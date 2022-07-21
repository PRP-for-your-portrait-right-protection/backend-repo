# import mongoengine as me
import mongoengine
# from flask_mongoengine import BaseQuerySet
# from mongoengine import Document
from flask_mongoengine import Document, MongoEngine, BaseQuerySet

db = mongoengine

class People(db.Document):
    _id = db.ObjectIdField()
    person_id = db.IntField(required=True)
    user_id = db.StringField(required=True)
    person_img_name = db.StringField(required=True)
    person_name = db.StringField(required=True)
    person_url = db.StringField(required=True)
    activation_YN = db.StringField(required=True, max_length=1)
    reg_date = db.StringField(required=True)
    mod_date = db.StringField()

    def __init__(self, user_id, person_img_name, person_name, person_url, activation_YN, reg_date, *args, **kwargs):
        super(People, self).__init__(*args, **kwargs)
        self.user_id = user_id
        self.person_img_name = person_img_name
        self.person_name = person_name
        self.person_url = person_url
        self.activation_YN = activation_YN
        self.reg_date = reg_date
        
class OriginCharacter(db.Document):
    _id = db.ObjectIdField()
    character_id = db.IntField(required=True)
    character_name = db.StringField(required=True)
    character_url = db.StringField(required=True)
    activation_YN = db.StringField(required=True, max_length=1)
    reg_date = db.StringField(required=True)
    mod_date = db.StringField()
    meta = { 'collection': 'tags', 'queryset_class': BaseQuerySet}  

class UploadCharacter(db.Document):
    _id = db.ObjectIdField()
    user_id = db.StringField(required=True)
    character_name = db.StringField(required=True)
    character_url = db.StringField(required=True)
    activation_YN = db.StringField(required=True, max_length=1)
    reg_date = db.StringField(required=True)
    mod_date = db.StringField()
    
    def __init__(self, user_id, character_name, character_url, activation_YN, reg_date, *args, **kwargs):
        super(UploadCharacter, self).__init__(*args, **kwargs)
        self.user_id = user_id
        self.character_name = character_name
        self.character_url = character_url
        self.activation_YN = activation_YN
        self.reg_date = reg_date

# class VideoOrigin(me.Document):
#     user_id = me.StringField(required=True)
#     video_name = me.StringField(required=True)
#     video_url = me.StringField(required=True)
#     activation_YN = me.StringField(max_length=1)
#     reg_date = me.StringField(required=True)
#     mod_date = me.StringField()
    
class VideoModification(db.Document):
    _id = db.ObjectIdField()
    user_id = db.StringField(required=True)
    video_name = db.StringField(required=True)
    video_modification_url = db.StringField(required=True)
    activation_YN = db.StringField(max_length=1)
    reg_date = db.StringField(required=True)
    mod_date = db.StringField()
    meta = { 'collection': 'tags', 'queryset_class': BaseQuerySet}  
    
    def __init__(self, user_id, video_name, video_modification_url, activation_YN, reg_date, *args, **kwargs):
        super(People, self).__init__(*args, **kwargs)
        self.user_id = user_id
        self.video_name = video_name
        self.video_modification_url = video_modification_url
        self.activation_YN = activation_YN
        self.reg_date = reg_date
    
class Member(db.Document):
    _id = db.ObjectIdField()
    user_id = db.StringField(required=True)
    password = db.StringField(required=True)
    name = db.StringField(required=True)
    phone = db.StringField(max_length=11)
    token = db.StringField()
    activation_YN = db.StringField(max_length=1)
    reg_date = db.StringField(required=True)
    mod_date = db.StringField()
    
    def __init__(self, user_id, password, name, phone, activation_YN, reg_date, *args, **kwargs):
        super(Member, self).__init__(*args, **kwargs)
        self.user_id = user_id
        self.password = password
        self.name = name
        self.phone = phone
        self.activation_YN = activation_YN
        self.reg_date = reg_date

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_userid(self):
        return self.user_id
    
    def get_id(self):
        return self._id
