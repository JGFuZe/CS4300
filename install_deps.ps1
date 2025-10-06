# install_in_active_venv.ps1
param(
  [switch]$WithDjangoBootstrap5,   # pip-install django-bootstrap5
  [switch]$WithBootstrapNpm,       # npm i bootstrap@5 @popperjs/core
  [switch]$ShowBootstrapCdn        # print CDN snippet
)

$ErrorActionPreference = "Stop"

# 0) Ensure we're inside an active venv
if (-not $env:VIRTUAL_ENV) {
  throw "No virtual environment detected. Activate your venv first, then run this script."
}

Write-Host "Using active venv: $env:VIRTUAL_ENV" -ForegroundColor Cyan
python -V
python -m pip -V

# 1) Build requirements (adds gyp-next; your existing pins are kept)
$requirements = @"
asgiref==3.7.2
Django==4.2.11
gyp-next==0.17.0
iniconfig==2.1.0
numpy==2.3.3
packaging==25.0
pluggy==1.6.0
Pygments==2.19.2
pytest==8.4.2
pytz==2024.1
setuptools==68.1.2
six==1.16.0
sqlparse==0.4.4
"@.Trim()

# Optionally add django-bootstrap5 (unpinned to avoid version conflicts;
# pin it later if you want exact reproducibility)
if ($WithDjangoBootstrap5) {
  $requirements = ($requirements + "`ndjango-bootstrap5")
}

# 2) Write requirements.txt next to this script
$requirementsPath = Join-Path $PSScriptRoot "requirements.txt"
$requirements | Set-Content -Path $requirementsPath -Encoding ASCII
Write-Host "Wrote $requirementsPath" -ForegroundColor DarkGray

# 3) Upgrade pip toolchain inside the venv
python -m pip install --upgrade pip wheel

# If you hit build issues (e.g., with numpy on some machines), uncomment:
# python -m pip install --upgrade "setuptools>=70"

# 4) Install Python deps
python -m pip install -r $requirementsPath --no-cache-dir


# 7) Show final installed Python packages
Write-Host "`n---- INSTALLED (pip freeze) ----" -ForegroundColor Green
python -m pip freeze
