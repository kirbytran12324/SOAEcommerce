import logging
import sys
from concurrent import futures
import grpc
import mysql.connector

sys.path.append("/app/grpc_compiled")
import order_pb2
import order_pb2_grpc


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrderProcessingService(order_pb2_grpc.OrderProcessingServicer):
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="grpc_mysql",
            user="root",
            password="root",
            database="ecommerce"
        )
        self.cursor = self.conn.cursor()

    def CalculateTotal(self, request, context):
        product_id = request.product_id
        quantity = request.quantity

        try:
            self.cursor.execute("SELECT price FROM products WHERE product_id = %s", (product_id,))
            result = self.cursor.fetchone()

            if not result:
                logger.warning(f"Product {product_id} not found in database.")
                return order_pb2.OrderResponse(message=f"Error: Product {product_id} not found.", total=0)

            price = result[0]
            total = price * quantity
            logger.info(f"Order confirmed: {quantity} x {product_id} = ${total:.2f}")
            return order_pb2.OrderResponse(message=f"Order confirmed: {quantity} x {product_id} = ${total:.2f}", total=total)
        except Exception as e:
            logger.error(f"Error processing order: {e}")
            return order_pb2.OrderResponse(message=f"Error processing order: {e}", total=0)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_pb2_grpc.add_OrderProcessingServicer_to_server(OrderProcessingService(), server)
    server.add_insecure_port('[::]:50051')
    logger.info("gRPC server started on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()