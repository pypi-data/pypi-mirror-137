from enum import IntEnum

class FieldUse(IntEnum):
    NONE    = 0
    CREATE  = 1
    GET     = 2
    SCAN    = 3
    DELETE  = 4
    UPDATE  = 5
    ALL     = 6