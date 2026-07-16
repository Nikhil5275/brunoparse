"""Engagement Pod Tools - Person 3"""
from google.cloud import bigquery
from config.settings import PROJECT_ID, BQ_DATASET

client = bigquery.Client(project=PROJECT_ID)

def query_member_segments(measure: str, dimensions: list, contract: str = "H1234"):
    """Query member segments with GROUP BY

    Args:
        measure: Measure code
        dimensions: List of columns to segment by (e.g., ['age_group', 'geography'])
        contract: Contract ID

    Returns:
        List of segment breakdowns
    """
    dimension_cols = ", ".join(dimensions)

    query = f"""
    SELECT
        {dimension_cols},
        COUNT(*) as member_count,
        AVG(compliant) as compliance_rate
    FROM `{PROJECT_ID}.{BQ_DATASET}.segment_performance`
    WHERE measure_code = '{measure}'
      AND contract_id = '{contract}'
    GROUP BY {dimension_cols}
    ORDER BY compliance_rate ASC
    LIMIT 10
    """

    result = client.query(query).to_dataframe()
    return result.to_dict('records')


def search_intervention_history(measure: str, year: int = 2024):
    """Get past intervention results

    Args:
        measure: Measure code
        year: Year to look at

    Returns:
        List of past interventions
    """
    query = f"""
    SELECT
        intervention_name,
        outcome_delta,
        population_size,
        cost_per_member,
        description
    FROM `{PROJECT_ID}.{BQ_DATASET}.historical_interventions`
    WHERE measure_code = '{measure}'
      AND year = {year}
    ORDER BY outcome_delta DESC
    LIMIT 5
    """

    result = client.query(query).to_dataframe()
    return result.to_dict('records')
