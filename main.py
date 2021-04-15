
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
	hash = hashlib.sha512(str(password).encode("utf-8")).hexdigest()
	# if password==null || password_hash==null:
	# 	response.status_code = 401
	if hash == password_hash:
		response.status_code = 204
		return{"method": "204", "hash": hash}
	else: 
		response.status_code = 401
		return{"method": "401", "hash": hash}

