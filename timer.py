# *************************************************************************
# Course: CSP1114 PROBLEM SOLVING AND PROGRAM DESIGN
# Lecture / Lab Section: TC1L / TL1L
# Trimester: 2530
# Group Name (from eBwise): TL1L-03
# Names: Alim Imanmalik | Wong Winson | Yong Zi Jing
# IDs: 252FC253VV | MEMBER_ID_2 | 252FC253BP
# *************************************************************************

from register import clear_screen, getch
import threading
import time
import sys
import msvcrt
import os
from classes import session, Product, Order, OrderItem
from sqlalchemy import select
from datetime import datetime, timezone

# order = {}

id = 0

# ground truth to compare against
start = time.time()

# def add_order():
#     global id
#     order[id] = {
#         'timestamp': time.time(),
#         'status': 0
#     }
#     print(f"Order #{id} created.")
#     id += 1

def complete_order():
    # this is meant to be a proof of concept only
    # while True:
    #     # for idx, val in order.items():
    #     #     print(idx, val)
    #     show_all()
    #     try:
    #         id = int(input("Finish order: "))
    #         if id in order:
    #             order[id]['status'] = 1
    #             print(f"Order #{id} completed.")
    #             break
    #         else:
    #             print(f"Invalid order id entered. There are currently {order.keys()} order(s) only.")
    #             continue
    #     except (ValueError, TypeError):
    #         print("Invalid input entered. Please try again.")
    #         continue
    # order[id]['status'] = 1
    pass

def show_all():
    # Get terminal dimensions
    TERMINAL_WIDTH = os.get_terminal_size().columns
    ORDER_WIDTH = 7  # "Order #"
    TIME_WIDTH = 8   # "HH:MM:SS"
    SEPARATOR_WIDTH = 3  # " | "
    ITEMS_WIDTH = TERMINAL_WIDTH - ORDER_WIDTH - TIME_WIDTH - (SEPARATOR_WIDTH * 2)



    # 1. Get all order ids and their timestamps of all pending orders
    pending = session.execute(
        select(Order.id, Order.created_at)
        .filter(Order.completed_at.is_(None))
    ).all()
    orderIds = [order[0] for order in pending]
    timestamps = {order[0]: order[1] for order in pending}
    # alternative approch using ==
    # orderIds = session.scalars(select(Order.id).filter(Order.completed_at == None)).all()

    # 2. Get order_id, product_id AND quantity together from OrderItem
    order_items = session.execute(
        select(OrderItem.order_id ,OrderItem.product_id, OrderItem.quantity)
        .filter(OrderItem.order_id.in_(orderIds))
    ).all()

    order_ids = [item[0] for item in order_items]
    productIds = [item[1] for item in order_items]
    quantities = [item[2] for item in order_items]

    product_map = {
        product.id: product.name 
        for product in session.query(Product).filter(Product.id.in_(set(productIds))).all()
    }

    # 3. Get the names of the product based on the product ids
    product_names = [product_map[id] for id in productIds]


    # 4. Group by order_id 
    orders = {}

    for order_id, qty, prod in zip(order_ids, quantities, product_names):
        if order_id not in orders:
            orders[order_id] = []
        orders[order_id].append(f"{qty}x {prod}")

    # 5. Print headers
    # Print header
    print()
    print(f"{"Order":>{ORDER_WIDTH}} | {"Time":^{TIME_WIDTH}} | {"Items":<{ITEMS_WIDTH}}")
    print("-" * TERMINAL_WIDTH)

    # 6. Calculate the elapsed time, display orders with elapsed time and items with truncation
    for order_id, items in orders.items():
        items_str = ", ".join(items)
        
        # Truncate if too long
        if len(items_str) > ITEMS_WIDTH:
            items_str = items_str[:ITEMS_WIDTH-3] + "..."

        # Calculate elapsed time
        created_at = timestamps[order_id].replace(tzinfo=timezone.utc)
        elapsed = (datetime.now(timezone.utc) - created_at).total_seconds()
        minutes, seconds = divmod(int(elapsed), 60)
        hours, minutes = divmod(minutes, 60)
        display_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        print(f"{order_id:>{ORDER_WIDTH}} | {display_time:^{TIME_WIDTH}} | {items_str}")



