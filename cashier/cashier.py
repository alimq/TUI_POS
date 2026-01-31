# *************************************************************************
# Course: CSP1114 PROBLEM SOLVING AND PROGRAM DESIGN
# Lecture / Lab Section: TC1L / TL1L
# Trimester: 2530
# Group Name (from eBwise): TL1L-03
# Names: Imanmalik Alim | Wong Winson | Yong Zi Jing
# IDs: 252FC253VV | 252FC2541L | 252FC253BP
# *************************************************************************

"""
Cashier's main menu and all the functions that are accessible to the cashier.
"""

import os
import time
from tools.register import run_register, clear_screen, restock_inventory, getch
store_balance = 1000 # hardcoded for now, will be based on the remaining balance in bank
from tools.timer import confirm

def cashier():
    while True:
        
        try:
            print("Cashier's menu")
            print()
            print("1. Cash register")
            print("2. Order fulfillment")
            # print("3. Inventory management")
            print("3. Exit")
            print()
            user = int(input('To: '))
            if user == 1:
                print("Loading the cash register")
                run_register()
                getch()
                clear_screen()
                
            elif user == 2:
                # print("Yet to be implemented")
                # print("To track the elapsed time the moment the customer has completed their order or payment to be eaxct to the moment the (overworked) cashier or the kitchen has completed the food and casheir delivered the item to customer")
                confirm()

                
            # elif user == 3:
            #     print("Loading the inventory management page")
            #     start_restock_system()

            elif user == 3:
                print("Goodbye.")
                break

            else:
                print("Please enter 1 to 3 only")
        except ValueError:
            print("Enter only numbers only")

if __name__=="__main__":
    cashier()
