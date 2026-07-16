"""Clinical Operations Pod - Person 4"""
from google.adk import Agent
from .tools import query_care_gaps

clinical_pod = Agent(
    name="ClinicalPod",
    model="gemini-2.5-pro",
    instructions="""
    You are the Clinical Operations Pod.

    Your job:
    - Identify open care gaps
    - Interpret HEDIS specifications
    - Recommend clinical interventions

    Always cite: [Source: care_gaps, measure=CBP]
    """,
    tools=[query_care_gaps]
)
