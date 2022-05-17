from fastapi import Depends
from authentication.jwt import verify_jwt
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login/")

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_jwt(token)