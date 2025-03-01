import mysql.connector
import json

def fetch_product_ids():
    """Fetch product IDs from MySQL and save to a JSON file."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="ecommerce"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT product_id FROM products")
        product_ids = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()

        # Save to a JSON file
        with open("../Business/Pyro4/client/product_ids.json", "w") as f:
            json.dump(product_ids, f)
        print(f"✅ Fetched {len(product_ids)} product IDs")

    except Exception as e:
        print(f"❌ Failed to fetch product IDs: {e}")
        raise

if __name__ == "__main__":
    fetch_product_ids()