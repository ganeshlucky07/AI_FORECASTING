from datetime import date

from sqlalchemy import Column, Date, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Product(Base):
    """
    Simple product master table used by the demand module.
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)

    demand_history = relationship("DemandHistory", back_populates="product")


class DemandHistory(Base):
    """
    Historical demand (sales/usage) per product and date.
    """

    __tablename__ = "demand_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)
    date = Column(Date, index=True)
    quantity = Column(Float)

    product = relationship("Product", back_populates="demand_history")


class Employee(Base):
    """
    Minimal employee table for workforce planning.
    """

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    department = Column(String, index=True)
    skill = Column(String, index=True)


class WorkforcePlan(Base):
    """
    Suggested staffing levels per department & date.
    """

    __tablename__ = "workforce_plans"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    department = Column(String, index=True)
    required_headcount = Column(Integer)


class BudgetHistory(Base):
    """
    Historical financial data used by the budget module.
    """

    __tablename__ = "budget_history"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    revenue = Column(Float)
    expenses = Column(Float)
    workforce_cost = Column(Float)

