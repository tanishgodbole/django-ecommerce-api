# Commerce API

Interview-ready Django REST API for a small online shop. It includes email/password registration, JWT access and refresh, a staff-managed product catalog, per-user carts, transactional checkout/cancellation, OpenAPI docs, deterministic seed data, and automated tests.

## Run locally

Requires Python 3.11+ (3.14 has not been validated) and PostgreSQL 15+ for the production-style configuration. SQLite is selected automatically when `DB_HOST` is unset, which makes local tests easy.

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo --seed 2026
python manage.py runserver
```

Set database variables from `.env` in your shell or use `docker compose up -d db` first. Swagger UI is at `/api/docs/`, ReDoc at `/api/redoc/`, and the OpenAPI schema at `/api/schema/`.

## Verify

```powershell
python manage.py check
python manage.py test --verbosity 2
```

Test output is written to `reports/test-report.txt` after the verification script is run. Postman collection: `postman/commerce-api.postman_collection.json`; set `baseUrl`, then obtain a token and use the `accessToken` variable. Product/category writes require a staff JWT. Collection includes 100 executable requests with status assertions, suitable for Postman Collection Runner or Newman.

## API overview

All application routes use `/api/v1/`. Public routes: register, login, refresh, category/product list/detail. Authenticated routes: profile, cart, cart items, order checkout/list/detail/cancel. Product/category mutations require staff. Routes are paginated; products support `search`, `ordering`, `category`, `price__gte`, and `price__lte` filters.

### Operational notes

Set a high-entropy `SECRET_KEY`, `DEBUG=0`, strict `ALLOWED_HOSTS`, HTTPS, and real PostgreSQL credentials in deployment. JWT access lasts 15 minutes; refresh lasts 7 days and rotates. This demo intentionally omits payment, shipping, tax, address, email verification, and idempotency-key processing. For production, add those workflows, refresh-token revocation/blacklisting, audit logging, and rate-limit tuning.
