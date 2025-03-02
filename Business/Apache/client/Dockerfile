FROM python:3.9-slim

WORKDIR /app

# Install Thrift compiler and dependencies
RUN apt-get update && \
    apt-get install -y thrift-compiler && \
    rm -rf /var/lib/apt/lists/*

# Create directory for generated code
RUN mkdir -p /app/gen_py

# Copy Thrift file and generate code
COPY thrift/order.thrift .
RUN thrift -r --gen py -out /app/gen_py order.thrift

# Install Python dependencies
COPY client/requirements.txt .
RUN pip install -r requirements.txt

# Copy client files
COPY client/locustfile.py .
COPY client/product_ids.json .

# Expose Locust web interface port
EXPOSE 8089

# Default command to run Locust
CMD ["locust", "-f", "locustfile.py", "--host=http://order_server:50000", "--web-port=8089"]