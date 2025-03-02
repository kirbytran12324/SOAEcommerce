import logging
import mysql.connector
from thrift.server import TServer
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from gen_py.order_service import OrderProcessingService
import sys
import os
sys.path.append(os.path.dirname(__file__))  # Add current directory to path

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class OrderProcessingHandler:
    def __init__(self):
        try:
            logger.info("Connecting to MySQL database...")
            self.conn_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="ecommerce_pool",
                pool_size=15,
                host="apache_mysql",
                user="root",
                password="root",
                database="ecommerce"
            )
            logger.info("Successfully connected to MySQL.")
        except mysql.connector.Error as e:
            logger.error(f"Failed to connect to MySQL: {e}")
            sys.exit(1)  # Exit if database connection fails

    def calculate_total(self, product_id, quantity):
        conn = None
        cursor = None
        try:
            conn = self.conn_pool.get_connection()
            if not conn.is_connected():
                conn.reconnect()

            cursor = conn.cursor()

            # Execute the query
            cursor.execute("SELECT price FROM products WHERE product_id = %s", (product_id,))
            result = cursor.fetchone()

            if not result:
                logger.warning(f"Product {product_id} not found in database.")
                return f"Error: Product {product_id} not found."

            price = result[0]
            total = price * quantity
            logger.info(f"Order confirmed: {quantity} x {product_id} = ${total:.2f}")
            return f"Order confirmed: {quantity} x {product_id} = ${total:.2f}"

        except mysql.connector.Error as e:
            logger.error(f"Error processing order: {e}")
            return f"Error processing order: {e}"
        finally:
            # Always close the cursor and connection
            if cursor:
                cursor.close()
            if conn:
                conn.close()

def start_server():
    logger.info("Initializing Thrift server...")
    handler = OrderProcessingHandler()
    processor = OrderProcessingService.Processor(handler)
    transport = TSocket.TServerSocket(host='0.0.0.0', port=50000)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)

    logger.info("Thrift server started on port 50000. Waiting for requests...")
    try:
        server.serve()
    except KeyboardInterrupt:
        logger.info("Shutting down Thrift server...")
    except Exception as e:
        logger.error(f"Server encountered an error: {e}")
    finally:
        if handler.conn:
            handler.conn.close()
            logger.info("Closed MySQL connection.")

if __name__ == "__main__":
    start_server()
