from classes import session, Product, Order, OrderItem

# ============ CART MANAGEMENT FUNCTIONS ============

def create_cart():
    """Create a new empty cart."""
    return []


def add_item_to_cart(cart, product, quantity):
    """
    Add a product to the cart with quantity validation.
    
    Args:
        cart: List of cart items
        product: Product object from database
        quantity: Integer quantity to add
        
    Returns:
        bool: True if added successfully, False otherwise
    """
    # Validate stock availability
    if product.stock_quantity <= 0:
        print(f"'{product.name}' is out of stock.")
        return False
    
    if quantity > product.stock_quantity:
        print(f"Insufficient stock. Only {product.stock_quantity} available.")
        
        # Offer to add available quantity
        choice = input(f"Add {product.stock_quantity} instead? (Y/N): ").upper()
        if choice == 'Y':
            quantity = product.stock_quantity
        else:
            return False
    
    # Check if product already in cart
    for item in cart:
        if item['product'].id == product.id:
            # Update quantity if already exists
            new_quantity = item['quantity'] + quantity
            if new_quantity > product.stock_quantity:
                print(f"Cannot add {quantity} more. Total would exceed stock.")
                return False
            
            item['quantity'] = new_quantity
            item['subtotal'] = product.price * new_quantity
            print(f"Updated '{product.name}' quantity to {new_quantity}")
            return True
    
    # Add new item to cart
    cart_item = {
        'product': product,
        'quantity': quantity,
        'subtotal': product.price * quantity
    }
    cart.append(cart_item)
    print(f"Added {quantity}x '{product.name}' to cart (${cart_item['subtotal']:.2f})")
    return True


def remove_item_from_cart(cart, index):
    """Remove item from cart by index."""
    if 0 <= index < len(cart):
        removed = cart.pop(index)
        print(f"Removed '{removed['product'].name}' from cart")
        return True
    return False


def calculate_cart_total(cart):
    """Calculate total cart value."""
    return sum(item['subtotal'] for item in cart)


def is_cart_empty(cart):
    """Check if cart is empty."""
    return len(cart) == 0


def display_cart(cart):
    """Display cart contents."""
    if is_cart_empty(cart):
        print("\n📦 Cart is empty.\n")
        return
    
    print("\n" + "="*50)
    print("SHOPPING CART")
    print("="*50)
    
    for i, item in enumerate(cart, 1):
        product = item['product']
        print(f"{i}. {product.name}")
        print(f"   Quantity: {item['quantity']} @ ${product.price:.2f} each")
        print(f"   Subtotal: ${item['subtotal']:.2f}")
        print("-" * 50)
    
    print(f"TOTAL: ${calculate_cart_total(cart):.2f}")
    print("="*50 + "\n")


def finalize_order(cart):
    """
    Create Order and OrderItem records in database from cart.
    
    Args:
        cart: List of cart items
        
    Returns:
        Order object if successful, None otherwise
    """
    if is_cart_empty(cart):
        print("Cannot finalize empty cart.")
        return None
    
    # Create Order record
    order = Order(total=calculate_cart_total(cart))
    session.add(order)
    session.flush()  # Get the order.id without committing yet
    
    # Create OrderItem records
    for item in cart:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item['product'].id,
            quantity=item['quantity'],
            subtotal=item['subtotal']
        )
        session.add(order_item)
        
        # Update product stock
        item['product'].stock_quantity -= item['quantity']
    
    # Commit all changes
    session.commit()
    print(f"✓ Order #{order.id} created successfully!")
    
    return order


# ============ PRODUCT CATALOG FUNCTIONS ============

def get_categories():
    """Get list of unique product categories."""
    categories = session.query(Product.category).distinct().filter(
        Product.category.isnot(None),
        Product.stock_quantity > 0
    ).all()
    return [cat[0] for cat in categories if cat[0]]


def get_products_by_category(category):
    """Get all products in a specific category."""
    return session.query(Product).filter(
        Product.category == category,
        Product.stock_quantity > 0
    ).all()


def get_all_products():
    """Get all products with stock."""
    return session.query(Product).filter(Product.stock_quantity > 0).all()


# ============ UI HELPER FUNCTIONS ============

def select_from_list(items, item_type="item"):
    """
    Display numbered list and return selected item.
    
    Args:
        items: List of Product objects or strings
        item_type: Description of what's being selected
        
    Returns:
        Selected item or None
    """
    if not items:
        print(f"No {item_type}s available.")
        return None
    
    print(f"\n--- Select {item_type.title()} ---")
    for i, item in enumerate(items, 1):
        # Display differently based on item type
        if isinstance(item, Product):
            print(f"{i}. {item.name} - ${item.price:.2f} (Stock: {item.stock_quantity})")
        else:
            print(f"{i}. {item}")
    
    while True:
        try:
            choice = int(input(f"\nSelect {item_type} (1-{len(items)}): "))
            if 1 <= choice <= len(items):
                return items[choice - 1]
            print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a number.")


def get_quantity_input():
    """Get and validate quantity input from user."""
    while True:
        try:
            quantity = int(input("Enter quantity: "))
            if quantity <= 0:
                print("Quantity must be positive.")
                continue
            return quantity
        except ValueError:
            print("Please enter a valid number.")


# ============ USAGE EXAMPLE ============

def example_usage():
    """Example of how to use these functions."""
    
    # Create a cart
    cart = create_cart()
    
    # Get a product from database
    product = session.query(Product).filter_by(name="Coffee").first()
    
    if product:
        # Add to cart
        add_item_to_cart(cart, product, 2)
        
        # Display cart
        display_cart(cart)
        
        # Finalize order
        order = finalize_order(cart)
        
        if order:
            print(f"Order total: ${order.total:.2f}")


# ============ MAIN FLOW (Replacing your current while loop) ============

def run_cashier_register():
    """Main cashier register flow."""
    cart = create_cart()
    
    while True:
        # Select category
        categories = get_categories()
        if not categories:
            print("No products available.")
            break
            
        category = select_from_list(categories, "category")
        if not category:
            continue
        
        # Select product from category
        products = get_products_by_category(category)
        product = select_from_list(products, "product")
        if not product:
            continue
        
        # Get quantity
        quantity = get_quantity_input()
        
        # Add to cart
        add_item_to_cart(cart, product, quantity)
        
        # Display current cart
        display_cart(cart)
        
        # Ask to continue or checkout
        choice = input("\n(Y) Checkout | (N) Add more items | (Q) Quit: ").upper()
        
        if choice == 'Y':
            if not is_cart_empty(cart):
                order = finalize_order(cart)
                if order:
                    print(f"\n✓ Order completed! Total: ${order.total:.2f}\n")
                break
            else:
                print("Cart is empty. Please add items first.")
        elif choice == 'Q':
            print("Session cancelled.")
            break
        # If 'N' or anything else, loop continues


if __name__ == "__main__":
    run_cashier_register()