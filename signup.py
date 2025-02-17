import uuid
from encryption import hash_password, encrypt_data
from config import get_db_connection

def validate_email(email):
    email = email.strip()
    return bool(email) and email.count("@") == 1 and "." in email.split("@")[1]

def validate_password(password):
    return len(password) >= 8 and any(not c.isalnum() for c in password) and any(c.isupper() for c in password)

def signup():
    while True:
        email = input('Write your email: ')
        if not validate_email(email):
            print("Invalid email. Try again.")
            continue

        password = input("Write your password: ")
        if not validate_password(password):
            print("Password does not meet the requirements. Try again.")
            continue

        password_confirmation = input('Repeat your password: ')
        if password_confirmation != password:
            print("Passwords do not match. Try again.")
            continue

        user_id = str(uuid.uuid4())  # Generowanie ID użytkownika
        hashed_password = hash_password(password)  # Hashowanie hasła
        encrypted_email = encrypt_data(email)  # Szyfrowanie e-maila

        try:
            # Łączenie z bazą danych i zapis do tabeli
            with get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO users (id, email, password_hash) VALUES (%s, %s, %s)",
                                   (user_id, encrypted_email, hashed_password))
                    connection.commit()  # Zatwierdzenie transakcji
            print(f"Registration successful! Your User ID: {user_id}")
        except Exception as e:
            print(f"Error: {e}")
        return
