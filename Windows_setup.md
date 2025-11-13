# Windows Setup Guide

## Step 1: Install Python

1. Download Python 3.8 or newer from [python.org](https://www.python.org/downloads/)
2. Click on "download python" and run the downloaded file (it will be called something like `python-3.11.0.exe`)
3. **Important**: Check the box "Add Python to PATH" at the bottom of the first screen
4. Click "Install Now" and wait for completion
5. **Verify it worked**: 
   - Press `Windows Key + R`, type `cmd`, press Enter
   - In the black window, type: `python --version`
   - You should see something like `Python 3.11.0`

## Step 2: Install Docker

1. Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop/)
2. Run the downloaded `Docker Desktop Installer.exe` file
3. Follow the installation wizard with default settings
4. When prompted, ensure "Use WSL 2 instead of Hyper-V" is selected (recommended)
5. Restart your computer when installation completes
6. **Verify it worked**:
   - Press `Windows Key + R`, type `cmd`, press Enter
   - In the black window, type: `docker --version`
   - You should see something like `Docker version 24.0.0`

## Step 3: Install Git

1. Download Git from [git-scm.com](https://git-scm.com/)
2. Run the downloaded `.exe` file (it will be called something like `Git-2.40.0-64-bit.exe`)
3. Follow the setup wizard with these settings:
   - Select "Use Git from the command line and also from 3rd-party software"
   - Choose "Checkout Windows-style, commit Unix-style line endings"
   - Use Windows' default console window
4. Click "Install" and wait for completion
5. **Verify it worked**:
   - Press `Windows Key + R`, type `cmd`, press Enter
   - In the black window, type: `git --version`
   - You should see something like `git version 2.40.0`

## Step 4: Install VS Code

1. Download VS Code from [code.visualstudio.com](https://code.visualstudio.com/)
2. Run the downloaded `.exe` file (it will be called something like `VSCodeUserSetup-x64-1.80.0.exe`)
3. Follow the installation wizard
4. **Important**: Check the box "Add to PATH" during installation
5. Click "Install" and wait for completion
6. **Verify it worked**:
   - Press `Windows Key + R`, type `cmd`, press Enter
   - In the black window, type: `code --version`
   - You should see something like `1.80.0`

[← Back to Main README](README.md)
