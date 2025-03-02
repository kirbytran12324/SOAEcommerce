FROM python:3.9-slim

RUN apt-get update && apt-get install -y thrift-compiler
COPY server/requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY thrift/order.thrift .
RUN thrift -r --gen py -out . order.thrift  # Generate during build

COPY server/ .
CMD ["python", "thrift_server.py"]