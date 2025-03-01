from locust import User, task, between, events
import grpc
import random
import uuid
import json
import time
import sys

# Add the root folder to the Python path
sys.path.append("/app/grpc_compiled")

# Import generated gRPC modules
import order_pb2
import order_pb2_grpc

class OrderProcessingUser(User):
    wait_time = between(1, 3)
    valid_product_ids = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel = grpc.insecure_channel('order_server:50051')
        self.stub = order_pb2_grpc.OrderProcessingStub(self.channel)  # ✅ Fixed import

    def on_start(self):
        """Load product IDs from JSON file."""
        super().on_start()  # ✅ Ensures Locust initializes correctly
        try:
            with open("/app/product_ids.json", "r") as f:
                self.valid_product_ids = json.load(f)
        except Exception as e:
            print(f"❌ Failed to load product IDs: {e}")

    @task
    def place_order(self):
        if not self.valid_product_ids:
            return

        product_id = (
            random.choice(self.valid_product_ids)
            if random.random() < 0.9
            else str(uuid.uuid4())[:8].upper()
        )
        quantity = random.randint(1, 10)

        start_time = time.time()
        try:
            response = self.stub.CalculateTotal(
                order_pb2.OrderRequest(product_id=product_id, quantity=quantity)  # ✅ Fixed import
            )
            events.request.fire(
                request_type="gRPC",
                name="place_order",
                response_time=int((time.time() - start_time) * 1000),
                response_length=len(str(response)),
                exception=None,
            )
        except Exception as e:
            events.request.fire(
                request_type="gRPC",
                name="place_order",
                response_time=int((time.time() - start_time) * 1000),
                response_length=0,
                exception=e,
            )
