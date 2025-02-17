from encryption import verify_password, decrypt_data
from config import get_db_connection

def login():
    email = input("Write your email: ")

    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, email, password_hash FROM users")
                users = cursor.fetchall()

                for stored_uuid, encrypted_email, stored_hashed_password in users:
                    decrypted_email = decrypt_data(encrypted_email)

                    if decrypted_email and decrypted_email == email:
                        password = input("Password: ")
                        if verify_password(password, stored_hashed_password):
                            print(f"You have logged in! Your User ID is: {stored_uuid}")
                            return
                        else:
                            print("Invalid password. Try again.")
                            return

                print("No such email in database. Try again.")
    except Exception as e:
        print(f"Error: {e}")
