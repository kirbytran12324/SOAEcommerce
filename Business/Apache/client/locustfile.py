from locust import User, task, between, events
import random
import uuid
import json
import time
import sys

from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport
sys.path.append("/app/gen_py")

from order_service import OrderProcessingService


class OrderProcessingUser(User):
    wait_time = between(1, 3)
    valid_product_ids = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transport = None
        self.client = None

    def on_start(self):
        """Load product IDs from JSON file and connect to Thrift service."""
        try:
            # Load product IDs from JSON file
            with open("/app/product_ids.json", "r") as f:
                self.valid_product_ids = json.load(f)

            if not self.valid_product_ids:
                print("⚠️ No product IDs found. Tests may fail.")

            # Connect to Thrift service
            self.transport = TSocket.TSocket('order_server', 50000)
            self.transport = TTransport.TBufferedTransport(self.transport)
            protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
            self.client = OrderProcessingService.Client(protocol)
            self.transport.open()
            print("✅ Connected to Order Processing Service")

        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            self.stop()

    @task
    def place_order(self):
        if not self.valid_product_ids:
            return  # Skip if no product IDs

        product_id = (
            random.choice(self.valid_product_ids)
            if random.random() < 0.9
            else str(uuid.uuid4())[:8].upper()
        )
        quantity = random.randint(1, 10)

        start_time = time.time()
        try:
            response = self.client.calculate_total(product_id, quantity)
            print(f"✅ Success: {response}")
            # Report success to Locust
            events.request.fire(
                request_type="Thrift",
                name="place_order",
                response_time=int((time.time() - start_time) * 1000),  # in milliseconds
                response_length=len(str(response)),
                exception=None,
            )
        except Exception as e:
            print(f"❌ Order Failed: {e}")
            # Report failure to Locust
            events.request.fire(
                request_type="Thrift",
                name="place_order",
                response_time=int((time.time() - start_time) * 1000),  # in milliseconds
                response_length=0,
                exception=e,
            )