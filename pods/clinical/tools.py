"""Clinical Pod Tools - Person 4"""
from google.cloud import bigquery
from config.settings import PROJECT_ID, BQ_DATASET

client = bigquery.Client(project=PROJECT_ID)

def query_care_gaps(measure: str, contract: str = "H1234", limit: int = 100):
    """Query open care gaps

    Args:
        measure: Measure code
        contract: Contract ID
        limit: Max gaps to return

    Returns:
        dict with total_open_gaps and top_priority_members
    """
    query = f"""
    SELECT
        member_id,
        measure_code,
        gap_status,
        days_open,
        closure_likelihood_score
    FROM `{PROJECT_ID}.{BQ_DATASET}.care_gaps`
    WHERE measure_code = '{measure}'
      AND gap_status = 'open'
      AND contract_id = '{contract}'
    ORDER BY closure_likelihood_score DESC
    LIMIT {limit}
    """

    result = client.query(query).to_dataframe()

    return {
        "total_open_gaps": len(result),
        "top_priority_members": result.head(10).to_dict('records')
    }
