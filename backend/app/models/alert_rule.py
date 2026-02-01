from app.extensions import db
from app.models.base import UUIDMixin

class AlertRule(UUIDMixin, db.Model):
    __tablename__ = "alert_rules"

    company_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("companies.id"),
        nullable=False
    )

    min_probability = db.Column(db.Float, nullable=False)
    risk_level = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
