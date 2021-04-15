
from fastapi import FastAPI, Response, status
from typing import Optional
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
def checkPassword(response: Response, password: Optional[str] = None, password_hash: Optional[str] = None):
	new_password = ''

	if password is None:
		new_password = password
	else:
		new_password = password.strip()
	hash = hashlib.sha512(str(new_password).encode("utf-8")).hexdigest()
	if password == "":
		response.status_code = 401
	elif hash == password_hash:
		response.status_code = 204
	else: 
		response.status_code = 401

