$BinDir = Join-Path $PWD "bin"
$UserPath = [Environment]::GetEnvironmentVariable("PATH", "User")

if ($UserPath -notlike "*$BinDir*") {
    $NewPath = "$UserPath;$BinDir"
    [Environment]::SetEnvironmentVariable("PATH", $NewPath, "User")
    Write-Host "✅ Da them $BinDir vao bien moi truong PATH cua Windows (User level)." -ForegroundColor Green
} else {
    Write-Host "⚡ PATH da ton tai san thư muc bin, bo qua." -ForegroundColor Yellow
}

Write-Host "🎉 Cai dat hoan tat! Vui long dong va mo lai cua so PowerShell/CMD de ap dung." -ForegroundColor Cyan
