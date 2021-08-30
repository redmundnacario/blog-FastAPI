from fastapi.testclient import TestClient
from fastapi import Depends
from sqlalchemy.orm import Session
import pytest
from fastapi.security import OAuth2PasswordBearer

from blog.oauth2 import get_current_user
from blog.database import get_db

from main import app
import json


client = TestClient(app)



def test_get_blogs():
    response_data = {
                "username" : "red@gmail.com",
                "password" : "12345"
            }

    token = client.post(
                    "/login",
                    data = response_data
    )
    token = token.json()["access_token"]
    response = client.get("/blogs",
        headers = {
            "Authorization" : f"bearer {token}"
        }
    )

    assert response.status_code == 200