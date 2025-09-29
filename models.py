from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

Base=declarative_base()

class Product(Base):
    __tablename__='products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    qty = Column(Integer)
    instock = Column(Boolean)

class Seller(Base):
    __tablename__='sellers'
    seller_id=Column(Integer, primary_key=True, index=True)
    name=Column(String, index=True)
    password=Column(String)

