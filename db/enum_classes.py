import enum

class ScopeClass(enum.Enum):
    user = "user"
    origin = "origin"
    
class StatusClass(enum.Enum):
    
    origin = "origin"
    processed = "processed"
    fail = "fail"
    deleted = "deleted"
    success = "SUCCESS"
    failure = "FAILURE"
    pending = "PENDING"

class FaceTypeClass(enum.Enum):
    mosic = "mosic"
    character = "character"

class SchemaName(enum.Enum):
    user = "user"
    whitelistFace = "whitelistFace"
    whitelistFaceImage = "whitelistFaceImage"
    blockCharacter = "blockCharacter"
    video = "video"
