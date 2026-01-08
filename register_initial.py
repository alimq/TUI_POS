from classes import session, Product, Order, OrderItem
from sqlalchemy import select

# 1. Show all categories and get category
def get_categories():
    """Returns all the categories"""
    """Example: """
    """Data type: """
    categories = session.scalars(select(Product.category).distinct().filter(Product.category.isnot(None))).all()
    return categories

# 2. Obtain user input for category 
def select_category(categories):
    """Returns: (category, action) action can be either 'cancel' (return to main menu), 'back' to main menu, or proceed (to next function)"""
    """Action for 'proceed' is determined by a successful function run"""
    #start enumerating with index 1 instead of 0 
    for i, cat in enumerate(categories, 1):
        print(f'{i}. {cat}')
    # print('B. Back to previous.')
    # print('H. Return to main menu.')
    print('Q. Cancel.')
    print('J. Go to cart.')
    while True:
        choice = input(f'Select category: ').upper()
        # if choice == 'B':
        #     return None, 'back'
        # elif choice == 'H':
        #     return None, 'home'
        if choice == 'Q':
            return None, 'cancel'
        elif choice == 'J':
            return None, 'cart'
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
    """Returns all the products for a certain category"""
    """Example: """
    """Data type: """
    products = [product.name for product in session.query(Product).distinct().filter(
        Product.category == category,
        Product.stock_quantity > 0
        ).all()]
    return products

#4. Select item from a list of available items  
def select_product(products):
    """Returns (product, action) action can be either 'cancel' (return to main menu), 'back' category selection, or proceed (to next function)"""
    for i, product in enumerate(products, 1):
        print(f'{i}. {product}')
    print('B. Back to categories.')
    # print('H. Return to main menu.')
    print('Q. Cancel.')
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
    print(f'{product} RM {price} Available stock: {stock}')
    print('B. Back to product selection.')
    print('H. Return to main menu.')
    print('Q. Cancel.')
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
    print(f'Added {quantity} x {productObj.name} to cart.')

#7. finalise the cart
def checkoutCart(cart):
    if not cart:
        print("Cart is empty")
        return None

    total = sum(item['subtotal'] for item in cart)
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

cart = []

# while True:
#     categories = get_categories()
#     category = select_category(categories)
#     products = get_products(category)
#     product = select_product(products)
#     quantity = select_quantity(product)
#     addToCart(product, quantity, cart)
#     choice = input("(Y) Checkout| (N) Add more items: ").upper()

#     if choice == "Y":
#         order = checkoutCart(cart)
#         break

# while True:
#     obtained = input("Please enter a number: ")
#     if obtained == 'Q' or obtained == 'q':
#         print('You chose to terminate this program.')
#         break
    
#     print(f'{int(obtained)} was the number you inputted.')


cart = []
state = 'category'  # Track current step

while True:
    if state == 'category':
        categories = get_categories()
        category, action = select_category(categories)
        
        if action == 'cancel':
            if len(cart) != 0:
                print(f'You have {len(cart)} in cart. Are you sure you want to cancel transaction.')
                warn = input(f'(Y) Yes. Cancel order. | (N) No. Modify cart instead. ').upper()
                if warn == 'Y':
                    print('Ordering cancelled.')
                    break
                elif warn == 'N':
                    print('Proceeding to modify cart.') # yet to be implemented. currently returns to the first ordering menu
                    action = 'category'
                # else:
                #     print('Please enter either Y or N only.')
            else:
                print("Ordering cancelled")
                break
        elif action == 'back' or action == 'home':
            # Already at first step, maybe exit or show menu
            print("Already at first step")
            continue
        elif action == 'proceed':
            state = 'product'
        elif action == 'cart':
            if len(cart) != 0:
                checkoutCart(cart)
            else:
                print("You have nothing in cart to checkout.")
    
    elif state == 'product':
        products = get_products(category)
        product, action = select_product(products)
        
        if action == 'cancel':
            print("Ordering cancelled")
            break
        elif action == 'back' or action == 'home':
            state = 'category'  # Go back to category selection
            continue
        elif action == 'proceed':
            state = 'quantity'
    
    elif state == 'quantity':
        quantity, action = select_quantity(product)
        
        if action == 'cancel':
            break
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
            break
        elif choice == 'A':
            state = 'category'  # Start over to add more
