from datetime import datetime
from app.extensions import db
from app.models.base import UUIDMixin

class AlertEvent(UUIDMixin, db.Model):
    __tablename__ = "alert_events"

    alert_rule_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("alert_rules.id"),
        nullable=False
    )
    prediction_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("predictions.id"),
        nullable=False
    )

    channel = db.Column(db.String(20))   # EMAIL / WEBHOOK
    status = db.Column(db.String(20))    # SENT / ACK / RESOLVED

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
