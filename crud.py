from sqlalchemy.orm import Session

import models
import schemas

def get_shippers(db: Session):
    return db.query(models.Shipper).all()


def get_shipper(db: Session, shipper_id: int):
    return (
        db.query(models.Shipper).filter(models.Shipper.ShipperID == shipper_id).first()
    )

def get_suppliers(db: Session):
	return (
		db.query(models.Supplier).all()
		)

def get_supplier_by_id(db: Session, supplier_id: int):
	return (
		db.query(models.Supplier).filter(models.Supplier.SupplierID == supplier_id).first()
		)

def get_supplier_products(db: Session, supplier_id: int):
	return (
		db.query(models.Product.ProductID, models.Product.ProductName, models.Product.Discontinued, models.Category).join(models.Supplier, models.Supplier.SupplierID == models.Product.SupplierID).join(models.Category, models.Category.CategoryID == models.Product.CategoryID).filter(models.Supplier.SupplierID == supplier_id).order_by(models.Product.ProductID.desc()).all()
		)

def add_supplier(db: Session, supplier: schemas.SupplierRequest, id: int):
		new_supplier = models.Supplier(SupplierID = id, CompanyName = supplier.CompanyName, ContactName = supplier.ContactName, ContactTitle = supplier.ContactTitle, Address = supplier.Address, City = supplier.City, PostalCode = supplier.PostalCode, Country = supplier.Country, Phone = supplier.Phone)
		db.add(new_supplier)
		db.commit()

def get_new_id(db: Session):
	return (
        db.query(models.Supplier).order_by(models.Supplier.SupplierID.desc()).first()
    )
# 