from pydantic import BaseModel, PositiveInt, constr
from typing import List


class Shipper(BaseModel):
    ShipperID: PositiveInt
    CompanyName: constr(max_length=40)
    Phone: constr(max_length=24)

    class Config:
        orm_mode = True

class Supplier(BaseModel):
    SupplierID: PositiveInt
    CompanyName: constr(max_length=40)
    # Fax: constr(max_length=40) = None	
    class Config:
        orm_mode = True

class SupplierID(BaseModel):
    SupplierID: PositiveInt
    CompanyName: constr(max_length=40) = None
    ContactName: constr(max_length=40) = None
    ContactTitle: constr(max_length=40) = None
    Address: constr(max_length=40)= None
    City: constr(max_length=40)= None
    Region: constr(max_length=40)= None
    PostalCode: constr(max_length=40)= None
    Country: constr(max_length=40)= None
    Phone: constr(max_length=40)= None
    Fax: constr(max_length=40)= None
    HomePage: constr(max_length=200)= None	

    class Config:
        orm_mode = True

class Category(BaseModel):
	CategoryID: PositiveInt = None
	CategoryName: constr(max_length=40)= None

	class Config:
		orm_mode = True

class ProductsSupplier(BaseModel):
	ProductID: PositiveInt = None
	ProductName: constr(max_length=40) = None
	Category: Category
	# CategoryID: PositiveInt = None
	Discontinued: int = None

	class Config:
		orm_mode = True




