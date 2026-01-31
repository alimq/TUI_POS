# *************************************************************************
# Course: CSP1114 PROBLEM SOLVING AND PROGRAM DESIGN
# Lecture / Lab Section: TC1L / TL1L
# Trimester: 2530
# Group Name (from eBwise): TL1L-03
# Names: Alim Imanmalik | Wong Winson | Yong Zi Jing
# IDs: 252FC253VV | MEMBER_ID_2 | 252FC253BP
# *************************************************************************

from classes import session, Product, Order, OrderItem
from sqlalchemy import select
import os

# 0. system level function
def clear_screen():
    '''
    This clears the screen entirely without leaving a trace, will be disabled for debugging purposes
    '''
    os.system('cls' if os.name == 'nt' else 'clear')
    #pass

def getch():
    import sys
    print()
    print("Please press any key to continue...")
    if sys.platform == 'win32':
        import msvcrt
        return msvcrt.getch().decode('utf-8')
    else:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# 1. Show all categories and get category
def get_categories():
    """
    Returns all the categories
    Selects the category column from the Product table that are distinct and place them in a list
    """
    categories = session.scalars(select(Product.category).distinct().filter(Product.category.isnot(None))).all()
    return categories

# 2. Obtain user input for category 
def select_category(categories):
    """
    1. Returns: (category, action). Action can be either 'cancel' (category selection), 'cart' (view cart and finalise payment) or 'proceed' (to item selection). 
    
    3. 
    """
    #start enumerating with index 1 instead of 0
    clear_screen()
    print("CASHIER MAIN MENU")
    print('='*60)
    print()
    print("Categories") 
    for i, cat in enumerate(categories, 1):
        print(f'{i}. {cat}')
    print()
    print('(Q) Cancel.')
    print('(J) Go to payment.')
    print('(M) Modify cart.')
    while True:
        choice = input(f'Select category: ').upper()
        if choice == 'Q':
            return None, 'cancel'
        elif choice == 'J':
            return None, 'payment'
        elif choice == 'M':
            return None, 'modify'
        try:
            category_no = int(choice)
            if category_no >= 1 and category_no <= len(categories):
                break
            print(f'Input can be from 1 to {len(categories)} only')
        except ValueError:
            print(f'Invalid input. Please enter a number ranging from 1 to {len(categories)} only.')
    return categories[category_no - 1], 'proceed'

# 3. Show available items of a particular category
def get_products(category):
    """Returns all the products for a certain category if and only they are still in stock"""
    products = [product.name for product in session.query(Product).distinct().filter(
        Product.category == category,
        Product.stock_quantity > 0
        ).all()]
    return products

#4. Select item from a list of available items  
def select_product(products):
    """
    1. Returns (product, action) 
    Action can be either 'cancel' (return to main menu), 'back' category selection, or 'proceed' (to qty input.)"""
    print()
    clear_screen()
    print('='*60)
    print('Items')
    for i, product in enumerate(products, 1):
        print(f'{i}. {product}')
    
    print()
    print('(B) Back to categories.')
    # print('H. Return to main menu.')
    print('(Q) Cancel.')
    print()
    while True:
        choice = input(f'Select product: ')

        if choice == 'B':
            return None, 'back'
        # elif choice == 'H':
        #     return None, 'home'
        elif choice == 'Q':
            return None, 'cancel'
        try:
            product_no = int(choice)
            if product_no >= 1 and product_no <= len(products):
                break
            print(f'Input can be from 1 to {len(products)} only.')
        except ValueError:
            print(f'Invalid input. Please enter a number ranging from 1 to {len(products)} only.')
    product = products[product_no - 1]
    return product, 'proceed'

#5. Provide desired quantity of a certain item
def select_quantity(product):
    """Returns (quantity, action) action can be either 'cancel' (return to main menu), 'back' to product selection, or proceed to cart"""
    stock = session.query(Product.stock_quantity).distinct().filter(Product.name == product).scalar()
    price = session.query(Product.price).distinct().filter(Product.name == product).scalar()
    print()
    print('-'*60)
    print(f'{product} RM {price} Available stock: {stock}')
    print()
    print('(B) Back to product selection.')
    print('(H) Return to main menu.')
    print('(Q) Cancel.')
    print()
    while True:
        choice = input('Please enter desired qty: ').upper()
        if choice == 'B':
            return None, 'back'
        elif choice == 'H':
            return None, 'home'
        elif choice == 'Q':
            return None, 'cancel'
        try:
            quantity = int(choice)
            if quantity >= 1 and quantity <= stock:
                break
            print(f'Input can be from 1 to {stock} only') 
        except ValueError:
            print(f'Invalid input. Please enter a number ranging from 1 to {stock}')
    return quantity, 'proceed'
    
#6. add selected item to cart
def addToCart(product, quantity, cart):
    productObj = session.query(Product).filter(Product.name == product).first()
    cart_item = {
        'product': productObj,
        'quantity': quantity,
        'subtotal': (productObj.price)*quantity
    }
    cart.append(cart_item)
    print('-'*60)
    print()
    print(f'Added {quantity} x {productObj.name} to cart.')

