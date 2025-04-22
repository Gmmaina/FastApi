from jose import jwt
from app.config import settings
from app import schemas
import pytest


def test_create_user(client):
    res = client.post(
        "/users/", json={"username": "testuser4", "email": "test4@gmail.com",  "phone_number":"0110081377", "password": "testpass"}
    )
    assert res.status_code == 201, res.json()
    new_user = schemas.UserResponse(**res.json())
    assert new_user.username == "testuser4"

def test_user_login(test_user, client):
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
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['user_id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
    assert ress.status_code == 200
    

@pytest.mark.parametrize("username, password, status_code",
    [
        ("testuser", "testpass11", 401),
        ("testuserqq", "testpass", 401),
        ("testuser@gmail.com", "testpass2", 401),
        ("testuser3", "testpass3", 401),
        ("testuser@gmail.com", "testpass4", 401),
        (None, "testpass", 422),
        ("testuser", None, 422),
    ]
)
  
def test_incorrect_login(test_user, client, username, password, status_code):
    res = client.post(
        "/login", data={"username": username, "password": password}
    )
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid Credentials"