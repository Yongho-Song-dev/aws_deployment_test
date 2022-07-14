import pytz

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel,Field

from starlette.status import  HTTP_404_NOT_FOUND
from sqlalchemy.orm import Session

from ..database import database, errors, models

KST = pytz.timezone('Asia/Seoul')
now = datetime.utcnow()    

class Todo(BaseModel):
    title: str
    description: str
    completed: bool
    created_at: Optional[datetime] = Field(
        default=str(datetime.now(tz=KST).isoformat()), 
        # default_factory=utc.localize(now).astimezone(KST),
        title="최초 생성 날짜 및 시간"
        )

    class Config:
        orm_mode = True 

router = APIRouter(
    tags=["Todos"]
)

get_db = database.get_db

# get todo
@router.get("/todos/{pk}", status_code=status.HTTP_200_OK)
async def get_todo(title: str, db : Session = Depends(get_db)):
    try:
        return await db.query(models.todos).filter(models.todos.title==title).all()
    except :
        return errors.raise_api_exception(detail="Todo not found", status_code = HTTP_404_NOT_FOUND )


@router.get("/todos")
async def get_todos(db : Session = Depends(get_db)):
    # todos = [await get_all_todos(pk) async for pk in await Todo.all_pks()]
    todos = db.query(models.todos).all()
    # todo_pks = await Todo.all_pks()
    # todos = []

    # async for pk in todo_pks:
    #     todo = await get_all_todos(pk)
    #     todos.append(todo)
    print(f"todos")
    return todos

async def get_all_todos(pk: str):
    todo = await Todo.get(pk)

    return {
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "created_at": todo.created_at
    }


# create todo
@router.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(todo: Todo, db: Session= Depends(get_db)):
    KST = pytz.timezone('Asia/Seoul')
    now = datetime.utcnow()    
    # todo.completed = int(todo.completed)
    # new_todo = await todo.save()
    # print(f"\ntodo 이전  : {todo} \n\n")
    # todo.created_at = pytz.utc.localize(now).astimezone(KST)
    
    new_todo = models.todos(
        title = todo.title,
        description = todo.description,
        completed= todo.completed,
        created_at = pytz.utc.localize(now).astimezone(KST)
    )
    # print(f"\ntodo 이후 : {new_todo} \n\n")
    db.add(new_todo)
    db.commit()
    
    return todo.dict()


# delete todo
@router.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(id: int, db: Session= Depends(get_db)):
    db_deletes = db.query(models.todos).filter(models.todos.id == id)
    if db_deletes is None :
        errors.raise_api_exception(detail="없는 데이터입니다.")
    else :
        data = db.query(models.todos).filter(models.todos.id == id).first()
    db_deletes.delete()
    db.commit()
    
    
    return data
    # await Todo.delete(pk)


# update todo
@router.put("/todos/{pk}", status_code=status.HTTP_200_OK)
async def update_todo(pk: str, todo: Todo):
    try:
        old_todo = await Todo.get(pk)
        print(old_todo)
        old_todo.title = todo.title
        old_todo.description = todo.description
        old_todo.completed = int(todo.completed)

        await old_todo.save()

        return old_todo
    except NotFoundError:
        return HTTPException(status_code=404, detail="Todo not found")
