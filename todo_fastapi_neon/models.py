from sqlmodel import SQLModel, Field
from database import engine
from dataclasses import field


class Todo_Base(SQLModel):
    title: str
    description: str

class Todo(Todo_Base, table=True):
    id: int|None = Field(default=None, primary_key=True)

class Todo_Create(Todo_Base):
    pass

class TodoUpdate(SQLModel):
    title: str | None = None
    description: str | None = None

class Todo_Response(Todo_Base):
    id: int = Field(primary_key=True)    
    


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)