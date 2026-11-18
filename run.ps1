# Collaborative Document App - PowerShell Launcher

$ROOT = $PSScriptRoot

Write-Host "Setting up and starting the application..." -ForegroundColor Cyan

# --- Backend setup ---
Write-Host "`nBackend setup..." -ForegroundColor Yellow
Set-Location "$ROOT\backend"

if (-not (Test-Path ".venv")) {
    Write-Host "Creating Python virtual environment..."
    python -m venv .venv
}

Write-Host "Activating virtual environment..."
& ".venv\Scripts\Activate.ps1"

Write-Host "Installing Python dependencies..."
pip install -q -r requirements.txt

# --- Frontend setup ---
Write-Host "`nFrontend setup..." -ForegroundColor Yellow
Set-Location "$ROOT\frontend"

# Check if key dependencies are installed
$needInstall = $false
if (-not (Test-Path "node_modules")) {
    $needInstall = $true
} elseif (-not (Test-Path "node_modules\@tiptap\extension-table")) {
    Write-Host "Missing dependencies detected..."
    $needInstall = $true
}

if ($needInstall) {
    Write-Host "Installing npm dependencies..."
    npm install
}

# --- Start both servers ---
Write-Host "`n" -NoNewline
Write-Host "========================================" -ForegroundColor Green
Write-Host "  App: http://localhost:5173" -ForegroundColor Green
Write-Host "  API: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "Login credentials:" -ForegroundColor Cyan
Write-Host "  alice@example.com / password123"
Write-Host "  bob@example.com / password123"
Write-Host "  carol@example.com / password123"
Write-Host "`nPress Ctrl+C to stop both servers`n" -ForegroundColor Yellow

# Create cleanup function
$cleanup = {
    Write-Host "`n`nStopping servers..." -ForegroundColor Yellow
    Get-Job | Stop-Job -PassThru | Remove-Job -Force
    Write-Host "Servers stopped." -ForegroundColor Green
    exit
}

# Register cleanup on Ctrl+C
Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action $cleanup | Out-Null
[Console]::TreatControlCAsInput = $false

# Start backend in background
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ROOT\backend'; .\.venv\Scripts\Activate.ps1; uvicorn app.main:app --reload --port 8000" -WindowStyle Normal

# Start frontend in background  
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ROOT\frontend'; npm run dev" -WindowStyle Normal

Write-Host "Servers started in separate windows." -ForegroundColor Green
Write-Host "Close those windows or press Ctrl+C here to stop." -ForegroundColor Yellow

# Wait for user to press Ctrl+C
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
}
finally {
    & $cleanup
}
