from classes import *
engine = create_engine("sqlite:///our.db")
Base.metadata.create_all(engine)


def hash(p):
    return p

h = {
    'cashier': 'hash123',
    'admin': 'hash123',
}

def load(u):
    print(u, 'loaded!')

while True:
    user = input("Input the user: ")
    if user == 'cashier' or user == 'admin':
        while True:
            password = input("Input the password: ")
            if hash(password) == h[user]:
                load(user)
                break
            else:
                print("Incorrect password. Try again")
        break
    else:
        print("User does not exist. Try again")