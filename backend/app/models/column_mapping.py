from app.extensions import db
from app.models.base import UUIDMixin
from datetime import datetime

class ColumnMapping(UUIDMixin, db.Model):
    __tablename__ = "column_mappings"

    company_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("companies.id"),
        nullable=False
    )

    mapping = db.Column(db.JSON, nullable=False)
    # example: { "cust_id": "customer_id", "months_active": "tenure" }

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
