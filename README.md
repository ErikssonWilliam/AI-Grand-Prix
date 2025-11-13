
# AI Grand Prix - Hackathon Setup Guide

Welcome to the Super Mario Kart AI Hackathon! This guide will walk you through the steps to set up your development environment and start building an AI to control the car. Your goal is to write a Python script that makes intelligent decisions based on real-time game data.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Linux Setup](#linux-setup)
- [Windows Setup](#windows-setup)
- [MacOS Setup](#macos-setup)
- [Verifying Installation](#verifying-installation)
- [Running the Project](#running-the-project)
- [Troubleshooting](#troubleshooting)

# Prerequisites

**Python:** The programming language you'll be using to write your AI.
**Docker:** A platform for running the super mario game engine without needing to install its dependencies.
**VSCode (or other code editor):** The code editor you'll use to write and edit your Python code.
**Git:** Version control tool you'll use to download the hackaton code and save your changes.

## Step 1: Install Python

### Windows
1. Download Python 3.8 or newer from [python.org](https://www.python.org/downloads/)
2. Click on "download python" and run the downloaded file (it will be called something like `python-3.11.0.exe`)
3. **Important**: Check the box "Add Python to PATH" at the bottom of the first screen
4. Click "Install Now" and wait for completion
5. **Verify it worked**: 
   - Press `Windows Key + R`, type `cmd`, press Enter
   - In the black window, type: `python --version`
   - You should see something like `Python 3.11.0`

### Mac

1. Open Terminal (Press `Cmd + Space`, type "Terminal", press Enter)
2. Copy and paste this command, then press Enter:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
3. Copy and paste this command: brew install python
4. **Verify it worked**: 
   - Write this command in the terminal: python3 --version
   - You shall now see a version number.

### Linux (Desbian / Ubuntu)

1. Open the terminal (Ctrl + Alt + T) and write these commands in the terminal:

sudo apt update
sudo apt install python3 python3-pip python3-venv -y

2. **Verify it worked**: 
python3 --version
pip3 --version

You shall now see version numbers for both.

## Step 2: Install Docker

### Windows
1. Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop/)
2. Run the downloaded `Docker Desktop Installer.exe` file
3. Follow the installation wizard with default settings
4. When prompted, ensure "Use WSL 2 instead of Hyper-V" is selected (recommended)
5. Restart your computer when installation completes
6. **Verify it worked**:
   - Open Command Prompt or PowerShell
   - Type: `docker --version`
   - You should see something like `Docker version 24.0.0`

### Mac
1. Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop/)
2. Double-click the downloaded `.dmg` file
3. Drag the Docker icon to your Applications folder
4. Open Docker from your Applications folder
5. Follow the setup instructions and grant necessary permissions
6. **Verify it worked**:
   - Open Terminal
   - Type: `docker --version`
   - You should see the Docker version number

### Linux (Debian/Ubuntu)
1. Open terminal and run these commands:
```bash
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USE
# Linux Setup

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

# Windows Setup

# Mac Setup
