import time
import Pyro4


def connect_to_ns():
    attempts = 0
    while attempts < 5:
        try:
            ns = Pyro4.locateNS(host="order_server", port=9095)
            print("✅ Connected to Name Server!")
            print("🔍 Registered Services:", ns.list())
            return ns
        except Exception as e:
            print(f"❌ Connection failed: {e}. Retrying...")
            attempts += 1
            time.sleep(2)
    print("❌ Could not connect after multiple attempts.")
    return None


def connect_to_service(ns):
    attempts = 0
    while attempts < 5:
        try:
            uri = ns.lookup("order.processing.service")
            print("✅ Found service URI:", uri)
            return uri
        except Pyro4.errors.NamingError:
            print("❌ Service not found. Retrying...")
            attempts += 1
            time.sleep(2)
    print("❌ Could not find service after multiple attempts.")
    return None


ns = connect_to_ns()
if ns:
    uri = connect_to_service(ns)
    if uri:
        order_service = Pyro4.Proxy(uri)

        product_id = input("Enter Product ID: ")
        quantity = int(input("Enter Quantity: "))

        response = order_service.calculate_total(product_id, quantity)
        print(response)