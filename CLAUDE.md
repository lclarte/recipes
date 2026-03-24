# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Personal recipe website for two users. FastAPI backend with Jinja2 server-side templates and SQLite.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Create users (run before first login — there is no registration page)
python create_user.py <username> <password>

# Run dev server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run in production (on VPS/Pi)
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Setup

1. Copy `.env.example` to `.env` and set `SECRET_KEY` (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)
2. `alembic upgrade head` to create/migrate the DB
3. Create both users with `create_user.py`

## Database migrations (Alembic)

Schema is managed by Alembic — **do not use** `Base.metadata.create_all()`.

```bash
# Apply all pending migrations (run this on deploy)
alembic upgrade head

# After editing app/models.py — generate a new migration
alembic revision --autogenerate -m "add prep_time to recipes"
# Review the generated file in alembic/versions/, then:
alembic upgrade head

# Inspect state
alembic current    # current revision
alembic history    # full migration history
```

The DB URL comes from `settings.DATABASE_URL` in `env.py` — `alembic.ini` does not set it.

## Architecture

- `app/main.py` — App entry point: mounts `/static`, registers routers (DB schema managed by Alembic, not create_all)
- `app/config.py` — Settings via pydantic-settings, loaded from `.env`
- `app/models.py` — `User` and `Recipe` SQLAlchemy models
- `app/auth.py` — bcrypt password hashing + JWT creation/decoding
- `app/routers/auth.py` — `/login` (GET/POST) and `/logout`
- `app/routers/recipes.py` — Recipe CRUD; auth check via `get_current_user()` helper that returns `None` and triggers redirect instead of raising 401
- `app/templates/` — Jinja2 templates, all extend `base.html`
- `app/static/css/style.css` — All styles

## Key details

- Auth: JWT stored in an `httponly` cookie named `access_token`; no server-side session
- All routes redirect to `/login` when unauthenticated (no 401 JSON responses)
- IP whitelisting is planned but not yet implemented
