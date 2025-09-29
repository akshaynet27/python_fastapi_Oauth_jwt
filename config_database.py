from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

basedir=os.path.abspath(os.path.dirname(__file__))
database_url='sqlite:///' + os.path.join(basedir, 'app.db')

engine=create_engine(database_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    db=session()
    try:
        yield db
    finally:
        db.close()