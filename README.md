# gaang — The Dallas Clearance Project

ITSS/OPRE 3312 squad repo.

## Layout

- `src/` — our Python modules (`intake.py`, `patterns.py`, `lockers.py`)
- `tests/` — pytest tests
- `data/` — raw input files
- `reports/` — outputs

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest
```

Run everything from the repo root.
