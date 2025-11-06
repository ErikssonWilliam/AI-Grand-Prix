FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    x11-apps \
    xauth \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY websocket_server.py .
COPY agent.py .
COPY training_agents/ ./training_agents/

ENV DISPLAY=:0

CMD ["python", "server.py"]