# app/seed.py

from app.extensions import db
from app.models.role import Role
from app.models.plan import Plan

def seed_roles_and_plans():
    roles = ["ADMIN", "ANALYST", "VIEWER"]

    for role_name in roles:
        if not Role.query.filter_by(name=role_name).first():
            db.session.add(Role(name=role_name))

    plans = [
        {
            "name": "FREE",
            "prediction_limit": 500,
            "api_limit": 1000,
            "alert_limit": 100
        },
        {
            "name": "STARTER",
            "prediction_limit": 5000,
            "api_limit": 10000,
            "alert_limit": 1000
        },
        {
            "name": "PRO",
            "prediction_limit": 50000,
            "api_limit": 100000,
            "alert_limit": 10000
        }
    ]

    for plan in plans:
        if not Plan.query.filter_by(name=plan["name"]).first():
            db.session.add(Plan(**plan))

    db.session.commit()
    print("✅ Roles & Plans seeded successfully")
