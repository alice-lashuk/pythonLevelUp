
from fastapi import FastAPI, Response, Request, status
from typing import Optional
from pydantic import BaseModel
import hashlib
from hashlib import sha256
from datetime import datetime, timedelta
from fastapi.templating import Jinja2Templates
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED

app = FastAPI()
app.id = 0
app.persons = []
templates = Jinja2Templates(directory="templates")
app.secret_key = "vsd;lgj[op"
app.access_token_s = ""
app.access_token_c = ""
security = HTTPBasic()

class PersonRequest(BaseModel):
    name: str
    surname: str

class PersonResp(BaseModel):
	id: int
	name: str
	surname: str
	register_date: str
	vaccination_date: str 


@app.post("/login_session")
def log_session( response: Response, credentials: HTTPBasicCredentials = Depends(security)):
	if credentials.username != "4dm1n" or credentials.password != "NotSoSecurePa$$":
		response.status_code = 401
	else:
		session_token = sha256(f"{credentials.username}{credentials.password}{app.secret_key}".encode()).hexdigest()
		app.access_token_c = session_token
		response.set_cookie(key="session_token", value="hello")


@app.post("/login_token")
def log_token(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
	if credentials.username != "4dm1n" or credentials.password != "NotSoSecurePa$$":
		response.status_code = 401
	else:
		session_token = sha256(f"{credentials.username}{credentials.password}{app.secret_key}".encode()).hexdigest()
		app.session_token_s = session_token
		return {"token": session_token}






@app.get("/hello")
def send_date(request: Request):
	date = datetime.date(datetime.now())
	return templates.TemplateResponse("template.html.j2", {"request": request, "date": date})

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
	new_person = PersonResp(id = app.id, name = request.name, surname = request.surname, register_date = str(register_date), vaccination_date = str(vac_date))
	app.persons.append(new_person)	
	return new_person

@app.get("/people")
def get_people():
	return app.persons

@app.get("/patient/{id}")
def get_person_by_id(id: str, response: Response):
	new_id = int(id)
	if new_id < 0:
		response.status_code = 400
	else:
		# if len(app.persons) < 1:
		if not app.persons:
			response.status_code = 404
		else:
			for i in app.persons:
				if i.id == new_id:
					response.status_code = 200
					return i
			response.status_code = 404



	
























