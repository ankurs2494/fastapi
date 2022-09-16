from os import access
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import schemas


auth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "45e7c652dbaa844bbdc4857cd0c1943bc7494752fe638dfa14ff3473e31b5001"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")  # type: ignore
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(token: str = Depends(auth2_scheme)):
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail='Could not validate token credentials', headers={"WWW-Authenticate": "Bearer"})
    
    return verify_access_token(token, credentials_exception)

