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
            time.sleep(2)  # Wait 2 seconds before retrying
    print("❌ Could not connect after multiple attempts.")
    return None

ns = connect_to_ns()
if ns:
    uri = ns.lookup("order.processing.service")
    order_service = Pyro4.Proxy(uri)
