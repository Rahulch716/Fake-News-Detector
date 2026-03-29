$ports = @(8000, 5000)

foreach ($port in $ports) {
    Write-Host "Checking port $port..."

    $connections = netstat -ano | findstr :$port

    if ($connections) {
        $pids = $connections | ForEach-Object {
            ($_ -split "\s+")[-1]
        } | Sort-Object -Unique

        foreach ($pid in $pids) {
            Write-Host "Killing PID $pid on port $port"
            taskkill /PID $pid /F
        }
    } else {
        Write-Host "Port $port is free"
    }
}

Write-Host "Done!"