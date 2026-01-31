from classes import session, Product, Order, OrderItem

class ShoppingCart:
    """Manages items in the shopping cart before order finalization."""
    
    def __init__(self):
        self.items = []  # List of cart items
    
    def add_item(self, product, quantity):
        """
        Add a product to the cart with quantity validation.
        
        Args:
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
        for item in self.items:
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
        self.items.append(cart_item)
        print(f"Added {quantity}x '{product.name}' to cart (${cart_item['subtotal']:.2f})")
        return True
    
    def remove_item(self, index):
        """Remove item from cart by index."""
        if 0 <= index < len(self.items):
            removed = self.items.pop(index)
            print(f"Removed '{removed['product'].name}' from cart")
            return True
        return False
    
    def get_total(self):
        """Calculate total cart value."""
        return sum(item['subtotal'] for item in self.items)
    
    def is_empty(self):
        """Check if cart is empty."""
        return len(self.items) == 0
    
    def display(self):
        """Display cart contents."""
        if self.is_empty():
            print("\n📦 Cart is empty.\n")
            return
        
        print("\n" + "="*50)
        print("SHOPPING CART")
        print("="*50)
        
        for i, item in enumerate(self.items, 1):
            product = item['product']
            print(f"{i}. {product.name}")
            print(f"   Quantity: {item['quantity']} @ ${product.price:.2f} each")
            print(f"   Subtotal: ${item['subtotal']:.2f}")
            print("-" * 50)
        
        print(f"TOTAL: ${self.get_total():.2f}")
        print("="*50 + "\n")
    
    def finalize_order(self):
        """
        Create Order and OrderItem records in database.
        
        Returns:
            Order object if successful, None otherwise
        """
        if self.is_empty():
            print("Cannot finalize empty cart.")
            return None
        
        # Create Order record
        order = Order(total=self.get_total())
        session.add(order)
        session.flush()  # Get the order.id without committing yet
        
        # Create OrderItem records
        for item in self.items:
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


class ProductCatalog:
    """Handles product database queries."""
    
    @staticmethod
    def get_categories():
        """Get list of unique product categories."""
        categories = session.query(Product.category).distinct().filter(
            Product.category.isnot(None),
            Product.stock_quantity > 0
        ).all()
        return [cat[0] for cat in categories if cat[0]]
    
    @staticmethod
    def get_products_by_category(category):
        """Get all products in a specific category."""
        return session.query(Product).filter(
            Product.category == category,
            Product.stock_quantity > 0
        ).all()
    
    @staticmethod
    def get_all_products():
        """Get all products with stock."""
        return session.query(Product).filter(Product.stock_quantity > 0).all()


# Usage Example:
def example_usage():
    """Example of how to use these classes."""
    
    # Create a cart
    cart = ShoppingCart()
    
    # Get a product from database
    product = session.query(Product).filter_by(name="Coffee").first()
    
    if product:
        # Add to cart
        cart.add_item(product, 2)
        
        # Display cart
        cart.display()
        
        # Finalize order
        order = cart.finalize_order()
        
        if order:
            print(f"Order total: ${order.total:.2f}")