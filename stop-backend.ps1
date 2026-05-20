# 실행 중인 백엔드(uvicorn) 전부 종료
Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
    Where-Object {
        $_.CommandLine -match "uvicorn" -or
        $_.CommandLine -match "multiprocessing\.spawn"
    } |
    ForEach-Object {
        Write-Host "종료 PID $($_.ProcessId)"
        Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
    }
Write-Host "완료. 포트 8000 확인:"
netstat -ano | findstr ":8000"
