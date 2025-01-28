import os


file_path = "credentials.txt"


if not os.path.exists(file_path):
    with open(file_path, 'w') as file:
        file.write("username: password\n")


def signup():
    while True:
            email = input('Write your email: ')
            password = input("Choose your password. Must be at least 8 characters long and consist of at least 1 capital letter and 1 special sign: ")


            if len(password) >= 8 and not(password.isalnum() and password.islower()):
                password_confirmation = input('Repeat your password to finalize: ')
            
                if password_confirmation == password:
                    with open(file_path, 'a') as file:
                        file.write(email + ": " + password + "\n")
                    print("Registration successful!")
                    break
                else:
                    print("Passwords do not match. Try again.")
            else:
                print("Password does not meet the requirements. Try again.")

signup()

def login():
    with open(file_path, 'r') as file:
        email = input("Write your email: ")
        for line in file:
            #technically try except is not necessary with this credential.txt and signup logic, but it will stay for case of manual file changes.
            try:
                stored_login, stored_password = line.strip().split(":")
            except ValueError:
                print("Invalid line format in credential source")
                continue

            match email:
                    case _ if stored_login != email:
                        continue

                    case _ if stored_login == email:
                        password = input("Password: ")
                        if password == stored_password.strip():
                            print("You have logged in!")
                            return
                        else:
                            print("Invalid password. Try again.")
                            return
    print("No such email in database. Try again")

login()