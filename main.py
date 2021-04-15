
from fastapi import FastAPI, Response, status
import hashlib

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello world!"}

@app.get("/method")
def root():
    return {"method": "GET"}

@app.put("/method")
def root():
    return {"method": "PUT"}

@app.post("/method", status_code=201)
def root():
    return {"method": "POST"}

@app.delete("/method")
def root():
    return {"method": f"DELETE"}

@app.options("/method")
def root():
    return {"method": "OPTIONS"}

@app.get("/auth")
def checkPassword(password, password_hash, response: Response):
	hash = hashlib.sha512(str(password).encode("utf-8")).hexdigest()
	if hash == password_hash:
		response.status_code = 204
	else: 
		response.status_code = 401

