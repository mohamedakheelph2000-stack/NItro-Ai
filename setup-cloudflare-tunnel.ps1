# ============================================================================
# Cloudflare Tunnel Setup Helper for Nitro AI
# ============================================================================
# This script helps you set up Cloudflare Tunnel for public access
# Run in PowerShell as Administrator

Write-Host "`n" -NoNewline
Write-Host "╔═══════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🌐 Cloudflare Tunnel Setup for Nitro AI           ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host "`n"

# Configuration
$TunnelName = "nitro-ai"
$LocalService = "http://localhost:8000"
$ConfigDir = "$env:USERPROFILE\.cloudflared"

# ============================================================================
# Step 1: Check if running as Administrator
# ============================================================================
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "⚠️  This script requires Administrator privileges" -ForegroundColor Yellow
    Write-Host "   Right-click PowerShell and select 'Run as Administrator'`n" -ForegroundColor Gray
    Read-Host "Press Enter to exit"
    exit
}

# ============================================================================
# Step 2: Check if cloudflared is installed
# ============================================================================
Write-Host "🔍 Checking for cloudflared installation..." -ForegroundColor Cyan

try {
    $version = cloudflared --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Cloudflared is installed: $version`n" -ForegroundColor Green
    } else {
        throw "Not installed"
    }
} catch {
    Write-Host "❌ Cloudflared not found`n" -ForegroundColor Red
    Write-Host "📦 Installing cloudflared via winget..." -ForegroundColor Yellow
    
    try {
        winget install --id Cloudflare.cloudflared --silent --accept-package-agreements --accept-source-agreements
        Write-Host "✅ Cloudflared installed successfully!`n" -ForegroundColor Green
        
        # Refresh PATH
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    } catch {
        Write-Host "❌ Installation failed. Please install manually from:" -ForegroundColor Red
        Write-Host "   https://github.com/cloudflare/cloudflared/releases`n" -ForegroundColor Gray
        Read-Host "Press Enter to exit"
        exit
    }
}

# ============================================================================
# Step 3: Login to Cloudflare
# ============================================================================
Write-Host "🔐 Cloudflare Login" -ForegroundColor Cyan
Write-Host "   This will open your browser for authentication`n" -ForegroundColor Gray

if (Test-Path "$ConfigDir\cert.pem") {
    Write-Host "✅ Already logged in (cert.pem found)`n" -ForegroundColor Green
} else {
    Read-Host "Press Enter to open browser and login"
    
    try {
        cloudflared tunnel login
        if (Test-Path "$ConfigDir\cert.pem") {
            Write-Host "✅ Login successful!`n" -ForegroundColor Green
        } else {
            Write-Host "❌ Login failed. Please try manually:`n   cloudflared tunnel login`n" -ForegroundColor Red
            Read-Host "Press Enter to exit"
            exit
        }
    } catch {
        Write-Host "❌ Login error: $_`n" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit
    }
}

# ============================================================================
# Step 4: Create Tunnel
# ============================================================================
Write-Host "🏗️  Creating Tunnel: $TunnelName" -ForegroundColor Cyan

# Check if tunnel already exists
$existingTunnel = cloudflared tunnel list 2>&1 | Select-String -Pattern $TunnelName

if ($existingTunnel) {
    Write-Host "✅ Tunnel '$TunnelName' already exists`n" -ForegroundColor Green
    
    # Extract tunnel ID
    $tunnelInfo = cloudflared tunnel list 2>&1 | Select-String -Pattern $TunnelName
    $TunnelID = ($tunnelInfo -split '\s+')[0]
} else {
    try {
        $createOutput = cloudflared tunnel create $TunnelName 2>&1
        Write-Host $createOutput
        
        # Extract tunnel ID from output
        $tunnelListOutput = cloudflared tunnel list 2>&1 | Select-String -Pattern $TunnelName
        $TunnelID = ($tunnelListOutput -split '\s+')[0]
        
        Write-Host "✅ Tunnel created successfully!" -ForegroundColor Green
        Write-Host "   Tunnel ID: $TunnelID`n" -ForegroundColor Gray
    } catch {
        Write-Host "❌ Failed to create tunnel: $_`n" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit
    }
}

# ============================================================================
# Step 5: Get Domain Name
# ============================================================================
Write-Host "🌍 Domain Configuration" -ForegroundColor Cyan
Write-Host "   Enter your domain/subdomain for public access`n" -ForegroundColor Gray

$Domain = Read-Host "   Your domain (e.g., nitro-ai.example.com)"

if ([string]::IsNullOrWhiteSpace($Domain)) {
    Write-Host "❌ Domain is required`n" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit
}

# ============================================================================
# Step 6: Create Config File
# ============================================================================
Write-Host "`n📝 Creating configuration file..." -ForegroundColor Cyan

$ConfigFile = "$ConfigDir\config.yml"
$CredentialsFile = "$ConfigDir\$TunnelID.json"

# Verify credentials file exists
if (-not (Test-Path $CredentialsFile)) {
    Write-Host "❌ Credentials file not found: $CredentialsFile" -ForegroundColor Red
    Write-Host "   Please create tunnel manually: cloudflared tunnel create $TunnelName`n" -ForegroundColor Gray
    Read-Host "Press Enter to exit"
    exit
}

# Create config.yml
$ConfigContent = @"
# Cloudflare Tunnel Configuration for Nitro AI
# Auto-generated by setup script

tunnel: $TunnelID
credentials-file: $CredentialsFile

