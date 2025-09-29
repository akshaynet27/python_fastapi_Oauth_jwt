from fastapi import FastAPI, Depends, APIRouter
from pydantic_models import Product, Seller
import json
from config_database import session, engine, get_db_session
import models
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import login


models.Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

app=FastAPI(title="Product Management website",description="This is a simple product management website",version="1.0.0")

app.include_router(login.router)
@app.get('/')
def greet():
    return "Hello World"


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

@app.get('/products',description="Get all products available in the database")
def get_products(db:Session = Depends(get_db_session),current_user:Seller = Depends(login.get_current_user)):
    db_products=db.query(models.Product).all()
    return db_products

@app.get('/product/{id}',description='Get a product by its ID. Returns the product details if found, otherwise returns an error message.')
def get_product_by_id(id: int, db: Session = Depends(get_db_session)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if db_product:
        return db_product
    return {"error": "Product not found"}

@app.post('/product',description="Add a new product to the database")
def add_product(product:Product,db:Session = Depends(get_db_session)):
    db.add(models.Product(**product.model_dump()))
    db.commit()
    return json.dumps({'message':'Product added successfully'})

@app.put('/product',description="Update an existing product in the database {ID cannot be updated}")
def update_product(id:int,product:Product,db: Session = Depends(get_db_session)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.price = product.price
        db_product.qty = product.qty
        db_product.instock = product.instock
        db.commit()
        return json.dumps({'message':'Product updated successfully'})
    return {"error":"Product not found"}

@app.delete('/product',description="Delete a product from the database by its ID")
def update_product(id:int,db: Session = Depends(get_db_session)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return json.dumps({'message':'Product deleted successfully'})
    return {"error":"Product not found"}

@app.post('/seller',description="Add a new seller to the database")
def create_seller(seller_details:Seller,db: Session = Depends(get_db_session)):
    hashed_pwd=pwd_context.hash(seller_details.password)
    db.add(models.Seller(name=seller_details.name,password=hashed_pwd))
    db.commit()
    return {'message':'Seller created successfully'}