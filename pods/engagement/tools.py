"""Engagement Pod Tools - Person 3"""
from google.cloud import bigquery
from config.settings import PROJECT_ID, BQ_DATASET

client = bigquery.Client(project=PROJECT_ID)

def query_member_segments(
    measure: str,
    dimensions: list,
    plan_type: str = None
):
    """
    Query member segments with GROUP BY.
    """

    dimension_cols = ", ".join(dimensions)

    plan_filter = ""
    if plan_type:
        plan_filter = f"AND plan_type = '{plan_type}'"

    query = f"""
    SELECT
        {dimension_cols},
        SUM(members_eligible) AS members_eligible,
        SUM(members_compliant) AS members_compliant,
        SAFE_DIVIDE(
            SUM(members_compliant),
            SUM(members_eligible)
        ) * 100 AS compliance_rate_pct
    FROM `{PROJECT_ID}.{BQ_DATASET}.segment_performance`
    WHERE measure_id = '{measure}'
    {plan_filter}
    GROUP BY {dimension_cols}
    ORDER BY compliance_rate_pct ASC
    LIMIT 10
    """

    result = client.query(query).to_dataframe()

    if result.empty:
        return {
            "error": f"No segment data found for measure {measure}"
        }

    return result.to_dict("records")


def search_intervention_history(
    measure: str,
    year: int = 2024
):
    """
    Return most effective historical interventions.
    """

    query = f"""
    SELECT
        intervention_type,
        primary_channel,
        members_targeted,
        members_closed,
        closure_rate_pct,
        cost_per_closure_usd,
        total_cost_est_usd,
        notes
    FROM `{PROJECT_ID}.{BQ_DATASET}.historical_interventions`
    WHERE measure_id = '{measure}'
      AND intervention_year = {year}
    ORDER BY closure_rate_pct DESC
    LIMIT 5
    """

    result = client.query(query).to_dataframe()

    if result.empty:
        return {
            "error": f"No interventions found for {measure} in {year}"
        }

    return result.to_dict("records")