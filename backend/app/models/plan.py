from app.extensions import db
from app.models.base import UUIDMixin

class Plan(UUIDMixin, db.Model):
    __tablename__ = "plans"

    name = db.Column(db.String(50), nullable=False)

    prediction_limit = db.Column(db.Integer)
    api_limit = db.Column(db.Integer)
    alert_limit = db.Column(db.Integer)
