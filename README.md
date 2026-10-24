# gaang — The Dallas Clearance Project

ITSS/OPRE 3312 squad repo.

## Layout

- `src/` — our Python modules
- `tests/` — pytest tests
- `data/` — raw input files (gitignored)
- `reports/` — outputs: CSVs, charts, maps

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest
```
