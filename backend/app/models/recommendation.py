from app.extensions import db
from app.models.base import UUIDMixin

class Recommendation(UUIDMixin, db.Model):
    __tablename__ = "recommendations"

    prediction_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("predictions.id"),
        nullable=False
    )

    type = db.Column(db.String(20))  # RULE / AI
    content = db.Column(db.Text, nullable=False)
