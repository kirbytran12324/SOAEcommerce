import Pyro4

ns = Pyro4.locateNS(host="order_server", port=9095)
uri = ns.lookup("order.processing.service")
order_service = Pyro4.Proxy(uri)

product_id = input("Enter Product ID: ")
quantity = int(input("Enter Quantity: "))

response = order_service.calculate_total(product_id, quantity)
print(response)
