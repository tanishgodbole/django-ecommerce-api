"""Execute collection GET requests and equivalent status/JSON assertions."""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.pop("SSLKEYLOGFILE", None)
collection = json.loads((ROOT / "postman/commerce-api.postman_collection.json").read_text(encoding="utf-8"))
base = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:8000"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
lines = [f"Collection: {collection['info']['name']}", f"Base URL: {base}", f"Requests: {len(collection['item'])}", ""]
passed = 0
for index, item in enumerate(collection["item"], 1):
    url = item["request"]["url"].replace("{{baseUrl}}", base)
    try:
        with opener.open(url, timeout=10) as response:
            body = response.read()
            json.loads(body)
            ok = response.status == 200
            detail = f"HTTP {response.status}; valid JSON"
    except urllib.error.HTTPError as error:
        ok, detail = False, f"HTTP {error.code}"
    except Exception as error:
        ok, detail = False, f"{type(error).__name__}: {error}"
    passed += int(ok)
    lines.append(f"{'PASS' if ok else 'FAIL'} {index:03d} {item['name']} — {detail}")
lines += ["", f"Result: {passed}/{len(collection['item'])} passed; {len(collection['item']) - passed} failed."]
report = "\n".join(lines) + "\n"
(ROOT / "reports").mkdir(exist_ok=True)
(ROOT / "reports/postman-smoke-report.txt").write_text(report, encoding="utf-8")
print(report)
if passed != len(collection["item"]):
    raise SystemExit(1)
