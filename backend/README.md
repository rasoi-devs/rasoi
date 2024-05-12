# Rasoi

<img src='web/public/icon-512.png' width="64">

_A social media for recipes 🍳._

[Logo Source](https://www.flaticon.com/free-icon/frying-pan_1222796?term=frying+pan&related_id=1222796)

## Backend for Rasoi

### Steps to run

- pgvector
    - You need to install [pgvector](https://github.com/pgvector/pgvector) and postgres (ofcourse).
    - Linux installation is straightforward mostly, just maybe some multiple postgres versions issue.
    - The installer uses `pg_config` command internally, so make sure it returns detail for your current active postgres version only.
    - for windows - things are ugly - you need to get full MSVC for C++ with windows (not the universal one - general windows dev) dev libraries
    - for windows: my pc had `C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat` - check for respective thing in your pc, it will be needed for pgvector installation.

- kaggle
    - To download datasets from kaggle, follow Kaggle's [authentication part](https://www.kaggle.com/docs/api#authentication).
    - While downloading dataset, there you may be prompted to do a `chmod`, do as instructed.

> Note that all python files contain some settings constants at the top, change them as per your requirements.

- dataset
    - (if you don't have poetry) `pip install poetry`
    - `poetry install`
    - `poetry run pip install tensorflow`
    - `poetry run python -m app.extra_recipes`
    - `poetry run python -m app.ingredients_food_com`
    - create a database called `rasoi3` in postgres
    - `poetry run python -m app.init_db` (you might need to extract some files in specific folder)


- run
    - dev: `poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
    - prod: `poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000`
    - for deployment in a server like ec2, use the server.txt file to get an idea.

These steps aren't thoroughly checked, may go wrong, use your developer mind to debug!


### Production deplyment (example)

> I have used [caddy](https://caddyserver.com/), instead of the commonly used [nginx](https://nginx.org/) for deployment and experimenting with a easily-configurable proxy server. The caddy file was of about 10 lines - simple.

```sql
create database rasoi3;
\c rasoi3
create extension vector;
```

```bash
# server is weak, just generate locally, then dump and upload and restore on server (use dbeaver or pg_dump for creating backup file)
psql -h localhost -U postgres -d rasoi3 < dump-rasoi3-202404251609.sql


# create two service unit files, so that it automatic restarts on reboot - good practice for deployment.

sudo nano /etc/systemd/system/rasoi-backend.service


[Unit]
Description=uvicorn rasoi backend
After=network.target
[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/git/rasoi/backend
Environment="PATH=/home/ubuntu/git/rasoi/backend/.venv/bin"
ExecStart=poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=on-failure
[Install]
WantedBy=multi-user.target


sudo nano /etc/systemd/system/rasoi-web.service

[Unit]
Description=next.js rasoi web frontend
After=network.target
[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/git/rasoi/web
ExecStart=/home/ubuntu/git/rasoi/web/start.bash
Restart=on-failure
[Install]
WantedBy=multi-user.target

sudo systemctl daemon-reload
sudo systemctl start rasoi-backend
sudo systemctl status rasoi-backend
sudo systemctl enable rasoi-backend

sudo systemctl daemon-reload
sudo systemctl start rasoi-web
sudo systemctl status rasoi-web
sudo systemctl enable rasoi-web

# to stop the server
sudo systemctl stop rasoi-backend
sudo systemctl stop rasoi-web

# logs
journalctl -u rasoi-backend.service
```