def show_all_live():
    stop_event = threading.Event()
    TERMINAL_WIDTH = os.get_terminal_size().columns
    ORDER_WIDTH = 7
    TIME_WIDTH = 8
    SEPARATOR_WIDTH = 3
    ITEMS_WIDTH = TERMINAL_WIDTH - ORDER_WIDTH - TIME_WIDTH - (SEPARATOR_WIDTH * 2)
    
    print(f"{"Order":>{ORDER_WIDTH}} | {"Time":^{TIME_WIDTH}} | {"Items":<{ITEMS_WIDTH}}")
    print("-" * TERMINAL_WIDTH)

    def update_display():
        first_run = True
        PREV_WIDTH = TERMINAL_WIDTH
        items_width = ITEMS_WIDTH
        
        while not stop_event.is_set():
            CURRENT_WIDTH = os.get_terminal_size().columns
            if CURRENT_WIDTH != PREV_WIDTH:
                clear_screen()
                items_width = CURRENT_WIDTH - ORDER_WIDTH - TIME_WIDTH - (SEPARATOR_WIDTH * 2)
                print(f"{"Order":>{ORDER_WIDTH}} | {"Time":^{TIME_WIDTH}} | {"Items":^{items_width}}")
                print("-" * CURRENT_WIDTH)
                PREV_WIDTH = CURRENT_WIDTH
                first_run = True
            
            # Query database for pending orders
            pending = session.execute(
                select(Order.id, Order.created_at)
                .filter(Order.completed_at.is_(None))
            ).all()
            
            if not pending:
                if first_run:
                    print("All orders have been fulfilled.")
                first_run = False
                time.sleep(1)
                continue
            
            orderIds = [order[0] for order in pending]
            timestamps = {order[0]: order[1] for order in pending}
            
            # Get order items
            order_items = session.execute(
                select(OrderItem.order_id, OrderItem.product_id, OrderItem.quantity)
                .filter(OrderItem.order_id.in_(orderIds))
            ).all()
            
            order_ids = [item[0] for item in order_items]
            productIds = [item[1] for item in order_items]
            quantities = [item[2] for item in order_items]
            
            # Get product names
            product_map = {
                product.id: product.name 
                for product in session.query(Product).filter(Product.id.in_(set(productIds))).all()
            }
            product_names = [product_map[pid] for pid in productIds]
            
            # Group by order_id
            orders = {}
            for order_id, qty, prod in zip(order_ids, quantities, product_names):
                if order_id not in orders:
                    orders[order_id] = []
                orders[order_id].append(f"{qty}x {prod}")
            
            # Display orders
            line_num = 3
            for order_id, items in orders.items():
                items_str = ", ".join(items)
                
                # Truncate if too long
                if len(items_str) > items_width:
                    items_str = items_str[:items_width-3] + "..."
                
                # Calculate elapsed time
                created_at = timestamps[order_id].replace(tzinfo=timezone.utc)
                elapsed = (datetime.now(timezone.utc) - created_at).total_seconds()
                minutes, seconds = divmod(int(elapsed), 60)
                hours, minutes = divmod(minutes, 60)
                display_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                
                display_line = f"{order_id:>{ORDER_WIDTH}} | {display_time:^{TIME_WIDTH}} | {items_str}"
                sys.stdout.write(f'\033[{line_num};1H{display_line}')
                sys.stdout.flush()
                line_num += 1
            
            sys.stdout.write(f'\033[{line_num+1};1H\n')
            sys.stdout.flush()

            if first_run:
                message_line = len(orders) + 4
                sys.stdout.write(f'\033[{message_line};1H')
                print("Press any key to return to menu...")

            first_run = False
            time.sleep(1)
    
    display_thread = threading.Thread(target=update_display)
    display_thread.start()
    msvcrt.getch()
    
    stop_event.set()
    display_thread.join()

