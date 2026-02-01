from app.extensions import db
from app.models.base import UUIDMixin

class RiskTimeline(UUIDMixin, db.Model):
    __tablename__ = "risk_timelines"

    prediction_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("predictions.id"),
        nullable=False
    )

    churn_probability = db.Column(db.Float, nullable=False)
    recorded_at = db.Column(db.DateTime, server_default=db.func.now())
