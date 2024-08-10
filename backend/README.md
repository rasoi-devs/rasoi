# Rasoi

<img src='../web/public/icon-512.png' width="64">

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
    - (if you don't have pipx) `sudo apt install pipx` - or similar command acc. to OS
    - (if you don't have poetry) `pipx install poetry`
    - cd into `<project root>/backend`
    - `poetry install`
    - `poetry run pip install tensorflow`
    - `poetry run python -m app.extra_recipes`
    - `poetry run python -m app.ingredients_food_com`
    - create a database called `rasoi3` in postgres
    - create pgvector extension to the database (`CREATE EXTENSION vector;`)
    - `poetry run python -m app.init_db`
        - Note: you might need to extract some files to specific folder.


- run
    - dev: `poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
    - prod: `poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000`

These steps aren't thoroughly checked, may go wrong, use your developer mind to debug!


### Production deplyment (example)

> Note: This is just a demo project, ofcourse **revealing server configuration might not be a good idea** in real-world production projects. These are just some notes for future reference - if I ever set up a server like this.

> Also, I would **love to be hacked** and learn something new out of it - **please do reach out to me** or **just raise an issue** if you could find a vulnerability in the server :)

> I have tried **[caddy](https://caddyserver.com/)**, but it might be unstable. The server stops to respond after a certain period. Better, use nginx.

```sql
create database rasoi3;
\c rasoi3
create extension vector;
```

```bash
# server is weak, just generate locally, then dump and upload and restore on server (use dbeaver or pg_dump for creating backup file)
psql -h localhost -U postgres -d rasoi3 < dump-rasoi3-202404251609.sql
# if you directly restore from the db backup, no ned to run init_db.py, for the most part
# also, just copy the extra_images_processed images to Food Images folder (if you don't run init_db.py)


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
ExecStart=/home/ubuntu/.local/bin/poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=on-failure
[Install]
WantedBy=multi-user.target


# chmod +x start.bash -> to web/start.bash
# also add **backend** server URL for image loading in web/next.conf.js

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

# Create nginx config for 2 proxy servers (:80, :90) for frontend and backend respectively.
server {
    listen 80;
    listen [::]:80;

    server_tokens off;

    location / {
        proxy_pass http://127.0.0.1:3000;
        include proxy_params;
    }
}

server {
    listen 90;
    listen [::]:90;

    server_tokens off;

    location / {
        proxy_pass http://127.0.0.1:8000;
        include proxy_params;
    }
}


# change frontend and backend endpoints in .env in web/ folder

# logs
journalctl -u rasoi-backend.service
```

### Troubleshoot
- `chmod +x start.bash` -> to `web/start.bash`.
- Check `.env`, set proper location.
- Also add **backend** server URL for image loading in web/next.conf.js