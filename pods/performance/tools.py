"""Performance Pod Tools - Person 2"""
from google.cloud import bigquery
from config.settings import PROJECT_ID, BQ_DATASET

client = bigquery.Client(project=PROJECT_ID)

def query_stars_performance(measure: str, contract: str, year: int = 2025):
    """Query current performance from BigQuery

    Args:
        measure: Measure code (e.g., 'CBP', 'CDC')
        contract: Contract ID (e.g., 'H1234')
        year: Year (default: 2025)

    Returns:
        dict with rate, star_rating, numerator, denominator
    """
    query = f"""
    SELECT measure_code, rate, star_rating, numerator, denominator
    FROM `{PROJECT_ID}.{BQ_DATASET}.stars_performance`
    WHERE measure_code = '{measure}'
      AND contract_id = '{contract}'
      AND year = {year}
    """

    result = client.query(query).to_dataframe()

    if result.empty:
        return {"error": f"No data for {measure}"}

    return result.to_dict('records')[0]


def compute_star_gap(current_rate: float, measure: str, target_star: int):
    """Calculate gap to target star threshold

    Args:
        current_rate: Current rate (0-1)
        measure: Measure code
        target_star: Target star level (2-5)

    Returns:
        dict with gap analysis
    """
    from config.cms_thresholds import STAR_THRESHOLDS

    target_threshold = STAR_THRESHOLDS[measure][target_star]
    gap = target_threshold - current_rate

    # Find current star
    current_star = 2
    for star in sorted(STAR_THRESHOLDS[measure].keys()):
        if current_rate >= STAR_THRESHOLDS[measure][star]:
            current_star = star

    return {
        "measure": measure,
        "current_rate": current_rate,
        "current_star": current_star,
        "target_star": target_star,
        "gap_percentage_points": round(gap, 3)
    }
