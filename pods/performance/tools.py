"""Performance Pod Tools - Person 2"""
from google.cloud import bigquery
from config.settings import PROJECT_ID, BQ_DATASET

client = bigquery.Client(project=PROJECT_ID)


def query_stars_performance(measure: str, contract: str = None, year: int = 2026) -> dict:
    """Query current HEDIS/STARs performance from BigQuery."""
    query = """
    SELECT measure_id, measure_name, plan_rate_pct, current_star_rating,
           members_compliant, members_eligible, gap_count, at_risk, trending
    FROM `{project}.{dataset}.stars_performance`
    WHERE measure_id = @measure
      AND measurement_year = @year
    """.format(project=PROJECT_ID, dataset=BQ_DATASET)

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("measure", "STRING", measure),
            bigquery.ScalarQueryParameter("year", "INT64", year),
        ]
    )

    result = client.query(query, job_config=job_config).to_dataframe()

    if result.empty:
        return {"error": f"No data for measure={measure}, year={year}"}

    row = result.iloc[0].to_dict()
    row["source"] = f"stars_performance, measure={measure}"
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


def query_benchmark_comparison(measure: str, year: int = 2026) -> dict:
    """Compare benchmark thresholds for a measure."""
    query = """
    SELECT measure_id, measure_name, plan_rate_pct, current_star_rating,
           benchmark_2star_pct, benchmark_3star_pct, benchmark_4star_pct, benchmark_5star_pct
    FROM `{project}.{dataset}.stars_performance`
    WHERE measure_id = @measure
      AND measurement_year = @year
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

    row = result.iloc[0].to_dict()
    return {
        "measure": measure,
        "year": year,
        "plan_rate_pct": row.get("plan_rate_pct"),
        "current_star_rating": row.get("current_star_rating"),
        "benchmarks": {
            "2_star": row.get("benchmark_2star_pct"),
            "3_star": row.get("benchmark_3star_pct"),
            "4_star": row.get("benchmark_4star_pct"),
            "5_star": row.get("benchmark_5star_pct"),
        },
        "source": f"stars_performance, measure={measure}",
    }


def forecast_star_trend(measure: str, contract: str = None) -> dict:
    """Forecast next year's rate using linear trend over historical data."""
    query = """
    SELECT measurement_year, plan_rate_pct, current_star_rating
    FROM `{project}.{dataset}.stars_performance`
    WHERE measure_id = @measure
    ORDER BY measurement_year ASC
    """.format(project=PROJECT_ID, dataset=BQ_DATASET)

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("measure", "STRING", measure),
        ]
    )

    result = client.query(query, job_config=job_config).to_dataframe()

    if len(result) < 2:
        return {"error": "Not enough historical data to forecast (need at least 2 years)"}

    rates = result["plan_rate_pct"].tolist()
    years = result["measurement_year"].tolist()
    avg_annual_change = (rates[-1] - rates[0]) / (len(rates) - 1)
    forecast_rate = round(rates[-1] + avg_annual_change, 3)

    return {
        "measure": measure,
        "historical": [{"year": y, "rate": r} for y, r in zip(years, rates)],
        "avg_annual_change": round(avg_annual_change, 3),
        "forecast_next_year": forecast_rate,
        "trend": "improving" if avg_annual_change > 0 else "declining" if avg_annual_change < 0 else "flat",
        "source": f"stars_performance, measure={measure}",
    }
