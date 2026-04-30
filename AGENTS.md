# Repository Guidelines

## Project Structure & Module Organization

This is a Django 5 project for the Smart Mall web app. Project settings and entry points live in `config/` (`settings.py`, `urls.py`, `wsgi.py`, `asgi.py`). The main application is `core/`, with models, views, forms, admin registration, and URL routes. HTML templates are in `core/templates/`; app-specific CSS is in `core/static/core/css/`. Database migrations are stored in `core/migrations/`. Automated tests are under `core/tests/` and are configured through `pytest.ini`.

## Build, Test, and Development Commands

- `python -m venv .venv && source .venv/bin/activate`: create and activate a local virtual environment.
- `pip install -r requirements.txt`: install Django, pytest, Selenium, deployment, and image dependencies.
- `python manage.py migrate`: apply database migrations to the local SQLite database.
- `python manage.py runserver`: run the development server at `http://127.0.0.1:8000/`.
- `pytest`: run the configured test suite in `core/tests/`.
- `python manage.py collectstatic --no-input`: collect static assets for deployment.
- `./build.sh`: Render-style build script; installs dependencies, collects static files, migrates, and creates the default admin user if missing.

## Coding Style & Naming Conventions

Follow standard Django conventions and keep code close to the existing style. Use 4-space indentation in Python. Name models and forms with `PascalCase` (`Loja`, `ProdutoForm`) and functions/view helpers with `snake_case`. Group templates by domain, such as `core/templates/core/public/vitrine.html` or `core/templates/core/lojista/dashboard.html`. Keep CSS scoped by shared base files or page area in `core/static/core/css/`. Prefer explicit imports and avoid broad refactors when changing a single workflow.

## Testing Guidelines

Tests use `pytest`, `pytest-django`, and Selenium for end-to-end flows. `pytest.ini` sets `DJANGO_SETTINGS_MODULE=config.settings`, test discovery to `core/tests`, and the `test_*.py` naming pattern. Add tests beside related coverage, for example `core/tests/test_vitrine.py` for storefront behavior or `core/tests/test_auth.py` for login and registration. Run `pytest` before opening a pull request.

## Commit & Pull Request Guidelines

Recent history uses short Portuguese/English messages with uppercase type prefixes, especially `FIX:` and `UPDATE:`. Keep commits focused, for example `FIX: Corrige permissão do lojista` or `UPDATE: Ajusta vitrine de produtos`. Pull requests should describe the change, list test evidence, link the relevant Jira issue when available, and include screenshots or screencast links for UI changes.

## Security & Configuration Tips

Do not commit secrets, production credentials, uploaded media, or local database changes unless intentionally required. Keep environment-specific settings out of source control and verify deployment behavior through `build.sh` and Django migrations.
