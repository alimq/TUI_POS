# *************************************************************************
# Course: CSP1114 PROBLEM SOLVING AND PROGRAM DESIGN
# Lecture / Lab Section: TC1L / TL1L
# Trimester: 2530
# Group Name (from eBwise): TL1L-03
# Names: Imanmalik Alim | Wong Winson | Yong Zi Jing
# IDs: MEMBER_ID_1 | MEMBER_ID_2 | 252FC253BP
# *************************************************************************
from classes import *
from cashier import cashier
from admin import admin
from register import clear_screen
from splash import bootup
import time

def hash(p):
    return p

h = {
    'cashier': 'hash123',
    'admin': 'hash123',
}

def load(u):
    print(u, 'loaded!')

while True:
    first_boot = True
    while True:
        user = input("Input the user: ")
        if user == 'cashier':
        # if user == 'cashier' or user == 'admin':
            password = input("Input the password: ")
            if hash(password) == h['cashier']:
                # load(user)
                clear_screen()
                if first_boot:
                    bootup()
                first_boot = False
                cashier()
                clear_screen()
                continue
            else:
                print("Incorrect password. Try again")
                clear_screen()
        elif user == 'admin':
            password = input("Input the password: ")
            if hash(password) == h['admin']:
                clear_screen()
                if first_boot:
                    bootup()
                first_boot = False
                admin()
                clear_screen()
                time.sleep(0.5)
                continue
            else:
                print("Incorrect password. Try again")
                time.sleep(0.5)
                clear_screen()

        else:
            print("User does not exist. Try again")
            time.sleep(0.5)
            clear_screen()