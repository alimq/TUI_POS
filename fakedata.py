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
order_total = [0] * 4
order_items = [
    OrderItem(1,3,5),
    OrderItem(1,4,4),
    OrderItem(2,7,3),
    OrderItem(3,6,2)
]
payments = [
    Payment(1,'ewallet'),
    Payment(2,'cash'),
    Payment(3,'cash'),
    Payment(4,'ewallet')
]
for pr in products:
    session.add(pr)
for oi in order_items:
    session.add(oi)
    order_total[oi.order_id-1] += oi.quantity *\
          products[oi.product_id-1].price
for o in order_total:
    session.add(Order(o))
for pa in payments:
    session.add(pa)
session.commit()