"""Clinical Pod Tools - Person 4"""
from google.cloud import bigquery
import os
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "qwiklabs-gcp-00-43ecffa89f51") 
BQ_DATASET = "humana_hackathon"

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
        gap_id,
        member_id,
        measure_id,
        measure_name,
        gap_status,
        due_date,
        last_service_date,
        outreach_attempts,
        care_gap_year
    FROM `{PROJECT_ID}.{BQ_DATASET}.care_gaps`
    WHERE measure_id = '{measure}'
      AND gap_status = 'open'
    ORDER BY due_date ASC, outreach_attempts ASC
    LIMIT {limit}
    """

    result = client.query(query).to_dataframe()

    if result.empty:
        return {
            "total_open_gaps": 0,
            "high_priority_gaps": [],
            "message": f"No open care gaps found for {measure}",
            "source": f"care_gaps, measure={measure}"
        }
    
    return {
        "total_open_gaps": len(result),
        "high_priority_gaps": result.head(10).to_dict('records'),
        "source": f"care_gaps, measure={measure}, year={result.iloc[0]['care_gap_year']}"
    }
