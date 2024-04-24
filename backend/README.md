# Rasoi

<img src='web/public/icon-512.png' width="64">

_A social media for recipes 🍳._

[Logo Source](https://www.flaticon.com/free-icon/frying-pan_1222796?term=frying+pan&related_id=1222796)

> NOTE: all of the specifications given below are not finalized, may change if required.

## Backend for Rasoi

### Steps to run

- You need to install [pgvector](https://github.com/pgvector/pgvector) and postgres (ofcourse).
- Linux installation is straightforward mostly, just maybe some multiple postgres versions issue.
- The installer uses `pg_config` command internally, so make sure it returns detail for your current active postgres version only.

- for windows - things are ugly - you need to get full MSVC for C++ with windows (not the universal one - general windows dev) dev libraries
- for windows: my pc had "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" - check for respective thing in your pc, it will be needed for pgvector installation.

- (if you don't have poetry) `pip install poetry`
- `poetry install`
- `poetry run pip install tensorflow`
- `poetry run python -m app.extra_recipes`
- `poetry run python -m app.ingredients_food_com`
- `poetry run python -m app.init_db`
- create a database called `rasoi3`
- `poetry run python -m app.main`

These steps aren't thoroughly checked, may go wrong, use your developer mind to debug!
