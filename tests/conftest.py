from sqlalchemy import create_engine
from app.database import get_db, Base
from app.main import app
import pytest
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app import models, schemas
from fastapi.testclient import TestClient
from app.oauth2 import create_access_token

# client = TestClient(app)


SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)


# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
        

# app.dependency_overrides[get_db] = override_get_db 

    
@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
   
@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
@pytest.fixture
def test_user(client):
    user_data = {
        "username": "testuser",
        "email": "testuser@gmail.com",
        "phone_number": "0110081477",  
        "password": "testpass"
    }
    res = client.post("/users/", json=user_data) 
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['user_id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session):
    post_data = [
        {
            "title": "test title",
            "content": "test content",
            "owner_id": test_user['user_id']
        },
        {
            "title": "second test title",
            "content": "second test content",
            "owner_id": test_user['user_id']
        },
        {
            "title": "third test title",
            "content": "third test content",
            "owner_id": test_user['user_id']
        },
        {
            "title": "fourth test title",
            "content": "fourth test content",
            "owner_id": test_user['user_id']
        },
        {
            "title": "fifth test title",
            "content": "fifth test content",
            "owner_id": test_user['user_id']
        }
    ]

    def create_post_model(post):
        return models.Posts(**post)

    post_map = map(create_post_model, post_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    # Query the posts from the database to return them
    posts = session.query(models.Posts).all()
    return posts