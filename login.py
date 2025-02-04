from encryption import decrypt_data, verify_password
from config import file_path

def validate_email(email):
    return bool(email.strip()) and email.count("@") == 1

def validate_password(password):
    return (
        len(password) >= 8 and
        any(not c.isalnum() for c in password) and
        any(c.isupper() for c in password)
    )

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