def confirm():
    stop_event = threading.Event()
    selected_order = None
    input_buffer = ""
    
    def update_display():
        nonlocal selected_order, input_buffer
        first_run = True
        PREV_WIDTH = os.get_terminal_size().columns
        
        while not stop_event.is_set():
            TERMINAL_WIDTH = os.get_terminal_size().columns
            ORDER_WIDTH = 7
            TIME_WIDTH = 8
            SEPARATOR_WIDTH = 3
            items_width = TERMINAL_WIDTH - ORDER_WIDTH - TIME_WIDTH - (SEPARATOR_WIDTH * 2)
            
            if TERMINAL_WIDTH != PREV_WIDTH:
                clear_screen()
                PREV_WIDTH = TERMINAL_WIDTH
                first_run = True
            
            # Query database for pending orders
            pending = session.execute(
                select(Order.id, Order.created_at)
                .filter(Order.completed_at.is_(None))
            ).all()
            
            if not pending:
                if first_run:
                    sys.stdout.write('\033[3;1H')
                    sys.stdout.write("All orders have been fulfilled.")
                    sys.stdout.write('\033[K')
                    sys.stdout.flush()
                first_run = False
                time.sleep(1)
                continue
            
            orderIds = [order[0] for order in pending]
            timestamps = {order[0]: order[1] for order in pending}
            
            # Get order items
            order_items = session.execute(
                select(OrderItem.order_id, OrderItem.product_id, OrderItem.quantity)
                .filter(OrderItem.order_id.in_(orderIds))
            ).all()
            
            order_ids = [item[0] for item in order_items]
            productIds = [item[1] for item in order_items]
            quantities = [item[2] for item in order_items]
            
            product_map = {
                product.id: product.name 
                for product in session.query(Product).filter(Product.id.in_(set(productIds))).all()
            }
            product_names = [product_map[pid] for pid in productIds]
            
            # Group by order_id
            orders = {}
            for order_id, qty, prod in zip(order_ids, quantities, product_names):
                if order_id not in orders:
                    orders[order_id] = []
                orders[order_id].append(f"{qty}x {prod}")
            
            if first_run or selected_order is None:
                # Display header
                sys.stdout.write('\033[1;1H')
                header = f"{"Order":>{ORDER_WIDTH}} | {"Time":^{TIME_WIDTH}} | {"Items":<{items_width}}"
                sys.stdout.write(header)
                sys.stdout.write('\033[K')
                
                sys.stdout.write('\033[2;1H')
                sys.stdout.write("-" * TERMINAL_WIDTH)
                sys.stdout.write('\033[K')
                first_run = False
            
            # Display all orders
            line_num = 3
            for order_id, items in orders.items():
                items_str = ", ".join(items)
                
                if len(items_str) > items_width:
                    items_str = items_str[:items_width-3] + "..."
                
                created_at = timestamps[order_id].replace(tzinfo=timezone.utc)
                elapsed = (datetime.now(timezone.utc) - created_at).total_seconds()
                minutes, seconds = divmod(int(elapsed), 60)
                hours, minutes = divmod(minutes, 60)
                display_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                
                display_line = f"{order_id:>{ORDER_WIDTH}} | {display_time:^{TIME_WIDTH}} | {items_str}"
                sys.stdout.write(f'\033[{line_num};1H{display_line}')
                sys.stdout.write('\033[K')  # Clear to end of line
                line_num += 1
            
            # Clear remaining lines if orders decreased
            for i in range(line_num, line_num + 10):
                sys.stdout.write(f'\033[{i};1H\033[K')
            
            # Show selected order details
            if selected_order is not None and selected_order in orders:
                detail_line = line_num + 2
                sys.stdout.write(f'\033[{detail_line};1H')
                sys.stdout.write("=" * TERMINAL_WIDTH)
                sys.stdout.write('\033[K')
                
                sys.stdout.write(f'\033[{detail_line+1};1H')
                sys.stdout.write(f"Order #{selected_order} Details:")
                sys.stdout.write('\033[K')
                
                sys.stdout.write(f'\033[{detail_line+2};1H')
                sys.stdout.write(f"Items: {', '.join(orders[selected_order])}")
                sys.stdout.write('\033[K')
                
                sys.stdout.write(f'\033[{detail_line+3};1H')
                sys.stdout.write(f"Created: {timestamps[selected_order]}")
                sys.stdout.write('\033[K')
                
                sys.stdout.write(f'\033[{detail_line+4};1H')
                sys.stdout.write("(Y) Mark as complete | (N) Cancel")
                sys.stdout.write('\033[K')
            else:
                # Show prompt
                prompt_line = line_num + 2
                sys.stdout.write(f'\033[{prompt_line};1H')
                prompt_text = f"Enter order # to view details{' (current: ' + input_buffer + ')' if input_buffer else ''} | (Q) Exit"
                sys.stdout.write(prompt_text)
                sys.stdout.write('\033[K')
            
            sys.stdout.flush()
            time.sleep(1)
    
    def handle_input():
        nonlocal selected_order, input_buffer
        
        while not stop_event.is_set():
            if msvcrt.kbhit():
                ch = msvcrt.getch().decode('utf-8', errors='ignore').upper()
                
                if selected_order is None:
                    # Main menu input
                    if ch == 'Q':
                        stop_event.set()
                        break
                    elif ch.isdigit():
                        input_buffer += ch
                    elif ch == '\r':  # Enter key
                        if input_buffer:
                            try:
                                selected_order = int(input_buffer)
                                input_buffer = ""
                            except ValueError:
                                input_buffer = ""
                    elif ch == '\x08':  # Backspace
                        input_buffer = input_buffer[:-1]
                else:
                    # Detail view input
                    if ch == 'Y':
                        # Mark order as complete
                        order_obj = session.query(Order).filter(Order.id == selected_order).first()
                        if order_obj:
                            order_obj.completed_at = datetime.now(timezone.utc)
                            session.commit()
                        selected_order = None
                    elif ch == 'N':
                        selected_order = None
            
            time.sleep(0.1)
    
    # Start threads
    display_thread = threading.Thread(target=update_display)
    input_thread = threading.Thread(target=handle_input)
    
    display_thread.start()
    input_thread.start()
    
    input_thread.join()
    display_thread.join()
    
    clear_screen()

