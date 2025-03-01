import grpc
import sys

sys.path.append("/app/grpc_compiled")
import order_pb2
import order_pb2_grpc

def run():
    with grpc.insecure_channel('order_server:50051') as channel:
        stub = order_pb2_grpc.OrderProcessingStub(channel)
        product_id = input("Enter Product ID: ")
        quantity = int(input("Enter Quantity: "))
        response = stub.CalculateTotal(order_pb2.OrderRequest(product_id=product_id, quantity=quantity))
        print(response.message)

if __name__ == '__main__':
    run()