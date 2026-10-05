from typing import Generic, TypeVar
from models.base_model import BaseModel
T = TypeVar('T', bound='BaseModel')


class Repository(Generic[T]):
    def __init__(self, session, model):
        self.session = session,
        self.model = model

    def find_by_id(self, id):
        return self.session.query(self.model).filter_by(self.model.id==id).first()