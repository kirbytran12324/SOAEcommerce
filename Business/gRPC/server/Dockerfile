FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the server code and protobuf files
COPY server/ .
COPY grpc_compiled/order_pb2.py grpc_compiled/order_pb2_grpc.py /app/grpc_compiled/

CMD ["python", "grpc_server.py"]