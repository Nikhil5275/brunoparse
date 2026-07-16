"""Compliance & Evidence Pod - Person 5"""
from google.adk import Agent
from .tools import cross_check_citations

compliance_pod = Agent(
    name="CompliancePod",
    model="gemini-2.0-flash",
    instructions="""
    You are the Compliance & Evidence Pod.

    Your job:
    - Verify all numerical claims have citations
    - Check for PII leaks (member names, IDs)
    - Validate star rating thresholds

    Output: APPROVED or list of issues
    """,
    tools=[cross_check_citations]
)
