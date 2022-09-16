from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

#----------------------------------------------
# Create user path function 
#----------------------------------------------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user : schemas.UserCreate, db: Session = Depends(get_db)):

    # hashed the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#----------------------------------------------
# GET user path function 
#----------------------------------------------
@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id : int, db: Session = Depends(get_db)):

    user = db.query(models.Users).filter(models.Users.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id : {id} was not found")
    return user



