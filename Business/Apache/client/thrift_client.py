import logging
import sys
from thrift import Thrift
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
sys.path.append("/app/gen_py")
from order_service import OrderProcessingService





# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def connect_to_service():
    logger.info("Attempting to connect to Thrift server at order_server:50000...")

    transport = TSocket.TSocket('order_server', 50000)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = OrderProcessingService.Client(protocol)

    try:
        transport.open()
        logger.info("Connected to Thrift server successfully.")
        return client, transport
    except Thrift.TException as ex:
        logger.error(f"Connection failed: {ex}")
        return None, None


if __name__ == "__main__":
    client, transport = connect_to_service()

    if client:
        try:
            product_id = input("Enter Product ID: ")
            quantity = int(input("Enter Quantity: "))
            logger.debug(f"Sending request: product_id={product_id}, quantity={quantity}")

            response = client.calculate_total(product_id, quantity)

            logger.info(f"Response received: {response}")
            print(response)
        except Exception as e:
            logger.error(f"Error during request: {e}")
        finally:
            transport.close()
            logger.info("Closed connection to Thrift server.")
