import pandas as pd
from time import time
import os
sales = pd.read_csv('Oden/sales_expanded02.csv')
cost = pd.read_csv('Oden/cost.csv')
dates = sales['Date'].unique()

# used when need to access multiple columns simultaneously and assigning to an object for daabase write 

# for index, row in df.iterrows():
#     print(row['Subtotal (RM)'])


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def process():
    while True:
        clear_screen()
        oden = {'Cheese tofu': 0, 'Fish ball':0, 'Fish cake': 0, 'Hotdog': 0, 'Lobster ball': 0}
        print("Available dates")
        for idx, date in enumerate(dates, 1):
            print(f'{idx}: {date}')
        try:
            # 0. Obtain user's desired date and time till which the simulation should stop at
            key = int(input("Please enter the index associated with the date, inclusive: "))
            hour = int(input("The hour to simulate until: "))
            time = f'{hour:02d}:00:00'
        
            # 1. Update the list of oden items with the numbers sold
            for item in oden:
                oden[item] = sales[(sales['Date'] == dates[key-1]) & (sales['Time'] <= time )][item].sum().item()
            print(oden)
            total = sum(oden.values())
            print(f'Total oden sold: {total}')
            
            # 2. Estimate till which batch of the package has been opened, since the operation didn't incorporated this functionality
            


            bye = input('Do you wish to exit? (Y/N): ').upper()
            if bye == 'Y':
                print('See you!')
                break
            
                

        except(ValueError):
            print("Invalid input. Please provide only int.")
            time.sleep(0.5)
            continue

        except(IndexError):
            print("Please check that you have entered valid ranges or integers")
            time.sleep(0.5)
            continue

        except(KeyboardInterrupt):
            print('See you again!')
            time.sleep(0.5)
            break


        
# hour = int(input('Please enter the hour in 24hr format'))
# time = f'{hour}:00:00'

# cheeseTofu = sales[(sales['Date'] == '13/01/2026') & (sales['Time'] <= time )]['Cheese tofu'].sum()
# fishBall = sales[(sales['Date'] == '13/01/2026') & (sales['Time'] <= time )]['Fish ball'].sum()

# print(cheeseTofu)

if __name__ == "__main__":
    process()