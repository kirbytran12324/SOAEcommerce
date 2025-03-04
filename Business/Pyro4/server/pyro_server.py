import Pyro4
import logging
import mysql.connector

# Set the hostname for Pyro4 to use in URIs
Pyro4.config.HOST = "order_server"

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@Pyro4.expose
class OrderProcessingService:
    def __init__(self):
        self.conn_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="ecommerce_pool",
            pool_size=12,
            host="mysql",
            user="root",
            password="root",
            database="ecommerce"
        )

    def calculate_total(self, product_id, quantity):
        try:
            conn = self.conn_pool.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT price FROM products WHERE product_id = %s", (product_id,))
            result = cursor.fetchone()

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
        finally:
            if conn:
                conn.close()

# Start the Pyro4 daemon with a fixed port
def start_server():
    try:
        daemon = Pyro4.Daemon(host="0.0.0.0", port=50000)
        daemon._pyroHmacKey = None
        ns = Pyro4.locateNS(host="order_server", port=9095)
        service = OrderProcessingService()
        uri = daemon.register(service, objectId="order.processing.service")
        uri = Pyro4.URI(f"PYRO:order.processing.service@order_server:50000")
        ns.register("order.processing.service", uri)
        logger.info(f"Order Processing Service registered with URI: {uri}")
        logger.info("Order Processing Service is running...")
        daemon.requestLoop()
    except Exception as e:
        logger.error(f"Error while starting the Pyro4 service: {e}")

if __name__ == "__main__":
    start_server()
