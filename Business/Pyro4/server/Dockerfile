FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get install -y net-tools


COPY pyro_server.py .
COPY start_server.sh .

RUN chmod +x start_server.sh

CMD ["./start_server.sh"]