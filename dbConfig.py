import mysql.connector

try:
    conn = mysql.connector.connect(
            user={"user name"},
            password={"user password"},
            host={"host ip"},
            port={port number},
            database={"db_name"}
    )
except:
    print("connect error!")
    exit(1)

cur = conn.cursor()
