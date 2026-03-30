$ips = @(
    "0.0.0.0",
    "1.1.1.1",
    "8.8.8.8"
)

$ports = @(80, 8000, 8080, 8888, 25565)

foreach ($ip in $ips) {
    Write-Host "Checking $ip..." -ForegroundColor Cyan

    foreach ($port in $ports) {
        $result = Test-NetConnection -ComputerName $ip -Port $port -WarningAction SilentlyContinue

        if ($result.TcpTestSucceeded) {
            Write-Host "  Port $port OPEN" -ForegroundColor Green
        }
        else {
            Write-Host "  Port $port CLOSED" -ForegroundColor DarkGray
        }
    }

    Write-Host ""
}
Read-Host -Prompt "Press Enter to exit"
