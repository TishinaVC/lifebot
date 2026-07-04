#!/bin/bash
# Lifebot Google Cloud Setup Script
# Run this on the GCP VM after SSH'ing in
set -e

echo "=== Lifebot Google Cloud Setup ==="

# Install Python and dependencies
echo "[1/7] Installing system packages..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git sqlite3

# Add swap (e2-micro only has 1GB RAM)
echo "[2/7] Setting up 1GB swap (e2-micro has limited RAM)..."
if [ ! -f /swapfile ]; then
    sudo fallocate -l 1G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    echo "  Swap enabled."
else
    echo "  Swap already exists, skipping."
fi

# Create bot directory
echo "[3/7] Creating bot directory..."
mkdir -p ~/lifebot
cd ~/lifebot

# Set up virtual environment
echo "[4/7] Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "[5/7] Installing Python dependencies..."
pip install --upgrade pip
pip install discord.py aiosqlite python-dotenv

# Create .env from example if it doesn't exist
if [ ! -f .env ]; then
    echo "[6/7] Creating .env file..."
    cat > .env << 'ENVEOF'
DISCORD_TOKEN=YOUR_TOKEN_HERE
DB_PATH=/home/ubuntu/lifebot/lifebot.db
PREFIX=!
ENVEOF
    echo "  -> Edit /home/ubuntu/lifebot/.env with your bot token!"
else
    echo "[6/7] .env already exists, skipping."
fi

# Create systemd service
echo "[7/7] Setting up systemd service..."
sudo tee /etc/systemd/system/lifebot.service > /dev/null << 'SVCEOF'
[Unit]
Description=Lifebot Discord Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/lifebot
ExecStart=/home/ubuntu/lifebot/venv/bin/python /home/ubuntu/lifebot/main.py
Restart=always
RestartSec=10
Environment=PYTHONUNBUFFERED=1
MemoryMax=800M

[Install]
WantedBy=multi-user.target
SVCEOF

sudo systemctl daemon-reload
sudo systemctl enable lifebot

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "Next steps:"
echo "  1. Edit .env: nano ~/lifebot/.env  (paste your Discord bot token)"
echo "  2. Start the bot: sudo systemctl start lifebot"
echo "  3. Check status: sudo systemctl status lifebot"
echo "  4. View logs: journalctl -u lifebot -f"
echo ""
echo "To update the bot later:"
echo "  Re-run upload script from PC, then: sudo systemctl restart lifebot"
