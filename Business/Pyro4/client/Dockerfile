FROM python:3.9-slim

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the client and Locust files
COPY order_client.py locustfile.py product_ids.json /app/

# Set working directory
WORKDIR /app

# Default command (can be overridden in docker-compose.yml)
CMD ["python", "order_client.py"]