from app.extensions import db
from app.models.base import UUIDMixin

class ChurnDriver(UUIDMixin, db.Model):
    __tablename__ = "churn_drivers"

    prediction_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("predictions.id"),
        nullable=False
    )

    feature_name = db.Column(db.String(100), nullable=False)
    impact_score = db.Column(db.Float, nullable=False)
