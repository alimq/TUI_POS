from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String,\
    Numeric, DateTime, func
from sqlalchemy import ForeignKey
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Session

# Creating an instance of the shared ORM session
engine = create_engine("sqlite:///our.db")
Base.metadata.create_all(engine)
session = Session(bind=engine)

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Numeric(10,2))
    stock_quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    total = Column(Numeric(10,2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class OrderItem(Base):
    __tablename__ = 'order_item'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Numeric(10,2), nullable=False)


class Payment(Base):
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    amount = Column(Numeric(10,2), nullable=False)
    method = Column(String(7),
                    CheckConstraint("method IN ('ewalllet','cash')"
                                    ,name="method"),
                    nullable=False
                    )
    created_at = Column(DateTime, server_default=func.now())