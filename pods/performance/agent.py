"""Performance Intelligence Pod - Person 2"""
from google.adk import Agent
from .tools import query_stars_performance, compute_star_gap, query_benchmark_comparison, forecast_star_trend

performance_pod = Agent(
    name="PerformancePod",
    instruction="""
    You are the Performance Intelligence Pod.
    
    Your job:
    - Query current HEDIS/STARs rates
    - Calculate gaps to star thresholds
    - Compare to benchmarks
    - Forecast trends
    
    CRITICAL: Always cite sources like [Source: stars_performance, measure=CBP]
    """,
    tools=[query_stars_performance, compute_star_gap, query_benchmark_comparison, forecast_star_trend]
)