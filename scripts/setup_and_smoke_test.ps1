param(
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = "Stop"

function Start-Step {
    param(
        [string]$Message,
        [scriptblock]$Action
    )

    Write-Host "`n==> $Message" -ForegroundColor Cyan
    & $Action
}

$condaExe = Join-Path $env:USERPROFILE "anaconda3\Scripts\conda.exe"
if (-not (Test-Path $condaExe)) {
    $condaCmd = Get-Command conda -ErrorAction SilentlyContinue
    if ($condaCmd) {
        $condaExe = $condaCmd.Source
    } else {
        throw "Conda not found. Install Anaconda/Miniconda or update conda path in this script."
    }
}

$envPath = Join-Path $ProjectRoot ".conda"

Start-Step "Ensuring project Conda environment exists at $envPath" {
    if (-not (Test-Path $envPath)) {
        & $condaExe create -p $envPath python=3.11 -y
    } else {
        Write-Host "Environment already exists. Skipping create."
    }
}

Start-Step "Installing Python dependencies" {
    & $condaExe run -p $envPath --no-capture-output python -m pip install --upgrade pip
    & $condaExe run -p $envPath --no-capture-output python -m pip install -r (Join-Path $ProjectRoot "requirements.txt") numpy scipy
}

Start-Step "Running PCA smoke test" {
    Push-Location (Join-Path $ProjectRoot "demo")
    try {
        & $condaExe run -p $envPath --no-capture-output python project_pca_baseline.py
    } finally {
        Pop-Location
    }
}

Start-Step "Generating model comparison report" {
    Push-Location (Join-Path $ProjectRoot "demo")
    try {
        & $condaExe run -p $envPath --no-capture-output python project_model_comparison_report.py
    } finally {
        Pop-Location
    }
}

Write-Host "`nSetup and smoke test completed successfully." -ForegroundColor Green
