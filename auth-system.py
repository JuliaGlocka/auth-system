import os

# Ścieżka do pliku credentials.txt
file_path = "credentials.txt"

# Tworzenie pliku, jeśli nie istnieje
if not os.path.exists(file_path):
    with open(file_path, 'w') as file:
        file.write("username: password\n")  # Nagłówki w pliku

# Funkcja rejestracji użytkownika
def signup():
    with open(file_path, 'a') as file:
        email = input('Write your email: ')
        password = input("Choose your password. Must be at least 8 characters long and consist of at least 1 capital letter and 1 special sign: ")
        
        # Warunek sprawdzający poprawność hasła
        if len(password) >= 8 and not(password.isalnum() and password.islower()):
            password_confirmation = input('Repeat your password to finalize: ')
            
            if password_confirmation == password:
                file.write(email + ": " + password + "\n")
                print("Registration successful!")
            else:
                print("Passwords do not match. Try again.")
                signup()  # Rekurencja w przypadku błędu (można zastąpić pętlą)
        else:
            print("Password does not meet the requirements. Try again.")
            signup()  # Rekurencja w przypadku błędu (można zastąpić pętlą)

# Wywołanie funkcji rejestracji
signup()

def login():
    with open(file_path, 'r') as file:
    email = input("Write your email: ")
    for line in file:
        login, _ = line.strip().split(":")    