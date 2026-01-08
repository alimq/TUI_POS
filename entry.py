# *************************************************************************
# Course: CSP1114 PROBLEM SOLVING AND PROGRAM DESIGN
# Lecture / Lab Section: TC1L / TL1L
# Trimester: 2530
# Group Name (from eBwise): TL1L-03
# Names: Imanmalik Alim | Wong Winson | Yong Zi Jing
# IDs: MEMBER_ID_1 | MEMBER_ID_2 | 252FC253BP
# *************************************************************************

from register import run_register, clear_screen, restock_inventory
store_balance = 1000 # hardcoded for now, will be based on the remaining balance in bank


while True:
    
    print("TUI_POS")

    print()
    print("1. Cash register")
    print("2. Order fulfillment")
    print("3. Inventory management")
    print("4. Exit")
    print()
    try:
        user = int(input('To: '))
        if user == 1:
            print("Loading the cash register")
            run_register()
            
        elif user == 2:
            print("Yet to be implemented")
            print("To track the elapsed time the moment the customer has completed their order or payment to be eaxct to the moment the (overworked) cashier or the kitchen has completed the food and casheir delivered the item to customer")
            
        elif user == 3:
            print("Loading the inventory management page")
            restock_inventory(store_balance)

        
        elif user == 4:
            print("Goodbye.")
            break

        else:
            print("Please enter 1 to 4 only")
    except ValueError:
        print("Enter only numbers only")