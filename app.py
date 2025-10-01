# app.py
import datetime

from flask import Flask, request, jsonify, abort
from flask_mail import Mail, Message
from flask_apscheduler import APScheduler

from models import db, Flashcard
from schemas import ma, flashcard_schema, flashcards_schema


# ─── 1) Globale Erweiterungen ─────────────────────────────────────────────────
mail      = Mail()
scheduler = APScheduler()


# ─── 2) Scheduler-Job konfigurieren ────────────────────────────────────────────
class JobConfig:
    SCHEDULER_API_ENABLED = True
    JOBS = [
        {
            'id':      'daily_reminder',
            'func':    'app:send_reminders',
            'trigger': 'cron',
            'hour':    8,
            'minute':  0
        }
    ]


# ─── 3) Reminder-Funktion ───────────────────────────────────────────────────────
def send_reminders():
    """Wird täglich um 08:00 vom Scheduler aufgerufen."""
    today = datetime.date.today()
    due = Flashcard.query.filter(Flashcard.next_review <= today).all()

    if not due:
        print("[Reminder] Keine Karten fällig.")
        return

    # E-Mail aufbauen
    msg = Message(
        subject="Flashcards Review für heute",
        sender="dein@account.de",         # <== hier Deine Absender-Adresse
        recipients=["dein@account.de"]     # <== hier Deine Empfänger-Adresse(n)
    )
    msg.body = "\n".join(f"{c.question} → {c.answer}" for c in due)
    mail.send(msg)

    print(f"[Reminder] E-Mail gesendet: {len(due)} Karten fällig.")


# ─── 4) App-Factory ─────────────────────────────────────────────────────────────
def create_app():
    # 4.1) Flask init (serve static/index.html auf "/")
    app = Flask(__name__, static_folder='static', 
                          static_url_path='')

    # 4.2) Grund-Config laden (z.B. DB-URI, Marshmallow-Settings)
    app.config.from_object('config.Config')

    # 4.3) Scheduler job-Config
    app.config.from_object(JobConfig)

    # 4.4) Mail-Server konfigurieren (ersetze Beispiel-Werte!)
    app.config.update(
        MAIL_SERVER   = 'smtp.gmail.com',
        MAIL_PORT     = 587,
        MAIL_USE_TLS  = True,
        MAIL_USERNAME = 'volblank@gmail.com',
        MAIL_PASSWORD = 'Quickborn!150493'
    )

    # 4.5) Extensions initialisieren
    mail.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    # 4.6) Tabellen anlegen (falls noch nicht vorhanden)
    with app.app_context():
        db.create_all()

    # ───── Endpoints ────────────────────────────────────────────────────────────

    # 5) Frontend: index.html ausliefern
    @app.route('/')
    def homepage():
        return app.send_static_file('index.html')

    # 6a) Karte anlegen (POST /flashcards)
    @app.route('/flashcards', methods=['POST'])
    def add_card():
        data = request.get_json()
        if not data or 'question' not in data or 'answer' not in data:
            abort(400, 'Bitte question und answer mitgeben.')
        card = Flashcard(
            question=data['question'],
            answer=data['answer'],
            next_review=datetime.date.today()
        )
        db.session.add(card)
        db.session.commit()
        return flashcard_schema.jsonify(card), 201

    # 6b) Karten auflisten (GET /flashcards?page=&per_page=)
    @app.route('/flashcards', methods=['GET'])
    def list_cards():
        # robustes Parsen mit Typ-Coercion
        page     = request.args.get('page',    default=1,  type=int)
        per_page = request.args.get('per_page', default=20, type=int)

        paginated = Flashcard.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        cards = flashcards_schema.dump(paginated.items)

        return jsonify({
            'page':     page,
            'per_page': per_page,
            'total':    paginated.total,
            'cards':    cards
        })

    # 6c) Karte reviewen (PUT /flashcards/<id>)
    @app.route('/flashcards/<int:id>', methods=['PUT'])
    def review_card(id):
        card = Flashcard.query.get_or_404(id)
        card.next_review = datetime.date.today() + datetime.timedelta(days=1)
        db.session.commit()
        return flashcard_schema.jsonify(card)

    # 6d) Karte löschen (DELETE /flashcards/<id>)
    @app.route('/flashcards/<int:id>', methods=['DELETE'])
    def delete_card(id):
        card = Flashcard.query.get_or_404(id)
        db.session.delete(card)
        db.session.commit()
        return '', 204

    # 7) Debug: alle Routen ausgeben
    for rule in app.url_map.iter_rules():
        print(f"{rule.methods} → {rule.rule}  (endpoint: {rule.endpoint})")

    return app


# ─── 8) Server starten ─────────────────────────────────────────────────────────
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
# app.py
# Haupt-Datei: Initialisiert Flask und verbindet alle Teile
