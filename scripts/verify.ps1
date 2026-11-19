$ErrorActionPreference = "Continue"
New-Item -ItemType Directory -Force reports, outputs | Out-Null
$python = Join-Path $PSScriptRoot "..\.venv\Scripts\python.exe"
if (-not (Test-Path $python)) { $python = "python" }
$log = @()
foreach ($argsList in @(@("manage.py", "check"), @("manage.py", "makemigrations", "--check", "--dry-run"), @("manage.py", "test", "--verbosity", "2"))) {
    $log += "`n> $python $($argsList -join ' ')"
    $result = & $python @argsList 2>&1
    $exitCode = $LASTEXITCODE
    $log += $result
    if ($exitCode -ne 0) { $log | Set-Content reports/test-report.txt; exit $exitCode }
}
$log | Set-Content reports/test-report.txt
& $python (Join-Path $PSScriptRoot "run_postman_smoke.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Get-Content reports/postman-smoke-report.txt | Add-Content reports/test-report.txt
Copy-Item reports/test-report.txt outputs/test-report.txt -Force
