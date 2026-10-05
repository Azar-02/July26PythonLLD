from sqlalchemy import Column, Integer, String
from models.base_model import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    name = Column(String)
    phone_number = Column(String)
    password = Column(String)