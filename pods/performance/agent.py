"""Performance Intelligence Pod - Person 2"""
from google.adk import Agent
from .tools import query_stars_performance, compute_star_gap

performance_pod = Agent(
    name="PerformancePod",
    model="gemini-2.0-flash",
    instructions="""
    You are the Performance Intelligence Pod.

    Your job:
    - Query current HEDIS/STARs rates
    - Calculate gaps to star thresholds
    - Compare to benchmarks
    - Forecast trends

    CRITICAL: Always cite sources like [Source: stars_performance, contract=H1234]
    """,
    tools=[query_stars_performance, compute_star_gap]
)
