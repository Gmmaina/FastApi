import pytest
from .database import session, client
from app import schemas
    
# def test_create_user():
#     res = client.post(
#         "/users/", json={"username": "testuser4", "email": "test4@gmail.com",  "phone_number":"0110081377", "password": "testpass"}
#     )
#     print(res.json())
#     new_user = schemas.UserResponse(**res.json())
#     assert new_user.username == "testuser4"    
#     assert res.status_code == 201
  
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
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data["password"]
    return new_user

def test_create_user(client):
    res = client.post(
        "/users/", json={"username": "testuser4", "email": "test4@gmail.com",  "phone_number":"0110081377", "password": "testpass"}
    )
    assert res.status_code == 201, res.json()
    new_user = schemas.UserResponse(**res.json())
    assert new_user.username == "testuser4"

def test_user_login(client, test_user):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']}
    )
    ress = client.post(
        "/login", data={"username": test_user['username'], "password": test_user['password']}
    )
    
    # res = client.post(
    #     "/login", data={"username": "testuser@gmail.com", "password": "testpass"}
    # )   
    # ress = client.post(
    #     "/login", data={"username": "testuser", "password": "testpass"}
    # )
    print(res.json())
    assert res.status_code == 200
    assert ress.status_code == 200