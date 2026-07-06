# Run a single backend instance (port 8000, clean stale uvicorn workers)
Write-Host "Stopping existing uvicorn / Python workers..."

Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
    Where-Object {
        $_.CommandLine -match "uvicorn" -or
        $_.CommandLine -match "multiprocessing\.spawn"
    } |
    ForEach-Object {
        Write-Host "  Stopping PID $($_.ProcessId)"
        Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
    }

Start-Sleep -Seconds 2

$port = 8000
$listeners = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
if ($listeners) {
    Write-Host "Warning: port $port is still in use. End all python.exe processes in Task Manager, then retry."
    $listeners | ForEach-Object { Write-Host "  LISTEN PID $($_.OwningProcess)" }
    exit 1
}

Set-Location $PSScriptRoot
$env:PYTHONPATH = ".;apps"
$env:PYTHONIOENCODING = "utf-8"
$env:KMP_DUPLICATE_LIB_OK = "TRUE"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null
Write-Host "Starting backend: http://127.0.0.1:$port (logs appear in this terminal)"
Write-Host "Stop: Ctrl+C"
python main.py
