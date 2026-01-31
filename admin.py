# *************************************************************************
# Course: CSP1114 PROBLEM SOLVING AND PROGRAM DESIGN
# Lecture / Lab Section: TC1L / TL1L
# Trimester: 2530
# Group Name (from eBwise): TL1L-03
# Names: Imanmalik Alim | Wong Winson | Yong Zi Jing
# IDs: 252FC253VV | 252FC2541L | 252FC253BP
# *************************************************************************

"""
Admin's main menu and all the associated funcitons accessible
"""

import os
import time
store_balance = 1000 # hardcoded for now, will be based on the remaining balance in bank
from timer import confirm
from admin_restock import start_restock_system
from register import clear_screen, getch

def admin():
    while True:
        
        try:
            print("Admin's menu")
            print()
            print("1. Inventory management")
            # print("2. Analysis")
            print("3. Exit")
            print()
            user = int(input('To: '))
            if user == 1:
                print("Loading the inventory management page")
                getch()
                start_restock_system()
                
            elif user == 2:
                # Analysis part
                pass

            elif user == 3:
                print("Goodbye.")
                break

            else:
                print("Please enter 1 to 3 only")
        except ValueError:
            print("Enter only numbers only")

if __name__=="__main__":
    admin()
