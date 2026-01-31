"""
The SQL schema for the oden sales, based on the existing ORM but slightly modified
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String,\
    Numeric, DateTime, func, Boolean
from sqlalchemy import ForeignKey

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Session, relationship

# Product table stores basic information of the oden items, such as selling price, category which in this case is oden and number of units per stick only
class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    category = Column(String(100))
    price = Column(Numeric(10,2)) # Selling Price (e.g. RM 1.50)
    sell_units = Column(Integer, nullable=False)
    # Total unopened packets currently in the storeroom
    stock_quantity = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class InventoryBatch(Base):
    __tablename__ = 'inventory_batch'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    vendor = Column(String(100))
    batch_cost = Column(Numeric(10, 2), nullable=False) # Purchase Price
    # Granular approximated units of the packet. Allows negative integers to account for user-induced errors such as scooping more or less at any given time and also accounts for production margins.
    units = Column(Integer, nullable=False)    
    opened_at = Column(DateTime(timezone=True), server_default=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)
    is_completed = Column(Boolean, default=False)
    product = relationship("Product", backref="batches")

# Database initialization
engine = create_engine("sqlite:///oden.db")
Base.metadata.create_all(engine)
session = Session(bind=engine)