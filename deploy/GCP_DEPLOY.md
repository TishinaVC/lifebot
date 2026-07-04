# Lifebot — Google Cloud Free Tier Deployment Guide

## Prerequisites
- Google account (Gmail — you already have this)
- Google Cloud CLI (gcloud) — download from https://cloud.google.com/sdk/docs/install
- Your Discord bot token (from https://discord.com/developers/applications)

## Step 1: Install Google Cloud CLI

1. Download from https://cloud.google.com/sdk/docs/install
2. Run the installer
3. Open a terminal and run:
   ```
   gcloud init
   ```
4. Sign in with your Google account when the browser opens
5. Create or select a project (name it `lifebot` if creating new)

## Step 2: Enable Compute Engine

```powershell
gcloud services enable compute.googleapis.com
```

## Step 3: Add Your SSH Key to GCP

```powershell
gcloud compute os-login ssh-keys add --key-file="C:\Users\jwema\.ssh\gcp_lifebot.pub"
```

## Step 4: Create the Always-Free VM

```powershell
gcloud compute instances create lifebot `
  --zone=us-central1-a `
  --machine-type=e2-micro `
  --image-family=ubuntu-2204-lts `
  --image-project=ubuntu-os-cloud `
  --boot-disk-size=30GB `
  --boot-disk-type=pd-standard `
  --metadata=ssh-keys="ubuntu:ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGoK8XnokyIaF1nlnrJYB5GxDelv7aBwJhnmggxQBUZU lifebot-gcp"
```

This creates an **e2-micro** (1 vCPU, 1GB RAM) in `us-central1-a` — always free tier.

## Step 5: SSH Into the VM

```powershell
gcloud compute ssh lifebot --zone=us-central1-a
```

**OR** using the SSH key directly:

```powershell
ssh -i C:\Users\jwema\.ssh\gcp_lifebot ubuntu@VM_EXTERNAL_IP
```

Find the external IP with:
```powershell
gcloud compute instances describe lifebot --zone=us-central1-a --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
```

## Step 6: Run Setup Script on the VM

After SSH'ing in:

```bash
cd ~
curl -sL https://raw.githubusercontent.com/YOUR_USER/lifebot/main/deploy/setup_gcp.sh | bash
```

**OR** upload first, then run (see Step 7).

## Step 7: Upload Bot Code

From PowerShell on your PC:

```powershell
.\deploy\upload_bot_gcp.ps1
```

This uploads everything to the VM. Then SSH in and run setup:

```powershell
gcloud compute ssh lifebot --zone=us-central1-a
```

```bash
cd ~/lifebot
chmod +x deploy/setup_gcp.sh
bash deploy/setup_gcp.sh
```

## Step 8: Add Your Bot Token

On the VM:

```bash
nano ~/lifebot/.env
```

Replace `YOUR_TOKEN_HERE` with your actual Discord bot token.
Save: `Ctrl+O`, `Enter`, `Ctrl+X`

## Step 9: Start the Bot

```bash
sudo systemctl start lifebot
sudo systemctl status lifebot
```

You should see `active (running)`. Check logs:

```bash
journalctl -u lifebot -f
```

## Step 10: Verify in Discord

Your bot should show online. Try `/help` in your server.

---

## Managing the Bot

| Action | Command |
|--------|---------|
| Start | `sudo systemctl start lifebot` |
| Stop | `sudo systemctl stop lifebot` |
| Restart | `sudo systemctl restart lifebot` |
| Status | `sudo systemctl status lifebot` |
| View logs | `journalctl -u lifebot -f` |
| View last 50 lines | `journalctl -u lifebot -n 50` |

## Updating the Bot

From PowerShell on your PC:

```powershell
.\deploy\upload_bot_gcp.ps1
```

Then on the VM (or via gcloud):

```bash
sudo systemctl restart lifebot
```

One-liner restart from PC:

```powershell
gcloud compute ssh lifebot --zone=us-central1-a --command="sudo systemctl restart lifebot"
```

## Backup the Database

```powershell
gcloud compute scp lifebot:~/lifebot/lifebot.db "c:\Users\jwema\OneDrive\Software Projects\Lifebot\lifebot_backup.db" --zone=us-central1-a
```

## SSH Key Files

- **Private key**: `C:\Users\jwema\.ssh\gcp_lifebot` (keep secret)
- **Public key**: `C:\Users\jwema\.ssh\gcp_lifebot.pub`

## Quick Reference — All gcloud Commands

```powershell
# Create VM
gcloud compute instances create lifebot --zone=us-central1-a --machine-type=e2-micro --image-family=ubuntu-2204-lts --image-project=ubuntu-os-cloud --boot-disk-size=30GB --boot-disk-type=pd-standard

# Get IP
gcloud compute instances describe lifebot --zone=us-central1-a --format='get(networkInterfaces[0].accessConfigs[0].natIP)'

# SSH in
gcloud compute ssh lifebot --zone=us-central1-a

# Restart bot remotely
gcloud compute ssh lifebot --zone=us-central1-a --command="sudo systemctl restart lifebot"

# Check status remotely
gcloud compute ssh lifebot --zone=us-central1-a --command="sudo systemctl status lifebot"

# View logs remotely
gcloud compute ssh lifebot --zone=us-central1-a --command="journalctl -u lifebot -n 50"

# Stop VM (saves resources, bot goes offline)
gcloud compute instances stop lifebot --zone=us-central1-a

# Start VM
gcloud compute instances start lifebot --zone=us-central1-a
```

## Troubleshooting

**Can't SSH in?**
- Try: `gcloud compute ssh lifebot --zone=us-central1-a` (gcloud handles keys automatically)
- Check VM is running: `gcloud compute instances list`

**Bot won't start?**
- Check logs: `journalctl -u lifebot -n 50`
- Verify .env: `cat ~/lifebot/.env`
- Run manually to see errors: `~/lifebot/venv/bin/python ~/lifebot/main.py`

**Out of memory?**
- e2-micro has 1GB RAM. If bot crashes with OOM, create a swap file:
  ```bash
  sudo fallocate -l 1G /swapfile
  sudo chmod 600 /swapfile
  sudo mkswap /swapfile
  sudo swapon /swapfile
  echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
  ```

**Need static IP?**
```powershell
gcloud compute addresses create lifebot-ip --region=us-central1
gcloud compute instances add-access-config lifebot --zone=us-central1-a --address=<RESERVED_IP>
```
