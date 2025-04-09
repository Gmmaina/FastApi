from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import psycopg.rows
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# postgres db connection

# while True:
#     try:
#         conn = psycopg.connect(
#             user="postgres",
#             password="383910maina",
#             host="127.0.0.1",
#             port="5432",
#             dbname="fastapi",
#             row_factory=psycopg.rows.dict_row,
#             autocommit = True
#         )
#         cursor = conn.cursor()
#         print("Connected to the database")
#         break
#     except Exception as e:
#         print(e)
#         print("Error connecting to the database")
#         time.sleep(5)
    
