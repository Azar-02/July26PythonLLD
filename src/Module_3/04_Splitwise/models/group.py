from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, declarative_base


group_members_table = Table(
    "group_members",
    BaseModel.metadata,
    Column("group_id", Integer, ForeignKey("user_groups.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
)

class Group(BaseModel):
    __tablename__ = "user_groups"

    name = Column(String)

    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_by = relationship("Users")

    expenses = relationship("Expense", back_populates=("group"))

    members = relationship("Users", secondary=group_members_table)