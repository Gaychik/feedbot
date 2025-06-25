import sqlite3
from database import models
conn =  sqlite3.connect("bot/database/app.db")
cursor = conn.cursor()

def get_user_by_phone(phone):
    cursor.execute("select * from users where phone = ?",(phone,))
    return cursor.fetchone()
def add_dish(d: models.Dish):
    try:
        cursor.execute("INSERT INTO dishes values(?,?,?,?,?,?)",d.to_tuple())
        conn.commit()
        return True 
    except: 
        return False
    
def get_dishes():
    cursor.execute("SELECT * FROM dishes")
    dishes = [] 
    for r in cursor.fetchall():
        dish = models.Dish()
        dish.from_tuple(r)
        dishes.append(dish)
    return dishes