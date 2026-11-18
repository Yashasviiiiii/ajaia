# Run Backend Tests - PowerShell Script

$ErrorActionPreference = "Stop"
$ROOT = $PSScriptRoot

Write-Host "Running Backend Tests..." -ForegroundColor Cyan

Set-Location $ROOT

# Activate virtual environment
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & ".venv\Scripts\Activate.ps1"
} else {
    Write-Host "Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv .venv
    & ".venv\Scripts\Activate.ps1"
}

# Install dependencies if needed
Write-Host "Installing test dependencies..." -ForegroundColor Yellow
pip install -q -r requirements.txt

# Run tests
Write-Host "`nRunning tests with coverage...`n" -ForegroundColor Green
pytest --cov=app --cov-report=term-missing --cov-report=html

# Show summary
Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Tests completed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "Coverage report: htmlcov\index.html" -ForegroundColor Cyan
