def normalize_churn(row, churn_def):
    """
    row: dict (CSV row after mapping)
    churn_def: dict (churn definition from frontend)
    """

    if not churn_def:
        return None  # prediction-only mode

    column = churn_def.get("column")
    value = row.get(column)

    churn_type = churn_def.get("type")

    if churn_type == "boolean":
        true_values = churn_def.get("true_values", [])
        return int(value in true_values)

    if churn_type == "categorical":
        churn_values = churn_def.get("churn_values", [])
        return int(value in churn_values)

    if churn_type == "date":
        return int(value not in [None, "", "null"])

    return None
