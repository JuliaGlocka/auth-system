import uuid
import os
from encryption import encrypt_data, hash_password
from config import file_path

def validate_email(email):
    return bool(email.strip()) and email.count("@") == 1

def validate_password(password):
    return (
        len(password) >= 8 and
        any(not c.isalnum() for c in password) and
        any(c.isupper() for c in password)
    )

def signup():
    print("Entered signup function")
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
