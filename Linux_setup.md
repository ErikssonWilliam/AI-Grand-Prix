## Step 1: Install Python

1. Open the terminal (Ctrl + Alt + T) and write these commands in the terminal:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

2. **Verify it worked**:
```bash
python3 --version
pip3 --version
```

You shall now see version numbers for both.

## Step 2: Install docker
1. Open terminal and run these commands:
```bash
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USE
```

2. Log out and log back in for the changes to take place.

3. **Verify it worked**:
```bash
  docker --version
```

You shall now see a version number.

## Step 3: Install Git

1. Open the terminal (Ctrl + Alt + T) and write these commands in the terminal:
```bash
sudo apt update
sudo apt install git -y
```

2. **Verify it worked**:
```bash
  git --version
```

You shall now see a version number.

## Step 4: Install VS Code

1. Open the terminal (Ctrl + Alt + T) and write this command in the terminal:
```bash
sudo snap install --classic code
```

2. **Verify it worked**:
```bash
  code --version
```

You shall now see a version number.
