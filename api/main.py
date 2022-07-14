import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from typing import Optional, List


from .routes import todos
# from dotenv import load_dotenv
from .database import database, models

models.Base.metadata.create_all(bind=database.sql_engine) 

class NoteIn(BaseModel):
    test: str
    completed: bool
    
class Note(BaseModel ):
    id: int
    text: str
    completed: bool
    

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root_test():
    return {"message":"정상통신"}

@app.get("/notes", response_model=List[Note])
async def read_notes():
    pass


# add routes
app.include_router(todos.router)


            
            