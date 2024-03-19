from fastapi.testclient import TestClient
from sqlmodel import Field, Session, SQLModel, create_engine, select

from todo_fastapi_neon.main import app, get_session, Todo
from todo_fastapi_neon import settings


# def test_write_main():

#     connection_string = str(settings.TEST_DATABASE_URL).replace(
#     "postgresql", "postgresql+psycopg")

#     engine = create_engine(
#         connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)

#     SQLModel.metadata.create_all(engine)  

#     with Session(engine) as session:  

#         def get_session_override():  
#                 return session  

#         app.dependency_overrides[get_session] = get_session_override 

#         client = TestClient(app=app)

#         test_title = "Testing ..."
#         test_description = "Testing 123"

#         response = client.post("/todos/",
#             json={"title": test_title, "description": test_description}
#         )

#         data = response.json()

#         assert response.status_code == 200
#         assert data["title"] == test_title
#         assert data["description"] == test_description



# def test_read_list_main():

#     connection_string = str(settings.TEST_DATABASE_URL).replace(
#     "postgresql", "postgresql+psycopg")

#     engine = create_engine(
#         connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)

#     SQLModel.metadata.create_all(engine)  

#     with Session(engine) as session:  

#         def get_session_override():  
#                 return session  

#         app.dependency_overrides[get_session] = get_session_override 
#         client = TestClient(app=app)

#         response = client.get("/todos/")
#         assert response.status_code == 200        


# def test_delete_main():

#     connection_string = str(settings.TEST_DATABASE_URL).replace(
#     "postgresql", "postgresql+psycopg")

#     engine = create_engine(
#         connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)

#     SQLModel.metadata.create_all(engine)

#     with Session(engine) as session:

#         def get_session_override():
#                 return session

#         app.dependency_overrides[get_session] = get_session_override
#         client = TestClient(app=app)

#         response = client.delete("/todos/3")
#         assert response.status_code == 200

#         response = client.get("/todos/")
#         assert response.status_code == 200
    






def test_update_main():

    connection_string = str(settings.TEST_DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg")

    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        def get_session_override():
                return session

        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app=app)

        # test_id = 0
        # test_title = "Testing ..."
        # test_description = "Testing 123"

        # response = client.post("/todos/",
        #     json={"id":test_id,"title": test_title, "description": test_description}
        # )

        # data = response.json()

    # Make a PUT request to update the todo with ID 0
        updated_data = {"title": "Updated Title", "description": "Updated Description"}
        response_update = client.put("/todos/5", json=updated_data)

        assert response_update.status_code == 200

        updated_todo = session.get(Todo, 5)
        assert updated_todo.title == updated_data["title"]
        assert updated_todo.description == updated_data["description"]
     
