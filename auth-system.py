import os
import uuid
import bcrypt
import getpass
from cryptography.fernet import Fernet

file_path = "credentials.txt"
key_file = "secret.key"

# Generowanie klucza szyfrowania, jeśli nie istnieje
if not os.path.exists(key_file):
    with open(key_file, 'wb') as keyfile:
        key = Fernet.generate_key()
        keyfile.write(key)
else:
    with open(key_file, 'rb') as keyfile:
        key = keyfile.read()

cipher = Fernet(key)

def hash_password(password):
    """Hashuje hasło za pomocą bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def verify_password(password, hashed_password):
    """Sprawdza, czy hasło pasuje do zaszyfrowanego hasła."""
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def encrypt_data(data):
    """Szyfruje dane przed zapisaniem do pliku."""
    return cipher.encrypt(data.encode()).decode()


def decrypt_data(data):
    """Odszyfrowuje dane pobrane z pliku."""
    return cipher.decrypt(data.encode()).decode()


def signup():
    """Rejestracja użytkownika z UUID i szyfrowaniem danych."""
    email = input('Write your email: ')
    password = getpass.getpass("Choose your password (min. 8 characters, 1 capital letter, 1 special character): ")

    if len(password) >= 8 and not (password.isalnum() and password.islower()):
        password_confirmation = getpass.getpass('Repeat your password: ')

        if password_confirmation == password:
            user_id = str(uuid.uuid4())  # Generowanie UUID
            hashed_password = hash_password(password)  # Hashowanie hasła
            encrypted_entry = encrypt_data(f"{user_id}: {email}: {hashed_password}")

            with open(file_path, 'a') as file:
                file.write(encrypted_entry + "\n")

            print(f"Registration successful! Your User ID: {user_id}")

            # Ukrycie pliku na Windows/Linux/Mac
            if os.name == 'nt':
                os.system(f"attrib +h {file_path}")  # Ukrywanie pliku na Windows
            else:
                os.system(f"chmod 600 {file_path}")  # Ograniczenie dostępu na Linux/Mac

        else:
            print("Passwords do not match. Try again.")
    else:
        print("Password does not meet the requirements. Try again.")


def login():
    """Logowanie użytkownika, odczytując zaszyfrowane dane."""
    email = input("Write your email: ")

    with open(file_path, 'r') as file:
        for line in file:
            try:
                decrypted_line = decrypt_data(line.strip())
                stored_uuid, stored_email, stored_hashed_password = decrypted_line.split(": ")
            except:
                print("Error reading data.")
                continue

            if stored_email != email:
                continue  # Szukamy dalej

            password = getpass.getpass("Password: ")
            if verify_password(password, stored_hashed_password):
                print(f"You have logged in! Your User ID is: {stored_uuid}")
                return
            else:
                print("Invalid password. Try again.")
                return

    print("No such email in database. Try again.")


# Uruchamiamy rejestrację i logowanie
signup()
login()
