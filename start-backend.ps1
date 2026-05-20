# 백엔드 1개만 실행 (8000 포트 uvicorn·유령 워커 정리)
Write-Host "기존 uvicorn / Python 워커 종료 중..."

Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
    Where-Object {
        $_.CommandLine -match "uvicorn" -or
        $_.CommandLine -match "multiprocessing\.spawn"
    } |
    ForEach-Object {
        Write-Host "  종료 PID $($_.ProcessId)"
        Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
    }

Start-Sleep -Seconds 2

$port = 8000
$listeners = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
if ($listeners) {
    Write-Host "경고: 포트 $port 가 아직 사용 중입니다. 작업 관리자에서 python.exe를 모두 종료한 뒤 다시 실행하세요."
    $listeners | ForEach-Object { Write-Host "  LISTEN PID $($_.OwningProcess)" }
    exit 1
}

Set-Location $PSScriptRoot
$env:PYTHONPATH = "apps"
Write-Host "백엔드 시작: http://127.0.0.1:$port (이 터미널에 로그가 표시됩니다)"
Write-Host "종료: Ctrl+C"
python -m uvicorn main:app --reload --host 127.0.0.1 --port $port
