# AGENTS.md

FastAPI backend for simon-neidig.eu. Stack: FastAPI + SQLAlchemy 2 (async) + Alembic + asyncpg, Python 3.14, `fastapi-users` for auth, pydantic v2.

## Commands

- Run dev server: `uvicorn app.main:app --reload` (app entrypoint is `app/main.py`).
- Config lives in `.env` (gitignored; copy from `.env.example`). App reads `DB_CONNECTION` (async asyncpg URL) + `SECRET_KEY` in `app/core/config.py`.
- DB is a local Postgres via docker (`docker run ... -p 127.0.0.1:5432:5432 postgres`) — a real DB must be up for the app and for migrations.
- Migrations: `alembic revision --autogenerate -m "msg"` then `alembic upgrade head` (see "Migrations" below).

## Architecture

- Layered: `app/api/routes/<domain>/` (thin HTTP layer) → `app/services/` → `app/db/queries/` (async SQLAlchemy `select`) → `app/db/models/`. Pydantic schemas in `app/schemas/`. Keep business logic out of routers.
- **New routers are NOT auto-discovered**: every router must be imported and added via `app.include_router(...)` in `app/main.py` (routes also use `fastapi_users` auth/register/reset/verify + users routers). Router prefix/tags are declared in the `APIRouter(...)` call in each domain file.
- i18n (de/en/fr): `get_language` dependency in `app/services/i18n.py` reads the `Accept-Language` header, default "en". Localized content lives in `<model>_translation` tables (joined by `iso639_1`); queries in `app/db/queries/*` return only the requested language. Static strings are in `app/resources/strings.py`.
- Auth: `fastapi-users`. Admin-only endpoints depend on `get_current_superuser = fastapi_users.current_user(superuser=True)`; public routes omit it.
- Style: every module has a detailed docstring header with author info. Follow the existing docstring + import-order style in neighboring files.

## Migrations

- Alembic reads a **sync** psycopg2 `sqlalchemy.url` from `alembic.ini` (gitignored), while the app uses the **async** asyncpg URL from `.env`. Both are untracked; the committed templates are `alembic.ini.example` / `.env.example`. CI copies the `.example` files over and injects `DB_TEST_PWD`.
- `app/db/alembic/env.py` dynamically imports every module under `app.db.models`, so new models are auto-picked-up; no manual import in env.py needed.
- Always run `alembic upgrade head` against a real DB after generating a revision.

## Testing

- No pytest: quality is gated by **Postman black-box tests**. Collection + environment are stored in `.postman/` and `collections/postman/environments/*.yaml`.
- CI flow (`.github/workflows/test.yaml`, on any push): boot postgres service → `alembic upgrade head` → seed test users via `scripts/create_test_users.sql` (test@/nonadmin@simon-neidig.eu) → `fastapi run app/main.py --port 8000` → run cloud collection via `postman collection run` (needs `POSTMAN_TOKEN`, `DB_TEST_PWD` secrets). The collection/environment are identified by hardcoded Postman-cloud IDs in that file.
- Local Postman: import `.postman/*.postman_collection.json` + an environment, or `newman run ... -e ...` against a running server. New/modified endpoints should be mirrored in the collection.

## Spec & deploy

- OpenAPI spec is code-first, committed at `spec/openapi.json`. Regenerate with `python scripts/generate_openapi.py` while the server runs on `localhost:8000` (note: directory is `spec/`, not `specs/`).
- `Dockerfile` entrypoint is `fastapi run app/main.py --port 80` on `python:3.14-slim`. `.github/workflows/build.yaml` pushes `ghcr.io/neidigsi/simonneidig_fastapi:latest` on push to `main`.