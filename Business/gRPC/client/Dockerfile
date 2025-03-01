FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY client/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the client code and root folder files
COPY client/ .
COPY grpc_compiled/order_pb2.py grpc_compiled/order_pb2_grpc.py /app/grpc_compiled/
COPY client/product_ids.json /app/

CMD ["python", "grpc_client.py"]