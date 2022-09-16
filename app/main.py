from http.client import HTTPMessage, HTTPResponse
from logging import exception
from pickle import TRUE
from typing import List
from turtle import title
from fastapi.params import Body
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor 
import time

from app.routers.auth import login
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth



# This will create a table if it does not exists
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# cursor_factory=RealDictCursor this will give the column name and value both
while TRUE:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
                                password='ankurs', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection is successfully")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(5)


# Instaed of database we have array to store post
my_post = [{"title": "my first post", "content": "Python Api Development", "id": 1},
            {"title": "my second post", "content": "Clouds deployment engineer roadmap", "id":2}]

def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p

def find_index_post(id):
    # to iterate over post and grep index we are using enumerate
    for i, p in enumerate(my_post):
        if p["id"] == id:
            return i

@app.get("/")
def root():
    return {"message": "Hello Ankur, Fits API development code"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)







