
**HÄR ÄR TANKEN BAKOM VÅRAN SETUP**

Welcome to the Super Mario Kart AI Hackathon! This guide will walk you through the steps to set up your development environment and start building an AI to control the car. Your goal is to write a Python script that makes intelligent decisions based on real-time game data.

**Prerequisites**

**Python:** The programming language you'll be using to write your AI.

**Docker:** A platform for running the C++ game engine without needing to install its dependencies.

  Docker for Linux: https://docs.docker.com/desktop/setup/install/linux/

**Step 1: Start the Game Server**

  Open your terminal and execute this command: docker run -p 8080:8080 -d mariokart-server:latest

  **HÄR ÄR TANKEN ATT (mariokart-server:latest): är en public docker image som innehåller C++ spelet. Detta kommer ligga som open source på dockerhub så spelarna kan pulla direkt från det.**

**Step 2: Set Up the Python Environment**

Create virtual environment and pip install -r requirements.txt

**Step 3: Understand the API**
The interaction between your Python agent and the C++ game is handled through a simple API with two key components: state and action.

**state:** A Python dictionary sent from the game to your agent. It contains all the real-time information you need to make decisions, such as your car's position (player_x, player_y), speed (player_speed), and game status (done, reward).

**action:** An integer you send from your agent to the game. It tells your car what to do. The available actions are:

**EXEMPEL ACTIONS**
0: Accelerate

1: Turn Left

2: Turn Right

3: Brake

**Step 4: Build and Run Your Agent**

Open the agent.py file in your code editor. You'll find a basic structure that connects to the game and runs a loop. Your task is to write your AI logic here.

To test your agent, save your changes and run the script from your terminal: python agent.py
