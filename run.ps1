# Convenience run script for PowerShell
Set-Location -Path $PSScriptRoot
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
