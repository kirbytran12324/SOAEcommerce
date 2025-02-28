#!/bin/bash

echo "Stopping any existing Pyro4 name servers..."
pkill -f pyro4-ns

echo "Starting Pyro4 name server..."
pyro4-ns -n 0.0.0.0 -p 9095 &
while ! nc -z 0.0.0.0 9095; do sleep 1; done

echo "Starting Order Processing Service..."
python pyro_server.py || echo "Error starting Order Processing Service"
