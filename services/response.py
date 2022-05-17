from re import I
from fastapi import HTTPException

def success_response(msg=None,data:dict={}):
    return {
        "message":msg,
        "data":data
    }

def error_response(status,msg=None):
    raise HTTPException(
        status=status,
        detail=msg
    )