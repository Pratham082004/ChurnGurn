from datetime import datetime
from app.extensions import db
from app.models.base import UUIDMixin

class Customer(UUIDMixin, db.Model):
    __tablename__ = "customers"

    company_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("companies.id"),
        nullable=False
    )

    external_customer_id = db.Column(db.String(100))
    attributes = db.Column(db.JSON, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
