from fastapi import APIRouter,Depends
from pydantic_models import Seller
import models
from config_database import session, get_db_session, engine
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)

router = APIRouter()
@router.post('/seller-signup',description="Add a new seller to the database")
def create_seller(seller_details:Seller,db: Session = Depends(get_db_session)):
    hashed_pwd=pwd_context.hash(seller_details.password)
    db.add(models.Seller(name=seller_details.name,password=hashed_pwd))
    db.commit()
    return {'message':'Seller created successfully'}