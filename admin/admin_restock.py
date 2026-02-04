# *************************************************************************
# Course: CSP1114 PROBLEM SOLVING AND PROGRAM DESIGN
# Lecture / Lab Section: TC1L / TL1L
# Trimester: 2530
# Group Name (from eBwise): TL1L-03
# Names: Imanmalik Alim | Wong Winson | Yong Zi Jing
# IDs: 252FC253VV | 252FC2541L | 252FC253BP
# *************************************************************************
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Database Setup ---
Base = declarative_base()
engine = create_engine('sqlite:///db/our.db')
Session = sessionmaker(bind=engine)
session = Session()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

Base.metadata.create_all(engine)

# --- Seed Data (Initial Setup) ---
def seed_data():
    if session.query(Product).count() < 16:
        session.query(Product).delete()
        initial_data = [
            ("Espresso", "Beverages", 3.5, 34), ("Latte", "Beverages", 4.5, 38),
            ("Cappuccino", "Beverages", 4.75, 30), ("Americano", "Beverages", 3.0, 34),
            ("Mocha", "Beverages", 5.25, 2), ("Croissant", "Pastries", 2.25, 20),
            ("Blueberry Muffin", "Pastries", 3.0, 14), ("Chocolate Chip Cookie", "Pastries", 1.75, 45),
            ("Danish", "Pastries", 2.5, 22), ("Turkey Club", "Sandwiches", 7.5, 12),
            ("BLT", "Sandwiches", 6.75, 18), ("Veggie Wrap", "Sandwiches", 6.25, 25),
            ("Potato Chips", "Snacks", 1.5, 38), ("Granola Bar", "Snacks", 2.0, 42),
            ("Oranges", "Fruits", 1.2, 50), ("Apple", "Fruits", 1.5, 60)
        ]
        for name, cat, price, qty in initial_data:
            session.add(Product(name=name, category=cat, price=price, stock_quantity=qty))
        session.commit()

# --- Main System ---
def start_restock_system():
    # seed_data()
    cart = []
    
    print("\n" + "="*55)
    print("   SECURE INVENTORY MANAGER - [VERIFIED PRICING]")
    print("="*55)

    while True:
        categories = [r.category for r in session.query(Product.category).distinct().all()]
        print("\n[MENU] Categories:")
        for i in range(len(categories)):
            print(f"{i+1}. {categories[i]}")
        
        add_item_idx = len(categories)+1
        del_idx = len(categories)+2
        print(f"{add_item_idx}. [ADD NEW ITEM / CATEGORY]")
        print(f"{del_idx}. [DELETE AN ITEM]")
        print("Q. [COMMIT & EXIT]")
        
        choice = input("\nAction: ").lower()
        if choice == 'q': break

        try:
            val = int(choice)

            # --- logic: ADD NEW ITEM with PRICE VALIDATION ---
            if val == add_item_idx:
                print("\n--- NEW PRODUCT REGISTRATION ---")
                for i in range(len(categories)): print(f"{i+1}. {categories[i]}")
                
                new_cat_idx = len(categories) + 1
                print(f"{new_cat_idx}. [NEW CATEGORY]")
                
                cat_c = int(input("Select Category: "))
                final_cat = input("Category Name: ") if cat_c == new_cat_idx else categories[cat_c - 1]
                
                name = input("Item Name: ")

                # --- START PRICE VALIDATION LOOP ---
                while True:
                    p_input = float(input(f"Enter Price for {name}: "))
                    if p_input < 0:
                        print("[!] INVALID PRICE: Price cannot be negative. Please re-enter.")
                    else:
                        price = p_input
                        break
                # --- END PRICE VALIDATION LOOP ---
                
                session.add(Product(name=name, category=final_cat, price=price, stock_quantity=0))
                session.commit()
                print(f"[SUCCESS] {name} added at ${price:.2f}")
                continue

            if val == del_idx:
                print("\n--- DELETE MODE ---")
                for i in range(len(categories)):
                    print(f"{i+1}. {categories[i]}")
                
                cat_c = int(input("Select Category to delete from: ")) - 1
                sel_cat = categories[cat_c]
                
                items = session.query(Product).filter(Product.category == sel_cat).all()
                print(f"\nItems in {sel_cat}:")
                for i in range(len(items)):
                    print(f"{i+1}. {items[i].name}")
                
                item_c = int(input("Select item number to PERMANENTLY DELETE: ")) - 1
                to_delete = items[item_c]
                
                # 二次确认
                confirm = input(f"Are you SURE you want to delete '{to_delete.name}'? (yes/no): ")
                if confirm.lower() == 'yes':
                    session.delete(to_delete)
                    session.commit()
                    print(f"[DELETED] {to_delete.name} has been removed from database.")
                else:
                    print("[CANCELLED] Deletion aborted.")
                continue


            # --- logic: RESTOCK EXISTING ---
            selected_cat = categories[val - 1]
            items = session.query(Product).filter(Product.category == selected_cat).all()
            for i in range(len(items)):
                print(f"{i+1}. {items[i].name:20} | ${items[i].price:<5.2f} | Stock: {items[i].stock_quantity}")

            it_idx = int(input("\nSelect Item: ")) - 1
            qty = int(input(f"Restock Quantity for {items[it_idx].name}: "))
            if qty > 0:
                cart.append((items[it_idx], qty))
                print(f"Added to cart: {items[it_idx].name} x{qty}")

        except (ValueError, IndexError):
            print("\n[ERROR] Invalid input. Please check numbers.")

    # Final Checkout
    if cart:
        print("\n" + "="*55)
        grand_total = 0
        for p, q in cart:
            sub = p.price * q
            grand_total += sub
            print(f"{p.name:22} | x{q:<4} | Sub: ${sub:>8.2f}")
        
        print("-" * 55)
        print(f"GRAND TOTAL: ${grand_total:>41.2f}")
        
        if input("\nConfirm Addition? (y/n): ").lower() == 'y':
            for p, q in cart: p.stock_quantity += q
            session.commit()
            print("[SUCCESS] Inventory Updated.")

if __name__ == "__main__":
    start_restock_system()