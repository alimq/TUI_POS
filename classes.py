from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String,\
    Numeric, DateTime, func

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Numeric(10,2))
    stock_quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
    def __init__(self,name,price,stock_q):
        self.name = name
        self.price = price
        self.stock_quantity = stock_q

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    total = Column(Numeric(10,2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    def __init__(self,total,created_at=None):
        self.total = total
        if created_at is not None:
            self.created_at = created_at

from sqlalchemy import ForeignKey

class OrderItem(Base):
    __tablename__ = 'order_item'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    def __init__(self,order_id,product_id,quantity):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity

from sqlalchemy import CheckConstraint

class Payment(Base):
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    method = Column(String(7),
                    CheckConstraint("method IN ('ewallet','cash')"
                                    ,name="method"),
                    nullable=False
                    )
    created_at = Column(DateTime, server_default=func.now())
    def __init__(self,order_id,method):
        self.order_id = order_id
        self.method = method

engine = create_engine("sqlite:///our.db")
Base.metadata.create_all(engine)