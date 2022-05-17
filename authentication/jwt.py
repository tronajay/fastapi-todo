import time, jwt
from decouple import config

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = "HS256"

def create_jwt_token(user:str):
    payload = {
        "user":user,
        "expires":time.time() + 600
    }
    token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token

def verify_jwt(token: str) -> dict:
    return {}
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}