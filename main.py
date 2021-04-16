
from fastapi import FastAPI, Response, status
from typing import Optional
from pydantic import BaseModel
import hashlib
from datetime import datetime, timedelta

app = FastAPI()
app.id = 0

class PersonRequest(BaseModel):
    name: str
    surname: str

class PersonResp(BaseModel):
	id: int
	name: str
	surname: str
	register_date: str
	vaccination_date: str 

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

@app.post("/register", response_model=PersonResp)
def registerPerson(response: Response, request:PersonRequest):
	app.id += 1
	register_date = datetime.date(datetime.now())
	new_name = request.name.strip()
	new_surname = request.surname.strip()
	new_name = new_name.replace(" ", "").replace('\n', "").replace('\r', "")
	new_surname = new_surname.replace(" ", "").replace('\n', "").replace('\r', "")

	result_name = ''.join(filter(str.isalpha, new_name))    
	result_surname =  ''.join(filter(str.isalpha, new_surname))    
	num_days = len(result_name) + len(result_surname)
	vac_date = register_date + timedelta(days=num_days)
	response.status_code = 201
	return PersonResp(id = app.id, name = request.name, surname = request.surname, register_date = str(register_date), vaccination_date = str(vac_date))
	

























