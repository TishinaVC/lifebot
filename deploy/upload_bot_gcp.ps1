# Lifebot Upload Script — uploads all bot files to Google Cloud VM
# Usage: .\deploy\upload_bot_gcp.ps1
# (Uses gcloud CLI — no need to know the IP)

param(
    [string]$Zone = "us-central1-a",
    [string]$Instance = "lifebot"
)

$sshKey = "$env:USERPROFILE\.ssh\gcp_lifebot"
$localPath = "c:\Users\jwema\OneDrive\Software Projects\Lifebot"

Write-Host "=== Uploading Lifebot to Google Cloud VM ($Instance in $Zone) ===" -ForegroundColor Cyan

# Get external IP
$ip = gcloud compute instances describe $Instance --zone=$Zone --format='get(networkInterfaces[0].accessConfigs[0].natIP)' 2>$null
if (-not $ip) {
    Write-Host "ERROR: Could not find VM '$Instance' in zone '$Zone'." -ForegroundColor Red
    Write-Host "Make sure gcloud CLI is installed and you've created the VM." -ForegroundColor Yellow
    Write-Host "Run: gcloud compute instances list  to see your VMs." -ForegroundColor Yellow
    exit 1
}

Write-Host "  VM IP: $ip" -ForegroundColor Green
$remotePath = "ubuntu@$ip`:~/lifebot"

# Upload directories
$dirs = @("cogs", "config", "database", "utils", "deploy")
foreach ($dir in $dirs) {
    Write-Host "  Uploading $dir/..." -ForegroundColor Yellow
    scp -i $sshKey -r "$localPath\$dir" $remotePath
}

# Upload root files
$files = @("main.py", "world.py", "requirements.txt", ".env.example")
foreach ($file in $files) {
    $fullPath = "$localPath\$file"
    if (Test-Path $fullPath) {
        Write-Host "  Uploading $file..." -ForegroundColor Yellow
        scp -i $sshKey "$fullPath" $remotePath
    }
}

Write-Host ""
Write-Host "=== Upload Complete! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. SSH in:  gcloud compute ssh $Instance --zone=$Zone"
Write-Host "  2. Edit .env: nano ~/lifebot/.env  (paste your Discord token)"
Write-Host "  3. Run setup: bash ~/lifebot/deploy/setup_gcp.sh"
Write-Host "  4. Start bot: sudo systemctl start lifebot"
Write-Host "  5. Check logs: journalctl -u lifebot -f"
Write-Host ""
Write-Host "Quick restart from PC:"
Write-Host "  gcloud compute ssh $Instance --zone=$Zone --command='sudo systemctl restart lifebot'"
