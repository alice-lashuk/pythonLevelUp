
from fastapi import FastAPI, Response, Request, status, Cookie
from typing import Optional
from pydantic import BaseModel
import hashlib
import sqlite3
from hashlib import sha256
from datetime import datetime, timedelta
from fastapi.templating import Jinja2Templates
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi.responses import PlainTextResponse, RedirectResponse, HTMLResponse, JSONResponse
import random

# http://4dm1n:NotSoSecurePa$$@127.0.0.1:8000/
USERNAME = "4dm1n"
PASSWORD = "NotSoSecurePa$$"
# SESSIONS_STORED = 1
SESSIONS_STORED = 3

app = FastAPI()
app.id = 0
app.persons = []
templates = Jinja2Templates(directory="templates")
app.secret_key = "vsd;lgj[op"
app.session_tokens = []
app.cookie_tokens = []
random.seed(datetime.now())
security = HTTPBasic()
app.acceptable_order = ["first_name", "last_name", "city"]


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific 


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()


@app.get("/categories")
async def get_categories():
	app.db_connection.row_factory = sqlite3.Row
	data = app.db_connection.execute("SELECT CategoryID, CategoryName FROM Categories ORDER BY CategoryID;").fetchall()
	return {"categories" :[{"id": f"{x['CategoryID']}".strip(), "name": f"{x['CategoryName']}".strip()} for x in data]}

@app.get("/customers")
async def get_customers():
	app.db_connection.row_factory = sqlite3.Row
	data = app.db_connection.execute("SELECT CustomerID, CompanyName, Address, PostalCode, City, Country FROM Customers ORDER BY CustomerID;").fetchall()
	return {"customers" :[{"id": f"{x['CustomerID']}".strip(), "name": x["CompanyName"].strip(), "full_address": f"{x['Address']} {x['PostalCode']} {x['City']} {x['Country']}".strip()} for x in data]}


@app.get("/products/{id}")
async def get_product(id: str,):
	app.db_connection.row_factory = sqlite3.Row
	data = app.db_connection.execute("SELECT ProductID, ProductName FROM Products WHERE ProductID = ?", (id,)).fetchone()
	if data == None:
		raise HTTPException(status_code=404, detail="Product not found")
	return {"id": data['ProductID'], "name": data['ProductName']}

@app.get("/employees")
async def get_emplpyees(limit: int, offset: int, order: str):
	if order not in app.acceptable_order:
		raise HTTPException(status_code=400, detail="Chnage order value")
	if order == "first_name":
		order = "FirstName"
	elif order == last_name:
		order == "LastName"
	elif order == city:
		order = "City"
	app.db_connection.row_factory = sqlite3.Row
	data = app.db_connection.execute("SELECT EmployeeID, LastName, FirstName, City FROM Employees ORDER BY ? LIMIT ?,?",(order,limit, offset,)).fetchall()
	return {"employees":[{"id": x["EmployeeID"], "last_name": x["LastName"], "first_name": x["FirstName"], "city": x["City"]} for x in data]}




class PersonRequest(BaseModel):
    name: str
    surname: str

class PersonResp(BaseModel):
	id: int
	name: str
	surname: str
	register_date: str
	vaccination_date: str 

def request_str(request: Request):
	return """
Request:
	method - '{method}'
	url - '{url}'
	query - '{query}'
	cookies - '{cookies}'
	""".format(
			method=request.method,
			url=request.url,
			query=request.query_params,
			cookies=request.cookies
		)

def log_request(request: Request):
	print(request_str(request))


def valid_credentials(credentials: HTTPBasicCredentials):
	return credentials.username == USERNAME and credentials.password == PASSWORD

def generate_token(credentials: HTTPBasicCredentials, randomize: bool = True):
	seed = credentials.username + credentials.password + (str(random.randint(0, 1000)) if randomize else "")
	return sha256(seed.encode()).hexdigest()

def store_token(token_store: [], token: str):
	if token not in token_store:
		if (len(token_store) >= SESSIONS_STORED):
			token_store.pop(0)
		token_store.append(token)

def logout(token_store: [], token: str, format: str):
	if token in token_store:
		token_store.remove(token)
		return RedirectResponse(url=f"/logged_out?format={format}", status_code=303)
	else:
		raise HTTPException(status_code=401, detail="Unathorised logout")

def welcome(token_store: [], token: str, format: str):
	if token in token_store:
		if format == "json":
			return JSONResponse(content={"message": "Welcome!"}, status_code=200)
		elif format == "html":
			return HTMLResponse(content="<h1>Welcome!</h1>", status_code=200)
		else:
			return PlainTextResponse(content="Welcome!", status_code=200)
	else:
		raise HTTPException(status_code=401, detail="Unathorised welcome")


@app.post("/login_session")
def log_session(request: Request, response: Response, credentials: HTTPBasicCredentials = Depends(security)):
	log_request(request)
	if valid_credentials(credentials):
		token = generate_token(credentials)
		store_token(app.cookie_tokens, token)
		response.status_code = 201
		response.set_cookie(key="session_token", value=token)
		return app.cookie_tokens
	else:
		response.status_code = 401		


@app.post("/login_token")
def log_token(request: Request, response: Response, credentials: HTTPBasicCredentials = Depends(security)):
	log_request(request)
	if valid_credentials(credentials):
		token = generate_token(credentials)
		store_token(app.session_tokens, token)
		response.status_code = 201
		return {"token": token}
	else:
		response.status_code = 401	

@app.delete("/logout_session")
def logout_session(request: Request, response: Response, format: Optional[str] = "plain", session_token: str = Cookie(None)):
	log_request(request)	
	return logout(app.cookie_tokens, session_token, format)

@app.delete("/logout_token")
def logout_token(request: Request, response: Response, token: str, format: Optional[str] = "plain"):
	log_request(request)
	return logout(app.session_tokens, token, format)

@app.get("/logged_out")
def logged_out(request: Request,response: Response, format: str):
	log_request(request)
	if format == "json":
		return JSONResponse(content={"message": "Logged out!"}, status_code=200)
	elif format == "html":
		return HTMLResponse(content="<h1>Logged out!</h1>", status_code=200)
	else:
		return PlainTextResponse(content="Logged out!", status_code=200)


@app.get("/welcome_session")
def welcome_session(request: Request, format: Optional[str] = None, session_token: str = Cookie(None)):
	log_request(request)
	return welcome(app.cookie_tokens, session_token, format)


@app.get("/welcome_token")
def welcome_token(request: Request, token: str, format: Optional[str] = None):
	log_request(request)
	return welcome(app.session_tokens, token, format)

@app.get("/reset")
def reset():
	app.session_tokens = []
	app.cookie_tokens = []
	return PlainTextResponse(content="OK", status_code=200)

@app.get("/sessions")
def get_sessions():
	return {
		"sessions_tokens": {
			"data": app.session_tokens,
			"id": id(app.session_tokens)
		}, 
		"cookie_tokes": {
			"data": app.cookie_tokens,
			"id": id(app.cookie_tokens)
		}
	}

@app.get("/hello")
def send_date(request: Request):
	date = datetime.date(datetime.now())
	return templates.TemplateResponse("template.html.j2", {"request": request, "date": date})



@app.get("/")
def root(request: Request):
	print(request_str(request))
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
		if not app.persons:
			response.status_code = 404
		else:
			for i in app.persons:
				if i.id == new_id:
					response.status_code = 200
					return i
			response.status_code = 404



	
























