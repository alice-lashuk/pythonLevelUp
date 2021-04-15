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

def test_checkPasswrod_method():
	response = client.get(f"/auth?password=haslo&password_hash=013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105e5786ceaabd62bbc27336153d0d316b2d13b36804080c44aa6198c533215")
	assert response.status_code == 204
	response = client.get(f"/auth?password=haslo&password_hash=f34ad4b3ae1e2cf33092e2abb60dc0444781c15d0e2e9ecdb37e4b14176a0164027b05900e09fa0f61a1882e0b89fbfa5dcfcc9765dd2ca4377e2c794837e091")
	assert response.status_code == 401
	response = client.get(f"/auth")
	assert response.status_code == 401
	space = " "
	response = client.get(f"/auth?password={space}&password_hash=f90ddd77e400dfe6a3fcf479b00b1ee29e7015c5bb8cd70f5f15b4886cc339275ff553fc8a053f8ddc7324f45168cffaf81f8c3ac93996f6536eef38e5e40768")
	assert response.status_code == 401
