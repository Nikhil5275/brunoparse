"""Performance Pod Tools - Person 2"""
from google.cloud import bigquery
from config.settings import PROJECT_ID, BQ_DATASET

client = bigquery.Client(project=PROJECT_ID)


def query_stars_performance(measure: str, contract: str, year: int = 2025) -> dict:
    """Query current HEDIS/STARs performance from BigQuery."""
    query = """
    SELECT measure_code, rate, star_rating, numerator, denominator
    FROM `{project}.{dataset}.stars_performance`
    WHERE measure_code = @measure
      AND contract_id = @contract
      AND year = @year
    """.format(project=PROJECT_ID, dataset=BQ_DATASET)

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("measure", "STRING", measure),
            bigquery.ScalarQueryParameter("contract", "STRING", contract),
            bigquery.ScalarQueryParameter("year", "INT64", year),
        ]
    )

    result = client.query(query, job_config=job_config).to_dataframe()

    if result.empty:
        return {"error": f"No data for measure={measure}, contract={contract}, year={year}"}

    row = result.iloc[0].to_dict()
    row["source"] = f"stars_performance, contract={contract}"
    return row


def compute_star_gap(current_rate: float, measure: str, target_star: int) -> dict:
    """Calculate gap between current rate and target star threshold."""
    from config.cms_thresholds import STAR_THRESHOLDS

    if measure not in STAR_THRESHOLDS:
        return {"error": f"Unknown measure: {measure}"}
    if target_star not in STAR_THRESHOLDS[measure]:
        return {"error": f"Invalid target_star: {target_star}"}

    thresholds = STAR_THRESHOLDS[measure]
    target_threshold = thresholds[target_star]
    gap = target_threshold - current_rate

    current_star = 1
    for star in sorted(thresholds.keys()):
        if current_rate >= thresholds[star]:
            current_star = star

    return {
        "measure": measure,
        "current_rate": current_rate,
        "current_star": current_star,
        "target_star": target_star,
        "target_threshold": target_threshold,
        "gap_percentage_points": round(gap, 3),
        "needs_improvement": gap > 0,
        "source": f"cms_thresholds, measure={measure}",
    }


def query_benchmark_comparison(measure: str, year: int = 2025) -> dict:
    """Compare performance across all contracts for a measure."""
    query = """
    SELECT
        contract_id,
        rate,
        star_rating,
        RANK() OVER (ORDER BY rate DESC) AS rank
    FROM `{project}.{dataset}.stars_performance`
    WHERE measure_code = @measure
      AND year = @year
    ORDER BY rate DESC
    """.format(project=PROJECT_ID, dataset=BQ_DATASET)

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("measure", "STRING", measure),
            bigquery.ScalarQueryParameter("year", "INT64", year),
        ]
    )

    result = client.query(query, job_config=job_config).to_dataframe()

    if result.empty:
        return {"error": f"No benchmark data for measure={measure}"}

    return {
        "measure": measure,
        "year": year,
        "total_contracts": len(result),
        "top_rate": float(result["rate"].max()),
        "avg_rate": round(float(result["rate"].mean()), 3),
        "records": result.to_dict("records"),
        "source": f"stars_performance, measure={measure}",
    }


def forecast_star_trend(measure: str, contract: str) -> dict:
    """Forecast next year's rate using linear trend over historical data."""
    query = """
    SELECT year, rate, star_rating
    FROM `{project}.{dataset}.stars_performance`
    WHERE measure_code = @measure
      AND contract_id = @contract
    ORDER BY year ASC
    """.format(project=PROJECT_ID, dataset=BQ_DATASET)

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("measure", "STRING", measure),
            bigquery.ScalarQueryParameter("contract", "STRING", contract),
        ]
    )

    result = client.query(query, job_config=job_config).to_dataframe()

    if len(result) < 2:
        return {"error": "Not enough historical data to forecast (need at least 2 years)"}

    rates = result["rate"].tolist()
    years = result["year"].tolist()
    avg_annual_change = (rates[-1] - rates[0]) / (len(rates) - 1)
    forecast_rate = round(rates[-1] + avg_annual_change, 3)

    return {
        "measure": measure,
        "contract": contract,
        "historical": [{"year": y, "rate": r} for y, r in zip(years, rates)],
        "avg_annual_change": round(avg_annual_change, 3),
        "forecast_next_year": forecast_rate,
        "trend": "improving" if avg_annual_change > 0 else "declining" if avg_annual_change < 0 else "flat",
        "source": f"stars_performance, contract={contract}",
    }