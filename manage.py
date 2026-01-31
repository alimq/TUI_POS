# *************************************************************************
# Course: CSP1114 PROBLEM SOLVING AND PROGRAM DESIGN
# Lecture / Lab Section: TC1L / TL1L
# Trimester: 2530
# Group Name (from eBwise): TL1L-03
# Names: Imanmalik Alim | Wong Winson | Yong Zi Jing
# IDs: 252FC253VV | 252FC2541L | 252FC253BP
# *************************************************************************

from classes import session, Product

# mock products to be inserted to database
products = [
    # Beverages
    Product(name="Espresso", category="Beverages", price=3.50, stock_quantity=50),
    Product(name="Cappuccino", category="Beverages", price=4.75, stock_quantity=30),
    Product(name="Latte", category="Beverages", price=4.50, stock_quantity=40),
    Product(name="Americano", category="Beverages", price=3.00, stock_quantity=35),
    Product(name="Mocha", category="Beverages", price=5.25, stock_quantity=25),
    
    # Pastries
    Product(name="Croissant", category="Pastries", price=2.25, stock_quantity=20),
    Product(name="Blueberry Muffin", category="Pastries", price=3.00, stock_quantity=15),
    Product(name="Chocolate Chip Cookie", category="Pastries", price=1.75, stock_quantity=40),
    Product(name="Danish", category="Pastries", price=2.50, stock_quantity=18),
    
    # Sandwiches
    Product(name="Turkey Club", category="Sandwiches", price=7.50, stock_quantity=12),
    Product(name="BLT", category="Sandwiches", price=6.75, stock_quantity=15),
    Product(name="Veggie Wrap", category="Sandwiches", price=6.25, stock_quantity=10),
    
    # Snacks
    Product(name="Potato Chips", category="Snacks", price=1.50, stock_quantity=30),
    Product(name="Granola Bar", category="Snacks", price=2.00, stock_quantity=25),
]

for product in products:
    session.add(product)

session.commit()

print(f'Successfully added {len(products)} to database')

print("Products added:")
for p in products:
    print(f'{p.name} ({p.category}): RM{p.price} - Stock {p.stock_quantity}')
