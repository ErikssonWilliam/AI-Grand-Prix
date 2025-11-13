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
  
### Step 5: Install VcXsrv (X Server for Windows)

1. Download VcXsrv from [sourceforge.net/projects/vcxsrv/](https://sourceforge.net/projects/vcxsrv/)
2. Run the installer and follow the setup wizard
3. After installation, launch "XLaunch" from Start Menu
4. Use these settings:
   - "Multiple windows"
   - Start no client
   - Check "Disable access control"
   - Finish
  
# Running the game

## Running the Game (Linux)

### Step 1: Fork and Clone the Repository

1. Go to the [AI Grand Prix repository](https://github.com/ErikssonWilliam/AI-Grand-Prix)
2. Click the "Fork" button in the top-right corner to create your own copy
3. Open terminal and clone your forked repository, replace YourUsername with the actual name:
```bash
git clone https://github.com/YourUsername/AI-Grand-Prix.git
cd AI-Grand-Prix
```

### Step 2: Setup a python virtual environment
1. Create the environment
```bash
python3 -m venv .venv
```
2. Activate the environment
```bash
.venv\Scripts\activate
```
Your terminal prompt should now show (venv) at the beginning

3. Move into the python-server folder
```bash
cd python-server
```
4. Install correct python packages
```bash
pip install -r requirements.txt
```

5. Move out to the root again
```bash
cd ..
```

### Step 3: Run the game

```bash
setup.bat
```

[← Back to Main README](README.md)