def modifyCart(cart):
    displayCart(cart)
    while True:
        try:
            idx = int(input("Enter the index of the item you wish to modify: "))
            if idx <= (len(cart)-1):
                break
            else:
                print(f"Please enter between 0 to {len(cart) - 1} only ")
        except:
            print("Invalid input")

    item = cart[idx]['product'].name
    price = cart[idx]['product'].price
    qty = cart[idx]['quantity']
    
    print(f'You selected {item}. ')
    print(f'Initial quantity: {qty}')
    stock = session.query(Product.stock_quantity).distinct().filter(Product.name == item).scalar()
    
    while True:
        try:
            newQty = int(input(f"Please enter new quantity.\n  {stock} available in stock: "))
            if newQty >= 1 and newQty <= stock:
                cart[idx]['quantity'] = newQty
                cart[idx]['subtotal'] = newQty*price
                break
            elif newQty == 0:
                print("Are you sure you wish to remove this item from cart?") 
                confirm = input("(Y) Yes | (N) No").upper().strip()
                if confirm == 'Y':
                    cart.pop(idx)
                    break
                elif confirm == 'N':
                    break

        except ValueError:
            print("Invalid input. Try again.")
            continue

#7. Display the cart
def displayCart(cart, payment=False):
    print()
    clear_screen()
    print('='*60)
    print()
    print('Shopping Cart')
    print()
    if not cart:
        print("Cart is empty")
        return None
    print(f'{'#':<4} {'Item':<20} {'Qty':^5} {'Price':>12} {'Subtotal':>12}')
    print('-'*60)
    for i, item in enumerate(cart):
        name = item['product'].name
        qty = item['quantity']
        price = item['product'].price
        subtotal = item['subtotal']
        price_str = f'RM   {price:.2f}'
        subtotal_str = f'RM   {subtotal:.2f}'
        print(f'{i:<4} {name:<20} {qty:^5} {price_str:>12}  {subtotal_str:>12}')
    
    print()
    if payment:
        total = sum(item['subtotal'] for item in cart)
        print('_'*60)
        print()
        print(f"{'TOTAL'} {total:>52.2f}")



#8. finalise the cart
def checkoutCart(cart):

    displayCart(cart, True)
    total = float(sum(item['subtotal'] for item in cart))
    print()
    print("Payment method.")
    while True:
        try:
            method = input("(1) Cash | (2) E-wallet: ")
            if method == '1' or method == '2':
                break
        except ValueError:
            print("Please enter either 1 or 2 only")
            continue
    if method == '1':
        while True:
            try:
                print(f'\n{'Total Due':20}: RM {total:<8.2f}')
                print()
                cash = float(input(f'{'>> Enter payment':20}: RM '))
                print()
                
                if cash >= total:
                    change = cash - total
                    clear_screen()
                    print('='*60)
                    print('Summary')
                    print()
                    print(f'{'Cash Paid':20}: RM {cash:>8.2f}')
                    print(f'{'Change':20}: RM {change:>8.2f}')
                    break
                else:
                    print(f"Insufficient payment. Need RM {(total - cash):.2f} more.")
            except ValueError:
                print("Invalid amount. Please enter a float or integer only.")

    elif method == '2':
        print("Confirm transaction only when payment is received")
        confirm = input("Payment confirmed? (Y/N)").upper().strip()
        while True:
            try:
                if confirm == 'Y':
                    print("Payment successful")
                    break
                elif confirm == 'N':
                    print("Payment has been cancelled!")
                    return None
            except ValueError:
                    print("Please enter either Y or N only.")
                    continue

    order = Order(total=total)
    session.add(order)
    session.flush()

    for item in cart:
        order_item = OrderItem(
            order_id = order.id,
            product_id = item['product'].id,
            quantity = item['quantity'],
            subtotal = item['subtotal']
        )
        session.add(order_item)

        item['product'].stock_quantity -= item['quantity']
    session.commit()
    print(f'Order #{order.id} created.')
    return order

def run_register(): 
    cart = []
    state = 'category'  # Track current step

    while True:
        if state == 'category':
            categories = get_categories()
            category, action = select_category(categories)
            
            if action == 'cancel':
                if len(cart) != 0:
                    print(f'You have {len(cart)} in cart. Are you sure you want to cancel transaction.')
                    warn = input(f'(Y) Yes. Cancel order. | (N) No. Return to menu. ').upper().strip()
                    if warn == 'Y':
                        print('Ordering cancelled.')
                        return
                    elif warn == 'N':
                        continue
                    # elif warn == 'N':
                    #     print('Proceeding to modify cart.') # yet to be implemented. currently returns to the first ordering menu
                    #     #action = 'category'
                    #     action = 'modify'
                    # else:
                    #     print('Please enter either Y or N only.')
                else:
                    print("Exit program.")
                    return
            elif action == 'back' or action == 'home':
                # Already at first step, maybe exit or show menu
                print("Already at first step")
                continue
            elif action == 'proceed':
                state = 'product'
            elif action == 'payment':
                if len(cart) != 0:
                    checkoutCart(cart)
                else:
                    print("You have nothing in cart to checkout yet.")
            
            elif action == 'modify':
                modifyCart(cart)
        
        elif state == 'product':
            products = get_products(category)
            product, action = select_product(products)
            
            if action == 'cancel':
                print("Ordering cancelled")
                return
            elif action == 'back' or action == 'home':
                state = 'category'  # Go back to category selection
                continue
            elif action == 'proceed':
                state = 'quantity'
        
        elif state == 'quantity':
            quantity, action = select_quantity(product)
            
            if action == 'cancel':
                return
            elif action == 'back':
                state = 'product'  # Go back to product selection
                continue
            elif action == 'home':
                state = 'category'
                continue
            # flow of program to be reviewed, checkout should be reserved for the cart
            elif action == 'proceed':
                addToCart(product, quantity, cart)
                state = 'checkout'
        
        elif state == 'checkout':
            # print("\nCart summary:")
            # display_cart(cart)
            
            choice = input("(Y) Checkout | (A) Add more items: ").upper()
            
            if choice == 'Y':
                checkoutCart(cart)
                return
            elif choice == 'A':
                state = 'category'  # Start over to add more

# WONG WINSON
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

#

if __name__ == '__main__':
    run_register()
    