from classes import session, Product

def restock_inventory(current_balance):

    print("\n=== Automated Restock System ===")

    out_of_stock_items = session.query(Product).filter(Product.stock_quantity <= 0).all()

    if not out_of_stock_items:

        print(" No items are currently out of stock.")

        return current_balance

    total_expenditure = 0

    for item in out_of_stock_items:

        print(f"\n[Stock Alert] Product: {item.name}")

        print(f" Original Price: ${item.price}")

        print(f" Current Balance: ${current_balance - total_expenditure}")

        try:

            buy_quantity = int(input(f"Enter quantity to purchase for '{item.name}' (0 to skip): "))

            if buy_quantity > 0:

                cost = buy_quantity * item.price

                if cost <= (current_balance - total_expenditure):

                    total_expenditure += cost

                    item.stock_quantity += buy_quantity

                    print(f" Ordered {buy_quantity} units. Cost: ${cost}")

                else:

                    print("Insufficient funds to complete this purchase!")

        except ValueError:

            print("Invalid input. Please enter a whole number.")





    if total_expenditure > 0:

        session.commit()

        current_balance -= total_expenditure

        print(f"\n Restock Complete! Total Spent: ${total_expenditure}")

        print(f" Final Balance: ${current_balance}")

    return current_balance

