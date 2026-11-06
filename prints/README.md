# prints/ moved

The entire print pipeline (books + bookkit engine + kdp_preflight +
postcards + EDITIONS/PRICING) migrated to **`prx0r/bookfactory`** on
2026-11-06 — one repo for books.

- Canonical docs: `bookfactory/BOOKS.md` (system), `PIPELINE.md` (commands),
  `FACTORY-SPEC.md` (product law), `AGENTS.md` (entry point).
- Books: `bookfactory/prints/practical-prayers`, `bookfactory/prints/tantric-prayer`, ...
- Gate: `python3 bookfactory/check.py` (stage-aware; PDF build is the LAST stage).
- Renderer env: `BOOKFACTORY_PRINTS` (default `<repo>/prints`),
  `BOOKFACTORY_TRANSLATIONS` (translation-work checkout).

Nothing book-related remains in this repo. `~/visuals/outputs` (visuals/
storyboards, standard_cards) is untouched and still lives here.
