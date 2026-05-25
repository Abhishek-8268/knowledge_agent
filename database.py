import sqlite3
import random
from datetime import datetime, timedelta

DB_NAME = "ecommerce.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print("Creating tables...")
    
    # 1. Customers Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            city TEXT NOT NULL
        )
    """)

    # 2. Products Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)

    # 3. Orders Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            product_id INTEGER,
            order_date TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        )
    """)

    conn.commit()
    return conn, cursor

def seed_db(conn, cursor):
    print("Seeding dummy data (50-200 rows total)...")
    
    # Clear existing data
    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM products")
    cursor.execute("DELETE FROM customers")

    # --- GENERATE 15 CUSTOMERS ---
    names = ["Abhishek", "Nitya", "Rohan", "Priya", "Amit", "Sneha", "Rahul", "Kavita", "Vikram", "Pooja", "Siddharth", "Neha", "Karan", "Anjali", "Manish"]
    cities = ["New Delhi", "Mumbai", "Bangalore", "Pune", "Motihari", "Hyderabad", "Chennai", "Kolkata", "Nagpur", "Ahmedabad"]
    
    customers = []
    for name in names:
        city = random.choice(cities)
        customers.append((name, city))
        
    cursor.executemany("INSERT INTO customers (name, city) VALUES (?, ?)", customers)

    # --- GENERATE 15 PRODUCTS ---
    product_data = [
        ("White Lace-up Sneakers", "Apparel", 4500.00),
        ("Mechanical Keyboard", "Tech", 6500.00),
        ("Hyderabadi Dum Chicken Biryani", "Food", 350.00),
        ("Noise Cancelling Headphones", "Tech", 12000.00),
        ("Farmhouse Pizza", "Food", 450.00),
        ("Cotton T-Shirt", "Apparel", 800.00),
        ("Wireless Mouse", "Tech", 1500.00),
        ("Kadhai Chicken", "Food", 400.00),
        ("Running Shoes", "Apparel", 3500.00),
        ("USB-C Hub", "Tech", 2000.00),
        ("Paneer Butter Masala", "Food", 300.00),
        ("Denim Jeans", "Apparel", 2500.00),
        ("Smartwatch", "Tech", 5000.00),
        ("Garlic Bread", "Food", 150.00),
        ("Sunglasses", "Apparel", 1200.00)
    ]
    cursor.executemany("INSERT INTO products (name, category, price) VALUES (?, ?, ?)", product_data)

    # --- GENERATE 120 ORDERS (Dates in April 2026) ---
    orders = []
    start_date = datetime(2026, 4, 1)
    
    for _ in range(120):
        customer_id = random.randint(1, 15)
        product_id = random.randint(1, 15)
        # Random day in April 2026
        random_days = random.randint(0, 29) 
        order_date = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")
        quantity = random.randint(1, 5)
        
        orders.append((customer_id, product_id, order_date, quantity))

    cursor.executemany("INSERT INTO orders (customer_id, product_id, order_date, quantity) VALUES (?, ?, ?, ?)", orders)

    conn.commit()
    
    # Verify the constraints
    cursor.execute("SELECT COUNT(*) FROM customers")
    c_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM products")
    p_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM orders")
    o_count = cursor.fetchone()[0]
    
    total_rows = c_count + p_count + o_count
    print(f"Database setup complete. Data saved to {DB_NAME}.")
    print(f"Total Rows Generated: {total_rows} (Customers: {c_count}, Products: {p_count}, Orders: {o_count})")

if __name__ == "__main__":
    connection, db_cursor = init_db()
    seed_db(connection, db_cursor)
    connection.close()