# models.py
# =============================================================================
# Hier definieren wir unsere Datenbank-Modelle mit SQLAlchemy.
# Jede Klasse ist später eine Tabelle in der Datenbank.
# =============================================================================

from flask_sqlalchemy import SQLAlchemy

# 1) Datenbank-Objekt anlegen
db = SQLAlchemy()

# ------------------------------------------------------------------------
# 2) Flashcard-Modell – unsere zentrale Tabelle "flashcards"
#    Jetzt mit owner_id als ForeignKey auf users.id
# ------------------------------------------------------------------------
class Flashcard(db.Model):
    __tablename__ = 'flashcards'
    
    id = db.Column(db.Integer, primary_key=True)            # Primärschlüssel
    question = db.Column(db.String(256), nullable=False)    # Frage-Text
    answer   = db.Column(db.String(256), nullable=False)    # Antwort-Text
    next_review = db.Column(db.Date, nullable=False)        # Nächstes Review-Datum

    # NEU: Verknüpfung zu User über ForeignKey
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),   # verweist auf users.id
        nullable=True               # optional, falls Karte keinem User gehört
    )
    
    def __repr__(self):
        return f"<Flashcard {self.id}: {self.question[:20]}...>"

# ------------------------------------------------------------------------
# 3) User-Modell – Tabelle "users"
# ------------------------------------------------------------------------
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username     = db.Column(db.String(64), unique=True, nullable=False)
    email        = db.Column(db.String(120), unique=True, nullable=False)
    password_hash= db.Column(db.String(128), nullable=False)

    # Beziehung: Ein User kann viele Flashcards besitzen
    flashcards = db.relationship(
        'Flashcard',
        backref='owner',  # über flashcard.owner greifst du auf den User
        lazy=True
    )

    def __repr__(self):
        return f"<User {self.username}>"

