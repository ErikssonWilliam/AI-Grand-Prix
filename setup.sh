#!/bin/bash
echo "Starting Mario Kart RL Hackathon..."

# Detect platform and set appropriate display
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Linux detected - using native X11"
    xhost +
    export DISPLAY=:0
    DOCKER_COMPOSE_FILE="docker-compose.linux.yml"
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macOS detected - using XQuartz"
    export DISPLAY=host.docker.internal:0
    DOCKER_COMPOSE_FILE="docker-compose.mac.yml" 
    
else
    echo "Unsupported platform: $OSTYPE"
    exit 1
fi

echo "Building Python server..."
docker-compose -f $DOCKER_COMPOSE_FILE build python-server

echo "Starting everything..."
docker-compose -f $DOCKER_COMPOSE_FILE up

#chmod +x setup.sh
#./setup.sh