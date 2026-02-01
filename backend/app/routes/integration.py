# app/routes/integration.py

from flask import Blueprint, jsonify, request, g
from app.utlis.api_key_auth import require_api_key

integration_bp = Blueprint("integration", __name__)

@integration_bp.route("/predict", methods=["POST"])
@require_api_key
def predict_churn():
    data = request.get_json()

    # company_id comes from API key
    company_id = g.company_id

    # 🔧 Stub for now
    return jsonify({
        "company_id": str(company_id),
        "churn_probability": 0.82,
        "risk_level": "HIGH"
    })
