# *************************************************************************
# Course: CSP1114 PROBLEM SOLVING AND PROGRAM DESIGN
# Lecture / Lab Section: TC1L / TL1L
# Trimester: 2530
# Group Name (from eBwise): TL1L-03
# Names: Imanmalik Alim | Wong Winson | Yong Zi Jing
# IDs: MEMBER_ID_1 | MEMBER_ID_2 | 252FC253BP
# *************************************************************************

import time
import sys
import threading
import PIL.Image
import msvcrt
import shutil
from register import clear_screen

def bootup():
    screen = r"""
.___________. __    __   __  .______     ______        _______.
|           ||  |  |  | |  | |   _  \   /  __  \      /       |
`---|  |----`|  |  |  | |  | |  |_)  | |  |  |  |    |   (----`
    |  |     |  |  |  | |  | |   ___/  |  |  |  |     \   \    
    |  |     |  `--'  | |  | |  |      |  `--'  | .----)   |   
    |__|      \______/  |__| | _|       \______/  |_______/    

            LESS FIDDLING, SHARPER INTUITION
                                                               
    """
    skip = threading.Event()

    def display_animation():
        for char in screen:
            if skip.is_set():
                clear_screen()
                break

            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.01)

    def wait_skip():
        msvcrt.getch()
        skip.set()

    display_thread = threading.Thread(target=display_animation)
    input_thread = threading.Thread(target=wait_skip, daemon=True)

    display_thread.start()
    input_thread.start()

    display_thread.join()

    time.sleep(1)
    clear_screen()




if __name__ == "__main__":
    bootup()
        
    


