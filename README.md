# Intelligentes Karteikarten-Lernsystem (Flask)

Dieses Repo enthält deine bestehende App **ohne Änderungen der Inhalte** – nur bereinigt für das Hosting.

## Start lokal
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export FLASK_ENV=production
python -c "import app; app.create_app().run(host='0.0.0.0', port=5000)"
# oder
gunicorn 'app:create_app()' -b 0.0.0.0:5000
```

Dann im Browser: http://localhost:5000

## Deploy auf Render (empfohlen)
1. Dieses Repo zu GitHub pushen.
2. Auf https://render.com → **New Web Service** → GitHub-Repo wählen.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn 'app:create_app()'`
5. Region & Free Tier wählen → Create Web Service.

## Struktur
- `app.py` – Flask App Factory `create_app()` inkl. Static-Serving von `static/index.html`
- `static/` – Frontend (dein bestehendes HTML/CSS/JS)
- `models.py`, `schemas.py`, `config.py`, `routes.py` – Backend/DB/API
- `requirements.txt` – Python-Abhängigkeiten
- `Procfile` – Startkommando für Render/Heroku
- `.gitignore` – schließt venv/ und lokale Artefakte aus

> Hinweis: Deine ursprünglichen **Sicherung**-Ordner und **venv** wurden entfernt, damit das Repo schlank bleibt.
