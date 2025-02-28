FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get install -y net-tools

COPY order_client.py .

CMD ["python", "order_client.py"]
