# CUDA PyTorch + YOLO 학습 — C: 용량 부족 시 D: venv 사용
$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$backend = Join-Path $repoRoot "backend"
$venvRoot = if ($env:VISION_VENV) { $env:VISION_VENV } else { "D:\ragwatson-vision-venv" }

Write-Host "Vision GPU venv: $venvRoot"
New-Item -ItemType Directory -Force -Path $venvRoot | Out-Null

$env:TMP = "D:\pip-tmp"
$env:TEMP = "D:\pip-tmp"
New-Item -ItemType Directory -Force -Path $env:TMP, "D:\pip-cache" | Out-Null

$py = Join-Path $venvRoot "Scripts\python.exe"
if (-not (Test-Path $py)) {
    Write-Host "Creating venv on D: ..."
    python -m venv $venvRoot
}

Write-Host "Installing CUDA PyTorch (cu126) into venv..."
& $py -m pip install --upgrade pip
& $py -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126 --cache-dir D:\pip-cache
& $py -m pip install "ultralytics>=8.3.0" "PyYAML>=6.0" "Pillow>=10.0.0"

Write-Host "CUDA check:"
& $py -c "import torch; print('torch', torch.__version__); print('cuda', torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no gpu')"

$env:PYTHONPATH = Join-Path $backend "apps"
$env:KMP_DUPLICATE_LIB_OK = "TRUE"
Set-Location $backend

Write-Host "Preparing dataset..."
& $py -m vision.adapter.inbound.cli.face_detector_cli prepare --force

Write-Host ""
Write-Host "Train (GPU auto):"
Write-Host "  `$env:PYTHONPATH = '$($env:PYTHONPATH)'"
Write-Host "  & '$py' -m vision.adapter.inbound.cli.face_detector_cli train --epochs 10 --device auto --batch 16"
