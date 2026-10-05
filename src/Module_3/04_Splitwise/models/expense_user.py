from sqlalchemy import Column, Integer, String, ForeignKey, Table, Enum as SAEnum
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, declarative_base
from models.expense_type import ExpenseType


class ExpenseUser(BaseModel):
    __tablename__ = "expense_users"

    expense_id = Column(Integer, ForeignKey("expenses.id"))
    expense = relationship("Expense", back_populates="expense_users")

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")

    amount = Column(Integer)
    expense_user_type = Column(SAEnum(ExpenseType))