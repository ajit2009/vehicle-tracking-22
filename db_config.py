# db_config.py

import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='sql7.freesqldatabase.com',       # Server address
        user='sql7770632',                     # Your database username
        password='rW4FZ1M34e',                # Your database password
        database='sql7770632',                 # Your database name
        port=3306                             # Default MySQL port
    )
