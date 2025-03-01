from locust import User, task, between, events
import Pyro4
import random
import uuid
import json
import time

class OrderProcessingUser(User):
    wait_time = between(1, 3)
    valid_product_ids = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ns = None  # Define ns in __init__
        self.order_service = None  # Define order_service in __init__

    def on_start(self):
        """Load product IDs from JSON file and connect to Pyro4 service."""
        try:
            # Load product IDs from JSON file
            with open("/app/product_ids.json", "r") as f:
                self.valid_product_ids = json.load(f)

            if not self.valid_product_ids:
                print("⚠️ No product IDs found. Tests may fail.")

            # Connect to Pyro4 service
            self.ns = Pyro4.locateNS(host="order_server", port=9095)
            uri = self.ns.lookup("order.processing.service")
            self.order_service = Pyro4.Proxy(uri)
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
            response = self.order_service.calculate_total(product_id, quantity)
            print(f"✅ Success: {response}")
            # Report success to Locust
            events.request.fire(
                request_type="Pyro4",
                name="place_order",
                response_time=int((time.time() - start_time) * 1000),  # in milliseconds
                response_length=len(str(response)),
                exception=None,
            )
        except Exception as e:
            print(f"❌ Order Failed: {e}")
            # Report failure to Locust
            events.request.fire(
                request_type="Pyro4",
                name="place_order",
                response_time=int((time.time() - start_time) * 1000),  # in milliseconds
                response_length=0,
                exception=e,
            )