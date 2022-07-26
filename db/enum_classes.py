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

class FaceTypeClass(enum.Enum):
    mosic = "mosic"
    character = "character"

class SchemaName(enum.Enum):
    user = "user"
    whitelistFace = "whitelistFace"
    whitelistFaceImage = "whitelistFaceImage"
    blockCharacter = "blockCharacter"
    video = "video"
