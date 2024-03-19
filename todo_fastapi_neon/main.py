# todo_fastapi_neon/main.py
import sys
import os

# Get the current directory of the script
current_dir = os.path.dirname(os.path.realpath(__file__))

# Add the project directory to the Python path
sys.path.append(current_dir)

from contextlib import asynccontextmanager
from typing import Annotated
from sqlmodel import Session, select
from fastapi import FastAPI, Depends, HTTPException
from database import engine
from models import Todo, create_db_and_tables, Todo_Create, Todo_Response, TodoUpdate



# The first part of the function, before the yield, will
# be executed before the application starts.
# https://fastapi.tiangolo.com/advanced/events/#lifespan-function
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan, title="Hello World API with DB", 
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8000", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ])

def get_session():
    with Session(engine) as session:
        yield session

new_session =  Annotated[Session, Depends(get_session)]


# Read Todo
@app.get("/todos/", response_model=list[Todo])
def read_todos(session: new_session):
        todos = session.exec(select(Todo)).all()
        return todos



#Create Todo
@app.post("/todos/", response_model=Todo_Response)
def create_todo(todo: Todo_Create, session: new_session):
        todo_to_insert = Todo.model_validate(todo)
        session.add(todo_to_insert)
        session.commit()
        session.refresh(todo_to_insert)
        return todo_to_insert


#delete todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, session: new_session):
        todo = session.get(Todo, todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        session.delete(todo)
        session.commit()
        return {"message": "Todo deleted"}


#update todo
@app.patch("/todos/{todo_id}")
def update_todo(todo_id: int, todo: TodoUpdate, session: new_session):
        todo_to_update = session.get(Todo, todo_id)
        if todo_to_update is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        todo_data = todo.model_dump(exclude_unset=True)
        todo_to_update.sqlmodel_update(todo_data)
        session.add(todo_to_update)
        session.commit()
        session.refresh(todo_to_update)
        return todo_to_update