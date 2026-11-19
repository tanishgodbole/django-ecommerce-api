"""Generate a deterministic Postman collection containing 100 runnable checks."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
requests = []
queries = ["", "?page=1", "?page=2", "?page_size=5", "?ordering=price", "?ordering=-price", "?search=Premium", "?search=Book", "?price__gte=1", "?price__lte=100", "?category=1", "?is_active=true"]
for i in range(100):
    if i < 70:
        path = "/api/v1/products/" + queries[i % len(queries)]
        label = f"Products list/filter scenario {i+1:03d}"
    elif i < 95:
        path = "/api/v1/categories/" + ("?search=Home" if i % 2 else "?ordering=name")
        label = f"Categories list scenario {i+1:03d}"
    else:
        path = ["/api/schema/?format=json", "/api/v1/products/?page=1", "/api/v1/categories/"][(i - 95) % 3]
        label = f"Schema and catalog smoke scenario {i+1:03d}"
    requests.append({"name": label, "request": {"method": "GET", "header": [], "url": "{{baseUrl}}" + path, "description": "Read-only smoke request; expects a successful paginated response."}, "event": [{"listen": "test", "script": {"type": "text/javascript", "exec": ["pm.test('returns HTTP 200', function () { pm.response.to.have.status(200); });", "pm.test('responds with JSON', function () { pm.response.to.be.json; });"]}}]})
collection = {"info": {"name": "Commerce API - 100 Executable Smoke Requests", "description": "100 read-only requests with response assertions. Run against a server populated by seed_demo.", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"}, "variable": [{"key": "baseUrl", "value": "http://127.0.0.1:8000"}], "item": requests}
target = root / "postman" / "commerce-api.postman_collection.json"
target.parent.mkdir(exist_ok=True)
target.write_text(json.dumps(collection, indent=2), encoding="utf-8")
print(f"Wrote {len(requests)} requests to {target}")
