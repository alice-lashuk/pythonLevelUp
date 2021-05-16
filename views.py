from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import PositiveInt
from sqlalchemy.orm import Session

import crud, schemas
from database import get_db

router = APIRouter()


@router.get("/shippers/{shipper_id}", response_model=schemas.Shipper)
async def get_shipper(shipper_id: PositiveInt, db: Session = Depends(get_db)):
    db_shipper = crud.get_shipper(db, shipper_id)
    if db_shipper is None:
        raise HTTPException(status_code=404, detail="Shipper not found")
    return db_shipper


@router.get("/shippers", response_model=List[schemas.Shipper])
async def get_shippers(db: Session = Depends(get_db)):
    return crud.get_shippers(db)

@router.get("/suppliers", response_model=List[schemas.Supplier])
async def get_suppliers(db: Session = Depends(get_db)):
    return crud.get_suppliers(db)

@router.get("/suppliers/{supplier_id}", response_model=schemas.SupplierID)
async def get_supplier_by_id(supplier_id: PositiveInt, db: Session = Depends(get_db)):
	db_supplier = crud.get_supplier_by_id(db, supplier_id)
	if db_supplier is None:
		raise HTTPException(status_code=404, detail="Supplier not found")
	return db_supplier


@router.get("/suppliers/{supplier_id}/products", response_model=List[schemas.ProductsSupplier])
async def get_supplier_products(supplier_id: PositiveInt, db: Session = Depends(get_db)):
	db_supplier = crud.get_supplier_by_id(db, supplier_id)
	if db_supplier is None:
		raise HTTPException(status_code=404, detail="Supplier not found")
	db_products = crud.get_supplier_products(db, supplier_id)
	return db_products

@router.post("/suppliers", response_model=schemas.SupplierResponse)
async def add_supplier(response: Response, request: schemas.SupplierRequest, db: Session = Depends(get_db)):
	new_id = crud.get_new_id(db).SupplierID + 1
	crud.add_supplier(db, request, new_id)
	new_supplier = schemas.SupplierResponse(SupplierID = new_id, CompanyName = request.CompanyName, ContactName = request.ContactName,ContactTitle = request.ContactTitle, Address = request.Address,  City = request.City, PostalCode = request.PostalCode, Country = request.Country, Phone= request.Phone, Fax= None, HomePage = None)
	response.status_code = 201
	return new_supplier

@router.put("/suppliers/{supplier_id}", response_model=schemas.SupplierResponse)
async def update_supplier(request: schemas.SupplierRequest, supplier_id: int, db: Session = Depends(get_db)):
	crud.update_supplier(db, supplier_id, request)
	updated_supplier = crud.get_supplier_by_id(db, supplier_id)
	return updated_supplier


@router.delete("/suppliers/{supplier_id}")
async def delete_supplier(response: Response, supplier_id: PositiveInt, db: Session = Depends(get_db)):
	db_supplier = crud.get_supplier_by_id(db, supplier_id)
	if db_supplier is None:
		raise HTTPException(status_code=404, detail="Supplier not found")
	crud.delete_supplier(db, supplier_id)
	response.status_code = 204












