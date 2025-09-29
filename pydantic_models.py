from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    name: str
    price: float
    qty:int
    instock:bool

class Seller(BaseModel): #The table contains seller_id as primary key which is auto generated so not including it here
    name: str
    password: str

class sellerLogin(BaseModel):  #Actually we can use the Seller class for login too but creating a separate class for clarity
    name: str
    password: str

class TokenData(BaseModel):
    name: Optional[str] = None