ingress:
  # Route your domain to localhost:8000 (Nitro AI backend)
  - hostname: $Domain
    service: $LocalService
    originRequest:
      noTLSVerify: true
  
  # Catch-all rule (required)
  - service: http_status:404
"@

$ConfigContent | Out-File -FilePath $ConfigFile -Encoding UTF8 -Force
Write-Host "✅ Configuration file created: $ConfigFile`n" -ForegroundColor Green

# ============================================================================
# Step 7: Route DNS
# ============================================================================
Write-Host "🗺️  Configuring DNS routing..." -ForegroundColor Cyan

try {
    cloudflared tunnel route dns $TunnelName $Domain 2>&1
    Write-Host "✅ DNS configured successfully!" -ForegroundColor Green
    Write-Host "   $Domain → Tunnel: $TunnelName`n" -ForegroundColor Gray
} catch {
    Write-Host "⚠️  DNS routing may already be configured or failed" -ForegroundColor Yellow
    Write-Host "   Check Cloudflare dashboard to verify`n" -ForegroundColor Gray
}

# ============================================================================
# Step 8: Generate API Key
# ============================================================================
Write-Host "🔑 Generating secure API key..." -ForegroundColor Cyan

$ApiKey = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
$ApiKeyBase64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($ApiKey))

Write-Host "✅ API Key generated!`n" -ForegroundColor Green
Write-Host "   API Key: " -NoNewline -ForegroundColor Gray
Write-Host $ApiKeyBase64 -ForegroundColor Yellow
Write-Host "`n   ⚠️  SAVE THIS KEY - You'll need it for .env and config.js`n" -ForegroundColor Red

# ============================================================================
# Step 9: Update Configuration Files
# ============================================================================
Write-Host "📝 Configuration Instructions" -ForegroundColor Cyan
Write-Host "   You need to update these files manually:`n" -ForegroundColor Gray

Write-Host "   1️⃣  Edit C:\Nitro AI\backend\.env:" -ForegroundColor White
Write-Host "      CLOUDFLARE_TUNNEL_DOMAIN=https://$Domain" -ForegroundColor Yellow
Write-Host "      ALLOWED_ORIGINS=http://localhost:3000,https://$Domain" -ForegroundColor Yellow
Write-Host "      ENABLE_API_KEY=True" -ForegroundColor Yellow
Write-Host "      API_KEY=$ApiKeyBase64" -ForegroundColor Yellow
Write-Host "      ENABLE_RATE_LIMIT=True`n" -ForegroundColor Yellow

Write-Host "   2️⃣  Edit C:\Nitro AI\frontend\config.js:" -ForegroundColor White
Write-Host "      CLOUDFLARE_TUNNEL_URL: 'https://$Domain'," -ForegroundColor Yellow
Write-Host "      API_KEY: '$ApiKeyBase64',`n" -ForegroundColor Yellow

# ============================================================================
# Step 10: Test Backend
# ============================================================================
Write-Host "🧪 Testing local backend..." -ForegroundColor Cyan

try {
    $healthCheck = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 3
    if ($healthCheck.StatusCode -eq 200) {
        Write-Host "✅ Backend is running on localhost:8000`n" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Backend not running on localhost:8000" -ForegroundColor Yellow
    Write-Host "   Make sure to start your backend before running the tunnel`n" -ForegroundColor Gray
}

# ============================================================================
# Step 11: Install as Service (Optional)
# ============================================================================
Write-Host "🔧 Install Tunnel as Windows Service?" -ForegroundColor Cyan
Write-Host "   This will run the tunnel automatically on system startup`n" -ForegroundColor Gray

$installService = Read-Host "   Install as service? (Y/N)"

if ($installService -eq "Y" -or $installService -eq "y") {
    try {
        cloudflared service install
        Write-Host "✅ Service installed!" -ForegroundColor Green
        
        Start-Service cloudflared
        Write-Host "✅ Service started!`n" -ForegroundColor Green
        
        Set-Service -Name cloudflared -StartupType Automatic
        Write-Host "✅ Auto-start enabled`n" -ForegroundColor Green
    } catch {
        Write-Host "❌ Service installation failed: $_" -ForegroundColor Red
        Write-Host "   You can try manually: cloudflared service install`n" -ForegroundColor Gray
    }
} else {
    Write-Host "⏭️  Skipped service installation`n" -ForegroundColor Gray
}

# ============================================================================
# Summary
# ============================================================================
Write-Host "`n" -NoNewline
Write-Host "╔═══════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║            ✅ Setup Complete!                        ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════╝" -ForegroundColor Green

Write-Host "`n📋 Next Steps:`n" -ForegroundColor Cyan

Write-Host "1. Update backend .env with the configuration above" -ForegroundColor White
Write-Host "2. Update frontend config.js with the API key" -ForegroundColor White
Write-Host "3. Restart your backend server" -ForegroundColor White
Write-Host "4. Start the tunnel (if not running as service):`n" -ForegroundColor White
Write-Host "   cloudflared tunnel run $TunnelName`n" -ForegroundColor Yellow

Write-Host "5. Test public access:" -ForegroundColor White
Write-Host "   https://$Domain`n" -ForegroundColor Yellow

Write-Host "📖 Full Guide: C:\Nitro AI\CLOUDFLARE_TUNNEL_GUIDE.md`n" -ForegroundColor Cyan

Write-Host "🎉 Your Nitro AI will be accessible from anywhere!`n" -ForegroundColor Green

Read-Host "Press Enter to exit"
