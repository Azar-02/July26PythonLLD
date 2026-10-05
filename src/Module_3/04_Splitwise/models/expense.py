from sqlalchemy import Column, Integer, String, ForeignKey, Table, Enum as SAEnum
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, declarative_base
from models.expense_type import ExpenseType


class Expense(BaseModel):
    __tablename__ = "expenses"

    description = Column(String)
    amount = Column(Integer)
    expense_type = Column(SAEnum(ExpenseType))

    group_id = Column(Integer, ForeignKey("user_groups.id"))
    group = relationship("Group", back_populates="expenses")

    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_by = relationship("User")

    expense_users = relationship("ExpenseUser", back_populates="expense")