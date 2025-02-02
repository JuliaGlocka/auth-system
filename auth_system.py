import os
import uuid
import bcrypt
import getpass
import cryptography
from cryptography.fernet import Fernet

file_path = "credentials.txt"
key_file = "secret.key"

# Generowanie i/lub odczyt klucza szyfrującego
if not os.path.exists(key_file):
    with open(key_file, 'wb') as keyfile:
        key = Fernet.generate_key()
        keyfile.write(key)
else:
    with open(key_file, 'rb') as keyfile:
        key = keyfile.read()

cipher = Fernet(key)

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def encrypt_data(data):
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(data):
    try:
        return cipher.decrypt(data).decode()
    except cryptography.fernet.InvalidToken as e:
        # Dodajemy szczegółowy komunikat błędu
        print(f"Decryption error: {e}. Data may be corrupted or invalid.")
        return None

def validate_email(email):
    return bool(email.strip()) and email.count("@") == 1

def validate_password(password):
    return (
        len(password) >= 8 and
        any(not c.isalnum() for c in password) and
        any(c.isupper() for c in password)
    )

def signup():
    print("Entered signup function")  # Debug: śledzenie przebiegu funkcji
    while True:
        email = input('Write your email: ')
        if not validate_email(email):
            if not email.strip():
                print("Email cannot be empty. Try again.")
            else:
                print("Invalid email. It must contain exactly one '@' and have valid parts before and after '@'. Try again.")
            continue

        print("Email is valid, proceeding to password step...")
        while True:
            # Używamy input() do testów – można zmienić z powrotem na getpass.getpass() gdy środowisko na to pozwoli
            password = input(
                "Write your password carefully. It will be displayed.\n"
                "Requirements:\n- Min. 8 characters\n- At least 1 capital letter\n- At least 1 special character\n"
            )
            if not validate_password(password):
                print("Password does not meet the requirements. Try again.")
                continue

            password_confirmation = input('Repeat your password: ')
            if password_confirmation != password:
                print("Passwords do not match. Try again.")
                continue

            print("Password confirmed, proceeding with registration...")
            user_id = str(uuid.uuid4())
            hashed_password = hash_password(password)
            encrypted_entry = encrypt_data(f"{user_id}:{email}:{hashed_password}")
            with open(file_path, 'a') as file:
                file.write(encrypted_entry + "\n")

            print(f"Registration successful! Your User ID: {user_id}")
            if os.name == 'nt':
                os.system(f"attrib +h {file_path}")
            else:
                os.system(f"chmod 600 {file_path}")
            return

def login():
    email = input("Write your email: ")
    try:
        with open(file_path, 'r') as file:
            for line in file:
                decrypted_line = decrypt_data(line.strip())
                if decrypted_line is None:
                    print("Skipping this entry due to decryption failure.")
                    continue

                try:
                    stored_uuid, stored_email, stored_hashed_password = decrypted_line.split(":")
                except ValueError:
                    print("Error: Data format is incorrect. Skipping entry.")
                    continue

                if stored_email.strip() != email.strip():
                    continue

                password = input("Password: ")
                if verify_password(password, stored_hashed_password.strip()):
                    print(f"You have logged in! Your User ID is: {stored_uuid}")
                    return
                else:
                    print("Invalid password. Try again.")
                    return
    except FileNotFoundError:
        print("Error: No credentials database found. Please sign up first.")

    print("No such email in database. Try again.")

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

choose()
