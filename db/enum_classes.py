import enum

class ScopeClass(enum.Enum):
    user = "user"
    origin = "origin"
    
class StatusClass(enum.Enum):
    success = "SUCCESS"
    origin = "ORIGIN"
    processed = "PROCCESSED"
    fail = "FAIL"
    deleted = "DELETED"
    failure = "FAILURE"

class FaceTypeClass(enum.Enum):
    mosaic = "mosaic"
    character = "character"

class SchemaName(enum.Enum):
    user = "user"
    whitelistFace = "whitelistFace"
    whitelistFaceImage = "whitelistFaceImage"
    blockCharacter = "blockCharacter"
    video = "video"
