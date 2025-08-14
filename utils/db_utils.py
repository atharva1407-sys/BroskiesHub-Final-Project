import sqlite3

def init_db():
    conn = sqlite3.connect('db/restaurant.db')
    c = conn.cursor()

    # Create menu table
    c.execute('''CREATE TABLE IF NOT EXISTS menu (
        item TEXT,
        category TEXT,
        price REAL,
        gst REAL
    )''')

    # Create orders table
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        total REAL,
        gst REAL,
        discount REAL,
        payment_method TEXT,
        order_type TEXT,
        date TEXT
    )''')

    # Create order_items table
    c.execute('''CREATE TABLE IF NOT EXISTS order_items (
        order_id INTEGER,
        item TEXT,
        quantity INTEGER,
        price REAL,
        FOREIGN KEY(order_id) REFERENCES orders(order_id)
    )''')

    conn.commit()
    conn.close()
