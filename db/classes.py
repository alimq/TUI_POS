# *************************************************************************
# Course: CSP1114 PROBLEM SOLVING AND PROGRAM DESIGN
# Lecture / Lab Section: TC1L / TL1L
# Trimester: 2530
# Group Name (from eBwise): TL1L-03
# Names: Imanmalik Alim | Wong Winson | Yong Zi Jing
# IDs: 252FC253VV | 252FC2541L | 252FC253BP
# *************************************************************************

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String,\
    Numeric, DateTime, func
from sqlalchemy import ForeignKey
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Session
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "our.db")
engine = create_engine(f"sqlite:///{db_path}")
Base = declarative_base()

# Define all table classes FIRST
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    category = Column(String(100))
    price = Column(Numeric(10,2))
    #stock_quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    stock_quantity = Column(Integer, default=0)
    last_updated = Column(DateTime)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    total = Column(Numeric(10,2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)


class OrderItem(Base):
    __tablename__ = 'order_item'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Numeric(10,2), nullable=False)


class Payment(Base):
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    amount = Column(Numeric(10,2), nullable=False)
    method = Column(String(7),
                    CheckConstraint("method IN ('ewalllet','cash')"
                                    ,name="method"),
                    nullable=False
                    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Creating an instance of the shared ORM session AFTER defining all classes
Base.metadata.create_all(engine)
session = Session(bind=engine)