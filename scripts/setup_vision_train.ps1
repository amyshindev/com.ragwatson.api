# Vision YOLO face training setup (GPU auto-detect)
# C: 용량 부족(~3GB)이면 backend/scripts/setup_vision_gpu.ps1 (D: venv) 사용
$ErrorActionPreference = "Stop"
$backend = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $backend

$env:TMP = if (Test-Path "D:\") { "D:\pip-tmp" } else { $env:TEMP }
$env:TEMP = $env:TMP
New-Item -ItemType Directory -Force -Path $env:TMP -ErrorAction SilentlyContinue | Out-Null

Write-Host "Installing CUDA PyTorch (cu126) + vision train dependencies..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126 -q
pip install "ultralytics>=8.3.0" "PyYAML>=6.0" "Pillow>=10.0.0" -q

Write-Host "Verifying GPU..."
python -c "import torch; print('torch', torch.__version__); print('cuda', torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no gpu')"

$env:PYTHONPATH = Join-Path $backend "apps"
$env:KMP_DUPLICATE_LIB_OK = "TRUE"
Set-Location $backend

Write-Host "Preparing yolo_train -> prepared_face_yolo..."
python -m vision.adapter.inbound.cli.face_detector_cli prepare --force

Write-Host ""
Write-Host "Done. Train (device=auto picks GPU when available):"
Write-Host "  python -m vision.adapter.inbound.cli.face_detector_cli train --epochs 10"
Write-Host "  python -m vision.adapter.inbound.cli.face_detector_cli train --epochs 10 --device 0 --batch 16"
