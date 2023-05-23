import mysql.connector

try:
    conn = mysql.connector.connect(
            user="kenny",
            password="Kenny061256",
            host="localhost",
            port=3306,
            database="telegram_db"
    )
except:
    print("connect error!")
    exit(1)

cur = conn.cursor()
