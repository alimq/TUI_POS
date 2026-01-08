from sqlalchemy.orm import Session
from sqlalchemy import text, create_engine
engine = create_engine("sqlite:///our.db")
session = Session(bind=engine)
session.execute(text("drop table if exists product"))
session.execute(text("drop table if exists payment"))
session.execute(text("drop table if exists 'order'"))
session.execute(text("drop table if exists order_item"))
from classes import *

# before adding fake data, clear the table
session.execute(text("delete from product"))
products = [
    Product("fries",6,40),
    Product("nachos, Dorito",6,20),
    Product("soft drink",5,30),
    Product("oil",10,20),
    Product("cheddar",6,15),
    Product("mozzarella",6,15),
    Product("cheese sauce",5,15),
    Product("minced beef",8,15),
    Product("minced chicken breasts",8,15),
    Product("corn starch",5,15)
]
# ...
from datetime import datetime
orders = [
    Order(0,datetime(2025,12,5)),
    Order(0,datetime(2025,12,7)),
    Order(0,datetime(2025,12,9)),

    Order(0,datetime(2025,12,12)),
    Order(0,datetime(2025,12,14)),
    Order(0,datetime(2025,12,15)),

    Order(0,datetime(2025,12,18)),
    Order(0,datetime(2025,12,19)),
    Order(0,datetime(2025,12,20)),
]
order_items = [
    OrderItem(1,3,5),
    OrderItem(1,4,4),

    OrderItem(2,7,3),
    OrderItem(2,3,3),
    OrderItem(2,4,6),

    OrderItem(3,6,2),
    OrderItem(3,7,2),
    OrderItem(3,3,4),
    OrderItem(3,4,3),

    OrderItem(4,6,1),
    OrderItem(4,7,3),
    OrderItem(4,3,3),
    OrderItem(4,4,2),

    OrderItem(5,6,5),
    OrderItem(5,7,2),
    OrderItem(5,3,6),
    OrderItem(5,4,1),

    OrderItem(6,6,10),
    OrderItem(6,7,4),
    OrderItem(6,3,7),
    OrderItem(6,4,0),

    OrderItem(7,6,11),
    OrderItem(7,7,5),
    OrderItem(7,3,8),
    OrderItem(7,4,1),

    OrderItem(8,6,12),
    OrderItem(8,7,7),
    OrderItem(8,3,4),
    OrderItem(8,4,0),

    OrderItem(9,6,13),
    OrderItem(9,7,9),
    OrderItem(9,3,1),
    OrderItem(9,4,1),
]
payments = [
    Payment(1,'ewallet'),
    Payment(2,'cash'),
    Payment(3,'cash'),
    Payment(4,'ewallet'),
    Payment(5,'ewallet'),
    Payment(6,'ewallet'),
    Payment(7,'cash'),
    Payment(8,'ewallet'),
    Payment(9,'ewallet')
]
for pr in products:
    session.add(pr)
for oi in order_items:
    session.add(oi)
    orders[oi.order_id-1].total += oi.quantity *\
          products[oi.product_id-1].price
for o in orders:
    session.add(o)
for pa in payments:
    session.add(pa)
session.commit()