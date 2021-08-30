from fastapi.testclient import TestClient

from main import app
from blog.token import create_access_token


client = TestClient(app)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

def test_login():

    data = {
                "username" : "red@gmail.com",
                "password" : "12345"
            }
    response = client.post(
                    "/login",
                    data = data
    )
    #check response status code
    assert response.status_code == 200

    #create jwt token
    access_token = create_access_token(
        data = {"sub": data["username"]}, expires_delta = ACCESS_TOKEN_EXPIRE_MINUTES
    )

    #check response json
    assert response.json() == {"access_token": access_token, "token_type": "bearer"}


def test_login_fail():
    data = {
                "username" : "red@gmail.com",
                "password" : "123456"
            }

    response = client.post(
                    "/login",
                    data = data
    )
    
    assert response.status_code == 401
    
    #check response json
    assert response.json() ==  {"detail" : "Incorrect username or password."}

def test_signup():
    data = {
                "username" : "john",
                "email" : "john@gmail.com",
                "password" : "123456"
            }

    response = client.post(
                    "/signup",
                    json = data
    )    

    assert response.status_code == 201


def test_signup_fail():
    data = {
                "username" : "john",
                "email" : "john@gmail.com"
            }

    response = client.post(
                    "/signup",
                    json = data
    )    

    assert response.status_code == 422