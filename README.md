# Campus Customs (HW4)

A Yale-themed apparel storefront: a React + Vite + TypeScript frontend, a FastAPI backend, and a PydanticAI chat agent that reads live product/price/stock data from a SQLite database.

## 1. Place the local data pack

The real database and product images are **not** included in this repo (see `.gitignore`). Before running anything, place the data pack you were given at:

```
data/
├── campus_customs.db
└── products/        # product images referenced by the catalogue
```

`data/` sits at the same level as `backend/` and `frontend/` (i.e. directly inside this repo's root).

## 2. Set up your API key

Copy `.env.example` to `.env` in this folder and fill in `PORTKEY_API_KEY`:

```bash
cp .env.example .env
```

`backend/agent.py` loads this `.env` automatically via `python-dotenv`.

## 3. Run the backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
uvicorn main:app --reload --port 8000
```

The API is now at `http://127.0.0.1:8000` (interactive docs at `/docs`).

## 4. Run the frontend

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

The site is now at `http://localhost:5174`, and expects the backend above at `http://127.0.0.1:8000`.

## Project layout

- `frontend/` — Vite + React + TypeScript site
- `backend/` — FastAPI app; the agent itself is `backend/agent.py`, `backend/models.py`, `backend/tools.py`, and `backend/prompts/prompt.md`
- `output/` — project documentation and deliverables: `harness.md`, `design.md`, `usability.md`, `app_check.html` (+ `app_check_images/`), `audit_trail.json`
- `AI_prompts.md` — log of prompts used to build this project, organized by problem number
