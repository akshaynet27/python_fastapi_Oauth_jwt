from fastapi import APIRouter,Depends,status,HTTPException
from pydantic_models import sellerLogin,TokenData
from config_database import session, get_db_session
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import models
from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

SECRET_KEY = "500fbe474d469cfa0fb35c6e41db87dc"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

outh2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post('/login',description="Login for sellers")
def login(request:OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db_session)):
    seller=db.query(models.Seller).filter(models.Seller.name == request.username).first()
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if not pwd_context.verify(request.password,seller.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Incorrect password")
    access_token = generate_token(data={"sub": seller.name})
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(outh2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("sub")
        if name is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        token_data = TokenData(name=name)
        return token_data
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")