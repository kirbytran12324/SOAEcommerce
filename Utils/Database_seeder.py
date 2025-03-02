import mysql.connector
import random
import uuid

# Sample product categories and names
product_categories = {
    "Electronics": ["Smartphone", "Laptop", "Headphones", "Smartwatch", "Tablet", "Bluetooth Speaker"],
    "Home Appliances": ["Microwave", "Refrigerator", "Washing Machine", "Air Purifier", "Vacuum Cleaner"],
    "Clothing": ["T-shirt", "Jeans", "Jacket", "Sneakers", "Backpack", "Sunglasses"],
    "Accessories": ["Wristwatch", "Handbag", "Wallet", "Belt", "Hat", "Scarf"],
    "Gaming": ["Gaming Mouse", "Mechanical Keyboard", "Gaming Chair", "VR Headset", "Graphics Card"]
}

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="root",
    database="ecommerce"
)
cursor = conn.cursor()

products = set()
while len(products) < 1000:
    category = random.choice(list(product_categories.keys()))
    product_name = random.choice(product_categories[category])
    product_id = str(uuid.uuid4())[:8].upper()
    price = round(random.uniform(10, 2000), 2)

    products.add((product_id, product_name, price))

# Insert into MySQL
cursor.executemany("INSERT INTO products (product_id, name, price) VALUES (%s, %s, %s)", list(products))
conn.commit()

print("Inserted 1000 unique real-world products.")
cursor.close()
conn.close()
