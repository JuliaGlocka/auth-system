
key_file = "secret.key"


import psycopg2

DB_CONFIG = {
    'dbname': 'auth_system',
    'user': 'auth_user',
    'password': 'securepassword',
    'host': 'localhost',
    'port': 5432
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

