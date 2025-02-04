from signup import signup
from login import login

def choose():
    while True:
        try:
            answer = int(input('Type 1 for signup, 2 for login or 0 to end program: '))
        except ValueError:
            print("Invalid input, please enter a number (1 or 2).")
            continue

        if answer == 1:
            signup()
        elif answer == 2:
            login()
        elif answer == 0:
            print("Program terminated.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 0.")
