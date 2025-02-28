#!/bin/bash

echo "Stopping any existing Pyro4 name servers..."
pkill -f pyro4-ns

echo "Starting Pyro4 name server..."
pyro4-ns -n order_server -p 9095 &
echo "Waiting for nameserver to start..."
while ! nc -z order_server 9095; do sleep 1; done
sleep 2  # Additional wait to ensure nameserver is ready

echo "Starting Order Processing Service..."
python pyro_server.py || echo "Error starting Order Processing Service"