from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
import pandas as pd
import uuid

from app.models.customer import Customer
from app.ml.model_loader import get_churn_model
from app.utlis.rbac import require_roles

predict_bp = Blueprint("predict", __name__)


@predict_bp.route("/customers", methods=["GET"])
@jwt_required()
@require_roles("ADMIN", "ANALYST")
def predict_customers():
    claims = get_jwt()
    company_id = uuid.UUID(claims["company_id"])

    customers = Customer.query.filter_by(company_id=company_id).all()

    if not customers:
        return jsonify({"error": "No customers found"}), 404

    rows = []
    ids = []

    for c in customers:
        attrs = c.attributes.copy()

        # remove churn if exists
        attrs.pop("churn", None)
        attrs.pop("customer_id", None)

        rows.append(attrs)
        ids.append(c.external_customer_id)

    df = pd.DataFrame(rows)

    model = get_churn_model()
    probs = model.predict_proba(df)[:, 1]

    results = [
        {
            "customer_id": ids[i],
            "churn_probability": round(float(probs[i]), 4)
        }
        for i in range(len(ids))
    ]

    return jsonify({
        "total_customers": len(results),
        "predictions": results
    }), 200


@predict_bp.route("/customer/<customer_id>", methods=["GET"])
@jwt_required()
@require_roles("ADMIN", "ANALYST")
def predict_single_customer(customer_id):
    claims = get_jwt()
    company_id = uuid.UUID(claims["company_id"])

    customer = Customer.query.filter_by(
        company_id=company_id,
        external_customer_id=customer_id
    ).first()

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    attrs = customer.attributes.copy()
    attrs.pop("churn", None)
    attrs.pop("customer_id", None)

    df = pd.DataFrame([attrs])

    model = get_churn_model()
    prob = model.predict_proba(df)[0][1]

    return jsonify({
        "customer_id": customer_id,
        "churn_probability": round(float(prob), 4)
    }), 200
