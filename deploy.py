import sqlite3

with sqlite3.connect('client.db') as conn:
    cur = conn.cursor()
    # cur.execute('DROP TABLE IF EXISTS "clients"')

    cur.execute('CREATE TABLE IF NOT EXISTS "clients" (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, phone INTEGER, name TEXT)')
    conn.commit()