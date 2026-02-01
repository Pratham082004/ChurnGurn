from datetime import datetime
from app.extensions import db
from app.models.base import UUIDMixin

class Prediction(UUIDMixin, db.Model):
    __tablename__ = "predictions"

    company_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("companies.id"),
        nullable=False
    )
    customer_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("customers.id"),
        nullable=False
    )

    churn_probability = db.Column(db.Float, nullable=False)
    risk_level = db.Column(db.String(20))
    model_version = db.Column(db.String(50))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