if __name__ == "__main__":
    while True:
        actions = ['Create new order', 'Complete order', 'Show all', 'Exit']
        for idx, action in enumerate(actions):
            print(idx, action)
        action = int(input("Proceed to: "))
        try:
            if action >= 0 and action <= len(actions) - 1:
                clear_screen()
                # if action == 0:
                #     add_order()
                #     time.sleep(1)
                #     clear_screen()
                if action == 0:
                    print("No longer available. This was meant for testing only.")
                    continue
                elif action == 1:
                    complete_order()
                    time.sleep(1)
                    clear_screen()
                elif action == 2:
                    confirm()
                    
                elif action == 3:
                    break
            else:
                print(f"Enter between 0 and {len(actions) - 1} only!")
                continue
        except (ValueError, TypeError):
            print("Invalid input. Please try again.")
            continue
    


### Implementation 2 ###

# results = session.execute(
#     # Start with the Order table
#     select(Order.id, Product.name, OrderItem.quantity)
#     # Join OrderItem to Order
#     .join(OrderItem, Order.id == OrderItem.order_id)
#     # Join Product to OrderItem
#     .join(Product, OrderItem.product_id == Product.id)
#     .filter(Order.completed_at.is_(None))
# ).all()

# # Group items by order_id
# from collections import defaultdict
# orders = defaultdict(list)

# for order_id, product_name, qty in results:
#     orders[order_id].append(f"{qty}x {product_name}")

# # Print each order with all its items on one line
# for order_id, items in orders.items():
#     items_str = ", ".join(items)
#     print(f"Order #{order_id}: {items_str}")