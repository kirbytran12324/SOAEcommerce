import Pyro4
import logging
import mysql.connector

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@Pyro4.expose
class OrderProcessingService:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="mysql_container",
                user="root",
                password="root",
                database="ecommerce"
            )
            self.cursor = self.conn.cursor()
            logger.info("Connected to the database successfully.")
        except mysql.connector.Error as err:
            logger.error(f"Database connection failed: {err}")

    def calculate_total(self, product_id, quantity):
        try:
            logger.debug(f"Received request: Product ID = {product_id}, Quantity = {quantity}")
            self.cursor.execute("SELECT price FROM products WHERE product_id = %s", (product_id,))
            result = self.cursor.fetchone()

            if not result:
                logger.warning(f"Product {product_id} not found in database.")
                return f"Error: Product {product_id} not found."

            price = result[0]
            total = price * quantity
            logger.info(f"Order confirmed: {quantity} x {product_id} = ${total:.2f}")
            return f"Order confirmed: {quantity} x {product_id} = ${total:.2f}"
        except Exception as e:
            logger.error(f"Error processing order: {e}")
            return f"Error processing order: {e}"

# Start the Pyro4 daemon with a fixed port
def start_server():
    try:
        daemon = Pyro4.Daemon(host="0.0.0.0", port=50000)
        ns = Pyro4.locateNS(host="order_server", port=9095)
        uri = daemon.register(OrderProcessingService)
        ns.register("order.processing.service", uri)
        logger.info(f"Order Processing Service registered with URI: {uri}")
        logger.info("Order Processing Service is running...")
        daemon.requestLoop()
    except Exception as e:
        logger.error(f"Error while starting the Pyro4 service: {e}")

if __name__ == "__main__":
    start_server()
