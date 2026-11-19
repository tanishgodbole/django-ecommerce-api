$ErrorActionPreference = "Continue"
New-Item -ItemType Directory -Force reports | Out-Null
python manage.py check 2>&1 | Tee-Object -FilePath reports/test-report.txt
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python manage.py test --verbosity 2 2>&1 | Tee-Object -FilePath reports/test-report.txt -Append
exit $LASTEXITCODE
