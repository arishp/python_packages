import sqlite3

def create_table():
    conn = sqlite3.connect("scraped_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scraped_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            value REAL
        )
    """)
    conn.commit()
    conn.close()

def insert_data(title, value):
    conn = sqlite3.connect("scraped_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scraped_data (title, value) VALUES (?, ?)", (title, value))
    conn.commit()
    conn.close()

def get_all_data():
    conn = sqlite3.connect("scraped_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scraped_data")
    data = cursor.fetchall()
    conn.close()
    return data

def get_average_value():
    conn = sqlite3.connect("scraped_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(value) FROM scraped_data")
    average = cursor.fetchone()[0]
    conn.close()
    return average