# static/config.py  (in Deinem Projekt‐Wurzelverzeichnis, neben app.py)

import os

# Basis‐Verzeichnis ermitteln
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # 1) Pfad zur SQLite-Datenbank (wird im Projektordner angelegt)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'flashcards.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 2) (Optional) Secret Key für Sessions, CSRF usw.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'geheim')

    # 3) Mail‐Defaults (falls Du Flask-Mail nutzt)
    # MAIL_SERVER   = 'smtp.example.com'
    # MAIL_PORT     = 587
    # MAIL_USE_TLS  = True
    # MAIL_USERNAME = 'dein@account'
    # MAIL_PASSWORD = 'deinPasswort'
# config.py
# Konfigurations-Datei: Einstellungen (Datenbank-URL, Debug-Mode)
