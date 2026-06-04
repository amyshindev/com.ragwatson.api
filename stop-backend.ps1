# Stop all running backend (uvicorn) processes
Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
    Where-Object {
        $_.CommandLine -match "uvicorn" -or
        $_.CommandLine -match "multiprocessing\.spawn"
    } |
    ForEach-Object {
        Write-Host "Stopping PID $($_.ProcessId)"
        Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
    }
Write-Host "Done. Checking port 8000:"
netstat -ano | findstr ":8000"
