from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from werkzeug.utils import secure_filename
import pandas as pd
import io
import uuid
import json

from app.extensions import db
from app.models.upload import Upload
from app.models.customer import Customer
from app.models.column_mapping import ColumnMapping
from app.utlis.rbac import require_roles
from app.utlis.churn_normalizer import normalize_churn
from app.utlis.canonical_fields import REQUIRED_FIELDS

upload_bp = Blueprint("upload", __name__)


# ============================
# FINAL CSV UPLOAD (WITH MAPPING + CHURN + UPSERT)
# ============================
@upload_bp.route("/csv", methods=["POST"])
@jwt_required()
@require_roles("ADMIN", "ANALYST")
def upload_csv():
    # ---------- Basic file checks ----------
    if "file" not in request.files:
        return jsonify({"error": "CSV file missing"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.lower().endswith(".csv"):
        return jsonify({"error": "Only CSV files are allowed"}), 400

    # ---------- Mapping & churn definition ----------
    mapping_json = request.form.get("mapping")
    churn_def_json = request.form.get("churn_definition")

    if not mapping_json:
        return jsonify({"error": "Column mapping missing"}), 400

    try:
        mapping = json.loads(mapping_json)
        churn_definition = json.loads(churn_def_json) if churn_def_json else None
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid mapping or churn definition JSON"}), 400

    # ---------- Auth context ----------
    claims = get_jwt()
    company_id = uuid.UUID(claims["company_id"])

    filename = secure_filename(file.filename)

    # ---------- Save upload record ----------
    upload = Upload(
        company_id=company_id,
        filename=filename,
        status="PROCESSING"
    )
    db.session.add(upload)
    db.session.commit()

    try:
        # ---------- Read CSV ----------
        stream = io.StringIO(file.stream.read().decode("utf-8"))
        df = pd.read_csv(stream)

        if df.empty:
            return jsonify({"error": "CSV is empty"}), 400

        # ---------- Apply column mapping ----------
        df = df.rename(columns=mapping)

        # ---------- Validate required fields ----------
        missing = [f for f in REQUIRED_FIELDS if f not in df.columns]
        if missing:
            return jsonify({
                "error": "Missing required fields after mapping",
                "missing_fields": missing
            }), 400

        # ---------- UPSERT customers + normalize churn ----------
        for _, row in df.iterrows():
            row_dict = row.to_dict()

            # 🔥 sanitize values for JSON storage
            for k, v in row_dict.items():
                if pd.isna(v):
                    row_dict[k] = None
                elif isinstance(v, pd.Timestamp):
                    row_dict[k] = v.isoformat()

            # ---------- Validate customer_id ----------
            if "customer_id" not in row_dict or not row_dict["customer_id"]:
                raise Exception("customer_id missing after mapping")

            # ---------- Normalize churn ----------
            churn_value = normalize_churn(row_dict, churn_definition)
            if churn_value is not None:
                row_dict["churn"] = churn_value

            external_id = str(row_dict["customer_id"])

            customer = Customer.query.filter_by(
                company_id=company_id,
                external_customer_id=external_id
            ).first()

            if customer:
                customer.attributes = row_dict
            else:
                customer = Customer(
                    company_id=company_id,
                    external_customer_id=external_id,
                    attributes=row_dict
                )
                db.session.add(customer)

        # ---------- Save mapping for reuse ----------
        column_mapping = ColumnMapping(
            company_id=company_id,
            mapping=mapping,
            churn_definition=churn_definition
        )
        db.session.add(column_mapping)

        upload.status = "COMPLETED"
        db.session.commit()

    except Exception as e:
        upload.status = "FAILED"
        db.session.commit()
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "message": "CSV uploaded successfully",
        "rows_processed": len(df)
    }), 201


# ============================
# CSV PREVIEW (FOR COLUMN MAPPING UI)
# ============================
@upload_bp.route("/csv/preview", methods=["POST"])
@jwt_required()
@require_roles("ADMIN", "ANALYST")
def preview_csv():
    if "file" not in request.files:
        return jsonify({"error": "CSV file missing"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.lower().endswith(".csv"):
        return jsonify({"error": "Only CSV files are allowed"}), 400

    try:
        stream = io.StringIO(file.stream.read().decode("utf-8"))
        df = pd.read_csv(stream)

        if df.empty:
            return jsonify({"error": "CSV is empty"}), 400

        return jsonify({
            "columns": list(df.columns),
            "sample_rows": df.head(5).to_dict(orient="records")
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
