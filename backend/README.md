# Xingyu Backend

FastAPI backend for the Xingyu poetry mini program.

## Run

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

- API: `http://127.0.0.1:8000/api/v1/health`
- Docs: `http://127.0.0.1:8000/docs`

The app creates SQLite tables and seed data on startup in development mode.

## Test

```bash
pytest
```

## Environment

Copy `.env.example` to `.env` if custom configuration is needed. Environment variables override defaults.
