from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}

def test_get_method():
    response = client.get(f"/method")
    assert response.status_code == 200
    assert response.json() == {"method": "GET"}

def test_put_method():
    response = client.put(f"/method")
    assert response.status_code == 200
    assert response.json() == {"method": "PUT"}

def test_post_method():
    response = client.post(f"/method")
    assert response.status_code == 201
    assert response.json() == {"method": "POST"}

def test_delete_method():
    response = client.delete(f"/method")
    assert response.status_code == 200
    assert response.json() == {"method": f"DELETE"}

def test_options_method():
    response = client.options(f"/method")
    assert response.status_code == 200
    assert response.json() == {"method": "OPTIONS"}
