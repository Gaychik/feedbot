import sqlite3

conn =  sqlite3.connect("bot/database/app.db")
cursor = conn.cursor()

def get_user_by_phone(phone):
    cursor.execute("select * from users where phone = ?",(phone,))
    return cursor.fetchone()
    