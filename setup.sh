#!/bin/bash
echo "Starting Mario Kart RL Hackathon..."

# Allow Docker to display windows
xhost +

echo "Building Python server..."
docker-compose build python-server

echo "Starting everything..."
docker-compose up

#chmod +x setup.sh
#./setup.sh