import pandas as pd
from sqlalchemy import func
from Oden import Product, InventoryBatch, session

# Metadata mapping for pieces per stick
PRODUCT_METADATA = {
    'Cheese tofu': 2,
    'Fish ball': 2,
    'Lobster ball': 2,
    'Fish cake': 2,
    'Hotdog': 3
}

def populate_stock():
    df = pd.read_csv('Oden/Cost.csv') 
    
    # 1. Convert to datetime objects to allow chronological sorting
    df['Date_Obj'] = pd.to_datetime(df['Date'], dayfirst=True)
    
    # 2. Extract unique dates and sort from smallest to largest
    sorted_date_objs = sorted(df['Date_Obj'].unique())
    
    print("\nAvailable Purchase Dates:")
    for i, date_obj in enumerate(sorted_date_objs, 1):
        # Format back to DD/MM/YYYY for clear display
        print(f"{i}. {date_obj.strftime('%d/%m/%Y')}")
    
    try:
        choice = int(input("\nSelect date index to process: ")) - 1
        if choice < 0: raise IndexError
        target_date_obj = sorted_date_objs[choice]
        target_date_str = target_date_obj.strftime('%d/%m/%Y')
    except (ValueError, IndexError):
        return print("Invalid selection.")

    # 3. Reset logic: Clear batches and stock counts to prevent duplicates
    session.query(InventoryBatch).delete()
    for p in session.query(Product).all():
        p.stock_quantity = 0
    session.commit()

    # 4. Filter all purchases up to the chosen date
    purchases = df[df['Date_Obj'] <= target_date_obj]
    
    records_added = 0
    for _, row in purchases.iterrows():
        item_name = str(row['Item']).strip()
        if item_name not in PRODUCT_METADATA:
            continue
            
        sell_units = PRODUCT_METADATA[item_name]
        
        # Case-insensitive query to find or create the product
        product = session.query(Product).filter(
            func.lower(Product.name) == func.lower(item_name)
        ).first()

        if not product:
            product = Product(
                name=item_name,
                category="Food",
                price=1.50,
                sell_units=sell_units,
                stock_quantity=0
            )
            session.add(product)
            session.flush() 
        
        qty_packets = int(row['Quantity'])
        product.stock_quantity += qty_packets
        
        for _ in range(qty_packets):
            batch = InventoryBatch(
                product_id=product.id,
                vendor=row['Vendor'],
                batch_cost=row['Unit Price'],
                units=row['Granular'],
                is_completed=False
            )
            session.add(batch)
            records_added += 1
            
    session.commit()
    print(f"Success! {records_added} packets added to the FIFO queue up to {target_date_str}.")

if __name__ == "__main__":
    populate_stock()