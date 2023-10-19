# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
#from my_database import Base,engine,SessionLocal
from sqlalchemy.orm import relationship


from sqlalchemy import create_engine,TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "sqlite:///./my_database.db"  # Use your database URL here

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
Base = declarative_base()


class UserCreate(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)  
    username = Column(String, index=True)
    email = Column(String, index = True,unique=True)
    password = Column(String, index=True)

class WatchList(Base):
    __tablename__ = "watchlists"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id",ondelete="CASCADE"),nullable = False)
    item_id = Column(Integer, ForeignKey("items.item_id",ondelete="CASCADE"),nullable = False)
    price = Column(Float)
    date = Column(TIMESTAMP)



class Item(Base):
    __tablename__ = "items"
    item_id = Column(Integer,primary_key=True,index=True)
    link = Column(String)
    site = Column(String)
    price = Column(Float)
    date = Column(TIMESTAMP)

class ItemValue(Base):
    __tablename__ = "itemvalue"
    value_id = Column(Integer,primary_key=True)
    item_id = Column(Integer,ForeignKey("watchlists.item_id",ondelete="CASCADE"))
    price = Column(Float)
    date = Column(TIMESTAMP)

try:
    Base.metadata.create_all(engine)

except Exception as e:
    print(f"Error creating tables: {e}")