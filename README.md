# TaDV: Task-aware Data Validation

TaDV generates data quality constraints from **downstream task code** and a **CSV dataset** using LLMs. Given a Python script and dataset, it detects accessed columns, extracts per-column assumptions, and produces executable data unit tests.

## Prerequisites

- **Python** >= 3.11
- **Node.js** >= 20.11 and **npm** >= 10
- **[uv](https://docs.astral.sh/uv/)** (Python package manager)
- An API key for at least one LLM provider (OpenAI, Anthropic, or Gemini)

## Setup

### 1. Clone and install

```bash
git clone git@github.com:guangchen811/tadv-demo.git && cd tadv-demo

# Backend
uv sync --all-extras --group dev

# Frontend
cd frontend && npm install && cd ..
```

### 2. Configure environment

Create a `.env` file in the project root:

```bash
# Set at least one LLM API key
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...

# Optional: override default model
LLM_PROVIDER=openai        # openai | anthropic | gemini
LLM_MODEL=gpt-4o-mini
```

### 3. Run

```bash
./start.sh
```

This starts both servers:

| Service  | URL                        |
|----------|----------------------------|
| Frontend | http://localhost:3000       |
| Backend  | http://localhost:8000       |
| API Docs | http://localhost:8000/docs  |

Press `Ctrl+C` to stop both.

Alternatively, start them separately:

```bash
# Backend only
uv run uvicorn tadv.api.v1.app:app --reload --port 8000

# Frontend only (in another terminal)
cd frontend && npm run dev
```

## Usage

1. **Load data** — use the built-in quick example, browse DVBench benchmark datasets, or upload your own Python/SQL file + CSV.
2. **Run inference** — click the inference button to detect columns, then generate constraints.
3. **Review** — inspect assumptions and constraints in the right panel; view the provenance flow graph in the bottom panel.
4. **Export** — export constraints as Great Expectations, Deequ (Scala), or JSON.

## Project Structure

```
src/tadv/
  api/v1/
    routes/             # FastAPI endpoints
    schemas.py          # Pydantic API models (snake_case → camelCase)
  generation/
    orchestrator.py     # LLM pipeline: profile → detect columns → extract assumptions → generate constraints
  llm/
    factory.py          # LLM provider setup
  profiling/            # Dataset profiling

frontend/src/
  api/                  # API client
  components/           # React UI (Header, Editor, Sidebar, Dialogs)
  store/slices/         # Zustand state management
  types/                # TypeScript types

benchmarks/DVBench/    # Bundled benchmark datasets (5 datasets, 50+ scripts)
tests/                  # Backend tests
```

## Tests

```bash
# Unit tests
uv run pytest

# E2E with real LLM calls (requires API keys)
RUN_LLM_TESTS=1 uv run pytest tests/integration/test_api_e2e.py -v

# Frontend type check + build
cd frontend && npm run build
```

## Supported LLM Providers

| Provider  | Example models                                      |
|-----------|-----------------------------------------------------|
| OpenAI    | gpt-4o, gpt-4o-mini, gpt-4-turbo                   |
| Anthropic | claude-sonnet-4-6, claude-opus-4-6, claude-haiku-4-5 |
| Gemini    | gemini-2.5-flash, gemini-2.5-pro                    |
