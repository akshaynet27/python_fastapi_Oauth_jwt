from fastapi import APIRouter,Depends,status,HTTPException
from pydantic_models import Product,TokenData
from config_database import session, get_db_session, engine
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import models
import login

models.Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
router = APIRouter()

products=[Product(id=1,name="Laptop",price=50000,qty=10,instock=True),
        Product(id=2,name="Mobile",price=20000,qty=5,instock=True),
        Product(id=3,name="Tablet",price=15000,qty=6,instock=True)
    ] # The Product used here is from pydantic_models.py (Mentioning it here because there is also a Product class in models.py which is ORM mapped)

def init_db():
    db=session()
    count = db.query(models.Product).count()
    if count == 0:
        for product in products:
            db.add(models.Product(**product.model_dump()))
        db.commit()

init_db()

@router.get('/products',description="Get all products available in the database")
def get_products(db:Session = Depends(get_db_session)):
    db_products=db.query(models.Product).all()
    return db_products

@router.get('/product/{id}',description='Get a product by its ID. Returns the product details if found, otherwise returns an error message.')
def get_product_by_id(id: int, db: Session = Depends(get_db_session)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if db_product:
        return db_product
    return {"error": "Product not found"}

@router.post('/product',description="Add a new product to the database")
def add_product(product:Product,db:Session = Depends(get_db_session),current_user:TokenData = Depends(login.get_current_user)):
    db.add(models.Product(**product.model_dump()))
    db.commit()
    return {'message':'Product added successfully'}

@router.put('/product',description="Update an existing product in the database {ID cannot be updated}")
def update_product(id:int,product:Product,db: Session = Depends(get_db_session),current_user:TokenData = Depends(login.get_current_user)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.price = product.price
        db_product.qty = product.qty
        db_product.instock = product.instock
        db.commit()
        return {'message':'Product updated successfully'}
    return {"error":"Product not found"}

@router.delete('/product',description="Delete a product from the database by its ID")
def update_product(id:int,db: Session = Depends(get_db_session),current_user:TokenData = Depends(login.get_current_user)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return {'message':'Product deleted successfully'}
    return {"error":"Product not found"}