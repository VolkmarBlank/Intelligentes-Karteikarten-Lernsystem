# schemas.py
# =============================================================================
# Hier legen wir die Marshmallow-Schemas an,
# damit wir unsere Flashcard-Objekte sauber in JSON umwandeln können.
# =============================================================================

from flask_marshmallow import Marshmallow
from models import Flashcard

# 1) Marshmallow-Objekt erzeugen
ma = Marshmallow()

# -----------------------------------------------------------------------------
# 2) Schema für einzelne Flashcard
# -----------------------------------------------------------------------------
class FlashcardSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Flashcard      # welches Datenbank-Modell serialisiert wird
        load_instance = True   # aus JSON wieder ein Modell-Objekt erzeugen
        include_fk = True      # Fremdschlüssel mit ausgeben, falls nötig

# 3) Schema-Instanzen
flashcard_schema  = FlashcardSchema()        # für Einzel-Objekte
flashcards_schema = FlashcardSchema(many=True)  # für Listen von Objekten# schemas.py
# Hier legen wir Marshmallow-Schemas für JSON-Serialisierung an
