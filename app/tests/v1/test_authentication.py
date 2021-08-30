from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_login():
    response = client.post(
                    "/login",
                    data={
                        "username" : "red@gmail.com",
                        "password" : "12345"
                    }
    )
    print(response.status_code)
    assert response.status_code == 200