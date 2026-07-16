"""Pod Router Agent - Person 1"""
from google.adk import Agent

router_agent = Agent(
    name="PodRouter",
    model="gemini-2.0-flash",
    instructions="""
    You are the Pod Router. Analyze the query and route to relevant pods.

    Routing rules:
    - Performance metrics (rates, trends, benchmarks) → Performance Pod
    - Segmentation, interventions → Engagement Pod
    - Care gaps, HEDIS questions → Clinical Pod
    - Always route to Compliance Pod last for validation

    For complex queries, route to multiple pods.

    Output format: List which pods to call.
    """,
    tools=[]  # Will add transfer_to_agent later
)
