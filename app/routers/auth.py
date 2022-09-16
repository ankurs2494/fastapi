from fastapi import Response, Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, auth2


router = APIRouter(
    prefix="/login",
    tags = ['Authentication']
    )

@router.post("/", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_NOT_FOUND, detail="Invalid Email or Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_NOT_FOUND, detail="Invalid Email or Credentials")

    access_token = auth2.create_access_token(data = {"user_id": user.id})


    return {"access_token": access_token, "token_type": "bearer"}

